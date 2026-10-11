#!/usr/bin/env bash
# Build the campaign harness out of one tcontract-rs checkout, into a target
# directory keyed by that checkout's commit.
#
#   build_for_tprims_rev.sh <tcontract-rs-dir> <out-var-file> [bin...]
#
# Writes shell assignments to <out-var-file>:
#   TPRIMS_REV, TPRIMS_DIRTY, TPRIMS_DIR, BIN_DIR, BUILD_FEATURES
#
# Two things this deliberately does *not* do.
#
# It does not build the harness from this repository. The harness is part of
# tcontract-rs (`benchmarks/benchmarks/tcbench`) and is compiled out of the same
# checkout as the library it measures, so `run.yaml`'s commit describes both.
# A harness built elsewhere could silently measure a different revision of the
# library than the one it was written against.
#
# It does not let baseline and candidate share a target directory, and it
# clears the compiler cache for the build: a cache keyed on inputs that do not
# include the sibling checkout can mix revisions, which is how a binary that
# did not contain the change under test once reached a measurement.
set -euo pipefail
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TPRIMS_DIR="$(cd "${1:?tcontract-rs checkout required}" && pwd -P)"
OUT_FILE="${2:?output variable file required}"
shift 2
BINS=("$@")
[[ ${#BINS[@]} -gt 0 ]] || BINS=(tcbench)

[[ -d "$TPRIMS_DIR/crates/tcontract" ]] || { echo "ERROR: $TPRIMS_DIR is not a tcontract-rs checkout" >&2; exit 1; }
MANIFEST="$TPRIMS_DIR/benchmarks/Cargo.toml"
[[ -f "$MANIFEST" ]] || { echo "ERROR: $MANIFEST not found" >&2; exit 1; }

rev="$(git -C "$TPRIMS_DIR" rev-parse HEAD)"
dirty=false
[[ -z "$(git -C "$TPRIMS_DIR" status --porcelain --untracked-files=no)" ]] || dirty=true
suffix=""; [[ $dirty == true ]] && suffix="-dirty"
target="$PROJECT_DIR/target/tcontract-rev/${rev:0:12}${suffix}"
profile="${BENCH_BUILD_PROFILE:-release}"

bin_args=(); for bin in "${BINS[@]}"; do bin_args+=(--bin "$bin"); done
profile_flag=(); subdir=debug
if [[ "$profile" == release ]]; then profile_flag=(--release); subdir=release; fi

FEATURES="${BENCH_FEATURES:-}"
# An empty feature list must not become `--features ""`, which cargo rejects.
feature_flag=(); [[ -n "$FEATURES" ]] && feature_flag=(--features "$FEATURES")
RUSTC_WRAPPER= CARGO_TARGET_DIR="$target" cargo build --manifest-path "$MANIFEST" \
    "${profile_flag[@]}" "${feature_flag[@]}" "${bin_args[@]}" >&2

bin_dir="$target/$subdir"
{
    printf 'TPRIMS_REV=%q\n' "$rev"
    printf 'TPRIMS_DIRTY=%q\n' "$dirty"
    printf 'TPRIMS_DIR=%q\n' "$TPRIMS_DIR"
    printf 'BIN_DIR=%q\n' "$bin_dir"
    # Not `%q`: a feature list is identifiers and commas, and quoting it would put a
    # backslash in front of every comma the manifest has to split on.
    printf 'BUILD_FEATURES=%s\n' "$FEATURES"
} > "$OUT_FILE"
echo "built ${BINS[*]} for tcontract-rs $rev (dirty=$dirty) in $bin_dir" >&2
