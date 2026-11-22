# `zqcbench` on `epyc-9575f`

- tcontract-rs commit: `807183f57ce77622f0af197b8c4fa3dced9a84c5`
- features: `tblis`
- tprims rows: `tprims` (the provider in the measured revision; see library above)
- external providers: `tblis` 2.0 @ `b16a732939d8454021e0a0f0097cf1cc1dd3ab19` tag `v2.0-beta2` sha256 `a7ddb0fba1fcaf1d5b5661e2e3e9bdfaa6e718db48d692be4e1e98ce6dc09970` (TBLIS 2.0, configuration skx; bundled BLIS 358e689cadd6757f564a2992cf46a2f7d6fa6bb0; built with ./configure --prefix=/home/ningyuan/projects/t4a_bench/workspace/tcontract-benchmark/target/tblis-v2.0-beta2 --with-blis-config-family=skx (cmake, Unix Makefiles, Release); libtblis.so sha256 a7ddb0fba1fcaf1d)
- harness commit: `633af61544120e8dde5783e0010aff1fab20ee09`
- toolkit commit: `ccb3da4650aade26b210de534dee368be419575b`
- measured binary SHA-256: `b0bf0ff83c453ca51b83bbb1fbc88ee8fe8d7ef567b7e8d04f4b831ad412eeba`
- hardware profile: `epyc-9575f`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-11-17T11:11:58.132461Z`
- timing policy: v2, median of 5 reps, priming 1500 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/v2/record_run.py zqcbench epyc-9575f zqcbench --external-provider-json target/tblis-providers.json --reps 5 --aa 2 --prime-ms 1500 --label pub-20261117-zqcbench`
- raw data: `data/v2-results/zqcbench/epyc-9575f/zqcbench/20261117T083842Z-pub-20261117-zqcbench/`

## What was measured

- **Workload** — One binary (two-operand) contraction per case, transcribed from ten complex-orbital paper routes at fixed occupied/virtual/auxiliary extents: three two-component spinor routes (X2CAMF CCSD/EOM, two-component RI-JK), five periodic k-space routes (periodic CCSD, GDF-HF, GW, BSE and the per-k-point AO-to-MO staging) and two molecular spatial routes (SO-MF/CPSCF and GHF/GKS response). The three ratios stand for the cc-pVDZ/cc-pVTZ/cc-pVQZ rung medians of a 5,239-molecule NAO statistics panel. One family (`ri-krgw/sigma.contract`) carries a batch index.
  Source: The corpus is defined by `benchmarks/benchmarks/zqcbench/corpus.rs` in the measured revision (`pins/tcontract-rs-v2.rev`); each case names the paper it was transcribed from in the corpus README, and the transcription material lives in the benchmark job's `out/complex_corpus/*/CORPUS.md`.
  Known blind spot: One binary contraction per timed call: permutations, denominators and forms with more than two operands are metadata, never separate timed cases.
  Known blind spot: Every case is c64; f64 is the real-orbital bench (`qcbench`), and the shared verifier's known-value fixture is a dedicated 12-MAC product, not a corpus family.
  Known blind spot: The extents are aspect-ratio classes derived from a 12 GiB whole-binary c64 budget, not a molecule; the binding case is the ao^4 exchange kernel `somf/cpscf.exchange_response` and the verify peak is A+B+2C (a blas build would add the TTGT arm).
  Known blind spot: The transcription is not machine-checked here: the corpus tests compare the literals against a second copy, not against the papers.
  Known blind spot: `tblis` is an external baseline linked from its own prefix (`TBLIS_ROOT`), not the measured checkout; its revision is recorded through the campaign TBLIS collector (`scripts/tblis_providers_json.py`).
  Known blind spot: The harness's census CSV carries no corpus `group` column, so the ratio classes are declared by this suite and the resolved extents remain facts of the measured revision's `corpus.rs`.
  Known blind spot: The library rows time one execution of a plan built before the clock, so a single call also pays the preparation recorded as `prepare_s` in the run CSV, and the ratio applies when the same shape and layout recur. Every other row times one call of its own entry point, and no reference here exposes a prepared contraction, so its per-call analysis is inside the time shown.
- **Rows** — one row per engine in every table below:
  - `plan` — This library with its planner choosing the route per case.
    Identity: the measured tcontract-rs revision in this run's manifest (`library.commit`), pinned by `pins/tcontract-rs-v2.rev`
    As measured: `tprims` (the provider in the measured revision; see library above)
  - `tblis` — Actual C++ TBLIS through the direct FFI adapter, as the independent third-party reference implementation. Pinned by release tag, not by a local revision.
    Identity: TBLIS v2.0-beta2 (the only tagged 2.0; its commit and the bundled BLIS revision are recorded per run, from `scripts/tblis_providers_json.py`)
    Caveat: Needs an install prefix (`TBLIS_ROOT`), and TBLIS 2.x builds through CMake. The page repeats the tag, commit, bundled BLIS revision and artifact hash the manifest recorded.
    As measured: `tblis` 2.0 @ `b16a732939d8454021e0a0f0097cf1cc1dd3ab19` tag `v2.0-beta2` sha256 `a7ddb0fba1fcaf1d5b5661e2e3e9bdfaa6e718db48d692be4e1e98ce6dc09970` (TBLIS 2.0, configuration skx; bundled BLIS 358e689cadd6757f564a2992cf46a2f7d6fa6bb0; built with ./configure --prefix=/home/ningyuan/projects/t4a_bench/workspace/tcontract-benchmark/target/tblis-v2.0-beta2 --with-blis-config-family=skx (cmake, Unix Makefiles, Release); libtblis.so sha256 a7ddb0fba1fcaf1d)

## Hardware

- CPU: `AMD EPYC 9575F 64-Core Processor`
- logical CPUs: `128`
- L3: `256 MiB (8 instances)`
- L3 domains: `32 MiB per 8-core CCX (CPUs 8k-8k+7 plus SMT siblings 8k+64-8k+71), 8 CCXs`
- OS / arch: `Linux 6.8.0-147-generic` / `x86_64`
- hostname: `ps`
- CPU sets: 1T -> `0`, 4T -> `0-3`

Every timed cell matches a successful verification census, including operation variants.
Each cell is median of process medians ± sample SD of those medians; W is the median
within-process sample SD. All values are milliseconds. These are descriptive spreads,
not confidence intervals. The between-process spread includes the rotating-order schedule.
Each process retains 5 chronological calls; 2 complete process sets are recorded.
Spread guide (computed from this run's own rows): per-engine between-start range median 0.33%, worst 12.00% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 11 of 420 engine cells exceed 5% and carry `!`; median within-process relative SD 0.09%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
The `vs plan` column is the rotation-averaged ratio
exp(mean over starts of log(engine median / plan median)),
with the per-start ratios beside it: `R > 1`
means the engine was slower than that first-declared row in that start. It removes a
row-position
effect only under one position effect shared by the engines and stable across starts,
and only where every declared engine has a measured row (`*` marks a cell where one has
no row, so no ratio there is position-balanced). `!` marks a cell where some engine's own
per-start median range exceeds 5% of its median, and `p` a balanced cell whose estimated
position-effect ratio exceeds 1.05. Flagged cells are retained, not discarded; the
between-start variation can exceed the difference being compared.
The `vs` columns mark only differences larger than the spread this run recorded for those
two rows (combined between-start SD, floored at 5%), always with the measured library as the subject:
`🔵 <row> X faster than <row>` / `🔴 <row> X slower than <row>` (the subject is the first column of the table, the compared row is named in
the cell, not only in the column header), `·` inside the band, `-` that row is not
measured in this arm. `notes` carries the cell warnings (`*` a declared row has no measurement,
`!` between-start range over 5%, `p` position effect over 5%, dispatch-dominated means the
row is under 20 us so 4T/8T pay thread-region start-up). Per-start ratios and every
chronological sample are in the run directory named at the top of this page (`run*.csv`).
These describe the recorded revisions; they are not a regression claim.

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
