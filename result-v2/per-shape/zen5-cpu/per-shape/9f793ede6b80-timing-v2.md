<!-- generated from data/v2-results/per-shape/zen5-cpu/per-shape/20261031T120047Z-pub-20261031-per-shape/report.md by scripts/publish_report.py; the report below is the source of truth -->

# `per-shape` on `zen5-cpu`

- tcontract-rs commit: `9f793ede6b8076fd7ce2251594a9552ad66aa339`
- features: `tblis`
- tprims rows: `tprims` (the provider in the measured revision; see library above)
- external providers: `tblis` 2.0 @ `b16a732939d8454021e0a0f0097cf1cc1dd3ab19` tag `v2.0-beta2` sha256 `407b4f6fef7f4ede52a224cb33a987893dca37fe1177f5412b407bc93ea834e6` (TBLIS 2.0, configuration zen3; bundled BLIS 358e689cadd6757f564a2992cf46a2f7d6fa6bb0; built with ./configure --prefix=/home/shinaoka/opt/tblis-v2.0-beta2-zen3 --with-blis-config-family=zen3 (cmake, Unix Makefiles, Release); libtblis.so sha256 407b4f6fef7f4ede)
- harness commit: `4f7f935ac58126107a8c7f098b684fa809d9b4b7`
- toolkit commit: `b71624bef111ce941bddaedcce3fdb6eab40f9eb`
- measured binary SHA-256: `d58043e7e73b59b64eac9c9841528665708ad6fd8cd9d5b310d10f92a1449001`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-31T12:02:10.230746Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 1 attempts
- command: `scripts/v2/record_run.py per-shape zen5-cpu per-shape --aa 2 --reps 5 --prime-ms 250 --external-provider-json /tmp/tmp.9C5AuzRU0f --label pub-20261031-per-shape`
- raw data: `data/v2-results/per-shape/zen5-cpu/per-shape/20261031T120047Z-pub-20261031-per-shape/`

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
  - `tblis` — Actual C++ TBLIS through the direct FFI adapter, as the independent third-party reference implementation. Pinned by release tag, not by a local revision: `benchmarks/scripts/build_tblis.sh` of the measured checkout builds it from the tag and writes the PROVENANCE this repository records.
    Identity: TBLIS v2.0-beta2 (the only tagged 2.0; its commit and the bundled BLIS revision are recorded per run, from `scripts/tblis_providers_json.py`)
    Caveat: Needs an install prefix (`TBLIS_ROOT`), and TBLIS 2.x builds through CMake, so the prefix cannot be made inside a bare checkout. The page repeats the tag, commit, bundled BLIS revision and artifact hash the manifest recorded.
    As measured: `tblis` 2.0 @ `b16a732939d8454021e0a0f0097cf1cc1dd3ab19` tag `v2.0-beta2` sha256 `407b4f6fef7f4ede52a224cb33a987893dca37fe1177f5412b407bc93ea834e6` (TBLIS 2.0, configuration zen3; bundled BLIS 358e689cadd6757f564a2992cf46a2f7d6fa6bb0; built with ./configure --prefix=/home/shinaoka/opt/tblis-v2.0-beta2-zen3 --with-blis-config-family=zen3 (cmake, Unix Makefiles, Release); libtblis.so sha256 407b4f6fef7f4ede)

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
Each process retains 5 chronological calls; 2 complete process sets are recorded.
Spread guide (computed from this run's own rows): per-engine between-start range median 1.20%, worst 7.75% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 4 of 84 engine cells exceed 5% and carry `!`; median within-process relative SD 0.62%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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

## per-shape, f64, 1T (CPU 4)

| case | plan (ms) | tblis (ms) | vs `tblis` | notes |
|---|---|---|---|---|
| `ij_jk_ik_f64_n64/n1/b1` | 0.0173375 ± 0.0001492 (W 0.00131889) | 0.0485205 ± 0.000269408 (W 0.0001921) | 🔵 tcontract 2.80× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ij_jk_kl_il_n64/n1/b1` | 0.034735 ± 4.24264e-05 (W 0.000753864) | 0.0970865 ± 0.000573464 (W 0.000259623) | 🔵 tcontract 2.80× faster than `tblis` |  |
| `ijk_jkl_il_8x16x8/n1/b1` | 0.0008465 ± 2.05061e-05 (W 4.78614e-06) | 0.016155 ± 9.19239e-05 (W 7.71152e-05) | 🔵 tcontract 19.08× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b16/n1/b1` | 0.005986 ± 2.12132e-05 (W 1.00547e-05) | 0.122088 ± 0.000595384 (W 0.00158835) | 🔵 tcontract 20.40× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b256/n1/b1` | 0.098188 ± 0.00033234 (W 0.00194206) | 1.89494 ± 0.0215003 (W 0.00437162) | 🔵 tcontract 19.30× faster than `tblis` |  |
| `ikb_knb_inb_n16_b64/n1/b1` | 0.0236145 ± 7.14178e-05 (W 0.00101858) | 0.473574 ± 0.00427941 (W 0.00258712) | 🔵 tcontract 20.05× faster than `tblis` |  |
| `ikb_knb_inb_n2_b16/n1/b1` | 0.0007915 ± 2.89914e-05 (W 1.68069e-05) | 0.0897275 ± 0.000467398 (W 9.9967e-05) | 🔵 tcontract 113.36× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b256/n1/b1` | 0.0090815 ± 3.60624e-05 (W 4.84749e-05) | 1.36527 ± 0.0200408 (W 0.00599987) | 🔵 tcontract 150.34× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b64/n1/b1` | 0.002419 ± 3.53553e-05 (W 8.13844e-06) | 0.344263 ± 0.00164332 (W 0.00204744) | 🔵 tcontract 142.32× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b16/n1/b1` | 0.001032 ± 5.65685e-05 (W 1.35374e-05) | 0.090935 ± 0.000758018 (W 0.00346223) | 🔵 tcontract 88.12× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b256/n1/b1` | 0.01327 ± 2.12132e-05 (W 6.40135e-05) | 1.4077 ± 0.0200337 (W 0.00380298) | 🔵 tcontract 106.08× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b64/n1/b1` | 0.003491 ± 3.53553e-05 (W 4.08895e-05) | 0.356305 ± 0.00219627 (W 0.00384535) | 🔵 tcontract 102.06× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b16/n1/b1` | 0.001453 ± 2.82843e-05 (W 6.48547e-06) | 0.097828 ± 0.00089944 (W 6.41332e-05) | 🔵 tcontract 67.33× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b256/n1/b1` | 0.019742 ± 0.000205061 (W 1.96593e-05) | 1.51084 ± 0.0220462 (W 0.0026725) | 🔵 tcontract 76.53× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b64/n1/b1` | 0.00545 ± 2.82843e-05 (W 0.00157196) | 0.378312 ± 0.00411607 (W 0.00203939) | 🔵 tcontract 69.41× faster than `tblis` | dispatch-dominated (row under 20 us) |

## per-shape, f64, 4T (CPU 4-7)

| case | plan (ms) | tblis (ms) | vs `tblis` | notes |
|---|---|---|---|---|
| `ij_jk_ik_f64_n64/n1/b1` | 0.011587 ± 7.07107e-06 (W 0.000154277) | 0.033888 ± 0.000560029 (W 0.00189325) | 🔵 tcontract 2.92× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ij_jk_kl_il_n64/n1/b1` | 0.023028 ± 0.000106066 (W 0.000276896) | 0.0700765 ± 0.00106985 (W 0.00182619) | 🔵 tcontract 3.04× faster than `tblis` |  |
| `ijk_jkl_il_8x16x8/n1/b1` | 0.000847 ± 7.07107e-06 (W 8.99816e-06) | 0.021981 ± 0.000581242 (W 0.000829953) | 🔵 tcontract 25.95× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b16/n1/b1` | 0.0024595 ± 6.36396e-06 (W 3.96659e-05) | 0.22744 ± 0.0022889 (W 0.00594304) | 🔵 tcontract 92.47× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b256/n1/b1` | 0.024561 ± 0.000106066 (W 6.53694e-05) | 1.21973 ± 0.0111716 (W 0.0143997) | 🔵 tcontract 49.66× faster than `tblis` |  |
| `ikb_knb_inb_n16_b64/n1/b1` | 0.007048 ± 7.77817e-05 (W 0.000731588) | 0.883199 ± 0.0265377 (W 0.0232424) | 🔵 tcontract 125.31× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b16/n1/b1` | 0.000782 ± 0 (W 1.3376e-05) | 0.0321 ± 0.000353553 (W 0.00167782) | 🔵 tcontract 41.05× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b256/n1/b1` | 0.008952 ± 7.07107e-06 (W 1.45641e-05) | 0.400247 ± 0.00532805 (W 0.00787353) | 🔵 tcontract 44.71× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b64/n1/b1` | 0.002425 ± 0 (W 1.06905e-05) | 0.10434 ± 0.00146654 (W 0.00314809) | 🔵 tcontract 43.03× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b16/n1/b1` | 0.001037 ± 2.12132e-05 (W 1.03427e-05) | 0.0717495 ± 0.000502753 (W 0.00101499) | 🔵 tcontract 69.19× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b256/n1/b1` | 0.01337 ± 0.000106066 (W 3.76713e-05) | 0.406915 ± 0.00254276 (W 0.00560587) | 🔵 tcontract 30.43× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b64/n1/b1` | 0.0035015 ± 6.36396e-06 (W 3.79954e-05) | 0.108377 ± 0.00157968 (W 0.00460088) | 🔵 tcontract 30.95× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b16/n1/b1` | 0.0014325 ± 7.07107e-07 (W 1.13593e-05) | 0.167623 ± 0.00480267 (W 0.00218144) | 🔵 tcontract 117.01× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b256/n1/b1` | 0.0062815 ± 0.000198697 (W 3.33163e-05) | 0.429317 ± 0.00548998 (W 0.0065303) | 🔵 tcontract 68.35× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b64/n1/b1` | 0.00279 ± 6.36396e-05 (W 2.74915e-05) | 0.279677 ± 0.00731856 (W 0.00510848) | 🔵 tcontract 100.24× faster than `tblis` | dispatch-dominated (row under 20 us) |

## per-shape, c64, 1T (CPU 4)

| case | plan (ms) | tblis (ms) | vs `tblis` | notes |
|---|---|---|---|---|
| `ij_jk_ik_c64_n32/n1/b1` | 0.0090315 ± 5.02046e-05 (W 2.20577e-05) | 0.024581 ± 0.000190919 (W 8.08999e-05) | 🔵 tcontract 2.72× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `mps_chain_L32_chi16/n1/b1` | 0.168089 ± 0.00237305 (W 0.0020587) | 0.895517 ± 0.00214748 (W 0.00271128) | 🔵 tcontract 5.33× faster than `tblis` |  |
| `mps_chain_L32_chi32/n1/b1` | 1.16257 ± 0.0064969 (W 0.00215971) | 2.54583 ± 0.0139781 (W 0.0071994) | 🔵 tcontract 2.19× faster than `tblis` |  |
| `mps_chain_L32_chi4/n1/b1` | 0.0331865 ± 0.00162281 (W 0.000262354) | 0.51697 ± 0.000871156 (W 0.00223886) | 🔵 tcontract 15.58× faster than `tblis` | `!` between-start range over 5% |
| `mps_chain_L32_chi64/n1/b1` | 10.9316 ± 0.0626581 (W 0.0237448) | 13.9598 ± 0.0364252 (W 0.0378085) | 🔵 tcontract 1.28× faster than `tblis` |  |
| `mps_chain_L32_chi8/n1/b1` | 0.0620905 ± 0.00159453 (W 0.000213949) | 0.595272 ± 0.00468953 (W 0.00449132) | 🔵 tcontract 9.59× faster than `tblis` |  |

## per-shape, c64, 4T (CPU 4-7)

| case | plan (ms) | tblis (ms) | vs `tblis` | notes |
|---|---|---|---|---|
| `ij_jk_ik_c64_n32/n1/b1` | 0.009983 ± 0.000120208 (W 0.000598467) | 0.0230785 ± 0.000234052 (W 0.00167665) | 🔵 tcontract 2.31× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `mps_chain_L32_chi16/n1/b1` | 0.180557 ± 0.000907218 (W 0.000468365) | 1.3009 ± 0.0389984 (W 0.0258231) | 🔵 tcontract 7.20× faster than `tblis` |  |
| `mps_chain_L32_chi32/n1/b1` | 0.995354 ± 0.00293944 (W 0.00507388) | 1.88252 ± 0.00860761 (W 0.0110286) | 🔵 tcontract 1.89× faster than `tblis` |  |
| `mps_chain_L32_chi4/n1/b1` | 0.0330415 ± 0.00028355 (W 0.00097123) | 0.975502 ± 0.00182716 (W 0.00419518) | 🔵 tcontract 29.52× faster than `tblis` |  |
| `mps_chain_L32_chi64/n1/b1` | 3.55917 ± 0.0112578 (W 0.0202173) | 5.61421 ± 0.149012 (W 0.0336987) | 🔵 tcontract 1.58× faster than `tblis` |  |
| `mps_chain_L32_chi8/n1/b1` | 0.062056 ± 0.000581242 (W 0.000335606) | 1.17723 ± 0.0561994 (W 0.0170743) | 🔵 tcontract 18.97× faster than `tblis` | `!` between-start range over 5% |

Not applicable to this population's shapes and reported as skipped: `ij_jk_ik_c64_n32/1`, `ij_jk_ik_f64_n64/1`, `ij_jk_kl_il_n64/1`, `ijk_jkl_il_8x16x8/1`, `ikb_knb_inb_n16_b16/1`, `ikb_knb_inb_n16_b256/1`, `ikb_knb_inb_n16_b64/1`, `ikb_knb_inb_n2_b16/1`, `ikb_knb_inb_n2_b256/1`, `ikb_knb_inb_n2_b64/1`, `ikb_knb_inb_n4_b16/1`, `ikb_knb_inb_n4_b256/1`, `ikb_knb_inb_n4_b64/1`, `ikb_knb_inb_n8_b16/1`, `ikb_knb_inb_n8_b256/1`, `ikb_knb_inb_n8_b64/1`, `mps_chain_L32_chi16/1`, `mps_chain_L32_chi32/1`, `mps_chain_L32_chi4/1`, `mps_chain_L32_chi64/1`, `mps_chain_L32_chi8/1`.

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
