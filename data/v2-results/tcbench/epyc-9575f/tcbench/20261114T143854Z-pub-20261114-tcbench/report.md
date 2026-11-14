# `tcbench` on `epyc-9575f`

- tcontract-rs commit: `a045446301442ebb7540c806d9914dccce62357a`
- features: `blas, tblis`
- tprims rows: `tprims` (the provider in the measured revision; see library above); `openblas` (the provider in the measured revision; see library above)
- external providers: `tblis` 2.0 @ `b16a732939d8454021e0a0f0097cf1cc1dd3ab19` tag `v2.0-beta2` sha256 `a6dbff05f181cbd5962d732b3c89c891ed90f449ecda460c973ba921ad03ff23` (TBLIS 2.0, configuration zen3; bundled BLIS 358e689cadd6757f564a2992cf46a2f7d6fa6bb0; built with ./configure --prefix=/home/ningyuan/projects/t4a_bench/workspace/tcontract-benchmark/target/tblis-v2.0-beta2 --with-blis-config-family=zen3 (cmake, Unix Makefiles, Release); libtblis.so sha256 a6dbff05f181cbd5)
- harness commit: `ce36f0bf324b093826c859f2a4d8a83ac309979c`
- toolkit commit: `926334592a5ef615617d169d9e2ab3c6bf7a7bd6`
- measured binary SHA-256: `9c1c668cc5dd7cb88cbbd1759e08d48825981d011a1a69a090f5506ba1cd1743`
- hardware profile: `epyc-9575f`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-11-14T15:25:15.796739Z`
- timing policy: v2, median of 5 reps, priming 1500 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/v2/record_run.py tcbench epyc-9575f tcbench --external-provider-json target/tblis-providers.json --aa 3 --reps 5 --prime-ms 1500 --label pub-20261114-tcbench`
- raw data: `data/v2-results/tcbench/epyc-9575f/tcbench/20261114T143854Z-pub-20261114-tcbench/`

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
    As measured: `tblis` 2.0 @ `b16a732939d8454021e0a0f0097cf1cc1dd3ab19` tag `v2.0-beta2` sha256 `a6dbff05f181cbd5962d732b3c89c891ed90f449ecda460c973ba921ad03ff23` (TBLIS 2.0, configuration zen3; bundled BLIS 358e689cadd6757f564a2992cf46a2f7d6fa6bb0; built with ./configure --prefix=/home/ningyuan/projects/t4a_bench/workspace/tcontract-benchmark/target/tblis-v2.0-beta2 --with-blis-config-family=zen3 (cmake, Unix Makefiles, Release); libtblis.so sha256 a6dbff05f181cbd5)

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
Each process retains 5 chronological calls; 3 complete process sets are recorded.
Spread guide (computed from this run's own rows): per-engine between-start range median 0.89%, worst 39.54% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 30 of 588 engine cells exceed 5% and carry `!`; median within-process relative SD 0.19%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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

## tcbench, f64, 1T (CPU 0)

| case | plan (ms) | ttgt (ms) | tblis (ms) | vs `ttgt` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `abc-bk-akc/n1/b1` | 0.344585 ± 0.00221465 (W 0.000852363) | 0.968559 ± 0.0251816 (W 0.00135503) | 0.897012 ± 0.0059543 (W 0.00199488) | 🔵 tcontract 2.81× faster than `ttgt` | 🔵 tcontract 2.60× faster than `tblis` |  |
| `abcijk-eiab-jkec/n1/b1` | 1.49385 ± 0.0120728 (W 0.00150105) | 5.37893 ± 0.0433519 (W 0.0167534) | 2.98798 ± 0.0411205 (W 0.00248813) | 🔵 tcontract 3.60× faster than `ttgt` | 🔵 tcontract 2.00× faster than `tblis` |  |
| `abcijk-eiac-jkeb/n1/b1` | 1.46073 ± 0.00766414 (W 0.00148417) | 5.78463 ± 0.0333763 (W 0.0150259) | 3.04393 ± 0.00806378 (W 0.00300381) | 🔵 tcontract 3.96× faster than `ttgt` | 🔵 tcontract 2.08× faster than `tblis` |  |
| `abcijk-eibc-jkea/n1/b1` | 1.60517 ± 0.0155266 (W 0.00219663) | 6.00771 ± 0.0392453 (W 0.00976275) | 2.96161 ± 0.0309166 (W 0.00377364) | 🔵 tcontract 3.74× faster than `ttgt` | 🔵 tcontract 1.85× faster than `tblis` |  |
| `abcijk-ejab-ikec/n1/b1` | 1.47011 ± 0.0105019 (W 0.00227081) | 5.27866 ± 0.0111809 (W 0.00884816) | 2.97819 ± 0.047276 (W 0.00177352) | 🔵 tcontract 3.59× faster than `ttgt` | 🔵 tcontract 2.03× faster than `tblis` |  |
| `abcijk-ejac-ikeb/n1/b1` | 1.47053 ± 0.00966054 (W 0.00245372) | 5.74298 ± 0.0532096 (W 0.0141982) | 2.95024 ± 0.0611184 (W 0.00285546) | 🔵 tcontract 3.91× faster than `ttgt` | 🔵 tcontract 2.01× faster than `tblis` |  |
| `abcijk-ejbc-ikea/n1/b1` | 1.60899 ± 0.0120563 (W 0.00191503) | 6.2031 ± 0.0818557 (W 0.0107587) | 3.00276 ± 0.0275096 (W 0.00375462) | 🔵 tcontract 3.86× faster than `ttgt` | 🔵 tcontract 1.87× faster than `tblis` |  |
| `abcijk-ekab-ijec/n1/b1` | 1.47175 ± 0.0104315 (W 0.00163247) | 5.50635 ± 0.0976105 (W 0.0302344) | 2.98629 ± 0.0613089 (W 0.00169712) | 🔵 tcontract 3.74× faster than `ttgt` | 🔵 tcontract 2.03× faster than `tblis` |  |
| `abcijk-ekac-ijeb/n1/b1` | 1.47062 ± 0.0101667 (W 0.00103886) | 6.81936 ± 0.237128 (W 0.0124076) | 3.0217 ± 0.0502533 (W 0.0011719) | 🔵 tcontract 4.64× faster than `ttgt` | 🔵 tcontract 2.05× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ekbc-ijea/n1/b1` | 1.61079 ± 0.00857903 (W 0.00197604) | 6.43877 ± 0.249685 (W 0.0227538) | 2.98677 ± 0.0248851 (W 0.00297151) | 🔵 tcontract 4.00× faster than `ttgt` | 🔵 tcontract 1.85× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ijma-mkbc/n1/b1` | 1.59984 ± 0.0112477 (W 0.00168484) | 21.9357 ± 0.250067 (W 0.0252734) | 2.9992 ± 0.0316345 (W 0.00242127) | 🔵 tcontract 13.71× faster than `ttgt` | 🔵 tcontract 1.87× faster than `tblis` |  |
| `abcijk-ijmb-mkac/n1/b1` | 1.47006 ± 0.0111048 (W 0.00205101) | 20.4535 ± 0.239789 (W 0.0250637) | 3.03613 ± 0.0571399 (W 0.00217237) | 🔵 tcontract 13.91× faster than `ttgt` | 🔵 tcontract 2.07× faster than `tblis` |  |
| `abcijk-ijmc-mkab/n1/b1` | 1.47205 ± 0.00898536 (W 0.00165278) | 21.2859 ± 0.244741 (W 0.0183127) | 2.97205 ± 0.0586823 (W 0.00206748) | 🔵 tcontract 14.46× faster than `ttgt` | 🔵 tcontract 2.02× faster than `tblis` |  |
| `abcijk-ikma-mjbc/n1/b1` | 1.60678 ± 0.0118624 (W 0.0019158) | 24.2523 ± 0.31352 (W 0.0373965) | 2.99978 ± 0.0307061 (W 0.00226995) | 🔵 tcontract 15.09× faster than `ttgt` | 🔵 tcontract 1.87× faster than `tblis` |  |
| `abcijk-ikmb-mjac/n1/b1` | 1.46098 ± 0.00660102 (W 0.00182178) | 22.3257 ± 0.177593 (W 0.0358954) | 2.97522 ± 0.0704615 (W 0.00172327) | 🔵 tcontract 15.28× faster than `ttgt` | 🔵 tcontract 2.04× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 1.46973 ± 0.00695422 (W 0.00138378) | 22.7649 ± 0.17748 (W 0.0379127) | 2.99474 ± 0.0438402 (W 0.002012) | 🔵 tcontract 15.49× faster than `ttgt` | 🔵 tcontract 2.04× faster than `tblis` |  |
| `abcijk-jkma-mibc/n1/b1` | 1.60614 ± 0.0107202 (W 0.00114212) | 75.3561 ± 0.691572 (W 0.0371533) | 2.9642 ± 0.0335305 (W 0.00374686) | 🔵 tcontract 46.92× faster than `ttgt` | 🔵 tcontract 1.85× faster than `tblis` |  |
| `abcijk-jkmb-miac/n1/b1` | 1.45825 ± 0.00790704 (W 0.00241914) | 59.8671 ± 0.421403 (W 0.10098) | 3.02362 ± 0.022278 (W 0.00252555) | 🔵 tcontract 41.05× faster than `ttgt` | 🔵 tcontract 2.07× faster than `tblis` |  |
| `abcijk-jkmc-miab/n1/b1` | 1.48519 ± 0.0144128 (W 0.00177714) | 60.6081 ± 0.386477 (W 0.0355179) | 2.95835 ± 0.042806 (W 0.00304679) | 🔵 tcontract 40.81× faster than `ttgt` | 🔵 tcontract 1.99× faster than `tblis` |  |
| `abcs-rc-abrs/n1/b1` | 0.173683 ± 0.00221349 (W 0.00117909) | 0.591865 ± 0.00413134 (W 0.00382781) | 0.684651 ± 0.00429447 (W 0.00283593) | 🔵 tcontract 3.41× faster than `ttgt` | 🔵 tcontract 3.94× faster than `tblis` |  |
| `abj-bka-kj/n1/b1` | 1.04677 ± 0.0369336 (W 0.00454407) | 1.29003 ± 0.00263382 (W 0.00129544) | 1.40804 ± 0.00698408 (W 0.00246626) | 🔵 tcontract 1.23× faster than `ttgt` | 🔵 tcontract 1.35× faster than `tblis` | `!` between-start range over 5% |
| `abjc-cbka-kj/n1/b1` | 0.786447 ± 0.0142636 (W 0.0118853) | 0.669142 ± 0.00458486 (W 0.00125098) | 0.819735 ± 0.00125694 (W 0.00627102) | 🔴 tcontract 1.18× slower than `ttgt` | · |  |
| `abjc-kbac-jk/n1/b1` | 0.219821 ± 0.0015064 (W 0.000804739) | 0.646453 ± 0.000672409 (W 0.000975738) | 0.678751 ± 0.00455571 (W 0.00410175) | 🔵 tcontract 2.94× faster than `ttgt` | 🔵 tcontract 3.09× faster than `tblis` |  |
| `abjcd-dkbac-jk/n1/b1` | 1.85097 ± 0.0426984 (W 0.00282158) | 10.5073 ± 0.040478 (W 0.0237599) | 4.00483 ± 0.0187959 (W 0.0215065) | 🔵 tcontract 5.68× faster than `ttgt` | 🔵 tcontract 2.16× faster than `tblis` |  |
| `abrs-qb-aqrs/n1/b1` | 0.170473 ± 0.00224024 (W 0.000676011) | 0.600995 ± 0.0270121 (W 0.0233853) | 0.679332 ± 0.00135347 (W 0.00324285) | 🔵 tcontract 3.53× faster than `ttgt` | 🔵 tcontract 3.98× faster than `tblis` | `!` between-start range over 5% |
| `adbjc-cbdka-kj/n1/b1` | 5.09973 ± 0.124924 (W 0.0216072) | 7.02355 ± 0.18938 (W 0.0400856) | 5.62749 ± 0.196647 (W 0.0303529) | 🔵 tcontract 1.38× faster than `ttgt` | 🔵 tcontract 1.10× faster than `tblis` | `!` between-start range over 5% |
| `ajb-kba-jk/n1/b1` | 0.490999 ± 0.00562269 (W 0.00166958) | 1.22459 ± 0.0037016 (W 0.000987568) | 1.20774 ± 0.000606708 (W 0.00403515) | 🔵 tcontract 2.49× faster than `ttgt` | 🔵 tcontract 2.46× faster than `tblis` |  |
| `ajbc-ckba-jk/n1/b1` | 0.333886 ± 0.0030124 (W 0.0032939) | 1.98215 ± 0.00548598 (W 0.00598262) | 0.71249 ± 0.00293677 (W 0.0030596) | 🔵 tcontract 5.94× faster than `ttgt` | 🔵 tcontract 2.13× faster than `tblis` |  |
| `ajbdc-ckbad-jk/n1/b1` | 1.87287 ± 0.0282455 (W 0.00537683) | 13.9948 ± 0.153089 (W 0.0169976) | 3.9199 ± 0.0260317 (W 0.0218967) | 🔵 tcontract 7.47× faster than `ttgt` | 🔵 tcontract 2.09× faster than `tblis` |  |
| `aqrs-pa-pqrs/n1/b1` | 0.099145 ± 0.000749598 (W 0.000358016) | 0.556576 ± 0.00249551 (W 0.00310152) | 0.642902 ± 0.00492527 (W 0.00210178) | 🔵 tcontract 5.61× faster than `ttgt` | 🔵 tcontract 6.48× faster than `tblis` |  |
| `ij-ik-kj/n1/b1` | 1.05558 ± 0.00238689 (W 0.00112369) | 2.43188 ± 0.0221604 (W 0.00176106) | 2.55491 ± 0.00970413 (W 0.00177868) | 🔵 tcontract 2.30× faster than `ttgt` | 🔵 tcontract 2.42× faster than `tblis` |  |
| `ij-ikl-ljk/n1/b1` | 0.431372 ± 0.00414559 (W 0.00193334) | 0.93716 ± 0.00297172 (W 0.00101391) | 1.27536 ± 0.002589 (W 0.00250901) | 🔵 tcontract 2.17× faster than `ttgt` | 🔵 tcontract 2.96× faster than `tblis` |  |
| `ij-kil-lkj/n1/b1` | 0.644443 ± 8.20183e-05 (W 0.00104705) | 1.31783 ± 0.00125395 (W 0.00203181) | 1.79417 ± 0.00255891 (W 0.00536575) | 🔵 tcontract 2.04× faster than `ttgt` | 🔵 tcontract 2.78× faster than `tblis` |  |
| `ijk-ikl-lj/n1/b1` | 0.352675 ± 0.00147314 (W 0.00115151) | 0.922311 ± 0.000405832 (W 0.000926569) | 1.00966 ± 0.00295336 (W 0.00389372) | 🔵 tcontract 2.62× faster than `ttgt` | 🔵 tcontract 2.86× faster than `tblis` |  |
| `ijk-il-jlk/n1/b1` | 0.369974 ± 0.00052347 (W 0.00145036) | 0.965049 ± 0.0240144 (W 0.000974819) | 0.93395 ± 0.00247038 (W 0.00171149) | 🔵 tcontract 2.61× faster than `ttgt` | 🔵 tcontract 2.52× faster than `tblis` |  |
| `ijk-ilk-jl/n1/b1` | 0.343555 ± 0.000631744 (W 0.000897425) | 0.921351 ± 0.00148288 (W 0.00113667) | 0.885733 ± 0.000698307 (W 0.00309917) | 🔵 tcontract 2.68× faster than `ttgt` | 🔵 tcontract 2.58× faster than `tblis` |  |
| `ijk-ilk-lj/n1/b1` | 0.348325 ± 0.0035108 (W 0.000883589) | 0.932781 ± 0.00241889 (W 0.00148296) | 1.00302 ± 0.0020063 (W 0.00354) | 🔵 tcontract 2.68× faster than `ttgt` | 🔵 tcontract 2.88× faster than `tblis` |  |
| `ijk-ilmk-mjl/n1/b1` | 0.138674 ± 0.0029563 (W 0.00162029) | 0.401273 ± 0.00278256 (W 0.00149105) | 0.567066 ± 0.00169896 (W 0.00190504) | 🔵 tcontract 2.89× faster than `ttgt` | 🔵 tcontract 4.09× faster than `tblis` |  |
| `ijkl-imjn-lnkm/n1/b1` | 1.98572 ± 0.0112698 (W 0.00225685) | 4.01284 ± 0.0192156 (W 0.00272149) | 4.19085 ± 0.0268005 (W 0.00424402) | 🔵 tcontract 2.02× faster than `ttgt` | 🔵 tcontract 2.11× faster than `tblis` |  |
| `ijkl-imjn-nlmk/n1/b1` | 1.96066 ± 0.013346 (W 0.00165036) | 4.04667 ± 0.0210208 (W 0.00439052) | 4.26631 ± 0.00946514 (W 0.00314133) | 🔵 tcontract 2.06× faster than `ttgt` | 🔵 tcontract 2.18× faster than `tblis` |  |
| `ijkl-imkn-jnlm/n1/b1` | 1.93156 ± 0.00991616 (W 0.000988917) | 4.04742 ± 0.0262737 (W 0.00295057) | 4.17653 ± 0.0237058 (W 0.00431504) | 🔵 tcontract 2.10× faster than `ttgt` | 🔵 tcontract 2.16× faster than `tblis` |  |
| `ijkl-imkn-njml/n1/b1` | 1.96094 ± 0.0182445 (W 0.00160928) | 4.05243 ± 0.0159648 (W 0.00164115) | 4.29136 ± 0.00977917 (W 0.00229698) | 🔵 tcontract 2.07× faster than `ttgt` | 🔵 tcontract 2.19× faster than `tblis` |  |
| `ijkl-imln-jnkm/n1/b1` | 1.93533 ± 0.00895647 (W 0.00107917) | 4.03184 ± 0.0133639 (W 0.0075984) | 4.17789 ± 0.00426131 (W 0.00719155) | 🔵 tcontract 2.08× faster than `ttgt` | 🔵 tcontract 2.16× faster than `tblis` |  |
| `ijkl-imln-njmk/n1/b1` | 1.95701 ± 0.0121675 (W 0.00198942) | 4.05447 ± 0.0196185 (W 0.00629683) | 4.24467 ± 0.0183303 (W 0.00411949) | 🔵 tcontract 2.07× faster than `ttgt` | 🔵 tcontract 2.17× faster than `tblis` |  |
| `ijkl-imnj-nlkm/n1/b1` | 1.95515 ± 0.0279287 (W 0.00097451) | 4.05106 ± 0.0183921 (W 0.00201219) | 4.29561 ± 0.010588 (W 0.00395011) | 🔵 tcontract 2.07× faster than `ttgt` | 🔵 tcontract 2.20× faster than `tblis` |  |
| `ijkl-imnk-njml/n1/b1` | 1.95903 ± 0.0154751 (W 0.000986888) | 4.05011 ± 0.0164749 (W 0.00165461) | 4.29014 ± 0.0171329 (W 0.00251952) | 🔵 tcontract 2.07× faster than `ttgt` | 🔵 tcontract 2.19× faster than `tblis` |  |
| `ijkl-minj-nlmk/n1/b1` | 2.42304 ± 0.0276424 (W 0.00153998) | 4.92398 ± 0.0191995 (W 0.00466062) | 5.1976 ± 0.0203071 (W 0.0018122) | 🔵 tcontract 2.03× faster than `ttgt` | 🔵 tcontract 2.15× faster than `tblis` |  |
| `ijkl-mink-jnlm/n1/b1` | 2.33771 ± 0.0177168 (W 0.00104325) | 4.81793 ± 0.00796849 (W 0.00555271) | 4.96765 ± 0.0408115 (W 0.00230765) | 🔵 tcontract 2.06× faster than `ttgt` | 🔵 tcontract 2.13× faster than `tblis` |  |
| `ijkl-minl-njmk/n1/b1` | 2.4082 ± 0.0186197 (W 0.0021771) | 4.95106 ± 0.0218833 (W 0.00333786) | 5.08254 ± 0.000930828 (W 0.0016923) | 🔵 tcontract 2.06× faster than `ttgt` | 🔵 tcontract 2.11× faster than `tblis` |  |

## tcbench, f64, 4T (CPU 0-3)

| case | plan (ms) | ttgt (ms) | tblis (ms) | vs `ttgt` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `abc-bk-akc/n1/b1` | 0.094396 ± 0.00078015 (W 0.000776769) | 0.611894 ± 0.0280955 (W 0.00609481) | 0.252999 ± 0.00101786 (W 0.00343754) | 🔵 tcontract 6.48× faster than `ttgt` | 🔵 tcontract 2.68× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-eiab-jkec/n1/b1` | 0.390604 ± 0.00501625 (W 0.00118368) | 3.52537 ± 0.028917 (W 0.0129889) | 0.794377 ± 0.00406943 (W 0.00310196) | 🔵 tcontract 9.03× faster than `ttgt` | 🔵 tcontract 2.03× faster than `tblis` |  |
| `abcijk-eiac-jkeb/n1/b1` | 0.376835 ± 0.00203835 (W 0.00176622) | 3.83415 ± 0.056719 (W 0.0132786) | 0.829805 ± 0.0129819 (W 0.00320528) | 🔵 tcontract 10.17× faster than `ttgt` | 🔵 tcontract 2.20× faster than `tblis` |  |
| `abcijk-eibc-jkea/n1/b1` | 0.413102 ± 0.00194939 (W 0.00138678) | 4.36764 ± 0.0670274 (W 0.0260481) | 0.798477 ± 0.00174641 (W 0.00238185) | 🔵 tcontract 10.57× faster than `ttgt` | 🔵 tcontract 1.93× faster than `tblis` |  |
| `abcijk-ejab-ikec/n1/b1` | 0.383234 ± 0.000957149 (W 0.00232709) | 3.32598 ± 0.0273551 (W 0.00960351) | 0.803126 ± 0.00523225 (W 0.00407841) | 🔵 tcontract 8.68× faster than `ttgt` | 🔵 tcontract 2.10× faster than `tblis` |  |
| `abcijk-ejac-ikeb/n1/b1` | 0.374974 ± 0.000895116 (W 0.00134422) | 3.92945 ± 0.102433 (W 0.0224336) | 0.805437 ± 0.00436216 (W 0.00206098) | 🔵 tcontract 10.48× faster than `ttgt` | 🔵 tcontract 2.15× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ejbc-ikea/n1/b1` | 0.414322 ± 0.000534444 (W 0.00150182) | 4.41646 ± 0.0407484 (W 0.0192066) | 0.811756 ± 0.00219315 (W 0.00329964) | 🔵 tcontract 10.66× faster than `ttgt` | 🔵 tcontract 1.96× faster than `tblis` |  |
| `abcijk-ekab-ijec/n1/b1` | 0.383693 ± 0.00102039 (W 0.00137335) | 3.54995 ± 0.0253196 (W 0.0143163) | 0.797717 ± 0.00112519 (W 0.00185362) | 🔵 tcontract 9.25× faster than `ttgt` | 🔵 tcontract 2.08× faster than `tblis` |  |
| `abcijk-ekac-ijeb/n1/b1` | 0.376754 ± 0.00146462 (W 0.00144827) | 5.06689 ± 0.073439 (W 0.0643177) | 0.833375 ± 0.00882829 (W 0.00236994) | 🔵 tcontract 13.45× faster than `ttgt` | 🔵 tcontract 2.21× faster than `tblis` |  |
| `abcijk-ekbc-ijea/n1/b1` | 0.413372 ± 0.000676782 (W 0.00146119) | 4.84667 ± 0.099176 (W 0.0136514) | 0.812235 ± 0.00252653 (W 0.00236783) | 🔵 tcontract 11.72× faster than `ttgt` | 🔵 tcontract 1.96× faster than `tblis` |  |
| `abcijk-ijma-mkbc/n1/b1` | 0.413503 ± 0.00109168 (W 0.0014124) | 20.057 ± 0.141688 (W 0.0188531) | 0.813177 ± 0.00302874 (W 0.00401499) | 🔵 tcontract 48.51× faster than `ttgt` | 🔵 tcontract 1.97× faster than `tblis` |  |
| `abcijk-ijmb-mkac/n1/b1` | 0.374905 ± 0.000183413 (W 0.0019859) | 18.7511 ± 0.199019 (W 0.0208735) | 0.830245 ± 0.00243739 (W 0.00244196) | 🔵 tcontract 50.02× faster than `ttgt` | 🔵 tcontract 2.21× faster than `tblis` |  |
| `abcijk-ijmc-mkab/n1/b1` | 0.382914 ± 0.00105418 (W 0.00109659) | 19.466 ± 0.0929721 (W 0.0244832) | 0.801116 ± 0.00269997 (W 0.00374705) | 🔵 tcontract 50.84× faster than `ttgt` | 🔵 tcontract 2.09× faster than `tblis` |  |
| `abcijk-ikma-mjbc/n1/b1` | 0.413902 ± 0.00240551 (W 0.00128115) | 22.501 ± 0.705053 (W 0.034527) | 0.813476 ± 0.00379608 (W 0.00384142) | 🔵 tcontract 54.36× faster than `ttgt` | 🔵 tcontract 1.97× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ikmb-mjac/n1/b1` | 0.375144 ± 0.00205003 (W 0.00159716) | 20.2731 ± 0.137003 (W 0.0222499) | 0.803637 ± 0.00186757 (W 0.0011947) | 🔵 tcontract 54.04× faster than `ttgt` | 🔵 tcontract 2.14× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 0.383084 ± 0.000462925 (W 0.00132815) | 21.2406 ± 0.181775 (W 0.0572218) | 0.798246 ± 0.0060177 (W 0.00344641) | 🔵 tcontract 55.45× faster than `ttgt` | 🔵 tcontract 2.08× faster than `tblis` |  |
| `abcijk-jkma-mibc/n1/b1` | 0.412353 ± 0.00141747 (W 0.00130369) | 72.1463 ± 16.1247 (W 0.0864867) | 0.796946 ± 0.000685055 (W 0.00269973) | 🔵 tcontract 174.96× faster than `ttgt` | 🔵 tcontract 1.93× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmb-miac/n1/b1` | 0.373384 ± 0.00227462 (W 0.00100363) | 57.0712 ± 6.78351 (W 0.0331492) | 0.837174 ± 0.00928499 (W 0.00329904) | 🔵 tcontract 152.85× faster than `ttgt` | 🔵 tcontract 2.24× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmc-miab/n1/b1` | 0.389494 ± 0.00197881 (W 0.0014113) | 57.7088 ± 6.86695 (W 0.0685735) | 0.795827 ± 0.00654121 (W 0.00407424) | 🔵 tcontract 148.16× faster than `ttgt` | 🔵 tcontract 2.04× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcs-rc-abrs/n1/b1` | 0.054287 ± 0.000400666 (W 0.000575927) | 0.390924 ± 0.000900517 (W 0.0123608) | 0.223981 ± 0.000979864 (W 0.00321369) | 🔵 tcontract 7.20× faster than `ttgt` | 🔵 tcontract 4.13× faster than `tblis` |  |
| `abj-bka-kj/n1/b1` | 0.189872 ± 0.00273705 (W 0.00131119) | 0.683211 ± 0.00175298 (W 0.00153589) | 0.390444 ± 0.00243368 (W 0.00382571) | 🔵 tcontract 3.60× faster than `ttgt` | 🔵 tcontract 2.06× faster than `tblis` |  |
| `abjc-cbka-kj/n1/b1` | 0.127004 ± 0.00720798 (W 0.00105101) | 0.433371 ± 0.024493 (W 0.00139091) | 0.271789 ± 0.00201496 (W 0.00292282) | 🔵 tcontract 3.41× faster than `ttgt` | 🔵 tcontract 2.14× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abjc-kbac-jk/n1/b1` | 0.067497 ± 0.00203814 (W 0.00146913) | 0.4722 ± 0.000882338 (W 0.00131981) | 0.22646 ± 0.00208063 (W 0.0029153) | 🔵 tcontract 7.00× faster than `ttgt` | 🔵 tcontract 3.36× faster than `tblis` | `!` between-start range over 5% |
| `abjcd-dkbac-jk/n1/b1` | 0.562306 ± 0.00993718 (W 0.00262939) | 9.45563 ± 0.0399854 (W 0.0457716) | 1.39219 ± 0.00404295 (W 0.0204568) | 🔵 tcontract 16.82× faster than `ttgt` | 🔵 tcontract 2.48× faster than `tblis` |  |
| `abrs-qb-aqrs/n1/b1` | 0.053308 ± 0.00072 (W 0.00135885) | 0.388283 ± 0.00106246 (W 0.00253504) | 0.223021 ± 0.00177265 (W 0.0033383) | 🔵 tcontract 7.28× faster than `ttgt` | 🔵 tcontract 4.18× faster than `tblis` |  |
| `adbjc-cbdka-kj/n1/b1` | 1.80399 ± 0.201243 (W 0.0164034) | 5.65226 ± 0.0148753 (W 0.0111336) | 1.76131 ± 0.0558045 (W 0.0249057) | 🔵 tcontract 3.13× faster than `ttgt` | · | `!` between-start range over 5%; `p` position effect over 5% |
| `ajb-kba-jk/n1/b1` | 0.134875 ± 0.00130885 (W 0.000994523) | 0.675562 ± 0.0031842 (W 0.00175514) | 0.334386 ± 0.00380808 (W 0.00167886) | 🔵 tcontract 5.01× faster than `ttgt` | 🔵 tcontract 2.48× faster than `tblis` |  |
| `ajbc-ckba-jk/n1/b1` | 0.100076 ± 0.00546514 (W 0.00138615) | 1.77158 ± 0.00533153 (W 0.00572331) | 0.24307 ± 0.0016752 (W 0.00288527) | 🔵 tcontract 17.70× faster than `ttgt` | 🔵 tcontract 2.43× faster than `tblis` | `!` between-start range over 5% |
| `ajbdc-ckbad-jk/n1/b1` | 0.564097 ± 0.00444746 (W 0.00237939) | 13.0918 ± 0.100658 (W 0.034125) | 1.38511 ± 0.0260254 (W 0.0208196) | 🔵 tcontract 23.21× faster than `ttgt` | 🔵 tcontract 2.46× faster than `tblis` |  |
| `aqrs-pa-pqrs/n1/b1` | 0.035239 ± 0.000606028 (W 0.000521995) | 0.370385 ± 0.0138622 (W 0.00311546) | 0.208312 ± 0.000497765 (W 0.00357357) | 🔵 tcontract 10.51× faster than `ttgt` | 🔵 tcontract 5.91× faster than `tblis` | `!` between-start range over 5% |
| `ij-ik-kj/n1/b1` | 0.278438 ± 0.00114401 (W 0.00266946) | 0.918232 ± 0.0290378 (W 0.00192454) | 0.72426 ± 0.00498386 (W 0.00237871) | 🔵 tcontract 3.30× faster than `ttgt` | 🔵 tcontract 2.60× faster than `tblis` | `!` between-start range over 5% |
| `ij-ikl-ljk/n1/b1` | 0.219021 ± 0.0112053 (W 0.00321509) | 0.46747 ± 0.0127746 (W 0.00131072) | 0.522268 ± 0.000930448 (W 0.00234873) | 🔵 tcontract 2.13× faster than `ttgt` | 🔵 tcontract 2.38× faster than `tblis` | `!` between-start range over 5% |
| `ij-kil-lkj/n1/b1` | 0.319907 ± 0.00312005 (W 0.00166932) | 0.666062 ± 0.00152717 (W 0.00141618) | 0.719379 ± 0.00292539 (W 0.00207253) | 🔵 tcontract 2.08× faster than `ttgt` | 🔵 tcontract 2.25× faster than `tblis` |  |
| `ijk-ikl-lj/n1/b1` | 0.097296 ± 0.00080514 (W 0.000998978) | 0.519238 ± 0.0228784 (W 0.000933721) | 0.283218 ± 0.000514036 (W 0.00216962) | 🔵 tcontract 5.34× faster than `ttgt` | 🔵 tcontract 2.91× faster than `tblis` | `!` between-start range over 5% |
| `ijk-il-jlk/n1/b1` | 0.097486 ± 9.81495e-05 (W 0.00136526) | 0.614964 ± 0.0220671 (W 0.00751457) | 0.258449 ± 0.000790337 (W 0.00209529) | 🔵 tcontract 6.31× faster than `ttgt` | 🔵 tcontract 2.65× faster than `tblis` | `!` between-start range over 5% |
| `ijk-ilk-jl/n1/b1` | 0.093906 ± 0.000500133 (W 0.000664364) | 0.504459 ± 0.000907513 (W 0.00114012) | 0.254989 ± 0.00248912 (W 0.00221454) | 🔵 tcontract 5.37× faster than `ttgt` | 🔵 tcontract 2.72× faster than `tblis` |  |
| `ijk-ilk-lj/n1/b1` | 0.097746 ± 0.00112607 (W 0.0010375) | 0.491319 ± 0.0214106 (W 0.00084483) | 0.282638 ± 0.000972574 (W 0.00222867) | 🔵 tcontract 5.03× faster than `ttgt` | 🔵 tcontract 2.89× faster than `tblis` | `!` between-start range over 5% |
| `ijk-ilmk-mjl/n1/b1` | 0.045908 ± 0.000886247 (W 0.00099552) | 0.23173 ± 0.00112942 (W 0.000835988) | 0.170433 ± 0.00121503 (W 0.00219191) | 🔵 tcontract 5.05× faster than `ttgt` | 🔵 tcontract 3.71× faster than `tblis` |  |
| `ijkl-imjn-lnkm/n1/b1` | 0.521628 ± 0.000610437 (W 0.00174095) | 1.39166 ± 0.000466083 (W 0.00205598) | 1.14475 ± 0.001375 (W 0.0027279) | 🔵 tcontract 2.67× faster than `ttgt` | 🔵 tcontract 2.19× faster than `tblis` |  |
| `ijkl-imjn-nlmk/n1/b1` | 0.509638 ± 0.00130083 (W 0.00100391) | 1.39669 ± 0.000662012 (W 0.00351075) | 1.18312 ± 0.00433225 (W 0.00142941) | 🔵 tcontract 2.74× faster than `ttgt` | 🔵 tcontract 2.32× faster than `tblis` |  |
| `ijkl-imkn-jnlm/n1/b1` | 0.500978 ± 0.000689797 (W 0.00158456) | 1.39819 ± 0.000665638 (W 0.00163886) | 1.14276 ± 0.00467532 (W 0.00150692) | 🔵 tcontract 2.79× faster than `ttgt` | 🔵 tcontract 2.28× faster than `tblis` |  |
| `ijkl-imkn-njml/n1/b1` | 0.505969 ± 0.0008903 (W 0.00167872) | 1.404 ± 0.000271073 (W 0.00232236) | 1.18274 ± 0.00362893 (W 0.00138105) | 🔵 tcontract 2.77× faster than `ttgt` | 🔵 tcontract 2.34× faster than `tblis` |  |
| `ijkl-imln-jnkm/n1/b1` | 0.499429 ± 0.00112398 (W 0.00135228) | 1.3974 ± 0.00380091 (W 0.00591551) | 1.14313 ± 0.00266338 (W 0.00230222) | 🔵 tcontract 2.80× faster than `ttgt` | 🔵 tcontract 2.29× faster than `tblis` |  |
| `ijkl-imln-njmk/n1/b1` | 0.504559 ± 0.00114928 (W 0.00112374) | 1.39681 ± 0.00411318 (W 0.00186349) | 1.17553 ± 0.00469053 (W 0.00195053) | 🔵 tcontract 2.77× faster than `ttgt` | 🔵 tcontract 2.33× faster than `tblis` |  |
| `ijkl-imnj-nlkm/n1/b1` | 0.510059 ± 0.0014077 (W 0.0019731) | 1.39335 ± 0.00477867 (W 0.00390339) | 1.18413 ± 0.00681656 (W 0.00376243) | 🔵 tcontract 2.73× faster than `ttgt` | 🔵 tcontract 2.32× faster than `tblis` |  |
| `ijkl-imnk-njml/n1/b1` | 0.505959 ± 0.000550121 (W 0.00132638) | 1.39392 ± 0.00265975 (W 0.00290943) | 1.17689 ± 0.00432498 (W 0.000802702) | 🔵 tcontract 2.76× faster than `ttgt` | 🔵 tcontract 2.33× faster than `tblis` |  |
| `ijkl-minj-nlmk/n1/b1` | 0.631423 ± 0.00477328 (W 0.00137454) | 1.71866 ± 0.00550515 (W 0.00604448) | 1.42549 ± 0.00829062 (W 0.00246046) | 🔵 tcontract 2.72× faster than `ttgt` | 🔵 tcontract 2.26× faster than `tblis` |  |
| `ijkl-mink-jnlm/n1/b1` | 0.602525 ± 0.00140158 (W 0.00113749) | 1.6513 ± 0.0035763 (W 0.00215166) | 1.36276 ± 0.00883624 (W 0.00252327) | 🔵 tcontract 2.74× faster than `ttgt` | 🔵 tcontract 2.26× faster than `tblis` |  |
| `ijkl-minl-njmk/n1/b1` | 0.625074 ± 0.0012755 (W 0.0024896) | 1.71626 ± 0.00885669 (W 0.00273736) | 1.41054 ± 0.00484918 (W 0.00219477) | 🔵 tcontract 2.75× faster than `ttgt` | 🔵 tcontract 2.26× faster than `tblis` |  |

## tcbench, c64, 1T (CPU 0)

| case | plan (ms) | ttgt (ms) | tblis (ms) | vs `ttgt` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `abc-bk-akc/n1/b1` | 1.33085 ± 0.0141252 (W 0.00109011) | 2.71432 ± 0.0188768 (W 0.00306491) | 2.67527 ± 0.00992441 (W 0.00155186) | 🔵 tcontract 2.04× faster than `ttgt` | 🔵 tcontract 2.01× faster than `tblis` |  |
| `abcijk-eiab-jkec/n1/b1` | 6.13371 ± 0.00485277 (W 0.00981868) | 23.4586 ± 0.0660045 (W 0.059318) | 11.2709 ± 0.0860734 (W 0.0532401) | 🔵 tcontract 3.82× faster than `ttgt` | 🔵 tcontract 1.84× faster than `tblis` |  |
| `abcijk-eiac-jkeb/n1/b1` | 6.07703 ± 0.0110122 (W 0.00607981) | 23.4398 ± 0.192096 (W 0.0884625) | 11.8472 ± 0.0924848 (W 0.0233222) | 🔵 tcontract 3.86× faster than `ttgt` | 🔵 tcontract 1.95× faster than `tblis` |  |
| `abcijk-eibc-jkea/n1/b1` | 6.20733 ± 0.0102897 (W 0.00407694) | 25.2889 ± 0.0852787 (W 0.053186) | 11.21 ± 0.047278 (W 0.0313178) | 🔵 tcontract 4.07× faster than `ttgt` | 🔵 tcontract 1.81× faster than `tblis` |  |
| `abcijk-ejab-ikec/n1/b1` | 6.08748 ± 0.0143583 (W 0.00656543) | 23.2384 ± 0.150679 (W 0.0341942) | 11.0471 ± 0.0212467 (W 0.0106337) | 🔵 tcontract 3.82× faster than `ttgt` | 🔵 tcontract 1.81× faster than `tblis` |  |
| `abcijk-ejac-ikeb/n1/b1` | 6.08232 ± 0.0112445 (W 0.00591107) | 23.4208 ± 0.082793 (W 0.050768) | 11.5305 ± 0.0738719 (W 0.00598387) | 🔵 tcontract 3.85× faster than `ttgt` | 🔵 tcontract 1.90× faster than `tblis` |  |
| `abcijk-ejbc-ikea/n1/b1` | 6.21425 ± 0.0146027 (W 0.00534094) | 25.6106 ± 0.105131 (W 0.0614994) | 11.7854 ± 0.0593344 (W 0.026201) | 🔵 tcontract 4.12× faster than `ttgt` | 🔵 tcontract 1.90× faster than `tblis` |  |
| `abcijk-ekab-ijec/n1/b1` | 6.08434 ± 0.00926565 (W 0.0073731) | 23.2997 ± 0.200445 (W 0.0660415) | 11.0396 ± 0.00896583 (W 0.0206184) | 🔵 tcontract 3.83× faster than `ttgt` | 🔵 tcontract 1.81× faster than `tblis` |  |
| `abcijk-ekac-ijeb/n1/b1` | 6.08479 ± 0.00951726 (W 0.00678177) | 24.0719 ± 0.16751 (W 0.03573) | 11.4049 ± 0.155938 (W 0.00780904) | 🔵 tcontract 3.96× faster than `ttgt` | 🔵 tcontract 1.87× faster than `tblis` |  |
| `abcijk-ekbc-ijea/n1/b1` | 6.22574 ± 0.00545343 (W 0.0080171) | 26.1461 ± 0.276679 (W 0.0550902) | 11.8 ± 0.0427781 (W 0.0251242) | 🔵 tcontract 4.20× faster than `ttgt` | 🔵 tcontract 1.90× faster than `tblis` |  |
| `abcijk-ijma-mkbc/n1/b1` | 6.21082 ± 0.0108433 (W 0.00753143) | 38.5499 ± 0.296046 (W 0.167307) | 11.8032 ± 0.0323933 (W 0.0259044) | 🔵 tcontract 6.21× faster than `ttgt` | 🔵 tcontract 1.90× faster than `tblis` |  |
| `abcijk-ijmb-mkac/n1/b1` | 6.07394 ± 0.00160622 (W 0.00725724) | 39.0865 ± 0.069895 (W 0.154272) | 11.3946 ± 0.131619 (W 0.010569) | 🔵 tcontract 6.44× faster than `ttgt` | 🔵 tcontract 1.88× faster than `tblis` |  |
| `abcijk-ijmc-mkab/n1/b1` | 6.09828 ± 0.0125676 (W 0.0106305) | 41.0348 ± 0.008888 (W 0.0733318) | 11.0388 ± 0.02228 (W 0.0163859) | 🔵 tcontract 6.73× faster than `ttgt` | 🔵 tcontract 1.81× faster than `tblis` |  |
| `abcijk-ikma-mjbc/n1/b1` | 6.21684 ± 0.0165572 (W 0.00408306) | 39.6455 ± 0.801204 (W 0.114441) | 11.8013 ± 0.0753179 (W 0.0192836) | 🔵 tcontract 6.38× faster than `ttgt` | 🔵 tcontract 1.90× faster than `tblis` |  |
| `abcijk-ikmb-mjac/n1/b1` | 6.08302 ± 0.011566 (W 0.00493969) | 39.8492 ± 0.166069 (W 0.0773645) | 11.6015 ± 0.0882546 (W 0.00888846) | 🔵 tcontract 6.55× faster than `ttgt` | 🔵 tcontract 1.91× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 6.0831 ± 0.00670798 (W 0.0139258) | 42.1759 ± 0.252258 (W 0.151213) | 11.0928 ± 0.0622661 (W 0.012027) | 🔵 tcontract 6.93× faster than `ttgt` | 🔵 tcontract 1.82× faster than `tblis` |  |
| `abcijk-jkma-mibc/n1/b1` | 6.20274 ± 0.0170067 (W 0.00411437) | 63.7786 ± 1.13606 (W 0.119812) | 11.2004 ± 0.0591983 (W 0.0208345) | 🔵 tcontract 10.28× faster than `ttgt` | 🔵 tcontract 1.81× faster than `tblis` |  |
| `abcijk-jkmb-miac/n1/b1` | 6.08129 ± 0.0126465 (W 0.00931261) | 64.5389 ± 1.73349 (W 0.0569053) | 11.8445 ± 0.109113 (W 0.0338238) | 🔵 tcontract 10.61× faster than `ttgt` | 🔵 tcontract 1.95× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-jkmc-miab/n1/b1` | 6.1317 ± 0.0110268 (W 0.00983836) | 63.242 ± 0.688521 (W 0.0715131) | 11.3928 ± 0.150328 (W 0.0489042) | 🔵 tcontract 10.31× faster than `ttgt` | 🔵 tcontract 1.86× faster than `tblis` |  |
| `abcs-rc-abrs/n1/b1` | 0.593874 ± 0.00307952 (W 0.00146323) | 1.19114 ± 0.00739331 (W 0.00149747) | 1.36073 ± 0.00580789 (W 0.00163189) | 🔵 tcontract 2.01× faster than `ttgt` | 🔵 tcontract 2.29× faster than `tblis` |  |
| `abj-bka-kj/n1/b1` | 2.49849 ± 0.00978415 (W 0.00208009) | 3.82466 ± 0.00246617 (W 0.00323917) | 4.0926 ± 0.0184849 (W 0.0035329) | 🔵 tcontract 1.53× faster than `ttgt` | 🔵 tcontract 1.64× faster than `tblis` |  |
| `abjc-cbka-kj/n1/b1` | 1.44576 ± 0.00331565 (W 0.00232486) | 1.67061 ± 0.00115131 (W 0.0032614) | 1.71326 ± 0.0122795 (W 0.00380643) | 🔵 tcontract 1.16× faster than `ttgt` | 🔵 tcontract 1.19× faster than `tblis` |  |
| `abjc-kbac-jk/n1/b1` | 0.7285 ± 0.00259299 (W 0.000837902) | 1.55194 ± 0.00417368 (W 0.00129762) | 1.48023 ± 0.00259452 (W 0.00341038) | 🔵 tcontract 2.13× faster than `ttgt` | 🔵 tcontract 2.03× faster than `tblis` |  |
| `abjcd-dkbac-jk/n1/b1` | 4.96422 ± 0.0920605 (W 0.0199313) | 16.4919 ± 0.264904 (W 0.0996862) | 10.3747 ± 0.0624259 (W 0.0349056) | 🔵 tcontract 3.32× faster than `ttgt` | 🔵 tcontract 2.09× faster than `tblis` |  |
| `abrs-qb-aqrs/n1/b1` | 0.563576 ± 0.00147021 (W 0.00107672) | 1.21941 ± 0.019987 (W 0.00425761) | 1.3665 ± 0.00283644 (W 0.00272643) | 🔵 tcontract 2.16× faster than `ttgt` | 🔵 tcontract 2.42× faster than `tblis` |  |
| `adbjc-cbdka-kj/n1/b1` | 9.31245 ± 0.138694 (W 0.0335949) | 13.3022 ± 0.0457784 (W 0.01285) | 11.1286 ± 0.193075 (W 0.0950795) | 🔵 tcontract 1.43× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `ajb-kba-jk/n1/b1` | 1.82927 ± 0.00798679 (W 0.000441169) | 3.89827 ± 0.00785986 (W 0.00216339) | 3.61651 ± 0.0206621 (W 0.0068667) | 🔵 tcontract 2.13× faster than `ttgt` | 🔵 tcontract 1.98× faster than `tblis` |  |
| `ajbc-ckba-jk/n1/b1` | 0.882053 ± 0.00244633 (W 0.0017008) | 2.84572 ± 0.418987 (W 0.00594275) | 1.554 ± 0.00858261 (W 0.00346818) | 🔵 tcontract 3.23× faster than `ttgt` | 🔵 tcontract 1.76× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `ajbdc-ckbad-jk/n1/b1` | 5.32604 ± 0.0547188 (W 0.0254703) | 19.8357 ± 0.109558 (W 0.147287) | 9.89049 ± 0.331381 (W 0.0487774) | 🔵 tcontract 3.72× faster than `ttgt` | 🔵 tcontract 1.86× faster than `tblis` | `!` between-start range over 5% |
| `aqrs-pa-pqrs/n1/b1` | 0.633023 ± 0.00208486 (W 0.00136393) | 1.16357 ± 0.00932861 (W 0.00164495) | 1.36442 ± 0.00922936 (W 0.0012086) | 🔵 tcontract 1.84× faster than `ttgt` | 🔵 tcontract 2.16× faster than `tblis` |  |
| `ij-ik-kj/n1/b1` | 4.48616 ± 0.00624244 (W 0.00145869) | 8.70599 ± 0.0277976 (W 0.00238742) | 8.99377 ± 0.0210735 (W 0.00287185) | 🔵 tcontract 1.94× faster than `ttgt` | 🔵 tcontract 2.00× faster than `tblis` |  |
| `ij-ikl-ljk/n1/b1` | 1.42179 ± 0.00113382 (W 0.00122228) | 2.67622 ± 0.0271766 (W 0.00498594) | 3.15001 ± 0.022794 (W 0.00215475) | 🔵 tcontract 1.88× faster than `ttgt` | 🔵 tcontract 2.22× faster than `tblis` |  |
| `ij-kil-lkj/n1/b1` | 2.04728 ± 0.000836441 (W 0.00128148) | 3.80463 ± 0.0540797 (W 0.0339921) | 4.42385 ± 0.0143048 (W 0.00488649) | 🔵 tcontract 1.86× faster than `ttgt` | 🔵 tcontract 2.16× faster than `tblis` |  |
| `ijk-ikl-lj/n1/b1` | 1.3106 ± 0.00365413 (W 0.00104076) | 2.6818 ± 0.00252017 (W 0.00340467) | 2.82338 ± 0.00527639 (W 0.00279776) | 🔵 tcontract 2.05× faster than `ttgt` | 🔵 tcontract 2.15× faster than `tblis` |  |
| `ijk-il-jlk/n1/b1` | 1.41152 ± 0.0116074 (W 0.00154242) | 2.73255 ± 0.0302348 (W 0.000958794) | 2.77034 ± 0.0108341 (W 0.00113482) | 🔵 tcontract 1.94× faster than `ttgt` | 🔵 tcontract 1.96× faster than `tblis` |  |
| `ijk-ilk-jl/n1/b1` | 1.3341 ± 0.00227581 (W 0.00100936) | 2.71572 ± 0.00495654 (W 0.000907941) | 2.67468 ± 0.00807733 (W 0.00241738) | 🔵 tcontract 2.04× faster than `ttgt` | 🔵 tcontract 2.00× faster than `tblis` |  |
| `ijk-ilk-lj/n1/b1` | 1.31652 ± 0.00789131 (W 0.00125925) | 2.70494 ± 0.00450409 (W 0.00126018) | 2.82455 ± 0.00834877 (W 0.00286207) | 🔵 tcontract 2.05× faster than `ttgt` | 🔵 tcontract 2.15× faster than `tblis` |  |
| `ijk-ilmk-mjl/n1/b1` | 0.49361 ± 0.00210781 (W 0.000988284) | 1.00557 ± 0.0155394 (W 0.00111345) | 1.14527 ± 0.00763601 (W 0.000751243) | 🔵 tcontract 2.04× faster than `ttgt` | 🔵 tcontract 2.32× faster than `tblis` |  |
| `ijkl-imjn-lnkm/n1/b1` | 7.72204 ± 0.0452393 (W 0.00412844) | 14.9004 ± 0.0307129 (W 0.0113535) | 15.1439 ± 0.0304442 (W 0.00598162) | 🔵 tcontract 1.93× faster than `ttgt` | 🔵 tcontract 1.96× faster than `tblis` |  |
| `ijkl-imjn-nlmk/n1/b1` | 7.63721 ± 0.0389135 (W 0.00245121) | 14.7691 ± 0.0426888 (W 0.00494232) | 15.4779 ± 0.125031 (W 0.00492838) | 🔵 tcontract 1.93× faster than `ttgt` | 🔵 tcontract 2.03× faster than `tblis` |  |
| `ijkl-imkn-jnlm/n1/b1` | 7.68433 ± 0.033723 (W 0.00382917) | 14.8957 ± 0.0227098 (W 0.0175106) | 15.0673 ± 0.123595 (W 0.00344475) | 🔵 tcontract 1.94× faster than `ttgt` | 🔵 tcontract 1.96× faster than `tblis` |  |
| `ijkl-imkn-njml/n1/b1` | 7.63623 ± 0.036051 (W 0.00345772) | 14.775 ± 0.0576973 (W 0.00697154) | 15.452 ± 0.0184891 (W 0.00798181) | 🔵 tcontract 1.93× faster than `ttgt` | 🔵 tcontract 2.02× faster than `tblis` |  |
| `ijkl-imln-jnkm/n1/b1` | 7.68117 ± 0.0333216 (W 0.00222151) | 14.9065 ± 0.036018 (W 0.0104954) | 15.1172 ± 0.0206597 (W 0.00439112) | 🔵 tcontract 1.94× faster than `ttgt` | 🔵 tcontract 1.97× faster than `tblis` |  |
| `ijkl-imln-njmk/n1/b1` | 7.61135 ± 0.0435128 (W 0.0666167) | 14.776 ± 0.0404749 (W 0.00781295) | 15.1558 ± 0.0570558 (W 0.00339637) | 🔵 tcontract 1.94× faster than `ttgt` | 🔵 tcontract 1.99× faster than `tblis` |  |
| `ijkl-imnj-nlkm/n1/b1` | 7.63786 ± 0.0440265 (W 0.00137491) | 14.778 ± 0.0485003 (W 0.00616426) | 15.413 ± 0.0918436 (W 0.00265422) | 🔵 tcontract 1.93× faster than `ttgt` | 🔵 tcontract 2.02× faster than `tblis` |  |
| `ijkl-imnk-njml/n1/b1` | 7.62322 ± 0.0235102 (W 0.00751484) | 14.7722 ± 0.0239816 (W 0.00684358) | 15.5242 ± 0.0582728 (W 0.00531287) | 🔵 tcontract 1.94× faster than `ttgt` | 🔵 tcontract 2.04× faster than `tblis` |  |
| `ijkl-minj-nlmk/n1/b1` | 9.43726 ± 0.0613961 (W 0.00502392) | 17.8715 ± 0.0611858 (W 0.00992085) | 18.9632 ± 0.0725418 (W 0.00705361) | 🔵 tcontract 1.89× faster than `ttgt` | 🔵 tcontract 2.01× faster than `tblis` |  |
| `ijkl-mink-jnlm/n1/b1` | 9.14794 ± 0.0510392 (W 0.00376556) | 17.9039 ± 0.0371889 (W 0.00886385) | 18.1473 ± 0.0687409 (W 0.0100752) | 🔵 tcontract 1.96× faster than `ttgt` | 🔵 tcontract 1.98× faster than `tblis` |  |
| `ijkl-minl-njmk/n1/b1` | 9.38552 ± 0.0215105 (W 0.00240029) | 17.8478 ± 0.0586483 (W 0.00677026) | 18.5397 ± 0.0741887 (W 0.00725457) | 🔵 tcontract 1.90× faster than `ttgt` | 🔵 tcontract 1.98× faster than `tblis` |  |

## tcbench, c64, 4T (CPU 0-3)

| case | plan (ms) | ttgt (ms) | tblis (ms) | vs `ttgt` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `abc-bk-akc/n1/b1` | 0.347975 ± 0.000905373 (W 0.00164887) | 1.11417 ± 0.00879147 (W 0.0160464) | 0.70839 ± 0.000755932 (W 0.00235805) | 🔵 tcontract 3.20× faster than `ttgt` | 🔵 tcontract 2.04× faster than `tblis` |  |
| `abcijk-eiab-jkec/n1/b1` | 1.55619 ± 0.00447596 (W 0.00280398) | 16.578 ± 0.0177239 (W 0.038833) | 2.9383 ± 0.0219731 (W 0.0230403) | 🔵 tcontract 10.65× faster than `ttgt` | 🔵 tcontract 1.89× faster than `tblis` |  |
| `abcijk-eiac-jkeb/n1/b1` | 1.55339 ± 0.00230228 (W 0.00213072) | 16.6414 ± 0.0774944 (W 0.0633582) | 3.10516 ± 0.0318701 (W 0.00661029) | 🔵 tcontract 10.71× faster than `ttgt` | 🔵 tcontract 2.00× faster than `tblis` |  |
| `abcijk-eibc-jkea/n1/b1` | 1.58503 ± 0.00330759 (W 0.00356158) | 18.3738 ± 0.0481935 (W 0.0849276) | 2.89323 ± 0.00429214 (W 0.00437513) | 🔵 tcontract 11.59× faster than `ttgt` | 🔵 tcontract 1.83× faster than `tblis` |  |
| `abcijk-ejab-ikec/n1/b1` | 1.54007 ± 0.00254189 (W 0.00200816) | 16.3387 ± 0.0936371 (W 0.0616674) | 2.85514 ± 0.00303713 (W 0.00507265) | 🔵 tcontract 10.61× faster than `ttgt` | 🔵 tcontract 1.85× faster than `tblis` |  |
| `abcijk-ejac-ikeb/n1/b1` | 1.5568 ± 0.00486734 (W 0.00227025) | 16.4539 ± 0.0506985 (W 0.0934821) | 2.93444 ± 0.018491 (W 0.00611314) | 🔵 tcontract 10.57× faster than `ttgt` | 🔵 tcontract 1.88× faster than `tblis` |  |
| `abcijk-ejbc-ikea/n1/b1` | 1.58618 ± 0.00202999 (W 0.002676) | 18.629 ± 0.0157908 (W 0.0631051) | 3.07828 ± 0.0150982 (W 0.00833642) | 🔵 tcontract 11.74× faster than `ttgt` | 🔵 tcontract 1.94× faster than `tblis` |  |
| `abcijk-ekab-ijec/n1/b1` | 1.54367 ± 0.00221963 (W 0.00262686) | 16.34 ± 0.0780057 (W 0.0623668) | 2.81626 ± 0.0101235 (W 0.00800163) | 🔵 tcontract 10.59× faster than `ttgt` | 🔵 tcontract 1.82× faster than `tblis` |  |
| `abcijk-ekac-ijeb/n1/b1` | 1.55486 ± 0.000441826 (W 0.00212771) | 17.2318 ± 0.0883936 (W 0.0526667) | 2.94879 ± 0.0144084 (W 0.00828684) | 🔵 tcontract 11.08× faster than `ttgt` | 🔵 tcontract 1.90× faster than `tblis` |  |
| `abcijk-ekbc-ijea/n1/b1` | 1.58705 ± 0.00237148 (W 0.00204209) | 19.1048 ± 0.123042 (W 0.0546173) | 3.06833 ± 0.00532278 (W 0.00715074) | 🔵 tcontract 12.04× faster than `ttgt` | 🔵 tcontract 1.93× faster than `tblis` |  |
| `abcijk-ijma-mkbc/n1/b1` | 1.58541 ± 0.00302461 (W 0.00407757) | 31.8444 ± 0.0378791 (W 0.0339891) | 3.07319 ± 0.0124638 (W 0.00437096) | 🔵 tcontract 20.09× faster than `ttgt` | 🔵 tcontract 1.94× faster than `tblis` |  |
| `abcijk-ijmb-mkac/n1/b1` | 1.55394 ± 0.00138761 (W 0.00261334) | 32.3016 ± 0.148668 (W 0.0357637) | 2.96212 ± 0.0173531 (W 0.00599173) | 🔵 tcontract 20.79× faster than `ttgt` | 🔵 tcontract 1.91× faster than `tblis` |  |
| `abcijk-ijmc-mkab/n1/b1` | 1.5391 ± 0.00163323 (W 0.00198585) | 34.3044 ± 0.109243 (W 0.083749) | 2.81653 ± 0.00189041 (W 0.00658843) | 🔵 tcontract 22.29× faster than `ttgt` | 🔵 tcontract 1.83× faster than `tblis` |  |
| `abcijk-ikma-mjbc/n1/b1` | 1.584 ± 0.00327958 (W 0.00588223) | 34.3926 ± 0.926729 (W 0.0692681) | 3.08724 ± 0.0109892 (W 0.00867917) | 🔵 tcontract 21.71× faster than `ttgt` | 🔵 tcontract 1.95× faster than `tblis` |  |
| `abcijk-ikmb-mjac/n1/b1` | 1.55452 ± 0.000361788 (W 0.00243661) | 33.2457 ± 0.321177 (W 0.094442) | 2.92743 ± 0.0133239 (W 0.00781263) | 🔵 tcontract 21.39× faster than `ttgt` | 🔵 tcontract 1.88× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 1.53623 ± 0.00522191 (W 0.00293814) | 35.7859 ± 0.32331 (W 0.147593) | 2.85012 ± 0.014716 (W 0.00691847) | 🔵 tcontract 23.29× faster than `ttgt` | 🔵 tcontract 1.86× faster than `tblis` |  |
| `abcijk-jkma-mibc/n1/b1` | 1.5857 ± 0.00256057 (W 0.0038282) | 57.4748 ± 0.213855 (W 0.0451814) | 2.88564 ± 0.00785222 (W 0.00466386) | 🔵 tcontract 36.25× faster than `ttgt` | 🔵 tcontract 1.82× faster than `tblis` |  |
| `abcijk-jkmb-miac/n1/b1` | 1.55594 ± 0.00319221 (W 0.00253691) | 56.3216 ± 0.793168 (W 0.0765093) | 3.12684 ± 0.0425582 (W 0.0185839) | 🔵 tcontract 36.20× faster than `ttgt` | 🔵 tcontract 2.01× faster than `tblis` |  |
| `abcijk-jkmc-miab/n1/b1` | 1.55086 ± 0.00650421 (W 0.00186863) | 57.3058 ± 0.626228 (W 0.222853) | 2.94002 ± 0.00448743 (W 0.00643079) | 🔵 tcontract 36.95× faster than `ttgt` | 🔵 tcontract 1.90× faster than `tblis` |  |
| `abcs-rc-abrs/n1/b1` | 0.161733 ± 0.000526859 (W 0.000894658) | 0.571506 ± 0.0030658 (W 0.00182741) | 0.398763 ± 0.00306294 (W 0.002664) | 🔵 tcontract 3.53× faster than `ttgt` | 🔵 tcontract 2.47× faster than `tblis` |  |
| `abj-bka-kj/n1/b1` | 0.527927 ± 0.000630505 (W 0.00142677) | 1.46439 ± 0.00582063 (W 0.00296297) | 1.06185 ± 0.00284881 (W 0.0021923) | 🔵 tcontract 2.77× faster than `ttgt` | 🔵 tcontract 2.01× faster than `tblis` |  |
| `abjc-cbka-kj/n1/b1` | 0.288858 ± 0.000265588 (W 0.00212131) | 0.915431 ± 0.00306828 (W 0.00232902) | 0.502339 ± 0.00389503 (W 0.00425544) | 🔵 tcontract 3.17× faster than `ttgt` | 🔵 tcontract 1.74× faster than `tblis` |  |
| `abjc-kbac-jk/n1/b1` | 0.199742 ± 0.0023217 (W 0.000909473) | 0.839995 ± 0.00293513 (W 0.0014218) | 0.426482 ± 0.00212665 (W 0.00309964) | 🔵 tcontract 4.21× faster than `ttgt` | 🔵 tcontract 2.14× faster than `tblis` |  |
| `abjcd-dkbac-jk/n1/b1` | 1.4618 ± 0.0264668 (W 0.0048894) | 13.4954 ± 0.498863 (W 0.0976507) | 3.15202 ± 0.0311608 (W 0.0251172) | 🔵 tcontract 9.23× faster than `ttgt` | 🔵 tcontract 2.16× faster than `tblis` | `!` between-start range over 5% |
| `abrs-qb-aqrs/n1/b1` | 0.153264 ± 0.00056676 (W 0.00117335) | 0.618624 ± 0.00322478 (W 0.00159541) | 0.404922 ± 0.00243033 (W 0.00401905) | 🔵 tcontract 4.04× faster than `ttgt` | 🔵 tcontract 2.64× faster than `tblis` |  |
| `adbjc-cbdka-kj/n1/b1` | 3.13292 ± 0.0230868 (W 0.0304961) | 9.34775 ± 0.0813701 (W 0.0227374) | 3.37846 ± 0.0213645 (W 0.0215464) | 🔵 tcontract 2.98× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `ajb-kba-jk/n1/b1` | 0.47779 ± 0.00619281 (W 0.00145449) | 1.64868 ± 0.00876623 (W 0.00159889) | 0.94345 ± 0.00239478 (W 0.00427388) | 🔵 tcontract 3.45× faster than `ttgt` | 🔵 tcontract 1.97× faster than `tblis` |  |
| `ajbc-ckba-jk/n1/b1` | 0.24235 ± 0.00174706 (W 0.00184063) | 2.14428 ± 0.0433708 (W 0.00341689) | 0.457491 ± 0.00168036 (W 0.00506067) | 🔵 tcontract 8.85× faster than `ttgt` | 🔵 tcontract 1.89× faster than `tblis` |  |
| `ajbdc-ckbad-jk/n1/b1` | 1.58162 ± 0.0294663 (W 0.00399038) | 16.1642 ± 0.222861 (W 0.0642228) | 3.08459 ± 0.0439117 (W 0.0225689) | 🔵 tcontract 10.22× faster than `ttgt` | 🔵 tcontract 1.95× faster than `tblis` |  |
| `aqrs-pa-pqrs/n1/b1` | 0.267029 ± 0.00628246 (W 0.00223197) | 0.557217 ± 0.0186369 (W 0.00101719) | 0.388763 ± 0.00217187 (W 0.00254649) | 🔵 tcontract 2.09× faster than `ttgt` | 🔵 tcontract 1.46× faster than `tblis` | `!` between-start range over 5% |
| `ij-ik-kj/n1/b1` | 1.15832 ± 0.00300617 (W 0.0022771) | 2.45498 ± 0.00113988 (W 0.00148564) | 2.34417 ± 0.00731476 (W 0.00138732) | 🔵 tcontract 2.12× faster than `ttgt` | 🔵 tcontract 2.02× faster than `tblis` |  |
| `ij-ikl-ljk/n1/b1` | 0.579706 ± 0.00693977 (W 0.00358749) | 0.959719 ± 0.0309878 (W 0.00131315) | 0.929111 ± 0.0024852 (W 0.00130686) | 🔵 tcontract 1.66× faster than `ttgt` | 🔵 tcontract 1.60× faster than `tblis` | `!` between-start range over 5% |
| `ij-kil-lkj/n1/b1` | 0.796376 ± 0.00457101 (W 0.00374542) | 1.44332 ± 0.0243004 (W 0.0089871) | 1.30361 ± 0.00752209 (W 0.00228926) | 🔵 tcontract 1.81× faster than `ttgt` | 🔵 tcontract 1.64× faster than `tblis` |  |
| `ijk-ikl-lj/n1/b1` | 0.341936 ± 0.00183634 (W 0.00129447) | 0.975899 ± 0.00715078 (W 0.000764786) | 0.748419 ± 0.00471331 (W 0.00327859) | 🔵 tcontract 2.85× faster than `ttgt` | 🔵 tcontract 2.19× faster than `tblis` |  |
| `ijk-il-jlk/n1/b1` | 0.502909 ± 0.00105128 (W 0.00168989) | 1.08931 ± 0.0141577 (W 0.0263132) | 0.719249 ± 0.00202897 (W 0.00166099) | 🔵 tcontract 2.17× faster than `ttgt` | 🔵 tcontract 1.43× faster than `tblis` |  |
| `ijk-ilk-jl/n1/b1` | 0.345825 ± 0.00202272 (W 0.00100895) | 1.06231 ± 0.00441041 (W 0.00172951) | 0.70508 ± 0.00233684 (W 0.00249572) | 🔵 tcontract 3.07× faster than `ttgt` | 🔵 tcontract 2.04× faster than `tblis` |  |
| `ijk-ilk-lj/n1/b1` | 0.343515 ± 0.00212279 (W 0.00107687) | 1.00618 ± 0.00561334 (W 0.00149534) | 0.742149 ± 0.00144375 (W 0.00206423) | 🔵 tcontract 2.93× faster than `ttgt` | 🔵 tcontract 2.16× faster than `tblis` |  |
| `ijk-ilmk-mjl/n1/b1` | 0.145124 ± 0.000301054 (W 0.00123394) | 0.437802 ± 0.00215486 (W 0.00163503) | 0.321196 ± 0.000867122 (W 0.00227284) | 🔵 tcontract 3.02× faster than `ttgt` | 🔵 tcontract 2.21× faster than `tblis` |  |
| `ijkl-imjn-lnkm/n1/b1` | 2.10241 ± 0.00458849 (W 0.00230835) | 4.24494 ± 0.0121855 (W 0.00574533) | 3.93262 ± 0.00381288 (W 0.00302976) | 🔵 tcontract 2.02× faster than `ttgt` | 🔵 tcontract 1.87× faster than `tblis` |  |
| `ijkl-imjn-nlmk/n1/b1` | 2.07252 ± 0.00551026 (W 0.002009) | 4.11025 ± 0.00542298 (W 0.00293385) | 4.02312 ± 0.0143621 (W 0.00205628) | 🔵 tcontract 1.98× faster than `ttgt` | 🔵 tcontract 1.94× faster than `tblis` |  |
| `ijkl-imkn-jnlm/n1/b1` | 2.0831 ± 0.00099286 (W 0.00225121) | 4.24704 ± 0.0135348 (W 0.00918059) | 3.92502 ± 0.0172031 (W 0.00295237) | 🔵 tcontract 2.04× faster than `ttgt` | 🔵 tcontract 1.88× faster than `tblis` |  |
| `ijkl-imkn-njml/n1/b1` | 2.06109 ± 0.00357991 (W 0.0020857) | 4.11285 ± 0.0212 (W 0.00201516) | 4.02202 ± 0.015 (W 0.00245651) | 🔵 tcontract 2.00× faster than `ttgt` | 🔵 tcontract 1.95× faster than `tblis` |  |
| `ijkl-imln-jnkm/n1/b1` | 2.08098 ± 0.00328164 (W 0.00146654) | 4.23429 ± 0.00629921 (W 0.006158) | 3.90465 ± 0.0184061 (W 0.00522343) | 🔵 tcontract 2.03× faster than `ttgt` | 🔵 tcontract 1.88× faster than `tblis` |  |
| `ijkl-imln-njmk/n1/b1` | 2.06048 ± 0.00166085 (W 0.0015631) | 4.13026 ± 0.0157954 (W 0.00185516) | 3.94898 ± 0.00578475 (W 0.00251307) | 🔵 tcontract 2.00× faster than `ttgt` | 🔵 tcontract 1.92× faster than `tblis` |  |
| `ijkl-imnj-nlkm/n1/b1` | 2.07497 ± 0.00349367 (W 0.00172038) | 4.10365 ± 0.0147898 (W 0.00271179) | 4.00786 ± 0.00972573 (W 0.00157149) | 🔵 tcontract 1.98× faster than `ttgt` | 🔵 tcontract 1.93× faster than `tblis` |  |
| `ijkl-imnk-njml/n1/b1` | 2.05906 ± 0.00171746 (W 0.00111206) | 4.12401 ± 0.019333 (W 0.00147884) | 4.01867 ± 0.00460982 (W 0.00242426) | 🔵 tcontract 2.00× faster than `ttgt` | 🔵 tcontract 1.95× faster than `tblis` |  |
| `ijkl-minj-nlmk/n1/b1` | 2.56502 ± 0.00257622 (W 0.00149178) | 5.019 ± 0.0172121 (W 0.00577568) | 4.89792 ± 0.0207519 (W 0.00266456) | 🔵 tcontract 1.96× faster than `ttgt` | 🔵 tcontract 1.91× faster than `tblis` |  |
| `ijkl-mink-jnlm/n1/b1` | 2.47485 ± 0.00175804 (W 0.00197032) | 5.12386 ± 0.00509103 (W 0.00415082) | 4.68552 ± 0.01082 (W 0.00223405) | 🔵 tcontract 2.07× faster than `ttgt` | 🔵 tcontract 1.89× faster than `tblis` |  |
| `ijkl-minl-njmk/n1/b1` | 2.5371 ± 0.00136347 (W 0.00116969) | 5.01534 ± 0.00904286 (W 0.00359395) | 4.81943 ± 0.0296858 (W 0.00219064) | 🔵 tcontract 1.98× faster than `ttgt` | 🔵 tcontract 1.90× faster than `tblis` |  |

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
