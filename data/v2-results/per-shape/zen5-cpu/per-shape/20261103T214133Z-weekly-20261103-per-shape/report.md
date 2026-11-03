# `per-shape` on `zen5-cpu`

- tcontract-rs commit: `9f793ede6b8076fd7ce2251594a9552ad66aa339`
- features: `tblis`
- tprims rows: `tprims` (the provider in the measured revision; see library above)
- external providers: `tblis` 2.0 @ `b16a732939d8454021e0a0f0097cf1cc1dd3ab19` tag `v2.0-beta2` sha256 `de00bf1552c15f9c4a5d3157f02c149b81aef0909107c51cbb54ba4b8e9b5827` (TBLIS 2.0, configuration zen3; bundled BLIS 358e689cadd6757f564a2992cf46a2f7d6fa6bb0; built with ./configure --prefix=/home/shinaoka/projects/tensor4all/tcontract-benchmark/target/tblis-v2.0-beta2 --with-blis-config-family=zen3 (cmake, Unix Makefiles, Release); libtblis.so sha256 de00bf1552c15f9c)
- harness commit: `152315f3bad3a68bf4f99f63e2be5ddc83421673`
- toolkit commit: `74e50e8199cb2c2f07e810744a0943fc3a8c1170`
- measured binary SHA-256: `d58043e7e73b59b64eac9c9841528665708ad6fd8cd9d5b310d10f92a1449001`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-11-03T21:42:55.942521Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/v2/record_run.py per-shape zen5-cpu per-shape --aa 2 --reps 5 --prime-ms 250 --external-provider-json /home/shinaoka/.local/state/tensor4all-weekly/20261103/tcontract/tblis-providers.json --label weekly-20261103-per-shape --no-publish`
- raw data: `data/v2-results/per-shape/zen5-cpu/per-shape/20261103T214133Z-weekly-20261103-per-shape/`

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
Spread guide (computed from this run's own rows): per-engine between-start range median 0.89%, worst 12.89% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 6 of 84 engine cells exceed 5% and carry `!`; median within-process relative SD 0.65%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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
| `ij_jk_ik_f64_n64/n1/b1` | 0.017347 ± 3.53553e-05 (W 2.69015e-05) | 0.04834 ± 0 (W 0.000239973) | 🔵 tcontract 2.79× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ij_jk_kl_il_n64/n1/b1` | 0.0348645 ± 0.000368403 (W 1.5744e-05) | 0.09664 ± 0.000666095 (W 0.00190352) | 🔵 tcontract 2.77× faster than `tblis` |  |
| `ijk_jkl_il_8x16x8/n1/b1` | 0.0008365 ± 7.77817e-06 (W 5.50379e-06) | 0.01615 ± 7.07107e-05 (W 5.22283e-05) | 🔵 tcontract 19.31× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b16/n1/b1` | 0.006001 ± 2.82843e-05 (W 1.3504e-05) | 0.122613 ± 0.000758018 (W 0.0011286) | 🔵 tcontract 20.43× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b256/n1/b1` | 0.100328 ± 0.00252225 (W 0.00106122) | 1.91707 ± 0.0008358 (W 0.00276677) | 🔵 tcontract 19.11× faster than `tblis` |  |
| `ikb_knb_inb_n16_b64/n1/b1` | 0.0234985 ± 0.000191626 (W 2.20657e-05) | 0.480469 ± 0.00163695 (W 0.0020703) | 🔵 tcontract 20.45× faster than `tblis` |  |
| `ikb_knb_inb_n2_b16/n1/b1` | 0.0007765 ± 2.19203e-05 (W 1.1246e-05) | 0.0899175 ± 9.82878e-05 (W 0.000749528) | 🔵 tcontract 115.80× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b256/n1/b1` | 0.0090665 ± 2.89914e-05 (W 3.44798e-05) | 1.38545 ± 0.0158116 (W 0.00265517) | 🔵 tcontract 152.81× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b64/n1/b1` | 0.0024295 ± 2.05061e-05 (W 0.000211698) | 0.348148 ± 0.000467398 (W 0.00181727) | 🔵 tcontract 143.30× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b16/n1/b1` | 0.001047 ± 7.07107e-06 (W 1.26429e-05) | 0.091455 ± 0.00013435 (W 0.000774454) | 🔵 tcontract 87.35× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b256/n1/b1` | 0.013786 ± 0.000595384 (W 0.000555389) | 1.42556 ± 0.00886995 (W 0.00450398) | 🔵 tcontract 103.41× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b64/n1/b1` | 0.003557 ± 1.41421e-05 (W 1.0019e-05) | 0.360031 ± 0.000269408 (W 0.00271902) | 🔵 tcontract 101.22× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b16/n1/b1` | 0.0014525 ± 7.07107e-07 (W 4.55463e-06) | 0.098538 ± 4.94975e-05 (W 0.000863643) | 🔵 tcontract 67.84× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b256/n1/b1` | 0.020077 ± 0.000510531 (W 3.08937e-05) | 1.52481 ± 0.0144801 (W 0.00292766) | 🔵 tcontract 75.95× faster than `tblis` |  |
| `ikb_knb_inb_n8_b64/n1/b1` | 0.00543 ± 0 (W 2.43993e-05) | 0.385562 ± 0.000999142 (W 0.00244214) | 🔵 tcontract 71.01× faster than `tblis` | dispatch-dominated (row under 20 us) |

## per-shape, f64, 4T (CPU 4-7)

| case | plan (ms) | tblis (ms) | vs `tblis` | notes |
|---|---|---|---|---|
| `ij_jk_ik_f64_n64/n1/b1` | 0.011797 ± 0.000106066 (W 0.000140286) | 0.0324405 ± 0.000170413 (W 0.00642846) | 🔵 tcontract 2.75× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ij_jk_kl_il_n64/n1/b1` | 0.0232835 ± 0.000410829 (W 0.000207396) | 0.066775 ± 0.00063781 (W 0.00281204) | 🔵 tcontract 2.87× faster than `tblis` |  |
| `ijk_jkl_il_8x16x8/n1/b1` | 0.000862 ± 1.41421e-05 (W 1.40991e-05) | 0.02148 ± 0.000127279 (W 0.000536302) | 🔵 tcontract 24.92× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b16/n1/b1` | 0.00252 ± 4.94975e-05 (W 6.68855e-05) | 0.235114 ± 0.00132441 (W 0.00577665) | 🔵 tcontract 93.30× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b256/n1/b1` | 0.024365 ± 2.82843e-05 (W 3.90997e-05) | 1.21717 ± 0.0154291 (W 0.0144614) | 🔵 tcontract 49.96× faster than `tblis` |  |
| `ikb_knb_inb_n16_b64/n1/b1` | 0.006763 ± 4.24264e-05 (W 3.11057e-05) | 0.925228 ± 0.084338 (W 0.0187468) | 🔵 tcontract 136.81× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b16/n1/b1` | 0.000791 ± 1.41421e-05 (W 1.35351e-05) | 0.0325005 ± 0.000523966 (W 0.00177819) | 🔵 tcontract 41.09× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b256/n1/b1` | 0.009002 ± 2.12132e-05 (W 2.5248e-05) | 0.403166 ± 0.0022882 (W 0.00414018) | 🔵 tcontract 44.79× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b64/n1/b1` | 0.002435 ± 1.41421e-05 (W 2.37726e-05) | 0.105256 ± 0.000892369 (W 0.00233979) | 🔵 tcontract 43.23× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b16/n1/b1` | 0.0010465 ± 6.43467e-05 (W 1.17082e-05) | 0.070071 ± 0.000708521 (W 0.000604658) | 🔵 tcontract 66.96× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b256/n1/b1` | 0.013325 ± 0.000212132 (W 8.17885e-05) | 0.408676 ± 0.00512157 (W 0.00729806) | 🔵 tcontract 30.67× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b64/n1/b1` | 0.003447 ± 7.07107e-05 (W 4.38853e-05) | 0.106943 ± 0.00184908 (W 0.00190434) | 🔵 tcontract 31.03× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b16/n1/b1` | 0.001498 ± 7.07107e-06 (W 1.40898e-05) | 0.168914 ± 0.000495682 (W 0.00188506) | 🔵 tcontract 112.76× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b256/n1/b1` | 0.0062315 ± 0.000184555 (W 3.72162e-05) | 0.424741 ± 0.00586545 (W 0.00648811) | 🔵 tcontract 68.16× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b64/n1/b1` | 0.0027105 ± 7.77817e-06 (W 2.23039e-05) | 0.281023 ± 0.00395343 (W 0.00638671) | 🔵 tcontract 103.68× faster than `tblis` | dispatch-dominated (row under 20 us) |

## per-shape, c64, 1T (CPU 4)

| case | plan (ms) | tblis (ms) | vs `tblis` | notes |
|---|---|---|---|---|
| `ij_jk_ik_c64_n32/n1/b1` | 0.0090565 ± 2.89914e-05 (W 1.62498e-05) | 0.024871 ± 2.12132e-05 (W 5.69541e-05) | 🔵 tcontract 2.75× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `mps_chain_L32_chi16/n1/b1` | 0.168068 ± 0.000431335 (W 0.00190146) | 0.90451 ± 0.00295359 (W 0.00221489) | 🔵 tcontract 5.38× faster than `tblis` |  |
| `mps_chain_L32_chi32/n1/b1` | 1.15972 ± 0.00870661 (W 0.00215028) | 2.55227 ± 0.00221042 (W 0.00451389) | 🔵 tcontract 2.20× faster than `tblis` |  |
| `mps_chain_L32_chi4/n1/b1` | 0.0325255 ± 0.00115471 (W 0.000371786) | 0.522007 ± 0.0060995 (W 0.0027025) | 🔵 tcontract 16.05× faster than `tblis` | `!` between-start range over 5% |
| `mps_chain_L32_chi64/n1/b1` | 10.9074 ± 0.0695461 (W 0.0114717) | 13.7328 ± 0.00578767 (W 0.0894439) | 🔵 tcontract 1.26× faster than `tblis` |  |
| `mps_chain_L32_chi8/n1/b1` | 0.0617305 ± 0.000234052 (W 0.00101438) | 0.59853 ± 0.00346412 (W 0.0026301) | 🔵 tcontract 9.70× faster than `tblis` |  |

## per-shape, c64, 4T (CPU 4-7)

| case | plan (ms) | tblis (ms) | vs `tblis` | notes |
|---|---|---|---|---|
| `ij_jk_ik_c64_n32/n1/b1` | 0.0098435 ± 7.77817e-06 (W 0.000159584) | 0.0235435 ± 0.00174302 (W 0.00148286) | 🔵 tcontract 2.39× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `mps_chain_L32_chi16/n1/b1` | 0.181012 ± 0.00150826 (W 0.00229977) | 1.34777 ± 0.00223163 (W 0.0206073) | 🔵 tcontract 7.45× faster than `tblis` |  |
| `mps_chain_L32_chi32/n1/b1` | 0.993545 ± 0.0086359 (W 0.00316845) | 1.89701 ± 0.00294722 (W 0.0103325) | 🔵 tcontract 1.91× faster than `tblis` |  |
| `mps_chain_L32_chi4/n1/b1` | 0.0340235 ± 0.000864792 (W 0.000307378) | 0.937636 ± 0.02709 (W 0.00430307) | 🔵 tcontract 27.56× faster than `tblis` |  |
| `mps_chain_L32_chi64/n1/b1` | 3.54544 ± 0.0121983 (W 0.0105549) | 5.58351 ± 0.0180362 (W 0.0290481) | 🔵 tcontract 1.57× faster than `tblis` |  |
| `mps_chain_L32_chi8/n1/b1` | 0.062136 ± 0.000807516 (W 0.00157833) | 1.158 ± 0.0474363 (W 0.0121289) | 🔵 tcontract 18.64× faster than `tblis` | `!` between-start range over 5% |

Not applicable to this population's shapes and reported as skipped: `ij_jk_ik_c64_n32/1`, `ij_jk_ik_f64_n64/1`, `ij_jk_kl_il_n64/1`, `ijk_jkl_il_8x16x8/1`, `ikb_knb_inb_n16_b16/1`, `ikb_knb_inb_n16_b256/1`, `ikb_knb_inb_n16_b64/1`, `ikb_knb_inb_n2_b16/1`, `ikb_knb_inb_n2_b256/1`, `ikb_knb_inb_n2_b64/1`, `ikb_knb_inb_n4_b16/1`, `ikb_knb_inb_n4_b256/1`, `ikb_knb_inb_n4_b64/1`, `ikb_knb_inb_n8_b16/1`, `ikb_knb_inb_n8_b256/1`, `ikb_knb_inb_n8_b64/1`, `mps_chain_L32_chi16/1`, `mps_chain_L32_chi32/1`, `mps_chain_L32_chi4/1`, `mps_chain_L32_chi64/1`, `mps_chain_L32_chi8/1`.

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
