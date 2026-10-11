#!/usr/bin/env python3
"""Generate result/INDEX.md: a table of contents over the per-revision pages.

Each result page is one `(suite, hardware profile, measured revision)`. The
index has two tables: the at-a-glance state of every cell, and the full list of
published pages keyed by revision and hardware.

The failure this exists to prevent: with one tracked report per
`(profile, suite)`, a cell that has not been re-measured keeps its old file, and
a reader -- human or agent -- sees a commit hash and a table without being able
to tell whether that cell reflects the current library or something weeks old.
Reports were self-describing; the *set* of them was not, so staleness leaked
into prose. Here it is structural and machine-checkable:

  status      meaning
  ----------  ---------------------------------------------------------------
  missing     no run recorded for this cell
  current     measured at the reference revision, or at a descendant
  N behind    N commits touching the suite's `invalidated_by` paths lie between
              the measured revision and pins/tcontract-rs.rev
  stale       as `behind`, but N exceeds the suite's `stale_after`
  dirty       the measured checkout had uncommitted changes; never comparable
  diverged    the measured revision is not an ancestor of the reference

`behind` counts invalidating commits, not raw distance: a suite that only
touches `crates/` is not out of date because a doc changed.
"""
import argparse
import pathlib
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "result/INDEX.md"


def load(path):
    return yaml.safe_load(pathlib.Path(path).read_text())


def git(checkout, *args):
    out = subprocess.run(["git", "-C", checkout, *args], capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed in {checkout}: {out.stderr.strip()}")
    return out.stdout.strip()


def reference_rev():
    return (ROOT / "pins/tcontract-rs.rev").read_text().strip()


def invalidating_distance(checkout, measured, reference, paths):
    """Commits touching `paths` that are in `reference` but not in `measured`."""
    if measured == reference:
        return 0
    try:
        git(checkout, "merge-base", "--is-ancestor", measured, reference)
    except RuntimeError:
        return None
    return int(git(checkout, "rev-list", "--count", f"{measured}..{reference}", "--", *paths) or 0)


def suite_hash(suite):
    import hashlib
    return hashlib.sha256((ROOT / "benchmarks/suites" / f"{suite['id']}.yaml").read_bytes()).hexdigest()


def coverage_of(suite, manifest):
    """How a page relates to the *current* declaration.

    `full` and `partial` are the run's own statement, but only meaningful while
    the declaration it was measured under is unchanged. Once the declaration
    moves -- an arm added, a size dropped -- the page cannot be described as
    full or partial against today's spec without comparing the two by hand, so
    it is labelled `declaration-changed` and the reader is told rather than
    misled. Evidence is immutable; declarations are not.
    """
    recorded = manifest.get("suite_sha256")
    if recorded and recorded == suite_hash(suite):
        return "full" if manifest["run_spec"].get("covers_declared_suite") else "partial"
    return "declaration-changed"


def page_relative(profile, suite, manifest):
    """The published page for a run. Must match scripts/publish_report.py."""
    tprims = manifest["tprims"]
    suffix = "-dirty" if tprims["dirty"] else ""
    version = f"-{tprims['version']}" if tprims.get("version") else ""
    return f"result/{profile}/{suite}/{tprims['commit'][:12]}{version}{suffix}.md"


def status_of(suite, manifest, checkout, reference, have_checkout):
    """(status, invalidating_commits) for one recorded run."""
    if manifest["tprims"]["dirty"]:
        return "dirty", None
    if not have_checkout:
        return "unknown", None
    distance = invalidating_distance(checkout, manifest["tprims"]["commit"], reference,
                                     suite["invalidated_by"])
    if distance is None:
        return "diverged", None
    if distance == 0:
        return "current", 0
    if distance > suite["stale_after"]:
        return "stale", distance
    return f"{distance} behind", distance


def collect():
    """The published pages, plus the cells that have no run at all."""
    profiles = [p["name"] for p in load(ROOT / "benchmarks/profiles.yaml")["profiles"]]
    suites = [load(f) for f in sorted((ROOT / "benchmarks/suites").glob("*.yaml"))]
    reference = reference_rev()
    checkout = ROOT / "extern/tcontract-rs"
    have_checkout = (checkout / ".git").exists()
    pages, missing = [], []
    for suite in suites:
        wanted = list(suite["required_profiles"]) + [p for p in suite.get("optional_profiles", [])]
        for profile in wanted:
            required = profile in suite["required_profiles"]
            cell = ROOT / "data/results" / profile / suite["id"]
            manifests = sorted(cell.glob("*/run.yaml")) if cell.is_dir() else []
            if not manifests:
                missing.append(dict(suite=suite["id"], profile=profile, required=required))
                continue
            # One page per revision: keep the newest run that produced it.
            per_page = {}
            for mf in manifests:
                m = load(mf)
                rel = page_relative(profile, suite["id"], m)
                status, distance = status_of(suite, m, checkout, reference, have_checkout)
                row = dict(
                    suite=suite["id"], profile=profile, required=required,
                    commit=m["tprims"]["commit"][:12], version=m["tprims"].get("version"),
                    date=m["timestamp"][:10], timestamp=m["timestamp"],
                    coverage=coverage_of(suite, m),
                    status=status, behind=distance, stale_after=suite["stale_after"],
                    page=rel if (ROOT / rel).exists() else None,
                    sort_key=(m["timestamp"], m["tprims"]["commit"][:12]),
                )
                if rel not in per_page or row["sort_key"] > per_page[rel]["sort_key"]:
                    per_page[rel] = row
            pages.extend(per_page.values())
    return pages, missing, reference, profiles, [s["id"] for s in suites], have_checkout


def cells(pages, missing):
    """(suite, profile) groups, newest page first, including cells with no run."""
    order, by = [], {}
    for r in missing:
        key = (r["suite"], r["profile"])
        by[key] = {"suite": r["suite"], "profile": r["profile"],
                   "required": r["required"], "runs": []}
        order.append(key)
    for r in pages:
        key = (r["suite"], r["profile"])
        if key not in by:
            by[key] = {"suite": r["suite"], "profile": r["profile"],
                       "required": r["required"], "runs": []}
            order.append(key)
        by[key]["runs"].append(r)
    out = []
    for key in order:
        cell = by[key]
        cell["runs"].sort(key=lambda r: r["sort_key"], reverse=True)
        full = [r for r in cell["runs"] if r["coverage"] == "full"]
        cell["newest"] = (full or cell["runs"])[0] if cell["runs"] else None
        out.append(cell)
    return out


def link(page):
    """A markdown link to a page, with a target that resolves from result/.

    INDEX.md lives in result/, so the target must be relative to that
    directory while the visible text stays the repository-relative path. Using
    the repository-relative path for both produced links to
    result/result/<profile>/... that 404.
    """
    target = pathlib.Path(page)
    try:
        target = target.relative_to(INDEX.parent.relative_to(ROOT))
    except ValueError:
        pass
    return f"[{page}]({target})"


def render(pages, missing, reference, generated):
    out = [
        "# Result index",
        "",
        "Generated by `scripts/gen_index.py`. **Do not edit by hand**; CI checks that",
        "this file is what the generator produces.",
        "",
        f"- Reference revision (`pins/tcontract-rs.rev`): `{reference}`",
        f"- Newest recorded run: `{generated}`",
        "- Every page below is one `(suite, hardware profile, revision)` and carries",
        "  its commit and hardware itself.",
        "",
        "## Cells",
        "",
        "The newest full-coverage page for each cell, and whether it is current.",
        "",
        "| suite | profile | revision | version | date | coverage | status | page |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for cell in cells(pages, missing):
        mark = "" if cell["required"] else " (optional)"
        r = cell["newest"]
        if r is None:
            out.append(f"| `{cell['suite']}` | `{cell['profile']}`{mark} | - | - | - | - | missing | - |")
        else:
            cell_link = link(r["page"]) if r.get("page") else "(no page)"
            out.append(f"| `{cell['suite']}` | `{cell['profile']}`{mark} | `{r['commit']}` | "
                       f"{r['version'] or '-'} | {r['date']} | {r['coverage']} | {r['status']} | {cell_link} |")
    out += [
        "",
        "`missing` is a normal cell, not an error: the campaign is not run on every",
        "profile for every commit. It becomes an error only for a profile a suite lists",
        "as `required`. `coverage` relates a page to the *current* declaration: `full`",
        "when it was measured over the whole spec and the declaration has not moved since,",
        "`partial` when it covered a subset, and `declaration-changed` when the declaration",
        "itself changed after the measurement, so the two have to be compared by hand. A",
        "partial or declaration-changed page never displaces a full-coverage one.",
        "",
        "## All pages",
        "",
        "| suite | profile | revision | version | date | coverage | status | page |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in sorted(pages, key=lambda r: (r["suite"], r["profile"], r["sort_key"]), reverse=True):
        page_link = link(r["page"]) if r.get("page") else "(no page)"
        out.append(f"| `{r['suite']}` | `{r['profile']}` | `{r['commit']}` | {r['version'] or '-'} | "
                   f"{r['date']} | {r['coverage']} | {r['status']} | {page_link} |")
    out.append("")
    return "\n".join(out).rstrip("\n") + "\n"


def broken_links(text):
    """Every markdown target in the index must name a file that exists."""
    import re
    missing = []
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
        if target.startswith(("http://", "https://", "#")):
            continue
        if not (INDEX.parent / target).exists():
            missing.append(target)
    return missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="fail if the committed file differs, or a required cell is missing/stale")
    ap.add_argument("--fail-on-stale", action="store_true",
                    help="also fail when a required cell is stale")
    ap.add_argument("--write", action="store_true", help="write result/INDEX.md")
    args = ap.parse_args()

    pages, missing, reference, _profiles, _suites, have_checkout = collect()
    published = [p for p in pages if p["page"]]
    stamps = [p["timestamp"] for p in published]
    text = render(published, missing, reference, max(stamps) if stamps else "none")

    problems = []
    if not have_checkout:
        problems.append("extern/tcontract-rs is absent, so currency cannot be computed "
                        "(run scripts/setup_extern_deps.sh)")
    for cell in missing:
        if cell["required"]:
            problems.append(f"required cell {cell['suite']}/{cell['profile']} has no run")
    for r in published:
        if not r["required"]:
            continue
        if r["status"] == "dirty":
            problems.append(f"required cell {r['suite']}/{r['profile']} was measured from a dirty checkout")
        elif r["status"] == "diverged":
            problems.append(f"required cell {r['suite']}/{r['profile']} is not an ancestor of the reference")
        elif r["status"] == "stale" and args.fail_on_stale:
            problems.append(f"required cell {r['suite']}/{r['profile']} is stale "
                            f"({r['behind']} invalidating commits > {r['stale_after']})")

    if args.write:
        INDEX.parent.mkdir(parents=True, exist_ok=True)
        INDEX.write_text(text)
        print(f"wrote {INDEX.relative_to(ROOT)}")
        return 0
    for target in broken_links(text):
        problems.append(f"generated index links to {target}, which does not exist")

    if args.check:
        if not INDEX.exists() or INDEX.read_text() != text:
            problems.append("result/INDEX.md is out of date; run scripts/gen_index.py --write")
        for p in problems:
            print(f"FAIL {p}", file=sys.stderr)
        return 1 if problems else 0
    print(text)
    for p in problems:
        print(f"note: {p}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
