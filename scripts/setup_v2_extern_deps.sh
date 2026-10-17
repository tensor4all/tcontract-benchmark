#!/usr/bin/env bash
# Materialise extern/tcontract-rs-v2 for the timing-v2 campaigns.
#
#   setup_v2_extern_deps.sh            # from pins/tcontract-rs-v2.rev, via a clone
#   setup_v2_extern_deps.sh <dir>      # symlink an existing checkout at <dir>
#
# The v2 campaigns pin their own measured revision (`pins/tcontract-rs-v2.rev`) and
# their own checkout directory, so they cannot disturb the legacy timing-v1 checkout
# and reference pin that `scripts/setup_extern_deps.sh` owns.
set -euo pipefail
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LINK="$PROJECT_DIR/extern/tcontract-rs-v2"
if [[ $# -ge 1 ]]; then
    DIR="$(cd "$1" && pwd -P)"
    [[ -d "$DIR/crates/tcontract" ]] || { echo "ERROR: $DIR is not a tcontract-rs checkout" >&2; exit 1; }
    rm -rf "$LINK"
    ln -sfn "$DIR" "$LINK"
    echo "extern/tcontract-rs-v2 -> $DIR ($(git -C "$DIR" rev-parse --short HEAD), dirty=$( [[ -n "$(git -C "$DIR" status --porcelain --untracked-files=no)" ]] && echo true || echo false ))"
    exit 0
fi
REV="$(sed -n 's/^[[:space:]]*\([0-9a-f]\{7,\}\)[[:space:]]*$/\1/p' "$PROJECT_DIR/pins/tcontract-rs-v2.rev" | tail -1)"
[[ -n "$REV" ]] || { echo "ERROR: pins/tcontract-rs-v2.rev names no revision" >&2; exit 1; }
if [[ -d "$LINK/.git" ]]; then
    git -C "$LINK" fetch -q origin
else
    rm -f "$LINK"
    git clone -q https://github.com/tensor4all/tcontract-rs "$LINK"
fi
git -C "$LINK" checkout -q "$REV"
echo "extern/tcontract-rs-v2 at $REV ($(git -C "$LINK" log --oneline -1))"
