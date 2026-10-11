# Result layout

`suite_id` identifies the workload; `target_profile` identifies the machine
(`benchmarks/profiles.yaml`). They are the two axes of every cell.

```text
data/results/<profile>/<suite>/<timestamp>/          raw: run.yaml, verify-*.txt, run*.csv, *.guard, report.md
result/<profile>/<suite>/<commit12>[-version][-dirty].md   one page per measured revision
result/INDEX.md                                      generated table of contents over those pages
```

A result page is one `(suite, hardware profile, measured revision)`, and it
carries that revision and the hardware itself: commit, version when the measured
project has one, features, harness commit, host CPU, logical CPU count, L3, OS
and arch, the CPU set used at each thread count, the timing policy, the providers
and the guarantees. Measuring a new revision adds a page rather than replacing
the previous one, so the tree keeps the history the index links to. A dirty
checkout gets its own `-dirty` page, because those numbers are not comparable
with a clean build of the same commit.

## run.yaml

Validated against `schemas/benchmark-run.schema.json` before it is written.
It records:

- the profile, suite, suite file, timestamp and the exact command;
- `tprims`: path, commit, dirty state, features of the checkout that was
  measured and that the harness was built from;
- `harness`: commit and dirty state;
- `build_jobs`: how many cargo jobs built that harness. It is not a measurement
  condition — the threads a run measured at come from its suite, and a build never
  overlaps a measurement — but it is recorded so a rebuild can match, and so a
  reader is not left guessing which of the two numbers was which;
- `host`: CPU, logical CPU count, OS, arch, L3 geometry;
- `threads`: the counts, the CPU set used for each, and the thread environment
  variables in force;
- `timing_policy`: version, priming, statistic, repetitions. The priming value is the
  one the harness reported in its banner, not the one the recorder asked for, so a
  manifest cannot claim a policy the measured checkout did not apply;
- `providers`: what was compared against, with versions or commits;
- `guards`: the idle window, the busy threshold, the attempt budget, the log files,
  and the harness output the priming was read from. The guard expands the declared
  CPUs with the SMT siblings their physical cores share, so a busy sibling fails the
  gate instead of sharing the measured core invisibly;
- `run_spec`: what this run covered, and whether that is the whole declaration. For a
  corpus with **fixed shapes** the suite declares `fixed_shapes: true` instead of
  `sizes_mib`, the runner is given no `--size`, and `sizes_mib` is empty: the size
  axis of the campaign does not apply to it;
- `providers[].tag` and `providers[].sha256`: the version tag a provider was pinned
  to, and the hash of the artifact that was linked, for a provider whose revision
  cannot be read out of the binary (a built C library, for example). Both optional.

## Index and staleness

`result/INDEX.md` is generated and has two tables: the newest full-coverage page
per cell with its currency, and every published page keyed by revision and
hardware. Its point is that reports are self-describing but the *set* of them
was not: with one tracked file per cell, a cell that has
not been re-measured keeps an old file, and a reader sees a commit hash and a
table without being able to tell whether that cell reflects the current library.

`status` is computed against `pins/tcontract-rs.rev`:

| status | meaning |
|---|---|
| `missing` | no run recorded for this cell |
| `current` | measured at the reference revision, or at a descendant |
| `N behind` | N commits touching the suite's `invalidated_by` paths lie between the measured revision and the reference |
| `stale` | as `behind`, but N exceeds the suite's `stale_after` |
| `dirty` | the measured checkout had uncommitted changes; never comparable |
| `diverged` | the measured revision is not an ancestor of the reference |

`behind` counts *invalidating* commits, not raw distance: a suite declaring only
`crates/` is not out of date because a document changed. `coverage` is `full`
when the cell was measured over the suite's whole declared spec and `partial`
otherwise; a partial run never displaces a full one.
