#!/usr/bin/env python3
"""Common body of the timing-v2 shims under `scripts/v2/`.

A timing-v2 entry point is the toolkit's, parameterised by a descriptor. This
repository carries two descriptors (`benchmarks/campaign-tcbench.yaml` and
`benchmarks/campaign-per-shape.yaml`), so each shim takes the campaign id as its
first argument, sets `CAMPAIGN_DESCRIPTOR` to that campaign's descriptor, and
hands the remaining arguments to the toolkit entry point unchanged:

    scripts/v2/record_run.py <campaign> <toolkit args...>

The shims live under `scripts/v2/`, not `scripts/`, so they never shadow the
legacy timing-v1 `scripts/*.py` entry points, which stay authoritative for the
committed v1 evidence.
"""
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
CAMPAIGNS = ("tcbench", "per-shape")


def run(module):
    argv = sys.argv[1:]
    if not argv or argv[0] not in CAMPAIGNS:
        sys.exit(f"ERROR: {sys.argv[0]}: pass the campaign id "
                 f"({'|'.join(CAMPAIGNS)}) first, then the toolkit arguments")
    if str(pathlib.Path(__file__).resolve().parent) not in sys.path:
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    os.environ["CAMPAIGN_DESCRIPTOR"] = f"benchmarks/campaign-{argv[0]}.yaml"
    toolkit = __import__(f"campaign_toolkit.{module}", fromlist=["main"])
    return toolkit.main(argv[1:], root=ROOT)
