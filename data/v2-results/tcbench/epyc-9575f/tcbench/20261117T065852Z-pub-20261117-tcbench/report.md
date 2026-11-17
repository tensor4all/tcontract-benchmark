# `tcbench` on `epyc-9575f`

- tcontract-rs commit: `807183f57ce77622f0af197b8c4fa3dced9a84c5`
- features: `blas, tblis`
- tprims rows: `tprims` (the provider in the measured revision; see library above); `openblas` (the provider in the measured revision; see library above)
- external providers: `tblis` 2.0 @ `b16a732939d8454021e0a0f0097cf1cc1dd3ab19` tag `v2.0-beta2` sha256 `a7ddb0fba1fcaf1d5b5661e2e3e9bdfaa6e718db48d692be4e1e98ce6dc09970` (TBLIS 2.0, configuration skx; bundled BLIS 358e689cadd6757f564a2992cf46a2f7d6fa6bb0; built with ./configure --prefix=/home/ningyuan/projects/t4a_bench/workspace/tcontract-benchmark/target/tblis-v2.0-beta2 --with-blis-config-family=skx (cmake, Unix Makefiles, Release); libtblis.so sha256 a7ddb0fba1fcaf1d)
- harness commit: `633af61544120e8dde5783e0010aff1fab20ee09`
- toolkit commit: `ccb3da4650aade26b210de534dee368be419575b`
- measured binary SHA-256: `06e7f4e65a76eece906c8c1f7562fe930ff6ade21af8be19da79cecdbee9e791`
- hardware profile: `epyc-9575f`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-11-17T07:45:07.738540Z`
- timing policy: v2, median of 5 reps, priming 1500 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/v2/record_run.py tcbench epyc-9575f tcbench --external-provider-json target/tblis-providers.json --reps 5 --aa 3 --prime-ms 1500 --label pub-20261117-tcbench`
- raw data: `data/v2-results/tcbench/epyc-9575f/tcbench/20261117T065852Z-pub-20261117-tcbench/`

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
Each process retains 5 chronological calls; 3 complete process sets are recorded.
Spread guide (computed from this run's own rows): per-engine between-start range median 0.87%, worst 60.32% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 36 of 588 engine cells exceed 5% and carry `!`; median within-process relative SD 0.23%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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
| `abc-bk-akc/n1/b1` | 0.343896 ± 0.00121289 (W 0.00100888) | 0.984659 ± 0.0217152 (W 0.00410978) | 0.685492 ± 0.00748792 (W 0.022286) | 🔵 tcontract 2.86× faster than `ttgt` | 🔵 tcontract 1.99× faster than `tblis` |  |
| `abcijk-eiab-jkec/n1/b1` | 1.49735 ± 0.0197517 (W 0.0102782) | 5.44015 ± 0.0618014 (W 0.0207077) | 1.84494 ± 0.0255379 (W 0.00520517) | 🔵 tcontract 3.63× faster than `ttgt` | 🔵 tcontract 1.23× faster than `tblis` |  |
| `abcijk-eiac-jkeb/n1/b1` | 1.4636 ± 0.00925787 (W 0.00132358) | 5.72389 ± 0.0388741 (W 0.00750103) | 3.19738 ± 0.0335309 (W 0.00776305) | 🔵 tcontract 3.91× faster than `ttgt` | 🔵 tcontract 2.18× faster than `tblis` |  |
| `abcijk-eibc-jkea/n1/b1` | 1.5988 ± 0.0132665 (W 0.00213415) | 5.99608 ± 0.0449664 (W 0.0119776) | 1.94519 ± 0.00777114 (W 0.00380852) | 🔵 tcontract 3.75× faster than `ttgt` | 🔵 tcontract 1.22× faster than `tblis` |  |
| `abcijk-ejab-ikec/n1/b1` | 1.48214 ± 0.011451 (W 0.00240156) | 5.28107 ± 0.0295143 (W 0.0342085) | 3.76648 ± 0.0216498 (W 0.00765353) | 🔵 tcontract 3.56× faster than `ttgt` | 🔵 tcontract 2.54× faster than `tblis` |  |
| `abcijk-ejac-ikeb/n1/b1` | 1.46347 ± 0.009137 (W 0.0015135) | 5.73153 ± 0.0856243 (W 0.0652878) | 3.08283 ± 0.0239513 (W 0.00383881) | 🔵 tcontract 3.92× faster than `ttgt` | 🔵 tcontract 2.11× faster than `tblis` |  |
| `abcijk-ejbc-ikea/n1/b1` | 1.60344 ± 0.0135867 (W 0.00130974) | 6.17697 ± 0.129305 (W 0.0149027) | 2.06701 ± 0.00888912 (W 0.00320109) | 🔵 tcontract 3.85× faster than `ttgt` | 🔵 tcontract 1.29× faster than `tblis` |  |
| `abcijk-ekab-ijec/n1/b1` | 1.47863 ± 0.0145567 (W 0.001844) | 5.70442 ± 0.0916987 (W 0.0145207) | 1.84845 ± 0.0226777 (W 0.00571836) | 🔵 tcontract 3.86× faster than `ttgt` | 🔵 tcontract 1.25× faster than `tblis` |  |
| `abcijk-ekac-ijeb/n1/b1` | 1.46243 ± 0.00850738 (W 0.00146616) | 7.07187 ± 0.197346 (W 0.0755755) | 3.18183 ± 0.0072548 (W 0.00653247) | 🔵 tcontract 4.84× faster than `ttgt` | 🔵 tcontract 2.18× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ekbc-ijea/n1/b1` | 1.59446 ± 0.0118548 (W 0.00161388) | 6.73537 ± 0.0459516 (W 0.0174337) | 2.07326 ± 0.0144131 (W 0.00392581) | 🔵 tcontract 4.22× faster than `ttgt` | 🔵 tcontract 1.30× faster than `tblis` |  |
| `abcijk-ijma-mkbc/n1/b1` | 1.59397 ± 0.00987082 (W 0.00114058) | 22.0025 ± 0.179702 (W 0.0394717) | 2.07094 ± 0.0065728 (W 0.0028578) | 🔵 tcontract 13.80× faster than `ttgt` | 🔵 tcontract 1.30× faster than `tblis` |  |
| `abcijk-ijmb-mkac/n1/b1` | 1.46009 ± 0.00840532 (W 0.0018881) | 20.5861 ± 0.0659213 (W 0.0209328) | 3.18446 ± 0.0242247 (W 0.00307234) | 🔵 tcontract 14.10× faster than `ttgt` | 🔵 tcontract 2.18× faster than `tblis` |  |
| `abcijk-ijmc-mkab/n1/b1` | 1.48141 ± 0.0153753 (W 0.00149128) | 21.1415 ± 0.0633638 (W 0.0416228) | 1.83827 ± 0.0197335 (W 0.00682571) | 🔵 tcontract 14.27× faster than `ttgt` | 🔵 tcontract 1.24× faster than `tblis` |  |
| `abcijk-ikma-mjbc/n1/b1` | 1.59986 ± 0.00884149 (W 0.00176531) | 24.2653 ± 0.153684 (W 0.0387316) | 2.07633 ± 0.00590466 (W 0.00306195) | 🔵 tcontract 15.17× faster than `ttgt` | 🔵 tcontract 1.30× faster than `tblis` |  |
| `abcijk-ikmb-mjac/n1/b1` | 1.46004 ± 0.00880147 (W 0.00206703) | 22.0795 ± 0.131487 (W 0.0158416) | 3.08099 ± 0.0158259 (W 0.00583267) | 🔵 tcontract 15.12× faster than `ttgt` | 🔵 tcontract 2.11× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 1.47638 ± 0.0177866 (W 0.00134591) | 22.8186 ± 0.25745 (W 0.0475938) | 3.76011 ± 0.0217168 (W 0.00607232) | 🔵 tcontract 15.46× faster than `ttgt` | 🔵 tcontract 2.55× faster than `tblis` |  |
| `abcijk-jkma-mibc/n1/b1` | 1.59667 ± 0.014436 (W 0.00204206) | 47.6062 ± 16.5237 (W 0.0460284) | 1.96148 ± 0.0116844 (W 0.00597004) | 🔵 tcontract 29.82× faster than `ttgt` | 🔵 tcontract 1.23× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmb-miac/n1/b1` | 1.46318 ± 0.00944898 (W 0.00133586) | 46.0576 ± 7.8486 (W 0.0485722) | 3.20954 ± 0.0133118 (W 0.00804018) | 🔵 tcontract 31.48× faster than `ttgt` | 🔵 tcontract 2.19× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmc-miab/n1/b1` | 1.49742 ± 0.011225 (W 0.00335633) | 47.6027 ± 7.34324 (W 0.0501339) | 1.82805 ± 0.0161969 (W 0.00812487) | 🔵 tcontract 31.79× faster than `ttgt` | 🔵 tcontract 1.22× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcs-rc-abrs/n1/b1` | 0.173503 ± 0.0013642 (W 0.000582417) | 0.590945 ± 0.00368865 (W 0.0174197) | 0.605675 ± 0.00728213 (W 0.0148547) | 🔵 tcontract 3.41× faster than `ttgt` | 🔵 tcontract 3.49× faster than `tblis` |  |
| `abj-bka-kj/n1/b1` | 1.03967 ± 0.0162017 (W 0.0112378) | 1.29209 ± 0.00170371 (W 0.00408887) | 1.04025 ± 0.0174846 (W 0.0359845) | 🔵 tcontract 1.24× faster than `ttgt` | · |  |
| `abjc-cbka-kj/n1/b1` | 0.783357 ± 0.0199902 (W 0.00736422) | 0.667062 ± 0.00306885 (W 0.000918771) | 0.760489 ± 0.00385343 (W 0.0142402) | 🔴 tcontract 1.17× slower than `ttgt` | · |  |
| `abjc-kbac-jk/n1/b1` | 0.217671 ± 0.00128592 (W 0.000815371) | 0.666082 ± 0.0104932 (W 0.00193994) | 0.604625 ± 0.000973944 (W 0.0123443) | 🔵 tcontract 3.06× faster than `ttgt` | 🔵 tcontract 2.78× faster than `tblis` |  |
| `abjcd-dkbac-jk/n1/b1` | 1.83621 ± 0.0119849 (W 0.004192) | 10.4917 ± 0.0737499 (W 0.0212009) | 3.95649 ± 0.0171284 (W 0.0317739) | 🔵 tcontract 5.71× faster than `ttgt` | 🔵 tcontract 2.15× faster than `tblis` |  |
| `abrs-qb-aqrs/n1/b1` | 0.168683 ± 0.000872143 (W 0.000945569) | 0.602904 ± 0.019141 (W 0.00384876) | 0.610804 ± 0.00982793 (W 0.0157158) | 🔵 tcontract 3.57× faster than `ttgt` | 🔵 tcontract 3.62× faster than `tblis` | `!` between-start range over 5% |
| `adbjc-cbdka-kj/n1/b1` | 5.1143 ± 0.037404 (W 0.0219103) | 7.00637 ± 0.104502 (W 0.00816657) | 7.05244 ± 0.636023 (W 0.0391994) | 🔵 tcontract 1.37× faster than `ttgt` | 🔵 tcontract 1.38× faster than `tblis` | `!` between-start range over 5% |
| `ajb-kba-jk/n1/b1` | 0.48918 ± 0.00149262 (W 0.00126123) | 1.231 ± 0.000986955 (W 0.000623545) | 0.912602 ± 0.0126991 (W 0.0105652) | 🔵 tcontract 2.52× faster than `ttgt` | 🔵 tcontract 1.87× faster than `tblis` |  |
| `ajbc-ckba-jk/n1/b1` | 0.335976 ± 0.00294851 (W 0.00232305) | 1.98747 ± 0.00957158 (W 0.00542366) | 0.671332 ± 0.005979 (W 0.013733) | 🔵 tcontract 5.92× faster than `ttgt` | 🔵 tcontract 2.00× faster than `tblis` |  |
| `ajbdc-ckbad-jk/n1/b1` | 1.79442 ± 0.00436933 (W 0.00577043) | 14.1278 ± 0.0965663 (W 0.0381226) | 3.74686 ± 0.0279772 (W 0.0439222) | 🔵 tcontract 7.87× faster than `ttgt` | 🔵 tcontract 2.09× faster than `tblis` |  |
| `aqrs-pa-pqrs/n1/b1` | 0.098146 ± 0.00137191 (W 0.000223099) | 0.567407 ± 0.021338 (W 0.00212309) | 0.49428 ± 0.00473076 (W 0.0160734) | 🔵 tcontract 5.78× faster than `ttgt` | 🔵 tcontract 5.04× faster than `tblis` | `!` between-start range over 5% |
| `ij-ik-kj/n1/b1` | 1.06849 ± 0.0160265 (W 0.000943189) | 2.42351 ± 0.00984617 (W 0.00217774) | 1.49799 ± 0.0125905 (W 0.0191294) | 🔵 tcontract 2.27× faster than `ttgt` | 🔵 tcontract 1.40× faster than `tblis` |  |
| `ij-ikl-ljk/n1/b1` | 0.432112 ± 0.00200702 (W 0.00108749) | 0.938311 ± 0.00173139 (W 0.00124283) | 1.05099 ± 0.00404258 (W 0.0150422) | 🔵 tcontract 2.17× faster than `ttgt` | 🔵 tcontract 2.43× faster than `tblis` |  |
| `ij-kil-lkj/n1/b1` | 0.644743 ± 0.00189327 (W 0.00117049) | 1.31943 ± 0.00323914 (W 0.00190865) | 1.45512 ± 0.00236609 (W 0.0133096) | 🔵 tcontract 2.05× faster than `ttgt` | 🔵 tcontract 2.26× faster than `tblis` |  |
| `ijk-ikl-lj/n1/b1` | 0.350646 ± 0.002133 (W 0.00111756) | 0.925202 ± 0.00132566 (W 0.000474418) | 0.768478 ± 0.0026446 (W 0.0228531) | 🔵 tcontract 2.64× faster than `ttgt` | 🔵 tcontract 2.19× faster than `tblis` |  |
| `ijk-il-jlk/n1/b1` | 0.370384 ± 0.000649431 (W 0.00134181) | 0.980629 ± 0.00216856 (W 0.00114996) | 0.626124 ± 0.0091608 (W 0.0249684) | 🔵 tcontract 2.65× faster than `ttgt` | 🔵 tcontract 1.69× faster than `tblis` |  |
| `ijk-ilk-jl/n1/b1` | 0.345356 ± 0.000522485 (W 0.0010064) | 0.927062 ± 0.000532009 (W 0.00115018) | 0.682601 ± 0.00428335 (W 0.0201209) | 🔵 tcontract 2.68× faster than `ttgt` | 🔵 tcontract 1.98× faster than `tblis` |  |
| `ijk-ilk-lj/n1/b1` | 0.349275 ± 0.000884031 (W 0.00115708) | 0.935781 ± 0.00124374 (W 0.000874159) | 0.763988 ± 0.00905534 (W 0.0126335) | 🔵 tcontract 2.68× faster than `ttgt` | 🔵 tcontract 2.19× faster than `tblis` |  |
| `ijk-ilmk-mjl/n1/b1` | 0.138395 ± 0.000583413 (W 0.00067658) | 0.402323 ± 0.0023253 (W 0.00135125) | 0.49808 ± 0.0055167 (W 0.0113687) | 🔵 tcontract 2.91× faster than `ttgt` | 🔵 tcontract 3.60× faster than `tblis` |  |
| `ijkl-imjn-lnkm/n1/b1` | 1.9875 ± 0.00930852 (W 0.00223413) | 4.03288 ± 0.00870606 (W 0.00207601) | 2.49895 ± 0.0146671 (W 0.0119019) | 🔵 tcontract 2.03× faster than `ttgt` | 🔵 tcontract 1.26× faster than `tblis` |  |
| `ijkl-imjn-nlmk/n1/b1` | 1.95958 ± 0.00599258 (W 0.00453192) | 4.02736 ± 0.0199822 (W 0.0026245) | 2.54404 ± 0.0147407 (W 0.0136634) | 🔵 tcontract 2.06× faster than `ttgt` | 🔵 tcontract 1.30× faster than `tblis` |  |
| `ijkl-imkn-jnlm/n1/b1` | 1.93666 ± 0.00945275 (W 0.00100151) | 4.02847 ± 0.00905644 (W 0.00073128) | 2.53359 ± 0.00876682 (W 0.012483) | 🔵 tcontract 2.08× faster than `ttgt` | 🔵 tcontract 1.31× faster than `tblis` |  |
| `ijkl-imkn-njml/n1/b1` | 1.95754 ± 0.0035708 (W 0.00111734) | 4.04437 ± 0.00679117 (W 0.00530359) | 2.56565 ± 0.0124427 (W 0.022605) | 🔵 tcontract 2.07× faster than `ttgt` | 🔵 tcontract 1.31× faster than `tblis` |  |
| `ijkl-imln-jnkm/n1/b1` | 1.93354 ± 0.00725971 (W 0.000856526) | 4.03884 ± 0.0109519 (W 0.00524909) | 2.46732 ± 0.0153549 (W 0.018762) | 🔵 tcontract 2.09× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` |  |
| `ijkl-imln-njmk/n1/b1` | 1.95513 ± 0.00340915 (W 0.00221169) | 4.03711 ± 0.0165712 (W 0.0105316) | 2.4997 ± 0.011922 (W 0.0151151) | 🔵 tcontract 2.06× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` |  |
| `ijkl-imnj-nlkm/n1/b1` | 1.961 ± 0.0063687 (W 0.00135219) | 4.04099 ± 0.00910302 (W 0.00363136) | 2.59193 ± 0.00198661 (W 0.0279695) | 🔵 tcontract 2.06× faster than `ttgt` | 🔵 tcontract 1.32× faster than `tblis` |  |
| `ijkl-imnk-njml/n1/b1` | 1.9548 ± 0.0029126 (W 0.000728257) | 4.03558 ± 0.00810552 (W 0.0037129) | 2.5782 ± 0.0053633 (W 0.0203913) | 🔵 tcontract 2.06× faster than `ttgt` | 🔵 tcontract 1.32× faster than `tblis` |  |
| `ijkl-minj-nlmk/n1/b1` | 2.42201 ± 0.00714721 (W 0.00151754) | 4.95366 ± 0.0259103 (W 0.00477384) | 3.02399 ± 0.015992 (W 0.0266678) | 🔵 tcontract 2.05× faster than `ttgt` | 🔵 tcontract 1.25× faster than `tblis` |  |
| `ijkl-mink-jnlm/n1/b1` | 2.33999 ± 0.00942711 (W 0.00106945) | 4.83287 ± 0.0237415 (W 0.00942773) | 3.01552 ± 0.0178789 (W 0.018634) | 🔵 tcontract 2.07× faster than `ttgt` | 🔵 tcontract 1.29× faster than `tblis` |  |
| `ijkl-minl-njmk/n1/b1` | 2.40989 ± 0.0120916 (W 0.00179408) | 4.96373 ± 0.0189894 (W 0.00312365) | 2.94467 ± 0.0102154 (W 0.0159599) | 🔵 tcontract 2.06× faster than `ttgt` | 🔵 tcontract 1.22× faster than `tblis` |  |

## tcbench, f64, 4T (CPU 0-3)

| case | plan (ms) | ttgt (ms) | tblis (ms) | vs `ttgt` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `abc-bk-akc/n1/b1` | 0.093726 ± 0.000490136 (W 0.000993393) | 0.614694 ± 0.0199895 (W 0.00741613) | 0.201722 ± 0.00236647 (W 0.00440747) | 🔵 tcontract 6.56× faster than `ttgt` | 🔵 tcontract 2.15× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-eiab-jkec/n1/b1` | 0.388223 ± 0.00490474 (W 0.00168104) | 3.52686 ± 0.0303013 (W 0.00955969) | 0.508098 ± 0.00257776 (W 0.00181482) | 🔵 tcontract 9.08× faster than `ttgt` | 🔵 tcontract 1.31× faster than `tblis` |  |
| `abcijk-eiac-jkeb/n1/b1` | 0.380254 ± 0.00317302 (W 0.00151005) | 3.85787 ± 0.0190991 (W 0.00973599) | 0.855524 ± 0.00399391 (W 0.00252989) | 🔵 tcontract 10.15× faster than `ttgt` | 🔵 tcontract 2.25× faster than `tblis` |  |
| `abcijk-eibc-jkea/n1/b1` | 0.413142 ± 0.000392263 (W 0.00190798) | 4.41502 ± 0.0321992 (W 0.0234498) | 0.530018 ± 0.000922768 (W 0.00352289) | 🔵 tcontract 10.69× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` |  |
| `abcijk-ejab-ikec/n1/b1` | 0.383304 ± 0.00184911 (W 0.00186448) | 3.32774 ± 0.0684197 (W 0.017117) | 0.991648 ± 0.00885405 (W 0.00350652) | 🔵 tcontract 8.68× faster than `ttgt` | 🔵 tcontract 2.59× faster than `tblis` |  |
| `abcijk-ejac-ikeb/n1/b1` | 0.378934 ± 0.00284457 (W 0.00111594) | 3.83482 ± 0.0263729 (W 0.0108816) | 0.824885 ± 0.00869377 (W 0.00331773) | 🔵 tcontract 10.12× faster than `ttgt` | 🔵 tcontract 2.18× faster than `tblis` |  |
| `abcijk-ejbc-ikea/n1/b1` | 0.414123 ± 0.00161878 (W 0.00127377) | 4.41907 ± 0.121997 (W 0.0346716) | 0.559606 ± 0.00285834 (W 0.00318965) | 🔵 tcontract 10.67× faster than `ttgt` | 🔵 tcontract 1.35× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ekab-ijec/n1/b1` | 0.382124 ± 0.00415046 (W 0.00234984) | 3.56432 ± 0.0536962 (W 0.0146168) | 0.503989 ± 0.00554275 (W 0.00258276) | 🔵 tcontract 9.33× faster than `ttgt` | 🔵 tcontract 1.32× faster than `tblis` |  |
| `abcijk-ekac-ijeb/n1/b1` | 0.378585 ± 0.00292629 (W 0.00160723) | 4.95451 ± 0.0965388 (W 0.0321064) | 0.850065 ± 0.00151733 (W 0.00259946) | 🔵 tcontract 13.09× faster than `ttgt` | 🔵 tcontract 2.25× faster than `tblis` |  |
| `abcijk-ekbc-ijea/n1/b1` | 0.413873 ± 0.00339893 (W 0.00284146) | 4.82526 ± 0.0527468 (W 0.0215978) | 0.558777 ± 0.00290794 (W 0.00305531) | 🔵 tcontract 11.66× faster than `ttgt` | 🔵 tcontract 1.35× faster than `tblis` |  |
| `abcijk-ijma-mkbc/n1/b1` | 0.413693 ± 0.00201967 (W 0.00184515) | 20.5079 ± 0.135247 (W 0.0145056) | 0.558906 ± 0.00487074 (W 0.00316768) | 🔵 tcontract 49.57× faster than `ttgt` | 🔵 tcontract 1.35× faster than `tblis` |  |
| `abcijk-ijmb-mkac/n1/b1` | 0.375325 ± 0.00338118 (W 0.000967879) | 19.0751 ± 0.204986 (W 0.0174786) | 0.849555 ± 0.00662125 (W 0.00245962) | 🔵 tcontract 50.82× faster than `ttgt` | 🔵 tcontract 2.26× faster than `tblis` |  |
| `abcijk-ijmc-mkab/n1/b1` | 0.381714 ± 0.00194104 (W 0.00167584) | 19.4556 ± 0.124913 (W 0.0218019) | 0.504309 ± 0.00566286 (W 0.00243304) | 🔵 tcontract 50.97× faster than `ttgt` | 🔵 tcontract 1.32× faster than `tblis` |  |
| `abcijk-ikma-mjbc/n1/b1` | 0.413103 ± 0.00127155 (W 0.00186377) | 22.5451 ± 0.425849 (W 0.0244697) | 0.561007 ± 0.00199437 (W 0.00395386) | 🔵 tcontract 54.57× faster than `ttgt` | 🔵 tcontract 1.36× faster than `tblis` |  |
| `abcijk-ikmb-mjac/n1/b1` | 0.376394 ± 0.0017185 (W 0.00173656) | 20.1538 ± 0.23041 (W 0.0593689) | 0.818516 ± 0.00842087 (W 0.00230869) | 🔵 tcontract 53.54× faster than `ttgt` | 🔵 tcontract 2.17× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 0.381334 ± 0.00136679 (W 0.00171568) | 21.0445 ± 0.272805 (W 0.0468944) | 0.990689 ± 0.0101429 (W 0.0028055) | 🔵 tcontract 55.19× faster than `ttgt` | 🔵 tcontract 2.60× faster than `tblis` |  |
| `abcijk-jkma-mibc/n1/b1` | 0.412963 ± 0.000965729 (W 0.00173686) | 73.0427 ± 16.5991 (W 0.111719) | 0.528188 ± 0.00407615 (W 0.00335325) | 🔵 tcontract 176.87× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmb-miac/n1/b1` | 0.379034 ± 0.00338255 (W 0.00131415) | 57.7731 ± 8.39005 (W 0.0345283) | 0.851065 ± 0.00767845 (W 0.00328809) | 🔵 tcontract 152.42× faster than `ttgt` | 🔵 tcontract 2.25× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmc-miab/n1/b1` | 0.389334 ± 0.00315692 (W 0.00182715) | 58.841 ± 7.85736 (W 0.0595309) | 0.508309 ± 0.00293539 (W 0.00353448) | 🔵 tcontract 151.13× faster than `ttgt` | 🔵 tcontract 1.31× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcs-rc-abrs/n1/b1` | 0.053268 ± 0.000704904 (W 0.000952843) | 0.391704 ± 0.0259248 (W 0.00119399) | 0.213551 ± 0.00365384 (W 0.00726451) | 🔵 tcontract 7.35× faster than `ttgt` | 🔵 tcontract 4.01× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abj-bka-kj/n1/b1` | 0.185092 ± 0.000557638 (W 0.00146029) | 0.682891 ± 0.00123012 (W 0.0151438) | 0.313347 ± 0.0057718 (W 0.00512395) | 🔵 tcontract 3.69× faster than `ttgt` | 🔵 tcontract 1.69× faster than `tblis` |  |
| `abjc-cbka-kj/n1/b1` | 0.124825 ± 0.00631149 (W 0.00118777) | 0.425692 ± 0.00383329 (W 0.00119354) | 0.262519 ± 0.0017762 (W 0.00363609) | 🔵 tcontract 3.41× faster than `ttgt` | 🔵 tcontract 2.10× faster than `tblis` | `!` between-start range over 5% |
| `abjc-kbac-jk/n1/b1` | 0.066967 ± 0.000165025 (W 0.000852529) | 0.47461 ± 0.00921208 (W 0.000994969) | 0.214061 ± 0.00473612 (W 0.0050622) | 🔵 tcontract 7.09× faster than `ttgt` | 🔵 tcontract 3.20× faster than `tblis` |  |
| `abjcd-dkbac-jk/n1/b1` | 0.545738 ± 0.0149083 (W 0.00279838) | 9.39148 ± 0.0260365 (W 0.0340299) | 1.40612 ± 0.0162554 (W 0.0113297) | 🔵 tcontract 17.21× faster than `ttgt` | 🔵 tcontract 2.58× faster than `tblis` | `!` between-start range over 5% |
| `abrs-qb-aqrs/n1/b1` | 0.052438 ± 0.000390683 (W 0.000635885) | 0.433262 ± 0.0253304 (W 0.00287179) | 0.216681 ± 0.00306237 (W 0.00723171) | 🔵 tcontract 8.26× faster than `ttgt` | 🔵 tcontract 4.13× faster than `tblis` | `!` between-start range over 5% |
| `adbjc-cbdka-kj/n1/b1` | 1.42104 ± 0.0243724 (W 0.0161088) | 5.64818 ± 0.0185368 (W 0.00626668) | 2.31352 ± 0.174627 (W 0.0094474) | 🔵 tcontract 3.97× faster than `ttgt` | 🔵 tcontract 1.63× faster than `tblis` | `!` between-start range over 5% |
| `ajb-kba-jk/n1/b1` | 0.133185 ± 0.00139795 (W 0.000717188) | 0.675752 ± 0.00348081 (W 0.00111818) | 0.261759 ± 0.00141812 (W 0.00571097) | 🔵 tcontract 5.07× faster than `ttgt` | 🔵 tcontract 1.97× faster than `tblis` |  |
| `ajbc-ckba-jk/n1/b1` | 0.102026 ± 0.00284363 (W 0.00104712) | 1.77813 ± 0.00649476 (W 0.00474339) | 0.24096 ± 0.000455448 (W 0.00605968) | 🔵 tcontract 17.43× faster than `ttgt` | 🔵 tcontract 2.36× faster than `tblis` | `!` between-start range over 5% |
| `ajbdc-ckbad-jk/n1/b1` | 0.555557 ± 0.016961 (W 0.0068928) | 13.1368 ± 0.0871008 (W 0.0640033) | 1.36808 ± 0.0100831 (W 0.0170584) | 🔵 tcontract 23.65× faster than `ttgt` | 🔵 tcontract 2.46× faster than `tblis` | `!` between-start range over 5% |
| `aqrs-pa-pqrs/n1/b1` | 0.035109 ± 0.000212054 (W 0.000777791) | 0.391594 ± 0.027252 (W 0.00113487) | 0.186312 ± 0.00303605 (W 0.00406539) | 🔵 tcontract 11.15× faster than `ttgt` | 🔵 tcontract 5.31× faster than `tblis` | `!` between-start range over 5% |
| `ij-ik-kj/n1/b1` | 0.277028 ± 0.00149503 (W 0.00404954) | 0.929901 ± 0.0248391 (W 0.00188781) | 0.407823 ± 0.00447369 (W 0.0056058) | 🔵 tcontract 3.36× faster than `ttgt` | 🔵 tcontract 1.47× faster than `tblis` | `!` between-start range over 5% |
| `ij-ikl-ljk/n1/b1` | 0.216711 ± 0.00344252 (W 0.00269455) | 0.49811 ± 0.0148992 (W 0.00350818) | 0.414573 ± 0.00316483 (W 0.00562655) | 🔵 tcontract 2.30× faster than `ttgt` | 🔵 tcontract 1.91× faster than `tblis` | `!` between-start range over 5% |
| `ij-kil-lkj/n1/b1` | 0.323427 ± 0.011839 (W 0.00222866) | 0.666302 ± 0.00247972 (W 0.00136751) | 0.553607 ± 0.00274972 (W 0.00432678) | 🔵 tcontract 2.06× faster than `ttgt` | 🔵 tcontract 1.71× faster than `tblis` | `!` between-start range over 5% |
| `ijk-ikl-lj/n1/b1` | 0.095966 ± 3.78594e-05 (W 0.000335365) | 0.518468 ± 0.0222311 (W 0.00136111) | 0.221931 ± 0.00324961 (W 0.00608485) | 🔵 tcontract 5.40× faster than `ttgt` | 🔵 tcontract 2.31× faster than `tblis` | `!` between-start range over 5% |
| `ijk-il-jlk/n1/b1` | 0.097576 ± 0.000502394 (W 0.000305786) | 0.612464 ± 0.0246871 (W 0.0115938) | 0.193712 ± 0.00552482 (W 0.00589108) | 🔵 tcontract 6.28× faster than `ttgt` | 🔵 tcontract 1.99× faster than `tblis` | `!` between-start range over 5% |
| `ijk-ilk-jl/n1/b1` | 0.094447 ± 0.000314977 (W 0.000298485) | 0.505559 ± 0.00206701 (W 0.00833933) | 0.203632 ± 0.00344635 (W 0.00479928) | 🔵 tcontract 5.35× faster than `ttgt` | 🔵 tcontract 2.16× faster than `tblis` |  |
| `ijk-ilk-lj/n1/b1` | 0.094946 ± 0.00105 (W 0.000843433) | 0.492889 ± 0.000352534 (W 0.000758914) | 0.22225 ± 0.00619577 (W 0.00810111) | 🔵 tcontract 5.19× faster than `ttgt` | 🔵 tcontract 2.34× faster than `tblis` | `!` between-start range over 5% |
| `ijk-ilmk-mjl/n1/b1` | 0.044628 ± 0.000572917 (W 0.00154652) | 0.23204 ± 0.000403436 (W 0.000947211) | 0.158074 ± 0.00202802 (W 0.0047334) | 🔵 tcontract 5.20× faster than `ttgt` | 🔵 tcontract 3.54× faster than `tblis` |  |
| `ijkl-imjn-lnkm/n1/b1` | 0.521788 ± 0.00247685 (W 0.00218925) | 1.3921 ± 0.00791893 (W 0.00212764) | 0.690941 ± 0.00617607 (W 0.00628568) | 🔵 tcontract 2.67× faster than `ttgt` | 🔵 tcontract 1.32× faster than `tblis` |  |
| `ijkl-imjn-nlmk/n1/b1` | 0.510149 ± 0.00117554 (W 0.00170018) | 1.39761 ± 0.00655768 (W 0.0014414) | 0.693821 ± 0.00608072 (W 0.00430355) | 🔵 tcontract 2.74× faster than `ttgt` | 🔵 tcontract 1.36× faster than `tblis` |  |
| `ijkl-imkn-jnlm/n1/b1` | 0.501749 ± 0.00156142 (W 0.00128853) | 1.39981 ± 0.00658141 (W 0.00211386) | 0.693221 ± 0.00471721 (W 0.00354842) | 🔵 tcontract 2.79× faster than `ttgt` | 🔵 tcontract 1.38× faster than `tblis` |  |
| `ijkl-imkn-njml/n1/b1` | 0.506089 ± 0.00150204 (W 0.00197915) | 1.41116 ± 0.0238069 (W 0.00277517) | 0.700621 ± 0.00741407 (W 0.00573687) | 🔵 tcontract 2.79× faster than `ttgt` | 🔵 tcontract 1.38× faster than `tblis` |  |
| `ijkl-imln-jnkm/n1/b1` | 0.501429 ± 0.00238475 (W 0.00169543) | 1.39822 ± 0.00549217 (W 0.00192881) | 0.666612 ± 0.0036855 (W 0.00477481) | 🔵 tcontract 2.79× faster than `ttgt` | 🔵 tcontract 1.33× faster than `tblis` |  |
| `ijkl-imln-njmk/n1/b1` | 0.505409 ± 0.00135545 (W 0.00165541) | 1.40284 ± 0.00400942 (W 0.0068225) | 0.676252 ± 0.0051307 (W 0.0053937) | 🔵 tcontract 2.78× faster than `ttgt` | 🔵 tcontract 1.34× faster than `tblis` |  |
| `ijkl-imnj-nlkm/n1/b1` | 0.508259 ± 0.000294806 (W 0.00153204) | 1.39675 ± 0.00499327 (W 0.00252985) | 0.71378 ± 0.00843843 (W 0.00555911) | 🔵 tcontract 2.75× faster than `ttgt` | 🔵 tcontract 1.40× faster than `tblis` |  |
| `ijkl-imnk-njml/n1/b1` | 0.506689 ± 0.000533573 (W 0.00199875) | 1.39813 ± 0.0102642 (W 0.00425843) | 0.695471 ± 0.00216973 (W 0.00705126) | 🔵 tcontract 2.76× faster than `ttgt` | 🔵 tcontract 1.37× faster than `tblis` |  |
| `ijkl-minj-nlmk/n1/b1` | 0.633243 ± 0.000524325 (W 0.00127338) | 1.71526 ± 0.0077108 (W 0.00441985) | 0.826586 ± 0.00677319 (W 0.00575236) | 🔵 tcontract 2.71× faster than `ttgt` | 🔵 tcontract 1.31× faster than `tblis` |  |
| `ijkl-mink-jnlm/n1/b1` | 0.602565 ± 0.000720162 (W 0.00143351) | 1.65365 ± 0.0042659 (W 0.002209) | 0.816157 ± 0.00124302 (W 0.00409041) | 🔵 tcontract 2.74× faster than `ttgt` | 🔵 tcontract 1.35× faster than `tblis` |  |
| `ijkl-minl-njmk/n1/b1` | 0.623734 ± 0.0019903 (W 0.00147546) | 1.72014 ± 0.00599422 (W 0.00327549) | 0.803367 ± 0.0017125 (W 0.00633547) | 🔵 tcontract 2.76× faster than `ttgt` | 🔵 tcontract 1.29× faster than `tblis` |  |

## tcbench, c64, 1T (CPU 0)

| case | plan (ms) | ttgt (ms) | tblis (ms) | vs `ttgt` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `abc-bk-akc/n1/b1` | 1.33211 ± 0.00679927 (W 0.00101348) | 2.71373 ± 0.00106521 (W 0.00348574) | 1.68187 ± 0.00243555 (W 0.00407434) | 🔵 tcontract 2.04× faster than `ttgt` | 🔵 tcontract 1.26× faster than `tblis` |  |
| `abcijk-eiab-jkec/n1/b1` | 6.13927 ± 0.00326501 (W 0.0139031) | 22.8211 ± 0.0775813 (W 0.0537001) | 6.31891 ± 0.0150945 (W 0.00770132) | 🔵 tcontract 3.72× faster than `ttgt` | · |  |
| `abcijk-eiac-jkeb/n1/b1` | 6.07794 ± 0.0223392 (W 0.00409364) | 22.7239 ± 0.0532628 (W 0.0628087) | 6.41038 ± 0.0125673 (W 0.00600029) | 🔵 tcontract 3.74× faster than `ttgt` | 🔵 tcontract 1.05× faster than `tblis` |  |
| `abcijk-eibc-jkea/n1/b1` | 6.19003 ± 0.0107715 (W 0.00652893) | 24.4646 ± 0.0393545 (W 0.0675828) | 6.01295 ± 0.0608526 (W 0.0116494) | 🔵 tcontract 3.95× faster than `ttgt` | · |  |
| `abcijk-ejab-ikec/n1/b1` | 6.09031 ± 0.0117354 (W 0.00936235) | 22.6897 ± 0.0324957 (W 0.0548202) | 9.01305 ± 0.0142367 (W 0.0134963) | 🔵 tcontract 3.73× faster than `ttgt` | 🔵 tcontract 1.48× faster than `tblis` |  |
| `abcijk-ejac-ikeb/n1/b1` | 6.07984 ± 0.00820014 (W 0.0100928) | 22.67 ± 0.0678396 (W 0.0915009) | 8.23376 ± 0.00579968 (W 0.0167268) | 🔵 tcontract 3.73× faster than `ttgt` | 🔵 tcontract 1.35× faster than `tblis` |  |
| `abcijk-ejbc-ikea/n1/b1` | 6.20653 ± 0.00322447 (W 0.00533477) | 24.8077 ± 0.0271676 (W 0.0495933) | 6.8809 ± 0.0784966 (W 0.00761712) | 🔵 tcontract 4.00× faster than `ttgt` | 🔵 tcontract 1.11× faster than `tblis` |  |
| `abcijk-ekab-ijec/n1/b1` | 6.09645 ± 0.0155288 (W 0.0106123) | 22.7233 ± 0.0315964 (W 0.0306863) | 6.38012 ± 0.0128976 (W 0.00699387) | 🔵 tcontract 3.73× faster than `ttgt` | · |  |
| `abcijk-ekac-ijeb/n1/b1` | 6.07048 ± 0.00456975 (W 0.00524072) | 23.4154 ± 0.124226 (W 0.0551452) | 6.4127 ± 0.0163301 (W 0.00515459) | 🔵 tcontract 3.86× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` |  |
| `abcijk-ekbc-ijea/n1/b1` | 6.20499 ± 0.00924328 (W 0.00268487) | 25.4405 ± 0.120799 (W 0.0501493) | 6.85572 ± 0.0762111 (W 0.00576768) | 🔵 tcontract 4.10× faster than `ttgt` | 🔵 tcontract 1.10× faster than `tblis` |  |
| `abcijk-ijma-mkbc/n1/b1` | 6.20859 ± 0.00859046 (W 0.00720446) | 38.1005 ± 0.13332 (W 0.10823) | 6.85105 ± 0.0185318 (W 0.00927824) | 🔵 tcontract 6.14× faster than `ttgt` | 🔵 tcontract 1.10× faster than `tblis` |  |
| `abcijk-ijmb-mkac/n1/b1` | 6.07186 ± 0.00545638 (W 0.00380084) | 38.4485 ± 0.0820991 (W 0.060891) | 6.40317 ± 0.0332853 (W 0.0074121) | 🔵 tcontract 6.33× faster than `ttgt` | 🔵 tcontract 1.05× faster than `tblis` |  |
| `abcijk-ijmc-mkab/n1/b1` | 6.08745 ± 0.00351999 (W 0.00944454) | 40.31 ± 0.0856095 (W 0.117309) | 6.37139 ± 0.0133043 (W 0.0108885) | 🔵 tcontract 6.62× faster than `ttgt` | · |  |
| `abcijk-ikma-mjbc/n1/b1` | 6.20497 ± 0.00239063 (W 0.00732973) | 40.4668 ± 0.644191 (W 0.0796505) | 6.94463 ± 0.0599896 (W 0.0146934) | 🔵 tcontract 6.52× faster than `ttgt` | 🔵 tcontract 1.12× faster than `tblis` |  |
| `abcijk-ikmb-mjac/n1/b1` | 6.06676 ± 0.00756331 (W 0.00505139) | 39.5721 ± 0.283669 (W 0.121205) | 8.21779 ± 0.00594282 (W 0.0089654) | 🔵 tcontract 6.52× faster than `ttgt` | 🔵 tcontract 1.35× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 6.09287 ± 0.0188287 (W 0.0115581) | 41.7616 ± 0.154461 (W 0.0800039) | 8.99095 ± 0.00751617 (W 0.00722701) | 🔵 tcontract 6.85× faster than `ttgt` | 🔵 tcontract 1.48× faster than `tblis` |  |
| `abcijk-jkma-mibc/n1/b1` | 6.19285 ± 0.0063849 (W 0.0079653) | 63.9951 ± 0.301523 (W 0.0882549) | 6.09109 ± 0.0243975 (W 0.0108628) | 🔵 tcontract 10.33× faster than `ttgt` | · |  |
| `abcijk-jkmb-miac/n1/b1` | 6.08083 ± 0.00465618 (W 0.00539045) | 63.6565 ± 0.671705 (W 0.0718712) | 6.42594 ± 0.0158753 (W 0.0075102) | 🔵 tcontract 10.47× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` |  |
| `abcijk-jkmc-miab/n1/b1` | 6.11746 ± 0.0186946 (W 0.00997465) | 63.5137 ± 0.301924 (W 0.0872614) | 6.29947 ± 0.00705877 (W 0.00886377) | 🔵 tcontract 10.38× faster than `ttgt` | · |  |
| `abcs-rc-abrs/n1/b1` | 0.590436 ± 0.000519711 (W 0.00114989) | 1.18503 ± 0.00233768 (W 0.0020609) | 1.02865 ± 0.00228445 (W 0.00849272) | 🔵 tcontract 2.01× faster than `ttgt` | 🔵 tcontract 1.74× faster than `tblis` |  |
| `abj-bka-kj/n1/b1` | 2.4907 ± 0.00551414 (W 0.000740691) | 3.82632 ± 0.0141404 (W 0.00545107) | 2.43122 ± 0.0042228 (W 0.00219509) | 🔵 tcontract 1.54× faster than `ttgt` | · |  |
| `abjc-cbka-kj/n1/b1` | 1.44781 ± 0.00466162 (W 0.00498575) | 1.66795 ± 0.00452966 (W 0.00293134) | 1.32201 ± 0.015131 (W 0.00128495) | 🔵 tcontract 1.15× faster than `ttgt` | 🔴 tcontract 1.10× slower than `tblis` |  |
| `abjc-kbac-jk/n1/b1` | 0.72924 ± 0.00173866 (W 0.000638319) | 1.55713 ± 0.016206 (W 0.00114413) | 1.04857 ± 0.00599814 (W 0.00838614) | 🔵 tcontract 2.14× faster than `ttgt` | 🔵 tcontract 1.44× faster than `tblis` |  |
| `abjcd-dkbac-jk/n1/b1` | 4.96306 ± 0.125602 (W 0.0225814) | 16.4152 ± 0.254095 (W 0.0837467) | 7.69287 ± 0.303014 (W 0.0618582) | 🔵 tcontract 3.31× faster than `ttgt` | 🔵 tcontract 1.55× faster than `tblis` | `!` between-start range over 5% |
| `abrs-qb-aqrs/n1/b1` | 0.562366 ± 0.000763132 (W 0.0013734) | 1.19813 ± 0.00166496 (W 0.0014183) | 1.02903 ± 0.00682263 (W 0.00905955) | 🔵 tcontract 2.13× faster than `ttgt` | 🔵 tcontract 1.83× faster than `tblis` |  |
| `adbjc-cbdka-kj/n1/b1` | 9.35474 ± 0.36424 (W 0.0679033) | 13.3569 ± 0.00972064 (W 0.0102762) | 9.47566 ± 0.452156 (W 0.139735) | 🔵 tcontract 1.43× faster than `ttgt` | · | `!` between-start range over 5%; `p` position effect over 5% |
| `ajb-kba-jk/n1/b1` | 1.81559 ± 0.00906032 (W 0.000897445) | 3.90379 ± 0.00966765 (W 0.00259239) | 2.25623 ± 0.0286956 (W 0.00596841) | 🔵 tcontract 2.15× faster than `ttgt` | 🔵 tcontract 1.24× faster than `tblis` |  |
| `ajbc-ckba-jk/n1/b1` | 0.881713 ± 0.00452997 (W 0.00223356) | 2.84683 ± 0.00942428 (W 0.00213474) | 1.12728 ± 0.0226184 (W 0.00227267) | 🔵 tcontract 3.23× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` |  |
| `ajbdc-ckbad-jk/n1/b1` | 5.32863 ± 0.0404558 (W 0.0153802) | 19.8641 ± 0.324591 (W 0.104439) | 7.63881 ± 0.203759 (W 0.0352603) | 🔵 tcontract 3.73× faster than `ttgt` | 🔵 tcontract 1.43× faster than `tblis` |  |
| `aqrs-pa-pqrs/n1/b1` | 0.633073 ± 0.00264649 (W 0.000923518) | 1.15058 ± 0.00310517 (W 0.0015449) | 0.73226 ± 0.00635047 (W 0.00155739) | 🔵 tcontract 1.82× faster than `ttgt` | 🔵 tcontract 1.16× faster than `tblis` |  |
| `ij-ik-kj/n1/b1` | 4.49961 ± 0.00787904 (W 0.00319363) | 8.69644 ± 0.0115945 (W 0.0048313) | 4.70701 ± 0.00583089 (W 0.00405944) | 🔵 tcontract 1.93× faster than `ttgt` | · |  |
| `ij-ikl-ljk/n1/b1` | 1.42165 ± 0.00219657 (W 0.00155908) | 2.63226 ± 0.0128028 (W 0.00545419) | 1.90771 ± 0.0161996 (W 0.00448386) | 🔵 tcontract 1.85× faster than `ttgt` | 🔵 tcontract 1.34× faster than `tblis` |  |
| `ij-kil-lkj/n1/b1` | 2.04887 ± 0.00123485 (W 0.00450854) | 3.78045 ± 0.0280428 (W 0.039832) | 2.6913 ± 0.00746224 (W 0.00689472) | 🔵 tcontract 1.85× faster than `ttgt` | 🔵 tcontract 1.31× faster than `tblis` |  |
| `ijk-ikl-lj/n1/b1` | 1.30648 ± 0.00823806 (W 0.000786206) | 2.68451 ± 0.00237855 (W 0.00159695) | 1.66909 ± 0.0110883 (W 0.00833715) | 🔵 tcontract 2.05× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` |  |
| `ijk-il-jlk/n1/b1` | 1.39347 ± 0.00162004 (W 0.00110016) | 2.71708 ± 0.00748893 (W 0.00325506) | 1.43852 ± 0.00336715 (W 0.00153548) | 🔵 tcontract 1.95× faster than `ttgt` | · |  |
| `ijk-ilk-jl/n1/b1` | 1.33295 ± 0.00958663 (W 0.000719944) | 2.72144 ± 0.00147331 (W 0.00108893) | 1.68388 ± 0.00623755 (W 0.00517687) | 🔵 tcontract 2.04× faster than `ttgt` | 🔵 tcontract 1.26× faster than `tblis` |  |
| `ijk-ilk-lj/n1/b1` | 1.31225 ± 0.00472965 (W 0.00148477) | 2.70685 ± 0.00311689 (W 0.00179417) | 1.68493 ± 0.00770484 (W 0.00363742) | 🔵 tcontract 2.06× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` |  |
| `ijk-ilmk-mjl/n1/b1` | 0.492869 ± 0.001905 (W 0.00115944) | 1.0288 ± 0.0011739 (W 0.00118254) | 0.890323 ± 0.00600623 (W 0.00403805) | 🔵 tcontract 2.09× faster than `ttgt` | 🔵 tcontract 1.81× faster than `tblis` |  |
| `ijkl-imjn-lnkm/n1/b1` | 7.75774 ± 0.00858939 (W 0.0048324) | 14.8648 ± 0.00153709 (W 0.0104817) | 8.60685 ± 0.0229036 (W 0.00701771) | 🔵 tcontract 1.92× faster than `ttgt` | 🔵 tcontract 1.11× faster than `tblis` |  |
| `ijkl-imjn-nlmk/n1/b1` | 7.64893 ± 0.00366391 (W 0.00586779) | 14.7548 ± 0.0169416 (W 0.00243887) | 8.8537 ± 0.0336909 (W 0.00319478) | 🔵 tcontract 1.93× faster than `ttgt` | 🔵 tcontract 1.16× faster than `tblis` |  |
| `ijkl-imkn-jnlm/n1/b1` | 7.70281 ± 0.0183764 (W 0.00345277) | 14.8743 ± 0.0119275 (W 0.0224674) | 8.58985 ± 0.0297309 (W 0.0107538) | 🔵 tcontract 1.93× faster than `ttgt` | 🔵 tcontract 1.12× faster than `tblis` |  |
| `ijkl-imkn-njml/n1/b1` | 7.63951 ± 0.0100212 (W 0.00584078) | 14.7336 ± 0.0129063 (W 0.0118894) | 8.84596 ± 0.0250918 (W 0.00477527) | 🔵 tcontract 1.93× faster than `ttgt` | 🔵 tcontract 1.16× faster than `tblis` |  |
| `ijkl-imln-jnkm/n1/b1` | 7.68348 ± 0.0180017 (W 0.00232717) | 14.8835 ± 0.017009 (W 0.0106891) | 8.00898 ± 0.0321417 (W 0.00267471) | 🔵 tcontract 1.94× faster than `ttgt` | · |  |
| `ijkl-imln-njmk/n1/b1` | 7.63011 ± 0.00957724 (W 0.0022723) | 14.7531 ± 0.00278733 (W 0.00638537) | 8.06708 ± 0.0238002 (W 0.00299507) | 🔵 tcontract 1.93× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` |  |
| `ijkl-imnj-nlkm/n1/b1` | 7.6536 ± 0.0194162 (W 0.00382457) | 14.7293 ± 0.0211399 (W 0.00433655) | 8.86335 ± 0.0345313 (W 0.00658995) | 🔵 tcontract 1.92× faster than `ttgt` | 🔵 tcontract 1.16× faster than `tblis` |  |
| `ijkl-imnk-njml/n1/b1` | 7.62779 ± 0.00362453 (W 0.00504805) | 14.7479 ± 0.0128026 (W 0.00549969) | 8.84825 ± 0.00832496 (W 0.00421984) | 🔵 tcontract 1.93× faster than `ttgt` | 🔵 tcontract 1.16× faster than `tblis` |  |
| `ijkl-minj-nlmk/n1/b1` | 9.43235 ± 0.0100777 (W 0.00138992) | 17.8285 ± 0.0310702 (W 0.00596006) | 10.7484 ± 0.0317448 (W 0.00299228) | 🔵 tcontract 1.89× faster than `ttgt` | 🔵 tcontract 1.14× faster than `tblis` |  |
| `ijkl-mink-jnlm/n1/b1` | 9.1894 ± 0.0110781 (W 0.00306123) | 17.8719 ± 0.0249057 (W 0.0118438) | 10.4432 ± 0.0103317 (W 0.00593968) | 🔵 tcontract 1.94× faster than `ttgt` | 🔵 tcontract 1.14× faster than `tblis` |  |
| `ijkl-minl-njmk/n1/b1` | 9.39248 ± 0.0260037 (W 0.00562814) | 17.8346 ± 0.00831574 (W 0.019731) | 9.71866 ± 0.0390458 (W 0.00249225) | 🔵 tcontract 1.90× faster than `ttgt` | · |  |

## tcbench, c64, 4T (CPU 0-3)

| case | plan (ms) | ttgt (ms) | tblis (ms) | vs `ttgt` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `abc-bk-akc/n1/b1` | 0.345716 ± 0.00195809 (W 0.00103368) | 1.10557 ± 0.0156787 (W 0.0228718) | 0.448331 ± 0.00158689 (W 0.00183747) | 🔵 tcontract 3.20× faster than `ttgt` | 🔵 tcontract 1.30× faster than `tblis` |  |
| `abcijk-eiab-jkec/n1/b1` | 1.55659 ± 0.00424308 (W 0.00244575) | 16.0819 ± 0.113744 (W 0.0451613) | 1.64728 ± 0.00451975 (W 0.00416697) | 🔵 tcontract 10.33× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` |  |
| `abcijk-eiac-jkeb/n1/b1` | 1.55404 ± 0.00152893 (W 0.00216768) | 16.0816 ± 0.140147 (W 0.10524) | 1.75917 ± 0.00275758 (W 0.00325938) | 🔵 tcontract 10.35× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-eibc-jkea/n1/b1` | 1.58539 ± 0.00180943 (W 0.00328722) | 17.6007 ± 0.116102 (W 0.0595304) | 1.62906 ± 0.00902171 (W 0.00654227) | 🔵 tcontract 11.10× faster than `ttgt` | · |  |
| `abcijk-ejab-ikec/n1/b1` | 1.54347 ± 0.00181913 (W 0.0017522) | 15.7502 ± 0.0804429 (W 0.0721147) | 2.31401 ± 0.0011694 (W 0.00353729) | 🔵 tcontract 10.20× faster than `ttgt` | 🔵 tcontract 1.50× faster than `tblis` |  |
| `abcijk-ejac-ikeb/n1/b1` | 1.55352 ± 0.00220048 (W 0.00123504) | 15.802 ± 0.12244 (W 0.0649941) | 2.11211 ± 0.00751175 (W 0.00529534) | 🔵 tcontract 10.17× faster than `ttgt` | 🔵 tcontract 1.36× faster than `tblis` |  |
| `abcijk-ejbc-ikea/n1/b1` | 1.58533 ± 0.00451221 (W 0.00219053) | 17.8967 ± 0.0730495 (W 0.0362573) | 1.81528 ± 0.00644245 (W 0.00518727) | 🔵 tcontract 11.29× faster than `ttgt` | 🔵 tcontract 1.15× faster than `tblis` |  |
| `abcijk-ekab-ijec/n1/b1` | 1.54159 ± 0.0030378 (W 0.00211103) | 15.8026 ± 0.135417 (W 0.0913532) | 1.65715 ± 0.00384761 (W 0.00321401) | 🔵 tcontract 10.25× faster than `ttgt` | 🔵 tcontract 1.07× faster than `tblis` |  |
| `abcijk-ekac-ijeb/n1/b1` | 1.55312 ± 0.00121604 (W 0.00197718) | 16.4294 ± 0.0966344 (W 0.0481036) | 1.79536 ± 0.00280459 (W 0.00550922) | 🔵 tcontract 10.58× faster than `ttgt` | 🔵 tcontract 1.16× faster than `tblis` |  |
| `abcijk-ekbc-ijea/n1/b1` | 1.58758 ± 0.00124396 (W 0.00245695) | 18.0358 ± 0.264894 (W 0.0518146) | 1.80096 ± 0.0097593 (W 0.00413622) | 🔵 tcontract 11.36× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ijma-mkbc/n1/b1` | 1.58385 ± 0.00454041 (W 0.0027889) | 31.3212 ± 0.0402991 (W 0.046306) | 1.81398 ± 0.0115513 (W 0.00659967) | 🔵 tcontract 19.78× faster than `ttgt` | 🔵 tcontract 1.15× faster than `tblis` |  |
| `abcijk-ijmb-mkac/n1/b1` | 1.55238 ± 0.00151847 (W 0.00266908) | 31.6136 ± 0.0907548 (W 0.0369916) | 1.7972 ± 0.00236157 (W 0.00408762) | 🔵 tcontract 20.36× faster than `ttgt` | 🔵 tcontract 1.16× faster than `tblis` |  |
| `abcijk-ijmc-mkab/n1/b1` | 1.54028 ± 0.00307074 (W 0.00134262) | 33.6784 ± 0.153572 (W 0.113863) | 1.65533 ± 0.00622367 (W 0.00346409) | 🔵 tcontract 21.87× faster than `ttgt` | 🔵 tcontract 1.07× faster than `tblis` |  |
| `abcijk-ikma-mjbc/n1/b1` | 1.584 ± 6.08276e-05 (W 0.00157853) | 33.8272 ± 0.048415 (W 0.0834295) | 1.81814 ± 0.0312331 (W 0.0069399) | 🔵 tcontract 21.36× faster than `ttgt` | 🔵 tcontract 1.15× faster than `tblis` |  |
| `abcijk-ikmb-mjac/n1/b1` | 1.55376 ± 0.00109569 (W 0.00195956) | 32.9224 ± 0.0461096 (W 0.0661786) | 2.11321 ± 0.0138892 (W 0.00563512) | 🔵 tcontract 21.19× faster than `ttgt` | 🔵 tcontract 1.36× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 1.53883 ± 0.00257286 (W 0.00282035) | 35.2473 ± 0.0338432 (W 0.102131) | 2.31462 ± 0.0014695 (W 0.0032812) | 🔵 tcontract 22.91× faster than `ttgt` | 🔵 tcontract 1.50× faster than `tblis` |  |
| `abcijk-jkma-mibc/n1/b1` | 1.58249 ± 0.000205264 (W 0.00238494) | 58.6027 ± 5.18261 (W 0.121767) | 1.633 ± 0.00827761 (W 0.00503152) | 🔵 tcontract 37.03× faster than `ttgt` | · | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmb-miac/n1/b1` | 1.55495 ± 0.00297875 (W 0.00161855) | 59.5308 ± 4.35113 (W 0.0594301) | 1.75858 ± 0.00242674 (W 0.0035597) | 🔵 tcontract 38.28× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmc-miab/n1/b1` | 1.55516 ± 0.00388821 (W 0.00277504) | 58.4674 ± 3.19492 (W 0.108092) | 1.64445 ± 0.00281628 (W 0.0016451) | 🔵 tcontract 37.60× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` | `!` between-start range over 5% |
| `abcs-rc-abrs/n1/b1` | 0.160274 ± 0.00108279 (W 0.00111567) | 0.571706 ± 0.00108669 (W 0.00190129) | 0.316757 ± 0.00320433 (W 0.00209666) | 🔵 tcontract 3.57× faster than `ttgt` | 🔵 tcontract 1.98× faster than `tblis` |  |
| `abj-bka-kj/n1/b1` | 0.523188 ± 0.00119081 (W 0.00152734) | 1.45753 ± 0.00508787 (W 0.00268537) | 0.655763 ± 0.00299305 (W 0.00273644) | 🔵 tcontract 2.79× faster than `ttgt` | 🔵 tcontract 1.25× faster than `tblis` |  |
| `abjc-cbka-kj/n1/b1` | 0.288568 ± 0.00373023 (W 0.0022425) | 0.913852 ± 0.023323 (W 0.00229082) | 0.400723 ± 0.00281128 (W 0.00193769) | 🔵 tcontract 3.17× faster than `ttgt` | 🔵 tcontract 1.39× faster than `tblis` |  |
| `abjc-kbac-jk/n1/b1` | 0.198921 ± 0.000990017 (W 0.00111942) | 0.835666 ± 0.00393474 (W 0.00158034) | 0.326086 ± 0.00215007 (W 0.00220045) | 🔵 tcontract 4.20× faster than `ttgt` | 🔵 tcontract 1.64× faster than `tblis` |  |
| `abjcd-dkbac-jk/n1/b1` | 1.45855 ± 0.00936371 (W 0.00382854) | 13.0323 ± 0.219144 (W 0.0287551) | 2.5108 ± 0.010763 (W 0.0310379) | 🔵 tcontract 8.94× faster than `ttgt` | 🔵 tcontract 1.72× faster than `tblis` |  |
| `abrs-qb-aqrs/n1/b1` | 0.152353 ± 0.000745433 (W 0.000555286) | 0.623534 ± 0.001535 (W 0.00292492) | 0.314877 ± 0.0028736 (W 0.0024253) | 🔵 tcontract 4.09× faster than `ttgt` | 🔵 tcontract 2.07× faster than `tblis` |  |
| `adbjc-cbdka-kj/n1/b1` | 3.16101 ± 0.0306889 (W 0.0347375) | 9.42307 ± 0.221654 (W 0.017331) | 3.05974 ± 0.127126 (W 0.0626435) | 🔵 tcontract 2.98× faster than `ttgt` | · | `!` between-start range over 5% |
| `ajb-kba-jk/n1/b1` | 0.469571 ± 0.00125734 (W 0.00179127) | 1.65479 ± 0.00893383 (W 0.00258646) | 0.597716 ± 0.00112766 (W 0.00349331) | 🔵 tcontract 3.52× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `ajbc-ckba-jk/n1/b1` | 0.23932 ± 0.00114473 (W 0.00141316) | 2.08402 ± 0.00582818 (W 0.00588482) | 0.352955 ± 0.00369722 (W 0.00152181) | 🔵 tcontract 8.71× faster than `ttgt` | 🔵 tcontract 1.47× faster than `tblis` |  |
| `ajbdc-ckbad-jk/n1/b1` | 1.55642 ± 0.0225845 (W 0.00675296) | 16.3331 ± 0.186271 (W 0.0935266) | 2.4382 ± 0.0436269 (W 0.0264863) | 🔵 tcontract 10.49× faster than `ttgt` | 🔵 tcontract 1.57× faster than `tblis` |  |
| `aqrs-pa-pqrs/n1/b1` | 0.266059 ± 0.00105 (W 0.00148814) | 0.528738 ± 0.0160085 (W 0.00134541) | 0.24168 ± 0.00274952 (W 0.00085612) | 🔵 tcontract 1.99× faster than `ttgt` | 🔴 tcontract 1.10× slower than `tblis` | `!` between-start range over 5% |
| `ij-ik-kj/n1/b1` | 1.15676 ± 0.00132429 (W 0.00219047) | 2.4568 ± 0.010508 (W 0.00165986) | 1.2367 ± 0.000641431 (W 0.00211281) | 🔵 tcontract 2.12× faster than `ttgt` | 🔵 tcontract 1.07× faster than `tblis` |  |
| `ij-ikl-ljk/n1/b1` | 0.578086 ± 0.00101491 (W 0.00172692) | 0.96147 ± 0.0267827 (W 0.000966654) | 0.697541 ± 0.00181052 (W 0.00232214) | 🔵 tcontract 1.66× faster than `ttgt` | 🔵 tcontract 1.21× faster than `tblis` | `!` between-start range over 5% |
| `ij-kil-lkj/n1/b1` | 0.802317 ± 0.00496774 (W 0.00395898) | 1.46959 ± 0.00897114 (W 0.0104271) | 0.946181 ± 0.0105276 (W 0.00113271) | 🔵 tcontract 1.83× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `ijk-ikl-lj/n1/b1` | 0.339285 ± 0.00109821 (W 0.00183699) | 0.98155 ± 0.00539488 (W 0.00117186) | 0.449962 ± 0.00200799 (W 0.00459387) | 🔵 tcontract 2.89× faster than `ttgt` | 🔵 tcontract 1.33× faster than `tblis` |  |
| `ijk-il-jlk/n1/b1` | 0.505109 ± 0.00415264 (W 0.00106202) | 1.11333 ± 0.00600214 (W 0.0193068) | 0.390694 ± 0.000642988 (W 0.00117253) | 🔵 tcontract 2.20× faster than `ttgt` | 🔴 tcontract 1.29× slower than `tblis` |  |
| `ijk-ilk-jl/n1/b1` | 0.346526 ± 0.00110639 (W 0.00155405) | 1.06639 ± 0.00439503 (W 0.00114103) | 0.449891 ± 0.00133372 (W 0.00118394) | 🔵 tcontract 3.08× faster than `ttgt` | 🔵 tcontract 1.30× faster than `tblis` |  |
| `ijk-ilk-lj/n1/b1` | 0.342616 ± 0.000963753 (W 0.00200831) | 1.00794 ± 0.00419711 (W 0.00134259) | 0.447511 ± 0.000857496 (W 0.00243818) | 🔵 tcontract 2.94× faster than `ttgt` | 🔵 tcontract 1.31× faster than `tblis` |  |
| `ijk-ilmk-mjl/n1/b1` | 0.146534 ± 0.000757914 (W 0.00157094) | 0.438522 ± 0.00117222 (W 0.000573686) | 0.249869 ± 0.00176283 (W 0.00242805) | 🔵 tcontract 2.99× faster than `ttgt` | 🔵 tcontract 1.71× faster than `tblis` |  |
| `ijkl-imjn-lnkm/n1/b1` | 2.10475 ± 0.00615594 (W 0.00189343) | 4.22713 ± 0.0154852 (W 0.00762852) | 2.26905 ± 0.00380281 (W 0.00355946) | 🔵 tcontract 2.01× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `ijkl-imjn-nlmk/n1/b1` | 2.07755 ± 0.0018664 (W 0.00217821) | 4.10993 ± 0.015623 (W 0.00257062) | 2.37255 ± 0.00175913 (W 0.00222127) | 🔵 tcontract 1.98× faster than `ttgt` | 🔵 tcontract 1.14× faster than `tblis` |  |
| `ijkl-imkn-jnlm/n1/b1` | 2.0827 ± 0.00261117 (W 0.000531197) | 4.25235 ± 0.0158651 (W 0.00612139) | 2.26166 ± 0.00249217 (W 0.00232861) | 🔵 tcontract 2.04× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `ijkl-imkn-njml/n1/b1` | 2.06401 ± 0.0019377 (W 0.00142051) | 4.10921 ± 0.0115025 (W 0.00207733) | 2.36282 ± 0.00102295 (W 0.00143721) | 🔵 tcontract 1.99× faster than `ttgt` | 🔵 tcontract 1.14× faster than `tblis` |  |
| `ijkl-imln-jnkm/n1/b1` | 2.0829 ± 0.00489291 (W 0.00131514) | 4.2508 ± 0.00810108 (W 0.00744637) | 2.1153 ± 0.011382 (W 0.000896859) | 🔵 tcontract 2.04× faster than `ttgt` | · |  |
| `ijkl-imln-njmk/n1/b1` | 2.06085 ± 0.00345437 (W 0.00264175) | 4.10894 ± 0.00694257 (W 0.00268208) | 2.16236 ± 0.00790596 (W 0.000908029) | 🔵 tcontract 1.99× faster than `ttgt` | · |  |
| `ijkl-imnj-nlkm/n1/b1` | 2.06989 ± 0.0045619 (W 0.00174185) | 4.10162 ± 0.0032853 (W 0.00306016) | 2.36643 ± 0.00222991 (W 0.00124165) | 🔵 tcontract 1.98× faster than `ttgt` | 🔵 tcontract 1.14× faster than `tblis` |  |
| `ijkl-imnk-njml/n1/b1` | 2.05846 ± 0.00256075 (W 0.00080439) | 4.10162 ± 0.0104708 (W 0.00284583) | 2.36197 ± 0.00274274 (W 0.00187143) | 🔵 tcontract 1.99× faster than `ttgt` | 🔵 tcontract 1.15× faster than `tblis` |  |
| `ijkl-minj-nlmk/n1/b1` | 2.57102 ± 0.00551286 (W 0.00208546) | 5.00236 ± 0.0152384 (W 0.0051788) | 2.86505 ± 0.0116375 (W 0.00198409) | 🔵 tcontract 1.95× faster than `ttgt` | 🔵 tcontract 1.11× faster than `tblis` |  |
| `ijkl-mink-jnlm/n1/b1` | 2.47799 ± 0.00210969 (W 0.00187051) | 5.12458 ± 0.0157117 (W 0.00517604) | 2.75762 ± 0.005344 (W 0.00157818) | 🔵 tcontract 2.07× faster than `ttgt` | 🔵 tcontract 1.11× faster than `tblis` |  |
| `ijkl-minl-njmk/n1/b1` | 2.54061 ± 0.00115005 (W 0.00128992) | 5.00723 ± 0.0163169 (W 0.00869693) | 2.59932 ± 0.00475326 (W 0.00209641) | 🔵 tcontract 1.97× faster than `ttgt` | · |  |

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
