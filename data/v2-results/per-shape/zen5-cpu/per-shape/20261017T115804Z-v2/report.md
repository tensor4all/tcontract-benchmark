# `per-shape` on `zen5-cpu`

- tcontract-rs commit: `7738bf43a0684e7d6f0769444e846f215fec86ab`
- features: `tblis`
- tprims rows: `tprims` (the provider in the measured revision; see library above)
- external providers: `tblis` 2.0 @ `b16a732939d8454021e0a0f0097cf1cc1dd3ab19` tag `v2.0-beta2` sha256 `de00bf1552c15f9c4a5d3157f02c149b81aef0909107c51cbb54ba4b8e9b5827` (TBLIS 2.0, configuration zen3; bundled BLIS 358e689cadd6757f564a2992cf46a2f7d6fa6bb0; built with ./configure --prefix=/home/shinaoka/projects/tensor4all/tcontract-benchmark/target/tblis-v2.0-beta2 --with-blis-config-family=zen3 (cmake, Unix Makefiles, Release); libtblis.so sha256 de00bf1552c15f9c)
- harness commit: `e8d2fb678a361ad86190c4b5ed0d8e7315ea6eba`
- toolkit commit: `5a3ae9a644a64c9ad86ead088d7696839991375f`
- measured binary SHA-256: `5dbc239a2db44622d5c9e868af14b68b803589cc24d1a3fb8539ac2d0c35771b`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-17T12:01:05.838134Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 3 attempts
- command: `scripts/v2/record_run.py per-shape zen5-cpu per-shape --external-provider-json target/tblis-providers.json --label v2 --reps 5 --aa 3 --prime-ms 250`
- raw data: `data/v2-results/per-shape/zen5-cpu/per-shape/20261017T115804Z-v2/`

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
Spread guide (computed from this run's own rows): per-engine between-start range median 1.99%, worst 17.35% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 26 of 126 engine cells exceed 5% and carry `!`; median within-process relative SD 0.75%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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
| `ij_jk_ik_f64_n64/n1/b1` | 0.017131 ± 6.61085e-05 (W 1.72134e-05) | 0.024596 ± 4.0501e-05 (W 0.000126318) | 0.048531 ± 0.000569767 (W 0.00192526) | 🔵 fork 1.44× faster than `packed` | 🔵 fork 2.83× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ij_jk_kl_il_n64/n1/b1` | 0.034204 ± 4.59021e-05 (W 0.00133427) | 0.049172 ± 3.5171e-05 (W 0.000198518) | 0.097031 ± 0.000297602 (W 0.000335679) | 🔵 fork 1.44× faster than `packed` | 🔵 fork 2.84× faster than `tblis` |  |
| `ijk_jkl_il_8x16x8/n1/b1` | 0.000721 ± 5.7735e-06 (W 5.21536e-06) | 0.004819 ± 4.04145e-05 (W 5.21536e-05) | 0.016221 ± 0.000160004 (W 0.000103679) | 🔵 fork 6.68× faster than `packed` | 🔵 fork 22.50× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b16/n1/b1` | 0.006071 ± 8.5049e-05 (W 1.22474e-05) | 0.016381 ± 0.00019186 (W 0.000448641) | 0.120795 ± 0.00083341 (W 0.000250524) | 🔵 fork 2.70× faster than `packed` | 🔵 fork 19.90× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b256/n1/b1` | 0.100347 ± 0.00212561 (W 0.000384794) | 0.251458 ± 0.00480083 (W 0.00439418) | 1.88716 ± 0.0100214 (W 0.00139785) | 🔵 fork 2.51× faster than `packed` | 🔵 fork 18.81× faster than `tblis` |  |
| `ikb_knb_inb_n16_b64/n1/b1` | 0.023894 ± 0.0001948 (W 2.94958e-05) | 0.062426 ± 0.000488713 (W 0.00156937) | 0.470896 ± 0.00621275 (W 0.00198898) | 🔵 fork 2.61× faster than `packed` | 🔵 fork 19.71× faster than `tblis` |  |
| `ikb_knb_inb_n2_b16/n1/b1` | 0.000601 ± 1.52753e-05 (W 1.78885e-05) | 0.003246 ± 6.65833e-05 (W 7.56968e-05) | 0.088475 ± 0.000828084 (W 9.41807e-05) | 🔵 fork 5.40× faster than `packed` | 🔵 fork 147.21× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b256/n1/b1` | 0.007825 ± 0.000323934 (W 2.5774e-05) | 0.039012 ± 0.000823582 (W 7.2479e-05) | 1.36515 ± 0.00778382 (W 0.0024819) | 🔵 fork 4.99× faster than `packed` | 🔵 fork 174.46× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b64/n1/b1` | 0.002074 ± 6.245e-05 (W 1.14018e-05) | 0.010449 ± 0.000301292 (W 0.000143758) | 0.3441 ± 0.00563249 (W 0.0017887) | 🔵 fork 5.04× faster than `packed` | 🔵 fork 165.91× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b16/n1/b1` | 0.000852 ± 5.19615e-06 (W 5.21536e-06) | 0.004278 ± 4.50925e-05 (W 7.23187e-05) | 0.090138 ± 0.000442856 (W 0.00134976) | 🔵 fork 5.02× faster than `packed` | 🔵 fork 105.80× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b256/n1/b1` | 0.012193 ± 0.000236291 (W 8.94427e-06) | 0.054952 ± 0.00126734 (W 0.00144988) | 1.39761 ± 0.00922178 (W 0.00237643) | 🔵 fork 4.51× faster than `packed` | 🔵 fork 114.62× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b64/n1/b1` | 0.003136 ± 4.08697e-05 (W 8.31865e-06) | 0.014417 ± 0.000642424 (W 0.000136291) | 0.348298 ± 0.00669843 (W 0.00202577) | 🔵 fork 4.60× faster than `packed` | 🔵 fork 111.06× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b16/n1/b1` | 0.001383 ± 4.95681e-05 (W 1.05024e-05) | 0.006552 ± 6.08276e-05 (W 7.72218e-05) | 0.097231 ± 0.00103767 (W 0.00145727) | 🔵 fork 4.74× faster than `packed` | 🔵 fork 70.30× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b256/n1/b1` | 0.018945 ± 0.000216842 (W 3.77783e-05) | 0.090428 ± 0.000473741 (W 0.00118526) | 1.49051 ± 0.0179379 (W 0.00216864) | 🔵 fork 4.77× faster than `packed` | 🔵 fork 78.68× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b64/n1/b1` | 0.00537 ± 0.000217601 (W 4.77619e-05) | 0.023624 ± 0.000167572 (W 0.000108038) | 0.379225 ± 0.00287784 (W 0.00152529) | 🔵 fork 4.40× faster than `packed` | 🔵 fork 70.62× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |

## per-shape, f64, 4T (CPU 4-7)

| case | plan (ms) | packed (ms) | tblis (ms) | vs `packed` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `ij_jk_ik_f64_n64/n1/b1` | 0.017132 ± 2.94449e-05 (W 1.94936e-05) | 0.024616 ± 0.000135094 (W 0.000131605) | 0.032531 ± 0.000119876 (W 0.00150348) | 🔵 fork 1.44× faster than `packed` | 🔵 fork 1.90× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ij_jk_kl_il_n64/n1/b1` | 0.034223 ± 0.000144938 (W 4.8024e-05) | 0.049142 ± 0.000174041 (W 0.000166251) | 0.068007 ± 0.000848454 (W 0.00167747) | 🔵 fork 1.44× faster than `packed` | 🔵 fork 1.99× faster than `tblis` |  |
| `ijk_jkl_il_8x16x8/n1/b1` | 0.000732 ± 5.7735e-07 (W 6.02495e-06) | 0.004809 ± 5.7735e-06 (W 1.94936e-05) | 0.02156 ± 0.000263289 (W 0.000239665) | 🔵 fork 6.57× faster than `packed` | 🔵 fork 29.45× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b16/n1/b1` | 0.006051 ± 6.09945e-05 (W 8.50294e-06) | 0.016261 ± 0.00121392 (W 0.000279151) | 0.23114 ± 0.0129006 (W 0.00552828) | 🔵 fork 2.69× faster than `packed` | 🔵 fork 38.20× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n16_b256/n1/b1` | 0.030006 ± 0.000147309 (W 0.00032043) | 0.06976 ± 0.000233024 (W 0.00125482) | 1.19887 ± 0.0116107 (W 0.0145144) | 🔵 fork 2.32× faster than `packed` | 🔵 fork 39.95× faster than `tblis` |  |
| `ikb_knb_inb_n16_b64/n1/b1` | 0.023534 ± 0.00018037 (W 2.77489e-05) | 0.061885 ± 0.00616639 (W 0.00162604) | 0.898422 ± 0.0293968 (W 0.0203344) | 🔵 fork 2.63× faster than `packed` | 🔵 fork 38.18× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `ikb_knb_inb_n2_b16/n1/b1` | 0.000591 ± 1.73205e-05 (W 1.73205e-05) | 0.003216 ± 5.55908e-05 (W 0.000172575) | 0.033562 ± 0.00102228 (W 0.00180027) | 🔵 fork 5.44× faster than `packed` | 🔵 fork 56.79× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b256/n1/b1` | 0.007874 ± 0.000304008 (W 3.35887e-05) | 0.038572 ± 0.000328406 (W 0.000535254) | 0.394454 ± 0.00763682 (W 0.00474172) | 🔵 fork 4.90× faster than `packed` | 🔵 fork 50.10× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n2_b64/n1/b1` | 0.002074 ± 7.2111e-05 (W 2.16795e-05) | 0.01045 ± 0.000442314 (W 7.62712e-05) | 0.106899 ± 0.00164012 (W 0.00351094) | 🔵 fork 5.04× faster than `packed` | 🔵 fork 51.54× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b16/n1/b1` | 0.000892 ± 2.3094e-05 (W 4.72229e-06) | 0.004178 ± 0.000105357 (W 0.00011811) | 0.070672 ± 0.000530856 (W 0.00186819) | 🔵 fork 4.68× faster than `packed` | 🔵 fork 79.23× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b256/n1/b1` | 0.012463 ± 0.000230651 (W 4.57624e-05) | 0.054131 ± 0.00418592 (W 0.00253644) | 0.399564 ± 0.00318572 (W 0.00683586) | 🔵 fork 4.34× faster than `packed` | 🔵 fork 32.06× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n4_b64/n1/b1` | 0.003186 ± 7.0946e-05 (W 2.16795e-05) | 0.014167 ± 0.000722054 (W 0.000670173) | 0.10746 ± 0.00188871 (W 0.00265917) | 🔵 fork 4.45× faster than `packed` | 🔵 fork 33.73× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b16/n1/b1` | 0.001302 ± 1.52753e-05 (W 5.59464e-06) | 0.006592 ± 0.000271509 (W 8.09271e-05) | 0.170007 ± 0.00142292 (W 0.00160126) | 🔵 fork 5.06× faster than `packed` | 🔵 fork 130.57× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b256/n1/b1` | 0.018875 ± 0.000335619 (W 0.000166239) | 0.090308 ± 0.00424921 (W 0.00131515) | 0.426303 ± 0.00401397 (W 0.00460371) | 🔵 fork 4.78× faster than `packed` | 🔵 fork 22.59× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `ikb_knb_inb_n8_b64/n1/b1` | 0.005009 ± 0.000239396 (W 1.83657e-05) | 0.024666 ± 0.00148178 (W 0.000282094) | 0.285121 ± 0.00486942 (W 0.00702834) | 🔵 fork 4.92× faster than `packed` | 🔵 fork 56.92× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |

## per-shape, c64, 1T (CPU 4)

| case | plan (ms) | packed (ms) | tblis (ms) | vs `packed` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `ij_jk_ik_c64_n32/n1/b1` | 0.008867 ± 1.18462e-05 (W 1.1327e-05) | 0.013065 ± 4.78226e-05 (W 6.66056e-05) | 0.024706 ± 6.245e-05 (W 5.81739e-05) | 🔵 fork 1.47× faster than `packed` | 🔵 fork 2.79× faster than `tblis` | dispatch-dominated (row under 20 us) |
| `mps_chain_L32_chi16/n1/b1` | 0.160288 ± 0.00101682 (W 0.00170151) | 0.302312 ± 0.000673485 (W 0.00211732) | 0.908391 ± 0.00149283 (W 0.00163093) | 🔵 fork 1.89× faster than `packed` | 🔵 fork 5.67× faster than `tblis` |  |
| `mps_chain_L32_chi32/n1/b1` | 1.15665 ± 0.000241634 (W 0.00224155) | 1.58018 ± 0.0026473 (W 0.0037958) | 2.53974 ± 0.00969071 (W 0.00798288) | 🔵 fork 1.37× faster than `packed` | 🔵 fork 2.20× faster than `tblis` |  |
| `mps_chain_L32_chi4/n1/b1` | 0.024586 ± 0.000327735 (W 0.000317387) | 0.073236 ± 0.00077735 (W 0.000186808) | 0.530758 ± 0.00389744 (W 0.00174918) | 🔵 fork 2.98× faster than `packed` | 🔵 fork 21.59× faster than `tblis` |  |
| `mps_chain_L32_chi64/n1/b1` | 10.9181 ± 0.0220653 (W 0.00852309) | 10.8949 ± 0.0197734 (W 0.0062841) | 13.8053 ± 0.0230555 (W 0.0180052) | · | 🔵 fork 1.26× faster than `tblis` |  |
| `mps_chain_L32_chi8/n1/b1` | 0.05342 ± 0.000205322 (W 0.000360072) | 0.11789 ± 0.00107155 (W 0.00168953) | 0.603122 ± 0.00240348 (W 0.00186196) | 🔵 fork 2.21× faster than `packed` | 🔵 fork 11.29× faster than `tblis` |  |

## per-shape, c64, 4T (CPU 4-7)

| case | plan (ms) | packed (ms) | tblis (ms) | vs `packed` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `ij_jk_ik_c64_n32/n1/b1` | 0.008886 ± 3.5171e-05 (W 1.71552e-05) | 0.013085 ± 0.000290266 (W 3.61566e-05) | 0.023944 ± 0.000908192 (W 0.00284643) | 🔵 fork 1.47× faster than `packed` | 🔵 fork 2.69× faster than `tblis` | `!` between-start range over 5%; dispatch-dominated (row under 20 us) |
| `mps_chain_L32_chi16/n1/b1` | 0.162012 ± 0.000529379 (W 0.00196476) | 0.303154 ± 0.000907097 (W 0.00214972) | 1.37682 ± 0.0334368 (W 0.0249652) | 🔵 fork 1.87× faster than `packed` | 🔵 fork 8.50× faster than `tblis` |  |
| `mps_chain_L32_chi32/n1/b1` | 1.15609 ± 0.00129287 (W 0.00193877) | 1.58125 ± 0.00367816 (W 0.00205588) | 1.91215 ± 0.0531135 (W 0.0120328) | 🔵 fork 1.37× faster than `packed` | 🔵 fork 1.65× faster than `tblis` | `!` between-start range over 5% |
| `mps_chain_L32_chi4/n1/b1` | 0.024786 ± 0.000215948 (W 0.00125744) | 0.073917 ± 0.000698743 (W 0.000319629) | 0.97245 ± 0.00103156 (W 0.00439366) | 🔵 fork 2.98× faster than `packed` | 🔵 fork 39.23× faster than `tblis` |  |
| `mps_chain_L32_chi64/n1/b1` | 4.07602 ± 0.16378 (W 0.0754234) | 4.06248 ± 0.107092 (W 0.137886) | 5.54452 ± 0.06653 (W 0.0260222) | · | 🔵 fork 1.36× faster than `tblis` | `!` between-start range over 5% |
| `mps_chain_L32_chi8/n1/b1` | 0.05333 ± 0.000311079 (W 0.000276299) | 0.120314 ± 0.00134281 (W 0.00168434) | 1.21968 ± 0.0195612 (W 0.0170136) | 🔵 fork 2.26× faster than `packed` | 🔵 fork 22.87× faster than `tblis` |  |

Not applicable to this population's shapes and reported as skipped: `ij_jk_ik_c64_n32/1`, `ij_jk_ik_f64_n64/1`, `ij_jk_kl_il_n64/1`, `ijk_jkl_il_8x16x8/1`, `ikb_knb_inb_n16_b16/1`, `ikb_knb_inb_n16_b256/1`, `ikb_knb_inb_n16_b64/1`, `ikb_knb_inb_n2_b16/1`, `ikb_knb_inb_n2_b256/1`, `ikb_knb_inb_n2_b64/1`, `ikb_knb_inb_n4_b16/1`, `ikb_knb_inb_n4_b256/1`, `ikb_knb_inb_n4_b64/1`, `ikb_knb_inb_n8_b16/1`, `ikb_knb_inb_n8_b256/1`, `ikb_knb_inb_n8_b64/1`, `mps_chain_L32_chi16/1`, `mps_chain_L32_chi32/1`, `mps_chain_L32_chi4/1`, `mps_chain_L32_chi64/1`, `mps_chain_L32_chi8/1`.

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
