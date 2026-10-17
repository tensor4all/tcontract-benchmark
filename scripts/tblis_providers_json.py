#!/usr/bin/env python3
"""Write the TBLIS identity as the timing-v2 `--external-provider-json` payload.

    scripts/tblis_providers_json.py [--out PATH]

The timing-v2 recorder refuses to record a suite that measures an external
provider (here `tblis`) unless it is told that provider's revision, so the
payload is a JSON list with one `tblis` entry carrying
`name`/`version`/`commit`/`path`/`note`/`tag`/`sha256`.

The identity is not reimplemented here: it is the legacy timing-v1 collector
`tblis_identity()` and its `providers_for()` entry in `scripts/record_run.py`,
which read `$TBLIS_ROOT/PROVENANCE` (written by
`extern/tcontract-rs/benchmarks/scripts/build_tblis.sh`). `$TBLIS_ROOT` is
checked first so a missing prefix fails with its own name rather than as a
recorder admission refusal several steps later.
"""
import argparse
import json
import os
import pathlib
import sys

SCRIPTS = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))
import record_run  # noqa: E402  the legacy timing-v1 collector, reused verbatim


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=pathlib.Path, default=None,
                    help="write the JSON here (default: stdout)")
    args = ap.parse_args(argv)

    root = os.environ.get("TBLIS_ROOT")
    if not root:
        sys.exit("ERROR: TBLIS_ROOT is unset; point it at the TBLIS install prefix built by "
                 "extern/tcontract-rs/benchmarks/scripts/build_tblis.sh (see docs/v2-layout.md)")
    provenance = pathlib.Path(root) / "PROVENANCE"
    if not provenance.exists():
        sys.exit(f"ERROR: {provenance} does not exist; TBLIS_ROOT must name a prefix that "
                 f"build_tblis.sh installed (see docs/v2-layout.md)")

    entries = record_run.providers_for(["tblis"])
    if len(entries) != 1 or entries[0].get("name") != "tblis" or not entries[0].get("commit"):
        sys.exit("ERROR: the legacy TBLIS collector did not yield one TBLIS entry with a commit")

    payload = json.dumps(entries, indent=2) + "\n"
    if args.out:
        args.out.write_text(payload)
        print(f"wrote {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
