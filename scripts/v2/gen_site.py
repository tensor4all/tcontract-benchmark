#!/usr/bin/env python3
"""Write `result-v2/index.html` over both timing-v2 campaigns; see `campaign_toolkit.site`."""
import pathlib
import sys

from campaign_toolkit import site

ROOT = pathlib.Path(__file__).resolve().parents[2]

if __name__ == "__main__":
    sys.exit(site.main(["--root", str(ROOT), "--site", str(ROOT / "result-v2"),
                        "--pin", "pins/tcontract-rs-v2.rev", *sys.argv[1:]]))
