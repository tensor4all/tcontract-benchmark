#!/usr/bin/env python3
"""Write the site under `result-v2/`: one toolkit site per timing-v2 campaign and a landing page.

    python3 scripts/v2/gen_site.py [--repo-ref main]

Nothing it writes is committed (see `.gitignore`); the Pages workflow runs it on every deploy from
the committed `data/`, `result-v2/` and `pins/`. Each campaign's site (`result-v2/<campaign>/`:
its landing page, history, the HTML copy of every page and the charts its descriptor declares) is
the toolkit's (`campaign_toolkit.site`), written with that campaign's descriptor selected, each in
its own process. What is this repository's own is `result-v2/index.html`, which links the two
campaigns and the frozen timing-v1 pages (`result/INDEX.md`, history only).
"""
import argparse
import html
import os
import pathlib
import subprocess
import sys

from campaign_toolkit import site

ROOT = pathlib.Path(__file__).resolve().parents[2]
CAMPAIGNS = {
    "tcbench": "tcbench: the TCCG contraction corpus",
    "per-shape": "per-shape: named contraction cases (lukbench)",
}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-ref", default="main", help="the branch the site is published from")
    args = ap.parse_args(argv)
    for campaign, title in CAMPAIGNS.items():
        env = dict(os.environ, CAMPAIGN_DESCRIPTOR=f"benchmarks/campaign-{campaign}.yaml")
        subprocess.run([sys.executable, "-m", "campaign_toolkit.site", "--root", str(ROOT),
                        "--repo-ref", args.repo_ref, "--title", f"tcontract {title}"],
                       env=env, check=True)
    blob = site._blob_base(ROOT)
    items = "".join(f'<li><a href="{c}/index.html">{html.escape(t)}</a></li>'
                    for c, t in CAMPAIGNS.items())
    legacy = f"{blob}/blob/{args.repo_ref}/result/INDEX.md"
    (ROOT / "result-v2" / "index.html").write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>tcontract benchmark results</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>{site.CSS}</style></head><body>
<h1>tcontract benchmark results</h1>
<p>Two timing-v2 campaigns measure <a href="https://github.com/tensor4all/tcontract-rs">tcontract-rs</a>
at the pinned revision, each with its own pages, charts and history.</p>
<ul>{items}</ul>
<h2>History</h2>
<p><a href="{html.escape(legacy)}">The legacy timing-v1 pages</a>
<span class="muted">(frozen; recorded before the timing-v2 campaigns and not regenerated)</span></p>
</body></html>
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
