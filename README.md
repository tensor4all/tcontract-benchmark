# tcontract-benchmark

The benchmark campaign for [tcontract-rs](https://github.com/tensor4all/tcontract-rs):
results keyed by **library commit × hardware profile**, with the staleness of
every cell visible rather than implied.

| | |
|---|---|
| Results site | [tensor4all.org/tcontract-benchmark](https://tensor4all.org/tcontract-benchmark/) — both campaigns' pages, charts and history |
| Latest results | [`result-v2/tcbench/INDEX.md`](result-v2/tcbench/INDEX.md), [`result-v2/per-shape/INDEX.md`](result-v2/per-shape/INDEX.md) — generated; older pages in each `HISTORY.md` |
| Result layout | [`docs/v2-layout.md`](docs/v2-layout.md); the frozen timing-v1 tree in [`docs/results.md`](docs/results.md) |
| Timing policy | [`docs/timing-policy.md`](docs/timing-policy.md) |
| Reference revision | [`pins/tcontract-rs-v2.rev`](pins/tcontract-rs-v2.rev) — what `status` is measured against |
| Design record | [`docs/worklog.md`](docs/worklog.md) — decisions, fixed failures, open items |

## How it works

The harness lives in tcontract-rs (`benchmarks/benchmarks/tcbench`) and is built
**out of the same checkout as the library it measures**, into a target directory
keyed by that commit. A harness built from this repository could silently
measure a different revision of the library than the one it was written against;
building it in place makes the recorded commit describe both.

```bash
./scripts/setup_v2_extern_deps.sh                     # clone tcontract-rs at pins/tcontract-rs-v2.rev
./scripts/setup_v2_extern_deps.sh /path/to/checkout   # or symlink a local checkout

# record one cell: build, verify, measure, validate, publish, reindex
# (the TBLIS row needs its provider payload first; see docs/v2-layout.md)
python3 scripts/v2/record_run.py tcbench zen5-cpu tcbench --external-provider-json target/tblis-providers.json

# check that the committed index is what the generator produces
python3 scripts/v2/gen_index.py tcbench --check
```

## What this repository is not

It is not the library's per-PR suite. tcontract-rs keeps its own rows at 1T and 4T,
its harness scripts (`benchmarks/scripts/{pinned.sh,idle_cpus.py}`) and the
`tcontract-benchmark` skill; this repository owns the campaign: the declarations,
the revision pin, the run manifests, the index and the published reports.
