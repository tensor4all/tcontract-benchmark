# `per-shape` on `zen5-cpu`

- tcontract-rs commit: `61a04eb1562c671775d1ce254212a598334d3dbb`
- features: `tblis`
- tprims rows: `tprims` (the provider in the measured revision; see library above)
- external providers: `tblis` 2.0 @ `b16a732939d8454021e0a0f0097cf1cc1dd3ab19` tag `v2.0-beta2` sha256 `de00bf1552c15f9c4a5d3157f02c149b81aef0909107c51cbb54ba4b8e9b5827` (TBLIS 2.0, configuration zen3; bundled BLIS 358e689cadd6757f564a2992cf46a2f7d6fa6bb0; built with ./configure --prefix=/home/shinaoka/projects/tensor4all/tcontract-benchmark/target/tblis-v2.0-beta2 --with-blis-config-family=zen3 (cmake, Unix Makefiles, Release); libtblis.so sha256 de00bf1552c15f9c)
- harness commit: `5eed415394a40c6b281b58e0d2c88080b81631d2`
- toolkit commit: `90fbeeb3dd2389b8a5d9bc63679f5e2bf3fc1741`
- measured binary SHA-256: `16d0d462f2cc4e607e1d6e7ff579c4f191dfc23835a7b6452ded8ef75b5e2568`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-20T08:46:27.455164Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/v2/record_run.py per-shape zen5-cpu per-shape --aa 3 --reps 5 --prime-ms 250 --external-provider-json /tmp/tblis-v2.json --label pub-61a04eb-per-shape`
- raw data: `data/v2-results/per-shape/zen5-cpu/per-shape/20261020T084358Z-pub-61a04eb-per-shape/`

## What was measured

- **Workload** — Small and large batched GEMMs, a two-step chain and the steps of a 32-site MPS chain, at fixed extents. One timed call is the whole program (a chain of pairwise steps), not one step.
  Source: The corpus is defined by `benchmarks/benchmarks/lukbench/corpus.rs` in the measured revision (`pins/tcontract-rs-v2.rev`); it carries the case definitions recorded from tensor4all/tcontract-rs#61.
  Known blind spot: Each case fixes its own dtype (f64 or c64); the suite declares both, and lukbench's census reports the wrong-dtype cells as skipped rather than dropping the case.
  Known blind spot: The declared identity is the numeric sentinel `n = 1`; the final step's real extents are the harness's own report, not the toolkit's identity.
  Known blind spot: One size per case: a ratio here says nothing about a neighbouring size, and the set is not a sweep.
  Known blind spot: `tblis` is an external baseline linked from its own prefix (`TBLIS_ROOT`, see `docs/v2-layout.md`), not the measured checkout; its revision is recorded through the campaign TBLIS collector (`scripts/tblis_providers_json.py`).
  Known blind spot: The harness's census CSV carries no corpus `group` column, so the corpus's own group labels and each case's native dtype and final-step extents are not part of this declaration; they remain facts of the recorded revision's `corpus.rs`.
- **Rows** — one row per engine in every table below:
  - `plan` — This library with its planner choosing the route per case.
    Identity: the measured tcontract-rs revision in this run's manifest (`library.commit`), pinned by `pins/tcontract-rs-v2.rev`
    As measured: `tprims` (the provider in the measured revision; see library above)
  - `packed` — This library with the packed driver forced. A diagnostic arm: it shows what the planner's other routes buy or cost on the same inputs.
    Identity: the measured tcontract-rs revision in this run's manifest (`library.commit`), pinned by `pins/tcontract-rs-v2.rev`
    As measured: `tprims` (the provider in the measured revision; see library above)
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
Spread guide (computed from this run's own rows): per-engine between-start range median 2.79%, worst 117.17% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 37 of 126 engine cells exceed 5% and carry `!`; median within-process relative SD 0.56%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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

## per-shape, f64, 1T (CPU 4)

| case | plan (ms) | packed (ms) | tblis (ms) | vs `packed` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `ij_jk_ik_f64_n64/n1/b1` | 0.017212 ± 1.0504e-05 (W 2.18701e-05) | 0.024986 ± 0.000347253 (W 6.68453e-05) | 0.04851 ± 0.000501189 (W 0.000289723) | 🔵 fork 1.45× faster than `packed` | 🔵 fork 2.82× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ij_jk_kl_il_n64/n1/b1` | 0.034475 ± 4.7085e-05 (W 6.42651e-05) | 0.049181 ± 0.000536347 (W 0.000338377) | 0.09678 ± 0.000216419 (W 0.000567273) | 🔵 fork 1.43× faster than `packed` | 🔵 fork 2.81× faster than `tblis` |  |
| `ijk_jkl_il_8x16x8/n1/b1` | 0.000832 ± 1.00167e-05 (W 6.73053e-06) | 0.005049 ± 0.00012741 (W 1.83112e-05) | 0.01622 ± 0.000135769 (W 9.6464e-05) | 🔵 fork 6.07× faster than `packed` | 🔵 fork 19.50× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b16/n1/b1` | 0.006152 ± 6.28517e-05 (W 1.66523e-05) | 0.016781 ± 0.000651154 (W 5.72713e-05) | 0.120754 ± 0.000873948 (W 0.000274671) | 🔵 fork 2.73× faster than `packed` | 🔵 fork 19.63× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b256/n1/b1` | 0.101008 ± 0.00123852 (W 0.000650722) | 0.261307 ± 0.0135546 (W 0.00703863) | 1.87751 ± 0.0162998 (W 0.0024538) | 🔵 fork 2.59× faster than `packed` | 🔵 fork 18.59× faster than `tblis` | `!` between-start range over 5% |
| `ikb_knb_inb_n16_b64/n1/b1` | 0.023774 ± 0.000112398 (W 2.37318e-05) | 0.064821 ± 0.00522663 (W 0.00180958) | 0.470586 ± 0.00476291 (W 0.00188406) | 🔵 fork 2.73× faster than `packed` | 🔵 fork 19.79× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `ikb_knb_inb_n2_b16/n1/b1` | 0.000721 ± 1.70392e-05 (W 8.78635e-06) | 0.003096 ± 0.00129042 (W 1.64317e-05) | 0.087844 ± 0.00106659 (W 8.74643e-05) | 🔵 fork 4.29× faster than `packed` | 🔵 fork 121.84× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b256/n1/b1` | 0.008166 ± 0.000260743 (W 1.41527e-05) | 0.040636 ± 0.0197545 (W 0.000191959) | 1.35029 ± 0.0264972 (W 0.00174416) | 🔵 fork 4.98× faster than `packed` | 🔵 fork 165.36× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b64/n1/b1` | 0.002214 ± 7.02377e-05 (W 8.61394e-06) | 0.010279 ± 0.0057081 (W 0.000125492) | 0.339662 ± 0.00636403 (W 0.00193058) | 🔵 fork 4.64× faster than `packed` | 🔵 fork 153.42× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b16/n1/b1` | 0.000952 ± 1.1547e-05 (W 8.61394e-06) | 0.004037 ± 0.00138572 (W 1.89816e-05) | 0.089196 ± 0.00164837 (W 0.00135697) | 🔵 fork 4.24× faster than `packed` | 🔵 fork 93.69× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b256/n1/b1` | 0.012563 ± 0.00030568 (W 4.90337e-05) | 0.056425 ± 0.0225295 (W 0.000722626) | 1.38873 ± 0.0198095 (W 0.00492288) | 🔵 fork 4.49× faster than `packed` | 🔵 fork 110.54× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b64/n1/b1` | 0.003296 ± 8.62168e-05 (W 1.48324e-05) | 0.014016 ± 0.00582035 (W 0.000141669) | 0.348509 ± 0.00254233 (W 0.00195116) | 🔵 fork 4.25× faster than `packed` | 🔵 fork 105.74× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b16/n1/b1` | 0.001402 ± 1.00167e-05 (W 8.43801e-06) | 0.006692 ± 0.00101528 (W 6.62216e-05) | 0.096349 ± 0.00150411 (W 0.00126342) | 🔵 fork 4.77× faster than `packed` | 🔵 fork 68.72× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b256/n1/b1` | 0.019165 ± 0.000252114 (W 3.60042e-05) | 0.09641 ± 0.016714 (W 0.00186199) | 1.51412 ± 0.0141234 (W 0.00389914) | 🔵 fork 5.03× faster than `packed` | 🔵 fork 79.00× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b64/n1/b1` | 0.005139 ± 4.04145e-05 (W 1.96036e-05) | 0.025077 ± 0.00378281 (W 0.000216455) | 0.374988 ± 0.00472845 (W 0.00146563) | 🔵 fork 4.88× faster than `packed` | 🔵 fork 72.97× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |

## per-shape, f64, 4T (CPU 4-7)

| case | plan (ms) | packed (ms) | tblis (ms) | vs `packed` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `ij_jk_ik_f64_n64/n1/b1` | 0.017392 ± 0.000146936 (W 2.21427e-05) | 0.024866 ± 0.000219955 (W 0.000297628) | 0.031158 ± 0.000902208 (W 0.00302558) | 🔵 fork 1.43× faster than `packed` | 🔵 fork 1.79× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ij_jk_kl_il_n64/n1/b1` | 0.034554 ± 0.000295603 (W 4.71169e-05) | 0.049703 ± 0.000842751 (W 0.0003786) | 0.067546 ± 0.00306139 (W 0.00196146) | 🔵 fork 1.44× faster than `packed` | 🔵 fork 1.95× faster than `tblis` | `!` between-start range over 5% |
| `ijk_jkl_il_8x16x8/n1/b1` | 0.000821 ± 2.60832e-05 (W 5.85662e-06) | 0.00511 ± 4.38216e-05 (W 3.36051e-05) | 0.02171 ± 0.000926266 (W 0.000421392) | 🔵 fork 6.22× faster than `packed` | 🔵 fork 26.44× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b16/n1/b1` | 0.006322 ± 0.0039227 (W 2.16795e-05) | 0.016882 ± 0.000231294 (W 0.000110079) | 0.239185 ± 0.0138592 (W 0.00847293) | 🔵 fork 2.67× faster than `packed` | 🔵 fork 37.83× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b256/n1/b1` | 0.030727 ± 0.000586348 (W 0.000374545) | 0.073857 ± 0.00123661 (W 0.00137053) | 1.22148 ± 0.0223882 (W 0.00604789) | 🔵 fork 2.40× faster than `packed` | 🔵 fork 39.75× faster than `tblis` |  |
| `ikb_knb_inb_n16_b64/n1/b1` | 0.023915 ± 0.0160412 (W 3.26236e-05) | 0.065842 ± 0.00213932 (W 0.00118268) | 0.907109 ± 0.00622857 (W 0.0237713) | 🔵 fork 2.75× faster than `packed` | 🔵 fork 37.93× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `ikb_knb_inb_n2_b16/n1/b1` | 0.000711 ± 3.27159e-05 (W 1.64712e-05) | 0.003096 ± 1.52753e-05 (W 1.62265e-05) | 0.031829 ± 0.00120788 (W 0.00179893) | 🔵 fork 4.35× faster than `packed` | 🔵 fork 44.77× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b256/n1/b1` | 0.008476 ± 0.000306573 (W 1.50433e-05) | 0.038632 ± 0.000744413 (W 0.00143991) | 0.391439 ± 0.00618481 (W 0.00591117) | 🔵 fork 4.56× faster than `packed` | 🔵 fork 46.18× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b64/n1/b1` | 0.002254 ± 8.2282e-05 (W 1.63799e-05) | 0.010449 ± 0.000109697 (W 1.48762e-05) | 0.104113 ± 0.00108835 (W 0.0017997) | 🔵 fork 4.64× faster than `packed` | 🔵 fork 46.19× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b16/n1/b1` | 0.000982 ± 3.05014e-05 (W 8.3666e-06) | 0.004017 ± 0.000176976 (W 1.9578e-05) | 0.070752 ± 0.000113578 (W 0.000951853) | 🔵 fork 4.09× faster than `packed` | 🔵 fork 72.05× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b256/n1/b1` | 0.012544 ± 0.000195244 (W 1.10136e-05) | 0.053901 ± 0.0158117 (W 0.00116848) | 0.402379 ± 0.0065625 (W 0.00691165) | 🔵 fork 4.30× faster than `packed` | 🔵 fork 32.08× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b64/n1/b1` | 0.003246 ± 6.4291e-05 (W 7.07107e-06) | 0.014166 ± 0.000547419 (W 4.15933e-05) | 0.105426 ± 0.00101718 (W 0.00393396) | 🔵 fork 4.36× faster than `packed` | 🔵 fork 32.48× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b16/n1/b1` | 0.001393 ± 3.09892e-05 (W 8.20366e-06) | 0.006752 ± 0.000142818 (W 6.49938e-05) | 0.167472 ± 0.000490561 (W 0.00305201) | 🔵 fork 4.85× faster than `packed` | 🔵 fork 120.22× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b256/n1/b1` | 0.019125 ± 9.34719e-05 (W 4.44556e-05) | 0.096219 ± 0.0019991 (W 0.0004214) | 0.42954 ± 0.00355105 (W 0.00627639) | 🔵 fork 5.03× faster than `packed` | 🔵 fork 22.46× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b64/n1/b1` | 0.0051 ± 6.37992e-05 (W 2.60058e-05) | 0.025077 ± 0.000265016 (W 0.000150395) | 0.277356 ± 0.00715867 (W 0.00370593) | 🔵 fork 4.92× faster than `packed` | 🔵 fork 54.38× faster than `tblis` | dispatch-dominated (row under 20 us) |

## per-shape, c64, 1T (CPU 4)

| case | plan (ms) | packed (ms) | tblis (ms) | vs `packed` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `ij_jk_ik_c64_n32/n1/b1` | 0.008967 ± 5.19615e-05 (W 1.41421e-05) | 0.013355 ± 0.00015308 (W 1.52381e-05) | 0.024796 ± 0.000120268 (W 4.50555e-05) | 🔵 fork 1.49× faster than `packed` | 🔵 fork 2.77× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `mps_chain_L32_chi16/n1/b1` | 0.167262 ± 0.000513135 (W 0.00187553) | 0.307252 ± 0.000884269 (W 0.00242258) | 0.900487 ± 0.00285531 (W 0.00139016) | 🔵 fork 1.84× faster than `packed` | 🔵 fork 5.38× faster than `tblis` |  |
| `mps_chain_L32_chi32/n1/b1` | 1.1625 ± 0.0122708 (W 0.00425509) | 1.58181 ± 0.00448416 (W 0.00217407) | 2.54616 ± 0.00766733 (W 0.00917997) | 🔵 fork 1.36× faster than `packed` | 🔵 fork 2.19× faster than `tblis` |  |
| `mps_chain_L32_chi4/n1/b1` | 0.03238 ± 0.000501209 (W 0.000445953) | 0.087583 ± 0.00194387 (W 0.000228648) | 0.52104 ± 0.00562169 (W 0.00190875) | 🔵 fork 2.70× faster than `packed` | 🔵 fork 16.09× faster than `tblis` |  |
| `mps_chain_L32_chi64/n1/b1` | 10.9295 ± 0.0190125 (W 0.0141624) | 10.9098 ± 0.0466757 (W 0.0531107) | 13.7951 ± 0.217075 (W 0.0470089) | · | 🔵 fork 1.26× faster than `tblis` |  |
| `mps_chain_L32_chi8/n1/b1` | 0.061334 ± 0.00140885 (W 0.000324824) | 0.131234 ± 0.00114122 (W 0.000599357) | 0.593204 ± 0.00641238 (W 0.00260204) | 🔵 fork 2.14× faster than `packed` | 🔵 fork 9.67× faster than `tblis` |  |

## per-shape, c64, 4T (CPU 4-7)

| case | plan (ms) | packed (ms) | tblis (ms) | vs `packed` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `ij_jk_ik_c64_n32/n1/b1` | 0.009017 ± 8.54225e-05 (W 1.64317e-05) | 0.013475 ± 3e-05 (W 4.10755e-05) | 0.024265 ± 0.0020939 (W 0.00167489) | 🔵 fork 1.49× faster than `packed` | 🔵 fork 2.69× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `mps_chain_L32_chi16/n1/b1` | 0.167542 ± 0.00196321 (W 0.000464231) | 0.308835 ± 0.00204946 (W 0.00222023) | 1.24855 ± 0.0655203 (W 0.0195045) | 🔵 fork 1.84× faster than `packed` | 🔵 fork 7.45× faster than `tblis` | `!` between-start range over 5% |
| `mps_chain_L32_chi32/n1/b1` | 1.16859 ± 0.00294051 (W 0.00243916) | 1.58637 ± 0.00104663 (W 0.0021976) | 1.91784 ± 0.0689343 (W 0.0163201) | 🔵 fork 1.36× faster than `packed` | 🔵 fork 1.64× faster than `tblis` | `!` between-start range over 5% |
| `mps_chain_L32_chi4/n1/b1` | 0.0324 ± 0.00172424 (W 0.000326599) | 0.088775 ± 0.00149661 (W 0.000739885) | 0.963705 ± 0.0390305 (W 0.00349278) | 🔵 fork 2.74× faster than `packed` | 🔵 fork 29.74× faster than `tblis` | `!` between-start range over 5% |
| `mps_chain_L32_chi64/n1/b1` | 3.96992 ± 0.0297125 (W 0.0933855) | 3.98066 ± 0.0874452 (W 0.0450319) | 5.5633 ± 0.0646773 (W 0.030059) | · | 🔵 fork 1.40× faster than `tblis` |  |
| `mps_chain_L32_chi8/n1/b1` | 0.060733 ± 0.00117251 (W 0.00118461) | 0.13471 ± 0.00185185 (W 0.00158633) | 1.14422 ± 0.0556097 (W 0.027762) | 🔵 fork 2.22× faster than `packed` | 🔵 fork 18.84× faster than `tblis` | `!` between-start range over 5% |

Not applicable to this population's shapes and reported as skipped: `ij_jk_ik_c64_n32/1`, `ij_jk_ik_f64_n64/1`, `ij_jk_kl_il_n64/1`, `ijk_jkl_il_8x16x8/1`, `ikb_knb_inb_n16_b16/1`, `ikb_knb_inb_n16_b256/1`, `ikb_knb_inb_n16_b64/1`, `ikb_knb_inb_n2_b16/1`, `ikb_knb_inb_n2_b256/1`, `ikb_knb_inb_n2_b64/1`, `ikb_knb_inb_n4_b16/1`, `ikb_knb_inb_n4_b256/1`, `ikb_knb_inb_n4_b64/1`, `ikb_knb_inb_n8_b16/1`, `ikb_knb_inb_n8_b256/1`, `ikb_knb_inb_n8_b64/1`, `mps_chain_L32_chi16/1`, `mps_chain_L32_chi32/1`, `mps_chain_L32_chi4/1`, `mps_chain_L32_chi64/1`, `mps_chain_L32_chi8/1`.

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
