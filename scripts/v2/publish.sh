#!/bin/sh
# One publication of both timing-v2 campaigns, then the site over the two.
# TBLIS_ROOT is the external provider the tcbench suite measures; the recorder refuses a
# suite that measures one without its identity.
set -eu
: "${TBLIS_ROOT:?set TBLIS_ROOT to the TBLIS install prefix}"
PROVIDERS=$(mktemp)
trap 'rm -f "$PROVIDERS"' EXIT
python3 scripts/tblis_providers_json.py --out "$PROVIDERS"
for campaign in tcbench per-shape; do
    case $campaign in tcbench) AA=4 ;; *) AA=3 ;; esac
    taskset -c 0-3,12-15 python3 scripts/v2/record_run.py "$campaign" zen5-cpu "$campaign" \
        --aa $AA --reps 5 --prime-ms 250 --external-provider-json "$PROVIDERS" \
        --label "pub-$(date -u +%Y%m%d)-$campaign"
done
python3 scripts/v2/gen_site.py
