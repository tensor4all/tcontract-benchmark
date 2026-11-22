#!/usr/bin/env python3
"""Check that every committed suite carries the shared granularity note, byte for byte.

The note is authored once, in `gen_suite_from_census.py`, and the suites are generated from it
and committed. Nothing regenerates them on a pull request -- that needs a harness binary at the
recorded revision -- so a hand edit, or a generator whose string drifted from its emitted text,
would go unnoticed until the next regeneration. This compares the generator's note with the
committed declarations semantically *and* byte for byte: the block the generator's own `yaml`
settings would emit must be the block the file carries, because a note that wraps differently
(or that breaks a word across a line) is a different declaration, even when it parses to the
same words in this one case.

It also pins the two text properties the declaration must keep: no intra-word break and no
stray whitespace, and a distinction between `ttgt`, whose tables and scratch are prepared
outside the clock, and `tblis`, whose analysis is inside its timed call. A blanket "no
reference exposes a prepared contraction" was wrong for `ttgt` and is exactly what this
asserts against.
"""
from __future__ import annotations

import importlib.util
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SUITES = ("tcbench", "per-shape", "qcbench", "zqcbench")


def load_generator():
    path = ROOT / "scripts" / "gen_suite_from_census.py"
    spec = importlib.util.spec_from_file_location("gen_suite_from_census", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def emitted_block(note):
    """The lines `gen_suite_from_census` would write for this note, at the suite's depth."""
    text = yaml.safe_dump(
        {"workloads": {"known_blind_spots": [note]}},
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
        width=100,
    )
    lines = text.splitlines()
    assert lines[:2] == ["workloads:", "  known_blind_spots:"], lines[:2]
    return lines[2:]


def committed_block(path):
    """The lines of the last item in the suite's `known_blind_spots` list."""
    lines = path.read_text().splitlines()
    start = lines.index("  known_blind_spots:") + 1
    end = start
    while end < len(lines) and (lines[end].startswith("  - ") or lines[end].startswith("    ")):
        end += 1
    last = end - 1
    while not lines[last].startswith("  - "):
        last -= 1
    return lines[last:end]


def main():
    note = load_generator().GRANULARITY_NOTE
    errors = []

    if note != note.strip():
        errors.append("GRANULARITY_NOTE has leading or trailing whitespace")
    if "\n" in note or "  " in note:
        errors.append("GRANULARITY_NOTE is not a single space-separated line")
    if re.search(r"\w- \w", note):
        errors.append("GRANULARITY_NOTE breaks a hyphenated word across the generator literal")
    for name in ("ttgt", "tblis"):
        if name not in note:
            errors.append(f"GRANULARITY_NOTE does not distinguish `{name}`")

    expected = emitted_block(note)
    for suite in SUITES:
        path = ROOT / "benchmarks" / "suites-v2" / f"{suite}.yaml"
        document = yaml.safe_load(path.read_text())
        spots = document["workloads"]["known_blind_spots"]
        if note not in spots:
            errors.append(f"{path.name}: the generator's note is not in known_blind_spots")
            continue
        block = committed_block(path)
        if block != expected:
            errors.append(
                f"{path.name}: the committed note is not byte-identical to what the generator "
                f"emits ({len(block)} lines against {len(expected)})"
            )

    for error in errors:
        print(f"FAIL {error}")
    if errors:
        return 1
    print(f"ok   {len(SUITES)} suites carry the generator's granularity note byte for byte")
    return 0


if __name__ == "__main__":
    sys.exit(main())
