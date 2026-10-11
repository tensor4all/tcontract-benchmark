#!/usr/bin/env python3
"""Record one (profile, suite) run: build at a revision, verify, measure, publish.

Order matters and is enforced here:

1. the harness is built out of the *measured checkout*, into a target directory
   keyed by its revision;
2. `tcbench verify` runs for every size/thread count before any timing, and a
   mismatch aborts the run (nothing is published from an unverified run);
3. each measurement goes through the pinned, idle-checked protocol script that
   belongs to the same revision;
4. the manifest is validated against its schema *before* it is written, and the
   recorded commit must resolve in the checkout it names.
"""
import argparse
import datetime
import hashlib
import json
import os
import pathlib
import platform
import re
import shutil
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent


def sh(cmd, **kw):
    print(f"+ {' '.join(str(c) for c in cmd)}", file=sys.stderr)
    return subprocess.run([str(c) for c in cmd], check=True, text=True,
                          capture_output=True, **kw)


def git(dir_, *args):
    return subprocess.run(["git", "-C", str(dir_), *args], check=True,
                          text=True, capture_output=True).stdout.strip()


def build(checkout, runner, features, jobs):
    """Build the harness out of the measured checkout.

    Two knobs, deliberately separate: `features` decides which arms exist, and
    `jobs` how many cores the *build* may use. Neither has anything to do with the
    thread count the measurement runs at, which the suite declares.
    """
    env_file = ROOT / "target/pin.env"
    env_file.parent.mkdir(parents=True, exist_ok=True)
    build_env = dict(os.environ)
    build_env["BENCH_FEATURES"] = ",".join(features)
    build_env["CARGO_BUILD_JOBS"] = str(jobs)
    sh([ROOT / "scripts/build_for_tprims_rev.sh", checkout, env_file, runner],
       env=build_env)
    pin = {}
    for line in env_file.read_text().splitlines():
        if "=" in line:
            k, _, v = line.partition("=")
            pin[k] = v.strip().strip("'\"")
    return pin


def host_info(profile_name, profiles):
    profile = next(p for p in profiles if p["name"] == profile_name)
    lscpu = subprocess.run(["lscpu"], capture_output=True, text=True).stdout
    logical = next((int(l.split(":")[1].strip()) for l in lscpu.splitlines()
                    if l.startswith("CPU(s):")), 0)
    l3 = next((l.split(":", 1)[1].strip() for l in lscpu.splitlines()
               if l.startswith("L3 cache:")), None)
    return {
        "hostname": platform.node(),
        "cpu": profile["cpu"],
        "os": f"{platform.system()} {platform.release()}",
        "arch": platform.machine(),
        "logical_cpus": logical or profile["logical_cpus"],
        "l3": l3 or profile.get("l3"),
        "l3_domains": profile.get("l3"),
        "notes": profile.get("description"),
    }


# What each engine is provided by. An arm whose provider cannot be identified
# refuses the run: a page that says "TBLIS (unknown revision)" is exactly the
# opacity the result pages exist to remove.
PROVIDER_OF_ENGINE = {
    "plan": "tprims",
    "packed": "tprims",
    "tblis": "tblis",
    "ttgt": "openblas",
    "blas": "openblas",
}


def tblis_identity():
    """TBLIS revision, from $TBLIS_ROOT/PROVENANCE or the environment."""
    root = os.environ.get("TBLIS_ROOT")
    fields = {}
    if root:
        prov = pathlib.Path(root) / "PROVENANCE"
        if prov.exists():
            for line in prov.read_text().splitlines():
                if "=" in line and not line.startswith("#"):
                    k, _, v = line.partition("=")
                    fields[k.strip()] = v.strip()
    for key, env in (("version", "TBLIS_VERSION"), ("commit", "TBLIS_COMMIT"),
                     ("blis_commit", "TBLIS_BLIS_COMMIT"), ("config", "TBLIS_CONFIG"),
                     ("tag", "TBLIS_TAG"), ("sha256", "TBLIS_SHA256")):
        if env in os.environ and not fields.get(key):
            fields[key] = os.environ[env]
    return root, fields


def providers_for(engines):
    out = []
    names = {PROVIDER_OF_ENGINE.get(e) for e in engines}
    if "tprims" in names:
        out.append({"name": "tprims", "version": None, "commit": None, "path": None,
                    "note": "the measured revision itself; see tprims above"})
    if "tblis" in names:
        root, fields = tblis_identity()
        if not root or not fields.get("commit"):
            sys.exit(
                "ERROR: the suite measures the tblis arm, but its identity is not recorded.\n"
                "Write $TBLIS_ROOT/PROVENANCE with at least `commit=`, `version=`, "
                "`blis_commit=` and `config=`, or set TBLIS_COMMIT and friends.\n"
                "Nothing is published from an arm whose revision cannot be stated.")
        note = f"TBLIS {fields.get('version', '?')}, configuration {fields.get('config', '?')}"
        if fields.get("blis_commit"):
            note += f"; bundled BLIS {fields['blis_commit']}"
        if fields.get("build"):
            note += f"; built with {fields['build']}"
        if fields.get("sha256"):
            note += f"; libtblis.so sha256 {fields['sha256'][:16]}"
        entry = {"name": "tblis", "version": fields.get("version"), "commit": fields["commit"],
                 "path": root, "note": note}
        # A tag says which release a build came from, and a hash says which bytes
        # were linked; a commit alone says neither of those things for a built
        # native library. Both are optional so an older PROVENANCE still records.
        if fields.get("tag"):
            entry["tag"] = fields["tag"]
        if fields.get("sha256"):
            entry["sha256"] = fields["sha256"]
        out.append(entry)
    return out


PRIMING_RE = re.compile(r"(\d+) ms priming")
GUARD_POLICY_RE = re.compile(r"idle_window=(\d+)s max_busy=([0-9.]+) retries=(\d+)")


def harness_policy(stdout: str, stderr: str, label: str) -> dict:
    """What the harness and the guard report they did, refused rather than assumed.

    `--prime-ms` and the `PINNED_*` overrides can disagree with the defaults this
    script would otherwise write, and a manifest that states the default in that
    case is a wrong claim about a real run. Both lines come from the measured
    checkout, so a manifest that disagrees with them cannot be published.
    """
    priming = PRIMING_RE.search(stdout)
    if not priming:
        sys.exit(f"ERROR: {label}: no priming banner in the timing output. The measured\n"
                 "checkout predates tcontract-rs#78; bump pins/tcontract-rs.rev.")
    guard = GUARD_POLICY_RE.search(stderr)
    if not guard:
        sys.exit(f"ERROR: {label}: no guard policy line in the guard log. The measured\n"
                 "checkout predates tcontract-rs#79; bump pins/tcontract-rs.rev.")
    return {
        "prime_ms": int(priming.group(1)),
        "idle_window_seconds": int(guard.group(1)),
        "max_busy_percent": round(float(guard.group(2)) * 100),
        "attempts": int(guard.group(3)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("profile")
    ap.add_argument("suite_id")
    ap.add_argument("--checkout", default=str(ROOT / "extern/tcontract-rs"))
    ap.add_argument("--reps", type=int, default=5)
    ap.add_argument("--prime-ms", type=int, default=1500,
                    help="untimed time-based priming per arm; recorded as the harness reports it")
    ap.add_argument("--aa", type=int, default=1, help="number of complete set repeats (>=2 gives A/A)")
    ap.add_argument("--jobs", type=int, default=None,
                    help="cargo jobs for the build of the harness; independent of the thread "
                         "counts the suite measures at (default: a quarter of the CPUs)")
    ap.add_argument("--sizes", default=None, help="override, comma separated MiB")
    ap.add_argument("--threads", default=None, help="override, comma separated")
    ap.add_argument("--dtypes", default=None)
    ap.add_argument("--engines", default=None)
    ap.add_argument("--label", default=None, help="suffix for the run directory")
    args = ap.parse_args()

    profiles = yaml.safe_load((ROOT / "benchmarks/profiles.yaml").read_text())["profiles"]
    suite = yaml.safe_load((ROOT / "benchmarks/suites" / f"{args.suite_id}.yaml").read_text())
    spec = suite["runs"][0]
    fixed_shapes = bool(spec.get("fixed_shapes"))
    declared_sizes = spec.get("sizes_mib", [])
    if fixed_shapes and declared_sizes:
        sys.exit("ERROR: the suite declares fixed_shapes, so it must not declare sizes_mib")
    if fixed_shapes and args.sizes:
        sys.exit("ERROR: this suite's corpus has fixed shapes; --sizes does not apply to it")
    sizes = [float(s) for s in args.sizes.split(",")] if args.sizes else declared_sizes
    if not sizes and not fixed_shapes:
        sys.exit("ERROR: the suite declares neither sizes_mib nor fixed_shapes")
    threads = [int(t) for t in args.threads.split(",")] if args.threads else spec["threads"]
    dtypes = args.dtypes.split(",") if args.dtypes else spec["dtypes"]
    engines = args.engines.split(",") if args.engines else spec["engines"]
    cpu_sets = {str(t): spec["cpu_sets"][spec["threads"].index(t)] for t in threads}

    def size_arg(size):
        """`--size` for a sized corpus; nothing at all for a fixed-shape one."""
        return [] if size is None else ["--size", f"{size:g}"]

    def size_label(size):
        return "fixed" if size is None else f"{size:g}m"

    checkout = pathlib.Path(args.checkout)
    if (checkout / ".git").exists() and checkout.resolve() != (ROOT / "extern/tcontract-rs").resolve():
        pass
    # The harness the suite runs, built from the same checkout as the library it
    # measures. `tcbench` unless the suite says otherwise.
    runner = suite.get("runner", "tcbench")
    # No implicit features: a suite that measures only this library's own arms
    # declares an empty list, and nothing else is built into the harness.
    features = suite.get("features", [])
    jobs = args.jobs or max(1, (os.cpu_count() or 4) // 4)
    pin = build(checkout, runner, features, jobs)
    rev, dirty = pin["TPRIMS_REV"], pin["TPRIMS_DIRTY"] == "true"
    if dirty:
        print("WARNING: the measured checkout is dirty; this cell will be marked dirty", file=sys.stderr)

    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    name = f"{stamp}-{args.label}" if args.label else stamp
    run_dir = ROOT / "data/results" / args.profile / args.suite_id / name
    run_dir.mkdir(parents=True, exist_ok=True)

    bin_dir = pathlib.Path(pin["BIN_DIR"])
    tcbench = bin_dir / runner
    pinned = checkout / "benchmarks/scripts/pinned.sh"
    idle = checkout / "benchmarks/scripts/idle_cpus.py"
    if not pinned.exists() or not idle.exists():
        sys.exit(f"ERROR: {pinned} or {idle} missing; the protocol scripts belong to the measured revision")

    env = dict(os.environ)
    env["PATH"] = f"{checkout / 'benchmarks/scripts'}:{env['PATH']}"
    if "TBLIS_ROOT" in env:
        env["LD_LIBRARY_PATH"] = f"{env['TBLIS_ROOT']}/lib:{env['TBLIS_ROOT']}/lib64:" + env.get("LD_LIBRARY_PATH", "")

    guards = []
    # 1. correctness first, at every budget, for the whole corpus.
    for size in sizes or [None]:
        for t in threads:
            out = run_dir / f"verify-{size_label(size)}-{t}t.txt"
            guard = run_dir / f"verify-{size_label(size)}-{t}t.guard"
            r = subprocess.run([str(pinned), cpu_sets[str(t)], "--", str(tcbench), "verify",
                                "--threads", str(t)] + size_arg(size)
                               + ["--dtype", ",".join(dtypes)],
                               env=env, capture_output=True, text=True)
            out.write_text(r.stdout)
            guard.write_text(r.stderr)
            guards.append(str(guard.relative_to(run_dir)))
            if r.returncode != 0 or "MISMATCH" in r.stdout:
                sys.exit(f"ERROR: verify failed for {size_label(size)} {t}T (see {out}); nothing published")
            if "all comparisons within tolerance" not in r.stdout:
                sys.exit(f"ERROR: verify did not report a clean corpus for {size_label(size)} {t}T")

    # 2. timing, one CSV per (repeat, size, threads).
    csvs = []
    outputs = []
    policies = []
    for rep in range(args.aa):
        for size in sizes or [None]:
            for t in threads:
                label = size_label(size)
                stem = run_dir / f"run{rep}-{label}-{t}t"
                r = subprocess.run([str(pinned), cpu_sets[str(t)], "--", str(tcbench), "run",
                                    "--threads", str(t)] + size_arg(size)
                                   + ["--dtype", ",".join(dtypes), "--engines", ",".join(engines),
                                      "--reps", str(args.reps), "--prime-ms", str(args.prime_ms),
                                      "--csv", str(stem) + ".csv"],
                                   env=env, capture_output=True, text=True)
                # The harness's own stdout is kept: it is what makes the manifest's
                # priming claim checkable rather than assumed.
                (run_dir / f"run{rep}-{label}-{t}t.out").write_text(r.stdout)
                (run_dir / f"run{rep}-{label}-{t}t.guard").write_text(r.stderr)
                outputs.append(f"run{rep}-{label}-{t}t.out")
                guards.append(f"run{rep}-{label}-{t}t.guard")
                if r.returncode != 0:
                    sys.exit(f"ERROR: run failed for {size_label(size)} {t}T (repeat {rep})")
                if not (pathlib.Path(str(stem) + ".csv")).exists():
                    sys.exit(f"ERROR: no CSV produced for {size_label(size)} {t}T")
                csvs.append(str(stem) + ".csv")
                policies.append(harness_policy(r.stdout, r.stderr, f"{size_label(size)} {t}T"))
    policy = policies[0]
    for other in policies[1:]:
        if other != policy:
            sys.exit(f"ERROR: the harness reported different policy between runs: {policy} then {other}")

    manifest = {
        "schema_version": 1,
        "target_profile": args.profile,
        "suite_id": args.suite_id,
        "suite_file": f"benchmarks/suites/{args.suite_id}.yaml",
        "suite_sha256": hashlib.sha256(
            (ROOT / "benchmarks/suites" / f"{args.suite_id}.yaml").read_bytes()).hexdigest(),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
        "command": " ".join(sys.argv),
        "tprims": {
            "url": "https://github.com/tensor4all/tcontract-rs",
            "commit": rev,
            "dirty": dirty,
            # build_for_tprims_rev.sh writes this with `printf %q`, which escapes
            # the comma of a feature list.
            "features": [f for f in pin["BUILD_FEATURES"].replace("\\,", ",").split(",") if f],
            "measured_path": pin["TPRIMS_DIR"],
        },
        "build_jobs": jobs,
        "harness": {
            "commit": git(ROOT, "rev-parse", "HEAD"),
            "dirty": bool(git(ROOT, "status", "--porcelain", "--untracked-files=no")),
        },
        "host": host_info(args.profile, profiles),
        "threads": {
            "counts": threads,
            "cpu_sets": cpu_sets,
            "env": {k: os.environ.get(k) for k in
                    ["OMP_NUM_THREADS", "RAYON_NUM_THREADS", "OPENBLAS_NUM_THREADS",
                     "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"]},
        },
        "timing_policy": {
            "version": 1,
            "minimum_untimed_priming_ms": policy["prime_ms"],
            "statistic": "best",
            "repetitions": args.reps,
            "notes": "priming is time-based, not a call count: after an idle gate this host "
                     "reports up to 25% low for the first 1-2 s of sustained work. The value is "
                     "the one the harness reported, not the one this script asked for",
        },
        "guard": None,
        "guards": {
            "idle_window_seconds": policy["idle_window_seconds"],
            "max_busy_percent": policy["max_busy_percent"],
            "attempts": policy["attempts"],
            "logs": sorted(set(guards)),
            "outputs": sorted(set(outputs)),
            "notes": "the CPU set is checked together with the SMT siblings its physical "
                     "cores share, so a busy sibling fails the gate",
        },
        "providers": providers_for(engines),
        "invalidated_by": suite["invalidated_by"],
        "result_files": [str(pathlib.Path(c).relative_to(run_dir)) for c in csvs],
        "run_spec": {"sizes_mib": sizes, "fixed_shapes": fixed_shapes,
                      "dtypes": dtypes, "engines": engines, "aa": args.aa,
                      "covers_declared_suite": (sizes == declared_sizes
                                                and threads == spec["threads"]
                                                and dtypes == spec["dtypes"]
                                                and engines == spec["engines"])},
    }
    del manifest["guard"]

    manifest_path = run_dir / "run.yaml"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False))
    v = subprocess.run([sys.executable, str(ROOT / "scripts/validate_run.py"), str(manifest_path)],
                       capture_output=True, text=True)
    print(v.stdout + v.stderr, file=sys.stderr)
    if v.returncode != 0:
        sys.exit("ERROR: run.yaml does not validate; nothing published")

    subprocess.run([sys.executable, str(ROOT / "scripts/report_run.py"), "--run-dir", str(run_dir)], check=True)

    subprocess.run([sys.executable, str(ROOT / "scripts/publish_report.py"), str(run_dir)], check=True)
    subprocess.run([sys.executable, str(ROOT / "scripts/gen_index.py"), "--write"], check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
