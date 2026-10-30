# `per-shape` on `zen5-cpu`

- tcontract-rs commit: `9f793ede6b8076fd7ce2251594a9552ad66aa339`
- features: `tblis`
- tprims rows: `tprims` (the provider in the measured revision; see library above)
- external providers: `tblis` 2.0 @ `b16a732939d8454021e0a0f0097cf1cc1dd3ab19` tag `v2.0-beta2` sha256 `de00bf1552c15f9c4a5d3157f02c149b81aef0909107c51cbb54ba4b8e9b5827` (TBLIS 2.0, configuration zen3; bundled BLIS 358e689cadd6757f564a2992cf46a2f7d6fa6bb0; built with ./configure --prefix=/home/shinaoka/projects/tensor4all/tcontract-benchmark/target/tblis-v2.0-beta2 --with-blis-config-family=zen3 (cmake, Unix Makefiles, Release); libtblis.so sha256 de00bf1552c15f9c)
- harness commit: `65c8a5df9c0dfb86a199eb41f50803700e73f97e`
- toolkit commit: `b71624bef111ce941bddaedcce3fdb6eab40f9eb`
- measured binary SHA-256: `d58043e7e73b59b64eac9c9841528665708ad6fd8cd9d5b310d10f92a1449001`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-30T15:57:05.106804Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/v2/record_run.py per-shape zen5-cpu per-shape --aa 2 --reps 5 --prime-ms 250 --external-provider-json /home/shinaoka/.local/state/tensor4all-weekly/20261031/tcontract/tblis-providers.json --label weekly-20261030-per-shape --no-publish`
- raw data: `data/v2-results/per-shape/zen5-cpu/per-shape/20261030T155542Z-weekly-20261030-per-shape/`

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
Each process retains 5 chronological calls; 2 complete process sets are recorded.
Spread guide (computed from this run's own rows): per-engine between-start range median 1.18%, worst 13.57% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 8 of 84 engine cells exceed 5% and carry `!`; median within-process relative SD 0.72%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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
| `ij_jk_ik_f64_n64/n1/b1` | 0.017177 ± 2.12132e-05 (W 2.72621e-05) | 0.0481505 ± 0.000127986 (W 6.64594e-05) | 🔵 tcontract 2.80× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ij_jk_kl_il_n64/n1/b1` | 0.034585 ± 4.24264e-05 (W 7.09134e-05) | 0.0971375 ± 0.000347189 (W 0.00156441) | 🔵 tcontract 2.81× faster than `tblis` |  |
| `ijk_jkl_il_8x16x8/n1/b1` | 0.000847 ± 2.12132e-05 (W 7.03014e-06) | 0.0160955 ± 0.000106773 (W 0.000105625) | 🔵 tcontract 19.00× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b16/n1/b1` | 0.0060165 ± 2.19203e-05 (W 9.03785e-06) | 0.122339 ± 0.000893076 (W 0.00186386) | 🔵 tcontract 20.33× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b256/n1/b1` | 0.0977685 ± 0.000304763 (W 0.00203862) | 1.91297 ± 0.0102714 (W 0.00291543) | 🔵 tcontract 19.57× faster than `tblis` |  |
| `ikb_knb_inb_n16_b64/n1/b1` | 0.0237795 ± 6.43467e-05 (W 3.73475e-05) | 0.478036 ± 0.00288995 (W 0.00299803) | 🔵 tcontract 20.10× faster than `tblis` |  |
| `ikb_knb_inb_n2_b16/n1/b1` | 0.000786 ± 2.12132e-05 (W 1.38892e-05) | 0.088516 ± 0.000708521 (W 8.75749e-05) | 🔵 tcontract 112.62× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b256/n1/b1` | 0.009047 ± 9.89949e-05 (W 4.3634e-05) | 1.37525 ± 0.0181924 (W 0.0042303) | 🔵 tcontract 152.01× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b64/n1/b1` | 0.00242 ± 2.12132e-05 (W 7.80672e-06) | 0.34451 ± 0.00248619 (W 0.00221278) | 🔵 tcontract 142.36× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b16/n1/b1` | 0.001042 ± 4.24264e-05 (W 2.09748e-05) | 0.0904695 ± 0.000382545 (W 0.0014983) | 🔵 tcontract 86.82× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b256/n1/b1` | 0.01334 ± 0.000162635 (W 4.38521e-05) | 1.41708 ± 0.000929138 (W 0.00246232) | 🔵 tcontract 106.23× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b64/n1/b1` | 0.003486 ± 4.24264e-05 (W 3.50204e-05) | 0.355696 ± 0.000779232 (W 0.00310683) | 🔵 tcontract 102.04× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b16/n1/b1` | 0.0014325 ± 2.75772e-05 (W 9.87934e-06) | 0.0979085 ± 0.000516895 (W 0.000925176) | 🔵 tcontract 68.35× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b256/n1/b1` | 0.0198175 ± 8.55599e-05 (W 2.14844e-05) | 1.52937 ± 0.0154637 (W 0.00431888) | 🔵 tcontract 77.17× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b64/n1/b1` | 0.0054505 ± 2.75772e-05 (W 2.13566e-05) | 0.381846 ± 0.0028758 (W 0.00279192) | 🔵 tcontract 70.06× faster than `tblis` | dispatch-dominated (row under 20 us) |

## per-shape, f64, 4T (CPU 4-7)

| case | plan (ms) | tblis (ms) | vs `tblis` | notes |
|---|---|---|---|---|
| `ij_jk_ik_f64_n64/n1/b1` | 0.011542 ± 0.00019799 (W 0.000104854) | 0.0339335 ± 0.00181373 (W 0.00273877) | 🔵 tcontract 2.94× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `ij_jk_kl_il_n64/n1/b1` | 0.0231685 ± 3.60624e-05 (W 0.000253078) | 0.0662545 ± 0.00035426 (W 0.00186733) | 🔵 tcontract 2.86× faster than `tblis` |  |
| `ijk_jkl_il_8x16x8/n1/b1` | 0.0008765 ± 2.19203e-05 (W 1.31098e-05) | 0.021591 ± 1.41421e-05 (W 0.000388041) | 🔵 tcontract 24.63× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b16/n1/b1` | 0.0024745 ± 7.14178e-05 (W 1.88092e-05) | 0.228097 ± 0.0163794 (W 0.00678033) | 🔵 tcontract 92.18× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b256/n1/b1` | 0.0244905 ± 3.60624e-05 (W 3.75682e-05) | 1.21958 ± 0.01492 (W 0.0133091) | 🔵 tcontract 49.80× faster than `tblis` |  |
| `ikb_knb_inb_n16_b64/n1/b1` | 0.006973 ± 0.000113137 (W 5.12651e-05) | 0.87579 ± 0.00048154 (W 0.022968) | 🔵 tcontract 125.60× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b16/n1/b1` | 0.000802 ± 2.82843e-05 (W 1.53676e-05) | 0.0318495 ± 0.00067953 (W 0.00159953) | 🔵 tcontract 39.71× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b256/n1/b1` | 0.0090065 ± 5.72756e-05 (W 2.55882e-05) | 0.396072 ± 0.00950634 (W 0.00492747) | 🔵 tcontract 43.98× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b64/n1/b1` | 0.002459 ± 4.94975e-05 (W 1.14727e-05) | 0.106164 ± 0.00126855 (W 0.00350108) | 🔵 tcontract 43.17× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b16/n1/b1` | 0.001082 ± 1.41421e-05 (W 1.89312e-05) | 0.071028 ± 0.000630739 (W 0.00100034) | 🔵 tcontract 65.65× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b256/n1/b1` | 0.0135305 ± 0.000403758 (W 7.99252e-05) | 0.401593 ± 0.00519936 (W 0.00593915) | 🔵 tcontract 29.68× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b64/n1/b1` | 0.003506 ± 0 (W 3.56587e-05) | 0.110147 ± 0.00352776 (W 0.00359759) | 🔵 tcontract 31.42× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b16/n1/b1` | 0.001458 ± 2.12132e-05 (W 3.7182e-06) | 0.168971 ± 0.00217577 (W 0.00235604) | 🔵 tcontract 115.89× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b256/n1/b1` | 0.0063515 ± 9.97021e-05 (W 2.45358e-05) | 0.425086 ± 0.00763675 (W 0.0048481) | 🔵 tcontract 66.93× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b64/n1/b1` | 0.002835 ± 1.41421e-05 (W 5.70645e-05) | 0.279198 ± 0.00792808 (W 0.00585499) | 🔵 tcontract 98.48× faster than `tblis` | dispatch-dominated (row under 20 us) |

## per-shape, c64, 1T (CPU 4)

| case | plan (ms) | tblis (ms) | vs `tblis` | notes |
|---|---|---|---|---|
| `ij_jk_ik_c64_n32/n1/b1` | 0.009027 ± 1.41421e-05 (W 3.60103e-05) | 0.0248665 ± 5.58614e-05 (W 0.000767291) | 🔵 tcontract 2.75× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `mps_chain_L32_chi16/n1/b1` | 0.167824 ± 0.00067953 (W 0.00214911) | 0.906914 ± 0.00451205 (W 0.00151659) | 🔵 tcontract 5.40× faster than `tblis` |  |
| `mps_chain_L32_chi32/n1/b1` | 1.16065 ± 0.00193394 (W 0.0016011) | 2.55814 ± 0.0112635 (W 0.00810256) | 🔵 tcontract 2.20× faster than `tblis` |  |
| `mps_chain_L32_chi4/n1/b1` | 0.033352 ± 0.00157261 (W 0.000446551) | 0.525925 ± 0.00155846 (W 0.00374519) | 🔵 tcontract 15.77× faster than `tblis` | `!` between-start range over 5% |
| `mps_chain_L32_chi64/n1/b1` | 10.9068 ± 0.0136415 (W 0.0159276) | 13.9973 ± 0.120829 (W 0.226848) | 🔵 tcontract 1.28× faster than `tblis` |  |
| `mps_chain_L32_chi8/n1/b1` | 0.0616305 ± 0.0018208 (W 0.00100637) | 0.600911 ± 0.00523471 (W 0.0020678) | 🔵 tcontract 9.75× faster than `tblis` |  |

## per-shape, c64, 4T (CPU 4-7)

| case | plan (ms) | tblis (ms) | vs `tblis` | notes |
|---|---|---|---|---|
| `ij_jk_ik_c64_n32/n1/b1` | 0.009963 ± 0.000190919 (W 0.000168536) | 0.024666 ± 0.00236598 (W 0.00184167) | 🔵 tcontract 2.48× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `mps_chain_L32_chi16/n1/b1` | 0.18162 ± 0.000977222 (W 0.00277528) | 1.2789 ± 0.00423698 (W 0.0183951) | 🔵 tcontract 7.04× faster than `tblis` |  |
| `mps_chain_L32_chi32/n1/b1` | 0.998685 ± 0.00644033 (W 0.00332292) | 1.91825 ± 0.0150677 (W 0.0189075) | 🔵 tcontract 1.92× faster than `tblis` |  |
| `mps_chain_L32_chi4/n1/b1` | 0.03479 ± 0.00182009 (W 0.000226621) | 0.933949 ± 0.053359 (W 0.00623517) | 🔵 tcontract 26.85× faster than `tblis` | `!` between-start range over 5% |
| `mps_chain_L32_chi64/n1/b1` | 3.56302 ± 0.0091733 (W 0.0446388) | 5.61343 ± 0.0782378 (W 0.0326731) | 🔵 tcontract 1.58× faster than `tblis` |  |
| `mps_chain_L32_chi8/n1/b1` | 0.063629 ± 0.00242255 (W 0.000275669) | 1.1663 ± 0.00546947 (W 0.0206237) | 🔵 tcontract 18.33× faster than `tblis` | `!` between-start range over 5% |

Not applicable to this population's shapes and reported as skipped: `ij_jk_ik_c64_n32/1`, `ij_jk_ik_f64_n64/1`, `ij_jk_kl_il_n64/1`, `ijk_jkl_il_8x16x8/1`, `ikb_knb_inb_n16_b16/1`, `ikb_knb_inb_n16_b256/1`, `ikb_knb_inb_n16_b64/1`, `ikb_knb_inb_n2_b16/1`, `ikb_knb_inb_n2_b256/1`, `ikb_knb_inb_n2_b64/1`, `ikb_knb_inb_n4_b16/1`, `ikb_knb_inb_n4_b256/1`, `ikb_knb_inb_n4_b64/1`, `ikb_knb_inb_n8_b16/1`, `ikb_knb_inb_n8_b256/1`, `ikb_knb_inb_n8_b64/1`, `mps_chain_L32_chi16/1`, `mps_chain_L32_chi32/1`, `mps_chain_L32_chi4/1`, `mps_chain_L32_chi64/1`, `mps_chain_L32_chi8/1`.

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
