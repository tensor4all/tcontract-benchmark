# `per-shape` on `epyc-9575f`

- tcontract-rs commit: `a045446301442ebb7540c806d9914dccce62357a`
- features: `tblis`
- tprims rows: `tprims` (the provider in the measured revision; see library above)
- external providers: `tblis` 2.0 @ `b16a732939d8454021e0a0f0097cf1cc1dd3ab19` tag `v2.0-beta2` sha256 `a6dbff05f181cbd5962d732b3c89c891ed90f449ecda460c973ba921ad03ff23` (TBLIS 2.0, configuration zen3; bundled BLIS 358e689cadd6757f564a2992cf46a2f7d6fa6bb0; built with ./configure --prefix=/home/ningyuan/projects/t4a_bench/workspace/tcontract-benchmark/target/tblis-v2.0-beta2 --with-blis-config-family=zen3 (cmake, Unix Makefiles, Release); libtblis.so sha256 a6dbff05f181cbd5)
- harness commit: `ce36f0bf324b093826c859f2a4d8a83ac309979c`
- toolkit commit: `926334592a5ef615617d169d9e2ab3c6bf7a7bd6`
- measured binary SHA-256: `b665fcfd2a8414847a49c90e330ac160f4de32ff1e6cc7504b1d7350437abef5`
- hardware profile: `epyc-9575f`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-11-14T15:30:12.361460Z`
- timing policy: v2, median of 5 reps, priming 1500 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/v2/record_run.py per-shape epyc-9575f per-shape --external-provider-json target/tblis-providers.json --aa 2 --reps 5 --prime-ms 1500 --label pub-20261114-per-shape`
- raw data: `data/v2-results/per-shape/epyc-9575f/per-shape/20261114T152521Z-pub-20261114-per-shape/`

## What was measured

- **Workload** — Small and large batched GEMMs, a two-step chain and the steps of a 32-site MPS chain, at fixed extents. One timed call is the whole program (a chain of pairwise steps), not one step.
  Source: The corpus is defined by `benchmarks/benchmarks/lukbench/corpus.rs` in the measured revision (`pins/tcontract-rs-v2.rev`); it carries the case definitions recorded from tensor4all/tcontract-rs#61.
  Known blind spot: Each case fixes its own dtype (f64 or c64); the suite declares both, and lukbench's census reports the wrong-dtype cells as skipped rather than dropping the case.
  Known blind spot: The declared identity is the numeric sentinel `n = 1`; the final step's real extents are the harness's own report, not the toolkit's identity.
  Known blind spot: One size per case: a ratio here says nothing about a neighbouring size, and the set is not a sweep.
  Known blind spot: `tblis` is an external baseline linked from its own prefix (`TBLIS_ROOT`, see `docs/v2-layout.md`), not the measured checkout; its revision is recorded through the campaign TBLIS collector (`scripts/tblis_providers_json.py`).
  Known blind spot: The harness's census CSV carries no corpus `group` column, so the corpus's own group labels and each case's native dtype and final-step extents are not part of this declaration; they remain facts of the recorded revision's `corpus.rs`.
  Known blind spot: The library rows time one execution of a plan built before the clock, so a single call also pays the preparation recorded as `prepare_s` in the run CSV, and the ratio applies when the same shape and layout recur. The reference rows time one call of their own entry point: `ttgt` has its offset tables and scratch prepared outside the clock, counted in its `prepare_s`; `tblis` exposes no prepared contraction, so the analysis it performs per call is inside its time.
- **Rows** — one row per engine in every table below:
  - `plan` — This library with its planner choosing the route per case.
    Identity: the measured tcontract-rs revision in this run's manifest (`library.commit`), pinned by `pins/tcontract-rs-v2.rev`
    As measured: `tprims` (the provider in the measured revision; see library above)
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
Each process retains 5 chronological calls; 2 complete process sets are recorded.
Spread guide (computed from this run's own rows): per-engine between-start range median 0.78%, worst 29.17% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 10 of 84 engine cells exceed 5% and carry `!`; median within-process relative SD 0.54%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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

## per-shape, f64, 1T (CPU 0)

| case | plan (ms) | tblis (ms) | vs `tblis` | notes |
|---|---|---|---|---|
| `ij_jk_ik_f64_n64/n1/b1` | 0.00564 ± 2.82843e-05 (W 3.05343e-05) | 0.028649 ± 0.000226274 (W 0.000117797) | 🔵 tcontract 5.08× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ij_jk_kl_il_n64/n1/b1` | 0.0112995 ± 0.000154856 (W 2.03348e-05) | 0.0571725 ± 0.000120915 (W 0.00012418) | 🔵 tcontract 5.06× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ijk_jkl_il_8x16x8/n1/b1` | 0.000375 ± 7.07107e-06 (W 1.11803e-05) | 0.009489 ± 4.24264e-05 (W 6.14069e-05) | 🔵 tcontract 25.30× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b16/n1/b1` | 0.00356 ± 0 (W 6.97231e-06) | 0.072032 ± 0.00026163 (W 0.000340506) | 🔵 tcontract 20.23× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b256/n1/b1` | 0.058588 ± 0.00019799 (W 0.000193262) | 1.1165 ± 0.000296278 (W 0.00204392) | 🔵 tcontract 19.06× faster than `tblis` |  |
| `ikb_knb_inb_n16_b64/n1/b1` | 0.01406 ± 4.24264e-05 (W 8.67691e-06) | 0.279723 ± 0.000799031 (W 0.000975575) | 🔵 tcontract 19.89× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b16/n1/b1` | 0.000495 ± 7.07107e-06 (W 1.25483e-05) | 0.052083 ± 2.12132e-05 (W 0.00033845) | 🔵 tcontract 105.22× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b256/n1/b1` | 0.00623 ± 0 (W 7.48214e-06) | 0.799672 ± 0.00191555 (W 0.000832013) | 🔵 tcontract 128.36× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b64/n1/b1` | 0.00165 ± 0 (W 4.97468e-06) | 0.200761 ± 0.000324562 (W 0.000673403) | 🔵 tcontract 121.67× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b16/n1/b1` | 0.000635 ± 2.12132e-05 (W 7.21075e-06) | 0.0530175 ± 7.00036e-05 (W 3.13282e-05) | 🔵 tcontract 83.49× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b256/n1/b1` | 0.0085545 ± 0.000318905 (W 0.00036216) | 0.82271 ± 0.00290621 (W 0.000785598) | 🔵 tcontract 96.17× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b64/n1/b1` | 0.0022 ± 8.48528e-05 (W 1.54942e-05) | 0.207096 ± 6.36396e-05 (W 0.000669944) | 🔵 tcontract 94.13× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b16/n1/b1` | 0.00086 ± 0 (W 6.51392e-06) | 0.0576275 ± 0.000536694 (W 8.48449e-05) | 🔵 tcontract 67.01× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b256/n1/b1` | 0.0120295 ± 5.72756e-05 (W 1.44413e-05) | 0.882273 ± 0.00101823 (W 0.000570439) | 🔵 tcontract 73.34× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b64/n1/b1` | 0.003275 ± 7.07107e-06 (W 7.98498e-06) | 0.222415 ± 9.2631e-05 (W 0.000462) | 🔵 tcontract 67.91× faster than `tblis` | dispatch-dominated (row under 20 us) |

## per-shape, f64, 4T (CPU 0-3)

| case | plan (ms) | tblis (ms) | vs `tblis` | notes |
|---|---|---|---|---|
| `ij_jk_ik_f64_n64/n1/b1` | 0.00483 ± 5.65685e-05 (W 0.000167014) | 0.021634 ± 0.00072832 (W 0.00172894) | 🔵 tcontract 4.48× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ij_jk_kl_il_n64/n1/b1` | 0.00952 ± 0.000282843 (W 0.000170041) | 0.041653 ± 0.00026163 (W 0.00277628) | 🔵 tcontract 4.38× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ijk_jkl_il_8x16x8/n1/b1` | 0.000385 ± 7.07107e-06 (W 4.97468e-06) | 0.0126745 ± 0.000133643 (W 0.000263141) | 🔵 tcontract 32.92× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b16/n1/b1` | 0.001495 ± 3.53553e-05 (W 3.70753e-05) | 0.145119 ± 0.00207182 (W 0.00796571) | 🔵 tcontract 97.07× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b256/n1/b1` | 0.0144695 ± 4.31335e-05 (W 4.79539e-05) | 0.74131 ± 0.000225567 (W 0.0144637) | 🔵 tcontract 51.23× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b64/n1/b1` | 0.004105 ± 7.07107e-06 (W 2.10614e-05) | 0.540523 ± 0.0528683 (W 0.00946828) | 🔵 tcontract 131.67× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b16/n1/b1` | 0.000525 ± 7.07107e-06 (W 1.16009e-05) | 0.021674 ± 0.00150614 (W 0.00143814) | 🔵 tcontract 41.28× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b256/n1/b1` | 0.00625 ± 0 (W 9.66608e-06) | 0.23642 ± 0.00868186 (W 0.00547738) | 🔵 tcontract 37.83× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b64/n1/b1` | 0.00166 ± 0 (W 6.01701e-06) | 0.061617 ± 0.00128693 (W 0.00235902) | 🔵 tcontract 37.12× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b16/n1/b1` | 0.00067 ± 0 (W 7.07107e-06) | 0.041923 ± 9.19239e-05 (W 0.00049316) | 🔵 tcontract 62.57× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b256/n1/b1` | 0.008785 ± 6.36396e-05 (W 4.10736e-05) | 0.24309 ± 0.00404465 (W 0.00571467) | 🔵 tcontract 27.67× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b64/n1/b1` | 0.002285 ± 7.07107e-06 (W 7.89814e-06) | 0.0652075 ± 0.00115895 (W 0.00245267) | 🔵 tcontract 28.54× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b16/n1/b1` | 0.000875 ± 7.07107e-06 (W 5.57586e-06) | 0.096826 ± 0.0080893 (W 0.000738416) | 🔵 tcontract 110.66× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b256/n1/b1` | 0.004285 ± 0.000883883 (W 2.74643e-05) | 0.25145 ± 0.00145664 (W 0.00422478) | 🔵 tcontract 58.68× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b64/n1/b1` | 0.00146 ± 0.000113137 (W 4.10957e-05) | 0.162709 ± 0.00413587 (W 0.00437974) | 🔵 tcontract 111.44× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |

## per-shape, c64, 1T (CPU 0)

| case | plan (ms) | tblis (ms) | vs `tblis` | notes |
|---|---|---|---|---|
| `ij_jk_ik_c64_n32/n1/b1` | 0.00303 ± 0 (W 1.40723e-05) | 0.0146145 ± 5.02046e-05 (W 3.82407e-05) | 🔵 tcontract 4.82× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `mps_chain_L32_chi16/n1/b1` | 0.0616275 ± 0.000142128 (W 9.11848e-05) | 0.532687 ± 0.00564201 (W 0.00235212) | 🔵 tcontract 8.64× faster than `tblis` |  |
| `mps_chain_L32_chi32/n1/b1` | 0.387359 ± 0.000417193 (W 0.00147729) | 1.49708 ± 0.00390252 (W 0.00131899) | 🔵 tcontract 3.86× faster than `tblis` |  |
| `mps_chain_L32_chi4/n1/b1` | 0.018729 ± 9.89949e-05 (W 0.000153329) | 0.306702 ± 0.00608819 (W 0.000659005) | 🔵 tcontract 16.38× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `mps_chain_L32_chi64/n1/b1` | 3.42575 ± 0.00394566 (W 0.00195724) | 7.48587 ± 0.0154361 (W 0.00816254) | 🔵 tcontract 2.19× faster than `tblis` |  |
| `mps_chain_L32_chi8/n1/b1` | 0.0354635 ± 0.000161927 (W 0.00022571) | 0.351256 ± 0.00602384 (W 0.000820323) | 🔵 tcontract 9.90× faster than `tblis` |  |

## per-shape, c64, 4T (CPU 0-3)

| case | plan (ms) | tblis (ms) | vs `tblis` | notes |
|---|---|---|---|---|
| `ij_jk_ik_c64_n32/n1/b1` | 0.003545 ± 6.36396e-05 (W 2.91569e-05) | 0.0143645 ± 0.000333047 (W 0.00166103) | 🔵 tcontract 4.05× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `mps_chain_L32_chi16/n1/b1` | 0.070727 ± 0.000268701 (W 0.00038271) | 0.876193 ± 0.00347897 (W 0.0127867) | 🔵 tcontract 12.39× faster than `tblis` |  |
| `mps_chain_L32_chi32/n1/b1` | 0.372625 ± 0.00383181 (W 0.00265747) | 1.18273 ± 0.014828 (W 0.00744793) | 🔵 tcontract 3.17× faster than `tblis` |  |
| `mps_chain_L32_chi4/n1/b1` | 0.019699 ± 0.00019799 (W 0.000174176) | 0.563487 ± 0.0358482 (W 0.00264485) | 🔵 tcontract 28.60× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `mps_chain_L32_chi64/n1/b1` | 1.35976 ± 0.0026863 (W 0.00495688) | 2.97013 ± 0.0522114 (W 0.0125769) | 🔵 tcontract 2.18× faster than `tblis` |  |
| `mps_chain_L32_chi8/n1/b1` | 0.0368735 ± 0.000671044 (W 0.000194671) | 0.782747 ± 0.0305597 (W 0.00961615) | 🔵 tcontract 21.23× faster than `tblis` | `!` between-start range over 5% |

Not applicable to this population's shapes and reported as skipped: `ij_jk_ik_c64_n32/1`, `ij_jk_ik_f64_n64/1`, `ij_jk_kl_il_n64/1`, `ijk_jkl_il_8x16x8/1`, `ikb_knb_inb_n16_b16/1`, `ikb_knb_inb_n16_b256/1`, `ikb_knb_inb_n16_b64/1`, `ikb_knb_inb_n2_b16/1`, `ikb_knb_inb_n2_b256/1`, `ikb_knb_inb_n2_b64/1`, `ikb_knb_inb_n4_b16/1`, `ikb_knb_inb_n4_b256/1`, `ikb_knb_inb_n4_b64/1`, `ikb_knb_inb_n8_b16/1`, `ikb_knb_inb_n8_b256/1`, `ikb_knb_inb_n8_b64/1`, `mps_chain_L32_chi16/1`, `mps_chain_L32_chi32/1`, `mps_chain_L32_chi4/1`, `mps_chain_L32_chi64/1`, `mps_chain_L32_chi8/1`.

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
