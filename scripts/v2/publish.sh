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
    # one complete engine-order rotation cycle per suite: tcbench declares 3 engines
    # (plan, ttgt, tblis; packed was dropped in 7f99a05), per-shape 2 (plan, tblis)
    case $campaign in tcbench) AA=3 ;; *) AA=2 ;; esac
    taskset -c 0-3,12-15 python3 scripts/v2/record_run.py "$campaign" zen5-cpu "$campaign" \
        --aa $AA --reps 5 --prime-ms 250 --external-provider-json "$PROVIDERS" \
        --label "pub-$(date -u +%Y%m%d)-$campaign"
done
