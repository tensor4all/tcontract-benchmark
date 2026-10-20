# `per-shape` on `zen5-cpu`

- tcontract-rs commit: `61a04eb1562c671775d1ce254212a598334d3dbb`
- features: `tblis`
- tprims rows: `tprims` (the provider in the measured revision; see library above)
- external providers: `tblis` 2.0 @ `b16a732939d8454021e0a0f0097cf1cc1dd3ab19` tag `v2.0-beta2` sha256 `de00bf1552c15f9c4a5d3157f02c149b81aef0909107c51cbb54ba4b8e9b5827` (TBLIS 2.0, configuration zen3; bundled BLIS 358e689cadd6757f564a2992cf46a2f7d6fa6bb0; built with ./configure --prefix=/home/shinaoka/projects/tensor4all/tcontract-benchmark/target/tblis-v2.0-beta2 --with-blis-config-family=zen3 (cmake, Unix Makefiles, Release); libtblis.so sha256 de00bf1552c15f9c)
- harness commit: `667c5b5cd90f6ca06b9dbaad754c51642c0df244`
- toolkit commit: `40e7e11c031788543163d3251b51ee24af72162c`
- measured binary SHA-256: `16d0d462f2cc4e607e1d6e7ff579c4f191dfc23835a7b6452ded8ef75b5e2568`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-20T13:18:52.003536Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/v2/record_run.py per-shape zen5-cpu per-shape --aa 2 --reps 5 --prime-ms 250 --external-provider-json /tmp/tblis-v2.json --label split-per-shape`
- raw data: `data/v2-results/per-shape/zen5-cpu/per-shape/20261020T131729Z-split-per-shape/`

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
Spread guide (computed from this run's own rows): per-engine between-start range median 1.47%, worst 15.77% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 8 of 84 engine cells exceed 5% and carry `!`; median within-process relative SD 0.48%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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
two rows (combined between-start SD, floored at 5%), always with the measured library as the subject:
`🔵 fork X faster than <row>` / `🔴 fork X slower than <row>` (the compared row is named in
the cell, not only in the column header), `·` inside the band, `-` that row is not
measured in this arm. `notes` carries the cell warnings (`*` a declared row has no measurement,
`!` between-start range over 5%, `p` position effect over 5%, dispatch-dominated means the
row is under 20 us so 4T/8T pay thread-region start-up). Per-start ratios and every
chronological sample are in the run directory named at the top of this page (`run*.csv`).
These describe the recorded revisions; they are not a regression claim.

## per-shape, f64, 1T (CPU 4)

| case | plan (ms) | tblis (ms) | vs `tblis` | notes |
|---|---|---|---|---|
| `ij_jk_ik_f64_n64/n1/b1` | 0.017392 ± 0.000240416 (W 1.9383e-05) | 0.048315 ± 0.000362039 (W 0.000712029) | 🔵 fork 2.78× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ij_jk_kl_il_n64/n1/b1` | 0.0345895 ± 0.000120915 (W 5.55944e-05) | 0.096905 ± 0.000473762 (W 0.00117263) | 🔵 fork 2.80× faster than `tblis` |  |
| `ijk_jkl_il_8x16x8/n1/b1` | 0.000827 ± 7.07107e-06 (W 7.421e-06) | 0.01611 ± 4.24264e-05 (W 6.48689e-05) | 🔵 fork 19.48× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b16/n1/b1` | 0.005961 ± 1.41421e-05 (W 9.88418e-06) | 0.122082 ± 0.00116885 (W 0.00020941) | 🔵 fork 20.48× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b256/n1/b1` | 0.0995955 ± 0.000226981 (W 0.00189542) | 1.90101 ± 0.0182921 (W 0.00151165) | 🔵 fork 19.09× faster than `tblis` |  |
| `ikb_knb_inb_n16_b64/n1/b1` | 0.0236895 ± 0.000135057 (W 0.00071655) | 0.476469 ± 0.00529199 (W 0.00245011) | 🔵 fork 20.11× faster than `tblis` |  |
| `ikb_knb_inb_n2_b16/n1/b1` | 0.000706 ± 7.07107e-06 (W 2.17621e-05) | 0.088945 ± 0.00128976 (W 0.000889009) | 🔵 fork 125.98× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b256/n1/b1` | 0.007995 ± 5.65685e-05 (W 2.59806e-05) | 1.37765 ± 0.0354847 (W 0.00212261) | 🔵 fork 172.31× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b64/n1/b1` | 0.002194 ± 4.24264e-05 (W 0.000525887) | 0.343272 ± 0.00543412 (W 0.00138063) | 🔵 fork 156.46× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b16/n1/b1` | 0.0009615 ± 1.48492e-05 (W 7.78054e-06) | 0.090633 ± 0.00157968 (W 0.000117547) | 🔵 fork 94.26× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b256/n1/b1` | 0.012388 ± 0.000446891 (W 4.29094e-05) | 1.41102 ± 0.0275149 (W 0.00193358) | 🔵 fork 113.90× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b64/n1/b1` | 0.0032415 ± 9.2631e-05 (W 1.68657e-05) | 0.353882 ± 0.00636891 (W 0.00150267) | 🔵 fork 109.17× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b16/n1/b1` | 0.0013525 ± 1.48492e-05 (W 1.13898e-05) | 0.0981975 ± 0.00115471 (W 0.0017477) | 🔵 fork 72.60× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b256/n1/b1` | 0.0187245 ± 0.000255266 (W 4.62826e-05) | 1.51725 ± 0.0276288 (W 0.00440746) | 🔵 fork 81.03× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b64/n1/b1` | 0.00523 ± 5.65685e-05 (W 1.94379e-05) | 0.381018 ± 0.00393929 (W 0.001424) | 🔵 fork 72.85× faster than `tblis` | dispatch-dominated (row under 20 us) |

## per-shape, f64, 4T (CPU 4-7)

| case | plan (ms) | tblis (ms) | vs `tblis` | notes |
|---|---|---|---|---|
| `ij_jk_ik_f64_n64/n1/b1` | 0.0172925 ± 7.14178e-05 (W 0.000580027) | 0.0345745 ± 0.00385444 (W 0.00231758) | 🔵 fork 2.00× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5%; dispatch-dominated (row under 20 us) |
| `ij_jk_kl_il_n64/n1/b1` | 0.034504 ± 4.24264e-05 (W 2.35634e-05) | 0.0643145 ± 0.00118299 (W 0.00275097) | 🔵 fork 1.86× faster than `tblis` |  |
| `ijk_jkl_il_8x16x8/n1/b1` | 0.000827 ± 7.07107e-06 (W 4.52533e-06) | 0.020593 ± 0.00033234 (W 0.000284946) | 🔵 fork 24.90× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b16/n1/b1` | 0.006131 ± 1.41421e-05 (W 8.83677e-06) | 0.237856 ± 0.00889045 (W 0.0086884) | 🔵 fork 38.80× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b256/n1/b1` | 0.030562 ± 3.53553e-05 (W 0.000319368) | 1.23459 ± 0.0166616 (W 0.00836432) | 🔵 fork 40.40× faster than `tblis` |  |
| `ikb_knb_inb_n16_b64/n1/b1` | 0.0235535 ± 8.41457e-05 (W 3.83966e-05) | 0.935297 ± 0.0180227 (W 0.0220441) | 🔵 fork 39.71× faster than `tblis` |  |
| `ikb_knb_inb_n2_b16/n1/b1` | 0.000711 ± 0 (W 1.04348e-05) | 0.032796 ± 0.000432749 (W 0.00279103) | 🔵 fork 46.13× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b256/n1/b1` | 0.0082055 ± 0.000297692 (W 1.0423e-05) | 0.397077 ± 0.00760847 (W 0.00677122) | 🔵 fork 48.39× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b64/n1/b1` | 0.002204 ± 8.48528e-05 (W 2.93387e-05) | 0.10516 ± 0.00213193 (W 0.00154837) | 🔵 fork 47.71× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b16/n1/b1` | 0.0009765 ± 7.77817e-06 (W 7.83368e-06) | 0.069344 ± 4.94975e-05 (W 0.00118229) | 🔵 fork 71.01× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b256/n1/b1` | 0.0125935 ± 8.55599e-05 (W 1.45335e-05) | 0.408062 ± 0.00102743 (W 0.00566896) | 🔵 fork 32.40× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b64/n1/b1` | 0.003321 ± 7.07107e-06 (W 6.63209e-06) | 0.109824 ± 0.00185686 (W 0.00266439) | 🔵 fork 33.07× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b16/n1/b1` | 0.0014125 ± 1.48492e-05 (W 1.11832e-05) | 0.168493 ± 0.00276337 (W 0.00246216) | 🔵 fork 119.29× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b256/n1/b1` | 0.0193965 ± 0.000594677 (W 7.78794e-05) | 0.427589 ± 0.00335098 (W 0.00686542) | 🔵 fork 22.04× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b64/n1/b1` | 0.004894 ± 6.36396e-05 (W 4.34835e-05) | 0.283121 ± 0.00512228 (W 0.00900804) | 🔵 fork 57.85× faster than `tblis` | dispatch-dominated (row under 20 us) |

## per-shape, c64, 1T (CPU 4)

| case | plan (ms) | tblis (ms) | vs `tblis` | notes |
|---|---|---|---|---|
| `ij_jk_ik_c64_n32/n1/b1` | 0.0090165 ± 5.58614e-05 (W 1.14958e-05) | 0.024796 ± 2.82843e-05 (W 6.05679e-05) | 🔵 fork 2.75× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `mps_chain_L32_chi16/n1/b1` | 0.16677 ± 7.07107e-07 (W 0.00149344) | 0.902882 ± 0.00165109 (W 0.000922655) | 🔵 fork 5.41× faster than `tblis` |  |
| `mps_chain_L32_chi32/n1/b1` | 1.16337 ± 0.000226274 (W 0.00370002) | 2.55319 ± 0.00716936 (W 0.0088201) | 🔵 fork 2.19× faster than `tblis` |  |
| `mps_chain_L32_chi4/n1/b1` | 0.031428 ± 0.000353553 (W 0.000315529) | 0.523002 ± 0.00109107 (W 0.00140626) | 🔵 fork 16.64× faster than `tblis` |  |
| `mps_chain_L32_chi64/n1/b1` | 10.894 ± 0.00289843 (W 0.0152492) | 13.7744 ± 0.0833757 (W 0.0606757) | 🔵 fork 1.26× faster than `tblis` |  |
| `mps_chain_L32_chi8/n1/b1` | 0.060502 ± 0.000581242 (W 0.000773789) | 0.59756 ± 0.00423628 (W 0.00192466) | 🔵 fork 9.88× faster than `tblis` |  |

## per-shape, c64, 4T (CPU 4-7)

| case | plan (ms) | tblis (ms) | vs `tblis` | notes |
|---|---|---|---|---|
| `ij_jk_ik_c64_n32/n1/b1` | 0.0089965 ± 4.31335e-05 (W 2.03568e-05) | 0.023704 ± 0.000666095 (W 0.0019987) | 🔵 fork 2.63× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `mps_chain_L32_chi16/n1/b1` | 0.168502 ± 0.000523966 (W 0.00218172) | 1.36423 ± 0.0557448 (W 0.0139513) | 🔵 fork 8.10× faster than `tblis` | `!` between-start range over 5% |
| `mps_chain_L32_chi32/n1/b1` | 1.1678 ± 0.00648275 (W 0.00241947) | 1.91434 ± 0.04721 (W 0.0222545) | 🔵 fork 1.64× faster than `tblis` |  |
| `mps_chain_L32_chi4/n1/b1` | 0.032049 ± 0.000155563 (W 0.000311519) | 0.957202 ± 0.0513112 (W 0.00253892) | 🔵 fork 29.87× faster than `tblis` | `!` between-start range over 5% |
| `mps_chain_L32_chi64/n1/b1` | 4.05505 ± 0.106823 (W 0.14407) | 5.56742 ± 0.0614476 (W 0.0175714) | 🔵 fork 1.37× faster than `tblis` |  |
| `mps_chain_L32_chi8/n1/b1` | 0.0610185 ± 0.000446184 (W 0.000216776) | 1.2677 ± 0.0499868 (W 0.0231547) | 🔵 fork 20.78× faster than `tblis` | `!` between-start range over 5% |

Not applicable to this population's shapes and reported as skipped: `ij_jk_ik_c64_n32/1`, `ij_jk_ik_f64_n64/1`, `ij_jk_kl_il_n64/1`, `ijk_jkl_il_8x16x8/1`, `ikb_knb_inb_n16_b16/1`, `ikb_knb_inb_n16_b256/1`, `ikb_knb_inb_n16_b64/1`, `ikb_knb_inb_n2_b16/1`, `ikb_knb_inb_n2_b256/1`, `ikb_knb_inb_n2_b64/1`, `ikb_knb_inb_n4_b16/1`, `ikb_knb_inb_n4_b256/1`, `ikb_knb_inb_n4_b64/1`, `ikb_knb_inb_n8_b16/1`, `ikb_knb_inb_n8_b256/1`, `ikb_knb_inb_n8_b64/1`, `mps_chain_L32_chi16/1`, `mps_chain_L32_chi32/1`, `mps_chain_L32_chi4/1`, `mps_chain_L32_chi64/1`, `mps_chain_L32_chi8/1`.

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
