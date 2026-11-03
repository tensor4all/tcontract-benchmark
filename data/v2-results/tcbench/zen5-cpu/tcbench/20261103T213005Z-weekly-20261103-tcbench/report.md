# `tcbench` on `zen5-cpu`

- tcontract-rs commit: `9f793ede6b8076fd7ce2251594a9552ad66aa339`
- features: `blas, tblis`
- tprims rows: `tprims` (the provider in the measured revision; see library above); `openblas` (the provider in the measured revision; see library above)
- external providers: `tblis` 2.0 @ `b16a732939d8454021e0a0f0097cf1cc1dd3ab19` tag `v2.0-beta2` sha256 `de00bf1552c15f9c4a5d3157f02c149b81aef0909107c51cbb54ba4b8e9b5827` (TBLIS 2.0, configuration zen3; bundled BLIS 358e689cadd6757f564a2992cf46a2f7d6fa6bb0; built with ./configure --prefix=/home/shinaoka/projects/tensor4all/tcontract-benchmark/target/tblis-v2.0-beta2 --with-blis-config-family=zen3 (cmake, Unix Makefiles, Release); libtblis.so sha256 de00bf1552c15f9c)
- harness commit: `152315f3bad3a68bf4f99f63e2be5ddc83421673`
- toolkit commit: `74e50e8199cb2c2f07e810744a0943fc3a8c1170`
- measured binary SHA-256: `81a1fe3ea90fe4e232eb039ed5d4206a345fbb8eda3959e3df263054b0d61f96`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-11-03T21:40:56.607712Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/v2/record_run.py tcbench zen5-cpu tcbench --aa 3 --reps 5 --prime-ms 250 --external-provider-json /home/shinaoka/.local/state/tensor4all-weekly/20261103/tcontract/tblis-providers.json --label weekly-20261103-tcbench --no-publish`
- raw data: `data/v2-results/tcbench/zen5-cpu/tcbench/20261103T213005Z-weekly-20261103-tcbench/`

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
Spread guide (computed from this run's own rows): per-engine between-start range median 1.00%, worst 73.16% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 28 of 588 engine cells exceed 5% and carry `!`; median within-process relative SD 0.31%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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
| `abc-bk-akc/n1/b1` | 1.01699 ± 0.00461456 (W 0.00138847) | 1.97764 ± 0.0262906 (W 0.00867731) | 1.50349 ± 0.0119666 (W 0.00592573) | 🔵 tcontract 1.94× faster than `ttgt` | 🔵 tcontract 1.48× faster than `tblis` |  |
| `abcijk-eiab-jkec/n1/b1` | 4.50152 ± 0.022696 (W 0.00993954) | 8.80939 ± 0.0648046 (W 0.0343271) | 5.45222 ± 0.0798939 (W 0.0276593) | 🔵 tcontract 1.96× faster than `ttgt` | 🔵 tcontract 1.21× faster than `tblis` |  |
| `abcijk-eiac-jkeb/n1/b1` | 4.31643 ± 0.00875882 (W 0.0216128) | 10.013 ± 0.0368875 (W 0.0428404) | 6.77075 ± 0.171979 (W 0.0212848) | 🔵 tcontract 2.32× faster than `ttgt` | 🔵 tcontract 1.57× faster than `tblis` |  |
| `abcijk-eibc-jkea/n1/b1` | 4.56453 ± 0.00787047 (W 0.00754094) | 11.6212 ± 0.0421256 (W 0.0740453) | 5.40203 ± 0.0455366 (W 0.0133741) | 🔵 tcontract 2.55× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `abcijk-ejab-ikec/n1/b1` | 4.45096 ± 0.0142583 (W 0.0103174) | 8.8401 ± 0.0271066 (W 0.00678719) | 5.41633 ± 0.063263 (W 0.0243921) | 🔵 tcontract 1.99× faster than `ttgt` | 🔵 tcontract 1.22× faster than `tblis` |  |
| `abcijk-ejac-ikeb/n1/b1` | 4.30379 ± 0.00734582 (W 0.00671969) | 10.0987 ± 0.0732572 (W 0.0223066) | 5.64737 ± 0.0690095 (W 0.0149859) | 🔵 tcontract 2.35× faster than `ttgt` | 🔵 tcontract 1.31× faster than `tblis` |  |
| `abcijk-ejbc-ikea/n1/b1` | 4.57311 ± 0.00744349 (W 0.00514874) | 11.603 ± 0.295519 (W 0.137059) | 5.69292 ± 0.0178761 (W 0.0158467) | 🔵 tcontract 2.54× faster than `ttgt` | 🔵 tcontract 1.24× faster than `tblis` |  |
| `abcijk-ekab-ijec/n1/b1` | 4.44467 ± 0.0200391 (W 0.00968233) | 9.1959 ± 0.0614863 (W 0.0207757) | 5.23571 ± 0.0662354 (W 0.020743) | 🔵 tcontract 2.07× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `abcijk-ekac-ijeb/n1/b1` | 4.30253 ± 0.00955702 (W 0.00704757) | 10.9538 ± 0.0317042 (W 0.0485887) | 5.86046 ± 0.00917023 (W 0.0176492) | 🔵 tcontract 2.55× faster than `ttgt` | 🔵 tcontract 1.36× faster than `tblis` |  |
| `abcijk-ekbc-ijea/n1/b1` | 4.55671 ± 0.0195762 (W 0.00801559) | 12.0516 ± 0.179674 (W 0.0516946) | 5.68075 ± 0.0242958 (W 0.0192886) | 🔵 tcontract 2.64× faster than `ttgt` | 🔵 tcontract 1.25× faster than `tblis` |  |
| `abcijk-ijma-mkbc/n1/b1` | 4.54621 ± 0.00755618 (W 0.0096012) | 38.4542 ± 0.124115 (W 0.0348561) | 5.69454 ± 0.0334512 (W 0.0207316) | 🔵 tcontract 8.46× faster than `ttgt` | 🔵 tcontract 1.25× faster than `tblis` |  |
| `abcijk-ijmb-mkac/n1/b1` | 4.29725 ± 0.0160194 (W 0.0136641) | 35.9752 ± 0.224935 (W 0.0705179) | 5.85995 ± 0.0189445 (W 0.031417) | 🔵 tcontract 8.37× faster than `ttgt` | 🔵 tcontract 1.36× faster than `tblis` |  |
| `abcijk-ijmc-mkab/n1/b1` | 4.44551 ± 0.00781531 (W 0.00948151) | 37.1911 ± 0.0627228 (W 0.160528) | 5.23186 ± 0.0255865 (W 0.00974991) | 🔵 tcontract 8.37× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `abcijk-ikma-mjbc/n1/b1` | 4.56116 ± 0.0102053 (W 0.0107571) | 43.1889 ± 0.544169 (W 0.0642021) | 5.68302 ± 0.0262631 (W 0.018852) | 🔵 tcontract 9.47× faster than `ttgt` | 🔵 tcontract 1.25× faster than `tblis` |  |
| `abcijk-ikmb-mjac/n1/b1` | 4.30882 ± 0.0149396 (W 0.00610965) | 38.5725 ± 0.220001 (W 0.0733169) | 5.60641 ± 0.0776897 (W 0.0179735) | 🔵 tcontract 8.95× faster than `ttgt` | 🔵 tcontract 1.30× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 4.44633 ± 0.0101426 (W 0.00788227) | 39.9616 ± 0.399187 (W 0.130425) | 5.41856 ± 0.0611872 (W 0.0232386) | 🔵 tcontract 8.99× faster than `ttgt` | 🔵 tcontract 1.22× faster than `tblis` |  |
| `abcijk-jkma-mibc/n1/b1` | 4.55383 ± 0.0114606 (W 0.00764153) | 125.684 ± 25.9002 (W 0.0855398) | 5.35467 ± 0.0259386 (W 0.0138978) | 🔵 tcontract 27.60× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmb-miac/n1/b1` | 4.30104 ± 0.0131703 (W 0.00527546) | 100.638 ± 10.6209 (W 0.0745382) | 6.74109 ± 0.148426 (W 0.044168) | 🔵 tcontract 23.40× faster than `ttgt` | 🔵 tcontract 1.57× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmc-miab/n1/b1` | 4.49403 ± 0.0146326 (W 0.00966795) | 102.644 ± 11.3048 (W 0.129541) | 5.48243 ± 0.0618637 (W 0.0211014) | 🔵 tcontract 22.84× faster than `ttgt` | 🔵 tcontract 1.22× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcs-rc-abrs/n1/b1` | 0.481326 ± 0.00271707 (W 0.00308156) | 1.14853 ± 0.0182477 (W 0.00467317) | 1.15152 ± 0.00982012 (W 0.00510472) | 🔵 tcontract 2.39× faster than `ttgt` | 🔵 tcontract 2.39× faster than `tblis` |  |
| `abj-bka-kj/n1/b1` | 2.49515 ± 0.0414137 (W 0.021053) | 2.70742 ± 0.0305249 (W 0.0197315) | 2.62472 ± 0.0165161 (W 0.00660723) | 🔵 tcontract 1.09× faster than `ttgt` | 🔵 tcontract 1.05× faster than `tblis` |  |
| `abjc-cbka-kj/n1/b1` | 1.53903 ± 0.0118718 (W 0.0160857) | 1.2136 ± 0.00506921 (W 0.00897382) | 1.39734 ± 0.0179974 (W 0.00572138) | 🔴 tcontract 1.27× slower than `ttgt` | 🔴 tcontract 1.10× slower than `tblis` |  |
| `abjc-kbac-jk/n1/b1` | 0.541788 ± 0.00118704 (W 0.00323137) | 1.20833 ± 0.0160449 (W 0.00630424) | 1.14752 ± 0.0090389 (W 0.00568434) | 🔵 tcontract 2.23× faster than `ttgt` | 🔵 tcontract 2.12× faster than `tblis` |  |
| `abjcd-dkbac-jk/n1/b1` | 4.27471 ± 0.000953945 (W 0.00638258) | 18.0249 ± 0.486492 (W 0.0590492) | 8.20574 ± 0.043739 (W 0.0497542) | 🔵 tcontract 4.22× faster than `ttgt` | 🔵 tcontract 1.92× faster than `tblis` | `!` between-start range over 5% |
| `abrs-qb-aqrs/n1/b1` | 0.472089 ± 0.00181986 (W 0.00236707) | 1.08707 ± 0.00797463 (W 0.00324797) | 1.15196 ± 0.00711837 (W 0.00662614) | 🔵 tcontract 2.30× faster than `ttgt` | 🔵 tcontract 2.44× faster than `tblis` |  |
| `adbjc-cbdka-kj/n1/b1` | 10.5638 ± 0.185433 (W 0.0478785) | 11.877 ± 0.143156 (W 0.0357812) | 9.80954 ± 0.263802 (W 0.0845337) | 🔵 tcontract 1.12× faster than `ttgt` | 🔴 tcontract 1.08× slower than `tblis` |  |
| `ajb-kba-jk/n1/b1` | 1.43205 ± 0.00474039 (W 0.00279102) | 2.37457 ± 0.00806221 (W 0.0123125) | 2.07851 ± 0.0215088 (W 0.0149921) | 🔵 tcontract 1.66× faster than `ttgt` | 🔵 tcontract 1.45× faster than `tblis` |  |
| `ajbc-ckba-jk/n1/b1` | 0.733636 ± 0.0150317 (W 0.00171639) | 3.65838 ± 0.029307 (W 0.0220814) | 1.19818 ± 0.0172091 (W 0.00837966) | 🔵 tcontract 4.99× faster than `ttgt` | 🔵 tcontract 1.63× faster than `tblis` |  |
| `ajbdc-ckbad-jk/n1/b1` | 4.10969 ± 0.0511992 (W 0.0137675) | 23.8293 ± 0.354312 (W 0.0699582) | 7.82008 ± 0.0163523 (W 0.0271317) | 🔵 tcontract 5.80× faster than `ttgt` | 🔵 tcontract 1.90× faster than `tblis` |  |
| `aqrs-pa-pqrs/n1/b1` | 0.502636 ± 0.00204859 (W 0.00318326) | 1.00163 ± 0.00839778 (W 0.00167124) | 1.08156 ± 0.00252484 (W 0.00711646) | 🔵 tcontract 1.99× faster than `ttgt` | 🔵 tcontract 2.15× faster than `tblis` |  |
| `ij-ik-kj/n1/b1` | 3.55868 ± 0.00469287 (W 0.00836553) | 4.6209 ± 0.0342199 (W 0.0063289) | 4.27975 ± 0.0149076 (W 0.00743633) | 🔵 tcontract 1.30× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `ij-ikl-ljk/n1/b1` | 1.22188 ± 0.00350052 (W 0.00235802) | 1.82404 ± 0.0244906 (W 0.0116041) | 2.13551 ± 0.00620699 (W 0.0069649) | 🔵 tcontract 1.49× faster than `ttgt` | 🔵 tcontract 1.75× faster than `tblis` |  |
| `ij-kil-lkj/n1/b1` | 1.79995 ± 0.0198708 (W 0.00483399) | 2.86456 ± 0.0601444 (W 0.00927041) | 3.00762 ± 0.0265912 (W 0.00881701) | 🔵 tcontract 1.59× faster than `ttgt` | 🔵 tcontract 1.67× faster than `tblis` |  |
| `ijk-ikl-lj/n1/b1` | 1.08837 ± 0.000663286 (W 0.00184463) | 1.63262 ± 0.0082625 (W 0.00464216) | 1.71402 ± 0.00821725 (W 0.00269709) | 🔵 tcontract 1.50× faster than `ttgt` | 🔵 tcontract 1.57× faster than `tblis` |  |
| `ijk-il-jlk/n1/b1` | 1.06025 ± 0.00637992 (W 0.00157606) | 1.89847 ± 0.0111041 (W 0.00737135) | 1.58516 ± 0.0114429 (W 0.00530566) | 🔵 tcontract 1.79× faster than `ttgt` | 🔵 tcontract 1.50× faster than `tblis` |  |
| `ijk-ilk-jl/n1/b1` | 1.01178 ± 0.00469638 (W 0.00302863) | 1.74055 ± 0.00853592 (W 0.0317337) | 1.52047 ± 0.00882121 (W 0.00392818) | 🔵 tcontract 1.72× faster than `ttgt` | 🔵 tcontract 1.50× faster than `tblis` |  |
| `ijk-ilk-lj/n1/b1` | 1.08455 ± 0.0176174 (W 0.00312291) | 1.74684 ± 0.0312568 (W 0.013028) | 1.70164 ± 0.00284324 (W 0.00406971) | 🔵 tcontract 1.61× faster than `ttgt` | 🔵 tcontract 1.57× faster than `tblis` |  |
| `ijk-ilmk-mjl/n1/b1` | 0.433197 ± 0.00241206 (W 0.0022143) | 0.677431 ± 0.00380189 (W 0.00233808) | 0.96156 ± 0.00309815 (W 0.00759459) | 🔵 tcontract 1.56× faster than `ttgt` | 🔵 tcontract 2.22× faster than `tblis` |  |
| `ijkl-imjn-lnkm/n1/b1` | 6.24917 ± 0.0392136 (W 0.0115282) | 7.97264 ± 0.0065709 (W 0.00932124) | 7.61361 ± 0.0589918 (W 0.0412721) | 🔵 tcontract 1.28× faster than `ttgt` | 🔵 tcontract 1.22× faster than `tblis` |  |
| `ijkl-imjn-nlmk/n1/b1` | 6.18085 ± 0.0572172 (W 0.0557558) | 7.96794 ± 0.00923953 (W 0.00869685) | 7.50969 ± 0.0348178 (W 0.0236443) | 🔵 tcontract 1.29× faster than `ttgt` | 🔵 tcontract 1.21× faster than `tblis` |  |
| `ijkl-imkn-jnlm/n1/b1` | 6.17158 ± 0.0494104 (W 0.00956009) | 7.93966 ± 0.0231775 (W 0.0103922) | 7.28526 ± 0.0589838 (W 0.0195982) | 🔵 tcontract 1.29× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `ijkl-imkn-njml/n1/b1` | 6.17832 ± 0.0135125 (W 0.00597688) | 7.96766 ± 0.0163833 (W 0.0158444) | 7.48528 ± 0.140654 (W 0.0268686) | 🔵 tcontract 1.29× faster than `ttgt` | 🔵 tcontract 1.21× faster than `tblis` |  |
| `ijkl-imln-jnkm/n1/b1` | 6.19485 ± 0.0277772 (W 0.0141343) | 7.96184 ± 0.0242984 (W 0.0114413) | 7.23513 ± 0.041289 (W 0.03593) | 🔵 tcontract 1.29× faster than `ttgt` | 🔵 tcontract 1.17× faster than `tblis` |  |
| `ijkl-imln-njmk/n1/b1` | 6.1906 ± 0.0187099 (W 0.0168687) | 8.00189 ± 0.0261897 (W 0.0108809) | 7.31291 ± 0.12886 (W 0.0217787) | 🔵 tcontract 1.29× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `ijkl-imnj-nlkm/n1/b1` | 6.19827 ± 0.0325893 (W 0.010654) | 7.94184 ± 0.0317641 (W 0.0108685) | 7.35261 ± 0.0666714 (W 0.015482) | 🔵 tcontract 1.28× faster than `ttgt` | 🔵 tcontract 1.19× faster than `tblis` |  |
| `ijkl-imnk-njml/n1/b1` | 6.16235 ± 0.0293527 (W 0.00573625) | 7.94857 ± 0.0999528 (W 0.0149276) | 7.24411 ± 0.0703355 (W 0.00780502) | 🔵 tcontract 1.29× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `ijkl-minj-nlmk/n1/b1` | 7.60319 ± 0.0353092 (W 0.0097993) | 9.64227 ± 0.0427968 (W 0.00854953) | 9.04807 ± 0.0163029 (W 0.0322117) | 🔵 tcontract 1.27× faster than `ttgt` | 🔵 tcontract 1.19× faster than `tblis` |  |
| `ijkl-mink-jnlm/n1/b1` | 7.47489 ± 0.0177572 (W 0.0147498) | 9.5199 ± 0.0292543 (W 0.0144823) | 8.62691 ± 0.0833223 (W 0.0225291) | 🔵 tcontract 1.27× faster than `ttgt` | 🔵 tcontract 1.15× faster than `tblis` |  |
| `ijkl-minl-njmk/n1/b1` | 7.55268 ± 0.0374013 (W 0.0100858) | 9.6214 ± 0.0331375 (W 0.0157291) | 8.82037 ± 0.116504 (W 0.0189424) | 🔵 tcontract 1.27× faster than `ttgt` | 🔵 tcontract 1.17× faster than `tblis` |  |

## tcbench, f64, 4T (CPU 4-7)

| case | plan (ms) | ttgt (ms) | tblis (ms) | vs `ttgt` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `abc-bk-akc/n1/b1` | 0.267628 ± 0.000951574 (W 0.0019773) | 1.22264 ± 0.0137153 (W 0.012352) | 0.426814 ± 0.00305227 (W 0.00437792) | 🔵 tcontract 4.57× faster than `ttgt` | 🔵 tcontract 1.59× faster than `tblis` |  |
| `abcijk-eiab-jkec/n1/b1` | 1.17151 ± 0.00391049 (W 0.00416103) | 5.6773 ± 0.0468946 (W 0.0259254) | 1.73294 ± 0.0797143 (W 0.0309328) | 🔵 tcontract 4.85× faster than `ttgt` | 🔵 tcontract 1.48× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-eiac-jkeb/n1/b1` | 1.09862 ± 0.00884252 (W 0.00199122) | 6.87077 ± 0.0273485 (W 0.0227537) | 2.22803 ± 0.064687 (W 0.0418712) | 🔵 tcontract 6.25× faster than `ttgt` | 🔵 tcontract 2.03× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-eibc-jkea/n1/b1` | 1.17345 ± 0.00498755 (W 0.00970696) | 8.60774 ± 0.142314 (W 0.0320021) | 1.4572 ± 0.00175334 (W 0.00655705) | 🔵 tcontract 7.34× faster than `ttgt` | 🔵 tcontract 1.24× faster than `tblis` |  |
| `abcijk-ejab-ikec/n1/b1` | 1.13935 ± 0.00522196 (W 0.00470612) | 5.71649 ± 0.0116899 (W 0.0232469) | 1.66718 ± 0.0297513 (W 0.0298715) | 🔵 tcontract 5.02× faster than `ttgt` | 🔵 tcontract 1.46× faster than `tblis` |  |
| `abcijk-ejac-ikeb/n1/b1` | 1.09269 ± 0.00458354 (W 0.0041148) | 7.01164 ± 0.0510129 (W 0.0419417) | 1.54549 ± 0.01069 (W 0.0176837) | 🔵 tcontract 6.42× faster than `ttgt` | 🔵 tcontract 1.41× faster than `tblis` |  |
| `abcijk-ejbc-ikea/n1/b1` | 1.17499 ± 0.00459889 (W 0.00636826) | 8.57501 ± 0.0347538 (W 0.0997555) | 1.52952 ± 0.00800375 (W 0.0095282) | 🔵 tcontract 7.30× faster than `ttgt` | 🔵 tcontract 1.30× faster than `tblis` |  |
| `abcijk-ekab-ijec/n1/b1` | 1.1423 ± 0.00526173 (W 0.00628708) | 6.07263 ± 0.0695237 (W 0.0130801) | 1.42808 ± 0.0548097 (W 0.0264444) | 🔵 tcontract 5.32× faster than `ttgt` | 🔵 tcontract 1.25× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ekac-ijeb/n1/b1` | 1.09295 ± 0.00373573 (W 0.00276907) | 7.76617 ± 0.0195006 (W 0.0384376) | 2.09114 ± 0.0236444 (W 0.0430492) | 🔵 tcontract 7.11× faster than `ttgt` | 🔵 tcontract 1.91× faster than `tblis` |  |
| `abcijk-ekbc-ijea/n1/b1` | 1.17083 ± 0.00307728 (W 0.00473942) | 9.15429 ± 0.0647805 (W 0.0570817) | 1.535 ± 0.00213389 (W 0.00617449) | 🔵 tcontract 7.82× faster than `ttgt` | 🔵 tcontract 1.31× faster than `tblis` |  |
| `abcijk-ijma-mkbc/n1/b1` | 1.17377 ± 0.00748844 (W 0.00427849) | 35.512 ± 0.219597 (W 0.0393304) | 1.52759 ± 0.00705426 (W 0.0113944) | 🔵 tcontract 30.25× faster than `ttgt` | 🔵 tcontract 1.30× faster than `tblis` |  |
| `abcijk-ijmb-mkac/n1/b1` | 1.08981 ± 0.0067882 (W 0.00399464) | 33.0557 ± 0.160905 (W 0.0723366) | 2.05483 ± 0.050693 (W 0.0349772) | 🔵 tcontract 30.33× faster than `ttgt` | 🔵 tcontract 1.89× faster than `tblis` |  |
| `abcijk-ijmc-mkab/n1/b1` | 1.13631 ± 0.00518347 (W 0.00540526) | 33.9621 ± 0.16896 (W 0.196477) | 1.48412 ± 0.0177252 (W 0.0396357) | 🔵 tcontract 29.89× faster than `ttgt` | 🔵 tcontract 1.31× faster than `tblis` |  |
| `abcijk-ikma-mjbc/n1/b1` | 1.17741 ± 0.00888725 (W 0.00413118) | 40.28 ± 0.203121 (W 0.0730526) | 1.53677 ± 0.0193051 (W 0.0139473) | 🔵 tcontract 34.21× faster than `ttgt` | 🔵 tcontract 1.31× faster than `tblis` |  |
| `abcijk-ikmb-mjac/n1/b1` | 1.09159 ± 0.0091436 (W 0.00277583) | 35.5959 ± 0.145586 (W 0.355982) | 1.53368 ± 0.00974619 (W 0.00760686) | 🔵 tcontract 32.61× faster than `ttgt` | 🔵 tcontract 1.40× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 1.13716 ± 0.00395799 (W 0.00447557) | 36.6786 ± 0.110659 (W 0.025029) | 1.68164 ± 0.0400547 (W 0.0321706) | 🔵 tcontract 32.25× faster than `ttgt` | 🔵 tcontract 1.48× faster than `tblis` |  |
| `abcijk-jkma-mibc/n1/b1` | 1.17377 ± 0.0109438 (W 0.00347594) | 124.095 ± 0.777561 (W 0.0794786) | 1.44327 ± 0.00634202 (W 0.00898779) | 🔵 tcontract 105.72× faster than `ttgt` | 🔵 tcontract 1.23× faster than `tblis` |  |
| `abcijk-jkmb-miac/n1/b1` | 1.09578 ± 0.00460829 (W 0.00121302) | 97.3775 ± 0.91969 (W 0.144063) | 2.21338 ± 0.0923871 (W 0.0301794) | 🔵 tcontract 88.87× faster than `ttgt` | 🔵 tcontract 2.02× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-jkmc-miab/n1/b1` | 1.16368 ± 0.00527857 (W 0.00553791) | 99.5114 ± 2.35118 (W 0.134516) | 1.71096 ± 0.0469148 (W 0.0423351) | 🔵 tcontract 85.51× faster than `ttgt` | 🔵 tcontract 1.47× faster than `tblis` | `!` between-start range over 5% |
| `abcs-rc-abrs/n1/b1` | 0.136514 ± 0.000161929 (W 0.00198257) | 0.750558 ± 0.0182162 (W 0.00387966) | 0.374648 ± 0.00269533 (W 0.00432467) | 🔵 tcontract 5.50× faster than `ttgt` | 🔵 tcontract 2.74× faster than `tblis` |  |
| `abj-bka-kj/n1/b1` | 0.484232 ± 0.00591937 (W 0.00248313) | 1.42415 ± 0.0122909 (W 0.0106625) | 0.716945 ± 0.00243187 (W 0.00719555) | 🔵 tcontract 2.94× faster than `ttgt` | 🔵 tcontract 1.48× faster than `tblis` |  |
| `abjc-cbka-kj/n1/b1` | 0.27911 ± 0.00355747 (W 0.00193436) | 0.790572 ± 0.00423591 (W 0.00295804) | 0.459766 ± 0.00557084 (W 0.00704044) | 🔵 tcontract 2.83× faster than `ttgt` | 🔵 tcontract 1.65× faster than `tblis` |  |
| `abjc-kbac-jk/n1/b1` | 0.152544 ± 0.000390309 (W 0.00269609) | 0.841217 ± 0.0216485 (W 0.005259) | 0.38165 ± 0.00260838 (W 0.00600395) | 🔵 tcontract 5.51× faster than `ttgt` | 🔵 tcontract 2.50× faster than `tblis` |  |
| `abjcd-dkbac-jk/n1/b1` | 1.41948 ± 0.026478 (W 0.00827996) | 15.9485 ± 0.0394938 (W 0.0646126) | 2.75928 ± 0.0324414 (W 0.0210452) | 🔵 tcontract 11.24× faster than `ttgt` | 🔵 tcontract 1.94× faster than `tblis` |  |
| `abrs-qb-aqrs/n1/b1` | 0.135111 ± 0.00347842 (W 0.00217071) | 0.737413 ± 0.00794108 (W 0.00442688) | 0.375249 ± 0.00278833 (W 0.00455593) | 🔵 tcontract 5.46× faster than `ttgt` | 🔵 tcontract 2.78× faster than `tblis` | `!` between-start range over 5% |
| `adbjc-cbdka-kj/n1/b1` | 5.92908 ± 0.0418588 (W 0.0899296) | 10.145 ± 0.0885647 (W 0.0207822) | 3.68874 ± 0.151901 (W 0.10692) | 🔵 tcontract 1.71× faster than `ttgt` | 🔴 tcontract 1.61× slower than `tblis` | `!` between-start range over 5% |
| `ajb-kba-jk/n1/b1` | 0.37611 ± 0.00192555 (W 0.00320912) | 1.25757 ± 0.00955297 (W 0.00451297) | 0.564551 ± 0.00458488 (W 0.00409525) | 🔵 tcontract 3.34× faster than `ttgt` | 🔵 tcontract 1.50× faster than `tblis` |  |
| `ajbc-ckba-jk/n1/b1` | 0.215722 ± 0.00497121 (W 0.00207651) | 3.19369 ± 0.0302943 (W 0.0287727) | 0.410184 ± 0.00568982 (W 0.00499574) | 🔵 tcontract 14.80× faster than `ttgt` | 🔵 tcontract 1.90× faster than `tblis` |  |
| `ajbdc-ckbad-jk/n1/b1` | 1.34323 ± 0.0450243 (W 0.0113656) | 22.9231 ± 0.437569 (W 0.10016) | 2.68646 ± 0.0152695 (W 0.0355752) | 🔵 tcontract 17.07× faster than `ttgt` | 🔵 tcontract 2.00× faster than `tblis` | `!` between-start range over 5% |
| `aqrs-pa-pqrs/n1/b1` | 0.280844 ± 0.00133675 (W 0.00206919) | 0.652425 ± 0.0203275 (W 0.0036819) | 0.345624 ± 0.00216899 (W 0.00287532) | 🔵 tcontract 2.32× faster than `ttgt` | 🔵 tcontract 1.23× faster than `tblis` | `!` between-start range over 5% |
| `ij-ik-kj/n1/b1` | 1.00569 ± 0.00413339 (W 0.00152479) | 1.50985 ± 0.629356 (W 0.00352493) | 1.20514 ± 0.00565443 (W 0.00200286) | · | 🔵 tcontract 1.20× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `ij-ikl-ljk/n1/b1` | 0.514378 ± 0.000103184 (W 0.00520904) | 0.944208 ± 0.0114549 (W 0.0119441) | 0.874128 ± 0.00589539 (W 0.00260097) | 🔵 tcontract 1.84× faster than `ttgt` | 🔵 tcontract 1.70× faster than `tblis` |  |
| `ij-kil-lkj/n1/b1` | 0.756489 ± 0.00408252 (W 0.00599961) | 1.60216 ± 0.0132929 (W 0.00795717) | 1.19858 ± 0.0136844 (W 0.00572891) | 🔵 tcontract 2.12× faster than `ttgt` | 🔵 tcontract 1.58× faster than `tblis` |  |
| `ijk-ikl-lj/n1/b1` | 0.28437 ± 5.80259e-05 (W 0.00204437) | 0.820619 ± 0.018571 (W 0.00339039) | 0.472189 ± 0.00385038 (W 0.00433024) | 🔵 tcontract 2.89× faster than `ttgt` | 🔵 tcontract 1.66× faster than `tblis` |  |
| `ijk-il-jlk/n1/b1` | 0.272657 ± 0.000520562 (W 0.00189309) | 1.15142 ± 0.0166411 (W 0.0148062) | 0.437615 ± 0.00359125 (W 0.00308997) | 🔵 tcontract 4.22× faster than `ttgt` | 🔵 tcontract 1.61× faster than `tblis` |  |
| `ijk-ilk-jl/n1/b1` | 0.265685 ± 0.00149541 (W 0.00173869) | 0.853609 ± 0.00944376 (W 0.00536517) | 0.425462 ± 0.00290829 (W 0.00407854) | 🔵 tcontract 3.21× faster than `ttgt` | 🔵 tcontract 1.60× faster than `tblis` |  |
| `ijk-ilk-lj/n1/b1` | 0.283658 ± 0.0012727 (W 0.00297239) | 0.857547 ± 0.00298826 (W 0.00722121) | 0.47256 ± 0.00129928 (W 0.00539296) | 🔵 tcontract 3.02× faster than `ttgt` | 🔵 tcontract 1.67× faster than `tblis` |  |
| `ijk-ilmk-mjl/n1/b1` | 0.119893 ± 0.0010491 (W 0.000591664) | 0.405004 ± 0.00234803 (W 0.0015909) | 0.283718 ± 0.00251819 (W 0.00202549) | 🔵 tcontract 3.38× faster than `ttgt` | 🔵 tcontract 2.37× faster than `tblis` |  |
| `ijkl-imjn-lnkm/n1/b1` | 1.5959 ± 0.00584138 (W 0.00579263) | 2.64946 ± 0.00578079 (W 0.0101972) | 2.08534 ± 0.290583 (W 0.010076) | 🔵 tcontract 1.66× faster than `ttgt` | 🔵 tcontract 1.31× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `ijkl-imjn-nlmk/n1/b1` | 1.5864 ± 0.0103831 (W 0.00564512) | 2.68349 ± 0.0152827 (W 0.00370157) | 2.03997 ± 0.0160431 (W 0.00881916) | 🔵 tcontract 1.69× faster than `ttgt` | 🔵 tcontract 1.29× faster than `tblis` |  |
| `ijkl-imkn-jnlm/n1/b1` | 1.57335 ± 0.00448955 (W 0.00723428) | 2.6399 ± 0.0183786 (W 0.0100858) | 2.00373 ± 0.017155 (W 0.00644471) | 🔵 tcontract 1.68× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `ijkl-imkn-njml/n1/b1` | 1.56813 ± 0.00367154 (W 0.00252409) | 2.67538 ± 0.0169908 (W 0.00663261) | 1.99473 ± 0.0153744 (W 0.00454411) | 🔵 tcontract 1.71× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `ijkl-imln-jnkm/n1/b1` | 1.56671 ± 0.000791519 (W 0.00448316) | 2.65509 ± 0.0279424 (W 0.00373744) | 1.98745 ± 0.00862389 (W 0.0050444) | 🔵 tcontract 1.69× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `ijkl-imln-njmk/n1/b1` | 1.57148 ± 0.0155469 (W 0.00776585) | 2.66978 ± 0.00865706 (W 0.00637623) | 1.99073 ± 0.0173261 (W 0.00844808) | 🔵 tcontract 1.70× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `ijkl-imnj-nlkm/n1/b1` | 1.5758 ± 0.00475867 (W 0.00695324) | 2.64029 ± 0.00156482 (W 0.0103572) | 2.02587 ± 0.0223205 (W 0.00296611) | 🔵 tcontract 1.68× faster than `ttgt` | 🔵 tcontract 1.29× faster than `tblis` |  |
| `ijkl-imnk-njml/n1/b1` | 1.56467 ± 0.00166921 (W 0.00528901) | 2.64895 ± 0.00291289 (W 0.00998591) | 2.00128 ± 0.00763576 (W 0.00569663) | 🔵 tcontract 1.69× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` |  |
| `ijkl-minj-nlmk/n1/b1` | 1.93499 ± 0.00564193 (W 0.00432275) | 3.26757 ± 0.0426181 (W 0.00889711) | 2.46275 ± 0.0146858 (W 0.00373517) | 🔵 tcontract 1.69× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `ijkl-mink-jnlm/n1/b1` | 1.89924 ± 0.00656515 (W 0.0135557) | 3.16683 ± 0.00939151 (W 0.00970723) | 2.35225 ± 0.0181007 (W 0.00622211) | 🔵 tcontract 1.67× faster than `ttgt` | 🔵 tcontract 1.24× faster than `tblis` |  |
| `ijkl-minl-njmk/n1/b1` | 1.92168 ± 0.0115902 (W 0.0045383) | 3.27116 ± 0.0308304 (W 0.0106878) | 2.40808 ± 0.0158967 (W 0.00991336) | 🔵 tcontract 1.70× faster than `ttgt` | 🔵 tcontract 1.25× faster than `tblis` |  |

## tcbench, c64, 1T (CPU 4)

| case | plan (ms) | ttgt (ms) | tblis (ms) | vs `ttgt` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `abc-bk-akc/n1/b1` | 4.06788 ± 0.00118286 (W 0.00692441) | 6.36279 ± 0.0315024 (W 0.0204106) | 4.93201 ± 0.0442311 (W 0.0175734) | 🔵 tcontract 1.56× faster than `ttgt` | 🔵 tcontract 1.21× faster than `tblis` |  |
| `abcijk-eiab-jkec/n1/b1` | 17.6253 ± 0.0240947 (W 0.0286803) | 41.4557 ± 0.10988 (W 0.0473998) | 19.0112 ± 0.0950088 (W 0.0534314) | 🔵 tcontract 2.35× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `abcijk-eiac-jkeb/n1/b1` | 17.2688 ± 0.0333573 (W 0.021966) | 42.5332 ± 0.134053 (W 0.0566473) | 20.7554 ± 0.103374 (W 0.0490545) | 🔵 tcontract 2.46× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `abcijk-eibc-jkea/n1/b1` | 17.643 ± 0.033662 (W 0.0223112) | 45.6687 ± 0.0728699 (W 0.0587863) | 19.0581 ± 0.0207026 (W 0.049792) | 🔵 tcontract 2.59× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `abcijk-ejab-ikec/n1/b1` | 17.5751 ± 0.0177861 (W 0.0324176) | 41.5807 ± 0.0941131 (W 0.121336) | 19.1183 ± 0.0449507 (W 0.0755328) | 🔵 tcontract 2.37× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `abcijk-ejac-ikeb/n1/b1` | 17.3145 ± 0.0541794 (W 0.0241814) | 42.963 ± 0.108852 (W 0.0859028) | 19.5325 ± 0.104816 (W 0.113898) | 🔵 tcontract 2.48× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ejbc-ikea/n1/b1` | 17.6694 ± 0.0390481 (W 0.0158841) | 46.0661 ± 0.0477442 (W 0.0932144) | 19.9975 ± 0.0398063 (W 0.0540405) | 🔵 tcontract 2.61× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ekab-ijec/n1/b1` | 17.5551 ± 0.0267968 (W 0.0318653) | 41.6028 ± 0.315736 (W 0.115062) | 18.8463 ± 0.068356 (W 0.0569511) | 🔵 tcontract 2.37× faster than `ttgt` | 🔵 tcontract 1.07× faster than `tblis` |  |
| `abcijk-ekac-ijeb/n1/b1` | 17.3179 ± 0.0486103 (W 0.0223085) | 44.0333 ± 0.300586 (W 0.0794311) | 19.9859 ± 0.0679777 (W 0.040198) | 🔵 tcontract 2.54× faster than `ttgt` | 🔵 tcontract 1.15× faster than `tblis` |  |
| `abcijk-ekbc-ijea/n1/b1` | 17.6492 ± 0.0613688 (W 0.0255022) | 47.4858 ± 0.297297 (W 0.105745) | 20.0302 ± 0.0848691 (W 0.026274) | 🔵 tcontract 2.69× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ijma-mkbc/n1/b1` | 17.7332 ± 0.105772 (W 0.0393255) | 66.1992 ± 0.169923 (W 0.0845083) | 20.073 ± 0.0225523 (W 0.0429115) | 🔵 tcontract 3.73× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ijmb-mkac/n1/b1` | 17.2776 ± 0.0218214 (W 0.0356074) | 67.282 ± 0.217844 (W 0.127738) | 19.9555 ± 0.0570129 (W 0.0264615) | 🔵 tcontract 3.89× faster than `ttgt` | 🔵 tcontract 1.15× faster than `tblis` |  |
| `abcijk-ijmc-mkab/n1/b1` | 17.5408 ± 0.0311859 (W 0.022327) | 79.376 ± 0.612308 (W 0.318599) | 18.8617 ± 0.0287366 (W 0.0789137) | 🔵 tcontract 4.53× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `abcijk-ikma-mjbc/n1/b1` | 17.6541 ± 0.024509 (W 0.0271132) | 70.5501 ± 1.04705 (W 0.123651) | 20.0134 ± 0.0637028 (W 0.0414363) | 🔵 tcontract 4.00× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ikmb-mjac/n1/b1` | 17.2977 ± 0.00734701 (W 0.011784) | 69.8634 ± 0.361027 (W 0.305533) | 19.5078 ± 0.0569999 (W 0.0471736) | 🔵 tcontract 4.04× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 17.5729 ± 0.0536269 (W 0.0267398) | 79.8903 ± 0.374673 (W 0.0785514) | 19.123 ± 0.05444 (W 0.0485124) | 🔵 tcontract 4.55× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `abcijk-jkma-mibc/n1/b1` | 17.6419 ± 0.0051821 (W 0.0243102) | 109.507 ± 1.57665 (W 0.414342) | 19.074 ± 0.0148536 (W 0.0509604) | 🔵 tcontract 6.21× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `abcijk-jkmb-miac/n1/b1` | 17.286 ± 0.0266325 (W 0.026652) | 108.731 ± 2.35882 (W 0.13317) | 20.6824 ± 0.0483715 (W 0.0870939) | 🔵 tcontract 6.29× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `abcijk-jkmc-miab/n1/b1` | 17.6254 ± 0.0168415 (W 0.0260306) | 114.006 ± 1.7016 (W 0.412355) | 19.0612 ± 0.0987837 (W 0.0482087) | 🔵 tcontract 6.47× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `abcs-rc-abrs/n1/b1` | 1.84597 ± 0.00884488 (W 0.00474225) | 3.01079 ± 0.0270143 (W 0.00720686) | 2.37765 ± 0.0252264 (W 0.0113425) | 🔵 tcontract 1.63× faster than `ttgt` | 🔵 tcontract 1.29× faster than `tblis` |  |
| `abj-bka-kj/n1/b1` | 7.55286 ± 0.0916694 (W 0.0163759) | 8.35059 ± 0.00826168 (W 0.0123557) | 8.38964 ± 0.0377751 (W 0.0613737) | 🔵 tcontract 1.11× faster than `ttgt` | 🔵 tcontract 1.11× faster than `tblis` |  |
| `abjc-cbka-kj/n1/b1` | 3.61071 ± 0.0850949 (W 0.0103325) | 3.66568 ± 0.0224981 (W 0.0208009) | 3.07011 ± 0.0257618 (W 0.0300097) | · | 🔴 tcontract 1.18× slower than `tblis` |  |
| `abjc-kbac-jk/n1/b1` | 1.96654 ± 0.00368388 (W 0.0054422) | 3.60548 ± 0.196114 (W 0.0208179) | 2.66673 ± 0.0449194 (W 0.0325299) | 🔵 tcontract 1.83× faster than `ttgt` | 🔵 tcontract 1.36× faster than `tblis` | `!` between-start range over 5% |
| `abjcd-dkbac-jk/n1/b1` | 12.9932 ± 0.056339 (W 0.104144) | 29.8319 ± 0.932491 (W 0.0639177) | 17.3549 ± 0.183679 (W 0.112382) | 🔵 tcontract 2.30× faster than `ttgt` | 🔵 tcontract 1.34× faster than `tblis` | `!` between-start range over 5% |
| `abrs-qb-aqrs/n1/b1` | 1.60176 ± 0.00486021 (W 0.0054304) | 2.97597 ± 0.103219 (W 0.0182615) | 2.50486 ± 0.0135773 (W 0.0211408) | 🔵 tcontract 1.86× faster than `ttgt` | 🔵 tcontract 1.56× faster than `tblis` | `!` between-start range over 5% |
| `adbjc-cbdka-kj/n1/b1` | 20.2112 ± 0.202276 (W 0.0483842) | 22.8861 ± 0.378276 (W 0.0322126) | 19.4173 ± 0.275281 (W 0.0736076) | 🔵 tcontract 1.13× faster than `ttgt` | · |  |
| `ajb-kba-jk/n1/b1` | 5.74946 ± 0.0161509 (W 0.0150771) | 7.98403 ± 0.0123377 (W 0.0152215) | 7.29356 ± 0.0672616 (W 0.044672) | 🔵 tcontract 1.39× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `ajbc-ckba-jk/n1/b1` | 2.30918 ± 0.0422281 (W 0.00501266) | 5.68482 ± 0.0390838 (W 0.0304997) | 3.04797 ± 0.0154941 (W 0.0558458) | 🔵 tcontract 2.46× faster than `ttgt` | 🔵 tcontract 1.32× faster than `tblis` |  |
| `ajbdc-ckbad-jk/n1/b1` | 12.4818 ± 0.0234552 (W 0.0324111) | 34.193 ± 0.0958272 (W 0.0847323) | 17.3578 ± 0.140916 (W 0.109212) | 🔵 tcontract 2.74× faster than `ttgt` | 🔵 tcontract 1.39× faster than `tblis` |  |
| `aqrs-pa-pqrs/n1/b1` | 2.04548 ± 0.005829 (W 0.00457351) | 2.59827 ± 0.0138774 (W 0.00504042) | 2.33861 ± 0.0110881 (W 0.00304729) | 🔵 tcontract 1.27× faster than `ttgt` | 🔵 tcontract 1.14× faster than `tblis` |  |
| `ij-ik-kj/n1/b1` | 14.4789 ± 0.0248243 (W 0.0221269) | 17.6868 ± 0.00969084 (W 0.0275678) | 15.2514 ± 0.0520843 (W 0.025844) | 🔵 tcontract 1.22× faster than `ttgt` | 🔵 tcontract 1.05× faster than `tblis` |  |
| `ij-ikl-ljk/n1/b1` | 4.8617 ± 0.013113 (W 0.0138387) | 5.80943 ± 0.0454735 (W 0.0363849) | 5.67116 ± 0.0522432 (W 0.0247732) | 🔵 tcontract 1.19× faster than `ttgt` | 🔵 tcontract 1.17× faster than `tblis` |  |
| `ij-kil-lkj/n1/b1` | 7.41239 ± 0.0543618 (W 0.0117451) | 8.67608 ± 0.0380105 (W 0.0221568) | 8.25429 ± 0.0628084 (W 0.0316163) | 🔵 tcontract 1.17× faster than `ttgt` | 🔵 tcontract 1.11× faster than `tblis` |  |
| `ijk-ikl-lj/n1/b1` | 4.20742 ± 0.0217753 (W 0.00919481) | 5.47756 ± 0.154109 (W 0.0185735) | 5.67791 ± 0.0072439 (W 0.0231461) | 🔵 tcontract 1.30× faster than `ttgt` | 🔵 tcontract 1.35× faster than `tblis` |  |
| `ijk-il-jlk/n1/b1` | 4.54714 ± 0.0340741 (W 0.00892134) | 6.33294 ± 0.0233984 (W 0.0223803) | 4.76854 ± 0.0504639 (W 0.0207576) | 🔵 tcontract 1.39× faster than `ttgt` | · |  |
| `ijk-ilk-jl/n1/b1` | 4.06197 ± 0.0348511 (W 0.00981329) | 5.99033 ± 0.0157317 (W 0.0167352) | 4.96916 ± 0.0325928 (W 0.021007) | 🔵 tcontract 1.47× faster than `ttgt` | 🔵 tcontract 1.22× faster than `tblis` |  |
| `ijk-ilk-lj/n1/b1` | 4.2016 ± 0.0128319 (W 0.0160284) | 5.9898 ± 0.023364 (W 0.00838259) | 5.25245 ± 0.172987 (W 0.0320864) | 🔵 tcontract 1.43× faster than `ttgt` | 🔵 tcontract 1.25× faster than `tblis` | `!` between-start range over 5% |
| `ijk-ilmk-mjl/n1/b1` | 1.62908 ± 0.00529511 (W 0.00420096) | 2.03479 ± 0.0323667 (W 0.00639467) | 2.06495 ± 0.00214415 (W 0.00523878) | 🔵 tcontract 1.25× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `ijkl-imjn-lnkm/n1/b1` | 25.0616 ± 0.08294 (W 0.0353684) | 30.7439 ± 0.167434 (W 0.0269303) | 26.6482 ± 0.156595 (W 0.0528485) | 🔵 tcontract 1.23× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` |  |
| `ijkl-imjn-nlmk/n1/b1` | 24.9865 ± 0.0447949 (W 0.0320202) | 30.6286 ± 0.177915 (W 0.0549658) | 27.4856 ± 0.070024 (W 0.0509604) | 🔵 tcontract 1.23× faster than `ttgt` | 🔵 tcontract 1.10× faster than `tblis` |  |
| `ijkl-imkn-jnlm/n1/b1` | 24.9698 ± 0.0358675 (W 0.0443242) | 30.7464 ± 0.176764 (W 0.0543358) | 26.6032 ± 0.114664 (W 0.0434375) | 🔵 tcontract 1.23× faster than `ttgt` | 🔵 tcontract 1.07× faster than `tblis` |  |
| `ijkl-imkn-njml/n1/b1` | 25.0923 ± 0.11525 (W 0.0381005) | 30.948 ± 0.253858 (W 0.0454208) | 27.4909 ± 0.316777 (W 0.0907773) | 🔵 tcontract 1.23× faster than `ttgt` | 🔵 tcontract 1.10× faster than `tblis` |  |
| `ijkl-imln-jnkm/n1/b1` | 24.9317 ± 0.0458852 (W 0.0315087) | 30.7061 ± 0.20496 (W 0.0437623) | 26.5818 ± 0.157654 (W 0.0959006) | 🔵 tcontract 1.23× faster than `ttgt` | 🔵 tcontract 1.07× faster than `tblis` |  |
| `ijkl-imln-njmk/n1/b1` | 24.9962 ± 0.11438 (W 0.0298562) | 30.7578 ± 0.228894 (W 0.0290095) | 27.0402 ± 0.0875871 (W 0.0390391) | 🔵 tcontract 1.23× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `ijkl-imnj-nlkm/n1/b1` | 24.9372 ± 0.0283682 (W 0.0180888) | 30.4636 ± 0.221808 (W 0.0425186) | 27.0819 ± 0.152419 (W 0.0372202) | 🔵 tcontract 1.22× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `ijkl-imnk-njml/n1/b1` | 24.9345 ± 0.0755946 (W 0.0339068) | 30.511 ± 0.223743 (W 0.0471155) | 27.122 ± 0.191939 (W 0.0289) | 🔵 tcontract 1.22× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `ijkl-minj-nlmk/n1/b1` | 30.653 ± 0.0808817 (W 0.0739486) | 36.7735 ± 0.230351 (W 0.0482953) | 33.1537 ± 0.188324 (W 0.0596833) | 🔵 tcontract 1.20× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `ijkl-mink-jnlm/n1/b1` | 29.9977 ± 0.0200975 (W 0.045776) | 36.7751 ± 0.252312 (W 0.124004) | 31.8078 ± 0.264222 (W 0.053863) | 🔵 tcontract 1.23× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` |  |
| `ijkl-minl-njmk/n1/b1` | 30.5687 ± 0.0917298 (W 0.0149514) | 36.6724 ± 0.318856 (W 0.046566) | 32.4912 ± 0.113085 (W 0.121072) | 🔵 tcontract 1.20× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` |  |

## tcbench, c64, 4T (CPU 4-7)

| case | plan (ms) | ttgt (ms) | tblis (ms) | vs `ttgt` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `abc-bk-akc/n1/b1` | 1.03799 ± 0.00152215 (W 0.00197601) | 2.7328 ± 0.019339 (W 0.0167865) | 1.26143 ± 0.0191257 (W 0.00568308) | 🔵 tcontract 2.63× faster than `ttgt` | 🔵 tcontract 1.22× faster than `tblis` |  |
| `abcijk-eiab-jkec/n1/b1` | 4.497 ± 0.00768017 (W 0.00764378) | 27.3932 ± 0.218442 (W 0.163956) | 5.04555 ± 0.876412 (W 0.0311048) | 🔵 tcontract 6.09× faster than `ttgt` | · | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-eiac-jkeb/n1/b1` | 4.37019 ± 0.0148538 (W 0.0109287) | 28.2968 ± 0.15895 (W 0.105815) | 5.53465 ± 0.0404976 (W 0.0152622) | 🔵 tcontract 6.47× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `abcijk-eibc-jkea/n1/b1` | 4.46647 ± 0.0177525 (W 0.00513902) | 30.9711 ± 0.113461 (W 0.107029) | 4.96913 ± 0.00329385 (W 0.0101277) | 🔵 tcontract 6.93× faster than `ttgt` | 🔵 tcontract 1.11× faster than `tblis` |  |
| `abcijk-ejab-ikec/n1/b1` | 4.45316 ± 0.0117241 (W 0.00856655) | 27.439 ± 0.152216 (W 0.150379) | 5.11645 ± 0.0133914 (W 0.0478834) | 🔵 tcontract 6.16× faster than `ttgt` | 🔵 tcontract 1.15× faster than `tblis` |  |
| `abcijk-ejac-ikeb/n1/b1` | 4.36911 ± 0.0155983 (W 0.00927374) | 28.5288 ± 0.0912481 (W 0.100135) | 5.16483 ± 0.0094049 (W 0.019175) | 🔵 tcontract 6.53× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `abcijk-ejbc-ikea/n1/b1` | 4.45981 ± 0.0136567 (W 0.0165492) | 31.4548 ± 0.0744924 (W 0.100874) | 5.2304 ± 0.00834491 (W 0.0184354) | 🔵 tcontract 7.05× faster than `ttgt` | 🔵 tcontract 1.17× faster than `tblis` |  |
| `abcijk-ekab-ijec/n1/b1` | 4.45951 ± 0.209413 (W 0.00881833) | 27.6876 ± 0.137822 (W 0.0408885) | 4.94971 ± 0.0486018 (W 0.0175277) | 🔵 tcontract 6.21× faster than `ttgt` | 🔵 tcontract 1.11× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ekac-ijeb/n1/b1` | 4.36347 ± 0.00707833 (W 0.00834042) | 28.9763 ± 0.325619 (W 0.322689) | 5.23496 ± 0.0169139 (W 0.0120337) | 🔵 tcontract 6.64× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `abcijk-ekbc-ijea/n1/b1` | 4.45834 ± 0.0170854 (W 0.00610179) | 32.7476 ± 0.798873 (W 0.0908402) | 5.21536 ± 0.027461 (W 0.0224496) | 🔵 tcontract 7.35× faster than `ttgt` | 🔵 tcontract 1.17× faster than `tblis` |  |
| `abcijk-ijma-mkbc/n1/b1` | 4.45621 ± 0.0319862 (W 0.00852605) | 53.0404 ± 0.107277 (W 0.133281) | 5.19957 ± 0.0106375 (W 0.0174714) | 🔵 tcontract 11.90× faster than `ttgt` | 🔵 tcontract 1.17× faster than `tblis` |  |
| `abcijk-ijmb-mkac/n1/b1` | 4.36413 ± 0.0268596 (W 0.00898994) | 53.9687 ± 0.377143 (W 0.119856) | 5.23684 ± 0.0159537 (W 0.0147085) | 🔵 tcontract 12.37× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `abcijk-ijmc-mkab/n1/b1` | 4.41718 ± 0.00334566 (W 0.00504496) | 64.3652 ± 0.913563 (W 0.132624) | 4.92848 ± 0.0102689 (W 0.0231583) | 🔵 tcontract 14.57× faster than `ttgt` | 🔵 tcontract 1.12× faster than `tblis` |  |
| `abcijk-ikma-mjbc/n1/b1` | 4.44174 ± 0.00480736 (W 0.00669174) | 56.6064 ± 0.203603 (W 0.0934756) | 5.21558 ± 0.00545773 (W 0.0168855) | 🔵 tcontract 12.74× faster than `ttgt` | 🔵 tcontract 1.17× faster than `tblis` |  |
| `abcijk-ikmb-mjac/n1/b1` | 4.36159 ± 0.0129085 (W 0.00877761) | 56.0158 ± 0.445071 (W 0.16941) | 5.13827 ± 0.0188046 (W 0.0222574) | 🔵 tcontract 12.84× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 4.42635 ± 0.0105125 (W 0.00763129) | 65.7475 ± 0.276528 (W 0.174243) | 5.16452 ± 0.00819921 (W 0.0379004) | 🔵 tcontract 14.85× faster than `ttgt` | 🔵 tcontract 1.17× faster than `tblis` |  |
| `abcijk-jkma-mibc/n1/b1` | 4.4492 ± 0.027671 (W 0.01006) | 95.7113 ± 1.01813 (W 0.32248) | 4.97435 ± 0.00850524 (W 0.010584) | 🔵 tcontract 21.51× faster than `ttgt` | 🔵 tcontract 1.12× faster than `tblis` |  |
| `abcijk-jkmb-miac/n1/b1` | 4.35785 ± 0.0137357 (W 0.00878244) | 95.6941 ± 2.99907 (W 0.285968) | 5.5118 ± 0.0269289 (W 0.0234743) | 🔵 tcontract 21.96× faster than `ttgt` | 🔵 tcontract 1.26× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-jkmc-miab/n1/b1` | 4.45988 ± 0.00228499 (W 0.0051017) | 101.252 ± 2.17204 (W 0.296912) | 5.08094 ± 0.036617 (W 0.0453842) | 🔵 tcontract 22.70× faster than `ttgt` | 🔵 tcontract 1.14× faster than `tblis` |  |
| `abcs-rc-abrs/n1/b1` | 0.471608 ± 0.00508307 (W 0.00284172) | 1.64136 ± 0.0165448 (W 0.0100393) | 0.705674 ± 0.00729479 (W 0.00873119) | 🔵 tcontract 3.48× faster than `ttgt` | 🔵 tcontract 1.50× faster than `tblis` |  |
| `abj-bka-kj/n1/b1` | 1.60747 ± 0.0128675 (W 0.00742143) | 3.63281 ± 0.0425933 (W 0.0242706) | 2.30097 ± 0.0225022 (W 0.0190182) | 🔵 tcontract 2.26× faster than `ttgt` | 🔵 tcontract 1.43× faster than `tblis` |  |
| `abjc-cbka-kj/n1/b1` | 0.815239 ± 0.005518 (W 0.00537073) | 2.089 ± 0.00492332 (W 0.0112389) | 0.927347 ± 0.0494895 (W 0.0430565) | 🔵 tcontract 2.56× faster than `ttgt` | 🔵 tcontract 1.14× faster than `tblis` | `!` between-start range over 5% |
| `abjc-kbac-jk/n1/b1` | 0.509169 ± 0.00147859 (W 0.00247203) | 2.20926 ± 0.214018 (W 0.0211329) | 0.769363 ± 0.012488 (W 0.00857197) | 🔵 tcontract 4.34× faster than `ttgt` | 🔵 tcontract 1.51× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abjcd-dkbac-jk/n1/b1` | 3.82562 ± 0.00528423 (W 0.0165298) | 22.0011 ± 0.500084 (W 0.0550611) | 5.21239 ± 0.0191057 (W 0.0305037) | 🔵 tcontract 5.75× faster than `ttgt` | 🔵 tcontract 1.36× faster than `tblis` |  |
| `abrs-qb-aqrs/n1/b1` | 0.414282 ± 0.00240385 (W 0.00267321) | 1.56042 ± 0.0626083 (W 0.0252572) | 0.72495 ± 0.00581824 (W 0.0110558) | 🔵 tcontract 3.77× faster than `ttgt` | 🔵 tcontract 1.75× faster than `tblis` | `!` between-start range over 5% |
| `adbjc-cbdka-kj/n1/b1` | 7.99283 ± 0.123325 (W 0.0539345) | 15.9154 ± 0.0606591 (W 0.0571717) | 7.29126 ± 0.0870004 (W 0.126863) | 🔵 tcontract 1.99× faster than `ttgt` | 🔴 tcontract 1.10× slower than `tblis` |  |
| `ajb-kba-jk/n1/b1` | 1.43439 ± 0.00627321 (W 0.00402897) | 3.56785 ± 0.0189499 (W 0.0123643) | 1.89977 ± 0.0552293 (W 0.0304674) | 🔵 tcontract 2.49× faster than `ttgt` | 🔵 tcontract 1.32× faster than `tblis` | `!` between-start range over 5% |
| `ajbc-ckba-jk/n1/b1` | 0.599436 ± 0.00596845 (W 0.00464955) | 4.22418 ± 0.0207668 (W 0.0153313) | 0.920344 ± 0.00215769 (W 0.0101332) | 🔵 tcontract 7.05× faster than `ttgt` | 🔵 tcontract 1.54× faster than `tblis` |  |
| `ajbdc-ckbad-jk/n1/b1` | 3.66514 ± 0.018179 (W 0.0375514) | 27.6946 ± 0.214697 (W 0.102075) | 5.15594 ± 0.0146637 (W 0.0290815) | 🔵 tcontract 7.56× faster than `ttgt` | 🔵 tcontract 1.41× faster than `tblis` |  |
| `aqrs-pa-pqrs/n1/b1` | 0.623852 ± 0.00651213 (W 0.00289808) | 1.21854 ± 0.0118381 (W 0.00275378) | 0.657855 ± 0.00422424 (W 0.00444469) | 🔵 tcontract 1.95× faster than `ttgt` | 🔵 tcontract 1.05× faster than `tblis` |  |
| `ij-ik-kj/n1/b1` | 3.68837 ± 0.010829 (W 0.00658748) | 5.02322 ± 0.0289545 (W 0.00824283) | 3.99894 ± 0.024662 (W 0.0133759) | 🔵 tcontract 1.36× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `ij-ikl-ljk/n1/b1` | 2.08523 ± 0.0135184 (W 0.0116059) | 2.24125 ± 0.0121847 (W 0.01719) | 1.69699 ± 0.0154295 (W 0.00882004) | 🔵 tcontract 1.07× faster than `ttgt` | 🔴 tcontract 1.23× slower than `tblis` |  |
| `ij-kil-lkj/n1/b1` | 3.09458 ± 0.0174148 (W 0.0101495) | 3.64171 ± 0.269754 (W 0.0228814) | 2.37613 ± 0.0114493 (W 0.0130902) | 🔵 tcontract 1.18× faster than `ttgt` | 🔴 tcontract 1.30× slower than `tblis` | `!` between-start range over 5% |
| `ijk-ikl-lj/n1/b1` | 1.06773 ± 0.00761035 (W 0.00180928) | 2.14534 ± 0.0198546 (W 0.00563266) | 1.42067 ± 0.0336325 (W 0.0128298) | 🔵 tcontract 2.01× faster than `ttgt` | 🔵 tcontract 1.33× faster than `tblis` |  |
| `ijk-il-jlk/n1/b1` | 1.85458 ± 0.0147257 (W 0.00984762) | 2.70133 ± 0.00943183 (W 0.034374) | 1.2166 ± 0.0092202 (W 0.00496506) | 🔵 tcontract 1.46× faster than `ttgt` | 🔴 tcontract 1.52× slower than `tblis` |  |
| `ijk-ilk-jl/n1/b1` | 1.03536 ± 0.00467634 (W 0.00263152) | 2.70207 ± 0.0200489 (W 0.0127702) | 1.27954 ± 0.0133631 (W 0.00658749) | 🔵 tcontract 2.61× faster than `ttgt` | 🔵 tcontract 1.24× faster than `tblis` |  |
| `ijk-ilk-lj/n1/b1` | 1.06541 ± 0.00362533 (W 0.00265057) | 2.67429 ± 0.00595826 (W 0.0086245) | 1.37006 ± 0.00500481 (W 0.00850632) | 🔵 tcontract 2.51× faster than `ttgt` | 🔵 tcontract 1.29× faster than `tblis` |  |
| `ijk-ilmk-mjl/n1/b1` | 0.458834 ± 0.00136311 (W 0.00233869) | 0.849492 ± 0.00762526 (W 0.00259601) | 0.544855 ± 0.000760935 (W 0.00308649) | 🔵 tcontract 1.85× faster than `ttgt` | 🔵 tcontract 1.19× faster than `tblis` |  |
| `ijkl-imjn-lnkm/n1/b1` | 6.8178 ± 0.0391919 (W 0.0137216) | 9.01157 ± 0.0173935 (W 0.0188512) | 7.04646 ± 0.0590399 (W 0.0159127) | 🔵 tcontract 1.32× faster than `ttgt` | · |  |
| `ijkl-imjn-nlmk/n1/b1` | 6.74374 ± 0.031322 (W 0.0108481) | 8.95554 ± 0.0392748 (W 0.0139876) | 7.11353 ± 0.0875156 (W 0.013562) | 🔵 tcontract 1.33× faster than `ttgt` | 🔵 tcontract 1.05× faster than `tblis` |  |
| `ijkl-imkn-jnlm/n1/b1` | 6.71266 ± 0.0301241 (W 0.00754462) | 8.94831 ± 0.0454768 (W 0.0136978) | 7.02541 ± 0.0320249 (W 0.0160137) | 🔵 tcontract 1.33× faster than `ttgt` | · |  |
| `ijkl-imkn-njml/n1/b1` | 6.72488 ± 0.0326736 (W 0.0106704) | 8.94362 ± 0.0228743 (W 0.0211799) | 7.06875 ± 0.0366984 (W 0.0158905) | 🔵 tcontract 1.33× faster than `ttgt` | · |  |
| `ijkl-imln-jnkm/n1/b1` | 6.70332 ± 0.0261096 (W 0.0107579) | 8.96 ± 0.0303055 (W 0.0277619) | 7.03465 ± 0.0243776 (W 0.0138413) | 🔵 tcontract 1.34× faster than `ttgt` | · |  |
| `ijkl-imln-njmk/n1/b1` | 6.70254 ± 0.0272144 (W 0.00664575) | 8.90483 ± 0.0647813 (W 0.0304774) | 7.0148 ± 0.0320271 (W 0.0178663) | 🔵 tcontract 1.33× faster than `ttgt` | · |  |
| `ijkl-imnj-nlkm/n1/b1` | 6.72702 ± 0.0274517 (W 0.014157) | 8.65203 ± 0.00686466 (W 0.0249633) | 6.9618 ± 0.0782815 (W 0.0106821) | 🔵 tcontract 1.29× faster than `ttgt` | · |  |
| `ijkl-imnk-njml/n1/b1` | 6.72462 ± 0.0263288 (W 0.02077) | 8.74332 ± 0.0281472 (W 0.0464394) | 7.01645 ± 0.0403045 (W 0.0171109) | 🔵 tcontract 1.30× faster than `ttgt` | · |  |
| `ijkl-minj-nlmk/n1/b1` | 8.30148 ± 0.044363 (W 0.00943901) | 10.5435 ± 0.522788 (W 0.0182367) | 8.66284 ± 0.0585849 (W 0.0276077) | 🔵 tcontract 1.27× faster than `ttgt` | · | `!` between-start range over 5% |
| `ijkl-mink-jnlm/n1/b1` | 8.05466 ± 0.018898 (W 0.0125513) | 10.7067 ± 0.0334177 (W 0.0189204) | 8.42909 ± 0.0446897 (W 0.0179421) | 🔵 tcontract 1.33× faster than `ttgt` | · |  |
| `ijkl-minl-njmk/n1/b1` | 8.24086 ± 0.0292599 (W 0.0104635) | 10.5282 ± 0.0298859 (W 0.0126751) | 8.46013 ± 0.0142865 (W 0.0190276) | 🔵 tcontract 1.28× faster than `ttgt` | · |  |

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
