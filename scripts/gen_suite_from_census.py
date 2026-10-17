#!/usr/bin/env python3
"""Turn the pinned harness's own census into a frozen timing-v2 suite declaration.

The census is the harness's declaration of the cell grid it covers: `verify` writes one
row per `(regime, family, dtype, order, m, n, k, batch, row, threads)` with a `status`
and a `note`, untimed and at the smallest setting. This script runs that census against
a built harness, folds it into a toolkit suite (one family per corpus case id, the
corpus group as the family group), and refuses to emit anything whose census does not
cover exactly the product the declaration would require a run to measure.

The generated file is committed and then frozen; nothing rebuilds it. Re-running the
script against the same binary emits a byte-identical file, so a diff is a real change
in the corpus or in the harness's census.

Usage:
    python3 scripts/gen_suite_from_census.py \
        --harness tcbench \
        --binary target/tcontract-rev/<rev>/release/tcbench \
        --revision 7738bf43a0684e7d6f0769444e846f215fec86ab \
        --out benchmarks/suites-v2/tcbench.yaml

The toolkit must be importable (it is pinned in `requirements.txt`); the declaration
check is the same `campaign_toolkit.timing_evidence.expected_cells` the recorder and the
validator use, not a re-implementation.
"""
from __future__ import annotations

import argparse
import csv
import pathlib
import shlex
import subprocess
import sys

import yaml

CENSUS_HEADER = ["regime", "family", "dtype", "order", "m", "n", "k",
                 "batch", "row", "threads", "status", "note"]

COMMON = dict(
    dtypes=["f64", "c64"],
    n="1",
    batch="1",
    threads=[1, 4],
    cpu_sets=["4", "4-7"],
    stale_after=20,
    optional_profiles=["zen5-cpu"],
)

HARNESSES = {
    "tcbench": dict(
        suite_id="tcbench",
        regime="tcbench",
        rows=["plan", "packed", "ttgt", "tblis"],
        # `blas` builds the OpenBLAS-backed `ttgt` engine and `tblis` the external
        # baseline; the suite's `features` is what the recorder exports as
        # `BENCH_FEATURES`, so both have to be named or the harness refuses the row.
        features=["blas", "tblis"],
        description=(
            "The TCCG 49-case tensor-contraction corpus, measured by `tcbench` out of the pinned "
            "`tcontract-rs` checkout. One family per case id. The declared identity shape is the "
            "numeric sentinel `n = 1`, a size spec rather than a matrix dimension: tcbench resolves "
            "its extents from a tensor-size target with rank-dependent rounding, so the resolved "
            "extents stay in the harness's own report and are not presented as geometry here."
        ),
        invalidated_by=[
            "crates/tcontract-kernel/**",
            "crates/tcontract/**",
            "crates/tcontract-exec/**",
            "benchmarks/benchmarks/tcbench/**",
            "benchmarks/src/**",
            "Cargo.toml",
            "Cargo.lock",
        ],
        workloads=dict(
            name="TCCG tensor-contraction corpus",
            description=(
                "One full tensor contraction per case, drawn from CCSD, CCSD(T), AO-to-MO "
                "integral transformation and tensor-times-matrix workloads. The cases are "
                "rank-3 to rank-6 contractions, so they exercise the packed driver's "
                "scatter path rather than a single matrix geometry."
            ),
            source=(
                "The corpus is defined by `benchmarks/benchmarks/tcbench/corpus.rs` in the "
                "measured revision (`pins/tcontract-rs-v2.rev`), after Springer & Bientinesi, "
                "\"Design of a High-Performance GEMM-like Tensor-Tensor Multiplication\" "
                "(arXiv:1607.00145) and the accompanying HPAC/tccg benchmark set."
            ),
            known_blind_spots=[
                "Every case is a full tensor contraction, not a matrix multiply; the declared "
                "`n` is a tensor-size spec, not a matrix dimension.",
                "Every case has unit batch, so a cost proportional to batch elements is invisible.",
                "`tblis` is an external baseline linked from its own prefix (`TBLIS_ROOT`, see "
                "`docs/v2-layout.md`), not the measured checkout; its revision is recorded through "
                "the campaign TBLIS collector (`scripts/tblis_providers_json.py`).",
                "The harness's census CSV carries no corpus `group` column and no resolved extents, "
                "so the corpus's own group labels and its resolved geometry are not part of this "
                "declaration; they remain facts of the recorded revision's `corpus.rs`.",
            ],
        ),
        engines_doc={
            "plan": dict(
                provider="tprims",
                summary="This library, with its planner choosing the route per case: the packed "
                        "driver, the copy-free faer path, or the elementwise path for an all-batch "
                        "case.",
                identity="the measured tcontract-rs revision in this run's manifest "
                         "(`library.commit`), pinned by `pins/tcontract-rs-v2.rev`",
            ),
            "packed": dict(
                provider="tprims",
                summary="This library with the packed driver forced instead of chosen. A diagnostic "
                        "arm: it shows what the planner's other routes buy or cost on the same inputs.",
                identity="the measured tcontract-rs revision in this run's manifest "
                         "(`library.commit`), pinned by `pins/tcontract-rs-v2.rev`",
            ),
            "ttgt": dict(
                provider="openblas",
                summary="Transpose-transpose-GEMM-transpose against the CBLAS-compatible BLAS the "
                        "harness linked: permute the operands into dense matrices, call GEMM, permute "
                        "the result back. An engine row, not a vendor arm.",
                identity="the OpenBLAS the harness linked, read from the harness's `info` output",
                caveat="The transposition is the naive gather, so this is an upper bound on TTGT's "
                       "cost rather than a tuned HPTT implementation.",
            ),
            "tblis": dict(
                provider="tblis",
                summary="Actual C++ TBLIS through the direct FFI adapter, as the independent "
                        "third-party reference implementation. Pinned by release tag, not by a local "
                        "revision: `benchmarks/scripts/build_tblis.sh` of the measured checkout "
                        "builds it from the tag and writes the PROVENANCE this repository records.",
                identity="TBLIS v2.0-beta2 (the only tagged 2.0; its commit and the bundled BLIS "
                         "revision are recorded per run, from `scripts/tblis_providers_json.py`)",
                caveat="Needs an install prefix (`TBLIS_ROOT`), and TBLIS 2.x builds through CMake, "
                       "so the prefix cannot be made inside a bare checkout. The page repeats the "
                       "tag, commit, bundled BLIS revision and artifact hash the manifest recorded.",
            ),
        },
    ),
    "per-shape": dict(
        suite_id="per-shape",
        regime="per-shape",
        rows=["plan", "packed", "tblis"],
        features=["tblis"],
        description=(
            "The 21-case per-shape contraction corpus, measured by `lukbench` out of the pinned "
            "`tcontract-rs` checkout. One family per case id. The cases are the shapes, so the "
            "declared identity shape is the numeric sentinel `n = 1`: a multi-step program (the "
            "MPS chain) has no single equivalent matrix shape, and the harness reports the final "
            "step's real extents in its own `case_m`/`case_n`/`case_k` columns. Each case fixes "
            "its own dtype, so the suite declares the whole rectangular f64 x c64 product and the "
            "harness reports the wrong-dtype cells as skipped."
        ),
        invalidated_by=[
            "crates/tcontract-kernel/**",
            "crates/tcontract/**",
            "crates/tcontract-exec/**",
            "benchmarks/benchmarks/lukbench/**",
            "benchmarks/src/**",
            "Cargo.toml",
            "Cargo.lock",
        ],
        workloads=dict(
            name="per-shape contraction set",
            description=(
                "Small and large batched GEMMs, a two-step chain and the steps of a 32-site MPS "
                "chain, at fixed extents. One timed call is the whole program (a chain of pairwise "
                "steps), not one step."
            ),
            source=(
                "The corpus is defined by `benchmarks/benchmarks/lukbench/corpus.rs` in the measured "
                "revision (`pins/tcontract-rs-v2.rev`); it carries the case definitions recorded "
                "from tensor4all/tcontract-rs#61."
            ),
            known_blind_spots=[
                "Each case fixes its own dtype (f64 or c64); the suite declares both, and lukbench's "
                "census reports the wrong-dtype cells as skipped rather than dropping the case.",
                "The declared identity is the numeric sentinel `n = 1`; the final step's real extents "
                "are the harness's own report, not the toolkit's identity.",
                "One size per case: a ratio here says nothing about a neighbouring size, and the set "
                "is not a sweep.",
                "`tblis` is an external baseline linked from its own prefix (`TBLIS_ROOT`, see "
                "`docs/v2-layout.md`), not the measured checkout; its revision is recorded through "
                "the campaign TBLIS collector (`scripts/tblis_providers_json.py`).",
                "The harness's census CSV carries no corpus `group` column, so the corpus's own "
                "group labels and each case's native dtype and final-step extents are not part of "
                "this declaration; they remain facts of the recorded revision's `corpus.rs`.",
            ],
        ),
        engines_doc={
            "plan": dict(
                provider="tprims",
                summary="This library with its planner choosing the route per case.",
                identity="the measured tcontract-rs revision in this run's manifest "
                         "(`library.commit`), pinned by `pins/tcontract-rs-v2.rev`",
            ),
            "packed": dict(
                provider="tprims",
                summary="This library with the packed driver forced. A diagnostic arm: it shows what "
                        "the planner's other routes buy or cost on the same inputs.",
                identity="the measured tcontract-rs revision in this run's manifest "
                         "(`library.commit`), pinned by `pins/tcontract-rs-v2.rev`",
            ),
            "tblis": dict(
                provider="tblis",
                summary="Actual C++ TBLIS through the direct FFI adapter, as the independent "
                        "third-party reference implementation. Pinned by release tag, not by a local "
                        "revision: `benchmarks/scripts/build_tblis.sh` of the measured checkout "
                        "builds it from the tag and writes the PROVENANCE this repository records.",
                identity="TBLIS v2.0-beta2 (the only tagged 2.0; its commit and the bundled BLIS "
                         "revision are recorded per run, from `scripts/tblis_providers_json.py`)",
                caveat="Needs an install prefix (`TBLIS_ROOT`), and TBLIS 2.x builds through CMake, "
                       "so the prefix cannot be made inside a bare checkout. The page repeats the "
                       "tag, commit, bundled BLIS revision and artifact hash the manifest recorded.",
            ),
        },
    ),
}


class Block(str):
    """A string emitted as a YAML block scalar, so generated prose stays readable."""


def block_representer(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:str", str(data), style="|")


yaml.add_representer(Block, block_representer, Dumper=yaml.SafeDumper)


def run_census(binary, harness, thread, args, out_path):
    """Run one untimed `verify` census pass and return the argv used."""
    spec = HARNESSES[harness]
    cmd = [str(binary), "verify",
           "--threads", str(thread),
           "--n", args.n,
           "--batch", args.batch,
           "--dtype", ",".join(args.dtypes),
           "--rows", ",".join(args.rows),
           "--regime", spec["regime"],
           "--census-csv", str(out_path)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit(f"ERROR: census failed at {thread}T (exit {proc.returncode})\n"
                 f"{proc.stdout[-2000:]}\n{proc.stderr[-2000:]}")
    if "all comparisons within tolerance" not in proc.stdout:
        sys.exit(f"ERROR: census at {thread}T did not report a clean grid; refusing to emit a "
                 f"suite from an unverified census")
    return cmd


def read_census(path):
    with open(path, newline="") as handle:
        reader = csv.DictReader(handle)
        missing = [c for c in CENSUS_HEADER if c not in (reader.fieldnames or [])]
        if missing:
            sys.exit(f"ERROR: {path}: census is missing the column(s) {missing}; expected at "
                     f"least {CENSUS_HEADER}. The harness's census contract changed.")
        rows = list(reader)
    for row in rows:
        if row["status"] not in ("ok", "skipped"):
            sys.exit(f"ERROR: {path}: census cell {row} has status {row['status']!r}; a suite is "
                     f"generated only from a census whose cells are all ok or skipped")
    return rows


def _cpu_set_for(thread):
    """The declared CPU set for one thread budget, from the repository's current suites."""
    if thread not in COMMON["threads"]:
        sys.exit(f"ERROR: no declared CPU set for a {thread}T budget; add it to COMMON")
    return COMMON["cpu_sets"][COMMON["threads"].index(thread)]


def build_suite(harness, args, rows):
    spec = HARNESSES[harness]
    families = {}
    for row in rows:
        # The census CSV of the pinned harness carries no corpus `group` column (its
        # `CensusRow` has one, its `write_csv` does not emit it), so the family group is
        # the suite's own label here. If a future census emits `group`, it is honoured.
        group = row.get("group") or spec["regime"]
        families.setdefault(group, set()).add(row["family"])
    if not families:
        sys.exit("ERROR: the census is empty; nothing to declare")
    family_groups = {group: sorted(families[group]) for group in sorted(families)}
    all_families = sorted({f for fams in family_groups.values() for f in fams})
    # Keep the requested dtype order (`[f64, c64]`), which is the order the recorder passes
    # to the harness and the order the declaration is expected to name.
    dtypes = list(dict.fromkeys(args.dtypes))
    seen_dtypes = {row["dtype"] for row in rows}
    if set(dtypes) != seen_dtypes:
        sys.exit(f"ERROR: the census covers dtypes {sorted(seen_dtypes)}, not the declared "
                 f"{dtypes}; refusing to emit a suite with a dtype the census does not cover")
    engines = list(args.rows)
    threads = sorted({int(row["threads"]) for row in rows})
    suite = {
        "schema_version": 1,
        "id": spec["suite_id"],
        "description": Block(spec["description"]),
        "invalidated_by": spec["invalidated_by"],
        "stale_after": COMMON["stale_after"],
        # No run exists yet, so the cell is optional; the first recorded cell moves it to required.
        "required_profiles": [],
        "optional_profiles": list(COMMON["optional_profiles"]),
        "features": list(spec["features"]),
        "family_groups": family_groups,
        "workloads": {k: Block(v) if isinstance(v, str) else v
                      for k, v in spec["workloads"].items()},
        "runs": [
            {
                "threads": threads,
                "cpu_sets": [_cpu_set_for(t) for t in threads],
                "dtypes": dtypes,
                "engines": engines,
                "populations": [
                    {
                        "regime": spec["regime"],
                        "groups": sorted(family_groups),
                        "n": [args.n],
                        "batch": [int(args.batch)],
                    }
                ],
            }
        ],
        "engines_doc": spec["engines_doc"],
    }
    return suite, all_families, dtypes, threads


def check_coverage(suite, rows):
    """The census cell set must equal the product the declaration requires.

    The product is the toolkit's own `expected_cells`, computed over the suite being
    emitted, so the generator, the recorder and the validator cannot disagree about what
    the declaration covers.
    """
    from campaign_toolkit import timing_evidence

    spec = suite["runs"][0]
    manifest = {
        "run_spec": {
            "populations": [
                {"regime": p["regime"], "families": sorted(
                    f for g in p["groups"] for f in suite["family_groups"][g]),
                 "n": p["n"], "batch": p["batch"]}
                for p in spec["populations"]
            ],
            "dtypes": spec["dtypes"],
            "engines": spec["engines"],
        },
        "threads": {"counts": spec["threads"]},
    }
    expected = timing_evidence.expected_cells(manifest)
    observed = {timing_evidence.cell(row)[:-1] for row in rows}
    if observed != expected:
        missing = sorted(expected - observed)
        extra = sorted(observed - expected)
        sys.exit("ERROR: the census does not cover the declared product; refusing to emit a suite\n"
                 f"  {len(missing)} declared cell(s) absent from the census, up to 5: {missing[:5]}\n"
                 f"  {len(extra)} census cell(s) not declared, up to 5: {extra[:5]}")
    return expected


def header_comment(harness, args, commands, families, dtypes, groups, threads):
    lines = [
        "# GENERATED by scripts/gen_suite_from_census.py -- do not edit by hand.",
        f"# Harness: {args.binary} ({harness})   Source revision: {args.revision}",
        "# Census (untimed `verify`, the smallest declared setting):",
    ]
    for cmd in commands:
        lines.append(f"#   {shlex.join(cmd)}")
    lines += [
        f"# Families: {len(families)} (one per case id); groups: {len(groups)} "
        f"({', '.join(groups)}); dtypes: {', '.join(dtypes)}; threads: "
        f"{', '.join(str(t) for t in threads)}.",
        f"# The declared identity shape is the numeric sentinel `n = {args.n}`: see the suite's "
        f"description and blind spots.",
        "",
    ]
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--harness", required=True, choices=sorted(HARNESSES))
    ap.add_argument("--binary", required=True, type=pathlib.Path,
                    help="the built harness binary")
    ap.add_argument("--revision", required=True,
                    help="the measured revision the binary was built from (for the header)")
    ap.add_argument("--out", required=True, type=pathlib.Path,
                    help="the suite YAML to write")
    ap.add_argument("--rows", default=None, help="engine rows, comma separated")
    ap.add_argument("--dtype", dest="dtypes", default=None, help="dtypes, comma separated")
    ap.add_argument("--n", default=COMMON["n"], help="the declared size spec")
    ap.add_argument("--batch", default=COMMON["batch"], help="the declared batch")
    ap.add_argument("--threads", default=None, help="thread budgets, comma separated")
    ap.add_argument("--workdir", default=None, type=pathlib.Path,
                    help="where the temporary census files go (default: target/census/<suite>)")
    args = ap.parse_args(argv)

    spec = HARNESSES[args.harness]
    if not args.binary.exists():
        sys.exit(f"ERROR: {args.binary} does not exist; build the harness first "
                 f"(scripts/build_for_tprims_rev.sh)")
    args.rows = [r for r in (args.rows.split(",") if args.rows else spec["rows"]) if r]
    args.dtypes = list(dict.fromkeys(
        d for d in (args.dtypes.split(",") if args.dtypes else COMMON["dtypes"]) if d))
    args.threads = [int(t) for t in (args.threads.split(",") if args.threads else COMMON["threads"])]
    unknown = [r for r in args.rows if r not in spec["rows"]]
    if unknown:
        sys.exit(f"ERROR: {unknown} is not one of this harness's measurable engine rows {spec['rows']}")

    workdir = args.workdir or pathlib.Path("target/census") / spec["suite_id"]
    workdir.mkdir(parents=True, exist_ok=True)
    commands, rows = [], []
    for thread in args.threads:
        census_path = workdir / f"{spec['suite_id']}-{thread}t.census.csv"
        commands.append(run_census(args.binary, args.harness, thread, args, census_path))
        rows.extend(read_census(census_path))

    suite, families, dtypes, threads = build_suite(args.harness, args, rows)
    expected = check_coverage(suite, rows)
    text = header_comment(args.harness, args, commands, families, dtypes,
                          sorted(suite["family_groups"]), threads)
    text += yaml.safe_dump(suite, sort_keys=False, default_flow_style=False,
                           allow_unicode=True, width=100)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text)
    print(f"wrote {args.out}: {len(families)} families, {len(suite['family_groups'])} groups, "
          f"{len(dtypes)} dtypes, {len(args.rows)} engines, {len(expected)} declared cells")
    return 0


if __name__ == "__main__":
    sys.exit(main())
