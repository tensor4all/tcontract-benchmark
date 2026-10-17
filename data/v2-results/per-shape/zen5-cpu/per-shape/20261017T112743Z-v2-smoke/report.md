# `per-shape` on `zen5-cpu`

- tcontract-rs commit: `7738bf43a0684e7d6f0769444e846f215fec86ab`
- features: `tblis`
- tprims rows: `tprims` (the provider in the measured revision; see library above)
- external providers: `tblis` 2.0 @ `b16a732939d8454021e0a0f0097cf1cc1dd3ab19` tag `v2.0-beta2` sha256 `de00bf1552c15f9c4a5d3157f02c149b81aef0909107c51cbb54ba4b8e9b5827` (TBLIS 2.0, configuration zen3; bundled BLIS 358e689cadd6757f564a2992cf46a2f7d6fa6bb0; built with ./configure --prefix=/home/shinaoka/projects/tensor4all/tcontract-benchmark/target/tblis-v2.0-beta2 --with-blis-config-family=zen3 (cmake, Unix Makefiles, Release); libtblis.so sha256 de00bf1552c15f9c)
- harness commit: `7190738b796c5c78f0375141b093a8d2f4a20a2e`
- toolkit commit: `5a3ae9a644a64c9ad86ead088d7696839991375f`
- measured binary SHA-256: `5dbc239a2db44622d5c9e868af14b68b803589cc24d1a3fb8539ac2d0c35771b`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-17T11:28:55.260628Z`
- timing policy: v2, median of 2 reps, priming 50 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/v2/record_run.py per-shape zen5-cpu per-shape --external-provider-json target/tblis-providers.json --label v2-smoke --reps 2 --aa 3 --prime-ms 50 --no-publish`
- raw data: `data/v2-results/per-shape/zen5-cpu/per-shape/20261017T112743Z-v2-smoke/`

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
Each process retains 2 chronological calls; 3 complete process sets are recorded.
Spread guide (computed from this run's own rows): per-engine between-start range median 2.78%, worst 22.85% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 40 of 126 engine cells exceed 5% and carry `!`; median within-process relative SD 0.39%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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
| `ij_jk_ik_f64_n64/n1/b1` | 0.017147 ± 0.000218884 (W 2.12132e-05) | 0.0249765 ± 0.00162593 (W 2.75772e-05) | 0.048585 ± 0.00139038 (W 0.00026163) | 🔵 fork 1.46× faster than `packed` | 🔵 fork 2.83× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `ij_jk_kl_il_n64/n1/b1` | 0.034764 ± 0.000946062 (W 9.89949e-05) | 0.049247 ± 0.000277608 (W 4.94975e-05) | 0.097146 ± 0.00128384 (W 2.12132e-05) | 🔵 fork 1.42× faster than `packed` | 🔵 fork 2.79× faster than `tblis` | `!` between-start range over 5% |
| `ijk_jkl_il_8x16x8/n1/b1` | 0.0007165 ± 3.04138e-06 (W 7.07107e-06) | 0.0049445 ± 6.07666e-05 (W 3.60624e-05) | 0.016115 ± 9.38527e-05 (W 3.53553e-05) | 🔵 fork 6.90× faster than `packed` | 🔵 fork 22.49× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b16/n1/b1` | 0.006021 ± 6.97501e-05 (W 1.41421e-05) | 0.0161305 ± 0.001566 (W 0.000319612) | 0.121712 ± 0.000347031 (W 0.000106066) | 🔵 fork 2.68× faster than `packed` | 🔵 fork 20.21× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b256/n1/b1` | 0.0995105 ± 0.00119817 (W 0.000269408) | 0.258031 ± 0.0162342 (W 0.00333684) | 1.89995 ± 0.0295692 (W 0.00150189) | 🔵 fork 2.59× faster than `packed` | 🔵 fork 19.09× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `ikb_knb_inb_n16_b64/n1/b1` | 0.0238395 ± 0.000898912 (W 6.29325e-05) | 0.062191 ± 0.00699194 (W 0.00101399) | 0.480189 ± 0.00442408 (W 0.00225991) | 🔵 fork 2.61× faster than `packed` | 🔵 fork 20.14× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `ikb_knb_inb_n2_b16/n1/b1` | 0.000616 ± 1.25831e-05 (W 7.07107e-06) | 0.003196 ± 4.09268e-05 (W 2.82843e-05) | 0.088996 ± 0.00045875 (W 9.2631e-05) | 🔵 fork 5.19× faster than `packed` | 🔵 fork 144.47× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b256/n1/b1` | 0.008366 ± 0.000285076 (W 7.77817e-06) | 0.0390425 ± 0.000760412 (W 9.97021e-05) | 1.36393 ± 0.0270421 (W 0.000729734) | 🔵 fork 4.67× faster than `packed` | 🔵 fork 163.03× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b64/n1/b1` | 0.002169 ± 7.93725e-05 (W 2.12132e-05) | 0.010259 ± 0.00038489 (W 4.24264e-05) | 0.345834 ± 0.00226648 (W 0.00168645) | 🔵 fork 4.73× faster than `packed` | 🔵 fork 159.44× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b16/n1/b1` | 0.0008915 ± 1.00042e-05 (W 1.41421e-05) | 0.004273 ± 6.13195e-05 (W 3.53553e-05) | 0.091936 ± 0.00128159 (W 0.00194808) | 🔵 fork 4.79× faster than `packed` | 🔵 fork 103.13× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b256/n1/b1` | 0.0125835 ± 0.000663895 (W 5.72756e-05) | 0.0538905 ± 0.000511144 (W 0.000311834) | 1.42514 ± 0.0323095 (W 0.00220971) | 🔵 fork 4.28× faster than `packed` | 🔵 fork 113.25× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b64/n1/b1` | 0.003206 ± 1.44338e-05 (W 1.41421e-05) | 0.014277 ± 6.96856e-05 (W 0.000169706) | 0.354986 ± 0.00129255 (W 0.00033234) | 🔵 fork 4.45× faster than `packed` | 🔵 fork 110.73× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b16/n1/b1` | 0.0013175 ± 1.52753e-05 (W 6.36396e-06) | 0.006622 ± 0.00012253 (W 9.97021e-05) | 0.097627 ± 0.00100452 (W 7.77817e-05) | 🔵 fork 5.03× faster than `packed` | 🔵 fork 74.10× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b256/n1/b1` | 0.019186 ± 0.000376277 (W 4.17193e-05) | 0.092201 ± 0.00470775 (W 0.00151604) | 1.51896 ± 0.0226035 (W 0.00184131) | 🔵 fork 4.81× faster than `packed` | 🔵 fork 79.17× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b64/n1/b1` | 0.005049 ± 0.000185558 (W 2.05061e-05) | 0.0237095 ± 0.000865597 (W 0.000488611) | 0.382047 ± 0.00293079 (W 0.00262124) | 🔵 fork 4.70× faster than `packed` | 🔵 fork 75.67× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |

## per-shape, f64, 4T (CPU 4-7)

| case | plan (ms) | packed (ms) | tblis (ms) | vs `packed` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `ij_jk_ik_f64_n64/n1/b1` | 0.017137 ± 2.94449e-05 (W 3.53553e-05) | 0.024591 ± 0.000101283 (W 3.53553e-05) | 0.032576 ± 0.00193534 (W 0.00271246) | 🔵 fork 1.43× faster than `packed` | 🔵 fork 1.90× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ij_jk_kl_il_n64/n1/b1` | 0.034229 ± 0.00140702 (W 3.53553e-05) | 0.049327 ± 0.000299357 (W 0.000206475) | 0.067962 ± 0.00836264 (W 0.00374767) | 🔵 fork 1.44× faster than `packed` | 🔵 fork 1.99× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `ijk_jkl_il_8x16x8/n1/b1` | 0.0007365 ± 1.1694e-05 (W 7.77817e-06) | 0.0049545 ± 7.97135e-05 (W 1.3435e-05) | 0.0212595 ± 0.000766914 (W 0.000453255) | 🔵 fork 6.73× faster than `packed` | 🔵 fork 28.87× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b16/n1/b1` | 0.006011 ± 6.13739e-05 (W 1.41421e-05) | 0.016496 ± 0.00129881 (W 0.000127279) | 0.235945 ± 0.011927 (W 0.00286237) | 🔵 fork 2.74× faster than `packed` | 🔵 fork 39.25× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b256/n1/b1` | 0.0301265 ± 0.000513276 (W 0.000297692) | 0.070045 ± 1.14054e-05 (W 0.000814587) | 1.22836 ± 0.00890008 (W 0.00707672) | 🔵 fork 2.33× faster than `packed` | 🔵 fork 40.77× faster than `tblis` |  |
| `ikb_knb_inb_n16_b64/n1/b1` | 0.0236545 ± 0.000336765 (W 2.05061e-05) | 0.064545 ± 0.00527852 (W 0.000177484) | 0.935597 ± 0.0336663 (W 0.00437063) | 🔵 fork 2.73× faster than `packed` | 🔵 fork 39.55× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `ikb_knb_inb_n2_b16/n1/b1` | 0.0006065 ± 1.99186e-05 (W 7.77817e-06) | 0.003276 ± 7.36546e-05 (W 4.24264e-05) | 0.033282 ± 0.00104069 (W 0.000566393) | 🔵 fork 5.40× faster than `packed` | 🔵 fork 54.88× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b256/n1/b1` | 0.0078745 ± 0.00032695 (W 7.07107e-06) | 0.0403755 ± 0.000813034 (W 0.000340118) | 0.400722 ± 0.00347933 (W 0.00692187) | 🔵 fork 5.13× faster than `packed` | 🔵 fork 50.89× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b64/n1/b1` | 0.002044 ± 8.37158e-05 (W 0) | 0.0108695 ± 0.000208295 (W 0.000325976) | 0.106624 ± 0.00132948 (W 0.00106915) | 🔵 fork 5.32× faster than `packed` | 🔵 fork 52.16× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b16/n1/b1` | 0.000887 ± 1.07742e-05 (W 7.07107e-07) | 0.004408 ± 0.000186045 (W 0.000248194) | 0.0701605 ± 0.000850163 (W 7.07107e-05) | 🔵 fork 4.97× faster than `packed` | 🔵 fork 79.10× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b256/n1/b1` | 0.0123585 ± 0.000220817 (W 2.19203e-05) | 0.057337 ± 0.00159416 (W 0.000226981) | 0.411652 ± 0.00604606 (W 0.00510036) | 🔵 fork 4.64× faster than `packed` | 🔵 fork 33.31× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b64/n1/b1` | 0.003206 ± 5.48483e-05 (W 7.07107e-06) | 0.0152235 ± 0.00135855 (W 0.00013435) | 0.108502 ± 0.00207464 (W 0.000985) | 🔵 fork 4.75× faster than `packed` | 🔵 fork 33.84× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b16/n1/b1` | 0.0013225 ± 8.66025e-06 (W 7.77817e-06) | 0.006888 ± 0.000386187 (W 2.82843e-05) | 0.164266 ± 0.00403655 (W 0.000970151) | 🔵 fork 5.21× faster than `packed` | 🔵 fork 124.21× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b256/n1/b1` | 0.019246 ± 0.000821433 (W 2.82843e-05) | 0.097266 ± 0.00522181 (W 0.00294722) | 0.434169 ± 0.00386466 (W 0.00636113) | 🔵 fork 5.05× faster than `packed` | 🔵 fork 22.56× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b64/n1/b1` | 0.0050245 ± 0.000189642 (W 1.3435e-05) | 0.024701 ± 0.000635011 (W 2.82843e-05) | 0.27883 ± 0.00253329 (W 0.00759433) | 🔵 fork 4.92× faster than `packed` | 🔵 fork 55.49× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |

## per-shape, c64, 1T (CPU 4)

| case | plan (ms) | packed (ms) | tblis (ms) | vs `packed` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `ij_jk_ik_c64_n32/n1/b1` | 0.008876 ± 3.59873e-05 (W 1.48492e-05) | 0.0132345 ± 4.17143e-05 (W 2.82843e-05) | 0.0248315 ± 0.000168749 (W 7.70746e-05) | 🔵 fork 1.49× faster than `packed` | 🔵 fork 2.80× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `mps_chain_L32_chi16/n1/b1` | 0.161521 ± 0.00123696 (W 0.00305258) | 0.290056 ± 0.000310994 (W 0.000545179) | 0.906814 ± 0.0129602 (W 0.000361332) | 🔵 fork 1.80× faster than `packed` | 🔵 fork 5.61× faster than `tblis` |  |
| `mps_chain_L32_chi32/n1/b1` | 1.15498 ± 0.00219137 (W 0.000453255) | 1.57936 ± 0.00467023 (W 0.00585131) | 2.56879 ± 0.014696 (W 0.00438548) | 🔵 fork 1.37× faster than `packed` | 🔵 fork 2.22× faster than `tblis` |  |
| `mps_chain_L32_chi4/n1/b1` | 0.0244355 ± 0.000223137 (W 0.000269408) | 0.0654065 ± 0.0063424 (W 4.94975e-05) | 0.525128 ± 0.00436817 (W 0.00220264) | 🔵 fork 2.68× faster than `packed` | 🔵 fork 21.49× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `mps_chain_L32_chi64/n1/b1` | 10.9665 ± 0.087778 (W 0.0240303) | 10.9053 ± 0.0141316 (W 0.0219118) | 14.0293 ± 0.0808752 (W 0.0125462) | · | 🔵 fork 1.28× faster than `tblis` |  |
| `mps_chain_L32_chi8/n1/b1` | 0.0531645 ± 0.000113689 (W 0.000162635) | 0.112099 ± 0.00397689 (W 0.00028355) | 0.600058 ± 0.00692798 (W 0.00256397) | 🔵 fork 2.11× faster than `packed` | 🔵 fork 11.29× faster than `tblis` | `!` between-start range over 5% |

## per-shape, c64, 4T (CPU 4-7)

| case | plan (ms) | packed (ms) | tblis (ms) | vs `packed` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `ij_jk_ik_c64_n32/n1/b1` | 0.0088965 ± 4.50009e-05 (W 1.48492e-05) | 0.0131245 ± 0.000139661 (W 3.53553e-05) | 0.0249665 ± 0.00193629 (W 0.00195515) | 🔵 fork 1.48× faster than `packed` | 🔵 fork 2.81× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `mps_chain_L32_chi16/n1/b1` | 0.161511 ± 0.00137147 (W 0.000524673) | 0.291548 ± 0.00241479 (W 0.00234406) | 1.3465 ± 0.0651638 (W 0.00501622) | 🔵 fork 1.81× faster than `packed` | 🔵 fork 8.34× faster than `tblis` | `!` between-start range over 5% |
| `mps_chain_L32_chi32/n1/b1` | 1.16376 ± 0.00913363 (W 0.000672459) | 1.5745 ± 0.00941446 (W 0.00185616) | 1.93205 ± 0.0264517 (W 0.00211142) | 🔵 fork 1.35× faster than `packed` | 🔵 fork 1.66× faster than `tblis` |  |
| `mps_chain_L32_chi4/n1/b1` | 0.0245205 ± 0.000119506 (W 0.000248194) | 0.065156 ± 0.00200295 (W 0.000233345) | 0.986898 ± 0.00964577 (W 0.00395273) | 🔵 fork 2.66× faster than `packed` | 🔵 fork 40.25× faster than `tblis` | `!` between-start range over 5% |
| `mps_chain_L32_chi64/n1/b1` | 3.95158 ± 0.0812599 (W 0.0279753) | 3.94839 ± 0.0493335 (W 0.045042) | 5.57578 ± 0.0230116 (W 0.0173135) | · | 🔵 fork 1.41× faster than `tblis` |  |
| `mps_chain_L32_chi8/n1/b1` | 0.0534745 ± 0.000942268 (W 0.000177484) | 0.110576 ± 0.00506445 (W 0.00123249) | 1.25515 ± 0.0210137 (W 0.00330007) | 🔵 fork 2.07× faster than `packed` | 🔵 fork 23.47× faster than `tblis` | `!` between-start range over 5% |

Not applicable to this population's shapes and reported as skipped: `ij_jk_ik_c64_n32/1`, `ij_jk_ik_f64_n64/1`, `ij_jk_kl_il_n64/1`, `ijk_jkl_il_8x16x8/1`, `ikb_knb_inb_n16_b16/1`, `ikb_knb_inb_n16_b256/1`, `ikb_knb_inb_n16_b64/1`, `ikb_knb_inb_n2_b16/1`, `ikb_knb_inb_n2_b256/1`, `ikb_knb_inb_n2_b64/1`, `ikb_knb_inb_n4_b16/1`, `ikb_knb_inb_n4_b256/1`, `ikb_knb_inb_n4_b64/1`, `ikb_knb_inb_n8_b16/1`, `ikb_knb_inb_n8_b256/1`, `ikb_knb_inb_n8_b64/1`, `mps_chain_L32_chi16/1`, `mps_chain_L32_chi32/1`, `mps_chain_L32_chi4/1`, `mps_chain_L32_chi64/1`, `mps_chain_L32_chi8/1`.

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
