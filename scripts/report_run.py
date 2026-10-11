#!/usr/bin/env python3
"""Turn one run's tcbench CSVs into the tracked report for a (profile, suite) cell.

Only the numbers that came from a verified run are published: every row here
was gated by `tcbench verify` (known values and full-output residuals) before
the timing pass started. The report repeats the run's provenance in its own
header, because a table that is copied into a discussion without its commit is
the thing this repository exists to stop.
"""
import argparse
import csv
import math
import pathlib
import statistics
import sys

import yaml


def read_rows(csv_paths):
    """Rows from the run CSVs, with the tensor size recovered from the filename.

    tcbench's rows carry the case, dtype, engine and thread count but not the
    nominal size; the file is named `<repeat>-<size>m-<threads>t.csv`, which is
    where the size comes from.
    """
    rows = []
    for p in csv_paths:
        stem = pathlib.Path(p).stem  # run0-16m-8t, or run0-fixed-8t
        try:
            parts = stem.split("-")
            token = parts[-2]
            # A suite whose corpus has fixed shapes runs with no --size at all, so
            # the file name says `fixed` where a sized one carries `<n>m`.
            size_mib = None if token == "fixed" else float(token.rstrip("m"))
        except (ValueError, IndexError):
            raise SystemExit(f"cannot read the nominal size from {p}")
        with open(p) as f:
            body = [line for line in f if not line.startswith("#")]
        for row in csv.DictReader(body):
            row["size_mib"] = size_mib
            rows.append(row)
    return rows


def render(manifest, suite, rows, run_dir, root, providers):
    size_mib = manifest.get("run_spec", {}).get("sizes_mib", [])
    counts = manifest["threads"]["counts"]
    dtypes = manifest.get("run_spec", {}).get("dtypes", [])
    engines = manifest.get("run_spec", {}).get("engines", [])
    out = [
        f"# `{manifest['suite_id']}` on `{manifest['target_profile']}`",
        "",
        f"- tcontract-rs commit: `{manifest['tprims']['commit']}`"
        + (" **(dirty)**" if manifest["tprims"]["dirty"] else ""),
        f"- features: `{', '.join(manifest['tprims']['features']) or 'default'}`",
        f"- harness commit: `{manifest['harness']['commit']}`",
        f"- hardware profile: `{manifest['target_profile']}`",
        f"- timestamp: `{manifest['timestamp']}`",
        f"- timing policy: v{manifest['timing_policy']['version']}, "
        f"{manifest['timing_policy']['statistic']} of {manifest['timing_policy']['repetitions']} reps, "
        f"priming {manifest['timing_policy']['minimum_untimed_priming_ms']} ms",
        f"- command: `{manifest['command']}`",
        f"- raw data: `{run_dir.relative_to(root)}/`",
        "## What was measured",
        "",
        f"- **Corpus `{suite['corpus']['name']}`** — {suite['corpus']['description']}",
        f"  Source: {suite['corpus']['source']}",
    ]
    for spot in suite["corpus"].get("known_blind_spots", []):
        out.append(f"  Known blind spot: {spot}")
    out += [
        f"- **Engines** — one row per engine in every table below:",
    ]
    label = lambda e: (suite["engines_doc"].get(e) or {}).get("label", e)
    for engine in engines:
        doc = suite["engines_doc"].get(engine)
        if doc is None:
            out.append(f"  - `{label(engine)}` — (undocumented in the suite declaration)")
            continue
        out.append(f"  - `{label(engine)}` — {doc['summary']}")
        # Prefer the identity recorded in *this run's* manifest over the suite's
        # generic sentence: a page should state what it actually measured.
        prov = providers.get(doc.get("provider"))
        if prov:
            bits = [prov["name"]]
            if prov.get("version"):
                bits.append(f"version {prov['version']}")
            if prov.get("commit"):
                bits.append(f"commit `{prov['commit']}`")
            line = ", ".join(bits)
            if prov.get("note"):
                line += f" — {prov['note']}"
            out.append(f"    Identity (as measured): {line}")
        else:
            out.append(f"    Identity: {doc['identity']}")
        if doc.get("caveat"):
            out.append(f"    Caveat: {doc['caveat']}")
    out += [
        *(
            f"- **Shapes** — the corpus has fixed shapes, so there is no nominal-size knob "
            f"and the runner is given no `--size`; each table below is one dtype and thread "
            f"count over the whole corpus.".splitlines()
            if not size_mib
            else [
                f"- **Sizes** — the nominal tensor size per case in MiB. TCCG's sizing rule scales",
                f"  every extent of a case from it, so the same case at 1 MiB and 16 MiB has the",
                f"  same shape structure at different magnitudes.",
            ]
        ),
        f"- **dtypes** — `f64` is a real double, `c64` a complex double. The complex rows",
        f"  are the harder case for this library and are never likelier to look good.",
        f"- **Numbers** — milliseconds, best wall time per case and engine. See the timing",
        f"  policy for what is inside and outside the timed region.",
        "",
        "## Hardware",
        "",
        f"- CPU: `{manifest['host']['cpu']}`",
        f"- logical CPUs: `{manifest['host']['logical_cpus']}`",
        f"- L3: `{manifest['host']['l3']}`",
        f"- L3 domains: `{manifest['host'].get('l3_domains') or manifest['host']['l3']}`",
        f"- OS / arch: `{manifest['host']['os']}` / `{manifest['host']['arch']}`",
        f"- hostname: `{manifest['host']['hostname']}`",
        f"- CPU sets: " + ", ".join(f"{t}T -> `{c}`"
                                    for t, c in sorted(manifest["threads"]["cpu_sets"].items())),
        "",
        f"Every row below passed `{suite.get('runner', 'tcbench')} verify` (known values and full-output residual "
        "<= 1e-10) before timing. Values are the geometric mean over "
        + (f"{manifest['run_spec']['aa']} complete set repeats" if manifest['run_spec']['aa'] > 1
           else "the timed repetitions (this run made a single complete set, so it carries no A/A)")
        + " of the best wall time per engine.",
        "",
        "Where the independent reference ran, the last column is `tprims [plan] / tblis`, a ratio of "
        "those two geomeans: above 1 means tprims took longer. The `±` after it is the largest "
        "scatter among the repetitions behind it (the harness's `spread`, `(max - min) / best`), so "
        "a row whose ratio is smaller than its own scatter is not separable from noise. The same "
        "number is in the CSV's `spread` column for every row.",
        "",
        "`prepare (µs)` is what each side spends *before* the timed call - the plan for tprims, the "
        "operand descriptors for the reference. The timing policy excludes that work, which is why "
        "the harness can build a plan once and time only execution, and the reference has nothing "
        "comparable to hoist: its own analysis is inside the one call it exposes. On microsecond "
        "cases the preparation can exceed the whole timed call, so a ratio there compares a "
        "prepared path with a one-shot call rather than two kernels.",
        "",
    ]
    for size in (size_mib or [None]):
        for dtype in dtypes:
            for threads in counts:
                group = [r for r in rows
                         if (size is None or float(r["size_mib"]) == float(size))
                         and r["dtype"] == dtype and int(r["threads"]) == threads]
                if not group:
                    continue
                heading = "fixed shapes" if size is None else f"{size} MiB"
                out.append(f"## {heading}, {dtype}, {threads}T "
                           f"(CPU {manifest['threads']['cpu_sets'].get(str(threads), '?')})")
                out.append("")
                ratio = "plan" in engines and "tblis" in engines
                gm = statistics.geometric_mean

                def times(case, engine):
                    return [float(r["seconds"]) for r in group
                            if r["case"] == case and r["engine"] == engine]

                def scatter():
                    # Rows recorded before the harness carried `spread` have none, and a
                    # single-repetition row has 0; absence is reported as no `±`.
                    s = [float(r["spread"]) for r in group
                         if r["engine"] in ("plan", "tblis") and r.get("spread") not in (None, "")]
                    return max(s) if s else None

                def prep(engine):
                    # Seconds each side spends before the timed call. Rows recorded
                    # before the harness carried the column report nothing.
                    s = [float(r["prepare_s"]) for r in group
                         if r["engine"] == engine and r.get("prepare_s") not in (None, "")]
                    return s

                def prep_cell(case=None):
                    def one(engine):
                        s = [float(r["prepare_s"]) for r in group
                             if r["engine"] == engine
                             and (case is None or r["case"] == case)
                             and r.get("prepare_s") not in (None, "")]
                        return f"{gm(s) * 1e6:.1f}" if s else "-"
                    sides = [one(e) for e in ("plan", "tblis") if e in engines]
                    return "/".join(sides) if sides else "-"

                def ratio_cell(left, right):
                    if not left or not right:
                        return "-"
                    r = gm(left) / gm(right)
                    sp = scatter()
                    return f"{r:.3f}" + (f" ±{sp * 100:.1f}%" if sp is not None else "")

                has_prep = any(prep(e) for e in engines)
                header = "| case | " + " | ".join(f"{label(e)} (ms)" for e in engines) + " |"
                if has_prep:
                    header = header[:-1] + "| prepare (µs) |"
                if ratio:
                    header = header[:-1] + "| tprims [plan] / tblis |"
                out.append(header)
                out.append("|" + "---|" * (len(engines) + (2 if ratio else 1) + (1 if has_prep else 0)))
                for case in sorted({r["case"] for r in group}):
                    cells = []
                    for e in engines:
                        s = times(case, e)
                        cells.append(f"{gm(s) * 1e3:.4f}" if s else "-")
                    if has_prep:
                        cells.append(prep_cell(case))
                    if ratio:
                        cells.append(ratio_cell(times(case, "plan"), times(case, "tblis")))
                    out.append(f"| `{case}` | " + " | ".join(cells) + " |")
                summary = []
                for e in engines:
                    s = [float(r["seconds"]) for r in group if r["engine"] == e]
                    summary.append(f"{gm(s) * 1e3:.4f}" if s else "-")
                if has_prep:
                    summary.append(prep_cell())
                if ratio:
                    summary.append(ratio_cell([float(r["seconds"]) for r in group if r["engine"] == "plan"],
                                               [float(r["seconds"]) for r in group if r["engine"] == "tblis"]))
                out.append(f"| **geomean** | " + " | ".join(summary) + " |")
                out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    args = ap.parse_args()
    run_dir = pathlib.Path(args.run_dir).resolve()
    manifest = yaml.safe_load((run_dir / "run.yaml").read_text())
    suite = yaml.safe_load((pathlib.Path(__file__).resolve().parent.parent
                            / "benchmarks/suites" / f"{manifest['suite_id']}.yaml").read_text())
    rows = read_rows(sorted(run_dir.glob("*.csv")))
    providers = {p["name"]: p for p in manifest.get("providers", [])}
    text = render(manifest, suite, rows, run_dir, pathlib.Path(__file__).resolve().parent.parent,
                  providers)
    (run_dir / "report.md").write_text(text)
    print(f"wrote {run_dir}/report.md from {len(rows)} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
