# tcontract-benchmark

The benchmark campaign for [tcontract-rs](https://github.com/tensor4all/tcontract-rs):
results keyed by **library commit × hardware profile**, with the staleness of
every cell visible rather than implied.

| | |
|---|---|
| Latest results | [`result/INDEX.md`](result/INDEX.md) — generated table of contents over the per-revision pages |
| Result layout | [`docs/results.md`](docs/results.md) |
| Timing policy | [`docs/timing-policy.md`](docs/timing-policy.md) |
| Reference revision | [`pins/tcontract-rs.rev`](pins/tcontract-rs.rev) — what `status` is measured against |
| Design record | [`docs/worklog.md`](docs/worklog.md) — decisions, fixed failures, open items |

## How it works

The harness lives in tcontract-rs (`benchmarks/benchmarks/tcbench`) and is built
**out of the same checkout as the library it measures**, into a target directory
keyed by that commit. A harness built from this repository could silently
measure a different revision of the library than the one it was written against;
building it in place makes the recorded commit describe both.

```bash
./scripts/setup_extern_deps.sh                     # clone tcontract-rs at pins/tcontract-rs.rev
./scripts/setup_extern_deps.sh /path/to/checkout   # or symlink a local checkout

# record one cell: build, verify, measure, validate, publish, reindex
python3 scripts/record_run.py zen5-cpu tcbench

# check that the committed index is what the generator produces
python3 scripts/gen_index.py --check
```

## What this repository is not

It is not the library's per-PR suite. tcontract-rs keeps its own rows at 1T and 4T,
its harness scripts (`benchmarks/scripts/{pinned.sh,idle_cpus.py}`) and the
`tcontract-benchmark` skill; this repository owns the campaign: the declarations,
the revision pin, the run manifests, the index and the published reports.
