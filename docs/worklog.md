# Work log

Design decisions, what was rejected, and what is still open. Measurements live
in `result/`; this file holds the reasoning.

## 2026-10-19 — the v2 campaign runs on the shared toolkit

The toolkit pin moves from a feature-branch revision to its main (`95caeef`), which carries the
control decision on the unchanged row's median, the observer's affinity recorded in
`threads.observer`, the ancestor pin check and the shared merge procedure. `scripts/v2/` was already
a set of thin shims selecting one of this repository's two descriptors by campaign id, so the pin was
the only thing left between this campaign and the rest.

Dry run, `--no-publish`, one thread, `f64`, four process sets (four engines need a multiple of four),
`target/tblis-v2.0-beta2` as `TBLIS_ROOT` for the external provider's identity:

```
scripts/v2/record_run.py tcbench zen5-cpu tcbench --threads 1 --dtypes f64 \
    --aa 4 --reps 2 --prime-ms 250 --external-provider-json <tblis.json> --no-publish
```

Built `tcbench` out of `extern/tcontract-rs-v2` at the pinned revision, verified the grid, timed 784
rows across `plan`/`packed`/`ttgt`/`tblis`, wrote and validated `run.yaml`, and produced a report
without publishing it: `data/v2-results/tcbench/zen5-cpu/tcbench/20261019T091003Z-v2-dry-run/`.

The recorder refused the first attempt with "v2 requires clean, committed toolkit and harness source"
because the pin edit was uncommitted - the same check that guards every other campaign. No timing
was published from either attempt.

## 2026-10-13 — the gate is content only, and the smoke build is gone

**What CI did.** Every PR ran `index` (the declarations, every recorded manifest, the generated
index) and `smoke`, which built the pinned harness the way the recorder does -- `tcbench` and
`lukbench` out of `tprims-rs` -- ten to sixteen minutes, twice per push of a recording branch because
the workflow fires on `push` as well as `pull_request`. It duplicated work that has already happened
by the time a PR exists: `scripts/record_run.py` builds, verifies and times that same revision on the
host that owns the numbers, and publishes nothing unless all three succeed. The harness is also a
workspace member of `tprims-rs`, whose own CI builds it for every PR there.

**What replaces it.** One job, `index`, on `ubuntu-slim`: the suites and profiles against their
schemas, every `data/results/*/*/*/run.yaml` against `validate_run.py`, and `gen_index.py --check`.
It is the only required status check on `main`, and auto-merge is enabled, so a recording or
documentation PR merges by itself once the content is consistent. Superseded runs on the same branch
are cancelled instead of queued.

**What this repository no longer checks.** That the pin builds -- see the argument above: a recording
cannot exist without that build, and a pin moved by hand still shows up as a stale or missing cell in
the index, which is the check that stays.

## Why the campaign is a separate repository

`tprims-rs` had one tracked report per `(profile, suite)` under a results
directory. Each file was self-describing, but the set of them was not: a cell
that had not been re-measured kept its old file, and a reader saw a commit hash
and a table without being able to tell whether it reflected the current library.
Staleness was carried in prose in the README, which no check can fail.

That is the same class of mistake that produced a retracted performance claim
during this work: two sides of a comparison measured at effectively different
revisions, and no way to see it from the numbers.

## Decisions

**The harness is not moved.** `tprims-benchmark` builds `tcbench` out of a
pinned checkout of `tprims-rs` with `--manifest-path`, rather than owning a
crate. Two reasons, in order of weight:

1. A result's recorded commit has to describe *both* the library and the
   harness. Building the harness from the measured checkout makes that true by
   construction; a harness living here could be built against a different
   revision of the library than the one it was written for.
2. A path dependency on a package that belongs to another workspace does not
   resolve: Cargo applies `workspace = true` inheritance against the *consuming*
   workspace root, so `extern/tprims-rs/benchmarks` failed to load with
   `stub: dependency.strided-basic was not found in workspace.dependencies`.
   This was verified, not assumed.

**Revision pinning without published crates.** `extern/tprims-rs` is a symlink
produced by `setup_extern_deps.sh`; `build_for_tprims_rev.sh` re-points it and
builds into `target/tprims-rev/<rev12>[-dirty]` with `RUSTC_WRAPPER=` cleared.
Baseline and candidate can never share compiled library artifacts. This came
from a concrete failure: a measurement was once taken from a binary that did not
contain the change under test, because two source trees shared a target
directory.

**Pages are keyed by revision, not by cell.** `result/<profile>/<suite>/<rev>.md`.
Measuring a new commit adds a page; the previous one is not overwritten, so the
tree keeps the history the index links to. A dirty checkout gets its own page.

**`behind` counts invalidating commits.** Each suite declares `invalidated_by`
source paths and a `stale_after` threshold. A documentation change does not make
a kernel result stale, and a counting rule that could not tell the difference
would be ignored in practice.

**Coverage is a column, not an apology.** The campaign is not run in full on
every profile for every commit. A partial run is recorded, marked `partial`, and
never displaces a full-coverage page.

## Failures found and fixed while building this

**The index was not deterministic.** It stamped the wall clock, so a freshly
generated file never matched the committed one and `--check` could not be exact;
CI failed on it. It now records the newest *recorded run* timestamp.

**Manifests recorded the measuring host's path.** `tprims.path` was
`/home/shinaoka/...`, so a committed manifest could not be verified anywhere
else and CI rightly rejected it. A manifest that only validates on the machine
that produced it is not evidence. `tprims` now requires `url` and `commit`, and
treats the local path as informational `measured_path`; validation resolves the
commit in a checkout that exists *here*, with a negative control that an
unresolvable commit fails.

**A partial run could look as good as a full one.** The first version of the
index showed commit/date/status but not what the run had covered. Found by
recording a smoke run and noticing it was indistinguishable from the full one.

## Open, not done

- **A corpus derived from application shape logs.** `tenferro-benchmark` already
  produces one (`TPRIMS_SHAPE_LOG` plus its `scripts/tprims_shape_corpus.py`,
  keeping shape groups up to a 95% time share plus the most frequent others).
  Re-implementing that consumer here would duplicate a tool owned by the
  repository that produces the logs; the right move is to consume its output as
  another declared suite. Until then, the TCCG corpus is the only workload, and
  it has a known blind spot: all 49 cases have unit batch extent, so
  per-batch-element cost is invisible in it.
- **The campaign is one host again, deliberately.** `epyc-cpu` was declared from the
  first commit as the second profile, an old shared 64-core workstation used for spot
  checks, and it was never measured: the cell would cost a full run on a machine whose
  load the campaign does not control. It is retired (2026-10-09) rather than left as a
  permanent `missing` row. A future machine is a new profile with its own name and its
  own L3 description, not a revival of this one.
- **`tprims.version` is recorded as null.** `tprims-rs` is unpublished; the field
  exists so a versioned project's pages are keyed by version as well as commit.
- **TBLIS is retired from the declaration.** It was the third-party reference arm,
  but it needs an external install (`TBLIS_ROOT`) and an unpublished local
  revision to say what it measured, which tied every cell to one host's
  installation. The `zen5-cpu` cell records `plan`, `packed` and `upstream`; the
  page that did measure TBLIS keeps its column, because evidence is immutable.
  The harness keeps the feature, so a cell can declare it again. tenferro-rs
  retired its own TBLIS extension in the same week (tenferro-rs#2004).

## A run discarded, and one rule tightened

A measurement was taken while `extern/tprims-rs` sat on the merged-PR head
`1e0bf3c`, not on `main` (the merge was a squash, so the head is not an ancestor
of `main`). Its page would have been `diverged` against the reference and failed
the index check for a required cell. The run and its page were discarded rather
than published, and the pin now points at `main`; the discarded revision is
recorded here because the fact that it happened is worth more than the file.

`invalidated_by` listed `benchmarks/**`, which made a README edit mark every
measurement stale. It now lists only paths whose change can alter a measured
result: the three library crates, the harness directory, the shared harness
library, and the two manifests that decide features and dependencies. A rule
that cannot tell a documentation change from a kernel change is a rule nobody
follows.

## Evidence is immutable, declarations are not

Adding the `tblis` arm to the declaration broke a manifest that had been correct
when it was written: `validate_run.py` recomputed `covers_declared_suite`
against the *current* declaration and disagreed with the recorded value. CI
caught it, and the fix is not to relax the check but to record what the manifest
was measured under.

`run.yaml` now carries `suite_sha256`, the declaration's hash at measurement
time. A manifest whose hash differs from today's declaration is checked for what
can be checked (schema, profile, suite, CPU sets, resolvable commit) and noted as
drifted; its declaration-derived claims are not re-judged, because the
declaration it was written against cannot be reconstructed. Manifests recorded
before the field existed carry the same notice.

`coverage` in the index now relates a page to the *current* declaration:
`full`, `partial`, or `declaration-changed` when the declaration moved after the
measurement. The older page for `0aeb77dd6728` shows the last of these, which is
the truth: it was measured against a three-arm declaration, and today's has four.
The newest page was re-measured after the declaration settled so that it is
`full`, not because the earlier number was wrong. Retiring the TBLIS arm moves
that newest page back to `declaration-changed` again, which is the same
statement about a different pair of declarations: four arms then, three now.

The same change fixed a smaller semantic bug: `harness.commit` had been
recording the *measured* checkout's commit, which merely duplicated
`tprims.commit`. It now records this repository's commit, which is what
distinguishes one reporting pipeline from another.

## The manifest stopped stating what the harness did not do

Two claims in every `run.yaml` were the recorder's own defaults rather than the
run's report: `minimum_untimed_priming_ms` and the guard's window, threshold and
attempt budget. They happened to be right, which is the worst kind of wrong — a
reader had no way to tell a stale record from a live one, and a `--prime-ms` or
`PINNED_*` override during a run would have made the manifest describe a policy
nobody applied. tprims-rs had the other half of the same gap: the campaign
recorded 500 ms of time-based priming while the harness did exactly one warm-up
call (tprims-rs#78), and the guard checked the declared CPUs without their SMT
siblings, so a busy sibling could share the measured physical core invisibly
(tprims-rs#79).

Both sides now meet in the middle:

- the measured checkout's harness prints what it applies (`N ms priming` is on
  `run`'s banner) and its guard echoes the policy it used (`pinned.sh: cpus=...
  idle_window=3s max_busy=0.05 retries=3`) together with the per-CPU report that
  names each SMT sibling it checked;
- the recorder passes `--prime-ms`, keeps each run's stdout as
  `run<N>-<size>m-<T>t.out`, reads the priming and the guard policy out of those
  two lines, requires every run in a cell to agree, and **refuses a measured
  checkout that reports neither** — that is the check that keeps the pin honest,
  because a checkout predating those banners cannot produce a trustworthy
  manifest;
- `guards` gained `outputs` (the retained stdout) and `notes` (the sibling
  coverage), both optional, so every previously recorded manifest still
  validates.

The pin moved to `e42f6af` and the `zen5-cpu`/`tcbench` cell was re-measured
under the three-arm declaration, so the cell is `full` and `current` again and
the first cell in this repository whose manifest's priming and guard are read
back from the run. What that cell does *not* establish: it is a single complete
set (`aa: 1`), so it carries no A/A, and the retired TBLIS column in the older
page stays as measured.

## 2026-10-09 the campaign loses its third arm, its third width and its second size

Four retirements, all of them about paying twice for the same answer.

- **TBLIS is retired** (`tcbench`'s fourth arm; the declaration change is the
  `2026-10-09` commit "declaration: retire the TBLIS arm", and the harness followed).
  It was the third-party reference, but it needed an external install and an
  unpublished local revision to say what it measured. It comes back pinned by release
  tag for the per-shape suite, where an independent reference earns its place, and not
  for `tcbench`.
- **The `upstream` arm (tensorprimitives-rs) is retired everywhere**, code and Cargo
  feature with it. It is the project this library was extracted from, so it is a
  lineage baseline rather than an independent one, and the measured cells say it
  nearly always loses: on the per-shape corpus `tprims [plan]` is ahead in 42 of 42
  rows, and on the TCCG corpus in 283 of 294. The exceptions are small and are recorded
  rather than hidden: `ij-ik-kj` at 1T, where the planner takes 1.26x the upstream time,
  and twelve more rows within 1.15x. Losing the arm loses the only external comparison
  `tcbench` had; the per-shape suite keeps TBLIS for that.
- **`tcbench` is measured at one size, two widths and two arms** (`tprims [plan]`,
  `tprims [packed]`). Its 49 rank-3-to-6 contractions are the only irregular-stride
  work in the campaign, so the corpus stays; the 8-thread width, the 1 MiB size and the
  third arm each cost about a third of a run to answer a question another row already
  answers. The first cell under the old declaration took 30 minutes
  (`20261009T080245Z`: 08:02:45 to 08:32:16), of which 7.4 minutes was priming and
  42 seconds one `verify` at 16 MiB; the reduced cell is a few minutes.
- **`lukas` is renamed `per-shape`.** The suite was named after the person whose figure
  it reconstructs, which is not what an identifier is for: the corpus's own property is
  that its cases *are* the shapes, one size each. The attribution stays where provenance
  belongs, in the suite's `corpus.source` field, `experiments/three-engine-contract/`
  and the harness's own documentation.

Engine columns are now labelled for a reader (`tprims [plan]`, `tprims [packed]`,
`tblis`) while the CSVs keep the machine-readable ids (`plan`, `packed`, `tblis`): a
suite declares the label, `report_run.py` prints it, and nothing about the data
changes. The old `lukas` page and its raw run are removed rather than orphaned — the
suite id no longer exists, so no index would reference them, and the commit that
created them keeps their history.

## 2026-10-09 the arm measured first was the slow one, and it was always `plan`

Every cell here compares engines measured in one process, per case, in the fixed
`ENGINE_ORDER` that puts `plan` first. The priming was 500 ms per arm, which the
timing policy allowed ("at least 0.5 s") and which is not enough for a short call.

Measured on `ij-ik-kj` (f64, 1 MiB, 1T, about 2 ms per call), through the measured
checkout's own guard:

| priming | pair in one process | `plan` alone | `packed` alone |
|---|---|---|---|
| 500 ms | plan 2.885, packed 2.210 | 2.893 | 3.084 |
| 1500 ms | plan 2.060, packed 2.202 | 2.061 | 2.206 |
| 3000 ms | plan 2.058, packed 2.199 | 2.060 | 2.210 |

The first arm measured for a case read 40% low; the arm after it looked 29% faster
than the same work measured on its own. At 1.5 s the position dependence is gone.
The self-check is a pair that resolves to the same driver and grid, which must
agree: with 500 ms such a pair differed by 27% (`abcijk-ijma-mkbc`, c64, 1 MiB, 4T),
with 1.5 s it agrees (2.722 against 2.830 ms).

What this changes about what is already published:

- **The cells recorded before this fix are not comparable across arms.** Their
  absolute times for the first arm are inflated, and the later arms' are not. Both
  suites are re-measured at the new pin and priming; the older pages stay as
  history, marked `declaration-changed`.
- **The claim that `tprims [plan]` wins 283 of 294 rows against the retired
  `upstream` arm was measured with `upstream` last, i.e. advantaged.** That is an
  upper bound on tprims' wins, not a measurement; the arm has since been deleted, so
  it cannot be re-measured. The decision to retire it stands on its nature — the
  project this library was extracted from — rather than on that count.
- **The faer/packed sweep of `tprims-rs#69` has the same shape**: its arms run in a
  fixed order per case with 500 ms of priming, so its later arms were advantaged.
  Its conclusion is conservative in the safe direction (faer's measured advantage is
  a lower bound, and "no packed win at 1T" is robust), but its margins are not the
  margins of a fair comparison and are marked so in the decision log.

## 2026-10-10 TBLIS comes back to the tcbench cell, and the pages show the ratio

The `tcbench` suite had no independent reference: its arms were this library's
planner and this library's packed driver, so a reader could tell that one internal
route beat another and nothing about whether either is competitive. TBLIS is back
as the third arm, and both suites now publish `tprims [plan] / tblis` per case.

Why the retirement was reversed. The arm was retired when the record could not name
which TBLIS it had measured (`docs/worklog.md`, 2026-10-09). That is no longer true
of the *other* suite: `per-shape` builds TBLIS from a release tag with
`benchmarks/scripts/build_tblis.sh` and records the tag, the TBLIS commit, the
bundled BLIS revision and the artifact's sha256 in every run and page. The same
provenance now covers the tcbench cell, so the objection that retired the arm has
no object left.

What it costs: the tcbench cell grew from two arms to three (the third is TBLIS's
own verify pass plus 49 cases x 1.5 s of priming per thread count), so a re-record is
about 50% longer. That is the price of a comparison this project's claim rests on:
without it, "tprims is fast" has no outside referent.

What the pages gained. `report_run.py` adds one column, `tprims [plan] / tblis`, and
appends the largest `spread` among the rows behind it as `±x%`. The scatter is now
recorded per row in the CSV (`spread`, from tprims-rs#92) and shown beside the ratio,
because a ratio of 1.03 means nothing on a host whose own repetitions scatter by
tens of percent: on `ij-ik-kj` 1 MiB 1T the ratio is 0.80 in f64 and 0.92 in c64 with
a scatter of 0.1%, and a row whose ratio is inside its own `±` is not a result.

What the new cell says (zen5-cpu, `0ec98136c4c8`, 16 MiB, 1T and 4T, 49 cases x 2
dtypes = 196 rows). `tprims [plan] / tblis` has a median of 0.833 and a minimum of
0.401, so the planner's choice is ahead of TBLIS on 180 of 196 rows. **On 16 rows it
is behind**, and on 14 of those the margin exceeds the row's own scatter, i.e. they
are not noise:

| case | dtype | T | plan/tblis | plan spread | tblis spread |
|---|---|---|---|---|---|
| `abjc-cbka-kj` | f64 | 4T | 1.524 | 3.8% | 14.3% |
| `adbjc-cbdka-kj` | f64 | 1T | 1.467 | 0.8% | 5.2% |
| `ajbc-ckba-jk` | f64 | 4T | 1.442 | 8.5% | 2.6% |
| `adbjc-cbdka-kj` | c64 | 1T | 1.416 | 1.3% | 1.2% |
| `abjc-cbka-kj` | f64 | 1T | 1.388 | 1.2% | 0.6% |

They are the cases whose output is transposed (`abjc-cbka-kj`, `ajbc-ckba-jk`,
`adbjc-cbdka-kj`, `ajbdc-ckbad-jk` — the rank-5 and rank-6 ones from CCSD(T) and
AO2MO), plus `ijk-il-jlk` in both dtypes at 4T. That is a concrete, reproducible
target for the next optimisation pass, and it was invisible while the suite had no
outside reference: the same rows show `packed` and `plan` within a few percent of
each other, so an internal comparison could only say that two tprims routes agree.
The two rows whose margin is smaller than their scatter, and the 109% scatter seen
on one row elsewhere in the cell, are recorded as such rather than dropped.

On the per-shape corpus the same ratio is 42/42 in tprims's favour, with a median of
0.042 and a minimum of 0.006 - tiny batched GEMMs and MPS chains, where TBLIS's
per-call setup dominates. The two corpora disagree because they ask different
questions, which is why both are published.

Where the 16 losing rows come from (measured after the cell, on the same binary and
the same host, each probe putting tprims and TBLIS in one process so the ratio is
free of session drift):

- **Not the planner's choice.** On every one of the 16, `plan` and `packed` agree to
  1.00 and the route is the packed driver. It has no alternative: the copy-free faer
  route requires each GEMM axis to be a contiguous group of its operands
  (`crates/tprims-contract/src/strategy/faer.rs`, `plan()` returning `None`), and
  these cases interleave contracted axes with output axes inside `A` - in
  `abjc-cbka-kj` the contracted `(a,b,c)` sits at axes 0, 1 and 3 - so the fusion
  fails and the planner records `Reason::NotFusable`. Raising or lowering
  `FaerLimit` cannot change that: faer is not disfavoured here, it is unavailable.
- **Not the gather/scatter path.** The rows report `regular_a`/`regular_b` of 1.00
  (0.67/1.00 for two of the c64 ones), i.e. the packing is regular panels, and the
  measured rows already ran the non-gathering writeback - `TCBENCH_WRITEBACK=fast` is
  the default and `gather` is what has to be asked for.
- **Not the blocking model.** `TCBENCH_BLOCKMODEL=analytical` against the shipping
  `legacy` constants: packed/tblis 1.554 against 1.541 (`abjc-cbka-kj` f64 1T),
  1.612 against 1.611 (`adbjc-cbdka-kj` f64 1T), 1.519 against 1.494, 1.684 against
  1.675 - no effect on any of the four probed.
- **Not the blocking values.** `TCBENCH_{MC,NC,KC}` at half and one and a half times
  the derived values move `packed` by at most 2.5% and leave the ratio between 1.51
  and 1.64.

What is left is the inner loop: tprims's `avx512.f64.real.24x8` and
`avx512.c64.planar.16x6` packed kernels against whatever BLIS drives through TBLIS's
TTGT formulation on exactly the shapes that cannot be fused. Closing that is
micro-kernel work, not a configuration change, and it is not attempted here; what
this record fixes is where the gap is and where it is not. On the per-shape corpus -
fusable, contiguous - the same comparison is 42/42 in tprims's favour with a median
of 0.042, which is why the two corpora are both published.

The per-shape cell is recorded twice end to end (A/A, `aa: 2`), because a ratio
needs a noise floor before it can be read. Same condition measured twice, 126 rows:

| statistic | value |
|---|---|
| time ratio A2/A, median | 0.9987 |
| time ratio A2/A, p90 | 1.0160 |
| rows off by more than 3% | 22 of 126 |
| rows off by more than 10% | 2 of 126 |
| per engine, median \|ratio - 1\| | plan 0.6%, packed 1.0%, tblis 0.7% |
| per engine, worst \|ratio - 1\| | plan 4.9%, packed 8.2%, tblis 25.0% |

So a cell of this shape reproduces to about 1% in the middle with a tail to tens of
percent, which is the number that decides whether a row may be quoted: the two rows
of the tcbench cell whose margin is smaller than their own scatter are exactly the
kind this cannot separate. The tcbench cell is not repeated: it is now a three-arm,
20-minute cell and an A/A would be 40 minutes, so its rows carry the per-repetition
`spread` instead and the per-shape A/A stands as this host's measured noise floor.

The 2026-10-09 cells stay as history. They were recorded without the third arm and
without a per-row scatter, so their rows cannot be quoted against an outside
implementation and their cross-arm margins cannot be separated from noise; the two
cells in this change are the ones to read.

## 2026-10-10 why the reference looks slow in the per-shape cell: setup, not kernels

The per-shape cell reports `tprims [plan] / tblis` down to 0.006, i.e. "tprims is 170
times faster". That is true and it is not a statement about kernels: the reference
pays a fixed cost per contraction that the prepared path does not pay at all.

Measured from the cell's own rows, per contraction:

| corpus family | tprims [plan] | tblis | note |
|---|---|---|---|
| batched `ikb_knb_inb`, 1T | 0.019-0.23 us | **3.2-4.5 us** | the same for n=2 and n=16, and for batch 16 and 256 |
| MPS chain, 64 steps per call, 1T | 0.34-1.6 us | **4.5-6.7 us** | chi 4, 8, 16; at chi=64 the reference is 133 us/step, i.e. compute-bound |

A cost that does not move with the problem size is setup, and the ratio's median by
case size says the same thing: **0.016** below 1 us, 0.021 in 1-10 us, 0.054 in
10-100 us, 0.329 in 100 us-1 ms, **0.747** above 1 ms. Where the contraction is big
enough to be compute-bound the two libraries are close; where it is not, the column
measures how much cheaper it is to keep a plan than to call a library.

Why the boundary is asymmetric, and it is structural rather than a harness bug:
the timing policy excludes plan and descriptor construction, which is exactly what
`Plan` is for and why the harness can hoist it; TBLIS 2.0 exposes no prepared
contraction at all - `tblis.h` has `tblis_tensor_mult` plus C++ view wrappers, nothing
to hoist - so its analysis is necessarily inside the timed call. Both arms build only
descriptors inside the region (tprims a `StridedView` per step, the reference three
`tblis_tensor` headers per call).

The suite now carries this as a `known_blind_spot`, so the page says it beside the
column, and the cell is re-recorded for that declaration alone. The practical reading:
**use the per-shape column for small-contraction setup behaviour, and the tcbench
column - 16 MiB, 5-250 ms calls, where the same reference is at parity or up to 1.5x
ahead - for kernel efficiency.** That is also where the work to match the reference
belongs, and it is not a small-size effect.

## 2026-10-10 the preparation the timing policy excludes is now a recorded column

The policy excludes plan and descriptor construction, which is what lets the harness
build a `Plan` once and time only `execute`. That exclusion is the whole reason this
library looks fast on microsecond cases, and until now the record said nothing about
its size. The harness now times it and writes `prepare_s` per row (tprims-rs #96): the
plan for tprims's arms, the operand descriptors for the reference. Everything below is
measured at the pin of the cells that follow.

| case | arm | timed call | preparation |
|---|---|---|---|
| `abjc-cbka-kj` f64 1T, 1 MiB | plan | 0.57 ms | 137 us |
| `abjc-cbka-kj` f64 1T, 4 MiB | plan | 17.9 ms | 989 us |
| `abjc-cbka-kj` f64 1T, 16 MiB | plan | 38.3 ms | **1431 us** |
| `abjc-cbka-kj` f64 1T, 16 MiB | packed | 38.2 ms | 993 us |
| `mps_chain_L32_chi4` | plan | 0.023 ms | 59 us |
| `mps_chain_L32_chi4` | packed | 0.050 ms | **355 us** |
| `mps_chain_L32_chi4` | tblis | 0.308 ms | 23 us |
| `ikb_knb_inb_n16_b16` | plan | 0.0037 ms | 1.3 us |
| `ikb_knb_inb_n16_b16` | tblis | 0.071 ms | 0.6 us |

Three things follow, and the first two are new.

- **Preparation is microseconds per plan on the fixed-shape corpus**, about 1 us per
  step: 59-62 us for a 64-step MPS chain. That is the order the harness was designed
  around, and it is now visible per case.
- **On the smallest cases the preparation is larger than the whole timed call.** At
  `mps_chain_L32_chi4` the `packed` arm prepares for 355 us and then executes in 50 us,
  while the reference's entire one-shot call is 308 us. So the per-shape ratio on
  microsecond cases compares a prepared path with a one-shot call, and the blind-spot
  note the suite gained says exactly that with this number behind it.
- **On the TCCG corpus preparation scales with the problem** - 137 us at 1 MiB to
  1.43 ms at 16 MiB - so it is allocation or analysis proportional to the extents. It
  is 2.6-3.7% of that case's call, which is why the cells may exclude it, but a reader
  is entitled to the number rather than to the assumption that it is negligible.

What has not changed: what is timed. The exclusion stands; the record stops hiding
its size. The reference still cannot be helped here - TBLIS 2.0 exposes no prepared
contraction, so its analysis is inside the call and `prepare_s` for its rows is only
the descriptors it builds outside, 0.4-0.5 us per step.

## 2026-10-10 where the 1.5x against the reference lives: the packing, not the kernel

Sixteen TCCG rows lose to the reference by more than their own scatter. This is the
investigation that located them, run against the pinned sources and the pinned binary.

What the reference does, read from `/tmp/tblis-build-v2.0-beta2/tblis` (tag v2.0-beta2):
it classifies the labels into batch (A and B and C), contracted (A and B), m (A and C)
and n (B and C), folds each group into one strided multi-index
(`frame/3t/mult.cxx:79-125`), and then runs its own blocked loop with **BLIS's context** -
kernel set and blocking parameters - rather than calling BLIS's gemm: it registers its own
packing and gemm kernels into BLIS (`frame/1m/packm/packm_blk_bsmtc.cxx`,
`frame/3m/gemm/gemm_ker_bsmtc.cxx` carry `PACKM_BSMTC_UKR`, `GEMM_BSMTC_UKR`, plus a `dpd`
family) and calls BLIS's micro-kernel `gemm_ukr` from inside them. It has no superscalar
path: it always packs. BLIS's zen3 configuration selects `bli_dgemm_haswell_asm_6x8`
(6x8) and `bli_zgemm_haswell_asm_3x4` (3x4), far smaller register tiles than this
library's 24x8 and 16x6.

Three measurements, in the order in which they rule things out. All on this host, one
core of one L3 domain, best of 5, 1500 ms of priming per arm.

**1. Not the kernel.** `experiments/openblas-kernel` runs a production kernel inside this
library's driver, packers, blocking and write-back, so the only difference is the kernel.
With its priming fixed (it used one warm-up call per arm, which understated the arm
measured first - ours, because the default family is always first), the default kernel
wins on every shape:

| case | ours (`avx512.f64.real.24x8`) | OpenBLAS (`dgemm_kernel_16x2_skylakex`) | ratio |
|---|---|---|---|
| `gemm-1024-col` | 47.6 GFLOP/s | 29.1 | 1.64x |
| `gemm-92160x40x48-col` | 29.4 | 21.1 | 1.39x |
| `gemm-3456x3456x24-col` | 39.0 | 19.9 | 1.96x |

`gemm-92160x40x48-col` is the effective GEMM of the worst losing tensor case, and the
default kernel is 1.39x *ahead* there: swapping kernels would make that row worse.

**2. Not the configuration.** On `abjc-cbka-kj` f64 16 MiB at 1T:
`TCBENCH_BLOCKMODEL=analytical` gives 1.554 against 1.541 for the shipping constants;
`TCBENCH_{MC,NC,KC}` at half and at one and a half times the derived values move the
packed arm by at most 2.5%; `TCBENCH_ORIENT=ba` 1.653; `TCBENCH_WRITEBACK=gather` 1.581.
At 4T, `TCBENCH_PARTITION=4x1` gives 1.495 against the default's 1.522. Nothing here is
the lever.

**3. The layout is what costs, not the dimensions.** Same dimensions (m=92160, n=40,
k=48), same family, blocking and partition, best of 5:

| how the case was requested | packed | reference | ratio | packed GFLOP/s |
|---|---|---|---|---|
| `--stress none` (TCCG sizing) | 37.95 ms | 24.81 ms | 1.541 | 9.3 |
| `--stress ragged` (m=86151, n=39, k=47) | 21.23 | 31.11 | 0.675 | 14.9 |
| `--stress padded` (m=92160, n=40, k=48) | 20.09 | 20.04 | 1.014 | 17.6 |
| contiguous column-major GEMM of the same dims (`experiments/openblas-kernel`) | 12.02 | - | - | 29.4 |

The corpus's strides are the explanation. In `abjc-cbka-kj` the folded `m` axis is the
label `j`, whose stride in `A = abjc` is `a*b` - not 1 - and the contracted group `(a,b,c)`
has strides `(1, a, a*b*j)`: a strided, interleaved panel, where the experiment's case is
a contiguous matrix. Same dimensions, same kernel, 3.2x apart.

So the 1.5x is the **packing of strided folded axes** - what the reference implements as
its BLIS-registered block-scatter packing - and it is not a micro-kernel project. The
next measurement is to give the kernel A/B experiment the corpus's label sets (a tensor
`Problem` rather than a matrix), so the packing cost is isolated the same way the kernel
just was. Neither the `prepare (us)` column nor the suite's blind-spot note covers this:
it is a packing cost, not a setup cost.

### What the packing reads, axis by axis

The plan for `abjc-cbka-kj` f64 16 MiB 1T records its own axes, and they say why a
contiguous matrix of the same dimensions is not the same problem. The m group is **three
axes** - extents 48 x 40 x 48 - with `A`-strides (92160, 48, 1) and output strides
(1, 48, 76800); the contracted axis is a single 48 at `A`-stride 1920 and `B`-stride 1, so
`B` is a plain contiguous panel and the output is contiguous within 1920-element runs.
Only `A` is interleaved, and the packing has to read it as a blocked, strided pattern
(a is stride-1 in 48-runs, b steps by 48, c jumps by 92160) rather than as a matrix. That
is exactly the shape of read that the reference implements as a BLIS-registered
block-scatter packm kernel (`PACKM_BSMTC_UKR`).

Two more things are ruled out, in addition to the three above:

- **The output's write-back alignment is not it.** Forcing `align_c_lines: true` in the
  packed arm's configuration (a temporary patch, reverted; the rows confirm
  `policy=auto align=true`) leaves the case at 38.17 ms against 38.24 ms with the shipping
  `false` at 1T, and 13.43 against 13.58 at 4T. Rounding strip boundaries to C's 64-byte
  lines buys nothing here.
- **Nor is it the second operand.** `B` is contiguous for this case (`k` at stride 1,
  `n` at stride 48), and the output is contiguous in its runs; the interleaving is in `A`
  only.

### How the instrument itself was caught being wrong

The lead this record ends on - "the packing of strided folded axes" - is still a lead, and
the attempt to confirm it produced two corrections worth keeping, because the same mistake
is easy to repeat.

An isolated experiment (`experiments/openblas-kernel`, tprims-rs#98) rebuilt this case's
operand layouts from the plan's own axis record and measured four layout combinations. It
came out 3.3x faster than the cell (11.6 ms against 38.1 ms) with the *same* family and
blocking, which read as "a plan-level traversal decision is worth 3.3x" - and that is what
was reported. It was wrong: two of the `m` axes have equal extent (48 and 48), the
reconstruction swapped them, and the "corpus" variant was therefore *a different
contraction*. Its tell was a residual of 1.4 against its own compact pair, which the binary
had compared across differently permuted buffers and so could not see.

Built instead from the harness's own `la`/`lb`/`lc` - read from the sized case, not
reconstructed - the plan is **identical to the cell's** on every recorded field: family
`avx512.f64.real.24x8`, mr/nr 24/8, blocking 264/1536/256, `StaticGrid{pm:0,pn:0}`,
`align_c_lines: false`, and the same three `m` axes at `A`-strides (92160, 48, 1) with the
contracted axis at 1920. So there is no plan difference to exploit, the 3.3x is retracted
(tprims-rs#99), and the planner's axis ordering is **not** implicated.

Two things the corrected measurements do say:

- **The layout does not move this case.** With the true layouts, swapping `A` to a compact
  `[m, k]` matrix and the output to a compact `[m, n]` matrix changes the time by 4% at most
  (50.4-52.1 ms across four combinations). So the case is not simply "an interleaved panel
  is expensive"; `A`'s contracted axis sitting at stride 1920 inside the `b`/`c` plane
  (measured from the harness's `la`) is not, by itself, what the 1.5x is made of.
- **The isolated experiment is not yet a valid instrument for this case**: it is 1.37x
  slower than the cell (52 vs 38 ms) with the same plan, dimensions and layouts, because it
  calls `execute_slices` (view construction per call) where the harness calls `execute_raw`.
  Until that is closed, an experiment cannot attribute the cell's cost.

So the phase-share measurement the design review asked for - A pack, kernel, write-back,
setup, measured on the harness's own path - is still the next step, and no change to the
planner is justified by anything measured so far. The stride-alignment sensitivity stands on
its own: `--stress padded`, which only perturbs the leading dimension, is 1.9x faster
(20.1 ms) and `ragged` 1.6x (21.2 ms), against 38.0 ms at the TCCG sizing that rounds
stride-1 extents to multiples of 24.

## 2026-10-10 the packed driver gets a blocked outer traversal, and it pays exactly where the reference does

The lead the previous entry closed on - the packing of strided folded axes - is now a
change rather than a plan: tprims-rs#101 (merged `0df08df4`) gives the packed driver a
blocked outer traversal. A block spans the output's fastest axis whole times a line's
worth (8 elements of `f64`) along the operand's fastest axis, its tiles are permuted into
the output's order, and it is emitted once. When the packed operand and the output disagree
about which axis is fastest, today's slices hold the output's fast axis once per
`product_of_the_other_axes` rows, so no reordering can make the pack read a whole line; a
block that spans whole runs of both axes can.

**It is enabled by measurement, not by geometry.** Over the 98 tcbench rows at 1T, measured
with the path on and off in one session, the class that wins without ever losing is
`n <= 64 && k > n` - a thin output against a deeper contraction, `m*k` operand elements
against `m*n` output ones - on top of a single K slab, a single NC panel, `pm == 1 && pn ==
1` and a non-Direct family. Everything else keeps the old traversal, with `grid_elems`,
`block_rows` and `mc` taking their previous values.

**This cell confirms it independently.** Re-recording the cell at the new pin, `tprims
[packed]` against the previous revision:

| case | dtype | 1T | 4T |
| --- | --- | --- | --- |
| `abjc-cbka-kj` | f64 | 35.9 -> 26.1 ms (**x1.38**) | 12.80 -> 12.77 ms (x1.00) |
| `abjc-cbka-kj` | c64 | 66.4 -> 56.7 ms (**x1.17**) | 20.26 -> 20.12 ms (x1.01) |
| `adbjc-cbdka-kj` | f64 | 42.8 -> 29.6 ms (**x1.45**) | 16.25 -> 15.08 ms (x1.08) |
| `adbjc-cbdka-kj` | c64 | 70.0 -> 55.7 ms (**x1.26**) | 22.30 -> 20.89 ms (x1.07) |

The 4T rows are unchanged by construction: the path is serial. In the phase instrument the
mechanism is the pack: `pack_a` 28.8 -> 6.4 ms, against about 8.6 ms of added permutation and
per-block work. The class is also the one where the reference wins - over this cell's
earlier revision TBLIS wins 12 of its 24 `n <= 64 && k <= 48` rows and 4 of 168 elsewhere -
so this closes the gap where this library was furthest behind, and it does nothing on the
rows where it was already ahead.

An independent review of the finished diff (`gpt-6.1-sol`) found two memory-safety blockers
and both were real, which is why the eligibility is as narrow as it is: a Direct family
could compute into `D`, leave its grid slot unwritten and have the emitter read it (the
guard now tests `collect`, and Direct families are refused outright), and the grid
permutation walks every column of the grid while a column-group worker fills only its own
(hence `pn == 1`). It also caught an unenforced row budget - the panel and the grid are
sized from the block *rounded up to whole `MR` tiles* - and per-execute allocations in the
block enumeration, both now fixed, plus a phase account that was not a partition: those two
phases were removed again and the design document says what the `setup` remainder can and
cannot support.

What is not claimed: the 4T rows (serial only), the blocked path's zero-allocation claim
(resting on reading the code - `tests/packed_workspace_alloc` exercises a matrix multiply,
whose one folded row axis can never select this path), and any generalisation of the
eligibility beyond the class it was fitted to. The design record, including the corrections,
is `docs/design/blocked-outer-traversal.md` sections 9-14 in tprims-rs.
