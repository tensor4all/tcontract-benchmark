<!-- generated from data/v2-results/tcbench/zen5-cpu/tcbench/20261020T130635Z-split-tcbench/report.md by scripts/publish_report.py; the report below is the source of truth -->

# `tcbench` on `zen5-cpu`

- tcontract-rs commit: `61a04eb1562c671775d1ce254212a598334d3dbb`
- features: `blas, tblis`
- tprims rows: `tprims` (the provider in the measured revision; see library above); `openblas` (the provider in the measured revision; see library above)
- external providers: `tblis` 2.0 @ `b16a732939d8454021e0a0f0097cf1cc1dd3ab19` tag `v2.0-beta2` sha256 `de00bf1552c15f9c4a5d3157f02c149b81aef0909107c51cbb54ba4b8e9b5827` (TBLIS 2.0, configuration zen3; bundled BLIS 358e689cadd6757f564a2992cf46a2f7d6fa6bb0; built with ./configure --prefix=/home/shinaoka/projects/tensor4all/tcontract-benchmark/target/tblis-v2.0-beta2 --with-blis-config-family=zen3 (cmake, Unix Makefiles, Release); libtblis.so sha256 de00bf1552c15f9c)
- harness commit: `7f99a0522f01566a81d1e18a56a0633175b518df`
- toolkit commit: `40e7e11c031788543163d3251b51ee24af72162c`
- measured binary SHA-256: `49a506769c3b6f4eb7fb15051e8eda22b937e38ce1b44d35a589002221058212`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-20T13:17:23.016835Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/v2/record_run.py tcbench zen5-cpu tcbench --aa 3 --reps 5 --prime-ms 250 --external-provider-json /tmp/tblis-v2.json --label split-tcbench`
- raw data: `data/v2-results/tcbench/zen5-cpu/tcbench/20261020T130635Z-split-tcbench/`

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
Spread guide (computed from this run's own rows): per-engine between-start range median 1.21%, worst 96.01% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 60 of 588 engine cells exceed 5% and carry `!`; median within-process relative SD 0.38%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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
`🔵 tcontract X faster than <row>` / `🔴 tcontract X slower than <row>` (the compared row is named in
the cell, not only in the column header), `·` inside the band, `-` that row is not
measured in this arm. `notes` carries the cell warnings (`*` a declared row has no measurement,
`!` between-start range over 5%, `p` position effect over 5%, dispatch-dominated means the
row is under 20 us so 4T/8T pay thread-region start-up). Per-start ratios and every
chronological sample are in the run directory named at the top of this page (`run*.csv`).
These describe the recorded revisions; they are not a regression claim.

## tcbench, f64, 1T (CPU 4)

| case | plan (ms) | ttgt (ms) | tblis (ms) | vs `ttgt` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `abc-bk-akc/n1/b1` | 1.02285 ± 0.00531706 (W 0.00446059) | 1.98301 ± 0.032701 (W 0.00684058) | 1.50903 ± 0.0103427 (W 0.00462223) | 🔵 tcontract 1.94× faster than `ttgt` | 🔵 tcontract 1.48× faster than `tblis` |  |
| `abcijk-eiab-jkec/n1/b1` | 4.50558 ± 0.0211412 (W 0.0106723) | 9.36466 ± 0.0892903 (W 0.0288636) | 5.3898 ± 0.0485413 (W 0.0258758) | 🔵 tcontract 2.08× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `abcijk-eiac-jkeb/n1/b1` | 4.33305 ± 0.0154197 (W 0.00372824) | 9.88126 ± 0.0812376 (W 0.0337048) | 6.62821 ± 0.0931292 (W 0.0459563) | 🔵 tcontract 2.28× faster than `ttgt` | 🔵 tcontract 1.53× faster than `tblis` |  |
| `abcijk-eibc-jkea/n1/b1` | 4.58498 ± 0.0111376 (W 0.0059959) | 11.6394 ± 0.111189 (W 0.0735768) | 5.386 ± 0.0319284 (W 0.0256863) | 🔵 tcontract 2.54× faster than `ttgt` | 🔵 tcontract 1.17× faster than `tblis` |  |
| `abcijk-ejab-ikec/n1/b1` | 4.44956 ± 0.0011705 (W 0.00774637) | 9.03208 ± 0.0837407 (W 0.0233326) | 5.42803 ± 0.0810121 (W 0.0179279) | 🔵 tcontract 2.03× faster than `ttgt` | 🔵 tcontract 1.22× faster than `tblis` |  |
| `abcijk-ejac-ikeb/n1/b1` | 4.33251 ± 0.00377608 (W 0.0156409) | 9.96738 ± 0.0216565 (W 0.0763864) | 5.61032 ± 0.0891277 (W 0.0175551) | 🔵 tcontract 2.30× faster than `ttgt` | 🔵 tcontract 1.29× faster than `tblis` |  |
| `abcijk-ejbc-ikea/n1/b1` | 4.59355 ± 0.00907982 (W 0.005028) | 11.9117 ± 0.270306 (W 0.146956) | 5.70325 ± 0.0234242 (W 0.0311007) | 🔵 tcontract 2.59× faster than `ttgt` | 🔵 tcontract 1.24× faster than `tblis` |  |
| `abcijk-ekab-ijec/n1/b1` | 4.45492 ± 0.0161574 (W 0.00633064) | 9.59394 ± 0.0179908 (W 0.0315831) | 5.24238 ± 0.062361 (W 0.00611152) | 🔵 tcontract 2.15× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `abcijk-ekac-ijeb/n1/b1` | 4.30943 ± 0.0154955 (W 0.0123831) | 11.3517 ± 0.0933112 (W 0.0340939) | 5.85637 ± 0.034663 (W 0.009291) | 🔵 tcontract 2.63× faster than `ttgt` | 🔵 tcontract 1.36× faster than `tblis` |  |
| `abcijk-ekbc-ijea/n1/b1` | 4.59384 ± 0.0146249 (W 0.00844126) | 12.1583 ± 0.128313 (W 0.0898188) | 5.71915 ± 0.00349412 (W 0.0655447) | 🔵 tcontract 2.65× faster than `ttgt` | 🔵 tcontract 1.24× faster than `tblis` |  |
| `abcijk-ijma-mkbc/n1/b1` | 4.59825 ± 0.00436254 (W 0.0128581) | 37.6575 ± 0.537648 (W 0.08065) | 5.69668 ± 0.00638745 (W 0.015802) | 🔵 tcontract 8.19× faster than `ttgt` | 🔵 tcontract 1.24× faster than `tblis` |  |
| `abcijk-ijmb-mkac/n1/b1` | 4.30815 ± 0.00658603 (W 0.0115485) | 36.1054 ± 0.17327 (W 0.159421) | 5.89748 ± 0.0764488 (W 0.0136993) | 🔵 tcontract 8.38× faster than `ttgt` | 🔵 tcontract 1.37× faster than `tblis` |  |
| `abcijk-ijmc-mkab/n1/b1` | 4.44205 ± 0.00502394 (W 0.00564214) | 36.8363 ± 0.15394 (W 0.113753) | 5.20393 ± 0.113893 (W 0.0117751) | 🔵 tcontract 8.29× faster than `ttgt` | 🔵 tcontract 1.17× faster than `tblis` |  |
| `abcijk-ikma-mjbc/n1/b1` | 4.59497 ± 0.0107752 (W 0.0123269) | 43.503 ± 1.28697 (W 0.402957) | 5.70716 ± 0.0105184 (W 0.0267507) | 🔵 tcontract 9.47× faster than `ttgt` | 🔵 tcontract 1.24× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ikmb-mjac/n1/b1` | 4.30572 ± 0.0139462 (W 0.0133986) | 38.5229 ± 0.327243 (W 0.164072) | 5.60874 ± 0.0286978 (W 0.0188662) | 🔵 tcontract 8.95× faster than `ttgt` | 🔵 tcontract 1.30× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 4.44546 ± 0.00530447 (W 0.011372) | 39.7032 ± 0.559082 (W 0.118127) | 5.41558 ± 0.0861462 (W 0.0206013) | 🔵 tcontract 8.93× faster than `ttgt` | 🔵 tcontract 1.22× faster than `tblis` |  |
| `abcijk-jkma-mibc/n1/b1` | 4.59253 ± 0.0171383 (W 0.00539351) | 86.2086 ± 27.1533 (W 0.0795827) | 5.40909 ± 0.0301634 (W 0.0217773) | 🔵 tcontract 18.77× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmb-miac/n1/b1` | 4.32487 ± 0.0121809 (W 0.00973337) | 87.8509 ± 12.0593 (W 0.0601446) | 6.486 ± 0.14977 (W 0.0352453) | 🔵 tcontract 20.31× faster than `ttgt` | 🔵 tcontract 1.50× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmc-miab/n1/b1` | 4.51748 ± 0.0121724 (W 0.00893576) | 85.9698 ± 12.1754 (W 0.0777283) | 5.37198 ± 0.124271 (W 0.0430138) | 🔵 tcontract 19.03× faster than `ttgt` | 🔵 tcontract 1.19× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcs-rc-abrs/n1/b1` | 0.483706 ± 0.00183861 (W 0.00238483) | 1.13627 ± 0.0433613 (W 0.0055323) | 1.16346 ± 0.0125897 (W 0.00704665) | 🔵 tcontract 2.35× faster than `ttgt` | 🔵 tcontract 2.41× faster than `tblis` | `!` between-start range over 5% |
| `abj-bka-kj/n1/b1` | 2.51197 ± 0.0598761 (W 0.0226213) | 2.70723 ± 0.0426522 (W 0.0118001) | 2.63277 ± 0.0350708 (W 0.00864343) | 🔵 tcontract 1.08× faster than `ttgt` | · |  |
| `abjc-cbka-kj/n1/b1` | 1.58795 ± 0.0886643 (W 0.00896798) | 1.25174 ± 0.00744136 (W 0.0127608) | 1.40662 ± 0.0083923 (W 0.0168473) | 🔴 tcontract 1.27× slower than `ttgt` | 🔴 tcontract 1.13× slower than `tblis` | `!` between-start range over 5% |
| `abjc-kbac-jk/n1/b1` | 0.542237 ± 0.00130204 (W 0.00202459) | 1.24687 ± 0.0149596 (W 0.0151647) | 1.13945 ± 0.00658232 (W 0.00403911) | 🔵 tcontract 2.30× faster than `ttgt` | 🔵 tcontract 2.10× faster than `tblis` |  |
| `abjcd-dkbac-jk/n1/b1` | 4.312 ± 0.0218002 (W 0.0157937) | 17.5385 ± 0.70402 (W 0.123731) | 8.23718 ± 0.0381248 (W 0.0498492) | 🔵 tcontract 4.07× faster than `ttgt` | 🔵 tcontract 1.91× faster than `tblis` | `!` between-start range over 5% |
| `abrs-qb-aqrs/n1/b1` | 0.47428 ± 0.00233385 (W 0.00231624) | 1.09238 ± 0.0401124 (W 0.00303602) | 1.15362 ± 0.00478909 (W 0.00513832) | 🔵 tcontract 2.30× faster than `ttgt` | 🔵 tcontract 2.43× faster than `tblis` | `!` between-start range over 5% |
| `adbjc-cbdka-kj/n1/b1` | 10.5236 ± 0.129782 (W 0.0510281) | 11.9114 ± 0.266733 (W 0.0281133) | 9.76886 ± 0.295365 (W 0.161982) | 🔵 tcontract 1.13× faster than `ttgt` | 🔴 tcontract 1.08× slower than `tblis` | `!` between-start range over 5% |
| `ajb-kba-jk/n1/b1` | 1.4483 ± 0.0159579 (W 0.00365413) | 2.44671 ± 0.0131669 (W 0.010804) | 2.10049 ± 0.0678306 (W 0.0288355) | 🔵 tcontract 1.69× faster than `ttgt` | 🔵 tcontract 1.45× faster than `tblis` | `!` between-start range over 5% |
| `ajbc-ckba-jk/n1/b1` | 0.746923 ± 0.00360426 (W 0.00267722) | 3.73151 ± 0.0323822 (W 0.0220078) | 1.22151 ± 0.0169505 (W 0.00921711) | 🔵 tcontract 5.00× faster than `ttgt` | 🔵 tcontract 1.64× faster than `tblis` |  |
| `ajbdc-ckbad-jk/n1/b1` | 4.11117 ± 0.0379059 (W 0.0163771) | 23.9419 ± 0.39927 (W 0.103945) | 7.83613 ± 0.00909766 (W 0.0842414) | 🔵 tcontract 5.82× faster than `ttgt` | 🔵 tcontract 1.91× faster than `tblis` |  |
| `aqrs-pa-pqrs/n1/b1` | 0.310767 ± 0.00803504 (W 0.00189266) | 1.0236 ± 0.0463331 (W 0.00232982) | 1.08404 ± 0.00720698 (W 0.00589051) | 🔵 tcontract 3.29× faster than `ttgt` | 🔵 tcontract 3.49× faster than `tblis` | `!` between-start range over 5% |
| `ij-ik-kj/n1/b1` | 3.42727 ± 0.00906348 (W 0.00304764) | 4.57754 ± 0.0459312 (W 0.00880157) | 4.25887 ± 0.0486755 (W 0.00948201) | 🔵 tcontract 1.34× faster than `ttgt` | 🔵 tcontract 1.24× faster than `tblis` |  |
| `ij-ikl-ljk/n1/b1` | 1.23629 ± 0.0896731 (W 0.00297074) | 1.7443 ± 0.0122161 (W 0.00475042) | 2.1481 ± 0.00103622 (W 0.00610044) | 🔵 tcontract 1.41× faster than `ttgt` | 🔵 tcontract 1.74× faster than `tblis` | `!` between-start range over 5% |
| `ij-kil-lkj/n1/b1` | 1.80859 ± 0.0210041 (W 0.00760842) | 2.68343 ± 0.0163726 (W 0.00906703) | 3.01408 ± 0.0134658 (W 0.00886053) | 🔵 tcontract 1.48× faster than `ttgt` | 🔵 tcontract 1.67× faster than `tblis` |  |
| `ijk-ikl-lj/n1/b1` | 1.09324 ± 0.0112258 (W 0.00239042) | 1.65022 ± 0.0312715 (W 0.00407936) | 1.72168 ± 0.00632518 (W 0.0051692) | 🔵 tcontract 1.51× faster than `ttgt` | 🔵 tcontract 1.57× faster than `tblis` |  |
| `ijk-il-jlk/n1/b1` | 1.06922 ± 0.00678907 (W 0.00143979) | 1.92501 ± 0.00653839 (W 0.0115919) | 1.59373 ± 0.0122893 (W 0.00548493) | 🔵 tcontract 1.80× faster than `ttgt` | 🔵 tcontract 1.49× faster than `tblis` |  |
| `ijk-ilk-jl/n1/b1` | 1.01535 ± 0.00538119 (W 0.000800442) | 1.79991 ± 0.022437 (W 0.0317847) | 1.51572 ± 0.00144919 (W 0.00423841) | 🔵 tcontract 1.77× faster than `ttgt` | 🔵 tcontract 1.49× faster than `tblis` |  |
| `ijk-ilk-lj/n1/b1` | 1.09219 ± 0.00410111 (W 0.00169833) | 1.77106 ± 0.0441005 (W 0.0137616) | 1.71284 ± 0.00507406 (W 0.0096312) | 🔵 tcontract 1.62× faster than `ttgt` | 🔵 tcontract 1.57× faster than `tblis` |  |
| `ijk-ilmk-mjl/n1/b1` | 0.43244 ± 0.0018966 (W 0.00243568) | 0.645105 ± 0.00459116 (W 0.00197862) | 0.962264 ± 0.00244954 (W 0.0015966) | 🔵 tcontract 1.49× faster than `ttgt` | 🔵 tcontract 2.23× faster than `tblis` |  |
| `ijkl-imjn-lnkm/n1/b1` | 6.2459 ± 0.0134593 (W 0.0129758) | 7.99269 ± 0.00440062 (W 0.020767) | 7.49739 ± 0.0805812 (W 0.0248932) | 🔵 tcontract 1.28× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `ijkl-imjn-nlmk/n1/b1` | 6.2245 ± 0.0214884 (W 0.0184086) | 7.94501 ± 0.0225863 (W 0.0205119) | 7.46713 ± 0.0706486 (W 0.0187893) | 🔵 tcontract 1.28× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `ijkl-imkn-jnlm/n1/b1` | 6.194 ± 0.0161613 (W 0.0193109) | 7.95336 ± 0.0233697 (W 0.00973691) | 7.31891 ± 0.059014 (W 0.0232373) | 🔵 tcontract 1.28× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `ijkl-imkn-njml/n1/b1` | 6.19524 ± 0.0123961 (W 0.00506159) | 7.98822 ± 0.051709 (W 0.0171373) | 7.3623 ± 0.0397131 (W 0.0165104) | 🔵 tcontract 1.29× faster than `ttgt` | 🔵 tcontract 1.19× faster than `tblis` |  |
| `ijkl-imln-jnkm/n1/b1` | 6.20651 ± 0.0181618 (W 0.0153373) | 8.00073 ± 0.0169917 (W 0.0192613) | 7.2719 ± 0.0232536 (W 0.0166816) | 🔵 tcontract 1.29× faster than `ttgt` | 🔵 tcontract 1.17× faster than `tblis` |  |
| `ijkl-imln-njmk/n1/b1` | 6.19449 ± 0.00797654 (W 0.0192608) | 8.00096 ± 0.0494702 (W 0.0223718) | 7.23978 ± 0.0350643 (W 0.0143849) | 🔵 tcontract 1.29× faster than `ttgt` | 🔵 tcontract 1.17× faster than `tblis` |  |
| `ijkl-imnj-nlkm/n1/b1` | 6.21922 ± 0.00547699 (W 0.0171875) | 7.91965 ± 0.00910254 (W 0.0201911) | 7.3611 ± 0.0545051 (W 0.0256664) | 🔵 tcontract 1.27× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `ijkl-imnk-njml/n1/b1` | 6.18684 ± 0.0123481 (W 0.00793732) | 7.91694 ± 0.0402608 (W 0.00936924) | 7.29387 ± 0.0490412 (W 0.00566382) | 🔵 tcontract 1.28× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `ijkl-minj-nlmk/n1/b1` | 7.61601 ± 0.0194739 (W 0.0116565) | 9.63974 ± 0.234164 (W 0.0115038) | 9.0476 ± 0.0233184 (W 0.0284457) | 🔵 tcontract 1.27× faster than `ttgt` | 🔵 tcontract 1.19× faster than `tblis` |  |
| `ijkl-mink-jnlm/n1/b1` | 7.49605 ± 0.00538104 (W 0.0145204) | 9.56304 ± 0.0283429 (W 0.0236546) | 8.71318 ± 0.0552065 (W 0.0141546) | 🔵 tcontract 1.28× faster than `ttgt` | 🔵 tcontract 1.16× faster than `tblis` |  |
| `ijkl-minl-njmk/n1/b1` | 7.58421 ± 0.0147923 (W 0.00989409) | 9.62112 ± 0.0311526 (W 0.0211486) | 8.81883 ± 0.0888094 (W 0.0124781) | 🔵 tcontract 1.27× faster than `ttgt` | 🔵 tcontract 1.16× faster than `tblis` |  |

## tcbench, f64, 4T (CPU 4-7)

| case | plan (ms) | ttgt (ms) | tblis (ms) | vs `ttgt` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `abc-bk-akc/n1/b1` | 0.274459 ± 0.00564036 (W 0.00235554) | 1.22415 ± 0.00812092 (W 0.011174) | 0.426272 ± 0.00171239 (W 0.00219096) | 🔵 tcontract 4.46× faster than `ttgt` | 🔵 tcontract 1.55× faster than `tblis` |  |
| `abcijk-eiab-jkec/n1/b1` | 1.18417 ± 0.0024712 (W 0.00684142) | 6.10264 ± 0.0691384 (W 0.0286052) | 1.71661 ± 0.065257 (W 0.0364378) | 🔵 tcontract 5.15× faster than `ttgt` | 🔵 tcontract 1.45× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-eiac-jkeb/n1/b1` | 1.10347 ± 0.00283682 (W 0.00842649) | 6.66644 ± 0.127924 (W 0.0455297) | 2.27037 ± 0.101732 (W 0.0892574) | 🔵 tcontract 6.04× faster than `ttgt` | 🔵 tcontract 2.06× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-eibc-jkea/n1/b1` | 1.18138 ± 0.00635904 (W 0.00373603) | 8.28778 ± 0.140263 (W 0.0318034) | 1.45727 ± 0.0112732 (W 0.0100148) | 🔵 tcontract 7.02× faster than `ttgt` | 🔵 tcontract 1.23× faster than `tblis` |  |
| `abcijk-ejab-ikec/n1/b1` | 1.15814 ± 0.0062026 (W 0.00930549) | 5.82026 ± 0.0801886 (W 0.0216486) | 1.6741 ± 0.0519182 (W 0.024801) | 🔵 tcontract 5.03× faster than `ttgt` | 🔵 tcontract 1.45× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ejac-ikeb/n1/b1` | 1.10433 ± 0.0281501 (W 0.00588232) | 7.02158 ± 0.0391812 (W 0.0361093) | 1.54933 ± 0.0121317 (W 0.0115918) | 🔵 tcontract 6.36× faster than `ttgt` | 🔵 tcontract 1.40× faster than `tblis` |  |
| `abcijk-ejbc-ikea/n1/b1` | 1.19251 ± 0.00490837 (W 0.00757716) | 8.57258 ± 0.190931 (W 0.0367552) | 1.53391 ± 0.00834705 (W 0.0118737) | 🔵 tcontract 7.19× faster than `ttgt` | 🔵 tcontract 1.29× faster than `tblis` |  |
| `abcijk-ekab-ijec/n1/b1` | 1.14914 ± 0.00525467 (W 0.00384546) | 6.36834 ± 0.0429717 (W 0.0322823) | 1.45176 ± 0.0478633 (W 0.0246134) | 🔵 tcontract 5.54× faster than `ttgt` | 🔵 tcontract 1.26× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ekac-ijeb/n1/b1` | 1.11463 ± 0.00789843 (W 0.0106028) | 8.18241 ± 0.129102 (W 0.0127355) | 2.05083 ± 0.0251982 (W 0.0492952) | 🔵 tcontract 7.34× faster than `ttgt` | 🔵 tcontract 1.84× faster than `tblis` |  |
| `abcijk-ekbc-ijea/n1/b1` | 1.18856 ± 0.00090261 (W 0.00442434) | 9.12041 ± 0.259537 (W 0.0744766) | 1.53606 ± 0.0708826 (W 0.0151501) | 🔵 tcontract 7.67× faster than `ttgt` | 🔵 tcontract 1.29× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ijma-mkbc/n1/b1` | 1.18954 ± 0.0138457 (W 0.00485734) | 35.4734 ± 0.77043 (W 0.205892) | 1.52521 ± 0.00958382 (W 0.00874211) | 🔵 tcontract 29.82× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` |  |
| `abcijk-ijmb-mkac/n1/b1` | 1.1019 ± 0.0106236 (W 0.0109079) | 32.9322 ± 0.296161 (W 0.128836) | 2.07282 ± 0.0313335 (W 0.0644487) | 🔵 tcontract 29.89× faster than `ttgt` | 🔵 tcontract 1.88× faster than `tblis` |  |
| `abcijk-ijmc-mkab/n1/b1` | 1.15533 ± 0.0166332 (W 0.01158) | 33.8816 ± 0.0475996 (W 0.114249) | 1.47918 ± 0.0327736 (W 0.0380358) | 🔵 tcontract 29.33× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` |  |
| `abcijk-ikma-mjbc/n1/b1` | 1.20015 ± 0.00507706 (W 0.0194663) | 38.0238 ± 1.6804 (W 0.103266) | 1.53729 ± 0.0109905 (W 0.0137214) | 🔵 tcontract 31.68× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ikmb-mjac/n1/b1` | 1.09933 ± 0.00350635 (W 0.00359835) | 34.9679 ± 0.289608 (W 0.0631437) | 1.54961 ± 0.0039661 (W 0.0056614) | 🔵 tcontract 31.81× faster than `ttgt` | 🔵 tcontract 1.41× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 1.15146 ± 0.637543 (W 0.00536656) | 35.9486 ± 0.117526 (W 0.253907) | 1.68262 ± 0.0471391 (W 0.047567) | 🔵 tcontract 31.22× faster than `ttgt` | · | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkma-mibc/n1/b1` | 1.19111 ± 0.00494495 (W 0.00393162) | 108.517 ± 15.0783 (W 0.076911) | 1.45502 ± 0.0149418 (W 0.0101618) | 🔵 tcontract 91.11× faster than `ttgt` | 🔵 tcontract 1.22× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmb-miac/n1/b1` | 1.10444 ± 0.0331226 (W 0.0169388) | 94.2978 ± 2.86827 (W 0.0724314) | 2.23083 ± 0.084888 (W 0.0643234) | 🔵 tcontract 85.38× faster than `ttgt` | 🔵 tcontract 2.02× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-jkmc-miab/n1/b1` | 1.18488 ± 0.00297877 (W 0.00789041) | 93.7902 ± 6.42814 (W 0.149175) | 1.70696 ± 0.0897914 (W 0.0504238) | 🔵 tcontract 79.16× faster than `ttgt` | 🔵 tcontract 1.44× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcs-rc-abrs/n1/b1` | 0.143737 ± 0.000613537 (W 0.00163691) | 0.760781 ± 0.0243518 (W 0.00980631) | 0.379925 ± 0.00513665 (W 0.00360282) | 🔵 tcontract 5.29× faster than `ttgt` | 🔵 tcontract 2.64× faster than `tblis` | `!` between-start range over 5% |
| `abj-bka-kj/n1/b1` | 0.496441 ± 0.0015918 (W 0.00230016) | 1.44195 ± 0.030788 (W 0.00533244) | 0.721016 ± 0.00631532 (W 0.00509739) | 🔵 tcontract 2.90× faster than `ttgt` | 🔵 tcontract 1.45× faster than `tblis` |  |
| `abjc-cbka-kj/n1/b1` | 0.287563 ± 0.00207424 (W 0.00309584) | 0.821433 ± 0.0219471 (W 0.00490112) | 0.463419 ± 0.00570496 (W 0.0076707) | 🔵 tcontract 2.86× faster than `ttgt` | 🔵 tcontract 1.61× faster than `tblis` | `!` between-start range over 5% |
| `abjc-kbac-jk/n1/b1` | 0.159986 ± 0.00155162 (W 0.000574588) | 0.89903 ± 0.0184703 (W 0.00311414) | 0.377841 ± 0.00136805 (W 0.003458) | 🔵 tcontract 5.62× faster than `ttgt` | 🔵 tcontract 2.36× faster than `tblis` |  |
| `abjcd-dkbac-jk/n1/b1` | 1.4372 ± 0.0520431 (W 0.0154948) | 16.2935 ± 0.0815897 (W 0.0657655) | 2.78756 ± 0.0117479 (W 0.0247743) | 🔵 tcontract 11.34× faster than `ttgt` | 🔵 tcontract 1.94× faster than `tblis` | `!` between-start range over 5% |
| `abrs-qb-aqrs/n1/b1` | 0.142454 ± 0.000115902 (W 0.00123244) | 0.742268 ± 0.0452536 (W 0.00393023) | 0.374374 ± 0.00141613 (W 0.00391182) | 🔵 tcontract 5.21× faster than `ttgt` | 🔵 tcontract 2.63× faster than `tblis` | `!` between-start range over 5% |
| `adbjc-cbdka-kj/n1/b1` | 6.11303 ± 0.0994579 (W 0.110704) | 9.88932 ± 0.0636778 (W 0.0247757) | 3.63788 ± 0.0536601 (W 0.11404) | 🔵 tcontract 1.62× faster than `ttgt` | 🔴 tcontract 1.68× slower than `tblis` |  |
| `ajb-kba-jk/n1/b1` | 0.385195 ± 0.00251649 (W 0.00854921) | 1.33519 ± 0.00167604 (W 0.00515895) | 0.567172 ± 0.00375049 (W 0.00305667) | 🔵 tcontract 3.47× faster than `ttgt` | 🔵 tcontract 1.47× faster than `tblis` |  |
| `ajbc-ckba-jk/n1/b1` | 0.220188 ± 0.00873699 (W 0.00246197) | 3.2739 ± 0.0207043 (W 0.0118759) | 0.407505 ± 0.000902109 (W 0.00422273) | 🔵 tcontract 14.87× faster than `ttgt` | 🔵 tcontract 1.85× faster than `tblis` | `!` between-start range over 5% |
| `ajbdc-ckbad-jk/n1/b1` | 1.44521 ± 0.0372325 (W 0.0144561) | 22.7595 ± 0.42405 (W 0.16936) | 2.68384 ± 0.0281551 (W 0.0353628) | 🔵 tcontract 15.75× faster than `ttgt` | 🔵 tcontract 1.86× faster than `tblis` |  |
| `aqrs-pa-pqrs/n1/b1` | 0.095757 ± 0.000746454 (W 0.00126556) | 0.655507 ± 0.0360072 (W 0.00852183) | 0.348958 ± 0.00309391 (W 0.00447461) | 🔵 tcontract 6.85× faster than `ttgt` | 🔵 tcontract 3.64× faster than `tblis` | `!` between-start range over 5% |
| `ij-ik-kj/n1/b1` | 0.877007 ± 0.00521308 (W 0.00346019) | 1.49641 ± 0.0382924 (W 0.00539752) | 1.21166 ± 0.00139136 (W 0.004903) | 🔵 tcontract 1.71× faster than `ttgt` | 🔵 tcontract 1.38× faster than `tblis` |  |
| `ij-ikl-ljk/n1/b1` | 0.541744 ± 0.00618434 (W 0.0118924) | 0.837205 ± 0.0140511 (W 0.014892) | 0.878701 ± 0.00114876 (W 0.00457615) | 🔵 tcontract 1.55× faster than `ttgt` | 🔵 tcontract 1.62× faster than `tblis` |  |
| `ij-kil-lkj/n1/b1` | 0.777651 ± 0.0071364 (W 0.00951924) | 1.52709 ± 0.0444837 (W 0.00485827) | 1.21035 ± 0.00795403 (W 0.00514271) | 🔵 tcontract 1.96× faster than `ttgt` | 🔵 tcontract 1.56× faster than `tblis` | `!` between-start range over 5% |
| `ijk-ikl-lj/n1/b1` | 0.29626 ± 0.00297789 (W 0.00711079) | 0.80993 ± 0.0136031 (W 0.00212032) | 0.476032 ± 0.00391548 (W 0.00491033) | 🔵 tcontract 2.73× faster than `ttgt` | 🔵 tcontract 1.61× faster than `tblis` |  |
| `ijk-il-jlk/n1/b1` | 0.284558 ± 0.00179637 (W 0.00163631) | 1.20715 ± 0.00821924 (W 0.0189171) | 0.436839 ± 0.00421073 (W 0.00376388) | 🔵 tcontract 4.24× faster than `ttgt` | 🔵 tcontract 1.54× faster than `tblis` |  |
| `ijk-ilk-jl/n1/b1` | 0.272656 ± 0.00159039 (W 0.00188554) | 0.91586 ± 0.0101701 (W 0.0115174) | 0.425961 ± 0.00150109 (W 0.00241856) | 🔵 tcontract 3.36× faster than `ttgt` | 🔵 tcontract 1.56× faster than `tblis` |  |
| `ijk-ilk-lj/n1/b1` | 0.293203 ± 0.00231872 (W 0.0035779) | 0.888367 ± 0.00706561 (W 0.010752) | 0.476214 ± 0.00469978 (W 0.00277531) | 🔵 tcontract 3.03× faster than `ttgt` | 🔵 tcontract 1.62× faster than `tblis` |  |
| `ijk-ilmk-mjl/n1/b1` | 0.134018 ± 0.0123608 (W 0.00464829) | 0.374845 ± 0.00189819 (W 0.00228551) | 0.285138 ± 0.00240265 (W 0.00289202) | 🔵 tcontract 2.80× faster than `ttgt` | 🔵 tcontract 2.13× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `ijkl-imjn-lnkm/n1/b1` | 1.61123 ± 0.00823415 (W 0.003544) | 2.65684 ± 0.0105434 (W 0.00938845) | 2.00296 ± 0.0892248 (W 0.00551709) | 🔵 tcontract 1.65× faster than `ttgt` | 🔵 tcontract 1.24× faster than `tblis` | `!` between-start range over 5% |
| `ijkl-imjn-nlmk/n1/b1` | 1.59261 ± 0.00294749 (W 0.00190977) | 2.65005 ± 0.0453938 (W 0.0167127) | 2.04142 ± 0.0177629 (W 0.00799338) | 🔵 tcontract 1.66× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` |  |
| `ijkl-imkn-jnlm/n1/b1` | 1.57983 ± 0.0100738 (W 0.00251023) | 2.65324 ± 0.010095 (W 0.00839806) | 1.9585 ± 0.039277 (W 0.00426264) | 🔵 tcontract 1.68× faster than `ttgt` | 🔵 tcontract 1.24× faster than `tblis` |  |
| `ijkl-imkn-njml/n1/b1` | 1.58153 ± 0.00455689 (W 0.0070287) | 2.66683 ± 0.0527794 (W 0.00377302) | 2.01818 ± 0.000405692 (W 0.00493049) | 🔵 tcontract 1.69× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` |  |
| `ijkl-imln-jnkm/n1/b1` | 1.58109 ± 0.00747346 (W 0.00297914) | 2.66616 ± 0.047326 (W 0.00331808) | 1.93664 ± 0.0395014 (W 0.00476245) | 🔵 tcontract 1.69× faster than `ttgt` | 🔵 tcontract 1.22× faster than `tblis` |  |
| `ijkl-imln-njmk/n1/b1` | 1.58286 ± 0.00532199 (W 0.00366845) | 2.66361 ± 0.0398704 (W 0.00792128) | 2.00508 ± 0.0131494 (W 0.00274126) | 🔵 tcontract 1.68× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `ijkl-imnj-nlkm/n1/b1` | 1.58933 ± 0.0180396 (W 0.00277535) | 2.61014 ± 0.0468293 (W 0.00796997) | 2.02611 ± 0.0154525 (W 0.00442367) | 🔵 tcontract 1.64× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `ijkl-imnk-njml/n1/b1` | 1.58392 ± 0.00362123 (W 0.00198083) | 2.64788 ± 0.0618488 (W 0.0178919) | 1.99822 ± 0.00423621 (W 0.00270256) | 🔵 tcontract 1.67× faster than `ttgt` | 🔵 tcontract 1.26× faster than `tblis` |  |
| `ijkl-minj-nlmk/n1/b1` | 1.9482 ± 0.00835491 (W 0.00381294) | 3.2494 ± 0.0978597 (W 0.00789619) | 2.4927 ± 0.0194658 (W 0.0075639) | 🔵 tcontract 1.67× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` | `!` between-start range over 5% |
| `ijkl-mink-jnlm/n1/b1` | 1.90857 ± 0.00421426 (W 0.0020462) | 3.19381 ± 0.0113358 (W 0.00568366) | 2.39724 ± 0.0228899 (W 0.00876457) | 🔵 tcontract 1.67× faster than `ttgt` | 🔵 tcontract 1.26× faster than `tblis` |  |
| `ijkl-minl-njmk/n1/b1` | 1.93583 ± 0.011488 (W 0.00421342) | 3.25426 ± 0.022167 (W 0.00962783) | 2.42657 ± 0.0118932 (W 0.00687315) | 🔵 tcontract 1.68× faster than `ttgt` | 🔵 tcontract 1.25× faster than `tblis` |  |

## tcbench, c64, 1T (CPU 4)

| case | plan (ms) | ttgt (ms) | tblis (ms) | vs `ttgt` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `abc-bk-akc/n1/b1` | 4.09463 ± 0.00935315 (W 0.00366029) | 6.22439 ± 0.0143995 (W 0.0131237) | 4.88367 ± 0.0915668 (W 0.0121643) | 🔵 tcontract 1.52× faster than `ttgt` | 🔵 tcontract 1.19× faster than `tblis` |  |
| `abcijk-eiab-jkec/n1/b1` | 17.6417 ± 0.0656206 (W 0.0398743) | 40.4034 ± 0.314905 (W 0.154452) | 19.0626 ± 0.0484812 (W 0.0382522) | 🔵 tcontract 2.29× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `abcijk-eiac-jkeb/n1/b1` | 17.3485 ± 0.0331363 (W 0.0384709) | 41.6311 ± 0.416121 (W 0.147938) | 20.7409 ± 0.0531627 (W 0.0633876) | 🔵 tcontract 2.40× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `abcijk-eibc-jkea/n1/b1` | 17.699 ± 0.0755809 (W 0.0515176) | 44.2609 ± 0.514921 (W 0.23434) | 19.0752 ± 0.0156594 (W 0.0505106) | 🔵 tcontract 2.50× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `abcijk-ejab-ikec/n1/b1` | 17.552 ± 0.0499853 (W 0.0233521) | 40.0906 ± 0.696366 (W 0.207034) | 19.1623 ± 0.0181233 (W 0.0676671) | 🔵 tcontract 2.28× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `abcijk-ejac-ikeb/n1/b1` | 17.3465 ± 0.0455898 (W 0.0311739) | 41.4635 ± 0.087023 (W 0.155468) | 19.5862 ± 0.0408531 (W 0.0499031) | 🔵 tcontract 2.39× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ejbc-ikea/n1/b1` | 17.7346 ± 0.0532983 (W 0.0264854) | 44.8488 ± 0.315903 (W 0.19302) | 20.0406 ± 0.144746 (W 0.0786914) | 🔵 tcontract 2.53× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ekab-ijec/n1/b1` | 17.5568 ± 0.03912 (W 0.0354285) | 40.1693 ± 0.511398 (W 0.18759) | 18.9457 ± 0.111539 (W 0.0550182) | 🔵 tcontract 2.29× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `abcijk-ekac-ijeb/n1/b1` | 17.3221 ± 0.0218223 (W 0.0331339) | 42.0908 ± 0.599044 (W 0.276064) | 20.0937 ± 0.0942966 (W 0.0593815) | 🔵 tcontract 2.43× faster than `ttgt` | 🔵 tcontract 1.16× faster than `tblis` |  |
| `abcijk-ekbc-ijea/n1/b1` | 17.7248 ± 0.0291059 (W 0.0323045) | 46.3918 ± 0.994555 (W 0.180908) | 20.0362 ± 0.0561482 (W 0.0568348) | 🔵 tcontract 2.62× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ijma-mkbc/n1/b1` | 17.6902 ± 0.0196647 (W 0.0400596) | 65.3523 ± 0.281218 (W 0.353685) | 20.05 ± 0.0335341 (W 0.0569771) | 🔵 tcontract 3.69× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ijmb-mkac/n1/b1` | 17.3242 ± 0.00416761 (W 0.0166666) | 66.4891 ± 0.395208 (W 0.185595) | 20.019 ± 0.0550133 (W 0.0293259) | 🔵 tcontract 3.84× faster than `ttgt` | 🔵 tcontract 1.16× faster than `tblis` |  |
| `abcijk-ijmc-mkab/n1/b1` | 17.5725 ± 0.0416818 (W 0.0205629) | 78.5712 ± 0.367915 (W 0.395757) | 18.8919 ± 0.0511433 (W 0.0575185) | 🔵 tcontract 4.47× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `abcijk-ikma-mjbc/n1/b1` | 17.7205 ± 0.0191547 (W 0.0222312) | 67.9744 ± 1.13381 (W 0.222589) | 20.0431 ± 0.113085 (W 0.0529211) | 🔵 tcontract 3.84× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ikmb-mjac/n1/b1` | 17.3413 ± 0.00825203 (W 0.0425077) | 68.306 ± 0.404453 (W 0.273582) | 19.5565 ± 0.0709065 (W 0.0458973) | 🔵 tcontract 3.94× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 17.6115 ± 0.0247502 (W 0.0396025) | 78.7183 ± 0.625653 (W 0.363869) | 19.1771 ± 0.0550355 (W 0.0949892) | 🔵 tcontract 4.47× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `abcijk-jkma-mibc/n1/b1` | 17.717 ± 0.0136717 (W 0.053977) | 108.179 ± 1.53313 (W 0.448375) | 19.1346 ± 0.00712636 (W 0.0435102) | 🔵 tcontract 6.11× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `abcijk-jkmb-miac/n1/b1` | 17.3376 ± 0.0289687 (W 0.0258173) | 107.926 ± 2.53451 (W 0.311947) | 20.7663 ± 0.121435 (W 0.104179) | 🔵 tcontract 6.22× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `abcijk-jkmc-miab/n1/b1` | 17.6168 ± 0.0476317 (W 0.0256042) | 112.501 ± 0.357282 (W 0.219771) | 19.0992 ± 0.0794095 (W 0.0768491) | 🔵 tcontract 6.39× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `abcs-rc-abrs/n1/b1` | 1.85371 ± 0.00968726 (W 0.00170922) | 2.83692 ± 0.050035 (W 0.0158576) | 2.37995 ± 0.00823633 (W 0.00678117) | 🔵 tcontract 1.53× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` |  |
| `abj-bka-kj/n1/b1` | 7.50665 ± 0.0196425 (W 0.0246714) | 8.28594 ± 0.0129382 (W 0.0215417) | 8.38317 ± 0.0862215 (W 0.0515112) | 🔵 tcontract 1.10× faster than `ttgt` | 🔵 tcontract 1.12× faster than `tblis` |  |
| `abjc-cbka-kj/n1/b1` | 3.59866 ± 0.0130693 (W 0.00737353) | 3.61986 ± 0.0430035 (W 0.00709593) | 3.06938 ± 0.0492831 (W 0.112191) | · | 🔴 tcontract 1.17× slower than `tblis` |  |
| `abjc-kbac-jk/n1/b1` | 1.98495 ± 0.00594672 (W 0.00670906) | 3.5152 ± 0.0432356 (W 0.0279026) | 2.6527 ± 0.00806959 (W 0.0160493) | 🔵 tcontract 1.77× faster than `ttgt` | 🔵 tcontract 1.34× faster than `tblis` |  |
| `abjcd-dkbac-jk/n1/b1` | 12.9034 ± 0.041752 (W 0.0696154) | 30.8228 ± 1.35638 (W 0.125435) | 17.2624 ± 0.100563 (W 0.123205) | 🔵 tcontract 2.39× faster than `ttgt` | 🔵 tcontract 1.34× faster than `tblis` | `!` between-start range over 5% |
| `abrs-qb-aqrs/n1/b1` | 1.60415 ± 0.00306239 (W 0.0042638) | 2.84507 ± 0.0189661 (W 0.0466808) | 2.46837 ± 0.0432838 (W 0.0890443) | 🔵 tcontract 1.77× faster than `ttgt` | 🔵 tcontract 1.54× faster than `tblis` |  |
| `adbjc-cbdka-kj/n1/b1` | 20.1972 ± 0.117433 (W 0.0717854) | 22.9013 ± 0.0645868 (W 0.027713) | 19.0408 ± 0.421993 (W 0.16405) | 🔵 tcontract 1.13× faster than `ttgt` | 🔴 tcontract 1.06× slower than `tblis` |  |
| `ajb-kba-jk/n1/b1` | 5.71551 ± 0.0275735 (W 0.0125291) | 7.97899 ± 0.00879882 (W 0.028894) | 7.25907 ± 0.0624066 (W 0.0657665) | 🔵 tcontract 1.40× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `ajbc-ckba-jk/n1/b1` | 2.2887 ± 0.0546888 (W 0.00577742) | 5.67706 ± 0.0417775 (W 0.0185196) | 2.97846 ± 0.075329 (W 0.0447263) | 🔵 tcontract 2.48× faster than `ttgt` | 🔵 tcontract 1.30× faster than `tblis` |  |
| `ajbdc-ckbad-jk/n1/b1` | 12.5923 ± 0.0159023 (W 0.0587873) | 34.8581 ± 0.619917 (W 0.0701703) | 17.2821 ± 0.0436596 (W 0.251679) | 🔵 tcontract 2.77× faster than `ttgt` | 🔵 tcontract 1.37× faster than `tblis` |  |
| `aqrs-pa-pqrs/n1/b1` | 2.05147 ± 0.00867164 (W 0.00252824) | 2.42963 ± 0.0180953 (W 0.0056326) | 2.33893 ± 0.00700591 (W 0.00562674) | 🔵 tcontract 1.18× faster than `ttgt` | 🔵 tcontract 1.14× faster than `tblis` |  |
| `ij-ik-kj/n1/b1` | 14.545 ± 0.0373988 (W 0.0269791) | 17.5841 ± 0.0492915 (W 0.0303254) | 15.3633 ± 0.150877 (W 0.0334509) | 🔵 tcontract 1.21× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` |  |
| `ij-ikl-ljk/n1/b1` | 4.85566 ± 0.00874994 (W 0.0137076) | 5.77676 ± 0.0302747 (W 0.00828946) | 5.77738 ± 0.128036 (W 0.0568154) | 🔵 tcontract 1.19× faster than `ttgt` | 🔵 tcontract 1.19× faster than `tblis` |  |
| `ij-kil-lkj/n1/b1` | 7.3876 ± 0.0527218 (W 0.0238566) | 8.64629 ± 0.0135428 (W 0.0249046) | 8.3613 ± 0.117263 (W 0.018174) | 🔵 tcontract 1.17× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `ijk-ikl-lj/n1/b1` | 4.20585 ± 0.00735389 (W 0.00909679) | 5.35505 ± 0.172614 (W 0.0144839) | 5.72225 ± 0.0263595 (W 0.0479507) | 🔵 tcontract 1.27× faster than `ttgt` | 🔵 tcontract 1.36× faster than `tblis` | `!` between-start range over 5% |
| `ijk-il-jlk/n1/b1` | 4.54136 ± 0.028075 (W 0.0128029) | 6.08742 ± 0.01135 (W 0.0218061) | 4.79699 ± 0.0284683 (W 0.00873278) | 🔵 tcontract 1.34× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` |  |
| `ijk-ilk-jl/n1/b1` | 4.05347 ± 0.0457373 (W 0.00223257) | 5.81656 ± 0.00860858 (W 0.00821939) | 5.06101 ± 0.07492 (W 0.0599626) | 🔵 tcontract 1.43× faster than `ttgt` | 🔵 tcontract 1.25× faster than `tblis` |  |
| `ijk-ilk-lj/n1/b1` | 4.24726 ± 0.0376048 (W 0.00580143) | 5.87705 ± 0.0245908 (W 0.0191476) | 5.27881 ± 0.156776 (W 0.0224661) | 🔵 tcontract 1.38× faster than `ttgt` | 🔵 tcontract 1.24× faster than `tblis` | `!` between-start range over 5% |
| `ijk-ilmk-mjl/n1/b1` | 1.63654 ± 0.092899 (W 0.00486405) | 2.0343 ± 0.012283 (W 0.00774164) | 2.00113 ± 0.0492852 (W 0.00470121) | 🔵 tcontract 1.24× faster than `ttgt` | 🔵 tcontract 1.22× faster than `tblis` | `!` between-start range over 5% |
| `ijkl-imjn-lnkm/n1/b1` | 25.0455 ± 0.0111267 (W 0.0246097) | 30.6713 ± 0.0561522 (W 0.0447236) | 26.7173 ± 0.213603 (W 0.0525752) | 🔵 tcontract 1.22× faster than `ttgt` | 🔵 tcontract 1.07× faster than `tblis` |  |
| `ijkl-imjn-nlmk/n1/b1` | 25.037 ± 0.0616313 (W 0.0262899) | 30.6132 ± 0.0920465 (W 0.0958351) | 27.6581 ± 1.33755 (W 0.0933873) | 🔵 tcontract 1.22× faster than `ttgt` | 🔵 tcontract 1.10× faster than `tblis` | `!` between-start range over 5% |
| `ijkl-imkn-jnlm/n1/b1` | 25.0424 ± 0.0159563 (W 0.0808255) | 30.6727 ± 0.0696237 (W 0.0461163) | 26.6235 ± 0.0641606 (W 0.169279) | 🔵 tcontract 1.22× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` |  |
| `ijkl-imkn-njml/n1/b1` | 25.0576 ± 0.126979 (W 0.0607328) | 30.6525 ± 0.0947113 (W 0.0631531) | 27.4099 ± 0.139429 (W 0.0541874) | 🔵 tcontract 1.22× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `ijkl-imln-jnkm/n1/b1` | 24.9733 ± 0.0551062 (W 0.0485082) | 30.6733 ± 0.0595771 (W 0.050211) | 26.7994 ± 0.240323 (W 0.0596535) | 🔵 tcontract 1.23× faster than `ttgt` | 🔵 tcontract 1.07× faster than `tblis` |  |
| `ijkl-imln-njmk/n1/b1` | 24.9973 ± 0.0539928 (W 0.0408256) | 30.5769 ± 0.0462903 (W 0.0314696) | 27.1292 ± 0.140011 (W 0.069578) | 🔵 tcontract 1.22× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `ijkl-imnj-nlkm/n1/b1` | 24.9747 ± 0.0746364 (W 0.0349987) | 30.3298 ± 0.00344775 (W 0.0584812) | 27.1344 ± 0.212312 (W 0.0704127) | 🔵 tcontract 1.21× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `ijkl-imnk-njml/n1/b1` | 25.0859 ± 0.0866974 (W 0.0562912) | 30.3846 ± 0.0528741 (W 0.0637209) | 27.1718 ± 0.0864176 (W 0.0767468) | 🔵 tcontract 1.21× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `ijkl-minj-nlmk/n1/b1` | 30.7741 ± 0.0361449 (W 0.0610051) | 36.618 ± 0.0578464 (W 0.0458639) | 33.4138 ± 0.317118 (W 0.11011) | 🔵 tcontract 1.19× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `ijkl-mink-jnlm/n1/b1` | 30.1136 ± 0.0391434 (W 0.044957) | 36.6034 ± 0.0919167 (W 0.0731365) | 31.9887 ± 0.263342 (W 0.11125) | 🔵 tcontract 1.22× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` |  |
| `ijkl-minl-njmk/n1/b1` | 30.7016 ± 0.035286 (W 0.0561862) | 36.6209 ± 0.0903527 (W 0.0562794) | 32.6117 ± 0.331689 (W 0.0851554) | 🔵 tcontract 1.19× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` |  |

## tcbench, c64, 4T (CPU 4-7)

| case | plan (ms) | ttgt (ms) | tblis (ms) | vs `ttgt` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `abc-bk-akc/n1/b1` | 1.06128 ± 0.0188053 (W 0.00891145) | 2.60967 ± 0.0223045 (W 0.027997) | 1.27134 ± 0.0244932 (W 0.012415) | 🔵 tcontract 2.46× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `abcijk-eiab-jkec/n1/b1` | 4.52693 ± 0.0236534 (W 0.0117671) | 25.0783 ± 0.0976981 (W 0.21448) | 5.08298 ± 0.0409968 (W 0.0440496) | 🔵 tcontract 5.54× faster than `ttgt` | 🔵 tcontract 1.12× faster than `tblis` |  |
| `abcijk-eiac-jkeb/n1/b1` | 4.38374 ± 0.017194 (W 0.0184038) | 25.6108 ± 0.418673 (W 0.23841) | 5.531 ± 0.0657434 (W 0.0300986) | 🔵 tcontract 5.84× faster than `ttgt` | 🔵 tcontract 1.26× faster than `tblis` |  |
| `abcijk-eibc-jkea/n1/b1` | 4.63143 ± 0.0413262 (W 1.47681) | 29.9574 ± 0.700425 (W 0.175069) | 4.98591 ± 0.01545 (W 0.0136559) | 🔵 tcontract 6.47× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `abcijk-ejab-ikec/n1/b1` | 4.46119 ± 0.00850054 (W 0.00855238) | 24.9926 ± 0.229565 (W 0.232088) | 5.14304 ± 0.0318598 (W 0.030693) | 🔵 tcontract 5.60× faster than `ttgt` | 🔵 tcontract 1.15× faster than `tblis` |  |
| `abcijk-ejac-ikeb/n1/b1` | 4.38059 ± 0.0098929 (W 0.0080157) | 26.0323 ± 0.423248 (W 0.216991) | 5.18182 ± 0.0212899 (W 0.0180512) | 🔵 tcontract 5.94× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `abcijk-ejbc-ikea/n1/b1` | 4.6387 ± 0.0625071 (W 1.10161) | 29.4765 ± 0.123412 (W 0.158792) | 5.22337 ± 0.00422198 (W 0.0168497) | 🔵 tcontract 6.35× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ekab-ijec/n1/b1` | 4.46501 ± 0.00984954 (W 0.00683985) | 25.6119 ± 0.460556 (W 0.261853) | 4.94326 ± 0.00842894 (W 0.0169241) | 🔵 tcontract 5.74× faster than `ttgt` | 🔵 tcontract 1.11× faster than `tblis` |  |
| `abcijk-ekac-ijeb/n1/b1` | 4.37525 ± 0.014574 (W 0.015546) | 26.7845 ± 0.050778 (W 0.207577) | 5.24262 ± 0.00824112 (W 0.028223) | 🔵 tcontract 6.12× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `abcijk-ekbc-ijea/n1/b1` | 4.59394 ± 1.75238 (W 0.388008) | 31.4087 ± 0.407826 (W 0.157877) | 5.24308 ± 0.0177456 (W 0.0180289) | 🔵 tcontract 6.84× faster than `ttgt` | · | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-ijma-mkbc/n1/b1` | 4.63373 ± 0.414765 (W 1.52903) | 51.4017 ± 0.159013 (W 0.174348) | 5.22137 ± 0.0141824 (W 0.0125817) | 🔵 tcontract 11.09× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-ijmb-mkac/n1/b1` | 4.38676 ± 0.0122481 (W 0.018253) | 52.9985 ± 0.331495 (W 0.384373) | 5.2478 ± 0.0052352 (W 0.0202619) | 🔵 tcontract 12.08× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `abcijk-ijmc-mkab/n1/b1` | 4.47235 ± 0.04126 (W 0.0660971) | 63.2983 ± 0.326563 (W 0.192484) | 4.96423 ± 0.00762844 (W 0.0253088) | 🔵 tcontract 14.15× faster than `ttgt` | 🔵 tcontract 1.11× faster than `tblis` |  |
| `abcijk-ikma-mjbc/n1/b1` | 4.61449 ± 0.0480204 (W 0.0291646) | 55.4111 ± 0.337458 (W 0.200125) | 5.22472 ± 0.00504221 (W 0.0321666) | 🔵 tcontract 12.01× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ikmb-mjac/n1/b1` | 4.41581 ± 0.0504824 (W 0.444922) | 54.8444 ± 0.656715 (W 0.243519) | 5.17247 ± 0.0231883 (W 0.0217037) | 🔵 tcontract 12.42× faster than `ttgt` | 🔵 tcontract 1.17× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 4.46446 ± 0.02082 (W 0.0572314) | 65.2358 ± 0.596095 (W 0.184369) | 5.1398 ± 0.0391311 (W 0.0312683) | 🔵 tcontract 14.61× faster than `ttgt` | 🔵 tcontract 1.15× faster than `tblis` |  |
| `abcijk-jkma-mibc/n1/b1` | 4.61676 ± 0.345422 (W 0.270185) | 94.4971 ± 5.73111 (W 0.223566) | 4.98047 ± 0.00408027 (W 0.0114053) | 🔵 tcontract 20.47× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-jkmb-miac/n1/b1` | 4.44723 ± 0.0453967 (W 0.0241609) | 93.3207 ± 9.42587 (W 0.252649) | 5.52313 ± 0.108975 (W 0.0163123) | 🔵 tcontract 20.98× faster than `ttgt` | 🔵 tcontract 1.24× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmc-miab/n1/b1` | 4.49227 ± 0.0251367 (W 0.00429939) | 98.0562 ± 4.14254 (W 0.169711) | 5.08553 ± 0.0629162 (W 0.0293535) | 🔵 tcontract 21.83× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` | `!` between-start range over 5% |
| `abcs-rc-abrs/n1/b1` | 0.483105 ± 0.00136557 (W 0.00417554) | 1.48985 ± 0.00478983 (W 0.0171732) | 0.71114 ± 0.0124279 (W 0.014174) | 🔵 tcontract 3.08× faster than `ttgt` | 🔵 tcontract 1.47× faster than `tblis` |  |
| `abj-bka-kj/n1/b1` | 1.65264 ± 0.0178495 (W 0.00998123) | 3.5552 ± 0.00733854 (W 0.0112786) | 2.30737 ± 0.0211645 (W 0.0112714) | 🔵 tcontract 2.15× faster than `ttgt` | 🔵 tcontract 1.40× faster than `tblis` |  |
| `abjc-cbka-kj/n1/b1` | 0.855828 ± 0.00771998 (W 0.00655505) | 2.06436 ± 0.0320646 (W 0.0297338) | 0.905037 ± 0.0450573 (W 0.0401064) | 🔵 tcontract 2.41× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` | `!` between-start range over 5% |
| `abjc-kbac-jk/n1/b1` | 0.516139 ± 0.00220724 (W 0.00179997) | 2.03337 ± 0.0353362 (W 0.010791) | 0.776731 ± 0.0125576 (W 0.0123927) | 🔵 tcontract 3.94× faster than `ttgt` | 🔵 tcontract 1.50× faster than `tblis` |  |
| `abjcd-dkbac-jk/n1/b1` | 3.86884 ± 0.024156 (W 0.0263289) | 22.5219 ± 1.00098 (W 0.128381) | 5.21054 ± 0.0460548 (W 0.045895) | 🔵 tcontract 5.82× faster than `ttgt` | 🔵 tcontract 1.35× faster than `tblis` | `!` between-start range over 5% |
| `abrs-qb-aqrs/n1/b1` | 0.426732 ± 0.00153929 (W 0.00192662) | 1.46067 ± 0.0458994 (W 0.0274359) | 0.730646 ± 0.00927763 (W 0.00933892) | 🔵 tcontract 3.42× faster than `ttgt` | 🔵 tcontract 1.71× faster than `tblis` | `!` between-start range over 5% |
| `adbjc-cbdka-kj/n1/b1` | 8.09107 ± 0.0452809 (W 0.130375) | 15.9819 ± 0.126195 (W 0.032426) | 7.35091 ± 0.113297 (W 0.118694) | 🔵 tcontract 1.98× faster than `ttgt` | 🔴 tcontract 1.10× slower than `tblis` |  |
| `ajb-kba-jk/n1/b1` | 1.49089 ± 0.0137896 (W 0.398846) | 3.49434 ± 0.00228556 (W 0.0197808) | 1.89142 ± 0.0227843 (W 0.0215525) | 🔵 tcontract 2.34× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `ajbc-ckba-jk/n1/b1` | 0.626472 ± 0.0179393 (W 0.00571845) | 4.17531 ± 0.0329215 (W 0.0160265) | 0.926277 ± 0.0125969 (W 0.011856) | 🔵 tcontract 6.66× faster than `ttgt` | 🔵 tcontract 1.48× faster than `tblis` | `!` between-start range over 5% |
| `ajbdc-ckbad-jk/n1/b1` | 3.73429 ± 0.0164849 (W 0.0445223) | 27.9003 ± 0.209547 (W 0.0866049) | 5.14154 ± 0.0282288 (W 0.0357834) | 🔵 tcontract 7.47× faster than `ttgt` | 🔵 tcontract 1.38× faster than `tblis` |  |
| `aqrs-pa-pqrs/n1/b1` | 0.638605 ± 0.00487083 (W 0.0149765) | 1.0694 ± 0.0106391 (W 0.00774805) | 0.660014 ± 0.00364148 (W 0.00319905) | 🔵 tcontract 1.67× faster than `ttgt` | · |  |
| `ij-ik-kj/n1/b1` | 3.71614 ± 0.00813434 (W 0.00664209) | 4.90521 ± 0.0236972 (W 0.00497787) | 4.03727 ± 0.00679195 (W 0.00937946) | 🔵 tcontract 1.32× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `ij-ikl-ljk/n1/b1` | 2.10187 ± 0.00270139 (W 0.00797502) | 2.22206 ± 0.01713 (W 0.0108829) | 1.69163 ± 0.0038202 (W 0.00554314) | 🔵 tcontract 1.06× faster than `ttgt` | 🔴 tcontract 1.24× slower than `tblis` |  |
| `ij-kil-lkj/n1/b1` | 3.21636 ± 0.0326549 (W 0.0447273) | 3.57372 ± 0.0512783 (W 0.0113479) | 2.42156 ± 0.0717028 (W 0.0565326) | 🔵 tcontract 1.11× faster than `ttgt` | 🔴 tcontract 1.33× slower than `tblis` | `!` between-start range over 5% |
| `ijk-ikl-lj/n1/b1` | 1.10168 ± 0.0115483 (W 0.488856) | 2.01224 ± 0.013435 (W 0.0187351) | 1.42296 ± 0.00795125 (W 0.00959996) | 🔵 tcontract 1.83× faster than `ttgt` | 🔵 tcontract 1.29× faster than `tblis` |  |
| `ijk-il-jlk/n1/b1` | 1.93941 ± 0.11393 (W 0.0998056) | 2.49009 ± 0.00978884 (W 0.0192823) | 1.22884 ± 0.0064201 (W 0.00664635) | 🔵 tcontract 1.28× faster than `ttgt` | 🔴 tcontract 1.58× slower than `tblis` | `!` between-start range over 5% |
| `ijk-ilk-jl/n1/b1` | 1.04965 ± 0.0171099 (W 0.00933467) | 2.50798 ± 0.0241118 (W 0.010195) | 1.27226 ± 0.0203945 (W 0.0102134) | 🔵 tcontract 2.39× faster than `ttgt` | 🔵 tcontract 1.21× faster than `tblis` |  |
| `ijk-ilk-lj/n1/b1` | 1.08066 ± 0.0316589 (W 0.0122031) | 2.52533 ± 0.0277027 (W 0.00654886) | 1.44165 ± 0.0501059 (W 0.0101447) | 🔵 tcontract 2.34× faster than `ttgt` | 🔵 tcontract 1.33× faster than `tblis` | `!` between-start range over 5% |
| `ijk-ilmk-mjl/n1/b1` | 0.466164 ± 0.00325342 (W 0.00339409) | 0.847262 ± 0.00311812 (W 0.00293293) | 0.546112 ± 0.0019434 (W 0.00418766) | 🔵 tcontract 1.82× faster than `ttgt` | 🔵 tcontract 1.17× faster than `tblis` |  |
| `ijkl-imjn-lnkm/n1/b1` | 7.0009 ± 1.7522 (W 1.71938) | 8.83702 ± 0.050081 (W 0.0269548) | 7.03167 ± 0.0765723 (W 0.0154662) | · | · | `!` between-start range over 5%; `p` position effect over 5% |
| `ijkl-imjn-nlmk/n1/b1` | 6.97318 ± 0.0466765 (W 1.37876) | 8.80999 ± 0.0637595 (W 0.0401371) | 7.18449 ± 0.106495 (W 0.0100507) | 🔵 tcontract 1.26× faster than `ttgt` | · |  |
| `ijkl-imkn-jnlm/n1/b1` | 6.91262 ± 0.0438739 (W 0.0582541) | 8.83159 ± 0.0111963 (W 0.040821) | 7.07368 ± 0.0515034 (W 0.0221901) | 🔵 tcontract 1.28× faster than `ttgt` | · |  |
| `ijkl-imkn-njml/n1/b1` | 6.88129 ± 0.0488491 (W 1.36797) | 8.80536 ± 0.0258053 (W 0.0105384) | 7.12856 ± 0.0337978 (W 0.0141353) | 🔵 tcontract 1.28× faster than `ttgt` | · |  |
| `ijkl-imln-jnkm/n1/b1` | 6.85614 ± 0.0269041 (W 0.0656714) | 8.82611 ± 0.0531005 (W 0.0265548) | 7.08526 ± 0.0499351 (W 0.0122173) | 🔵 tcontract 1.29× faster than `ttgt` | · |  |
| `ijkl-imln-njmk/n1/b1` | 6.84903 ± 1.69912 (W 0.268099) | 8.74741 ± 0.0381305 (W 0.0107499) | 7.0631 ± 0.0279084 (W 0.014294) | · | · | `!` between-start range over 5%; `p` position effect over 5% |
| `ijkl-imnj-nlkm/n1/b1` | 6.88253 ± 0.0171369 (W 0.0587557) | 8.53002 ± 0.0191866 (W 0.022061) | 7.07942 ± 0.0964772 (W 0.012659) | 🔵 tcontract 1.24× faster than `ttgt` | · |  |
| `ijkl-imnk-njml/n1/b1` | 6.86327 ± 0.00740794 (W 1.39123) | 8.62762 ± 0.0192576 (W 0.0336499) | 7.06713 ± 0.0687701 (W 0.0155882) | 🔵 tcontract 1.26× faster than `ttgt` | · |  |
| `ijkl-minj-nlmk/n1/b1` | 8.46281 ± 0.107199 (W 0.0181336) | 10.4068 ± 0.048554 (W 0.0128381) | 8.69618 ± 0.0827295 (W 0.0233784) | 🔵 tcontract 1.23× faster than `ttgt` | · |  |
| `ijkl-mink-jnlm/n1/b1` | 8.25911 ± 2.00691 (W 1.14242) | 10.5008 ± 0.0547408 (W 0.0244029) | 8.48695 ± 0.327046 (W 0.0192838) | · | · | `!` between-start range over 5%; `p` position effect over 5% |
| `ijkl-minl-njmk/n1/b1` | 8.41427 ± 0.0551723 (W 1.18604) | 10.4839 ± 0.052422 (W 0.0359228) | 8.51244 ± 0.044907 (W 0.0178335) | 🔵 tcontract 1.25× faster than `ttgt` | · |  |

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
