#!/usr/bin/env bash
# Materialise extern/tcontract-rs.
#
#   setup_extern_deps.sh            # from pins/tcontract-rs.rev, via a clone
#   setup_extern_deps.sh <dir>      # symlink an existing checkout at <dir>
#
# A path dependency must resolve for *any* cargo command, even with the feature
# off, so this has to run before the first build.
set -euo pipefail
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LINK="$PROJECT_DIR/extern/tcontract-rs"
if [[ $# -ge 1 ]]; then
    DIR="$(cd "$1" && pwd -P)"
    [[ -d "$DIR/crates/tcontract" ]] || { echo "ERROR: $DIR is not a tcontract-rs checkout" >&2; exit 1; }
    rm -rf "$LINK"
    ln -sfn "$DIR" "$LINK"
    echo "extern/tcontract-rs -> $DIR ($(git -C "$DIR" rev-parse --short HEAD), dirty=$( [[ -n "$(git -C "$DIR" status --porcelain --untracked-files=no)" ]] && echo true || echo false ))"
    exit 0
fi
REV="$(grep -v '^#' "$PROJECT_DIR/pins/tcontract-rs.rev" | tr -d '[:space:]')"
[[ -n "$REV" ]] || { echo "ERROR: pins/tcontract-rs.rev is empty" >&2; exit 1; }
if [[ -d "$LINK/.git" ]]; then
    git -C "$LINK" fetch -q origin
else
    rm -f "$LINK"
    git clone -q https://github.com/tensor4all/tcontract-rs "$LINK"
fi
git -C "$LINK" checkout -q "$REV"
echo "extern/tcontract-rs at $REV ($(git -C "$LINK" log --oneline -1))"
