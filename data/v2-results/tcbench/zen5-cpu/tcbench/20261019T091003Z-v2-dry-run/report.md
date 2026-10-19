# `tcbench` on `zen5-cpu`

- tcontract-rs commit: `7738bf43a0684e7d6f0769444e846f215fec86ab`
- features: `blas, tblis`
- tprims rows: `tprims` (the provider in the measured revision; see library above); `openblas` (the provider in the measured revision; see library above)
- external providers: `tblis` 2.0 @ `b16a732939d8454021e0a0f0097cf1cc1dd3ab19` tag `v2.0-beta2` sha256 `de00bf1552c15f9c4a5d3157f02c149b81aef0909107c51cbb54ba4b8e9b5827` (TBLIS 2.0, configuration zen3; bundled BLIS 358e689cadd6757f564a2992cf46a2f7d6fa6bb0; built with ./configure --prefix=/home/shinaoka/projects/tensor4all/tcontract-benchmark/target/tblis-v2.0-beta2 --with-blis-config-family=zen3 (cmake, Unix Makefiles, Release); libtblis.so sha256 de00bf1552c15f9c)
- harness commit: `8a322be7b08391ddb882c1bdcfad7e53da17f590`
- toolkit commit: `95caeefa9ae7c8461ccdf75d3b65455d4ed799b0`
- measured binary SHA-256: `42465ca076ad7a6a4643426da240bc4a6e524198a842799c0e0d278c5b15982b`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-19T09:14:12.974814Z`
- timing policy: v2, median of 2 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/v2/record_run.py tcbench zen5-cpu tcbench --threads 1 --dtypes f64 --aa 4 --reps 2 --prime-ms 250 --external-provider-json /tmp/tblis-v2.json --label v2-dry-run --no-publish`
- raw data: `data/v2-results/tcbench/zen5-cpu/tcbench/20261019T091003Z-v2-dry-run/`

## What was measured

- **Workload** — One full tensor contraction per case, drawn from CCSD, CCSD(T), AO-to-MO integral transformation and tensor-times-matrix workloads. The cases are rank-3 to rank-6 contractions, so they exercise the packed driver's scatter path rather than a single matrix geometry.
  Source: The corpus is defined by `benchmarks/benchmarks/tcbench/corpus.rs` in the measured revision (`pins/tcontract-rs-v2.rev`), after Springer & Bientinesi, "Design of a High-Performance GEMM-like Tensor-Tensor Multiplication" (arXiv:1607.00145) and the accompanying HPAC/tccg benchmark set.
  Known blind spot: Every case is a full tensor contraction, not a matrix multiply; the declared `n` is a tensor-size spec, not a matrix dimension.
  Known blind spot: Every case has unit batch, so a cost proportional to batch elements is invisible.
  Known blind spot: `tblis` is an external baseline linked from its own prefix (`TBLIS_ROOT`, see `docs/v2-layout.md`), not the measured checkout; its revision is recorded through the campaign TBLIS collector (`scripts/tblis_providers_json.py`).
  Known blind spot: The harness's census CSV carries no corpus `group` column and no resolved extents, so the corpus's own group labels and its resolved geometry are not part of this declaration; they remain facts of the recorded revision's `corpus.rs`.
- **Rows** — one row per engine in every table below:
  - `plan` — This library, with its planner choosing the route per case: the packed driver, the copy-free faer path, or the elementwise path for an all-batch case.
    Identity: the measured tcontract-rs revision in this run's manifest (`library.commit`), pinned by `pins/tcontract-rs-v2.rev`
    As measured: `tprims` (the provider in the measured revision; see library above)
  - `packed` — This library with the packed driver forced instead of chosen. A diagnostic arm: it shows what the planner's other routes buy or cost on the same inputs.
    Identity: the measured tcontract-rs revision in this run's manifest (`library.commit`), pinned by `pins/tcontract-rs-v2.rev`
    As measured: `tprims` (the provider in the measured revision; see library above)
  - `ttgt` — Transpose-transpose-GEMM-transpose against the CBLAS-compatible BLAS the harness linked: permute the operands into dense matrices, call GEMM, permute the result back. An engine row, not a vendor arm.
    Identity: the OpenBLAS the harness linked, read from the harness's `info` output
    Caveat: The transposition is the naive gather, so this is an upper bound on TTGT's cost rather than a tuned HPTT implementation.
    As measured: `openblas` (the provider in the measured revision; see library above)
  - `tblis` — Actual C++ TBLIS through the direct FFI adapter, as the independent third-party reference implementation. Pinned by release tag, not by a local revision: `benchmarks/scripts/build_tblis.sh` of the measured checkout builds it from the tag and writes the PROVENANCE this repository records.
    Identity: TBLIS v2.0-beta2 (the only tagged 2.0; its commit and the bundled BLIS revision are recorded per run, from `scripts/tblis_providers_json.py`)
    Caveat: Needs an install prefix (`TBLIS_ROOT`), and TBLIS 2.x builds through CMake, so the prefix cannot be made inside a bare checkout. The page repeats the tag, commit, bundled BLIS revision and artifact hash the manifest recorded.
    As measured: `tblis` 2.0 @ `b16a732939d8454021e0a0f0097cf1cc1dd3ab19` tag `v2.0-beta2` sha256 `de00bf1552c15f9c4a5d3157f02c149b81aef0909107c51cbb54ba4b8e9b5827` (TBLIS 2.0, configuration zen3; bundled BLIS 358e689cadd6757f564a2992cf46a2f7d6fa6bb0; built with ./configure --prefix=/home/shinaoka/projects/tensor4all/tcontract-benchmark/target/tblis-v2.0-beta2 --with-blis-config-family=zen3 (cmake, Unix Makefiles, Release); libtblis.so sha256 de00bf1552c15f9c)

## Hardware

- CPU: `AMD Ryzen AI 9 HX 470`
- logical CPUs: `24`
- L3: `24 MiB (2 instances)`
- L3 domains: `0-3: 16 MiB shared; 4-11: 8 MiB shared`
- OS / arch: `Linux 7.0.0-38-generic` / `x86_64`
- hostname: `shinaoka-EVO-X1Pro`
- CPU sets: 1T -> `4`

Every timed cell matches a successful verification census, including operation variants.
Each cell is median of process medians ± sample SD of those medians; W is the median
within-process sample SD. All values are milliseconds. These are descriptive spreads,
not confidence intervals. The between-process spread includes the rotating-order schedule.
Each process retains 2 chronological calls; 4 complete process sets are recorded.
Spread guide (computed from this run's own rows): per-engine between-start range median 1.37%, worst 12.74% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 22 of 196 engine cells exceed 5% and carry `!`; median within-process relative SD 0.19%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
The `vs plan` column is the rotation-averaged ratio exp(mean over starts of
log(engine median / plan median)), with the per-start ratios beside it: `R > 1`
means the engine was slower than that first-declared row in that start. It removes a
row-position
effect only under one position effect shared by the engines and stable across starts,
and only where every declared engine has a measured row (`*` marks a cell where one has
no row, so no ratio there is position-balanced). `!` marks a cell where some engine's own
per-start median range exceeds 5% of its median, and `p` a balanced cell whose estimated
position-effect ratio exceeds 1.05. Flagged cells are retained, not discarded; the
between-start variation can exceed the difference being compared.
The `vs` columns mark only differences larger than the spread this run recorded for those
two rows (combined between-start SD, floored at 5%), always with the fork as the subject:
`🔵 fork X faster than <row>` / `🔴 fork X slower than <row>` (the compared row is named in
the cell, not only in the column header), `·` inside the band, `-` that row is not
measured in this arm. `notes` carries the cell warnings (`*` a declared row has no measurement,
`!` between-start range over 5%, `p` position effect over 5%, dispatch-dominated means the
row is under 20 us so 4T/8T pay thread-region start-up). Per-start ratios and every
chronological sample are in the run directory named at the top of this page (`run*.csv`).
These describe the recorded revisions; they are not a regression claim.

## tcbench, f64, 1T (CPU 4)

| case | plan (ms) | packed (ms) | ttgt (ms) | tblis (ms) | vs `packed` | vs `ttgt` | vs `tblis` | notes |
|---|---|---|---|---|---|---|---|---|
| `abc-bk-akc/n1/b1` | 1.02267 ± 0.00227593 (W 0.00145558) | 1.02285 ± 0.00211491 (W 0.000421436) | 1.97885 ± 0.0138692 (W 0.00155175) | 1.52113 ± 0.0032369 (W 0.00296101) | · | 🔵 fork 1.93× faster than `ttgt` | 🔵 fork 1.49× faster than `tblis` |  |
| `abcijk-eiab-jkec/n1/b1` | 4.52362 ± 0.0292154 (W 0.00395662) | 4.52132 ± 0.0306666 (W 0.00776439) | 8.89139 ± 0.0611419 (W 0.023431) | 5.45227 ± 0.153352 (W 0.0511482) | · | 🔵 fork 1.97× faster than `ttgt` | 🔵 fork 1.21× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-eiac-jkeb/n1/b1` | 4.30435 ± 0.0118022 (W 0.002104) | 4.31717 ± 0.019513 (W 0.0109343) | 10.0171 ± 0.0286154 (W 0.0146109) | 6.62014 ± 0.290114 (W 0.00874903) | · | 🔵 fork 2.33× faster than `ttgt` | 🔵 fork 1.54× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-eibc-jkea/n1/b1` | 4.58357 ± 0.0601709 (W 0.00245826) | 4.57627 ± 0.0598058 (W 0.00293273) | 11.858 ± 0.152758 (W 0.0394244) | 5.44148 ± 0.0351763 (W 0.0119229) | · | 🔵 fork 2.59× faster than `ttgt` | 🔵 fork 1.19× faster than `tblis` |  |
| `abcijk-ejab-ikec/n1/b1` | 4.45562 ± 0.00961082 (W 0.00682888) | 4.45658 ± 0.00874797 (W 0.00557518) | 8.86466 ± 0.0437056 (W 0.0240791) | 5.4761 ± 0.131386 (W 0.032028) | · | 🔵 fork 1.99× faster than `ttgt` | 🔵 fork 1.23× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ejac-ikeb/n1/b1` | 4.33231 ± 0.00626216 (W 0.00385373) | 4.32894 ± 0.021123 (W 0.00722274) | 10.1199 ± 0.0757057 (W 0.043958) | 5.6445 ± 0.127664 (W 0.00872782) | · | 🔵 fork 2.34× faster than `ttgt` | 🔵 fork 1.30× faster than `tblis` |  |
| `abcijk-ejbc-ikea/n1/b1` | 4.61905 ± 0.0839595 (W 0.0138851) | 4.62398 ± 0.0847908 (W 0.0182776) | 11.8871 ± 0.110504 (W 0.0452439) | 5.69039 ± 0.0950991 (W 0.0266512) | · | 🔵 fork 2.57× faster than `ttgt` | 🔵 fork 1.23× faster than `tblis` |  |
| `abcijk-ekab-ijec/n1/b1` | 4.44771 ± 0.0217442 (W 0.0103185) | 4.43918 ± 0.00913578 (W 0.00749887) | 9.2076 ± 0.0495898 (W 0.0276991) | 5.33263 ± 0.166304 (W 0.00926663) | · | 🔵 fork 2.07× faster than `ttgt` | 🔵 fork 1.20× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ekac-ijeb/n1/b1` | 4.33267 ± 0.0124572 (W 0.00868822) | 4.33934 ± 0.0406233 (W 0.0102757) | 10.9785 ± 0.209617 (W 0.0322119) | 5.86858 ± 0.173516 (W 0.0191842) | · | 🔵 fork 2.53× faster than `ttgt` | 🔵 fork 1.35× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ekbc-ijea/n1/b1` | 4.62329 ± 0.0714902 (W 0.00705551) | 4.58906 ± 0.0747209 (W 0.00505157) | 12.4397 ± 0.258111 (W 0.11054) | 5.75107 ± 0.0658589 (W 0.0128223) | · | 🔵 fork 2.69× faster than `ttgt` | 🔵 fork 1.24× faster than `tblis` |  |
| `abcijk-ijma-mkbc/n1/b1` | 4.60356 ± 0.0795811 (W 0.00688934) | 4.59714 ± 0.0863688 (W 0.00289702) | 38.7019 ± 0.265233 (W 0.0646083) | 5.62783 ± 0.110198 (W 0.0275153) | · | 🔵 fork 8.41× faster than `ttgt` | 🔵 fork 1.22× faster than `tblis` |  |
| `abcijk-ijmb-mkac/n1/b1` | 4.33441 ± 0.0165396 (W 0.00453043) | 4.32696 ± 0.0187568 (W 0.00636538) | 36.5262 ± 0.301672 (W 0.139159) | 5.87432 ± 0.166441 (W 0.0229743) | · | 🔵 fork 8.43× faster than `ttgt` | 🔵 fork 1.36× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ijmc-mkab/n1/b1` | 4.45675 ± 0.0195257 (W 0.00919557) | 4.45104 ± 0.0121377 (W 0.00511486) | 37.1679 ± 0.100838 (W 0.0362714) | 5.30334 ± 0.150343 (W 0.00744513) | · | 🔵 fork 8.34× faster than `ttgt` | 🔵 fork 1.19× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ikma-mjbc/n1/b1` | 4.62374 ± 0.0701516 (W 0.00553983) | 4.63007 ± 0.0861765 (W 0.00908208) | 43.7957 ± 0.434364 (W 0.0735172) | 5.76374 ± 0.0717669 (W 0.0129118) | · | 🔵 fork 9.47× faster than `ttgt` | 🔵 fork 1.25× faster than `tblis` |  |
| `abcijk-ikmb-mjac/n1/b1` | 4.31922 ± 0.0224104 (W 0.00233451) | 4.31521 ± 0.0151843 (W 0.00384666) | 39.5156 ± 0.301235 (W 0.0551193) | 5.66588 ± 0.117503 (W 0.0160315) | · | 🔵 fork 9.15× faster than `ttgt` | 🔵 fork 1.31× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 4.45598 ± 0.024066 (W 0.0106791) | 4.44783 ± 0.0201682 (W 0.0066415) | 40.1674 ± 0.270231 (W 0.112792) | 5.48309 ± 0.0998304 (W 0.0187447) | · | 🔵 fork 9.01× faster than `ttgt` | 🔵 fork 1.23× faster than `tblis` |  |
| `abcijk-jkma-mibc/n1/b1` | 4.59038 ± 0.0596357 (W 0.00731042) | 4.57587 ± 0.0508064 (W 0.00854008) | 127.749 ± 1.52861 (W 0.0989744) | 5.42687 ± 0.0652302 (W 0.014204) | · | 🔵 fork 27.83× faster than `ttgt` | 🔵 fork 1.18× faster than `tblis` |  |
| `abcijk-jkmb-miac/n1/b1` | 4.3202 ± 0.0395096 (W 0.00207925) | 4.31641 ± 0.0235119 (W 0.00940417) | 101.338 ± 0.171585 (W 0.0409224) | 6.58853 ± 0.202636 (W 0.0242707) | · | 🔵 fork 23.46× faster than `ttgt` | 🔵 fork 1.53× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-jkmc-miab/n1/b1` | 4.51675 ± 0.0258758 (W 0.013878) | 4.53244 ± 0.0272793 (W 0.00382863) | 103.617 ± 0.759217 (W 0.348085) | 5.47071 ± 0.0264496 (W 0.00488151) | · | 🔵 fork 22.94× faster than `ttgt` | 🔵 fork 1.21× faster than `tblis` |  |
| `abcs-rc-abrs/n1/b1` | 0.486093 ± 0.00289051 (W 0.00217471) | 0.487027 ± 0.00246309 (W 0.00251129) | 1.14518 ± 0.0104399 (W 0.0063477) | 1.15718 ± 0.0103976 (W 0.00548326) | · | 🔵 fork 2.36× faster than `ttgt` | 🔵 fork 2.38× faster than `tblis` |  |
| `abj-bka-kj/n1/b1` | 2.48382 ± 0.0731216 (W 0.00902127) | 2.48173 ± 0.074342 (W 0.00542598) | 2.64855 ± 0.0276905 (W 0.00525981) | 2.55265 ± 0.0389103 (W 0.00330785) | · | 🔵 fork 1.07× faster than `ttgt` | · | `!` between-start range over 5% |
| `abjc-cbka-kj/n1/b1` | 1.54703 ± 0.0141192 (W 0.00520749) | 1.55035 ± 0.0109206 (W 0.00793763) | 1.20001 ± 0.00717693 (W 0.0105062) | 1.39907 ± 0.00990899 (W 0.0103291) | · | 🔴 fork 1.29× slower than `ttgt` | 🔴 fork 1.11× slower than `tblis` |  |
| `abjc-kbac-jk/n1/b1` | 0.542275 ± 0.00165349 (W 0.00296843) | 0.54208 ± 0.00203408 (W 0.00287616) | 1.23299 ± 0.0267758 (W 0.00444912) | 1.16268 ± 0.0291847 (W 0.00718703) | · | 🔵 fork 2.27× faster than `ttgt` | 🔵 fork 2.14× faster than `tblis` | `!` between-start range over 5% |
| `abjcd-dkbac-jk/n1/b1` | 4.29222 ± 0.042605 (W 0.0159534) | 4.3102 ± 0.0401378 (W 0.0234275) | 18.0487 ± 0.478007 (W 0.122115) | 8.17458 ± 0.0401218 (W 0.0266045) | · | 🔵 fork 4.20× faster than `ttgt` | 🔵 fork 1.90× faster than `tblis` | `!` between-start range over 5% |
| `abrs-qb-aqrs/n1/b1` | 0.478882 ± 0.00131791 (W 0.00235855) | 0.478378 ± 0.00452695 (W 0.00298965) | 1.0943 ± 0.0212716 (W 0.00273438) | 1.15058 ± 0.00701649 (W 0.0024579) | · | 🔵 fork 2.29× faster than `ttgt` | 🔵 fork 2.40× faster than `tblis` |  |
| `adbjc-cbdka-kj/n1/b1` | 11.3621 ± 0.393267 (W 0.055732) | 11.3746 ± 0.381742 (W 0.0652744) | 12.0182 ± 0.137262 (W 0.0231694) | 10.3843 ± 0.715851 (W 0.0793151) | · | 🔵 fork 1.06× faster than `ttgt` | 🔴 fork 1.09× slower than `tblis` | `!` between-start range over 5% |
| `ajb-kba-jk/n1/b1` | 1.44474 ± 0.00548241 (W 0.00212203) | 1.44436 ± 0.00596809 (W 0.0014379) | 2.38497 ± 0.0129062 (W 0.00539134) | 2.10132 ± 0.0290512 (W 0.00577317) | · | 🔵 fork 1.65× faster than `ttgt` | 🔵 fork 1.45× faster than `tblis` |  |
| `ajbc-ckba-jk/n1/b1` | 0.737343 ± 0.0273591 (W 0.00416521) | 0.740344 ± 0.0248657 (W 0.00483873) | 3.58266 ± 0.0571624 (W 0.0373589) | 1.22724 ± 0.0105776 (W 0.00371231) | · | 🔵 fork 4.86× faster than `ttgt` | 🔵 fork 1.66× faster than `tblis` | `!` between-start range over 5% |
| `ajbdc-ckbad-jk/n1/b1` | 4.20695 ± 0.0464543 (W 0.0105914) | 4.22029 ± 0.0339407 (W 0.0139668) | 24.0298 ± 0.374969 (W 0.0297756) | 7.80158 ± 0.0309204 (W 0.0217983) | · | 🔵 fork 5.71× faster than `ttgt` | 🔵 fork 1.85× faster than `tblis` |  |
| `aqrs-pa-pqrs/n1/b1` | 0.317534 ± 0.00645151 (W 0.00266332) | 0.472924 ± 0.00200078 (W 0.00253215) | 1.01887 ± 0.00669907 (W 0.00125335) | 1.08401 ± 0.0152121 (W 0.00511097) | 🔵 fork 1.49× faster than `packed` | 🔵 fork 3.21× faster than `ttgt` | 🔵 fork 3.41× faster than `tblis` |  |
| `ij-ik-kj/n1/b1` | 3.42904 ± 0.00771731 (W 0.00109849) | 3.66797 ± 0.0121275 (W 0.00254947) | 4.63592 ± 0.0179106 (W 0.00476449) | 4.29506 ± 0.021352 (W 0.00340401) | 🔵 fork 1.07× faster than `packed` | 🔵 fork 1.35× faster than `ttgt` | 🔵 fork 1.25× faster than `tblis` |  |
| `ij-ikl-ljk/n1/b1` | 1.23146 ± 0.00199221 (W 0.0014128) | 1.22809 ± 0.00729293 (W 0.000715239) | 1.84497 ± 0.0435307 (W 0.016995) | 2.1579 ± 0.00779325 (W 0.00421153) | · | 🔵 fork 1.50× faster than `ttgt` | 🔵 fork 1.75× faster than `tblis` | `!` between-start range over 5% |
| `ij-kil-lkj/n1/b1` | 1.81634 ± 0.0222583 (W 0.00109142) | 1.82229 ± 0.0217231 (W 0.000598566) | 2.85915 ± 0.0299649 (W 0.00635477) | 3.04026 ± 0.00976064 (W 0.0112989) | · | 🔵 fork 1.57× faster than `ttgt` | 🔵 fork 1.67× faster than `tblis` |  |
| `ijk-ikl-lj/n1/b1` | 1.09288 ± 0.00573498 (W 0.00101293) | 1.09187 ± 0.00683511 (W 0.000329158) | 1.63492 ± 0.00817772 (W 0.00128587) | 1.71869 ± 0.00591999 (W 0.00284434) | · | 🔵 fork 1.50× faster than `ttgt` | 🔵 fork 1.57× faster than `tblis` |  |
| `ijk-il-jlk/n1/b1` | 1.06722 ± 0.00424966 (W 0.00110485) | 1.07125 ± 0.00349588 (W 0.000580888) | 1.91149 ± 0.018937 (W 0.00211814) | 1.56917 ± 0.00254659 (W 0.000655134) | · | 🔵 fork 1.79× faster than `ttgt` | 🔵 fork 1.47× faster than `tblis` |  |
| `ijk-ilk-jl/n1/b1` | 1.01969 ± 0.0035528 (W 0.00109425) | 1.02316 ± 0.00214871 (W 0.00120774) | 1.69913 ± 0.00952367 (W 0.0284787) | 1.51269 ± 0.0218268 (W 0.00272378) | · | 🔵 fork 1.67× faster than `ttgt` | 🔵 fork 1.48× faster than `tblis` |  |
| `ijk-ilk-lj/n1/b1` | 1.09436 ± 0.00244029 (W 0.000198343) | 1.09406 ± 0.00613155 (W 0.000981818) | 1.71718 ± 0.0253684 (W 0.0104496) | 1.71868 ± 0.00623519 (W 0.00592237) | · | 🔵 fork 1.57× faster than `ttgt` | 🔵 fork 1.57× faster than `tblis` |  |
| `ijk-ilmk-mjl/n1/b1` | 0.433452 ± 0.00148159 (W 0.00182434) | 0.43474 ± 0.00173135 (W 0.00296101) | 0.683809 ± 0.000808953 (W 0.000470933) | 0.958558 ± 0.00268358 (W 0.000633921) | · | 🔵 fork 1.58× faster than `ttgt` | 🔵 fork 2.21× faster than `tblis` |  |
| `ijkl-imjn-lnkm/n1/b1` | 6.26094 ± 0.0162261 (W 0.000602455) | 6.26138 ± 0.0111733 (W 0.00824239) | 8.04049 ± 0.0199152 (W 0.0216173) | 7.19062 ± 0.0326409 (W 0.00986166) | · | 🔵 fork 1.28× faster than `ttgt` | 🔵 fork 1.15× faster than `tblis` |  |
| `ijkl-imjn-nlmk/n1/b1` | 6.22899 ± 0.234428 (W 0.0123906) | 6.2167 ± 0.00577495 (W 0.00856165) | 8.03375 ± 0.0237754 (W 0.0134598) | 7.32234 ± 0.0451971 (W 0.0165668) | · | 🔵 fork 1.29× faster than `ttgt` | 🔵 fork 1.18× faster than `tblis` | `!` between-start range over 5% |
| `ijkl-imkn-jnlm/n1/b1` | 6.18282 ± 0.0243489 (W 0.00403829) | 6.19076 ± 0.0262114 (W 0.00190565) | 7.99085 ± 0.0478539 (W 0.00808329) | 7.12618 ± 0.051113 (W 0.00577353) | · | 🔵 fork 1.29× faster than `ttgt` | 🔵 fork 1.15× faster than `tblis` |  |
| `ijkl-imkn-njml/n1/b1` | 6.19831 ± 0.018512 (W 0.00253922) | 6.19813 ± 0.0263976 (W 0.00698127) | 8.04707 ± 0.0291746 (W 0.0363492) | 7.2696 ± 0.0744512 (W 0.00874196) | · | 🔵 fork 1.30× faster than `ttgt` | 🔵 fork 1.17× faster than `tblis` |  |
| `ijkl-imln-jnkm/n1/b1` | 6.19523 ± 0.0189442 (W 0.0164533) | 6.18759 ± 0.0129662 (W 0.00438512) | 8.02171 ± 0.0328644 (W 0.0165134) | 7.11989 ± 0.0296032 (W 0.00478535) | · | 🔵 fork 1.29× faster than `ttgt` | 🔵 fork 1.15× faster than `tblis` |  |
| `ijkl-imln-njmk/n1/b1` | 6.19721 ± 0.0218373 (W 0.00564943) | 6.19769 ± 0.0204932 (W 0.00518946) | 8.02057 ± 0.0374127 (W 0.00411607) | 7.25989 ± 0.220904 (W 0.00398879) | · | 🔵 fork 1.29× faster than `ttgt` | 🔵 fork 1.17× faster than `tblis` | `!` between-start range over 5% |
| `ijkl-imnj-nlkm/n1/b1` | 6.19201 ± 0.0156359 (W 0.0111825) | 6.1991 ± 0.00281934 (W 0.00988217) | 7.9586 ± 0.0175693 (W 0.0197757) | 7.27039 ± 0.0576944 (W 0.0115227) | · | 🔵 fork 1.29× faster than `ttgt` | 🔵 fork 1.17× faster than `tblis` |  |
| `ijkl-imnk-njml/n1/b1` | 6.18179 ± 0.0124736 (W 0.0107257) | 6.16754 ± 0.0295656 (W 0.00565332) | 7.98485 ± 0.22631 (W 0.0320666) | 7.25168 ± 0.249487 (W 0.00813314) | · | 🔵 fork 1.29× faster than `ttgt` | 🔵 fork 1.17× faster than `tblis` | `!` between-start range over 5% |
| `ijkl-minj-nlmk/n1/b1` | 7.62003 ± 0.0275989 (W 0.0175515) | 7.61245 ± 0.050987 (W 0.00917719) | 9.61997 ± 0.0329625 (W 0.00952508) | 8.95861 ± 0.144571 (W 0.0282022) | · | 🔵 fork 1.26× faster than `ttgt` | 🔵 fork 1.18× faster than `tblis` |  |
| `ijkl-mink-jnlm/n1/b1` | 7.48465 ± 0.0286778 (W 0.0108424) | 7.49508 ± 0.022584 (W 0.0191308) | 9.58412 ± 0.0500924 (W 0.0180581) | 8.71169 ± 0.123188 (W 0.0404189) | · | 🔵 fork 1.28× faster than `ttgt` | 🔵 fork 1.16× faster than `tblis` |  |
| `ijkl-minl-njmk/n1/b1` | 7.568 ± 0.0399597 (W 0.00492783) | 7.56159 ± 0.0201064 (W 0.0107572) | 9.61425 ± 0.0373714 (W 0.00771489) | 8.79557 ± 0.0816073 (W 0.00721567) | · | 🔵 fork 1.27× faster than `ttgt` | 🔵 fork 1.16× faster than `tblis` |  |

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
