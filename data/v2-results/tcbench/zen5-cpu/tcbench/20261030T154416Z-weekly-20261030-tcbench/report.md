# `tcbench` on `zen5-cpu`

- tcontract-rs commit: `9f793ede6b8076fd7ce2251594a9552ad66aa339`
- features: `blas, tblis`
- tprims rows: `tprims` (the provider in the measured revision; see library above); `openblas` (the provider in the measured revision; see library above)
- external providers: `tblis` 2.0 @ `b16a732939d8454021e0a0f0097cf1cc1dd3ab19` tag `v2.0-beta2` sha256 `de00bf1552c15f9c4a5d3157f02c149b81aef0909107c51cbb54ba4b8e9b5827` (TBLIS 2.0, configuration zen3; bundled BLIS 358e689cadd6757f564a2992cf46a2f7d6fa6bb0; built with ./configure --prefix=/home/shinaoka/projects/tensor4all/tcontract-benchmark/target/tblis-v2.0-beta2 --with-blis-config-family=zen3 (cmake, Unix Makefiles, Release); libtblis.so sha256 de00bf1552c15f9c)
- harness commit: `65c8a5df9c0dfb86a199eb41f50803700e73f97e`
- toolkit commit: `b71624bef111ce941bddaedcce3fdb6eab40f9eb`
- measured binary SHA-256: `81a1fe3ea90fe4e232eb039ed5d4206a345fbb8eda3959e3df263054b0d61f96`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-30T15:55:07.435233Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/v2/record_run.py tcbench zen5-cpu tcbench --aa 3 --reps 5 --prime-ms 250 --external-provider-json /home/shinaoka/.local/state/tensor4all-weekly/20261031/tcontract/tblis-providers.json --label weekly-20261030-tcbench --no-publish`
- raw data: `data/v2-results/tcbench/zen5-cpu/tcbench/20261030T154416Z-weekly-20261030-tcbench/`

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
Spread guide (computed from this run's own rows): per-engine between-start range median 1.09%, worst 62.15% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 31 of 588 engine cells exceed 5% and carry `!`; median within-process relative SD 0.29%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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
| `abc-bk-akc/n1/b1` | 1.01589 ± 0.00299078 (W 0.000870148) | 1.96325 ± 0.0112932 (W 0.00501197) | 1.51036 ± 0.0079065 (W 0.00290784) | 🔵 tcontract 1.93× faster than `ttgt` | 🔵 tcontract 1.49× faster than `tblis` |  |
| `abcijk-eiab-jkec/n1/b1` | 4.52178 ± 0.0263152 (W 0.00872357) | 8.91299 ± 0.0651799 (W 0.0138024) | 5.46392 ± 0.111188 (W 0.023086) | 🔵 tcontract 1.97× faster than `ttgt` | 🔵 tcontract 1.21× faster than `tblis` |  |
| `abcijk-eiac-jkeb/n1/b1` | 4.30935 ± 0.0100748 (W 0.0124209) | 10.0457 ± 0.0338852 (W 0.0404634) | 6.76354 ± 0.191684 (W 0.0330664) | 🔵 tcontract 2.33× faster than `ttgt` | 🔵 tcontract 1.57× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-eibc-jkea/n1/b1` | 4.58219 ± 0.0341819 (W 0.0116578) | 11.5645 ± 0.131067 (W 0.0267711) | 5.43609 ± 0.0519014 (W 0.0119139) | 🔵 tcontract 2.52× faster than `ttgt` | 🔵 tcontract 1.19× faster than `tblis` |  |
| `abcijk-ejab-ikec/n1/b1` | 4.44913 ± 0.0153948 (W 0.00863633) | 8.81999 ± 0.00712909 (W 0.0133591) | 5.53182 ± 0.0927039 (W 0.0186448) | 🔵 tcontract 1.98× faster than `ttgt` | 🔵 tcontract 1.24× faster than `tblis` |  |
| `abcijk-ejac-ikeb/n1/b1` | 4.30588 ± 0.0157478 (W 0.00654083) | 10.0928 ± 0.0237216 (W 0.0414159) | 5.68648 ± 0.101199 (W 0.0157165) | 🔵 tcontract 2.34× faster than `ttgt` | 🔵 tcontract 1.32× faster than `tblis` |  |
| `abcijk-ejbc-ikea/n1/b1` | 4.58601 ± 0.0264532 (W 0.00635097) | 11.6871 ± 0.123922 (W 0.0988038) | 5.76387 ± 0.0541468 (W 0.0328645) | 🔵 tcontract 2.55× faster than `ttgt` | 🔵 tcontract 1.26× faster than `tblis` |  |
| `abcijk-ekab-ijec/n1/b1` | 4.44752 ± 0.00985037 (W 0.00902107) | 9.26163 ± 0.122745 (W 0.0167469) | 5.30905 ± 0.129786 (W 0.0167028) | 🔵 tcontract 2.08× faster than `ttgt` | 🔵 tcontract 1.19× faster than `tblis` |  |
| `abcijk-ekac-ijeb/n1/b1` | 4.30416 ± 0.00767526 (W 0.00605696) | 11.053 ± 0.016572 (W 0.0489681) | 5.97215 ± 0.0625271 (W 0.00829109) | 🔵 tcontract 2.57× faster than `ttgt` | 🔵 tcontract 1.39× faster than `tblis` |  |
| `abcijk-ekbc-ijea/n1/b1` | 4.56826 ± 0.0197307 (W 0.00926691) | 12.3423 ± 0.190741 (W 0.112434) | 5.73927 ± 0.0401076 (W 0.0133877) | 🔵 tcontract 2.70× faster than `ttgt` | 🔵 tcontract 1.26× faster than `tblis` |  |
| `abcijk-ijma-mkbc/n1/b1` | 4.57859 ± 0.00354206 (W 0.0105882) | 38.6016 ± 0.16387 (W 0.0460156) | 5.73109 ± 0.0443732 (W 0.0174199) | 🔵 tcontract 8.43× faster than `ttgt` | 🔵 tcontract 1.25× faster than `tblis` |  |
| `abcijk-ijmb-mkac/n1/b1` | 4.30054 ± 0.00762655 (W 0.00728757) | 36.0417 ± 0.134365 (W 0.0588951) | 5.95049 ± 0.0821902 (W 0.0134498) | 🔵 tcontract 8.38× faster than `ttgt` | 🔵 tcontract 1.38× faster than `tblis` |  |
| `abcijk-ijmc-mkab/n1/b1` | 4.42657 ± 0.0250262 (W 0.00353111) | 37.2437 ± 0.0657094 (W 0.146654) | 5.30842 ± 0.0640641 (W 0.0120312) | 🔵 tcontract 8.41× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `abcijk-ikma-mjbc/n1/b1` | 4.58125 ± 0.0183015 (W 0.00594113) | 43.7785 ± 0.286429 (W 0.0544916) | 5.77004 ± 0.0504893 (W 0.00788874) | 🔵 tcontract 9.56× faster than `ttgt` | 🔵 tcontract 1.26× faster than `tblis` |  |
| `abcijk-ikmb-mjac/n1/b1` | 4.31184 ± 0.00644176 (W 0.0141661) | 38.5741 ± 0.24115 (W 0.415226) | 5.72093 ± 0.0257128 (W 0.00858243) | 🔵 tcontract 8.95× faster than `ttgt` | 🔵 tcontract 1.33× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 4.43897 ± 0.00492155 (W 0.00409567) | 39.9626 ± 0.261807 (W 0.0417452) | 5.51593 ± 0.0912441 (W 0.0314308) | 🔵 tcontract 9.00× faster than `ttgt` | 🔵 tcontract 1.24× faster than `tblis` |  |
| `abcijk-jkma-mibc/n1/b1` | 4.5706 ± 0.0148504 (W 0.00685772) | 114.284 ± 25.7651 (W 0.13954) | 5.4074 ± 0.0538034 (W 0.010181) | 🔵 tcontract 25.00× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmb-miac/n1/b1` | 4.30781 ± 0.0225324 (W 0.00788033) | 100.331 ± 13.8122 (W 0.0568094) | 6.72057 ± 0.092322 (W 0.0236539) | 🔵 tcontract 23.29× faster than `ttgt` | 🔵 tcontract 1.56× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmc-miab/n1/b1` | 4.50272 ± 0.0118699 (W 0.0044253) | 96.7492 ± 12.1217 (W 0.414285) | 5.43304 ± 0.175711 (W 0.028583) | 🔵 tcontract 21.49× faster than `ttgt` | 🔵 tcontract 1.21× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcs-rc-abrs/n1/b1` | 0.483521 ± 0.00204432 (W 0.00268915) | 1.13645 ± 0.0137699 (W 0.00451414) | 1.15782 ± 0.00737994 (W 0.00925416) | 🔵 tcontract 2.35× faster than `ttgt` | 🔵 tcontract 2.39× faster than `tblis` |  |
| `abj-bka-kj/n1/b1` | 2.47121 ± 0.0319245 (W 0.0115189) | 2.73809 ± 0.0436063 (W 0.0198843) | 2.64428 ± 0.0261646 (W 0.00791116) | 🔵 tcontract 1.11× faster than `ttgt` | 🔵 tcontract 1.07× faster than `tblis` |  |
| `abjc-cbka-kj/n1/b1` | 1.54198 ± 0.0132659 (W 0.0129401) | 1.20514 ± 0.00497961 (W 0.0116568) | 1.40203 ± 0.00630281 (W 0.00426525) | 🔴 tcontract 1.28× slower than `ttgt` | 🔴 tcontract 1.10× slower than `tblis` |  |
| `abjc-kbac-jk/n1/b1` | 0.541196 ± 0.00350142 (W 0.00248442) | 1.20581 ± 0.0120396 (W 0.00745788) | 1.15228 ± 0.00535428 (W 0.00394215) | 🔵 tcontract 2.23× faster than `ttgt` | 🔵 tcontract 2.13× faster than `tblis` |  |
| `abjcd-dkbac-jk/n1/b1` | 4.27617 ± 0.0625647 (W 0.0289551) | 18.4244 ± 0.594895 (W 0.13474) | 8.20376 ± 0.0998817 (W 0.0377725) | 🔵 tcontract 4.31× faster than `ttgt` | 🔵 tcontract 1.92× faster than `tblis` | `!` between-start range over 5% |
| `abrs-qb-aqrs/n1/b1` | 0.478131 ± 0.00139743 (W 0.0020518) | 1.09022 ± 0.00458228 (W 0.00385509) | 1.14358 ± 0.00289694 (W 0.00565762) | 🔵 tcontract 2.28× faster than `ttgt` | 🔵 tcontract 2.39× faster than `tblis` |  |
| `adbjc-cbdka-kj/n1/b1` | 10.4133 ± 0.132882 (W 0.0346356) | 12.1108 ± 0.150146 (W 0.0245116) | 9.75629 ± 0.171291 (W 0.097954) | 🔵 tcontract 1.16× faster than `ttgt` | 🔴 tcontract 1.07× slower than `tblis` |  |
| `ajb-kba-jk/n1/b1` | 1.44306 ± 0.00914079 (W 0.00328989) | 2.36882 ± 0.00179 (W 0.00269644) | 2.13771 ± 0.0237347 (W 0.0278667) | 🔵 tcontract 1.64× faster than `ttgt` | 🔵 tcontract 1.48× faster than `tblis` |  |
| `ajbc-ckba-jk/n1/b1` | 0.735891 ± 0.00557791 (W 0.00194721) | 3.63182 ± 0.076267 (W 0.0132681) | 1.22115 ± 0.0114586 (W 0.00787255) | 🔵 tcontract 4.94× faster than `ttgt` | 🔵 tcontract 1.66× faster than `tblis` |  |
| `ajbdc-ckbad-jk/n1/b1` | 4.12937 ± 0.0108866 (W 0.0195989) | 23.9123 ± 0.408046 (W 0.0988412) | 7.85195 ± 0.0324719 (W 0.0344071) | 🔵 tcontract 5.79× faster than `ttgt` | 🔵 tcontract 1.90× faster than `tblis` |  |
| `aqrs-pa-pqrs/n1/b1` | 0.506902 ± 0.00168035 (W 0.00276308) | 1.02651 ± 0.00463755 (W 0.00845388) | 1.09989 ± 0.00725814 (W 0.00937625) | 🔵 tcontract 2.03× faster than `ttgt` | 🔵 tcontract 2.17× faster than `tblis` |  |
| `ij-ik-kj/n1/b1` | 3.55571 ± 0.0102642 (W 0.00764064) | 4.60969 ± 0.00762768 (W 0.00946899) | 4.28333 ± 0.0252472 (W 0.0126109) | 🔵 tcontract 1.30× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `ij-ikl-ljk/n1/b1` | 1.2282 ± 0.00234239 (W 0.00478819) | 1.84317 ± 0.00914209 (W 0.00600283) | 2.14092 ± 0.00447866 (W 0.00475046) | 🔵 tcontract 1.50× faster than `ttgt` | 🔵 tcontract 1.74× faster than `tblis` |  |
| `ij-kil-lkj/n1/b1` | 1.81311 ± 0.0121587 (W 0.00605508) | 2.8376 ± 0.00258596 (W 0.00872558) | 3.01518 ± 0.00453384 (W 0.00894682) | 🔵 tcontract 1.57× faster than `ttgt` | 🔵 tcontract 1.66× faster than `tblis` |  |
| `ijk-ikl-lj/n1/b1` | 1.0967 ± 0.00214414 (W 0.00419469) | 1.63845 ± 0.0016655 (W 0.00275006) | 1.73328 ± 0.0116481 (W 0.00361809) | 🔵 tcontract 1.49× faster than `ttgt` | 🔵 tcontract 1.58× faster than `tblis` |  |
| `ijk-il-jlk/n1/b1` | 1.06933 ± 0.00484059 (W 0.00304458) | 1.89088 ± 0.00356836 (W 0.00767237) | 1.59122 ± 0.0108049 (W 0.00790102) | 🔵 tcontract 1.77× faster than `ttgt` | 🔵 tcontract 1.49× faster than `tblis` |  |
| `ijk-ilk-jl/n1/b1` | 1.0168 ± 0.00125184 (W 0.00081533) | 1.73022 ± 0.0218408 (W 0.0284464) | 1.53115 ± 0.0179541 (W 0.00569754) | 🔵 tcontract 1.70× faster than `ttgt` | 🔵 tcontract 1.51× faster than `tblis` |  |
| `ijk-ilk-lj/n1/b1` | 1.09024 ± 0.000567715 (W 0.0031095) | 1.77323 ± 0.0270606 (W 0.0217081) | 1.72721 ± 0.00519529 (W 0.00269983) | 🔵 tcontract 1.63× faster than `ttgt` | 🔵 tcontract 1.58× faster than `tblis` |  |
| `ijk-ilmk-mjl/n1/b1` | 0.43113 ± 0.000556502 (W 0.00328862) | 0.683932 ± 0.00140927 (W 0.00216884) | 0.960551 ± 0.00694761 (W 0.00303359) | 🔵 tcontract 1.59× faster than `ttgt` | 🔵 tcontract 2.23× faster than `tblis` |  |
| `ijkl-imjn-lnkm/n1/b1` | 6.26206 ± 0.0144054 (W 0.0100743) | 7.98754 ± 0.0221329 (W 0.0121165) | 7.68734 ± 0.0899776 (W 0.0181443) | 🔵 tcontract 1.28× faster than `ttgt` | 🔵 tcontract 1.23× faster than `tblis` |  |
| `ijkl-imjn-nlmk/n1/b1` | 6.21278 ± 0.0201504 (W 0.0117524) | 8.0109 ± 0.0157514 (W 0.0133596) | 7.46036 ± 0.103618 (W 0.0094103) | 🔵 tcontract 1.29× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `ijkl-imkn-jnlm/n1/b1` | 6.18658 ± 0.0234097 (W 0.0100537) | 7.99297 ± 0.00310252 (W 0.0150979) | 7.3072 ± 0.079047 (W 0.0182201) | 🔵 tcontract 1.29× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `ijkl-imkn-njml/n1/b1` | 6.20618 ± 0.0245524 (W 0.0221342) | 8.0055 ± 0.0147871 (W 0.0117506) | 7.39208 ± 0.0902779 (W 0.011402) | 🔵 tcontract 1.29× faster than `ttgt` | 🔵 tcontract 1.19× faster than `tblis` |  |
| `ijkl-imln-jnkm/n1/b1` | 6.1739 ± 0.0270012 (W 0.0175602) | 7.98773 ± 0.0149174 (W 0.0196917) | 7.30593 ± 0.0327469 (W 0.019786) | 🔵 tcontract 1.29× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `ijkl-imln-njmk/n1/b1` | 6.19124 ± 0.0254126 (W 0.00831807) | 8.01201 ± 0.020254 (W 0.0116729) | 7.33264 ± 0.138104 (W 0.0144437) | 🔵 tcontract 1.29× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `ijkl-imnj-nlkm/n1/b1` | 6.20577 ± 0.0340636 (W 0.0111935) | 7.9433 ± 0.0180354 (W 0.0108604) | 7.38741 ± 0.020271 (W 0.0118625) | 🔵 tcontract 1.28× faster than `ttgt` | 🔵 tcontract 1.19× faster than `tblis` |  |
| `ijkl-imnk-njml/n1/b1` | 6.18441 ± 0.0201395 (W 0.00791105) | 7.98559 ± 0.0366468 (W 0.00908775) | 7.36701 ± 0.0462948 (W 0.0254672) | 🔵 tcontract 1.29× faster than `ttgt` | 🔵 tcontract 1.19× faster than `tblis` |  |
| `ijkl-minj-nlmk/n1/b1` | 7.61377 ± 0.0117555 (W 0.0125135) | 9.66651 ± 0.028469 (W 0.0225461) | 9.06584 ± 0.0916438 (W 0.0166759) | 🔵 tcontract 1.27× faster than `ttgt` | 🔵 tcontract 1.19× faster than `tblis` |  |
| `ijkl-mink-jnlm/n1/b1` | 7.482 ± 0.0206875 (W 0.0117352) | 9.54519 ± 0.0200464 (W 0.0101458) | 8.64993 ± 0.0680497 (W 0.0136495) | 🔵 tcontract 1.28× faster than `ttgt` | 🔵 tcontract 1.16× faster than `tblis` |  |
| `ijkl-minl-njmk/n1/b1` | 7.58446 ± 0.0386825 (W 0.0116993) | 9.67511 ± 0.0302477 (W 0.0117714) | 8.78694 ± 0.0333244 (W 0.0178663) | 🔵 tcontract 1.28× faster than `ttgt` | 🔵 tcontract 1.16× faster than `tblis` |  |

## tcbench, f64, 4T (CPU 4-7)

| case | plan (ms) | ttgt (ms) | tblis (ms) | vs `ttgt` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `abc-bk-akc/n1/b1` | 0.265027 ± 0.00175964 (W 0.00211853) | 1.25718 ± 0.018055 (W 0.0257461) | 0.4261 ± 0.00376131 (W 0.0035288) | 🔵 tcontract 4.74× faster than `ttgt` | 🔵 tcontract 1.61× faster than `tblis` |  |
| `abcijk-eiab-jkec/n1/b1` | 1.15864 ± 0.00643273 (W 0.00768489) | 5.68757 ± 0.0263339 (W 0.0214623) | 1.68922 ± 0.054056 (W 0.0329741) | 🔵 tcontract 4.91× faster than `ttgt` | 🔵 tcontract 1.46× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-eiac-jkeb/n1/b1` | 1.09173 ± 0.00385545 (W 0.00269078) | 6.91663 ± 0.0481938 (W 0.0391301) | 2.21646 ± 0.0845481 (W 0.0491898) | 🔵 tcontract 6.34× faster than `ttgt` | 🔵 tcontract 2.03× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-eibc-jkea/n1/b1` | 1.17393 ± 0.00664417 (W 0.00317466) | 8.36811 ± 0.166017 (W 0.0265068) | 1.45864 ± 0.00523788 (W 0.0108224) | 🔵 tcontract 7.13× faster than `ttgt` | 🔵 tcontract 1.24× faster than `tblis` |  |
| `abcijk-ejab-ikec/n1/b1` | 1.13719 ± 0.00386871 (W 0.00416152) | 5.71382 ± 0.0466715 (W 0.0102688) | 1.67109 ± 0.0388122 (W 0.0267686) | 🔵 tcontract 5.02× faster than `ttgt` | 🔵 tcontract 1.47× faster than `tblis` |  |
| `abcijk-ejac-ikeb/n1/b1` | 1.08977 ± 0.00688547 (W 0.00306801) | 7.03484 ± 0.0301367 (W 0.036145) | 1.54808 ± 0.00253273 (W 0.00964358) | 🔵 tcontract 6.46× faster than `ttgt` | 🔵 tcontract 1.42× faster than `tblis` |  |
| `abcijk-ejbc-ikea/n1/b1` | 1.17284 ± 0.0165414 (W 0.00652144) | 8.47359 ± 0.179648 (W 0.0638974) | 1.53943 ± 0.00991442 (W 0.00754237) | 🔵 tcontract 7.22× faster than `ttgt` | 🔵 tcontract 1.31× faster than `tblis` |  |
| `abcijk-ekab-ijec/n1/b1` | 1.13898 ± 0.00651217 (W 0.00464382) | 6.04766 ± 0.00935368 (W 0.0116799) | 1.47277 ± 0.035084 (W 0.04211) | 🔵 tcontract 5.31× faster than `ttgt` | 🔵 tcontract 1.29× faster than `tblis` |  |
| `abcijk-ekac-ijeb/n1/b1` | 1.08913 ± 0.00494274 (W 0.00177444) | 7.78989 ± 0.0507702 (W 0.0141141) | 2.05217 ± 0.00835539 (W 0.0268968) | 🔵 tcontract 7.15× faster than `ttgt` | 🔵 tcontract 1.88× faster than `tblis` |  |
| `abcijk-ekbc-ijea/n1/b1` | 1.16984 ± 0.00476102 (W 0.00346137) | 9.25969 ± 0.279455 (W 0.0431464) | 1.53423 ± 0.00601701 (W 0.0079399) | 🔵 tcontract 7.92× faster than `ttgt` | 🔵 tcontract 1.31× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ijma-mkbc/n1/b1` | 1.17386 ± 0.00772046 (W 0.00386397) | 35.2886 ± 0.20859 (W 0.0425508) | 1.53195 ± 0.0158176 (W 0.00992853) | 🔵 tcontract 30.06× faster than `ttgt` | 🔵 tcontract 1.31× faster than `tblis` |  |
| `abcijk-ijmb-mkac/n1/b1` | 1.08794 ± 0.0054175 (W 0.00277716) | 32.9127 ± 0.196104 (W 0.133179) | 2.07641 ± 0.011488 (W 0.0550031) | 🔵 tcontract 30.25× faster than `ttgt` | 🔵 tcontract 1.91× faster than `tblis` |  |
| `abcijk-ijmc-mkab/n1/b1` | 1.13566 ± 0.00821127 (W 0.00625456) | 33.8287 ± 0.121096 (W 0.0950037) | 1.48939 ± 0.0296814 (W 0.0368978) | 🔵 tcontract 29.79× faster than `ttgt` | 🔵 tcontract 1.31× faster than `tblis` |  |
| `abcijk-ikma-mjbc/n1/b1` | 1.1745 ± 0.00649937 (W 0.00367336) | 39.9979 ± 0.635994 (W 0.0607822) | 1.52279 ± 0.013517 (W 0.0108232) | 🔵 tcontract 34.06× faster than `ttgt` | 🔵 tcontract 1.30× faster than `tblis` |  |
| `abcijk-ikmb-mjac/n1/b1` | 1.08764 ± 0.00344073 (W 0.00343827) | 35.3004 ± 0.0739834 (W 0.0725722) | 1.53354 ± 0.00767593 (W 0.00837432) | 🔵 tcontract 32.46× faster than `ttgt` | 🔵 tcontract 1.41× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 1.13107 ± 0.0064234 (W 0.005538) | 36.5015 ± 0.0760462 (W 0.105742) | 1.66911 ± 0.0539547 (W 0.0308122) | 🔵 tcontract 32.27× faster than `ttgt` | 🔵 tcontract 1.48× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-jkma-mibc/n1/b1` | 1.17988 ± 0.00887129 (W 0.00448835) | 79.0741 ± 28.2852 (W 0.179353) | 1.44795 ± 0.018744 (W 0.010673) | 🔵 tcontract 67.02× faster than `ttgt` | 🔵 tcontract 1.23× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmb-miac/n1/b1` | 1.09289 ± 0.0037058 (W 0.00143496) | 78.6355 ± 12.5173 (W 0.0874993) | 2.24059 ± 0.07803 (W 0.0438443) | 🔵 tcontract 71.95× faster than `ttgt` | 🔵 tcontract 2.05× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmc-miab/n1/b1` | 1.15337 ± 0.00861531 (W 0.00571558) | 77.7194 ± 12.9636 (W 0.0733767) | 1.6789 ± 0.0431062 (W 0.0542166) | 🔵 tcontract 67.38× faster than `ttgt` | 🔵 tcontract 1.46× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcs-rc-abrs/n1/b1` | 0.135906 ± 0.000855742 (W 0.00196555) | 0.804058 ± 0.0134786 (W 0.00626148) | 0.375174 ± 0.00334295 (W 0.00816118) | 🔵 tcontract 5.92× faster than `ttgt` | 🔵 tcontract 2.76× faster than `tblis` |  |
| `abj-bka-kj/n1/b1` | 0.488526 ± 0.00184398 (W 0.00276857) | 1.41183 ± 0.0439356 (W 0.0118889) | 0.721061 ± 0.0107438 (W 0.00853456) | 🔵 tcontract 2.89× faster than `ttgt` | 🔵 tcontract 1.48× faster than `tblis` | `!` between-start range over 5% |
| `abjc-cbka-kj/n1/b1` | 0.285491 ± 0.042123 (W 0.00798332) | 0.793292 ± 0.0237442 (W 0.00372553) | 0.457278 ± 0.00297288 (W 0.00792711) | 🔵 tcontract 2.78× faster than `ttgt` | 🔵 tcontract 1.60× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abjc-kbac-jk/n1/b1` | 0.153127 ± 0.00161378 (W 0.00198355) | 0.84533 ± 0.0239845 (W 0.00522109) | 0.382509 ± 0.00386826 (W 0.00425561) | 🔵 tcontract 5.52× faster than `ttgt` | 🔵 tcontract 2.50× faster than `tblis` | `!` between-start range over 5% |
| `abjcd-dkbac-jk/n1/b1` | 1.47972 ± 0.0220329 (W 0.0133713) | 16.1175 ± 0.322249 (W 0.0479591) | 2.74371 ± 0.0258852 (W 0.0408285) | 🔵 tcontract 10.89× faster than `ttgt` | 🔵 tcontract 1.85× faster than `tblis` |  |
| `abrs-qb-aqrs/n1/b1` | 0.134372 ± 0.00139409 (W 0.00162434) | 0.740021 ± 0.0025221 (W 0.0034428) | 0.372749 ± 0.00242639 (W 0.00674215) | 🔵 tcontract 5.51× faster than `ttgt` | 🔵 tcontract 2.77× faster than `tblis` |  |
| `adbjc-cbdka-kj/n1/b1` | 6.10747 ± 0.145093 (W 0.164088) | 10.1202 ± 0.0484781 (W 0.0215742) | 3.66953 ± 0.114708 (W 0.0884111) | 🔵 tcontract 1.66× faster than `ttgt` | 🔴 tcontract 1.66× slower than `tblis` | `!` between-start range over 5% |
| `ajb-kba-jk/n1/b1` | 0.379225 ± 0.00368346 (W 0.0054473) | 1.25309 ± 0.00316051 (W 0.0047253) | 0.56501 ± 0.00516413 (W 0.00648915) | 🔵 tcontract 3.30× faster than `ttgt` | 🔵 tcontract 1.49× faster than `tblis` |  |
| `ajbc-ckba-jk/n1/b1` | 0.21842 ± 0.00256239 (W 0.0044389) | 3.19034 ± 0.0642922 (W 0.0208012) | 0.405997 ± 0.00164957 (W 0.00617943) | 🔵 tcontract 14.61× faster than `ttgt` | 🔵 tcontract 1.86× faster than `tblis` |  |
| `ajbdc-ckbad-jk/n1/b1` | 1.40864 ± 0.0267583 (W 0.00731902) | 22.3924 ± 0.384595 (W 0.111987) | 2.68971 ± 0.0508263 (W 0.0381646) | 🔵 tcontract 15.90× faster than `ttgt` | 🔵 tcontract 1.91× faster than `tblis` |  |
| `aqrs-pa-pqrs/n1/b1` | 0.280377 ± 0.000245622 (W 0.00200337) | 0.652514 ± 0.00162805 (W 0.00364615) | 0.351982 ± 0.00495099 (W 0.00501235) | 🔵 tcontract 2.33× faster than `ttgt` | 🔵 tcontract 1.26× faster than `tblis` |  |
| `ij-ik-kj/n1/b1` | 1.00979 ± 0.00361032 (W 0.00291477) | 1.51172 ± 0.00471054 (W 0.00447462) | 1.21436 ± 0.00593262 (W 0.00435622) | 🔵 tcontract 1.50× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `ij-ikl-ljk/n1/b1` | 0.517693 ± 0.00211983 (W 0.00403235) | 0.97251 ± 0.0251359 (W 0.00665167) | 0.879496 ± 0.00474013 (W 0.0043915) | 🔵 tcontract 1.88× faster than `ttgt` | 🔵 tcontract 1.70× faster than `tblis` | `!` between-start range over 5% |
| `ij-kil-lkj/n1/b1` | 0.754374 ± 0.00252672 (W 0.0037739) | 1.6038 ± 0.023756 (W 0.00849267) | 1.21393 ± 0.00532783 (W 0.00338766) | 🔵 tcontract 2.13× faster than `ttgt` | 🔵 tcontract 1.61× faster than `tblis` |  |
| `ijk-ikl-lj/n1/b1` | 0.28505 ± 0.00123798 (W 0.00165319) | 0.821786 ± 0.00408616 (W 0.00226332) | 0.476748 ± 0.0053637 (W 0.00466428) | 🔵 tcontract 2.88× faster than `ttgt` | 🔵 tcontract 1.67× faster than `tblis` |  |
| `ijk-il-jlk/n1/b1` | 0.274675 ± 0.000398433 (W 0.00154398) | 1.1702 ± 0.0101448 (W 0.0100812) | 0.438986 ± 0.0051926 (W 0.00426198) | 🔵 tcontract 4.26× faster than `ttgt` | 🔵 tcontract 1.60× faster than `tblis` |  |
| `ijk-ilk-jl/n1/b1` | 0.267441 ± 0.000974415 (W 0.00879567) | 0.880151 ± 0.0243995 (W 0.00267357) | 0.4246 ± 0.000956462 (W 0.00352231) | 🔵 tcontract 3.29× faster than `ttgt` | 🔵 tcontract 1.59× faster than `tblis` | `!` between-start range over 5% |
| `ijk-ilk-lj/n1/b1` | 0.284299 ± 0.00162582 (W 0.00266504) | 0.867076 ± 0.0106203 (W 0.00953884) | 0.471407 ± 0.00532162 (W 0.00393509) | 🔵 tcontract 3.05× faster than `ttgt` | 🔵 tcontract 1.66× faster than `tblis` |  |
| `ijk-ilmk-mjl/n1/b1` | 0.120827 ± 0.00125998 (W 0.00146499) | 0.407106 ± 0.00297158 (W 0.00180599) | 0.287411 ± 0.000648724 (W 0.00246017) | 🔵 tcontract 3.37× faster than `ttgt` | 🔵 tcontract 2.38× faster than `tblis` |  |
| `ijkl-imjn-lnkm/n1/b1` | 1.60237 ± 0.0126412 (W 0.00368831) | 2.66078 ± 0.0322438 (W 0.00766382) | 2.12431 ± 0.0719705 (W 0.0181261) | 🔵 tcontract 1.66× faster than `ttgt` | 🔵 tcontract 1.33× faster than `tblis` | `!` between-start range over 5% |
| `ijkl-imjn-nlmk/n1/b1` | 1.58219 ± 0.0109921 (W 0.00249231) | 2.69126 ± 0.0235576 (W 0.00934925) | 2.05477 ± 0.0164289 (W 0.00523118) | 🔵 tcontract 1.70× faster than `ttgt` | 🔵 tcontract 1.30× faster than `tblis` |  |
| `ijkl-imkn-jnlm/n1/b1` | 1.56492 ± 0.00949419 (W 0.00282408) | 2.66582 ± 0.0238501 (W 0.00514099) | 2.00219 ± 0.0330486 (W 0.00476011) | 🔵 tcontract 1.70× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` |  |
| `ijkl-imkn-njml/n1/b1` | 1.57628 ± 0.0199983 (W 0.00729316) | 2.68242 ± 0.0171507 (W 0.00561726) | 2.00141 ± 0.0103137 (W 0.00695663) | 🔵 tcontract 1.70× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `ijkl-imln-jnkm/n1/b1` | 1.56669 ± 0.0127604 (W 0.00380721) | 2.65193 ± 0.0176621 (W 0.00608799) | 2.00157 ± 0.037186 (W 0.00495317) | 🔵 tcontract 1.69× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` |  |
| `ijkl-imln-njmk/n1/b1` | 1.57528 ± 0.00778192 (W 0.0032565) | 2.67905 ± 0.0224866 (W 0.00796226) | 2.00697 ± 0.0204647 (W 0.00826652) | 🔵 tcontract 1.70× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `ijkl-imnj-nlkm/n1/b1` | 1.5789 ± 0.00596876 (W 0.00492688) | 2.63943 ± 0.00501136 (W 0.00698869) | 2.03163 ± 0.0210936 (W 0.00443309) | 🔵 tcontract 1.67× faster than `ttgt` | 🔵 tcontract 1.29× faster than `tblis` |  |
| `ijkl-imnk-njml/n1/b1` | 1.56437 ± 0.00432901 (W 0.00676256) | 2.66708 ± 0.0201088 (W 0.00619566) | 1.98874 ± 0.00911716 (W 0.00207596) | 🔵 tcontract 1.70× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `ijkl-minj-nlmk/n1/b1` | 1.94067 ± 0.0180318 (W 0.00183888) | 3.293 ± 0.0167838 (W 0.0107208) | 2.47011 ± 0.0341291 (W 0.00501466) | 🔵 tcontract 1.70× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `ijkl-mink-jnlm/n1/b1` | 1.89976 ± 0.00994789 (W 0.00244782) | 3.1809 ± 0.0219203 (W 0.00340531) | 2.37446 ± 0.0217574 (W 0.00887021) | 🔵 tcontract 1.67× faster than `ttgt` | 🔵 tcontract 1.25× faster than `tblis` |  |
| `ijkl-minl-njmk/n1/b1` | 1.92224 ± 0.016929 (W 0.00371239) | 3.30203 ± 0.0142027 (W 0.00833245) | 2.41506 ± 0.0242904 (W 0.00552519) | 🔵 tcontract 1.72× faster than `ttgt` | 🔵 tcontract 1.26× faster than `tblis` |  |

## tcbench, c64, 1T (CPU 4)

| case | plan (ms) | ttgt (ms) | tblis (ms) | vs `ttgt` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `abc-bk-akc/n1/b1` | 4.09813 ± 0.0338636 (W 0.0029219) | 6.35233 ± 0.0324205 (W 0.0162815) | 4.99486 ± 0.0516582 (W 0.0339036) | 🔵 tcontract 1.55× faster than `ttgt` | 🔵 tcontract 1.22× faster than `tblis` |  |
| `abcijk-eiab-jkec/n1/b1` | 17.6203 ± 0.0380274 (W 0.0143629) | 41.6202 ± 0.213628 (W 0.359616) | 19.1758 ± 0.227811 (W 0.0369057) | 🔵 tcontract 2.36× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `abcijk-eiac-jkeb/n1/b1` | 17.2765 ± 0.0725315 (W 0.0140676) | 42.5906 ± 0.199429 (W 0.0786805) | 21.0476 ± 0.252052 (W 0.0511607) | 🔵 tcontract 2.47× faster than `ttgt` | 🔵 tcontract 1.22× faster than `tblis` |  |
| `abcijk-eibc-jkea/n1/b1` | 17.6533 ± 0.0328138 (W 0.03764) | 45.8978 ± 0.265056 (W 0.124337) | 19.1557 ± 0.0754487 (W 0.0420176) | 🔵 tcontract 2.60× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `abcijk-ejab-ikec/n1/b1` | 17.565 ± 0.0339929 (W 0.028458) | 41.9648 ± 0.341345 (W 0.0926524) | 19.3398 ± 0.144445 (W 0.106699) | 🔵 tcontract 2.39× faster than `ttgt` | 🔵 tcontract 1.10× faster than `tblis` |  |
| `abcijk-ejac-ikeb/n1/b1` | 17.3351 ± 0.0608234 (W 0.0305507) | 43.1612 ± 0.156142 (W 0.140592) | 19.7824 ± 0.257842 (W 0.0724267) | 🔵 tcontract 2.49× faster than `ttgt` | 🔵 tcontract 1.14× faster than `tblis` |  |
| `abcijk-ejbc-ikea/n1/b1` | 17.7106 ± 0.0411173 (W 0.0294763) | 46.343 ± 0.174852 (W 0.0991733) | 20.1589 ± 0.101264 (W 0.0478409) | 🔵 tcontract 2.62× faster than `ttgt` | 🔵 tcontract 1.14× faster than `tblis` |  |
| `abcijk-ekab-ijec/n1/b1` | 17.582 ± 0.0532136 (W 0.0266244) | 41.736 ± 0.248773 (W 0.0997611) | 18.8913 ± 0.145641 (W 0.0691276) | 🔵 tcontract 2.37× faster than `ttgt` | 🔵 tcontract 1.07× faster than `tblis` |  |
| `abcijk-ekac-ijeb/n1/b1` | 17.3132 ± 0.0321119 (W 0.0264376) | 43.2439 ± 0.544202 (W 0.116467) | 20.1223 ± 0.0799491 (W 0.0448955) | 🔵 tcontract 2.50× faster than `ttgt` | 🔵 tcontract 1.16× faster than `tblis` |  |
| `abcijk-ekbc-ijea/n1/b1` | 17.7304 ± 0.0626293 (W 0.027201) | 47.3346 ± 0.850884 (W 0.111595) | 20.1901 ± 0.072765 (W 0.0290966) | 🔵 tcontract 2.67× faster than `ttgt` | 🔵 tcontract 1.14× faster than `tblis` |  |
| `abcijk-ijma-mkbc/n1/b1` | 17.7052 ± 0.0207953 (W 0.0340224) | 66.8721 ± 0.314471 (W 0.150753) | 20.1375 ± 0.051759 (W 0.0618603) | 🔵 tcontract 3.78× faster than `ttgt` | 🔵 tcontract 1.14× faster than `tblis` |  |
| `abcijk-ijmb-mkac/n1/b1` | 17.3209 ± 0.0556785 (W 0.0303648) | 67.6387 ± 0.131663 (W 0.0714354) | 20.1232 ± 0.191109 (W 0.0434912) | 🔵 tcontract 3.91× faster than `ttgt` | 🔵 tcontract 1.16× faster than `tblis` |  |
| `abcijk-ijmc-mkab/n1/b1` | 17.5737 ± 0.0299759 (W 0.0187719) | 79.6305 ± 0.185154 (W 0.375607) | 18.8932 ± 0.0901325 (W 0.0812493) | 🔵 tcontract 4.53× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `abcijk-ikma-mjbc/n1/b1` | 17.6941 ± 0.0374032 (W 0.0194737) | 70.6937 ± 0.147643 (W 0.124653) | 20.1129 ± 0.0414589 (W 0.0409052) | 🔵 tcontract 4.00× faster than `ttgt` | 🔵 tcontract 1.14× faster than `tblis` |  |
| `abcijk-ikmb-mjac/n1/b1` | 17.3419 ± 0.0893635 (W 0.0233281) | 69.5886 ± 0.297557 (W 0.0635628) | 19.7857 ± 0.216667 (W 0.0364448) | 🔵 tcontract 4.01× faster than `ttgt` | 🔵 tcontract 1.14× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 17.5659 ± 0.0277446 (W 0.064169) | 80.1402 ± 0.601792 (W 0.363133) | 19.235 ± 0.147011 (W 0.090048) | 🔵 tcontract 4.56× faster than `ttgt` | 🔵 tcontract 1.10× faster than `tblis` |  |
| `abcijk-jkma-mibc/n1/b1` | 17.6512 ± 0.0462527 (W 0.0209475) | 108.477 ± 0.763262 (W 0.138846) | 19.1217 ± 0.0659931 (W 0.0392507) | 🔵 tcontract 6.15× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `abcijk-jkmb-miac/n1/b1` | 17.3099 ± 0.0816847 (W 0.0211341) | 109.566 ± 2.25813 (W 0.194586) | 20.9114 ± 0.23666 (W 0.0852137) | 🔵 tcontract 6.33× faster than `ttgt` | 🔵 tcontract 1.21× faster than `tblis` |  |
| `abcijk-jkmc-miab/n1/b1` | 17.6137 ± 0.0292406 (W 0.01489) | 113.399 ± 1.34777 (W 0.111439) | 19.2754 ± 0.216052 (W 0.0976601) | 🔵 tcontract 6.44× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `abcs-rc-abrs/n1/b1` | 1.86006 ± 0.0128565 (W 0.00475417) | 3.00828 ± 0.0473936 (W 0.00938518) | 2.39494 ± 0.0223758 (W 0.00734796) | 🔵 tcontract 1.62× faster than `ttgt` | 🔵 tcontract 1.29× faster than `tblis` |  |
| `abj-bka-kj/n1/b1` | 7.51646 ± 0.0280854 (W 0.0192376) | 8.33934 ± 0.036503 (W 0.0194543) | 8.32793 ± 0.0807521 (W 0.0419689) | 🔵 tcontract 1.11× faster than `ttgt` | 🔵 tcontract 1.11× faster than `tblis` |  |
| `abjc-cbka-kj/n1/b1` | 3.51927 ± 0.0339672 (W 0.00942484) | 3.67422 ± 0.0181445 (W 0.0265431) | 3.08067 ± 0.00765106 (W 0.0819518) | · | 🔴 tcontract 1.14× slower than `tblis` |  |
| `abjc-kbac-jk/n1/b1` | 1.97102 ± 0.0103908 (W 0.00316117) | 3.68061 ± 0.0432905 (W 0.0153874) | 2.64868 ± 0.0323697 (W 0.0117567) | 🔵 tcontract 1.87× faster than `ttgt` | 🔵 tcontract 1.34× faster than `tblis` |  |
| `abjcd-dkbac-jk/n1/b1` | 12.8543 ± 0.0902159 (W 0.0970067) | 29.3154 ± 1.10198 (W 0.0261224) | 17.4574 ± 0.260988 (W 0.0530174) | 🔵 tcontract 2.28× faster than `ttgt` | 🔵 tcontract 1.36× faster than `tblis` | `!` between-start range over 5% |
| `abrs-qb-aqrs/n1/b1` | 1.60438 ± 0.00513369 (W 0.00389502) | 3.00504 ± 0.0549803 (W 0.016368) | 2.53516 ± 0.0205475 (W 0.017856) | 🔵 tcontract 1.87× faster than `ttgt` | 🔵 tcontract 1.58× faster than `tblis` |  |
| `adbjc-cbdka-kj/n1/b1` | 20.1002 ± 0.0770026 (W 0.082504) | 22.8244 ± 0.0223302 (W 0.0326222) | 19.493 ± 0.239081 (W 0.0919018) | 🔵 tcontract 1.14× faster than `ttgt` | · |  |
| `ajb-kba-jk/n1/b1` | 5.67805 ± 0.0863644 (W 0.0108116) | 7.99991 ± 0.0238988 (W 0.0135133) | 7.28943 ± 0.0323404 (W 0.0549013) | 🔵 tcontract 1.41× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` |  |
| `ajbc-ckba-jk/n1/b1` | 2.25641 ± 0.0641428 (W 0.00504638) | 5.7046 ± 0.0483444 (W 0.0145173) | 2.99273 ± 0.0457512 (W 0.0857729) | 🔵 tcontract 2.53× faster than `ttgt` | 🔵 tcontract 1.33× faster than `tblis` | `!` between-start range over 5% |
| `ajbdc-ckbad-jk/n1/b1` | 12.5576 ± 0.0715327 (W 0.0896963) | 34.5907 ± 0.255046 (W 0.0533011) | 17.5484 ± 0.147268 (W 0.187703) | 🔵 tcontract 2.75× faster than `ttgt` | 🔵 tcontract 1.40× faster than `tblis` |  |
| `aqrs-pa-pqrs/n1/b1` | 2.05839 ± 0.00321035 (W 0.004169) | 2.59273 ± 0.0158541 (W 0.0107395) | 2.36904 ± 0.0229083 (W 0.00672394) | 🔵 tcontract 1.26× faster than `ttgt` | 🔵 tcontract 1.15× faster than `tblis` |  |
| `ij-ik-kj/n1/b1` | 14.5639 ± 0.01141 (W 0.0184547) | 17.7467 ± 0.0278157 (W 0.0315218) | 15.5604 ± 0.0532563 (W 0.0238034) | 🔵 tcontract 1.22× faster than `ttgt` | 🔵 tcontract 1.07× faster than `tblis` |  |
| `ij-ikl-ljk/n1/b1` | 4.87593 ± 0.0373901 (W 0.0105872) | 5.80074 ± 0.0102693 (W 0.0103946) | 5.74792 ± 0.0557054 (W 0.0113134) | 🔵 tcontract 1.19× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `ij-kil-lkj/n1/b1` | 7.44316 ± 0.0122113 (W 0.021992) | 8.69121 ± 0.0128917 (W 0.0146115) | 8.38503 ± 0.0195175 (W 0.0283819) | 🔵 tcontract 1.17× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `ijk-ikl-lj/n1/b1` | 4.20182 ± 0.0302896 (W 0.0109486) | 5.50739 ± 0.161884 (W 0.0181677) | 5.76983 ± 0.056655 (W 0.0489098) | 🔵 tcontract 1.31× faster than `ttgt` | 🔵 tcontract 1.37× faster than `tblis` | `!` between-start range over 5% |
| `ijk-il-jlk/n1/b1` | 4.58732 ± 0.0180682 (W 0.0115028) | 6.3578 ± 0.0196834 (W 0.0263677) | 4.81282 ± 0.0268288 (W 0.00483958) | 🔵 tcontract 1.39× faster than `ttgt` | · |  |
| `ijk-ilk-jl/n1/b1` | 4.09782 ± 0.0138482 (W 0.0161069) | 6.02044 ± 0.025789 (W 0.0100209) | 4.99979 ± 0.0352635 (W 0.00986162) | 🔵 tcontract 1.47× faster than `ttgt` | 🔵 tcontract 1.22× faster than `tblis` |  |
| `ijk-ilk-lj/n1/b1` | 4.21219 ± 0.00531985 (W 0.00751683) | 6.02094 ± 0.0110062 (W 0.0195178) | 5.57997 ± 0.0303838 (W 0.0285719) | 🔵 tcontract 1.43× faster than `ttgt` | 🔵 tcontract 1.32× faster than `tblis` |  |
| `ijk-ilmk-mjl/n1/b1` | 1.64097 ± 0.00109533 (W 0.0035838) | 2.02962 ± 0.0268535 (W 0.0162168) | 2.09057 ± 0.0226998 (W 0.00839353) | 🔵 tcontract 1.24× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `ijkl-imjn-lnkm/n1/b1` | 25.0618 ± 0.065943 (W 0.0385217) | 30.8715 ± 0.0316115 (W 0.052523) | 27.0402 ± 0.192759 (W 0.0401915) | 🔵 tcontract 1.23× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `ijkl-imjn-nlmk/n1/b1` | 25.0763 ± 0.0237049 (W 0.0287261) | 30.7755 ± 0.0258772 (W 0.0366164) | 27.9033 ± 0.189868 (W 0.0722206) | 🔵 tcontract 1.23× faster than `ttgt` | 🔵 tcontract 1.11× faster than `tblis` |  |
| `ijkl-imkn-jnlm/n1/b1` | 24.9903 ± 0.0710864 (W 0.0252483) | 30.8473 ± 0.0344047 (W 0.0708619) | 27.1503 ± 0.0575945 (W 0.0579462) | 🔵 tcontract 1.23× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `ijkl-imkn-njml/n1/b1` | 25.1031 ± 0.0727676 (W 0.028597) | 30.7712 ± 0.0192261 (W 0.0514306) | 27.7519 ± 0.020854 (W 0.0493092) | 🔵 tcontract 1.23× faster than `ttgt` | 🔵 tcontract 1.11× faster than `tblis` |  |
| `ijkl-imln-jnkm/n1/b1` | 25.0449 ± 0.0794608 (W 0.0367193) | 30.8006 ± 0.0384029 (W 0.031041) | 27.0156 ± 0.121288 (W 0.0497877) | 🔵 tcontract 1.23× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `ijkl-imln-njmk/n1/b1` | 25.0389 ± 0.0824578 (W 0.0256107) | 30.8009 ± 0.0777002 (W 0.0202462) | 27.4482 ± 0.0838354 (W 0.0515296) | 🔵 tcontract 1.23× faster than `ttgt` | 🔵 tcontract 1.10× faster than `tblis` |  |
| `ijkl-imnj-nlkm/n1/b1` | 25.017 ± 0.0688046 (W 0.0306668) | 30.486 ± 0.066605 (W 0.0374824) | 27.4214 ± 0.146266 (W 0.0514039) | 🔵 tcontract 1.22× faster than `ttgt` | 🔵 tcontract 1.10× faster than `tblis` |  |
| `ijkl-imnk-njml/n1/b1` | 25.0476 ± 0.0614016 (W 0.0193231) | 30.636 ± 0.135358 (W 0.0414057) | 27.3364 ± 0.0967146 (W 0.0531486) | 🔵 tcontract 1.22× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `ijkl-minj-nlmk/n1/b1` | 30.7165 ± 0.16349 (W 0.0430718) | 36.815 ± 0.0943895 (W 0.0508188) | 33.7336 ± 0.186405 (W 0.0528848) | 🔵 tcontract 1.20× faster than `ttgt` | 🔵 tcontract 1.10× faster than `tblis` |  |
| `ijkl-mink-jnlm/n1/b1` | 30.1624 ± 0.0829292 (W 0.0147623) | 36.7793 ± 0.145811 (W 0.00886825) | 32.5129 ± 0.106737 (W 0.0839345) | 🔵 tcontract 1.22× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `ijkl-minl-njmk/n1/b1` | 30.7229 ± 0.0482653 (W 0.107518) | 36.7887 ± 0.0655805 (W 0.0458367) | 33.1167 ± 0.196079 (W 0.0181579) | 🔵 tcontract 1.20× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |

## tcbench, c64, 4T (CPU 4-7)

| case | plan (ms) | ttgt (ms) | tblis (ms) | vs `ttgt` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `abc-bk-akc/n1/b1` | 1.03594 ± 0.00559123 (W 0.00118016) | 2.73933 ± 0.036706 (W 0.0355357) | 1.26188 ± 0.0307188 (W 0.00934054) | 🔵 tcontract 2.64× faster than `ttgt` | 🔵 tcontract 1.22× faster than `tblis` |  |
| `abcijk-eiab-jkec/n1/b1` | 4.47448 ± 0.0113099 (W 0.010279) | 27.4148 ± 0.171329 (W 0.0718468) | 5.06625 ± 0.0284258 (W 0.030084) | 🔵 tcontract 6.13× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-eiac-jkeb/n1/b1` | 4.3408 ± 0.00859508 (W 0.00871206) | 28.05 ± 0.0510561 (W 0.110171) | 5.48921 ± 0.0294644 (W 0.0271233) | 🔵 tcontract 6.46× faster than `ttgt` | 🔵 tcontract 1.26× faster than `tblis` |  |
| `abcijk-eibc-jkea/n1/b1` | 4.4583 ± 0.0214931 (W 0.00599545) | 31.1352 ± 0.0558231 (W 0.0997002) | 4.9589 ± 0.0169407 (W 0.00528226) | 🔵 tcontract 6.98× faster than `ttgt` | 🔵 tcontract 1.11× faster than `tblis` |  |
| `abcijk-ejab-ikec/n1/b1` | 4.42933 ± 0.0129269 (W 0.00683772) | 27.55 ± 0.0511268 (W 0.108345) | 5.13422 ± 0.0419844 (W 0.0295714) | 🔵 tcontract 6.22× faster than `ttgt` | 🔵 tcontract 1.16× faster than `tblis` |  |
| `abcijk-ejac-ikeb/n1/b1` | 4.35495 ± 0.0178233 (W 0.00615798) | 28.4453 ± 0.178081 (W 0.0575883) | 5.15018 ± 0.0119258 (W 0.0082447) | 🔵 tcontract 6.53× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `abcijk-ejbc-ikea/n1/b1` | 4.46043 ± 0.0187545 (W 0.00464651) | 31.4552 ± 0.0387515 (W 0.0704114) | 5.21913 ± 0.0297685 (W 0.013577) | 🔵 tcontract 7.05× faster than `ttgt` | 🔵 tcontract 1.17× faster than `tblis` |  |
| `abcijk-ekab-ijec/n1/b1` | 4.42885 ± 0.0129623 (W 0.00689613) | 27.7203 ± 0.168118 (W 0.0553575) | 4.91935 ± 0.0116827 (W 0.0206534) | 🔵 tcontract 6.26× faster than `ttgt` | 🔵 tcontract 1.11× faster than `tblis` |  |
| `abcijk-ekac-ijeb/n1/b1` | 4.35166 ± 0.0118205 (W 0.00544606) | 29.1641 ± 0.201073 (W 0.038084) | 5.24696 ± 0.00947331 (W 0.0123178) | 🔵 tcontract 6.70× faster than `ttgt` | 🔵 tcontract 1.21× faster than `tblis` |  |
| `abcijk-ekbc-ijea/n1/b1` | 4.4471 ± 0.0137215 (W 0.009469) | 32.9168 ± 0.288523 (W 0.0773181) | 5.20222 ± 0.0199455 (W 0.0123575) | 🔵 tcontract 7.40× faster than `ttgt` | 🔵 tcontract 1.17× faster than `tblis` |  |
| `abcijk-ijma-mkbc/n1/b1` | 4.44974 ± 0.0244325 (W 0.00918243) | 52.954 ± 0.406632 (W 0.119329) | 5.18548 ± 0.0244391 (W 0.0150191) | 🔵 tcontract 11.90× faster than `ttgt` | 🔵 tcontract 1.17× faster than `tblis` |  |
| `abcijk-ijmb-mkac/n1/b1` | 4.35529 ± 0.00949892 (W 0.00454585) | 53.9932 ± 0.057904 (W 0.0867147) | 5.22985 ± 0.00960015 (W 0.0128835) | 🔵 tcontract 12.40× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `abcijk-ijmc-mkab/n1/b1` | 4.44294 ± 0.0308554 (W 0.00989077) | 64.795 ± 0.198594 (W 0.165387) | 4.88221 ± 0.0221447 (W 0.0105233) | 🔵 tcontract 14.58× faster than `ttgt` | 🔵 tcontract 1.10× faster than `tblis` |  |
| `abcijk-ikma-mjbc/n1/b1` | 4.45198 ± 0.0305335 (W 0.00862892) | 56.8573 ± 1.35184 (W 0.146979) | 5.19172 ± 0.0257177 (W 0.0181476) | 🔵 tcontract 12.77× faster than `ttgt` | 🔵 tcontract 1.17× faster than `tblis` |  |
| `abcijk-ikmb-mjac/n1/b1` | 4.34689 ± 0.0102005 (W 0.00814986) | 56.3817 ± 0.933592 (W 0.176445) | 5.13945 ± 0.00894294 (W 0.0176408) | 🔵 tcontract 12.97× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 4.4326 ± 0.0156708 (W 0.0105728) | 65.7594 ± 0.522647 (W 0.0784907) | 5.13904 ± 0.008571 (W 0.0604227) | 🔵 tcontract 14.84× faster than `ttgt` | 🔵 tcontract 1.16× faster than `tblis` |  |
| `abcijk-jkma-mibc/n1/b1` | 4.45994 ± 0.0143709 (W 0.00913105) | 94.601 ± 1.14449 (W 0.118917) | 4.94919 ± 0.00339385 (W 0.00991877) | 🔵 tcontract 21.21× faster than `ttgt` | 🔵 tcontract 1.11× faster than `tblis` |  |
| `abcijk-jkmb-miac/n1/b1` | 4.36558 ± 0.00888082 (W 0.0120886) | 93.1547 ± 1.04932 (W 0.215001) | 5.4722 ± 0.0220782 (W 0.0344126) | 🔵 tcontract 21.34× faster than `ttgt` | 🔵 tcontract 1.25× faster than `tblis` |  |
| `abcijk-jkmc-miab/n1/b1` | 4.4889 ± 0.0323182 (W 0.00898156) | 99.1968 ± 0.493667 (W 0.0763891) | 5.0268 ± 0.0338294 (W 0.0367136) | 🔵 tcontract 22.10× faster than `ttgt` | 🔵 tcontract 1.12× faster than `tblis` |  |
| `abcs-rc-abrs/n1/b1` | 0.471065 ± 0.00584973 (W 0.00238743) | 1.62927 ± 0.00916684 (W 0.00819947) | 0.711565 ± 0.00952089 (W 0.00902336) | 🔵 tcontract 3.46× faster than `ttgt` | 🔵 tcontract 1.51× faster than `tblis` |  |
| `abj-bka-kj/n1/b1` | 1.62255 ± 0.0202098 (W 0.00361271) | 3.68253 ± 0.0625062 (W 0.0151965) | 2.29036 ± 0.0152806 (W 0.0088426) | 🔵 tcontract 2.27× faster than `ttgt` | 🔵 tcontract 1.41× faster than `tblis` |  |
| `abjc-cbka-kj/n1/b1` | 0.810314 ± 0.0201524 (W 0.00770045) | 2.08793 ± 0.02267 (W 0.0119192) | 0.898485 ± 0.0470306 (W 0.0408825) | 🔵 tcontract 2.58× faster than `ttgt` | 🔵 tcontract 1.11× faster than `tblis` | `!` between-start range over 5% |
| `abjc-kbac-jk/n1/b1` | 0.510941 ± 0.00404914 (W 0.00241456) | 2.21028 ± 0.0574358 (W 0.0213495) | 0.772308 ± 0.00652292 (W 0.0148803) | 🔵 tcontract 4.33× faster than `ttgt` | 🔵 tcontract 1.51× faster than `tblis` | `!` between-start range over 5% |
| `abjcd-dkbac-jk/n1/b1` | 3.81874 ± 0.0136568 (W 0.0277675) | 22.0985 ± 0.520125 (W 0.0538733) | 5.21364 ± 0.0194198 (W 0.0323823) | 🔵 tcontract 5.79× faster than `ttgt` | 🔵 tcontract 1.37× faster than `tblis` |  |
| `abrs-qb-aqrs/n1/b1` | 0.414199 ± 0.00190835 (W 0.00268055) | 1.55018 ± 0.050824 (W 0.0282965) | 0.716514 ± 0.0106331 (W 0.00917899) | 🔵 tcontract 3.74× faster than `ttgt` | 🔵 tcontract 1.73× faster than `tblis` | `!` between-start range over 5% |
| `adbjc-cbdka-kj/n1/b1` | 7.9637 ± 0.0684684 (W 0.137277) | 15.8576 ± 0.0084713 (W 0.0238317) | 7.2961 ± 0.0376946 (W 0.106999) | 🔵 tcontract 1.99× faster than `ttgt` | 🔴 tcontract 1.09× slower than `tblis` |  |
| `ajb-kba-jk/n1/b1` | 1.44701 ± 0.0120056 (W 0.00425718) | 3.57352 ± 0.0328402 (W 0.0111254) | 1.86581 ± 0.0607696 (W 0.0109388) | 🔵 tcontract 2.47× faster than `ttgt` | 🔵 tcontract 1.29× faster than `tblis` | `!` between-start range over 5% |
| `ajbc-ckba-jk/n1/b1` | 0.597999 ± 0.0137445 (W 0.00715117) | 4.21239 ± 0.0486587 (W 0.0136471) | 0.907583 ± 0.0209789 (W 0.0146787) | 🔵 tcontract 7.04× faster than `ttgt` | 🔵 tcontract 1.52× faster than `tblis` |  |
| `ajbdc-ckbad-jk/n1/b1` | 3.65487 ± 0.0160083 (W 0.0335625) | 27.2851 ± 0.722208 (W 0.153214) | 5.13975 ± 0.03613 (W 0.0554848) | 🔵 tcontract 7.47× faster than `ttgt` | 🔵 tcontract 1.41× faster than `tblis` |  |
| `aqrs-pa-pqrs/n1/b1` | 0.618049 ± 0.0109476 (W 0.00370692) | 1.22673 ± 0.00317909 (W 0.00564689) | 0.661324 ± 0.00296426 (W 0.00513475) | 🔵 tcontract 1.98× faster than `ttgt` | 🔵 tcontract 1.07× faster than `tblis` |  |
| `ij-ik-kj/n1/b1` | 3.70398 ± 0.00391652 (W 0.00462742) | 5.03692 ± 0.00298986 (W 0.00966565) | 4.06062 ± 0.0111201 (W 0.00510506) | 🔵 tcontract 1.36× faster than `ttgt` | 🔵 tcontract 1.10× faster than `tblis` |  |
| `ij-ikl-ljk/n1/b1` | 2.081 ± 0.0119014 (W 0.0134854) | 2.25263 ± 0.0454924 (W 0.0231853) | 1.69659 ± 0.00847731 (W 0.00421894) | 🔵 tcontract 1.08× faster than `ttgt` | 🔴 tcontract 1.23× slower than `tblis` |  |
| `ij-kil-lkj/n1/b1` | 3.11047 ± 0.0153392 (W 0.0203452) | 3.67527 ± 0.0149498 (W 0.0136169) | 2.39317 ± 0.0210329 (W 0.0259935) | 🔵 tcontract 1.18× faster than `ttgt` | 🔴 tcontract 1.30× slower than `tblis` |  |
| `ijk-ikl-lj/n1/b1` | 1.07122 ± 0.0035253 (W 0.00158402) | 2.16897 ± 0.00335719 (W 0.00969935) | 1.41766 ± 0.0606511 (W 0.00545272) | 🔵 tcontract 2.02× faster than `ttgt` | 🔵 tcontract 1.32× faster than `tblis` | `!` between-start range over 5% |
| `ijk-il-jlk/n1/b1` | 1.85405 ± 0.0114584 (W 0.0123516) | 2.73548 ± 0.0280403 (W 0.0362951) | 1.2258 ± 0.00423835 (W 0.00419072) | 🔵 tcontract 1.48× faster than `ttgt` | 🔴 tcontract 1.51× slower than `tblis` |  |
| `ijk-ilk-jl/n1/b1` | 1.03575 ± 0.00570955 (W 0.00167262) | 2.71438 ± 0.0255316 (W 0.0142534) | 1.26585 ± 0.0111904 (W 0.00582819) | 🔵 tcontract 2.62× faster than `ttgt` | 🔵 tcontract 1.22× faster than `tblis` |  |
| `ijk-ilk-lj/n1/b1` | 1.06416 ± 0.00314134 (W 0.00359286) | 2.66098 ± 0.0161419 (W 0.00701873) | 1.43578 ± 0.0278065 (W 0.00742324) | 🔵 tcontract 2.50× faster than `ttgt` | 🔵 tcontract 1.35× faster than `tblis` |  |
| `ijk-ilmk-mjl/n1/b1` | 0.460314 ± 0.00281511 (W 0.00250341) | 0.853031 ± 0.00278915 (W 0.0029502) | 0.54824 ± 0.00251758 (W 0.00336532) | 🔵 tcontract 1.85× faster than `ttgt` | 🔵 tcontract 1.19× faster than `tblis` |  |
| `ijkl-imjn-lnkm/n1/b1` | 6.81511 ± 0.032468 (W 0.0121417) | 8.9773 ± 0.0228885 (W 0.0407116) | 7.13618 ± 0.0846412 (W 0.0133058) | 🔵 tcontract 1.32× faster than `ttgt` | · |  |
| `ijkl-imjn-nlmk/n1/b1` | 6.8023 ± 0.0373076 (W 0.0128149) | 8.9906 ± 0.101966 (W 0.0280672) | 7.21328 ± 0.104905 (W 0.0145754) | 🔵 tcontract 1.32× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` |  |
| `ijkl-imkn-jnlm/n1/b1` | 6.75309 ± 0.0429487 (W 0.0150294) | 8.99695 ± 0.0423481 (W 0.0219932) | 7.16662 ± 0.0941363 (W 0.0187994) | 🔵 tcontract 1.33× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` |  |
| `ijkl-imkn-njml/n1/b1` | 6.7611 ± 0.0331449 (W 0.0114375) | 8.98892 ± 0.0464226 (W 0.0250957) | 7.19785 ± 0.0582029 (W 0.0194414) | 🔵 tcontract 1.33× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` |  |
| `ijkl-imln-jnkm/n1/b1` | 6.74447 ± 0.0306026 (W 0.00980151) | 8.99813 ± 0.0703939 (W 0.0228213) | 7.16345 ± 0.0817517 (W 0.014549) | 🔵 tcontract 1.33× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` |  |
| `ijkl-imln-njmk/n1/b1` | 6.75025 ± 0.0345063 (W 0.0130124) | 8.98969 ± 0.0874645 (W 0.00819083) | 7.14663 ± 0.0614424 (W 0.0142996) | 🔵 tcontract 1.33× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` |  |
| `ijkl-imnj-nlkm/n1/b1` | 6.76977 ± 0.0354126 (W 0.0137948) | 8.70489 ± 0.0533593 (W 0.0407418) | 7.14418 ± 0.12059 (W 0.0135333) | 🔵 tcontract 1.29× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` |  |
| `ijkl-imnk-njml/n1/b1` | 6.77981 ± 0.0586983 (W 0.0145124) | 8.75257 ± 0.0309697 (W 0.0497665) | 7.12085 ± 0.107159 (W 0.0248745) | 🔵 tcontract 1.29× faster than `ttgt` | · |  |
| `ijkl-minj-nlmk/n1/b1` | 8.34652 ± 0.0346239 (W 0.0139546) | 10.57 ± 0.032763 (W 0.0140794) | 8.7947 ± 0.0876804 (W 0.0165076) | 🔵 tcontract 1.27× faster than `ttgt` | 🔵 tcontract 1.05× faster than `tblis` |  |
| `ijkl-mink-jnlm/n1/b1` | 8.09477 ± 0.0473625 (W 0.0114651) | 10.7181 ± 0.101543 (W 0.00997376) | 8.48593 ± 0.0616787 (W 0.00901657) | 🔵 tcontract 1.32× faster than `ttgt` | · |  |
| `ijkl-minl-njmk/n1/b1` | 8.28978 ± 0.0209613 (W 0.015797) | 10.6239 ± 0.0809015 (W 0.0219862) | 8.65166 ± 0.0706513 (W 0.00615347) | 🔵 tcontract 1.28× faster than `ttgt` | · |  |

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
