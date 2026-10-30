#!/usr/bin/env python3
"""Write the TBLIS identity as the timing-v2 `--external-provider-json` payload.

    scripts/tblis_providers_json.py [--out PATH]

The timing-v2 recorder refuses to record a suite that measures an external
provider (here `tblis`) unless it is told that provider's revision, so the
payload is a JSON list with one `tblis` entry carrying
`name`/`version`/`commit`/`path`/`note`/`tag`/`sha256`.

The identity is read from `$TBLIS_ROOT/PROVENANCE` (written by
`extern/tcontract-rs/benchmarks/scripts/build_tblis.sh`), with `TBLIS_*` environment
variables filling fields it leaves out; the entry is the one the legacy timing-v1
recorder wrote, moved here when that recorder was removed (tensor4all-meta#76 D10).
`$TBLIS_ROOT` is checked first so a missing prefix fails with its own name rather than
as a recorder admission refusal several steps later.
"""
import argparse
import json
import os
import pathlib
import sys



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


def tblis_entry():
    """The `tblis` provider entry; refuses when its revision cannot be stated."""
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
    return entry


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

    entries = [tblis_entry()]

    payload = json.dumps(entries, indent=2) + "\n"
    if args.out:
        args.out.write_text(payload)
        print(f"wrote {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
