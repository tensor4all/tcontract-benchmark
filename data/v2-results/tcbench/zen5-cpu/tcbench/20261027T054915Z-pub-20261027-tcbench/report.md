# `tcbench` on `zen5-cpu`

- tcontract-rs commit: `71a11a80b454fec3e465c62dd00a6294d3254c1d`
- features: `blas, tblis`
- tprims rows: `tprims` (the provider in the measured revision; see library above); `openblas` (the provider in the measured revision; see library above)
- external providers: `tblis` 2.0 @ `b16a732939d8454021e0a0f0097cf1cc1dd3ab19` tag `v2.0-beta2` sha256 `de00bf1552c15f9c4a5d3157f02c149b81aef0909107c51cbb54ba4b8e9b5827` (TBLIS 2.0, configuration zen3; bundled BLIS 358e689cadd6757f564a2992cf46a2f7d6fa6bb0; built with ./configure --prefix=/home/shinaoka/projects/tensor4all/tcontract-benchmark/target/tblis-v2.0-beta2 --with-blis-config-family=zen3 (cmake, Unix Makefiles, Release); libtblis.so sha256 de00bf1552c15f9c)
- harness commit: `d6e613b60c587e82ed50e37dbc1a2f1d15e7bd82`
- toolkit commit: `467573e6e3e405b8ec30b3b61d096c1d0c9893c3`
- measured binary SHA-256: `0eb4eecc7871df9724e19b91551e5fa2216878fe6462fbcbc3a56ade7089c09c`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-27T06:01:39.250335Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/v2/record_run.py tcbench zen5-cpu tcbench --aa 3 --reps 5 --prime-ms 250 --external-provider-json /tmp/tmp.MUn3muUn4e --label pub-20261027-tcbench`
- raw data: `data/v2-results/tcbench/zen5-cpu/tcbench/20261027T054915Z-pub-20261027-tcbench/`

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
- CPU sets: 1T -> `4`, 4T -> `4-7`

Every timed cell matches a successful verification census, including operation variants.
Each cell is median of process medians ± sample SD of those medians; W is the median
within-process sample SD. All values are milliseconds. These are descriptive spreads,
not confidence intervals. The between-process spread includes the rotating-order schedule.
Each process retains 5 chronological calls; 3 complete process sets are recorded.
Spread guide (computed from this run's own rows): per-engine between-start range median 1.16%, worst 95.40% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 66 of 588 engine cells exceed 5% and carry `!`; median within-process relative SD 0.35%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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

## tcbench, f64, 1T (CPU 4)

| case | plan (ms) | ttgt (ms) | tblis (ms) | vs `ttgt` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `abc-bk-akc/n1/b1` | 1.01794 ± 0.00443117 (W 0.00106079) | 1.96348 ± 0.0768397 (W 0.00876575) | 1.5096 ± 0.0134334 (W 0.00503342) | 🔵 tcontract 1.93× faster than `ttgt` | 🔵 tcontract 1.48× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-eiab-jkec/n1/b1` | 4.5107 ± 0.0204637 (W 0.00938232) | 9.37293 ± 0.364707 (W 0.0221302) | 5.30282 ± 0.200563 (W 0.0214801) | 🔵 tcontract 2.08× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-eiac-jkeb/n1/b1` | 4.31211 ± 0.0131862 (W 0.00584497) | 10.0035 ± 0.0818343 (W 0.0303721) | 6.73243 ± 0.143545 (W 0.0394991) | 🔵 tcontract 2.32× faster than `ttgt` | 🔵 tcontract 1.56× faster than `tblis` |  |
| `abcijk-eibc-jkea/n1/b1` | 4.55798 ± 0.0101551 (W 0.00850704) | 11.7354 ± 0.243486 (W 0.0490686) | 5.38107 ± 0.0425443 (W 0.0207291) | 🔵 tcontract 2.57× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `abcijk-ejab-ikec/n1/b1` | 4.44939 ± 0.0153621 (W 0.00615275) | 8.78668 ± 0.00722955 (W 0.0324166) | 5.40421 ± 0.082064 (W 0.01038) | 🔵 tcontract 1.97× faster than `ttgt` | 🔵 tcontract 1.21× faster than `tblis` |  |
| `abcijk-ejac-ikeb/n1/b1` | 4.30954 ± 0.0129229 (W 0.0167466) | 10.0854 ± 0.086062 (W 0.0349293) | 5.70084 ± 0.0746483 (W 0.0154477) | 🔵 tcontract 2.34× faster than `ttgt` | 🔵 tcontract 1.32× faster than `tblis` |  |
| `abcijk-ejbc-ikea/n1/b1` | 4.58319 ± 0.0162306 (W 0.00613537) | 11.6197 ± 0.302623 (W 0.0254492) | 5.70712 ± 0.0633298 (W 0.0240172) | 🔵 tcontract 2.54× faster than `ttgt` | 🔵 tcontract 1.25× faster than `tblis` |  |
| `abcijk-ekab-ijec/n1/b1` | 4.4383 ± 0.0130606 (W 0.00560663) | 9.24075 ± 0.226553 (W 0.018793) | 5.23814 ± 0.0839772 (W 0.00735467) | 🔵 tcontract 2.08× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `abcijk-ekac-ijeb/n1/b1` | 4.30415 ± 0.0102738 (W 0.00773117) | 11.0761 ± 0.377198 (W 0.0495159) | 5.82742 ± 0.0739508 (W 0.018928) | 🔵 tcontract 2.57× faster than `ttgt` | 🔵 tcontract 1.35× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ekbc-ijea/n1/b1` | 4.56492 ± 0.0163258 (W 0.00472756) | 12.6156 ± 0.557342 (W 0.0924343) | 5.70998 ± 0.0632067 (W 0.0158726) | 🔵 tcontract 2.76× faster than `ttgt` | 🔵 tcontract 1.25× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ijma-mkbc/n1/b1` | 4.55689 ± 0.0129709 (W 0.00705907) | 38.6099 ± 0.65184 (W 0.162898) | 5.67976 ± 0.0871306 (W 0.0169469) | 🔵 tcontract 8.47× faster than `ttgt` | 🔵 tcontract 1.25× faster than `tblis` |  |
| `abcijk-ijmb-mkac/n1/b1` | 4.29898 ± 0.0186098 (W 0.00402693) | 35.0889 ± 0.687213 (W 0.0682277) | 5.86639 ± 0.0343339 (W 0.0263531) | 🔵 tcontract 8.16× faster than `ttgt` | 🔵 tcontract 1.36× faster than `tblis` |  |
| `abcijk-ijmc-mkab/n1/b1` | 4.449 ± 0.00812919 (W 0.00760574) | 36.1483 ± 0.72765 (W 0.168519) | 5.24182 ± 0.0504621 (W 0.00925987) | 🔵 tcontract 8.13× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `abcijk-ikma-mjbc/n1/b1` | 4.56625 ± 0.018705 (W 0.00555592) | 41.75 ± 0.212156 (W 0.0514282) | 5.69499 ± 0.078653 (W 0.0218142) | 🔵 tcontract 9.14× faster than `ttgt` | 🔵 tcontract 1.25× faster than `tblis` |  |
| `abcijk-ikmb-mjac/n1/b1` | 4.31123 ± 0.0167615 (W 0.00963936) | 37.4082 ± 0.278988 (W 0.0716474) | 5.63601 ± 0.0496891 (W 0.015807) | 🔵 tcontract 8.68× faster than `ttgt` | 🔵 tcontract 1.31× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 4.44652 ± 0.00499461 (W 0.0119818) | 39.5465 ± 0.538005 (W 0.0826728) | 5.41871 ± 0.112875 (W 0.00623014) | 🔵 tcontract 8.89× faster than `ttgt` | 🔵 tcontract 1.22× faster than `tblis` |  |
| `abcijk-jkma-mibc/n1/b1` | 4.55744 ± 0.0199309 (W 0.00763737) | 84.3456 ± 27.2449 (W 0.173928) | 5.38147 ± 0.0482819 (W 0.0108298) | 🔵 tcontract 18.51× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmb-miac/n1/b1` | 4.29664 ± 0.0056963 (W 0.00718929) | 84.0916 ± 11.651 (W 0.0979786) | 6.7238 ± 0.140863 (W 0.0429008) | 🔵 tcontract 19.57× faster than `ttgt` | 🔵 tcontract 1.56× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmc-miab/n1/b1` | 4.50348 ± 0.0172012 (W 0.00521833) | 81.78 ± 12.7967 (W 0.157608) | 5.33668 ± 0.193722 (W 0.0426935) | 🔵 tcontract 18.16× faster than `ttgt` | 🔵 tcontract 1.19× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcs-rc-abrs/n1/b1` | 0.480696 ± 0.00301256 (W 0.00207324) | 1.09926 ± 0.0745759 (W 0.00768832) | 1.15604 ± 0.00434004 (W 0.00449575) | 🔵 tcontract 2.29× faster than `ttgt` | 🔵 tcontract 2.40× faster than `tblis` | `!` between-start range over 5% |
| `abj-bka-kj/n1/b1` | 2.45477 ± 0.0183207 (W 0.0121251) | 2.72834 ± 0.0319373 (W 0.00959232) | 2.62835 ± 0.00177459 (W 0.00841868) | 🔵 tcontract 1.11× faster than `ttgt` | 🔵 tcontract 1.07× faster than `tblis` |  |
| `abjc-cbka-kj/n1/b1` | 1.5272 ± 0.0118483 (W 0.00730463) | 1.23236 ± 0.054097 (W 0.0127495) | 1.3989 ± 0.0117976 (W 0.00568466) | 🔴 tcontract 1.24× slower than `ttgt` | 🔴 tcontract 1.09× slower than `tblis` | `!` between-start range over 5% |
| `abjc-kbac-jk/n1/b1` | 0.539724 ± 0.00152419 (W 0.00194021) | 1.25141 ± 0.008264 (W 0.00582612) | 1.14598 ± 0.00563978 (W 0.00634289) | 🔵 tcontract 2.32× faster than `ttgt` | 🔵 tcontract 2.12× faster than `tblis` |  |
| `abjcd-dkbac-jk/n1/b1` | 4.29728 ± 0.0357392 (W 0.0075723) | 17.6258 ± 0.501771 (W 0.0748809) | 8.18292 ± 0.0434941 (W 0.0294133) | 🔵 tcontract 4.10× faster than `ttgt` | 🔵 tcontract 1.90× faster than `tblis` | `!` between-start range over 5% |
| `abrs-qb-aqrs/n1/b1` | 0.477176 ± 0.00187966 (W 0.00211255) | 1.07657 ± 0.0376118 (W 0.00284866) | 1.1493 ± 0.0123571 (W 0.0052384) | 🔵 tcontract 2.26× faster than `ttgt` | 🔵 tcontract 2.41× faster than `tblis` | `!` between-start range over 5% |
| `adbjc-cbdka-kj/n1/b1` | 10.7063 ± 0.160128 (W 0.147868) | 11.478 ± 0.244458 (W 0.0660779) | 9.74673 ± 0.212474 (W 0.033326) | 🔵 tcontract 1.07× faster than `ttgt` | 🔴 tcontract 1.10× slower than `tblis` |  |
| `ajb-kba-jk/n1/b1` | 1.44463 ± 0.013409 (W 0.00372683) | 2.43051 ± 0.0543273 (W 0.00699073) | 2.06448 ± 0.0421401 (W 0.0299503) | 🔵 tcontract 1.68× faster than `ttgt` | 🔵 tcontract 1.43× faster than `tblis` |  |
| `ajbc-ckba-jk/n1/b1` | 0.724354 ± 0.0182537 (W 0.00472036) | 3.66186 ± 0.023749 (W 0.0117635) | 1.20827 ± 0.00293649 (W 0.00591657) | 🔵 tcontract 5.06× faster than `ttgt` | 🔵 tcontract 1.67× faster than `tblis` |  |
| `ajbdc-ckbad-jk/n1/b1` | 4.12715 ± 0.0621401 (W 0.0118069) | 23.6929 ± 0.62058 (W 0.102415) | 7.81034 ± 0.0304677 (W 0.0295495) | 🔵 tcontract 5.74× faster than `ttgt` | 🔵 tcontract 1.89× faster than `tblis` |  |
| `aqrs-pa-pqrs/n1/b1` | 0.506091 ± 0.00240774 (W 0.00246958) | 0.980852 ± 0.0302513 (W 0.0120185) | 1.09738 ± 0.0027321 (W 0.00472465) | 🔵 tcontract 1.94× faster than `ttgt` | 🔵 tcontract 2.17× faster than `tblis` | `!` between-start range over 5% |
| `ij-ik-kj/n1/b1` | 3.57068 ± 0.00252772 (W 0.00443922) | 4.55314 ± 0.0608993 (W 0.0057872) | 4.28752 ± 0.0093628 (W 0.00454121) | 🔵 tcontract 1.28× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `ij-ikl-ljk/n1/b1` | 1.23721 ± 0.0060712 (W 0.00590671) | 1.72548 ± 0.00627045 (W 0.00707952) | 2.14879 ± 0.0131274 (W 0.00594097) | 🔵 tcontract 1.39× faster than `ttgt` | 🔵 tcontract 1.74× faster than `tblis` |  |
| `ij-kil-lkj/n1/b1` | 1.82832 ± 0.0437637 (W 0.0140145) | 2.71665 ± 0.0142098 (W 0.0271871) | 3.05006 ± 0.00940226 (W 0.00689682) | 🔵 tcontract 1.49× faster than `ttgt` | 🔵 tcontract 1.67× faster than `tblis` |  |
| `ijk-ikl-lj/n1/b1` | 1.09675 ± 0.00141816 (W 0.000830881) | 1.5768 ± 0.00433242 (W 0.00380264) | 1.71917 ± 0.00671645 (W 0.00218591) | 🔵 tcontract 1.44× faster than `ttgt` | 🔵 tcontract 1.57× faster than `tblis` |  |
| `ijk-il-jlk/n1/b1` | 1.06629 ± 0.00207417 (W 0.00159894) | 1.94629 ± 0.0861682 (W 0.00902214) | 1.58709 ± 0.00656784 (W 0.00521113) | 🔵 tcontract 1.83× faster than `ttgt` | 🔵 tcontract 1.49× faster than `tblis` | `!` between-start range over 5% |
| `ijk-ilk-jl/n1/b1` | 1.01808 ± 0.00305596 (W 0.00165975) | 1.81331 ± 0.545301 (W 0.038794) | 1.52224 ± 0.00992517 (W 0.00357588) | 🔵 tcontract 1.78× faster than `ttgt` | 🔵 tcontract 1.50× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `ijk-ilk-lj/n1/b1` | 1.08868 ± 0.00125941 (W 0.00240489) | 1.69835 ± 0.0298275 (W 0.0123299) | 1.71055 ± 0.010356 (W 0.00547082) | 🔵 tcontract 1.56× faster than `ttgt` | 🔵 tcontract 1.57× faster than `tblis` |  |
| `ijk-ilmk-mjl/n1/b1` | 0.433514 ± 0.000816782 (W 0.00238802) | 0.644942 ± 0.0148714 (W 0.00206663) | 0.962083 ± 0.0013488 (W 0.00286909) | 🔵 tcontract 1.49× faster than `ttgt` | 🔵 tcontract 2.22× faster than `tblis` |  |
| `ijkl-imjn-lnkm/n1/b1` | 6.27011 ± 0.0116486 (W 0.00847997) | 8.01804 ± 0.10854 (W 0.017765) | 7.65799 ± 0.0525117 (W 0.0604205) | 🔵 tcontract 1.28× faster than `ttgt` | 🔵 tcontract 1.22× faster than `tblis` |  |
| `ijkl-imjn-nlmk/n1/b1` | 6.20198 ± 0.0172539 (W 0.00703549) | 7.98362 ± 0.0649605 (W 0.00740525) | 7.55224 ± 0.0830525 (W 0.014926) | 🔵 tcontract 1.29× faster than `ttgt` | 🔵 tcontract 1.22× faster than `tblis` |  |
| `ijkl-imkn-jnlm/n1/b1` | 6.18671 ± 0.00466707 (W 0.00519656) | 7.97689 ± 0.0177693 (W 0.00564636) | 7.31372 ± 0.0426548 (W 0.0102403) | 🔵 tcontract 1.29× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `ijkl-imkn-njml/n1/b1` | 6.20436 ± 0.0102202 (W 0.00494466) | 7.9566 ± 0.00802149 (W 0.0200862) | 7.45007 ± 0.112706 (W 0.00730823) | 🔵 tcontract 1.28× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `ijkl-imln-jnkm/n1/b1` | 6.19274 ± 0.0101788 (W 0.0111736) | 7.9371 ± 0.10077 (W 0.0116268) | 7.31114 ± 0.106825 (W 0.0349743) | 🔵 tcontract 1.28× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `ijkl-imln-njmk/n1/b1` | 6.18329 ± 0.0131221 (W 0.0134449) | 7.97457 ± 0.103952 (W 0.0116555) | 7.35304 ± 0.0910208 (W 0.00999813) | 🔵 tcontract 1.29× faster than `ttgt` | 🔵 tcontract 1.19× faster than `tblis` |  |
| `ijkl-imnj-nlkm/n1/b1` | 6.20357 ± 0.00495663 (W 0.00507568) | 7.91097 ± 0.0713258 (W 0.0106646) | 7.31998 ± 0.0360932 (W 0.020427) | 🔵 tcontract 1.28× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `ijkl-imnk-njml/n1/b1` | 6.1833 ± 0.00718526 (W 0.00364129) | 7.88007 ± 0.0924206 (W 0.0132221) | 7.33097 ± 0.0416461 (W 0.00321479) | 🔵 tcontract 1.27× faster than `ttgt` | 🔵 tcontract 1.19× faster than `tblis` |  |
| `ijkl-minj-nlmk/n1/b1` | 7.63532 ± 0.0256086 (W 0.00640885) | 9.57544 ± 0.0189022 (W 0.00916706) | 9.10466 ± 0.013075 (W 0.014224) | 🔵 tcontract 1.25× faster than `ttgt` | 🔵 tcontract 1.19× faster than `tblis` |  |
| `ijkl-mink-jnlm/n1/b1` | 7.47918 ± 0.00580508 (W 0.00862451) | 9.5273 ± 0.00186107 (W 0.00914746) | 8.68953 ± 0.0785146 (W 0.0243706) | 🔵 tcontract 1.27× faster than `ttgt` | 🔵 tcontract 1.16× faster than `tblis` |  |
| `ijkl-minl-njmk/n1/b1` | 7.61562 ± 0.0355827 (W 0.00646152) | 9.61971 ± 0.0517648 (W 0.0132023) | 8.76061 ± 0.0446705 (W 0.0154441) | 🔵 tcontract 1.26× faster than `ttgt` | 🔵 tcontract 1.15× faster than `tblis` |  |

## tcbench, f64, 4T (CPU 4-7)

| case | plan (ms) | ttgt (ms) | tblis (ms) | vs `ttgt` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `abc-bk-akc/n1/b1` | 0.278031 ± 0.00244453 (W 0.00491642) | 1.23121 ± 0.0260197 (W 0.0322219) | 0.425449 ± 0.00371403 (W 0.00454057) | 🔵 tcontract 4.43× faster than `ttgt` | 🔵 tcontract 1.53× faster than `tblis` |  |
| `abcijk-eiab-jkec/n1/b1` | 1.19796 ± 0.0068374 (W 0.00458627) | 5.67009 ± 0.0304039 (W 0.0888064) | 1.67365 ± 0.0847698 (W 0.0616506) | 🔵 tcontract 4.73× faster than `ttgt` | 🔵 tcontract 1.40× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-eiac-jkeb/n1/b1` | 1.11443 ± 0.0112396 (W 0.0127194) | 6.80757 ± 0.0323226 (W 0.0517361) | 2.21848 ± 0.0921559 (W 0.0404482) | 🔵 tcontract 6.11× faster than `ttgt` | 🔵 tcontract 1.99× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-eibc-jkea/n1/b1` | 1.19851 ± 0.00491206 (W 0.00555565) | 8.31218 ± 0.151326 (W 0.0319864) | 1.45547 ± 0.00704989 (W 0.00773694) | 🔵 tcontract 6.94× faster than `ttgt` | 🔵 tcontract 1.21× faster than `tblis` |  |
| `abcijk-ejab-ikec/n1/b1` | 1.16505 ± 0.00309065 (W 0.00229164) | 5.67277 ± 0.0455703 (W 0.0242856) | 1.67517 ± 0.0647126 (W 0.0275058) | 🔵 tcontract 4.87× faster than `ttgt` | 🔵 tcontract 1.44× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ejac-ikeb/n1/b1` | 1.11488 ± 0.00539742 (W 0.00293344) | 6.99565 ± 0.0414563 (W 0.0547962) | 1.53964 ± 0.0107117 (W 0.00717894) | 🔵 tcontract 6.27× faster than `ttgt` | 🔵 tcontract 1.38× faster than `tblis` |  |
| `abcijk-ejbc-ikea/n1/b1` | 1.20236 ± 0.175059 (W 0.0034564) | 8.68473 ± 0.172985 (W 0.0485184) | 1.54137 ± 0.0116979 (W 0.0108418) | 🔵 tcontract 7.22× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-ekab-ijec/n1/b1` | 1.16149 ± 0.00429192 (W 0.00800659) | 6.09584 ± 0.207895 (W 0.0475713) | 1.43715 ± 0.0489371 (W 0.0397071) | 🔵 tcontract 5.25× faster than `ttgt` | 🔵 tcontract 1.24× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ekac-ijeb/n1/b1` | 1.11469 ± 0.00331288 (W 0.00455987) | 7.82131 ± 0.20999 (W 0.0643392) | 2.0498 ± 0.0146353 (W 0.0249502) | 🔵 tcontract 7.02× faster than `ttgt` | 🔵 tcontract 1.84× faster than `tblis` |  |
| `abcijk-ekbc-ijea/n1/b1` | 1.20463 ± 0.00620357 (W 0.00557435) | 9.20057 ± 0.302397 (W 0.142877) | 1.53755 ± 0.0057412 (W 0.0110405) | 🔵 tcontract 7.64× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ijma-mkbc/n1/b1` | 1.20549 ± 0.00606258 (W 0.00408775) | 34.5289 ± 0.467753 (W 0.0315554) | 1.53356 ± 0.00250652 (W 0.0101907) | 🔵 tcontract 28.64× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `abcijk-ijmb-mkac/n1/b1` | 1.11386 ± 0.00247754 (W 0.00605462) | 32.816 ± 0.62183 (W 0.0314206) | 2.05138 ± 0.0383382 (W 0.0489677) | 🔵 tcontract 29.46× faster than `ttgt` | 🔵 tcontract 1.84× faster than `tblis` |  |
| `abcijk-ijmc-mkab/n1/b1` | 1.17069 ± 0.640989 (W 0.00875471) | 33.6214 ± 0.467276 (W 0.445361) | 1.49967 ± 0.0225723 (W 0.0365864) | 🔵 tcontract 28.72× faster than `ttgt` | · | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-ikma-mjbc/n1/b1` | 1.21616 ± 0.0172949 (W 0.516541) | 38.2395 ± 1.40671 (W 0.0632203) | 1.53711 ± 0.0123044 (W 0.00987278) | 🔵 tcontract 31.44× faster than `ttgt` | 🔵 tcontract 1.26× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ikmb-mjac/n1/b1` | 1.10707 ± 0.00170669 (W 0.00256586) | 34.2863 ± 0.102297 (W 0.0529741) | 1.53727 ± 0.0214406 (W 0.0108482) | 🔵 tcontract 30.97× faster than `ttgt` | 🔵 tcontract 1.39× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 1.1607 ± 0.00251774 (W 0.00509245) | 36.69 ± 0.235101 (W 0.135731) | 1.65556 ± 0.0487684 (W 0.0339729) | 🔵 tcontract 31.61× faster than `ttgt` | 🔵 tcontract 1.43× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-jkma-mibc/n1/b1` | 1.20242 ± 0.0138011 (W 0.00441522) | 124.448 ± 22.0495 (W 0.138189) | 1.45163 ± 0.00777626 (W 0.0095395) | 🔵 tcontract 103.50× faster than `ttgt` | 🔵 tcontract 1.21× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmb-miac/n1/b1` | 1.11737 ± 0.00643945 (W 0.00171068) | 97.1673 ± 6.96074 (W 0.13272) | 2.24176 ± 0.117143 (W 0.0399023) | 🔵 tcontract 86.96× faster than `ttgt` | 🔵 tcontract 2.01× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmc-miab/n1/b1` | 1.19456 ± 0.00782465 (W 0.00587972) | 98.7175 ± 11.3992 (W 0.162502) | 1.67653 ± 0.0832679 (W 0.0379387) | 🔵 tcontract 82.64× faster than `ttgt` | 🔵 tcontract 1.40× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcs-rc-abrs/n1/b1` | 0.145994 ± 0.000699007 (W 0.00100688) | 0.686405 ± 0.0515144 (W 0.031822) | 0.376127 ± 0.00284275 (W 0.00658481) | 🔵 tcontract 4.70× faster than `ttgt` | 🔵 tcontract 2.58× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abj-bka-kj/n1/b1` | 0.498073 ± 0.0021546 (W 0.00269001) | 1.36442 ± 0.0269081 (W 0.0111061) | 0.722663 ± 0.00340434 (W 0.00867225) | 🔵 tcontract 2.74× faster than `ttgt` | 🔵 tcontract 1.45× faster than `tblis` |  |
| `abjc-cbka-kj/n1/b1` | 0.294842 ± 0.01166 (W 0.00317719) | 0.753653 ± 0.0236413 (W 0.00806012) | 0.458275 ± 0.00565077 (W 0.00853079) | 🔵 tcontract 2.56× faster than `ttgt` | 🔵 tcontract 1.55× faster than `tblis` | `!` between-start range over 5% |
| `abjc-kbac-jk/n1/b1` | 0.162935 ± 0.00253795 (W 0.00173633) | 0.8777 ± 0.0173187 (W 0.00287418) | 0.376971 ± 0.000687125 (W 0.00415001) | 🔵 tcontract 5.39× faster than `ttgt` | 🔵 tcontract 2.31× faster than `tblis` |  |
| `abjcd-dkbac-jk/n1/b1` | 1.43643 ± 0.00289495 (W 0.0139105) | 16.2963 ± 0.0604311 (W 0.0489072) | 2.74073 ± 0.0329156 (W 0.051396) | 🔵 tcontract 11.35× faster than `ttgt` | 🔵 tcontract 1.91× faster than `tblis` |  |
| `abrs-qb-aqrs/n1/b1` | 0.142337 ± 0.00158951 (W 0.0017169) | 0.727794 ± 0.0364025 (W 0.0198386) | 0.377512 ± 0.00228083 (W 0.00518665) | 🔵 tcontract 5.11× faster than `ttgt` | 🔵 tcontract 2.65× faster than `tblis` | `!` between-start range over 5% |
| `adbjc-cbdka-kj/n1/b1` | 6.15592 ± 0.0313706 (W 0.166885) | 9.78036 ± 0.0821376 (W 0.0318448) | 3.522 ± 0.132238 (W 0.0662732) | 🔵 tcontract 1.59× faster than `ttgt` | 🔴 tcontract 1.75× slower than `tblis` | `!` between-start range over 5% |
| `ajb-kba-jk/n1/b1` | 0.387997 ± 0.00109502 (W 0.00167833) | 1.24281 ± 0.0570388 (W 0.00458635) | 0.563062 ± 0.00513206 (W 0.00337664) | 🔵 tcontract 3.20× faster than `ttgt` | 🔵 tcontract 1.45× faster than `tblis` | `!` between-start range over 5% |
| `ajbc-ckba-jk/n1/b1` | 0.233267 ± 0.0107036 (W 0.008006) | 3.23352 ± 0.0273285 (W 0.0143849) | 0.406848 ± 0.00455726 (W 0.00763436) | 🔵 tcontract 13.86× faster than `ttgt` | 🔵 tcontract 1.74× faster than `tblis` | `!` between-start range over 5% |
| `ajbdc-ckbad-jk/n1/b1` | 1.40926 ± 0.0284514 (W 0.0110411) | 23.0185 ± 0.378806 (W 0.0898153) | 2.67279 ± 0.00869768 (W 0.0138177) | 🔵 tcontract 16.33× faster than `ttgt` | 🔵 tcontract 1.90× faster than `tblis` |  |
| `aqrs-pa-pqrs/n1/b1` | 0.188566 ± 0.00764714 (W 0.00384353) | 0.654721 ± 0.0411177 (W 0.00225377) | 0.350431 ± 0.000217003 (W 0.00495216) | 🔵 tcontract 3.47× faster than `ttgt` | 🔵 tcontract 1.86× faster than `tblis` | `!` between-start range over 5% |
| `ij-ik-kj/n1/b1` | 0.945894 ± 0.00345231 (W 0.00368193) | 1.4499 ± 0.00748727 (W 0.00266217) | 1.21333 ± 0.00551072 (W 0.00370373) | 🔵 tcontract 1.53× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` |  |
| `ij-ikl-ljk/n1/b1` | 0.526728 ± 0.00758624 (W 0.0206731) | 0.851727 ± 0.010577 (W 0.00298579) | 0.875734 ± 0.00370248 (W 0.0032496) | 🔵 tcontract 1.62× faster than `ttgt` | 🔵 tcontract 1.66× faster than `tblis` |  |
| `ij-kil-lkj/n1/b1` | 0.767008 ± 0.0171717 (W 0.0084528) | 1.44216 ± 0.00386238 (W 0.00377117) | 1.21476 ± 0.00399509 (W 0.00504501) | 🔵 tcontract 1.88× faster than `ttgt` | 🔵 tcontract 1.58× faster than `tblis` |  |
| `ijk-ikl-lj/n1/b1` | 0.298872 ± 0.00276791 (W 0.00827525) | 0.774392 ± 0.0299467 (W 0.00474863) | 0.477615 ± 0.00252052 (W 0.00411583) | 🔵 tcontract 2.59× faster than `ttgt` | 🔵 tcontract 1.60× faster than `tblis` | `!` between-start range over 5% |
| `ijk-il-jlk/n1/b1` | 0.284106 ± 0.000664961 (W 0.00139717) | 1.10932 ± 0.0195647 (W 0.0159786) | 0.435046 ± 0.00310859 (W 0.00294186) | 🔵 tcontract 3.90× faster than `ttgt` | 🔵 tcontract 1.53× faster than `tblis` |  |
| `ijk-ilk-jl/n1/b1` | 0.275707 ± 0.0140083 (W 0.00796377) | 0.830106 ± 0.0564223 (W 0.0104861) | 0.429946 ± 0.00341659 (W 0.003721) | 🔵 tcontract 3.01× faster than `ttgt` | 🔵 tcontract 1.56× faster than `tblis` | `!` between-start range over 5% |
| `ijk-ilk-lj/n1/b1` | 0.291686 ± 0.00292208 (W 0.00150896) | 0.83495 ± 0.023021 (W 0.0102866) | 0.475959 ± 0.00273797 (W 0.0040929) | 🔵 tcontract 2.86× faster than `ttgt` | 🔵 tcontract 1.63× faster than `tblis` | `!` between-start range over 5% |
| `ijk-ilmk-mjl/n1/b1` | 0.128982 ± 0.00114983 (W 0.00424798) | 0.384844 ± 0.0122382 (W 0.00167645) | 0.286599 ± 0.00277402 (W 0.00342472) | 🔵 tcontract 2.98× faster than `ttgt` | 🔵 tcontract 2.22× faster than `tblis` | `!` between-start range over 5% |
| `ijkl-imjn-lnkm/n1/b1` | 1.61939 ± 0.00768277 (W 0.0132927) | 2.58948 ± 0.0137514 (W 0.00952206) | 1.99016 ± 0.0766164 (W 0.0100781) | 🔵 tcontract 1.60× faster than `ttgt` | 🔵 tcontract 1.23× faster than `tblis` | `!` between-start range over 5% |
| `ijkl-imjn-nlmk/n1/b1` | 1.59322 ± 0.00124309 (W 0.0106872) | 2.60101 ± 0.0181247 (W 0.0114589) | 2.03796 ± 0.0124904 (W 0.00229739) | 🔵 tcontract 1.63× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` |  |
| `ijkl-imkn-jnlm/n1/b1` | 1.58043 ± 0.00263823 (W 0.00179269) | 2.65412 ± 0.0271899 (W 0.0133814) | 1.96449 ± 0.0437546 (W 0.00276315) | 🔵 tcontract 1.68× faster than `ttgt` | 🔵 tcontract 1.24× faster than `tblis` |  |
| `ijkl-imkn-njml/n1/b1` | 1.58406 ± 0.0072963 (W 0.0107636) | 2.63611 ± 0.0361416 (W 0.00938491) | 2.02218 ± 0.01229 (W 0.00436991) | 🔵 tcontract 1.66× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` |  |
| `ijkl-imln-jnkm/n1/b1` | 1.58065 ± 0.00848212 (W 0.00189205) | 2.58974 ± 0.0535406 (W 0.0154567) | 1.9576 ± 0.0332533 (W 0.00447395) | 🔵 tcontract 1.64× faster than `ttgt` | 🔵 tcontract 1.24× faster than `tblis` |  |
| `ijkl-imln-njmk/n1/b1` | 1.58163 ± 0.0124294 (W 0.00320669) | 2.57439 ± 0.0437893 (W 0.00795188) | 1.98043 ± 0.0160392 (W 0.00576759) | 🔵 tcontract 1.63× faster than `ttgt` | 🔵 tcontract 1.25× faster than `tblis` |  |
| `ijkl-imnj-nlkm/n1/b1` | 1.58598 ± 0.00550882 (W 0.00729821) | 2.59808 ± 0.0320853 (W 0.0105836) | 2.02658 ± 0.00669999 (W 0.00393695) | 🔵 tcontract 1.64× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` |  |
| `ijkl-imnk-njml/n1/b1` | 1.57807 ± 0.00241047 (W 0.00362718) | 2.61806 ± 0.00562967 (W 0.00953566) | 1.998 ± 0.00469134 (W 0.00211541) | 🔵 tcontract 1.66× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `ijkl-minj-nlmk/n1/b1` | 1.95163 ± 0.00649485 (W 0.00325496) | 3.18805 ± 0.0246903 (W 0.00596008) | 2.48598 ± 0.0145123 (W 0.00631954) | 🔵 tcontract 1.63× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `ijkl-mink-jnlm/n1/b1` | 1.90298 ± 0.00535364 (W 0.0111765) | 3.18055 ± 0.00982686 (W 0.0139348) | 2.3716 ± 0.0324331 (W 0.00566602) | 🔵 tcontract 1.67× faster than `ttgt` | 🔵 tcontract 1.25× faster than `tblis` |  |
| `ijkl-minl-njmk/n1/b1` | 1.93624 ± 0.00228553 (W 0.0046649) | 3.22624 ± 0.0379491 (W 0.00481399) | 2.41773 ± 0.263575 (W 0.00416579) | 🔵 tcontract 1.67× faster than `ttgt` | 🔵 tcontract 1.25× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |

## tcbench, c64, 1T (CPU 4)

| case | plan (ms) | ttgt (ms) | tblis (ms) | vs `ttgt` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `abc-bk-akc/n1/b1` | 4.07524 ± 0.028528 (W 0.0101234) | 6.17993 ± 0.00962588 (W 0.0134836) | 4.84485 ± 0.0817775 (W 0.0122709) | 🔵 tcontract 1.52× faster than `ttgt` | 🔵 tcontract 1.19× faster than `tblis` |  |
| `abcijk-eiab-jkec/n1/b1` | 17.5874 ± 0.0260374 (W 0.0261971) | 40.3001 ± 0.338014 (W 0.180823) | 19.1211 ± 0.0841938 (W 0.0797727) | 🔵 tcontract 2.29× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `abcijk-eiac-jkeb/n1/b1` | 17.2403 ± 0.0380012 (W 0.0118172) | 40.9855 ± 0.0872324 (W 0.242927) | 20.7685 ± 0.174373 (W 0.10015) | 🔵 tcontract 2.38× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `abcijk-eibc-jkea/n1/b1` | 17.643 ± 0.0274763 (W 0.0163338) | 44.3979 ± 0.386796 (W 0.190487) | 19.1055 ± 0.0271886 (W 0.0241393) | 🔵 tcontract 2.52× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `abcijk-ejab-ikec/n1/b1` | 17.5364 ± 0.0210727 (W 0.015816) | 39.8095 ± 0.34103 (W 0.197836) | 19.2521 ± 0.0943995 (W 0.0640983) | 🔵 tcontract 2.27× faster than `ttgt` | 🔵 tcontract 1.10× faster than `tblis` |  |
| `abcijk-ejac-ikeb/n1/b1` | 17.2643 ± 0.00902661 (W 0.0127813) | 41.4916 ± 0.104581 (W 0.170113) | 19.5236 ± 0.125458 (W 0.0301672) | 🔵 tcontract 2.40× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ejbc-ikea/n1/b1` | 17.7271 ± 0.0753387 (W 0.0126859) | 44.5288 ± 0.324967 (W 0.149531) | 20.0601 ± 0.04606 (W 0.0572643) | 🔵 tcontract 2.51× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ekab-ijec/n1/b1` | 17.5356 ± 0.0161845 (W 0.0178722) | 40.0853 ± 0.246559 (W 0.169161) | 18.9264 ± 0.0398644 (W 0.0510406) | 🔵 tcontract 2.29× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `abcijk-ekac-ijeb/n1/b1` | 17.2654 ± 0.0139595 (W 0.011435) | 42.0671 ± 0.103896 (W 0.2994) | 19.9751 ± 0.0825042 (W 0.0213338) | 🔵 tcontract 2.44× faster than `ttgt` | 🔵 tcontract 1.16× faster than `tblis` |  |
| `abcijk-ekbc-ijea/n1/b1` | 17.7571 ± 0.0467841 (W 0.0268233) | 46.0008 ± 0.158829 (W 0.195788) | 20.0521 ± 0.0553947 (W 0.0309035) | 🔵 tcontract 2.59× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ijma-mkbc/n1/b1` | 17.7407 ± 0.0839223 (W 0.0184146) | 65.3348 ± 0.257419 (W 0.223492) | 20.021 ± 0.087191 (W 0.0403043) | 🔵 tcontract 3.68× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ijmb-mkac/n1/b1` | 17.278 ± 0.0385744 (W 0.0182435) | 66.3901 ± 0.172876 (W 0.203252) | 19.9637 ± 0.0672003 (W 0.409895) | 🔵 tcontract 3.84× faster than `ttgt` | 🔵 tcontract 1.16× faster than `tblis` |  |
| `abcijk-ijmc-mkab/n1/b1` | 17.5035 ± 0.022304 (W 0.0116025) | 78.0934 ± 0.239032 (W 0.328814) | 18.8438 ± 0.0276052 (W 0.0288521) | 🔵 tcontract 4.46× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `abcijk-ikma-mjbc/n1/b1` | 17.7447 ± 0.0771396 (W 0.0290562) | 69.3671 ± 1.26057 (W 0.27605) | 20.0297 ± 0.0561899 (W 0.0487995) | 🔵 tcontract 3.91× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ikmb-mjac/n1/b1` | 17.3047 ± 0.0353422 (W 0.0157871) | 68.8393 ± 0.676454 (W 0.293761) | 19.5402 ± 0.115519 (W 0.0334488) | 🔵 tcontract 3.98× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 17.5217 ± 0.0174882 (W 0.0289365) | 78.7813 ± 0.326993 (W 0.235073) | 19.1302 ± 0.102898 (W 0.0977664) | 🔵 tcontract 4.50× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `abcijk-jkma-mibc/n1/b1` | 17.6242 ± 0.0745309 (W 0.0129547) | 110.233 ± 8.84611 (W 0.481191) | 19.1125 ± 0.0243648 (W 0.0358601) | 🔵 tcontract 6.25× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-jkmb-miac/n1/b1` | 17.232 ± 0.0219867 (W 0.0102746) | 109.856 ± 7.57774 (W 0.250042) | 20.7166 ± 0.164192 (W 0.0851573) | 🔵 tcontract 6.38× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-jkmc-miab/n1/b1` | 17.6043 ± 0.016235 (W 0.0258212) | 114.341 ± 2.45119 (W 0.282031) | 19.0423 ± 0.0851079 (W 0.0530628) | 🔵 tcontract 6.50× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `abcs-rc-abrs/n1/b1` | 1.8539 ± 0.00278768 (W 0.00333837) | 2.84659 ± 0.0327128 (W 0.0119668) | 2.3737 ± 0.0148022 (W 0.00915232) | 🔵 tcontract 1.54× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` |  |
| `abj-bka-kj/n1/b1` | 7.4452 ± 0.024525 (W 0.0371474) | 8.24107 ± 0.0291838 (W 0.0162133) | 8.35931 ± 0.0561397 (W 0.0555794) | 🔵 tcontract 1.11× faster than `ttgt` | 🔵 tcontract 1.12× faster than `tblis` |  |
| `abjc-cbka-kj/n1/b1` | 3.55847 ± 0.0525645 (W 0.00689273) | 3.61915 ± 0.0173875 (W 0.0211368) | 3.10754 ± 0.0950016 (W 0.0509139) | · | 🔴 tcontract 1.15× slower than `tblis` | `!` between-start range over 5% |
| `abjc-kbac-jk/n1/b1` | 1.96955 ± 0.00640047 (W 0.0025827) | 3.59938 ± 0.0248189 (W 0.038824) | 2.62928 ± 0.018054 (W 0.0126749) | 🔵 tcontract 1.83× faster than `ttgt` | 🔵 tcontract 1.33× faster than `tblis` |  |
| `abjcd-dkbac-jk/n1/b1` | 12.8446 ± 0.0681705 (W 0.0874687) | 30.3301 ± 0.996042 (W 0.148382) | 17.5234 ± 0.217906 (W 0.14851) | 🔵 tcontract 2.36× faster than `ttgt` | 🔵 tcontract 1.36× faster than `tblis` | `!` between-start range over 5% |
| `abrs-qb-aqrs/n1/b1` | 1.6081 ± 0.0051462 (W 0.00907187) | 2.8707 ± 0.0362559 (W 0.0276133) | 2.47729 ± 0.0316654 (W 0.0223828) | 🔵 tcontract 1.79× faster than `ttgt` | 🔵 tcontract 1.54× faster than `tblis` |  |
| `adbjc-cbdka-kj/n1/b1` | 20.1182 ± 0.0505831 (W 0.0846701) | 22.8346 ± 0.0408497 (W 0.0299771) | 19.4497 ± 0.247647 (W 0.153965) | 🔵 tcontract 1.14× faster than `ttgt` | · |  |
| `ajb-kba-jk/n1/b1` | 5.67689 ± 0.00789919 (W 0.01002) | 7.96911 ± 0.0108856 (W 0.0103526) | 7.22836 ± 0.0734255 (W 0.075077) | 🔵 tcontract 1.40× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `ajbc-ckba-jk/n1/b1` | 2.28783 ± 0.0318428 (W 0.0128087) | 5.6905 ± 0.0184155 (W 0.00702219) | 3.00463 ± 0.102763 (W 0.0445216) | 🔵 tcontract 2.49× faster than `ttgt` | 🔵 tcontract 1.31× faster than `tblis` | `!` between-start range over 5% |
| `ajbdc-ckbad-jk/n1/b1` | 12.5195 ± 0.0658828 (W 0.0736998) | 34.7452 ± 0.256725 (W 0.124673) | 17.3355 ± 0.049274 (W 0.159353) | 🔵 tcontract 2.78× faster than `ttgt` | 🔵 tcontract 1.38× faster than `tblis` |  |
| `aqrs-pa-pqrs/n1/b1` | 2.05717 ± 0.00220885 (W 0.00385281) | 2.44466 ± 0.0176313 (W 0.00692556) | 2.34189 ± 0.0271759 (W 0.00505283) | 🔵 tcontract 1.19× faster than `ttgt` | 🔵 tcontract 1.14× faster than `tblis` |  |
| `ij-ik-kj/n1/b1` | 14.5317 ± 0.00834563 (W 0.0118251) | 17.6144 ± 0.0197449 (W 0.00634116) | 15.3949 ± 0.0566131 (W 0.0102191) | 🔵 tcontract 1.21× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` |  |
| `ij-ikl-ljk/n1/b1` | 4.87627 ± 0.00643236 (W 0.010403) | 5.77852 ± 0.00547635 (W 0.0293859) | 5.64523 ± 0.015733 (W 0.00643235) | 🔵 tcontract 1.19× faster than `ttgt` | 🔵 tcontract 1.16× faster than `tblis` |  |
| `ij-kil-lkj/n1/b1` | 7.43824 ± 0.0216902 (W 0.0190031) | 8.67644 ± 0.0180508 (W 0.0284493) | 8.25088 ± 0.057335 (W 0.0139764) | 🔵 tcontract 1.17× faster than `ttgt` | 🔵 tcontract 1.11× faster than `tblis` |  |
| `ijk-ikl-lj/n1/b1` | 4.20627 ± 0.00397557 (W 0.00211246) | 5.33937 ± 0.112875 (W 0.00518511) | 5.72275 ± 0.0179797 (W 0.0226469) | 🔵 tcontract 1.27× faster than `ttgt` | 🔵 tcontract 1.36× faster than `tblis` |  |
| `ijk-il-jlk/n1/b1` | 4.53962 ± 0.0229682 (W 0.00375058) | 6.06637 ± 0.00628929 (W 0.013435) | 4.80296 ± 0.0488788 (W 0.00530526) | 🔵 tcontract 1.34× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` |  |
| `ijk-ilk-jl/n1/b1` | 4.09971 ± 0.0225864 (W 0.00304831) | 5.82063 ± 0.00228342 (W 0.00592179) | 5.00104 ± 0.0483782 (W 0.0118268) | 🔵 tcontract 1.42× faster than `ttgt` | 🔵 tcontract 1.22× faster than `tblis` |  |
| `ijk-ilk-lj/n1/b1` | 4.20719 ± 0.0326204 (W 0.00479785) | 5.88059 ± 0.00452148 (W 0.00651454) | 5.52047 ± 0.155178 (W 0.0178337) | 🔵 tcontract 1.40× faster than `ttgt` | 🔵 tcontract 1.31× faster than `tblis` | `!` between-start range over 5% |
| `ijk-ilmk-mjl/n1/b1` | 1.6354 ± 0.00373285 (W 0.00295219) | 2.02404 ± 0.00839436 (W 0.00502612) | 2.11911 ± 0.0137104 (W 0.0103976) | 🔵 tcontract 1.24× faster than `ttgt` | 🔵 tcontract 1.30× faster than `tblis` |  |
| `ijkl-imjn-lnkm/n1/b1` | 25.1185 ± 0.015394 (W 0.0137989) | 30.6312 ± 0.00538074 (W 0.018447) | 26.7872 ± 0.0493845 (W 0.0333144) | 🔵 tcontract 1.22× faster than `ttgt` | 🔵 tcontract 1.07× faster than `tblis` |  |
| `ijkl-imjn-nlmk/n1/b1` | 25.0587 ± 0.0312139 (W 0.0307793) | 30.4901 ± 0.0432862 (W 0.0413531) | 27.5172 ± 0.0148709 (W 0.0321362) | 🔵 tcontract 1.22× faster than `ttgt` | 🔵 tcontract 1.10× faster than `tblis` |  |
| `ijkl-imkn-jnlm/n1/b1` | 24.984 ± 0.0421476 (W 0.0340685) | 30.5768 ± 0.0536513 (W 0.025969) | 26.7277 ± 0.176817 (W 0.039385) | 🔵 tcontract 1.22× faster than `ttgt` | 🔵 tcontract 1.07× faster than `tblis` |  |
| `ijkl-imkn-njml/n1/b1` | 25.0551 ± 0.0139938 (W 0.0294445) | 30.5503 ± 0.0313236 (W 0.0293969) | 27.5202 ± 0.105872 (W 0.0589288) | 🔵 tcontract 1.22× faster than `ttgt` | 🔵 tcontract 1.10× faster than `tblis` |  |
| `ijkl-imln-jnkm/n1/b1` | 24.9389 ± 0.0302637 (W 0.0257774) | 30.6435 ± 0.0464984 (W 0.0281185) | 26.5808 ± 0.313526 (W 0.092484) | 🔵 tcontract 1.23× faster than `ttgt` | 🔵 tcontract 1.07× faster than `tblis` |  |
| `ijkl-imln-njmk/n1/b1` | 25.0093 ± 0.0263867 (W 0.0153965) | 30.5178 ± 0.0284774 (W 0.0328219) | 27.1703 ± 0.111744 (W 0.0422131) | 🔵 tcontract 1.22× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `ijkl-imnj-nlkm/n1/b1` | 25.0027 ± 0.0279384 (W 0.0166715) | 30.2711 ± 0.00561714 (W 0.0259369) | 27.2353 ± 0.333656 (W 0.0375192) | 🔵 tcontract 1.21× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `ijkl-imnk-njml/n1/b1` | 25.0066 ± 0.010452 (W 0.00904395) | 30.3472 ± 0.0175514 (W 0.0725427) | 27.1809 ± 0.169145 (W 0.0402319) | 🔵 tcontract 1.21× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `ijkl-minj-nlmk/n1/b1` | 30.7029 ± 0.035249 (W 0.035655) | 36.5698 ± 0.0248043 (W 0.026413) | 33.462 ± 0.292694 (W 0.065069) | 🔵 tcontract 1.19× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `ijkl-mink-jnlm/n1/b1` | 30.0421 ± 0.0329864 (W 0.0215463) | 36.5047 ± 0.00851953 (W 0.0149423) | 31.9449 ± 0.125825 (W 0.0404596) | 🔵 tcontract 1.22× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` |  |
| `ijkl-minl-njmk/n1/b1` | 30.6282 ± 0.0224492 (W 0.0266936) | 36.5417 ± 0.0474413 (W 0.0454153) | 32.7172 ± 0.0772795 (W 0.0362124) | 🔵 tcontract 1.19× faster than `ttgt` | 🔵 tcontract 1.07× faster than `tblis` |  |

## tcbench, c64, 4T (CPU 4-7)

| case | plan (ms) | ttgt (ms) | tblis (ms) | vs `ttgt` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `abc-bk-akc/n1/b1` | 1.07167 ± 0.00485846 (W 0.439577) | 2.63068 ± 0.0262159 (W 0.0249766) | 1.25431 ± 0.0246157 (W 0.00539655) | 🔵 tcontract 2.45× faster than `ttgt` | 🔵 tcontract 1.17× faster than `tblis` |  |
| `abcijk-eiab-jkec/n1/b1` | 4.57692 ± 0.0297709 (W 1.00203) | 25.6254 ± 0.617499 (W 0.189833) | 5.07813 ± 0.0199943 (W 0.0370521) | 🔵 tcontract 5.60× faster than `ttgt` | 🔵 tcontract 1.11× faster than `tblis` |  |
| `abcijk-eiac-jkeb/n1/b1` | 4.35569 ± 0.0166089 (W 0.0150556) | 26.1588 ± 0.591592 (W 0.26505) | 5.521 ± 0.00734927 (W 0.0293138) | 🔵 tcontract 6.01× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `abcijk-eibc-jkea/n1/b1` | 4.62091 ± 0.0289302 (W 1.50422) | 30.3951 ± 0.225578 (W 0.108468) | 4.96204 ± 0.00647264 (W 0.0191148) | 🔵 tcontract 6.58× faster than `ttgt` | 🔵 tcontract 1.07× faster than `tblis` |  |
| `abcijk-ejab-ikec/n1/b1` | 4.46593 ± 0.00878336 (W 0.0115609) | 26.0865 ± 0.413449 (W 0.0588966) | 5.11644 ± 0.0113118 (W 0.0491031) | 🔵 tcontract 5.84× faster than `ttgt` | 🔵 tcontract 1.15× faster than `tblis` |  |
| `abcijk-ejac-ikeb/n1/b1` | 4.4128 ± 0.0142778 (W 0.927784) | 26.7784 ± 0.433877 (W 0.233829) | 5.14933 ± 0.00906232 (W 0.0160055) | 🔵 tcontract 6.07× faster than `ttgt` | 🔵 tcontract 1.17× faster than `tblis` |  |
| `abcijk-ejbc-ikea/n1/b1` | 4.63173 ± 0.0121387 (W 1.6094) | 30.3097 ± 0.674692 (W 0.194995) | 5.18951 ± 0.0115014 (W 0.0148812) | 🔵 tcontract 6.54× faster than `ttgt` | 🔵 tcontract 1.12× faster than `tblis` |  |
| `abcijk-ekab-ijec/n1/b1` | 4.45837 ± 0.0438201 (W 0.0130904) | 26.2789 ± 0.476534 (W 0.105812) | 4.92595 ± 0.0106022 (W 0.024507) | 🔵 tcontract 5.89× faster than `ttgt` | 🔵 tcontract 1.10× faster than `tblis` |  |
| `abcijk-ekac-ijeb/n1/b1` | 4.34762 ± 0.00515821 (W 0.0102498) | 28.0634 ± 0.413211 (W 0.22356) | 5.24098 ± 0.0163396 (W 0.0132571) | 🔵 tcontract 6.45× faster than `ttgt` | 🔵 tcontract 1.21× faster than `tblis` |  |
| `abcijk-ekbc-ijea/n1/b1` | 4.63729 ± 0.0396337 (W 1.41254) | 31.2071 ± 0.187549 (W 0.217163) | 5.20657 ± 0.00103805 (W 0.0135581) | 🔵 tcontract 6.73× faster than `ttgt` | 🔵 tcontract 1.12× faster than `tblis` |  |
| `abcijk-ijma-mkbc/n1/b1` | 4.62586 ± 0.00220062 (W 1.66882) | 52.023 ± 0.441732 (W 0.236314) | 5.21435 ± 0.00454384 (W 0.0120601) | 🔵 tcontract 11.25× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ijmb-mkac/n1/b1` | 4.36095 ± 0.0132439 (W 0.0110263) | 53.4307 ± 0.687681 (W 0.415198) | 5.25181 ± 0.00457169 (W 0.018957) | 🔵 tcontract 12.25× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `abcijk-ijmc-mkab/n1/b1` | 4.44781 ± 0.0150117 (W 0.0170323) | 63.6682 ± 0.610586 (W 0.124578) | 4.92087 ± 0.0196824 (W 0.0188837) | 🔵 tcontract 14.31× faster than `ttgt` | 🔵 tcontract 1.11× faster than `tblis` |  |
| `abcijk-ikma-mjbc/n1/b1` | 4.64588 ± 0.625523 (W 1.43836) | 55.1385 ± 1.01168 (W 0.254726) | 5.21804 ± 0.00305664 (W 0.0158771) | 🔵 tcontract 11.87× faster than `ttgt` | · | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-ikmb-mjac/n1/b1` | 4.35685 ± 0.0578483 (W 0.0111082) | 55.3099 ± 0.291814 (W 0.238431) | 5.14611 ± 0.011852 (W 0.0152559) | 🔵 tcontract 12.69× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 4.4654 ± 0.994111 (W 0.0204964) | 63.7622 ± 0.468885 (W 0.26273) | 5.10158 ± 0.0174384 (W 0.0273186) | 🔵 tcontract 14.28× faster than `ttgt` | · | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkma-mibc/n1/b1` | 4.60298 ± 1.98945 (W 0.276751) | 94.328 ± 6.52978 (W 0.19555) | 4.97065 ± 0.0135281 (W 0.0113425) | 🔵 tcontract 20.49× faster than `ttgt` | · | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmb-miac/n1/b1` | 4.39967 ± 0.0315913 (W 0.030209) | 91.9519 ± 9.58616 (W 0.17077) | 5.57268 ± 0.0208367 (W 0.0363605) | 🔵 tcontract 20.90× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmc-miab/n1/b1` | 4.51175 ± 0.0199261 (W 0.0317257) | 98.2707 ± 4.29287 (W 0.191822) | 5.07065 ± 0.0165167 (W 0.0256893) | 🔵 tcontract 21.78× faster than `ttgt` | 🔵 tcontract 1.12× faster than `tblis` | `!` between-start range over 5% |
| `abcs-rc-abrs/n1/b1` | 0.484141 ± 0.00488487 (W 0.0023415) | 1.49172 ± 0.0187593 (W 0.00722891) | 0.708652 ± 0.0103298 (W 0.0117719) | 🔵 tcontract 3.08× faster than `ttgt` | 🔵 tcontract 1.46× faster than `tblis` |  |
| `abj-bka-kj/n1/b1` | 1.63083 ± 0.38646 (W 0.0138939) | 3.57172 ± 0.0239909 (W 0.0254066) | 2.27979 ± 0.0126583 (W 0.0151486) | 🔵 tcontract 2.19× faster than `ttgt` | 🔵 tcontract 1.40× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abjc-cbka-kj/n1/b1` | 0.789129 ± 0.0253548 (W 0.005503) | 2.04699 ± 0.00932193 (W 0.00956829) | 0.957364 ± 0.0413132 (W 0.035102) | 🔵 tcontract 2.59× faster than `ttgt` | 🔵 tcontract 1.21× faster than `tblis` | `!` between-start range over 5% |
| `abjc-kbac-jk/n1/b1` | 0.515479 ± 0.00298998 (W 0.0029707) | 2.09652 ± 0.0275454 (W 0.0446882) | 0.782677 ± 0.00040572 (W 0.00969547) | 🔵 tcontract 4.07× faster than `ttgt` | 🔵 tcontract 1.52× faster than `tblis` |  |
| `abjcd-dkbac-jk/n1/b1` | 3.87257 ± 0.0569306 (W 0.0332597) | 22.0051 ± 1.11162 (W 0.0395208) | 5.19876 ± 0.0269801 (W 0.046202) | 🔵 tcontract 5.68× faster than `ttgt` | 🔵 tcontract 1.34× faster than `tblis` | `!` between-start range over 5% |
| `abrs-qb-aqrs/n1/b1` | 0.423787 ± 0.00258426 (W 0.00285129) | 1.50296 ± 0.0180405 (W 0.0331981) | 0.724953 ± 0.0131799 (W 0.00996802) | 🔵 tcontract 3.55× faster than `ttgt` | 🔵 tcontract 1.71× faster than `tblis` |  |
| `adbjc-cbdka-kj/n1/b1` | 8.21159 ± 0.0556363 (W 0.236359) | 15.8739 ± 0.0818873 (W 0.0158339) | 7.39039 ± 0.083955 (W 0.10917) | 🔵 tcontract 1.93× faster than `ttgt` | 🔴 tcontract 1.11× slower than `tblis` |  |
| `ajb-kba-jk/n1/b1` | 1.49312 ± 0.0116648 (W 0.768353) | 3.52354 ± 0.0127916 (W 0.0103513) | 1.83911 ± 0.0436313 (W 0.0119695) | 🔵 tcontract 2.36× faster than `ttgt` | 🔵 tcontract 1.23× faster than `tblis` |  |
| `ajbc-ckba-jk/n1/b1` | 0.613634 ± 0.012863 (W 0.0086585) | 4.20773 ± 0.0288905 (W 0.0204189) | 0.915778 ± 0.0152505 (W 0.0132935) | 🔵 tcontract 6.86× faster than `ttgt` | 🔵 tcontract 1.49× faster than `tblis` |  |
| `ajbdc-ckbad-jk/n1/b1` | 3.69332 ± 0.0219844 (W 0.0248547) | 28.1067 ± 0.334338 (W 0.0662549) | 5.14486 ± 0.0294119 (W 0.0494693) | 🔵 tcontract 7.61× faster than `ttgt` | 🔵 tcontract 1.39× faster than `tblis` |  |
| `aqrs-pa-pqrs/n1/b1` | 0.634868 ± 0.00506661 (W 0.0094274) | 1.07818 ± 0.008405 (W 0.00170529) | 0.660658 ± 0.0024095 (W 0.0028375) | 🔵 tcontract 1.70× faster than `ttgt` | · |  |
| `ij-ik-kj/n1/b1` | 3.72375 ± 0.0141247 (W 0.038885) | 4.89464 ± 0.00620576 (W 0.00417622) | 4.04307 ± 0.0248298 (W 0.0107413) | 🔵 tcontract 1.31× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `ij-ikl-ljk/n1/b1` | 2.11967 ± 0.014378 (W 0.0488647) | 2.18899 ± 0.0273853 (W 0.00787722) | 1.70108 ± 0.0347481 (W 0.00950119) | · | 🔴 tcontract 1.25× slower than `tblis` |  |
| `ij-kil-lkj/n1/b1` | 3.21611 ± 0.052815 (W 0.0576162) | 3.58268 ± 0.0221951 (W 0.0118588) | 2.38759 ± 0.0116866 (W 0.0207998) | 🔵 tcontract 1.11× faster than `ttgt` | 🔴 tcontract 1.35× slower than `tblis` |  |
| `ijk-ikl-lj/n1/b1` | 1.10186 ± 0.016731 (W 0.0138968) | 2.00784 ± 0.0104829 (W 0.00423589) | 1.40335 ± 0.0104258 (W 0.00884938) | 🔵 tcontract 1.82× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `ijk-il-jlk/n1/b1` | 1.94574 ± 0.112389 (W 0.08586) | 2.47645 ± 0.0250915 (W 0.0183171) | 1.22284 ± 0.00862204 (W 0.00302019) | 🔵 tcontract 1.27× faster than `ttgt` | 🔴 tcontract 1.59× slower than `tblis` | `!` between-start range over 5% |
| `ijk-ilk-jl/n1/b1` | 1.06364 ± 0.010148 (W 0.4462) | 2.5127 ± 0.00771942 (W 0.0129898) | 1.26953 ± 0.00993308 (W 0.00757136) | 🔵 tcontract 2.36× faster than `ttgt` | 🔵 tcontract 1.19× faster than `tblis` |  |
| `ijk-ilk-lj/n1/b1` | 1.09973 ± 0.00798093 (W 0.461081) | 2.52218 ± 0.00326447 (W 0.0103534) | 1.41586 ± 0.0320781 (W 0.00816093) | 🔵 tcontract 2.29× faster than `ttgt` | 🔵 tcontract 1.29× faster than `tblis` |  |
| `ijk-ilmk-mjl/n1/b1` | 0.464744 ± 0.0023663 (W 0.00469613) | 0.835056 ± 0.00267904 (W 0.00344821) | 0.546709 ± 0.00632372 (W 0.0017859) | 🔵 tcontract 1.80× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `ijkl-imjn-lnkm/n1/b1` | 6.9252 ± 0.0290241 (W 0.0193714) | 8.776 ± 0.0370798 (W 0.0173418) | 7.04137 ± 0.0660065 (W 0.00903506) | 🔵 tcontract 1.27× faster than `ttgt` | · |  |
| `ijkl-imjn-nlmk/n1/b1` | 6.86739 ± 0.0140666 (W 0.0162181) | 8.75376 ± 0.0204708 (W 0.0228944) | 7.15834 ± 0.0847982 (W 0.0130034) | 🔵 tcontract 1.27× faster than `ttgt` | · |  |
| `ijkl-imkn-jnlm/n1/b1` | 6.82772 ± 0.033694 (W 0.0648559) | 8.78647 ± 0.0371877 (W 0.0144346) | 7.1006 ± 0.0736993 (W 0.015518) | 🔵 tcontract 1.29× faster than `ttgt` | · |  |
| `ijkl-imkn-njml/n1/b1` | 6.86052 ± 0.0579375 (W 1.15798) | 8.73282 ± 0.01252 (W 0.0171734) | 7.13722 ± 0.078167 (W 0.0138662) | 🔵 tcontract 1.27× faster than `ttgt` | · |  |
| `ijkl-imln-jnkm/n1/b1` | 6.8297 ± 0.030574 (W 0.0544104) | 8.74754 ± 0.0103947 (W 0.0182328) | 7.08176 ± 0.0785612 (W 0.00856779) | 🔵 tcontract 1.28× faster than `ttgt` | · |  |
| `ijkl-imln-njmk/n1/b1` | 6.91826 ± 0.0610356 (W 1.49099) | 8.72431 ± 0.0501333 (W 0.029253) | 7.04073 ± 0.0594173 (W 0.0103933) | 🔵 tcontract 1.26× faster than `ttgt` | · |  |
| `ijkl-imnj-nlkm/n1/b1` | 6.98263 ± 1.73347 (W 0.755166) | 8.5079 ± 0.0312475 (W 0.0326962) | 7.06593 ± 0.104843 (W 0.0173645) | · | · | `!` between-start range over 5%; `p` position effect over 5% |
| `ijkl-imnk-njml/n1/b1` | 6.93776 ± 0.0703809 (W 1.28147) | 8.58554 ± 0.0211645 (W 0.0372386) | 7.03061 ± 0.0288578 (W 0.00708192) | 🔵 tcontract 1.24× faster than `ttgt` | · |  |
| `ijkl-minj-nlmk/n1/b1` | 8.45456 ± 1.81239 (W 1.38498) | 10.3705 ± 0.0278069 (W 0.0216016) | 8.72077 ± 0.103623 (W 0.0189452) | · | · | `!` between-start range over 5%; `p` position effect over 5% |
| `ijkl-mink-jnlm/n1/b1` | 8.20052 ± 0.0115013 (W 0.0461732) | 10.4996 ± 0.0133769 (W 0.0260766) | 8.43444 ± 0.0747072 (W 0.0117441) | 🔵 tcontract 1.28× faster than `ttgt` | · |  |
| `ijkl-minl-njmk/n1/b1` | 8.37594 ± 0.0693424 (W 0.0219314) | 10.4627 ± 0.0853463 (W 0.0242086) | 8.49052 ± 0.0523802 (W 0.0152191) | 🔵 tcontract 1.25× faster than `ttgt` | · |  |

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
