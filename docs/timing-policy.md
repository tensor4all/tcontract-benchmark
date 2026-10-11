# Timing policy, version 1

Recorded in every `run.yaml` as `timing_policy`. A run carries the version in
force when it was taken; do not compare ratios across versions, and do not use
an earlier version's numbers to assess a later library revision.

## What is timed

Steady-state operation execution. Inputs, layouts, plans, pools and provider
handles are prepared before the clock starts. The clock stops after the
operation and its completion synchronisation, with outputs still alive.

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
