# Timing policy, version 1

Recorded in every `run.yaml` as `timing_policy`. A run carries the version in
force when it was taken; do not compare ratios across versions, and do not use
an earlier version's numbers to assess a later library revision.

## What is timed

Steady-state operation execution. Inputs, layouts, plans, pools and provider
handles are prepared before the clock starts. The clock stops after the
operation and its completion synchronisation, with outputs still alive.

## What a ratio means

The engine rows are timed at the granularity their API offers, so a ratio between two of them is
a **throughput** ratio, not a per-call one:

- `plan` and `packed` time one execution of a `Plan` built before the clock. Per call the operation
  costs `prepare_s + seconds`; the recorded row is the per-iteration cost of a program that performs
  the same contraction repeatedly, with the same shape and layout each time.
- `ttgt` and `tblis` time one call of their own entry point. `ttgt` has its scratch and its
  M/N/K tables prepared outside (`prepare_s`), and nothing analytical excluded; `tblis` exposes no
  prepared contraction at all, so the analysis it performs on every call is inside its number and
  there is no separate figure to add.

For a fixed problem let `P` be the plan's construction, `E` one prepared execution, `A` the
reference's own per-call analysis and `K` its execution. A program that performs the contraction
`N` times costs `P + N*E` against `N*(A + K)`; per iteration that is `P/N + E` against `A + K`.
At `N = 1` the prepared side is `P + E`, and as `N` grows the `P/N` term vanishes and it tends to
`E`. The rows are therefore compared at `N -> inf`, and they are not the same quantity at
`N = 1` — an accidental equality at some finite `N` says nothing about either limit. Every row
carries `prepare_s` in the raw `run*.csv`, so the per-call figure is recoverable without a
re-run.

The excluded work is not always small. Across the committed v2 cells, `prepare_s` for the library
rows is 1.2-2.2% of the timed call at the median on `tcbench`, but 137 and 229 of its 588 rows sit
above 5% (worst 128%); 41 of 288 `qcbench` rows are above 10%; and on `per-shape` the median share
is 54-65% (worst 664%). On that last suite the ratio reports what a loop of small contractions
costs, not what one call costs.

## Priming

At least 1.5 s of untimed, time-based priming per arm, and the same amount on
every arm. A fixed call count is not equivalent: after an idle gate this host
reads up to 25% low for the first 1-2 s of sustained AVX-512 work (measured:
39.8 GFLOP/s for a kernel that reads 52.6 once warm). A count-based warm-up also
biases a ratio when the two arms have different durations.

**0.5 s was too short**, and not only as a ratio: on a case whose call is about
2 ms, the arm measured first read 40% low (2.89 ms against 2.06 ms settled) and
the arm measured after it looked 29% faster than the same work measured on its
own. Every cell compares engines measured in one process in a fixed order, so the
arm measured first — always `plan` — was the one penalised, and a pair that
resolves to the same driver and grid differed by 27% where it must agree. At
1.5 s the dependence on position disappears (verified at 3 s as well) and the
same pair agrees. Two arms that resolve to the same driver and grid are the
built-in check of this paragraph.

## Statistic and repetitions

`best` wall time per engine and case, over 5 repetitions, with the complete set
repeated for A/A when a comparison is being made. A scan flags suspects; only a
complete paired run makes a performance claim.

## Guarding the host

Every measurement runs through `benchmarks/scripts/pinned.sh` of the measured
checkout: `taskset` to the declared CPU set, a 3-second `/proc/stat` idle window,
at most 5% busy before and after, 3 attempts. A spoiled run is discarded, not
published. The check covers the declared CPUs **and the SMT siblings their
physical cores share** (tcontract-rs#79): a busy sibling contends with the core
being measured and is invisible in that core's own counters, so a run can
otherwise pass the gate while sharing a core with someone else's work. The guard
log says which CPUs it expanded to.

The manifest states the priming the *harness* reported, not the value the
recorder asked for (`run` echoes it; tcontract-rs#78), and the harness's stdout is
kept next to the guard log so a reader can check the claim.

## What a report may and may not claim

A report states the revision, the host, the coverage and the guards, and it is a
claim about *that* cell. It is not evidence about a population the run did not
contain: a corpus whose cases all have unit batch extent says nothing about
per-batch-element cost, and the index's `coverage` column is the mechanism that
keeps that visible.
