# `tcbench` on `zen5-cpu`

- tcontract-rs commit: `9f793ede6b8076fd7ce2251594a9552ad66aa339`
- features: `blas, tblis`
- tprims rows: `tprims` (the provider in the measured revision; see library above); `openblas` (the provider in the measured revision; see library above)
- external providers: `tblis` 2.0 @ `b16a732939d8454021e0a0f0097cf1cc1dd3ab19` tag `v2.0-beta2` sha256 `407b4f6fef7f4ede52a224cb33a987893dca37fe1177f5412b407bc93ea834e6` (TBLIS 2.0, configuration zen3; bundled BLIS 358e689cadd6757f564a2992cf46a2f7d6fa6bb0; built with ./configure --prefix=/home/shinaoka/opt/tblis-v2.0-beta2-zen3 --with-blis-config-family=zen3 (cmake, Unix Makefiles, Release); libtblis.so sha256 407b4f6fef7f4ede)
- harness commit: `4f7f935ac58126107a8c7f098b684fa809d9b4b7`
- toolkit commit: `b71624bef111ce941bddaedcce3fdb6eab40f9eb`
- measured binary SHA-256: `81a1fe3ea90fe4e232eb039ed5d4206a345fbb8eda3959e3df263054b0d61f96`
- hardware profile: `zen5-cpu`
- host role: `development` — **provisional**: recorded on a development host, superseded by the measurement host's dataset
- timestamp: `2026-10-31T12:00:42.613773Z`
- timing policy: v2, median of 5 reps, priming 250 ms (time-based, identical on every row)
- guards: idle window 3 s, max busy 5.0% including SMT siblings, 1 attempts
- command: `scripts/v2/record_run.py tcbench zen5-cpu tcbench --aa 3 --reps 5 --prime-ms 250 --external-provider-json /tmp/tmp.9C5AuzRU0f --label pub-20261031-tcbench`
- raw data: `data/v2-results/tcbench/zen5-cpu/tcbench/20261031T114950Z-pub-20261031-tcbench/`

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
Each process retains 5 chronological calls; 3 complete process sets are recorded.
Spread guide (computed from this run's own rows): per-engine between-start range median 3.94%, worst 76.58% among cells of 1 us or more (a sub-microsecond row is timer and scheduler jitter, not kernel time); 271 of 588 engine cells exceed 5% and carry `!`; median within-process relative SD 0.35%. A cell whose `±`, `!` or `p` is as large as the difference you are reading is not evidence of a regression.
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
| `abc-bk-akc/n1/b1` | 1.01877 ± 0.00367343 (W 0.00283701) | 1.98675 ± 0.00479453 (W 0.00204592) | 1.50789 ± 0.0070617 (W 0.00537983) | 🔵 tcontract 1.95× faster than `ttgt` | 🔵 tcontract 1.48× faster than `tblis` |  |
| `abcijk-eiab-jkec/n1/b1` | 4.49585 ± 0.00728473 (W 0.0140921) | 8.84422 ± 0.0372189 (W 0.0343073) | 5.4167 ± 0.0882432 (W 0.0216351) | 🔵 tcontract 1.97× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `abcijk-eiac-jkeb/n1/b1` | 4.30776 ± 0.0170577 (W 0.00489071) | 10.0016 ± 0.0200977 (W 0.0223446) | 6.67871 ± 0.131374 (W 0.024591) | 🔵 tcontract 2.32× faster than `ttgt` | 🔵 tcontract 1.55× faster than `tblis` |  |
| `abcijk-eibc-jkea/n1/b1` | 4.57392 ± 0.00688341 (W 0.0082733) | 11.6008 ± 0.141815 (W 0.0593111) | 5.37719 ± 0.111191 (W 0.0157094) | 🔵 tcontract 2.54× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `abcijk-ejab-ikec/n1/b1` | 4.45519 ± 0.00917826 (W 0.0216016) | 8.81184 ± 0.0271419 (W 0.0283353) | 5.4076 ± 0.0610333 (W 0.0209351) | 🔵 tcontract 1.98× faster than `ttgt` | 🔵 tcontract 1.21× faster than `tblis` |  |
| `abcijk-ejac-ikeb/n1/b1` | 4.31883 ± 0.0250106 (W 0.00731588) | 10.1243 ± 0.0313646 (W 0.0550895) | 5.6979 ± 0.0491022 (W 0.0244232) | 🔵 tcontract 2.34× faster than `ttgt` | 🔵 tcontract 1.32× faster than `tblis` |  |
| `abcijk-ejbc-ikea/n1/b1` | 4.59933 ± 0.0298551 (W 0.00990584) | 11.7506 ± 0.158477 (W 0.0989989) | 5.72422 ± 0.0315336 (W 0.0272538) | 🔵 tcontract 2.55× faster than `ttgt` | 🔵 tcontract 1.24× faster than `tblis` |  |
| `abcijk-ekab-ijec/n1/b1` | 4.44125 ± 0.011271 (W 0.00822257) | 9.19075 ± 0.018135 (W 0.0178668) | 5.24109 ± 0.0479376 (W 0.0242516) | 🔵 tcontract 2.07× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `abcijk-ekac-ijeb/n1/b1` | 4.33422 ± 0.0343239 (W 0.0145626) | 10.978 ± 0.0485536 (W 0.0586142) | 5.83242 ± 0.0472269 (W 0.0254654) | 🔵 tcontract 2.53× faster than `ttgt` | 🔵 tcontract 1.35× faster than `tblis` |  |
| `abcijk-ekbc-ijea/n1/b1` | 4.58819 ± 0.0252334 (W 0.0143616) | 12.0502 ± 0.0821297 (W 0.072063) | 5.69056 ± 0.0303495 (W 0.0110358) | 🔵 tcontract 2.63× faster than `ttgt` | 🔵 tcontract 1.24× faster than `tblis` |  |
| `abcijk-ijma-mkbc/n1/b1` | 4.56074 ± 0.0155719 (W 0.0136828) | 38.6931 ± 0.339652 (W 0.0634987) | 5.71247 ± 0.0222764 (W 0.0325759) | 🔵 tcontract 8.48× faster than `ttgt` | 🔵 tcontract 1.25× faster than `tblis` |  |
| `abcijk-ijmb-mkac/n1/b1` | 4.30068 ± 0.0226607 (W 0.0158072) | 36.0543 ± 0.185059 (W 0.125925) | 5.85589 ± 0.00739105 (W 0.0176146) | 🔵 tcontract 8.38× faster than `ttgt` | 🔵 tcontract 1.36× faster than `tblis` |  |
| `abcijk-ijmc-mkab/n1/b1` | 4.4509 ± 0.0149104 (W 0.0300822) | 37.028 ± 0.203323 (W 0.291331) | 5.21711 ± 0.0412488 (W 0.011845) | 🔵 tcontract 8.32× faster than `ttgt` | 🔵 tcontract 1.17× faster than `tblis` |  |
| `abcijk-ikma-mjbc/n1/b1` | 4.56394 ± 0.0188354 (W 0.0107262) | 43.9189 ± 0.294771 (W 0.0838898) | 5.68909 ± 0.0472336 (W 0.0216713) | 🔵 tcontract 9.62× faster than `ttgt` | 🔵 tcontract 1.25× faster than `tblis` |  |
| `abcijk-ikmb-mjac/n1/b1` | 4.30379 ± 0.0165339 (W 0.0101345) | 38.7438 ± 0.164748 (W 0.0714202) | 5.62428 ± 0.0937225 (W 0.0248185) | 🔵 tcontract 9.00× faster than `ttgt` | 🔵 tcontract 1.31× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 4.44264 ± 0.0165225 (W 0.00706413) | 40.0749 ± 0.280592 (W 0.190307) | 5.38513 ± 0.0499849 (W 0.0123526) | 🔵 tcontract 9.02× faster than `ttgt` | 🔵 tcontract 1.21× faster than `tblis` |  |
| `abcijk-jkma-mibc/n1/b1` | 4.55987 ± 0.00856126 (W 0.0116789) | 125.834 ± 28.1562 (W 0.104303) | 5.37659 ± 0.0354148 (W 0.0470334) | 🔵 tcontract 27.60× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmb-miac/n1/b1` | 4.31036 ± 0.0199439 (W 0.0127935) | 99.7314 ± 11.3841 (W 0.136804) | 6.80059 ± 0.146203 (W 0.0430457) | 🔵 tcontract 23.14× faster than `ttgt` | 🔵 tcontract 1.58× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmc-miab/n1/b1` | 4.49208 ± 0.0298765 (W 0.0139691) | 100.746 ± 11.5362 (W 0.096466) | 5.50364 ± 0.050574 (W 0.0228775) | 🔵 tcontract 22.43× faster than `ttgt` | 🔵 tcontract 1.23× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcs-rc-abrs/n1/b1` | 0.48513 ± 0.00400645 (W 0.00212372) | 1.13661 ± 0.0174595 (W 0.0051384) | 1.1645 ± 0.0103381 (W 0.00872867) | 🔵 tcontract 2.34× faster than `ttgt` | 🔵 tcontract 2.40× faster than `tblis` |  |
| `abj-bka-kj/n1/b1` | 2.53105 ± 0.0467367 (W 0.0284736) | 2.70472 ± 0.0413608 (W 0.00998223) | 2.64698 ± 0.0159812 (W 0.0108273) | 🔵 tcontract 1.07× faster than `ttgt` | · |  |
| `abjc-cbka-kj/n1/b1` | 1.55522 ± 0.0158395 (W 0.0163147) | 1.20443 ± 0.00340964 (W 0.0109799) | 1.40419 ± 0.013225 (W 0.00835927) | 🔴 tcontract 1.29× slower than `ttgt` | 🔴 tcontract 1.11× slower than `tblis` |  |
| `abjc-kbac-jk/n1/b1` | 0.540413 ± 0.00628683 (W 0.0047011) | 1.21154 ± 0.032327 (W 0.0066823) | 1.14651 ± 0.00571079 (W 0.00493191) | 🔵 tcontract 2.24× faster than `ttgt` | 🔵 tcontract 2.12× faster than `tblis` |  |
| `abjcd-dkbac-jk/n1/b1` | 4.29669 ± 0.00634456 (W 0.0120698) | 18.3304 ± 0.575248 (W 0.140602) | 8.26162 ± 0.0925372 (W 0.0558489) | 🔵 tcontract 4.27× faster than `ttgt` | 🔵 tcontract 1.92× faster than `tblis` | `!` between-start range over 5% |
| `abrs-qb-aqrs/n1/b1` | 0.476013 ± 0.00274354 (W 0.00222287) | 1.10341 ± 0.0131145 (W 0.0172896) | 1.15007 ± 0.0063622 (W 0.00947219) | 🔵 tcontract 2.32× faster than `ttgt` | 🔵 tcontract 2.42× faster than `tblis` |  |
| `adbjc-cbdka-kj/n1/b1` | 10.5846 ± 0.0738853 (W 0.067563) | 11.8075 ± 0.208632 (W 0.0382844) | 9.73054 ± 0.191709 (W 0.05541) | 🔵 tcontract 1.12× faster than `ttgt` | 🔴 tcontract 1.09× slower than `tblis` |  |
| `ajb-kba-jk/n1/b1` | 1.43436 ± 0.00266689 (W 0.00175929) | 2.37053 ± 0.00293525 (W 0.00414368) | 2.09141 ± 0.0539141 (W 0.0280708) | 🔵 tcontract 1.65× faster than `ttgt` | 🔵 tcontract 1.46× faster than `tblis` |  |
| `ajbc-ckba-jk/n1/b1` | 0.734474 ± 0.0105009 (W 0.00670012) | 3.59538 ± 0.0185102 (W 0.028657) | 1.2143 ± 0.00121808 (W 0.00731242) | 🔵 tcontract 4.90× faster than `ttgt` | 🔵 tcontract 1.65× faster than `tblis` |  |
| `ajbdc-ckbad-jk/n1/b1` | 4.12939 ± 0.0243499 (W 0.0193646) | 23.6333 ± 0.609178 (W 0.0629532) | 7.89235 ± 0.0780502 (W 0.0527556) | 🔵 tcontract 5.72× faster than `ttgt` | 🔵 tcontract 1.91× faster than `tblis` |  |
| `aqrs-pa-pqrs/n1/b1` | 0.508503 ± 0.00298355 (W 0.00274789) | 1.02034 ± 0.00137766 (W 0.00189544) | 1.08819 ± 0.00604067 (W 0.00571302) | 🔵 tcontract 2.01× faster than `ttgt` | 🔵 tcontract 2.14× faster than `tblis` |  |
| `ij-ik-kj/n1/b1` | 3.57144 ± 0.0137697 (W 0.00215452) | 4.60747 ± 0.00697497 (W 0.00712724) | 4.25991 ± 0.0333113 (W 0.0121899) | 🔵 tcontract 1.29× faster than `ttgt` | 🔵 tcontract 1.19× faster than `tblis` |  |
| `ij-ikl-ljk/n1/b1` | 1.23334 ± 0.00889715 (W 0.00330688) | 1.8602 ± 0.00876254 (W 0.0123586) | 2.14697 ± 0.010826 (W 0.00704714) | 🔵 tcontract 1.51× faster than `ttgt` | 🔵 tcontract 1.74× faster than `tblis` |  |
| `ij-kil-lkj/n1/b1` | 1.84058 ± 0.0167665 (W 0.00237902) | 2.86123 ± 0.00646122 (W 0.00485336) | 3.04268 ± 0.011975 (W 0.00714519) | 🔵 tcontract 1.55× faster than `ttgt` | 🔵 tcontract 1.65× faster than `tblis` |  |
| `ijk-ikl-lj/n1/b1` | 1.09287 ± 0.00844877 (W 0.00280027) | 1.63765 ± 0.00208858 (W 0.00263886) | 1.71772 ± 0.00653579 (W 0.00438185) | 🔵 tcontract 1.50× faster than `ttgt` | 🔵 tcontract 1.57× faster than `tblis` |  |
| `ijk-il-jlk/n1/b1` | 1.06479 ± 0.00401303 (W 0.00183562) | 1.9174 ± 0.00449839 (W 0.00571545) | 1.59523 ± 0.0179356 (W 0.00480275) | 🔵 tcontract 1.80× faster than `ttgt` | 🔵 tcontract 1.50× faster than `tblis` |  |
| `ijk-ilk-jl/n1/b1` | 1.01556 ± 0.0040992 (W 0.00138434) | 1.70992 ± 0.0258346 (W 0.0349857) | 1.51634 ± 0.0228392 (W 0.00568817) | 🔵 tcontract 1.68× faster than `ttgt` | 🔵 tcontract 1.49× faster than `tblis` |  |
| `ijk-ilk-lj/n1/b1` | 1.08391 ± 0.00429388 (W 0.00149028) | 1.7391 ± 0.0164796 (W 0.0153687) | 1.7172 ± 0.00763708 (W 0.0026294) | 🔵 tcontract 1.60× faster than `ttgt` | 🔵 tcontract 1.58× faster than `tblis` |  |
| `ijk-ilmk-mjl/n1/b1` | 0.431317 ± 0.000555095 (W 0.00224315) | 0.682129 ± 0.00214011 (W 0.0026804) | 0.962005 ± 0.004563 (W 0.00290621) | 🔵 tcontract 1.58× faster than `ttgt` | 🔵 tcontract 2.23× faster than `tblis` |  |
| `ijkl-imjn-lnkm/n1/b1` | 6.26985 ± 0.0152126 (W 0.012599) | 7.97318 ± 0.0322062 (W 0.0256203) | 7.55898 ± 0.0421889 (W 0.0415573) | 🔵 tcontract 1.27× faster than `ttgt` | 🔵 tcontract 1.21× faster than `tblis` |  |
| `ijkl-imjn-nlmk/n1/b1` | 6.22286 ± 0.0013146 (W 0.00946239) | 7.99992 ± 0.0362388 (W 0.0211993) | 7.51356 ± 0.0812361 (W 0.0240633) | 🔵 tcontract 1.29× faster than `ttgt` | 🔵 tcontract 1.21× faster than `tblis` |  |
| `ijkl-imkn-jnlm/n1/b1` | 6.1975 ± 0.0166003 (W 0.022463) | 7.97077 ± 0.0220155 (W 0.0190264) | 7.29798 ± 0.0298286 (W 0.0171815) | 🔵 tcontract 1.29× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `ijkl-imkn-njml/n1/b1` | 6.20746 ± 0.00595774 (W 0.0121246) | 7.98405 ± 0.0159894 (W 0.0197795) | 7.39032 ± 0.0543838 (W 0.0136452) | 🔵 tcontract 1.29× faster than `ttgt` | 🔵 tcontract 1.19× faster than `tblis` |  |
| `ijkl-imln-jnkm/n1/b1` | 6.18688 ± 0.0183539 (W 0.00922235) | 7.97531 ± 0.0227212 (W 0.0102357) | 7.26262 ± 0.0373013 (W 0.0426058) | 🔵 tcontract 1.29× faster than `ttgt` | 🔵 tcontract 1.17× faster than `tblis` |  |
| `ijkl-imln-njmk/n1/b1` | 6.19638 ± 0.0118238 (W 0.00992915) | 8.02162 ± 0.0264394 (W 0.013954) | 7.29347 ± 0.0686438 (W 0.0074225) | 🔵 tcontract 1.29× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `ijkl-imnj-nlkm/n1/b1` | 6.20997 ± 0.0134199 (W 0.012178) | 7.93762 ± 0.033144 (W 0.022371) | 7.38002 ± 0.0216648 (W 0.0137208) | 🔵 tcontract 1.28× faster than `ttgt` | 🔵 tcontract 1.19× faster than `tblis` |  |
| `ijkl-imnk-njml/n1/b1` | 6.19113 ± 0.0148181 (W 0.00730498) | 7.95256 ± 0.033585 (W 0.00980475) | 7.27576 ± 0.0121874 (W 0.0159956) | 🔵 tcontract 1.28× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` |  |
| `ijkl-minj-nlmk/n1/b1` | 7.64119 ± 0.0357714 (W 0.0304759) | 9.63947 ± 0.0350513 (W 0.0225934) | 9.13439 ± 0.0671795 (W 0.0479139) | 🔵 tcontract 1.26× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `ijkl-mink-jnlm/n1/b1` | 7.49034 ± 0.0105785 (W 0.00863201) | 9.54339 ± 0.0258928 (W 0.0254554) | 8.71213 ± 0.0567251 (W 0.0410062) | 🔵 tcontract 1.27× faster than `ttgt` | 🔵 tcontract 1.16× faster than `tblis` |  |
| `ijkl-minl-njmk/n1/b1` | 7.57887 ± 0.00819415 (W 0.0173314) | 9.63524 ± 0.0475911 (W 0.0226531) | 8.89291 ± 0.0870409 (W 0.0166928) | 🔵 tcontract 1.27× faster than `ttgt` | 🔵 tcontract 1.17× faster than `tblis` |  |

## tcbench, f64, 4T (CPU 4-7)

| case | plan (ms) | ttgt (ms) | tblis (ms) | vs `ttgt` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `abc-bk-akc/n1/b1` | 0.264955 ± 0.0303951 (W 0.0019298) | 1.23599 ± 0.162354 (W 0.0160954) | 0.424453 ± 0.0485824 (W 0.00409726) | 🔵 tcontract 4.66× faster than `ttgt` | 🔵 tcontract 1.60× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-eiab-jkec/n1/b1` | 1.15596 ± 0.0775848 (W 0.00635572) | 5.74703 ± 0.361108 (W 0.0189584) | 1.8654 ± 0.322653 (W 0.0679258) | 🔵 tcontract 4.97× faster than `ttgt` | 🔵 tcontract 1.61× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-eiac-jkeb/n1/b1` | 1.09315 ± 0.0320993 (W 0.00401568) | 6.94581 ± 0.277825 (W 0.041613) | 2.24071 ± 0.436658 (W 0.06506) | 🔵 tcontract 6.35× faster than `ttgt` | 🔵 tcontract 2.05× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-eibc-jkea/n1/b1` | 1.17752 ± 0.0778543 (W 0.00840899) | 8.57783 ± 2.5504 (W 0.0842931) | 1.45401 ± 0.179069 (W 0.0142981) | 🔵 tcontract 7.28× faster than `ttgt` | 🔵 tcontract 1.23× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-ejab-ikec/n1/b1` | 1.1354 ± 0.0794062 (W 0.00696525) | 5.73398 ± 0.459757 (W 0.0179721) | 1.66064 ± 0.328909 (W 0.0490596) | 🔵 tcontract 5.05× faster than `ttgt` | 🔵 tcontract 1.46× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-ejac-ikeb/n1/b1` | 1.08933 ± 0.0316997 (W 0.0042805) | 7.0572 ± 0.692969 (W 0.0339458) | 1.56149 ± 0.246427 (W 0.0117635) | 🔵 tcontract 6.48× faster than `ttgt` | 🔵 tcontract 1.43× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-ejbc-ikea/n1/b1` | 1.17392 ± 0.0773547 (W 0.0155123) | 8.68128 ± 2.5855 (W 0.0560412) | 1.52665 ± 0.235362 (W 0.00868816) | 🔵 tcontract 7.40× faster than `ttgt` | 🔵 tcontract 1.30× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-ekab-ijec/n1/b1` | 1.135 ± 0.0811286 (W 0.00715819) | 6.25178 ± 0.896285 (W 0.0178589) | 1.48594 ± 0.304154 (W 0.0461806) | 🔵 tcontract 5.51× faster than `ttgt` | 🔵 tcontract 1.31× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-ekac-ijeb/n1/b1` | 1.09118 ± 0.0332732 (W 0.00564318) | 7.81167 ± 0.39221 (W 0.0332415) | 2.03797 ± 0.457026 (W 0.0414674) | 🔵 tcontract 7.16× faster than `ttgt` | 🔵 tcontract 1.87× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-ekbc-ijea/n1/b1` | 1.18013 ± 0.0783187 (W 0.0123858) | 9.26432 ± 2.68283 (W 0.0401547) | 1.53418 ± 0.232155 (W 0.00622582) | 🔵 tcontract 7.85× faster than `ttgt` | 🔵 tcontract 1.30× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-ijma-mkbc/n1/b1` | 1.1725 ± 0.0715608 (W 0.00530564) | 35.8229 ± 0.501576 (W 0.0565623) | 1.5454 ± 0.207503 (W 0.0128264) | 🔵 tcontract 30.55× faster than `ttgt` | 🔵 tcontract 1.32× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-ijmb-mkac/n1/b1` | 1.08961 ± 0.0305099 (W 0.00295492) | 33.0303 ± 9.70185 (W 0.12788) | 2.03781 ± 0.433251 (W 0.023309) | 🔵 tcontract 30.31× faster than `ttgt` | 🔵 tcontract 1.87× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-ijmc-mkab/n1/b1` | 1.13738 ± 0.0808544 (W 0.00798795) | 34.0362 ± 7.89412 (W 0.160739) | 1.45038 ± 0.338174 (W 0.0442514) | 🔵 tcontract 29.93× faster than `ttgt` | · | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-ikma-mjbc/n1/b1` | 1.1818 ± 0.0718157 (W 0.0138127) | 40.5235 ± 0.757753 (W 0.054828) | 1.53976 ± 0.235828 (W 0.0126503) | 🔵 tcontract 34.29× faster than `ttgt` | 🔵 tcontract 1.30× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-ikmb-mjac/n1/b1` | 1.09041 ± 0.0283654 (W 0.00585877) | 35.9584 ± 9.05144 (W 0.152262) | 1.55343 ± 0.235651 (W 0.0154779) | 🔵 tcontract 32.98× faster than `ttgt` | 🔵 tcontract 1.42× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-ikmc-mjab/n1/b1` | 1.13476 ± 0.0824049 (W 0.00706246) | 36.8434 ± 9.08582 (W 0.0656972) | 1.67565 ± 0.341763 (W 0.0493003) | 🔵 tcontract 32.47× faster than `ttgt` | 🔵 tcontract 1.48× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkma-mibc/n1/b1` | 1.16902 ± 0.0747959 (W 0.0090529) | 77.9249 ± 29.3512 (W 0.126695) | 1.45504 ± 0.168687 (W 0.0069915) | 🔵 tcontract 66.66× faster than `ttgt` | 🔵 tcontract 1.24× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmb-miac/n1/b1` | 1.09367 ± 0.0386395 (W 0.00279159) | 85.7712 ± 12.328 (W 0.0905815) | 2.29038 ± 0.410302 (W 0.0389433) | 🔵 tcontract 78.43× faster than `ttgt` | 🔵 tcontract 2.09× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-jkmc-miab/n1/b1` | 1.15817 ± 0.0874597 (W 0.00841718) | 84.4743 ± 12.079 (W 0.135305) | 1.77518 ± 0.348294 (W 0.0297893) | 🔵 tcontract 72.94× faster than `ttgt` | 🔵 tcontract 1.53× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcs-rc-abrs/n1/b1` | 0.140292 ± 0.0186924 (W 0.00186388) | 0.809533 ± 0.151821 (W 0.00544852) | 0.381914 ± 0.0393381 (W 0.00949858) | 🔵 tcontract 5.77× faster than `ttgt` | 🔵 tcontract 2.72× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abj-bka-kj/n1/b1` | 0.492019 ± 0.0652721 (W 0.00300164) | 1.43318 ± 0.180728 (W 0.0139106) | 0.711961 ± 0.175114 (W 0.00793232) | 🔵 tcontract 2.91× faster than `ttgt` | 🔵 tcontract 1.45× faster than `tblis` | `!` between-start range over 5% |
| `abjc-cbka-kj/n1/b1` | 0.284592 ± 0.0716841 (W 0.00752011) | 0.797912 ± 0.131284 (W 0.00501113) | 0.466663 ± 0.102105 (W 0.00812936) | 🔵 tcontract 2.80× faster than `ttgt` | 🔵 tcontract 1.64× faster than `tblis` | `!` between-start range over 5% |
| `abjc-kbac-jk/n1/b1` | 0.155721 ± 0.0270104 (W 0.00199289) | 0.858905 ± 0.371134 (W 0.00662526) | 0.381894 ± 0.0657303 (W 0.0056836) | 🔵 tcontract 5.52× faster than `ttgt` | 🔵 tcontract 2.45× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abjcd-dkbac-jk/n1/b1` | 1.46182 ± 0.36635 (W 0.0105644) | 16.2638 ± 1.05131 (W 0.056661) | 2.77745 ± 0.30995 (W 0.0358356) | 🔵 tcontract 11.13× faster than `ttgt` | 🔵 tcontract 1.90× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abrs-qb-aqrs/n1/b1` | 0.135834 ± 0.019488 (W 0.00299142) | 0.753257 ± 0.0766041 (W 0.00412043) | 0.376454 ± 0.0258319 (W 0.00356226) | 🔵 tcontract 5.55× faster than `ttgt` | 🔵 tcontract 2.77× faster than `tblis` | `!` between-start range over 5% |
| `adbjc-cbdka-kj/n1/b1` | 6.42772 ± 0.194829 (W 0.126479) | 10.1676 ± 0.293239 (W 0.0166705) | 3.69195 ± 1.00481 (W 0.0694743) | 🔵 tcontract 1.58× faster than `ttgt` | 🔴 tcontract 1.74× slower than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `ajb-kba-jk/n1/b1` | 0.381413 ± 0.0544474 (W 0.00285206) | 1.26245 ± 0.158037 (W 0.0120038) | 0.571279 ± 0.136138 (W 0.00664615) | 🔵 tcontract 3.31× faster than `ttgt` | 🔵 tcontract 1.50× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `ajbc-ckba-jk/n1/b1` | 0.222315 ± 0.0476043 (W 0.0031695) | 3.28859 ± 0.110924 (W 0.0160057) | 0.412201 ± 0.0929677 (W 0.00412257) | 🔵 tcontract 14.79× faster than `ttgt` | 🔵 tcontract 1.85× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `ajbdc-ckbad-jk/n1/b1` | 1.39601 ± 0.3727 (W 0.0127792) | 22.695 ± 1.18363 (W 0.0595247) | 2.73248 ± 0.14873 (W 0.0150812) | 🔵 tcontract 16.26× faster than `ttgt` | 🔵 tcontract 1.96× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `aqrs-pa-pqrs/n1/b1` | 0.282498 ± 0.0141639 (W 0.0021679) | 0.662347 ± 0.0464462 (W 0.00275171) | 0.355645 ± 0.0143538 (W 0.0073983) | 🔵 tcontract 2.34× faster than `ttgt` | 🔵 tcontract 1.26× faster than `tblis` | `!` between-start range over 5% |
| `ij-ik-kj/n1/b1` | 1.0167 ± 0.0382537 (W 0.00561503) | 1.51168 ± 0.0777061 (W 0.00876012) | 1.21834 ± 0.0829938 (W 0.00336612) | 🔵 tcontract 1.49× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` | `!` between-start range over 5% |
| `ij-ikl-ljk/n1/b1` | 0.514722 ± 0.0662594 (W 0.00294158) | 0.968922 ± 0.0881977 (W 0.0113156) | 0.8779 ± 0.0754928 (W 0.00363422) | 🔵 tcontract 1.88× faster than `ttgt` | 🔵 tcontract 1.71× faster than `tblis` | `!` between-start range over 5% |
| `ij-kil-lkj/n1/b1` | 0.752195 ± 0.111643 (W 0.00417149) | 1.62201 ± 0.0646816 (W 0.00740513) | 1.21996 ± 0.0928499 (W 0.0076301) | 🔵 tcontract 2.16× faster than `ttgt` | 🔵 tcontract 1.62× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `ijk-ikl-lj/n1/b1` | 0.287477 ± 0.0458656 (W 0.00192759) | 0.820334 ± 0.0991195 (W 0.00415116) | 0.474026 ± 0.0717767 (W 0.00586074) | 🔵 tcontract 2.85× faster than `ttgt` | 🔵 tcontract 1.65× faster than `tblis` | `!` between-start range over 5% |
| `ijk-il-jlk/n1/b1` | 0.275675 ± 0.0309193 (W 0.00180929) | 1.19313 ± 0.0606129 (W 0.0153003) | 0.440723 ± 0.0204352 (W 0.00415743) | 🔵 tcontract 4.33× faster than `ttgt` | 🔵 tcontract 1.60× faster than `tblis` | `!` between-start range over 5% |
| `ijk-ilk-jl/n1/b1` | 0.2676 ± 0.0235636 (W 0.00449337) | 0.862803 ± 0.160135 (W 0.00427836) | 0.423352 ± 0.0580976 (W 0.00563088) | 🔵 tcontract 3.22× faster than `ttgt` | 🔵 tcontract 1.58× faster than `tblis` | `!` between-start range over 5% |
| `ijk-ilk-lj/n1/b1` | 0.284641 ± 0.0292406 (W 0.00224551) | 0.880216 ± 0.202813 (W 0.0055502) | 0.474778 ± 0.050539 (W 0.0035058) | 🔵 tcontract 3.09× faster than `ttgt` | 🔵 tcontract 1.67× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `ijk-ilmk-mjl/n1/b1` | 0.120966 ± 0.00988829 (W 0.00181603) | 0.407271 ± 0.0541097 (W 0.0022584) | 0.286836 ± 0.0273945 (W 0.00367961) | 🔵 tcontract 3.37× faster than `ttgt` | 🔵 tcontract 2.37× faster than `tblis` | `!` between-start range over 5% |
| `ijkl-imjn-lnkm/n1/b1` | 1.60659 ± 0.104653 (W 0.00680037) | 2.67279 ± 0.134816 (W 0.00523066) | 2.1476 ± 0.139947 (W 0.00757036) | 🔵 tcontract 1.66× faster than `ttgt` | 🔵 tcontract 1.34× faster than `tblis` | `!` between-start range over 5% |
| `ijkl-imjn-nlmk/n1/b1` | 1.59174 ± 0.103295 (W 0.00450595) | 2.71156 ± 0.171454 (W 0.00739429) | 2.07807 ± 0.201395 (W 0.00651454) | 🔵 tcontract 1.70× faster than `ttgt` | 🔵 tcontract 1.31× faster than `tblis` | `!` between-start range over 5% |
| `ijkl-imkn-jnlm/n1/b1` | 1.58753 ± 0.113915 (W 0.0175534) | 2.67258 ± 0.137946 (W 0.00585762) | 2.007 ± 0.144845 (W 0.0112615) | 🔵 tcontract 1.68× faster than `ttgt` | 🔵 tcontract 1.26× faster than `tblis` | `!` between-start range over 5% |
| `ijkl-imkn-njml/n1/b1` | 1.57781 ± 0.104305 (W 0.0015059) | 2.71699 ± 0.152288 (W 0.00598132) | 2.03957 ± 0.184835 (W 0.00249537) | 🔵 tcontract 1.72× faster than `ttgt` | 🔵 tcontract 1.29× faster than `tblis` | `!` between-start range over 5% |
| `ijkl-imln-jnkm/n1/b1` | 1.58353 ± 0.110179 (W 0.00434851) | 2.68452 ± 0.120915 (W 0.0103867) | 2.02265 ± 0.161861 (W 0.00515317) | 🔵 tcontract 1.70× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` | `!` between-start range over 5% |
| `ijkl-imln-njmk/n1/b1` | 1.58316 ± 0.102429 (W 0.0122159) | 2.70308 ± 0.157846 (W 0.00881333) | 2.01766 ± 0.183482 (W 0.0024564) | 🔵 tcontract 1.71× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` | `!` between-start range over 5% |
| `ijkl-imnj-nlkm/n1/b1` | 1.58729 ± 0.105335 (W 0.00434491) | 2.63994 ± 0.123523 (W 0.00480783) | 2.03035 ± 0.174165 (W 0.0054605) | 🔵 tcontract 1.66× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` | `!` between-start range over 5% |
| `ijkl-imnk-njml/n1/b1` | 1.57999 ± 0.102862 (W 0.00228307) | 2.67286 ± 0.128551 (W 0.00561332) | 2.02751 ± 0.168534 (W 0.00501285) | 🔵 tcontract 1.69× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` | `!` between-start range over 5% |
| `ijkl-minj-nlmk/n1/b1` | 1.95022 ± 0.159617 (W 0.0141628) | 3.30508 ± 0.118898 (W 0.0191887) | 2.50469 ± 0.271242 (W 0.0103959) | 🔵 tcontract 1.69× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` | `!` between-start range over 5% |
| `ijkl-mink-jnlm/n1/b1` | 1.91231 ± 0.111941 (W 0.0025642) | 3.16628 ± 0.133991 (W 0.0135609) | 2.39874 ± 0.194798 (W 0.0164132) | 🔵 tcontract 1.66× faster than `ttgt` | 🔵 tcontract 1.25× faster than `tblis` | `!` between-start range over 5% |
| `ijkl-minl-njmk/n1/b1` | 1.93431 ± 0.143952 (W 0.00261427) | 3.29308 ± 0.111461 (W 0.00907603) | 2.42255 ± 0.253393 (W 0.00582754) | 🔵 tcontract 1.70× faster than `ttgt` | 🔵 tcontract 1.25× faster than `tblis` | `!` between-start range over 5% |

## tcbench, c64, 1T (CPU 4)

| case | plan (ms) | ttgt (ms) | tblis (ms) | vs `ttgt` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `abc-bk-akc/n1/b1` | 4.0999 ± 0.023524 (W 0.00569292) | 6.37429 ± 0.0364427 (W 0.0205782) | 4.94296 ± 0.0511743 (W 0.0264599) | 🔵 tcontract 1.55× faster than `ttgt` | 🔵 tcontract 1.21× faster than `tblis` |  |
| `abcijk-eiab-jkec/n1/b1` | 17.6429 ± 0.0614491 (W 0.0386572) | 41.8582 ± 0.259742 (W 0.0744654) | 19.2212 ± 0.153114 (W 0.116981) | 🔵 tcontract 2.37× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `abcijk-eiac-jkeb/n1/b1` | 17.2928 ± 0.026324 (W 0.0323368) | 42.6856 ± 0.0911614 (W 0.0827091) | 20.7521 ± 0.0962235 (W 0.114801) | 🔵 tcontract 2.47× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `abcijk-eibc-jkea/n1/b1` | 17.6799 ± 0.00336454 (W 0.0330737) | 45.8494 ± 0.216666 (W 0.138223) | 19.0843 ± 0.259908 (W 0.0677945) | 🔵 tcontract 2.59× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `abcijk-ejab-ikec/n1/b1` | 17.5773 ± 0.0592497 (W 0.0342037) | 41.7996 ± 0.0716649 (W 0.0867647) | 19.0758 ± 0.128844 (W 0.0733654) | 🔵 tcontract 2.38× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `abcijk-ejac-ikeb/n1/b1` | 17.2843 ± 0.0634321 (W 0.0282965) | 43.1669 ± 0.287119 (W 0.0706543) | 19.4983 ± 0.0553981 (W 0.0509667) | 🔵 tcontract 2.50× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ejbc-ikea/n1/b1` | 17.7045 ± 0.00656891 (W 0.0358871) | 46.2139 ± 0.214304 (W 0.191602) | 20.0588 ± 0.153091 (W 0.064911) | 🔵 tcontract 2.61× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ekab-ijec/n1/b1` | 17.5629 ± 0.0647131 (W 0.034607) | 41.5158 ± 0.1219 (W 0.24992) | 18.8453 ± 0.101171 (W 0.0539621) | 🔵 tcontract 2.36× faster than `ttgt` | 🔵 tcontract 1.07× faster than `tblis` |  |
| `abcijk-ekac-ijeb/n1/b1` | 17.2995 ± 0.0582279 (W 0.0301986) | 43.6461 ± 0.152553 (W 0.117368) | 19.9478 ± 0.151575 (W 0.0736073) | 🔵 tcontract 2.52× faster than `ttgt` | 🔵 tcontract 1.15× faster than `tblis` |  |
| `abcijk-ekbc-ijea/n1/b1` | 17.7159 ± 0.021422 (W 0.0362893) | 47.574 ± 0.318339 (W 0.0944768) | 20.0752 ± 0.190996 (W 0.0874191) | 🔵 tcontract 2.69× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ijma-mkbc/n1/b1` | 17.7067 ± 0.0450192 (W 0.03681) | 66.7283 ± 0.29232 (W 0.154728) | 20.003 ± 0.197694 (W 0.0631651) | 🔵 tcontract 3.77× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ijmb-mkac/n1/b1` | 17.2765 ± 0.0493405 (W 0.0170107) | 67.55 ± 0.264385 (W 0.104841) | 19.9039 ± 0.125723 (W 0.063423) | 🔵 tcontract 3.91× faster than `ttgt` | 🔵 tcontract 1.15× faster than `tblis` |  |
| `abcijk-ijmc-mkab/n1/b1` | 17.5768 ± 0.0583351 (W 0.0163324) | 79.434 ± 0.354805 (W 0.228713) | 18.8297 ± 0.12853 (W 0.124457) | 🔵 tcontract 4.52× faster than `ttgt` | 🔵 tcontract 1.07× faster than `tblis` |  |
| `abcijk-ikma-mjbc/n1/b1` | 17.6912 ± 0.012033 (W 0.0339811) | 70.5686 ± 1.50135 (W 0.0913962) | 20.095 ± 0.161793 (W 0.0575766) | 🔵 tcontract 3.99× faster than `ttgt` | 🔵 tcontract 1.14× faster than `tblis` |  |
| `abcijk-ikmb-mjac/n1/b1` | 17.2882 ± 0.0450101 (W 0.0360693) | 69.7838 ± 0.638515 (W 0.0967746) | 19.4622 ± 0.266743 (W 0.0484367) | 🔵 tcontract 4.04× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `abcijk-ikmc-mjab/n1/b1` | 17.5797 ± 0.0502014 (W 0.0305005) | 80.1656 ± 0.455568 (W 0.156982) | 19.1406 ± 0.100495 (W 0.0653685) | 🔵 tcontract 4.56× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `abcijk-jkma-mibc/n1/b1` | 17.7518 ± 0.0523106 (W 0.0377374) | 110.618 ± 1.66238 (W 0.326374) | 19.0619 ± 0.247279 (W 0.0518785) | 🔵 tcontract 6.23× faster than `ttgt` | 🔵 tcontract 1.07× faster than `tblis` |  |
| `abcijk-jkmb-miac/n1/b1` | 17.2916 ± 0.0192676 (W 0.0372502) | 111.969 ± 1.79731 (W 0.304466) | 20.7605 ± 0.116076 (W 0.0796275) | 🔵 tcontract 6.48× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` |  |
| `abcijk-jkmc-miab/n1/b1` | 17.6408 ± 0.0619612 (W 0.0402662) | 114.561 ± 1.00082 (W 0.206771) | 19.1468 ± 0.164052 (W 0.0729593) | 🔵 tcontract 6.49× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `abcs-rc-abrs/n1/b1` | 1.87027 ± 0.0200218 (W 0.00643385) | 2.98899 ± 0.053765 (W 0.0096814) | 2.36766 ± 0.00771663 (W 0.00824085) | 🔵 tcontract 1.60× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `abj-bka-kj/n1/b1` | 7.53598 ± 0.0649598 (W 0.0478295) | 8.38747 ± 0.034772 (W 0.012778) | 8.45413 ± 0.0878443 (W 0.0895518) | 🔵 tcontract 1.11× faster than `ttgt` | 🔵 tcontract 1.12× faster than `tblis` |  |
| `abjc-cbka-kj/n1/b1` | 3.59097 ± 0.102191 (W 0.0194417) | 3.67009 ± 0.0140216 (W 0.00849408) | 3.03725 ± 0.038905 (W 0.0441213) | · | 🔴 tcontract 1.18× slower than `tblis` | `!` between-start range over 5% |
| `abjc-kbac-jk/n1/b1` | 1.98225 ± 0.00487564 (W 0.00235127) | 3.66078 ± 0.0328809 (W 0.0190827) | 2.63831 ± 0.0188565 (W 0.00971529) | 🔵 tcontract 1.85× faster than `ttgt` | 🔵 tcontract 1.33× faster than `tblis` |  |
| `abjcd-dkbac-jk/n1/b1` | 12.8886 ± 0.0716662 (W 0.0644435) | 29.1229 ± 0.949991 (W 0.120022) | 17.2913 ± 0.205755 (W 0.128346) | 🔵 tcontract 2.26× faster than `ttgt` | 🔵 tcontract 1.34× faster than `tblis` | `!` between-start range over 5% |
| `abrs-qb-aqrs/n1/b1` | 1.60538 ± 0.00394721 (W 0.0024655) | 2.95254 ± 0.0314357 (W 0.0366354) | 2.46803 ± 0.0445121 (W 0.00857309) | 🔵 tcontract 1.84× faster than `ttgt` | 🔵 tcontract 1.54× faster than `tblis` |  |
| `adbjc-cbdka-kj/n1/b1` | 20.2661 ± 0.181001 (W 0.0783462) | 22.9385 ± 0.13835 (W 0.0568971) | 19.4279 ± 0.612021 (W 0.356923) | 🔵 tcontract 1.13× faster than `ttgt` | · | `!` between-start range over 5% |
| `ajb-kba-jk/n1/b1` | 5.73931 ± 0.0360876 (W 0.0171137) | 8.02601 ± 0.0795884 (W 0.0433033) | 7.30461 ± 0.0519444 (W 0.0946649) | 🔵 tcontract 1.40× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `ajbc-ckba-jk/n1/b1` | 2.3253 ± 0.0487741 (W 0.0212257) | 5.66498 ± 0.0241709 (W 0.0114639) | 2.98067 ± 0.105951 (W 0.0590873) | 🔵 tcontract 2.44× faster than `ttgt` | 🔵 tcontract 1.28× faster than `tblis` | `!` between-start range over 5% |
| `ajbdc-ckbad-jk/n1/b1` | 12.5768 ± 0.0432321 (W 0.129993) | 34.257 ± 0.457645 (W 0.0908022) | 17.3096 ± 0.255141 (W 0.205964) | 🔵 tcontract 2.72× faster than `ttgt` | 🔵 tcontract 1.38× faster than `tblis` |  |
| `aqrs-pa-pqrs/n1/b1` | 2.06399 ± 0.00321612 (W 0.00378877) | 2.59379 ± 0.0506432 (W 0.00479052) | 2.33471 ± 0.0125058 (W 0.00589012) | 🔵 tcontract 1.26× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` |  |
| `ij-ik-kj/n1/b1` | 14.6109 ± 0.0315612 (W 0.019784) | 17.7686 ± 0.00573336 (W 0.0511994) | 15.4315 ± 0.0907385 (W 0.0265173) | 🔵 tcontract 1.22× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` |  |
| `ij-ikl-ljk/n1/b1` | 4.88515 ± 0.0182685 (W 0.00739725) | 5.80328 ± 0.00465133 (W 0.0282851) | 5.67056 ± 0.0390022 (W 0.0296089) | 🔵 tcontract 1.19× faster than `ttgt` | 🔵 tcontract 1.16× faster than `tblis` |  |
| `ij-kil-lkj/n1/b1` | 7.44824 ± 0.0285971 (W 0.0242173) | 8.68411 ± 0.00698505 (W 0.0179096) | 8.37022 ± 0.0253872 (W 0.0818839) | 🔵 tcontract 1.17× faster than `ttgt` | 🔵 tcontract 1.12× faster than `tblis` |  |
| `ijk-ikl-lj/n1/b1` | 4.23358 ± 0.0261154 (W 0.00878656) | 5.53164 ± 0.906125 (W 0.0250611) | 5.72415 ± 0.133898 (W 0.03769) | 🔵 tcontract 1.31× faster than `ttgt` | 🔵 tcontract 1.35× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `ijk-il-jlk/n1/b1` | 4.55491 ± 0.017375 (W 0.00620597) | 6.37331 ± 0.0287323 (W 0.0180756) | 4.7964 ± 0.034658 (W 0.00926529) | 🔵 tcontract 1.40× faster than `ttgt` | 🔵 tcontract 1.05× faster than `tblis` |  |
| `ijk-ilk-jl/n1/b1` | 4.09468 ± 0.0165048 (W 0.013084) | 6.0196 ± 0.0184031 (W 0.0127932) | 5.01134 ± 0.0921117 (W 0.0265723) | 🔵 tcontract 1.47× faster than `ttgt` | 🔵 tcontract 1.22× faster than `tblis` |  |
| `ijk-ilk-lj/n1/b1` | 4.24778 ± 0.0300879 (W 0.0103427) | 6.01714 ± 0.0293405 (W 0.00911093) | 5.52047 ± 0.150671 (W 0.0238711) | 🔵 tcontract 1.42× faster than `ttgt` | 🔵 tcontract 1.30× faster than `tblis` | `!` between-start range over 5% |
| `ijk-ilmk-mjl/n1/b1` | 1.64411 ± 0.00835998 (W 0.00458749) | 2.04746 ± 0.0108774 (W 0.0115764) | 2.0878 ± 0.0544125 (W 0.00638455) | 🔵 tcontract 1.25× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` |  |
| `ijkl-imjn-lnkm/n1/b1` | 25.1486 ± 0.10497 (W 0.0556852) | 30.8445 ± 0.100073 (W 0.0513117) | 26.6671 ± 0.157584 (W 0.054508) | 🔵 tcontract 1.23× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` |  |
| `ijkl-imjn-nlmk/n1/b1` | 25.095 ± 0.0229139 (W 0.0343079) | 30.7932 ± 0.0472475 (W 0.0345557) | 27.5171 ± 0.217096 (W 0.0746343) | 🔵 tcontract 1.23× faster than `ttgt` | 🔵 tcontract 1.10× faster than `tblis` |  |
| `ijkl-imkn-jnlm/n1/b1` | 25.1054 ± 0.115866 (W 0.0375878) | 30.9089 ± 0.0598922 (W 0.0508801) | 26.7101 ± 0.188233 (W 0.0550082) | 🔵 tcontract 1.23× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` |  |
| `ijkl-imkn-njml/n1/b1` | 25.119 ± 0.0380568 (W 0.0217354) | 30.7689 ± 0.0853868 (W 0.0369902) | 27.4275 ± 0.104435 (W 0.0550364) | 🔵 tcontract 1.22× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` |  |
| `ijkl-imln-jnkm/n1/b1` | 24.9927 ± 0.0340988 (W 0.052173) | 30.8924 ± 0.0729891 (W 0.0634906) | 26.735 ± 0.0518088 (W 0.041247) | 🔵 tcontract 1.24× faster than `ttgt` | 🔵 tcontract 1.07× faster than `tblis` |  |
| `ijkl-imln-njmk/n1/b1` | 25.0756 ± 0.0845901 (W 0.039594) | 30.8401 ± 0.270404 (W 0.0712222) | 26.9316 ± 0.164385 (W 0.0526258) | 🔵 tcontract 1.23× faster than `ttgt` | 🔵 tcontract 1.07× faster than `tblis` |  |
| `ijkl-imnj-nlkm/n1/b1` | 25.0106 ± 0.0473592 (W 0.0391908) | 30.5581 ± 0.10906 (W 0.0517581) | 26.9182 ± 0.32544 (W 0.0389385) | 🔵 tcontract 1.22× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `ijkl-imnk-njml/n1/b1` | 25.0969 ± 0.12026 (W 0.0127438) | 30.5541 ± 0.10394 (W 0.0514495) | 26.9625 ± 0.126112 (W 0.0788102) | 🔵 tcontract 1.22× faster than `ttgt` | 🔵 tcontract 1.07× faster than `tblis` |  |
| `ijkl-minj-nlmk/n1/b1` | 30.691 ± 0.135809 (W 0.0398004) | 36.7711 ± 0.0804639 (W 0.0379409) | 33.1921 ± 0.280036 (W 0.0779885) | 🔵 tcontract 1.20× faster than `ttgt` | 🔵 tcontract 1.08× faster than `tblis` |  |
| `ijkl-mink-jnlm/n1/b1` | 30.1233 ± 0.122375 (W 0.0411438) | 36.8037 ± 0.151444 (W 0.0254017) | 31.7077 ± 0.381953 (W 0.0537281) | 🔵 tcontract 1.22× faster than `ttgt` | 🔵 tcontract 1.05× faster than `tblis` |  |
| `ijkl-minl-njmk/n1/b1` | 30.7306 ± 0.100117 (W 0.0385507) | 36.7485 ± 0.132575 (W 0.0626639) | 32.7091 ± 0.248995 (W 0.049779) | 🔵 tcontract 1.20× faster than `ttgt` | 🔵 tcontract 1.06× faster than `tblis` |  |

## tcbench, c64, 4T (CPU 4-7)

| case | plan (ms) | ttgt (ms) | tblis (ms) | vs `ttgt` | vs `tblis` | notes |
|---|---|---|---|---|---|---|
| `abc-bk-akc/n1/b1` | 1.04207 ± 0.0523416 (W 0.00844633) | 2.72374 ± 0.0897455 (W 0.0453254) | 1.28377 ± 0.182509 (W 0.00959127) | 🔵 tcontract 2.61× faster than `ttgt` | 🔵 tcontract 1.23× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-eiab-jkec/n1/b1` | 4.49409 ± 0.108457 (W 0.00871855) | 27.452 ± 1.59025 (W 0.101725) | 5.06958 ± 0.414367 (W 0.0483397) | 🔵 tcontract 6.11× faster than `ttgt` | 🔵 tcontract 1.13× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-eiac-jkeb/n1/b1` | 4.3568 ± 0.121832 (W 0.00908765) | 28.2168 ± 1.73942 (W 0.0714473) | 5.52734 ± 0.642628 (W 0.0455107) | 🔵 tcontract 6.48× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-eibc-jkea/n1/b1` | 4.5066 ± 0.124172 (W 0.0146433) | 31.1294 ± 2.33047 (W 0.104923) | 4.98365 ± 0.354003 (W 0.0198318) | 🔵 tcontract 6.91× faster than `ttgt` | 🔵 tcontract 1.11× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ejab-ikec/n1/b1` | 4.43834 ± 0.121198 (W 0.00933945) | 27.3736 ± 2.3125 (W 0.0736568) | 5.12127 ± 0.267049 (W 0.0467536) | 🔵 tcontract 6.17× faster than `ttgt` | 🔵 tcontract 1.15× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ejac-ikeb/n1/b1` | 4.34986 ± 0.103648 (W 0.00885257) | 28.5191 ± 2.59061 (W 0.068897) | 5.13698 ± 0.41231 (W 0.016302) | 🔵 tcontract 6.56× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ejbc-ikea/n1/b1` | 4.46373 ± 0.142075 (W 0.0112931) | 31.5326 ± 2.8078 (W 0.0629577) | 5.21932 ± 0.421307 (W 0.0251231) | 🔵 tcontract 7.06× faster than `ttgt` | 🔵 tcontract 1.17× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ekab-ijec/n1/b1` | 4.4436 ± 0.116469 (W 0.0072256) | 27.7447 ± 1.6064 (W 0.0647531) | 4.94059 ± 0.364903 (W 0.0244451) | 🔵 tcontract 6.24× faster than `ttgt` | 🔵 tcontract 1.11× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ekac-ijeb/n1/b1` | 4.34032 ± 0.116663 (W 0.0066313) | 29.3686 ± 1.92225 (W 0.0697503) | 5.29109 ± 0.399862 (W 0.019539) | 🔵 tcontract 6.77× faster than `ttgt` | 🔵 tcontract 1.22× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ekbc-ijea/n1/b1` | 4.46431 ± 0.136566 (W 0.0173006) | 33.0183 ± 2.14346 (W 0.104324) | 5.22449 ± 0.42715 (W 0.0210083) | 🔵 tcontract 7.40× faster than `ttgt` | 🔵 tcontract 1.17× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ijma-mkbc/n1/b1` | 4.51791 ± 0.113699 (W 0.01563) | 53.1679 ± 1.67029 (W 0.0484113) | 5.23306 ± 0.426145 (W 0.0161324) | 🔵 tcontract 11.77× faster than `ttgt` | 🔵 tcontract 1.16× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ijmb-mkac/n1/b1` | 4.38469 ± 0.0698837 (W 0.00916964) | 54.9896 ± 5.62393 (W 0.421238) | 5.26185 ± 0.387803 (W 0.0183707) | 🔵 tcontract 12.54× faster than `ttgt` | 🔵 tcontract 1.20× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abcijk-ijmc-mkab/n1/b1` | 4.42348 ± 0.116568 (W 0.0167574) | 64.9654 ± 3.47758 (W 0.110098) | 4.97028 ± 0.321596 (W 0.0351794) | 🔵 tcontract 14.69× faster than `ttgt` | 🔵 tcontract 1.12× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ikma-mjbc/n1/b1` | 4.46245 ± 0.123451 (W 0.014818) | 57.0617 ± 1.51348 (W 0.135709) | 5.22929 ± 0.415185 (W 0.017766) | 🔵 tcontract 12.79× faster than `ttgt` | 🔵 tcontract 1.17× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ikmb-mjac/n1/b1` | 4.36467 ± 0.0903458 (W 0.00591837) | 56.135 ± 5.2674 (W 0.313561) | 5.16411 ± 0.400609 (W 0.0262314) | 🔵 tcontract 12.86× faster than `ttgt` | 🔵 tcontract 1.18× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-ikmc-mjab/n1/b1` | 4.42178 ± 0.114535 (W 0.00546476) | 65.8917 ± 6.25309 (W 0.105717) | 5.12073 ± 0.263614 (W 0.0424041) | 🔵 tcontract 14.90× faster than `ttgt` | 🔵 tcontract 1.16× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-jkma-mibc/n1/b1` | 4.50806 ± 0.12443 (W 0.0165457) | 98.1365 ± 1.31364 (W 0.251567) | 4.95832 ± 0.319083 (W 0.0197002) | 🔵 tcontract 21.77× faster than `ttgt` | 🔵 tcontract 1.10× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-jkmb-miac/n1/b1` | 4.3801 ± 0.0973143 (W 0.0142976) | 98.22 ± 4.2358 (W 0.153221) | 5.54238 ± 0.63893 (W 0.0211446) | 🔵 tcontract 22.42× faster than `ttgt` | 🔵 tcontract 1.27× faster than `tblis` | `!` between-start range over 5% |
| `abcijk-jkmc-miab/n1/b1` | 4.483 ± 0.123666 (W 0.0142511) | 100.357 ± 2.89335 (W 0.129557) | 5.14748 ± 0.466339 (W 0.116002) | 🔵 tcontract 22.39× faster than `ttgt` | 🔵 tcontract 1.15× faster than `tblis` | `!` between-start range over 5% |
| `abcs-rc-abrs/n1/b1` | 0.47569 ± 0.0511135 (W 0.00435927) | 1.63196 ± 0.0641443 (W 0.0103786) | 0.724615 ± 0.146697 (W 0.00965696) | 🔵 tcontract 3.43× faster than `ttgt` | 🔵 tcontract 1.52× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `abj-bka-kj/n1/b1` | 1.65265 ± 0.165256 (W 0.00728366) | 3.69226 ± 0.132224 (W 0.0147585) | 2.32335 ± 0.252812 (W 0.0151348) | 🔵 tcontract 2.23× faster than `ttgt` | 🔵 tcontract 1.41× faster than `tblis` | `!` between-start range over 5% |
| `abjc-cbka-kj/n1/b1` | 0.832215 ± 0.264565 (W 0.00727641) | 2.10579 ± 0.0963262 (W 0.0135465) | 0.913448 ± 0.23521 (W 0.0213955) | 🔵 tcontract 2.53× faster than `ttgt` | · | `!` between-start range over 5%; `p` position effect over 5% |
| `abjc-kbac-jk/n1/b1` | 0.512839 ± 0.0953054 (W 0.00272591) | 2.21985 ± 0.407486 (W 0.0370517) | 0.763426 ± 0.174995 (W 0.0140318) | 🔵 tcontract 4.33× faster than `ttgt` | 🔵 tcontract 1.49× faster than `tblis` | `!` between-start range over 5% |
| `abjcd-dkbac-jk/n1/b1` | 3.85215 ± 0.18935 (W 0.036628) | 22.0504 ± 1.58602 (W 0.0581332) | 5.27906 ± 0.556095 (W 0.0362792) | 🔵 tcontract 5.72× faster than `ttgt` | 🔵 tcontract 1.37× faster than `tblis` | `!` between-start range over 5% |
| `abrs-qb-aqrs/n1/b1` | 0.417159 ± 0.0357542 (W 0.00447516) | 1.56084 ± 0.210423 (W 0.0211046) | 0.731197 ± 0.107177 (W 0.0153509) | 🔵 tcontract 3.74× faster than `ttgt` | 🔵 tcontract 1.75× faster than `tblis` | `!` between-start range over 5% |
| `adbjc-cbdka-kj/n1/b1` | 8.11191 ± 0.375798 (W 0.0994431) | 16.0014 ± 0.401728 (W 0.140218) | 7.44361 ± 0.798123 (W 0.130513) | 🔵 tcontract 1.97× faster than `ttgt` | · | `!` between-start range over 5% |
| `ajb-kba-jk/n1/b1` | 1.45282 ± 0.0896712 (W 0.00510891) | 3.5698 ± 0.283663 (W 0.0119954) | 1.87166 ± 0.223713 (W 0.0203586) | 🔵 tcontract 2.46× faster than `ttgt` | 🔵 tcontract 1.29× faster than `tblis` | `!` between-start range over 5% |
| `ajbc-ckba-jk/n1/b1` | 0.61035 ± 0.118151 (W 0.00943151) | 4.22564 ± 0.27564 (W 0.0128468) | 0.922584 ± 0.0918436 (W 0.0151936) | 🔵 tcontract 6.92× faster than `ttgt` | 🔵 tcontract 1.51× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `ajbdc-ckbad-jk/n1/b1` | 3.71181 ± 0.219736 (W 0.0338454) | 27.4325 ± 1.77248 (W 0.122754) | 5.15406 ± 0.328055 (W 0.0442498) | 🔵 tcontract 7.39× faster than `ttgt` | 🔵 tcontract 1.39× faster than `tblis` | `!` between-start range over 5% |
| `aqrs-pa-pqrs/n1/b1` | 0.627353 ± 0.0386655 (W 0.00401048) | 1.24183 ± 0.0688047 (W 0.00551353) | 0.668048 ± 0.0448363 (W 0.00941335) | 🔵 tcontract 1.98× faster than `ttgt` | · | `!` between-start range over 5% |
| `ij-ik-kj/n1/b1` | 3.72161 ± 0.139566 (W 0.00657943) | 5.05168 ± 0.134247 (W 0.0137581) | 4.04946 ± 0.219626 (W 0.00992917) | 🔵 tcontract 1.36× faster than `ttgt` | 🔵 tcontract 1.09× faster than `tblis` | `!` between-start range over 5% |
| `ij-ikl-ljk/n1/b1` | 2.06677 ± 0.0976856 (W 0.0120374) | 2.33037 ± 0.0354627 (W 0.0225659) | 1.6858 ± 0.168329 (W 0.00945054) | 🔵 tcontract 1.13× faster than `ttgt` | 🔴 tcontract 1.23× slower than `tblis` | `!` between-start range over 5% |
| `ij-kil-lkj/n1/b1` | 3.11504 ± 0.0947318 (W 0.008856) | 3.66621 ± 0.0885758 (W 0.0255493) | 2.43143 ± 0.221496 (W 0.0204736) | 🔵 tcontract 1.18× faster than `ttgt` | 🔴 tcontract 1.28× slower than `tblis` | `!` between-start range over 5% |
| `ijk-ikl-lj/n1/b1` | 1.0733 ± 0.072435 (W 0.00370708) | 2.30219 ± 0.0788268 (W 0.0126632) | 1.50758 ± 0.140175 (W 0.00827265) | 🔵 tcontract 2.14× faster than `ttgt` | 🔵 tcontract 1.40× faster than `tblis` | `!` between-start range over 5% |
| `ijk-il-jlk/n1/b1` | 1.85255 ± 0.0628791 (W 0.0128097) | 2.7193 ± 0.0805127 (W 0.0108045) | 1.23186 ± 0.0907197 (W 0.00451269) | 🔵 tcontract 1.47× faster than `ttgt` | 🔴 tcontract 1.50× slower than `tblis` | `!` between-start range over 5% |
| `ijk-ilk-jl/n1/b1` | 1.04216 ± 0.0618276 (W 0.00290223) | 2.72049 ± 0.0760714 (W 0.0114019) | 1.2719 ± 0.176848 (W 0.00498346) | 🔵 tcontract 2.61× faster than `ttgt` | 🔵 tcontract 1.22× faster than `tblis` | `!` between-start range over 5%; `p` position effect over 5% |
| `ijk-ilk-lj/n1/b1` | 1.07096 ± 0.0767055 (W 0.00329554) | 2.69185 ± 0.065686 (W 0.00766232) | 1.44224 ± 0.163023 (W 0.0127239) | 🔵 tcontract 2.51× faster than `ttgt` | 🔵 tcontract 1.35× faster than `tblis` | `!` between-start range over 5% |
| `ijk-ilmk-mjl/n1/b1` | 0.46055 ± 0.0747366 (W 0.0053669) | 0.864086 ± 0.0740343 (W 0.00431918) | 0.553596 ± 0.134766 (W 0.00500434) | 🔵 tcontract 1.88× faster than `ttgt` | · | `!` between-start range over 5%; `p` position effect over 5% |
| `ijkl-imjn-lnkm/n1/b1` | 6.86005 ± 0.202479 (W 0.010368) | 9.13799 ± 0.135707 (W 0.0279845) | 7.14837 ± 0.350027 (W 0.012124) | 🔵 tcontract 1.33× faster than `ttgt` | · | `!` between-start range over 5% |
| `ijkl-imjn-nlmk/n1/b1` | 6.79521 ± 0.257122 (W 0.00884434) | 8.97425 ± 0.123965 (W 0.0126269) | 7.20723 ± 0.422169 (W 0.0238482) | 🔵 tcontract 1.32× faster than `ttgt` | · | `!` between-start range over 5% |
| `ijkl-imkn-jnlm/n1/b1` | 6.78711 ± 0.293459 (W 0.00690391) | 9.04085 ± 0.145917 (W 0.032224) | 7.11794 ± 0.376899 (W 0.014696) | 🔵 tcontract 1.33× faster than `ttgt` | · | `!` between-start range over 5% |
| `ijkl-imkn-njml/n1/b1` | 6.75114 ± 0.243418 (W 0.00668182) | 9.00375 ± 0.188949 (W 0.024315) | 7.20225 ± 0.464381 (W 0.016443) | 🔵 tcontract 1.33× faster than `ttgt` | · | `!` between-start range over 5% |
| `ijkl-imln-jnkm/n1/b1` | 6.78811 ± 0.277936 (W 0.0102143) | 9.0245 ± 0.149146 (W 0.0130766) | 7.14913 ± 0.338142 (W 0.0137314) | 🔵 tcontract 1.33× faster than `ttgt` | · | `!` between-start range over 5% |
| `ijkl-imln-njmk/n1/b1` | 6.75075 ± 0.239573 (W 0.00742039) | 9.0763 ± 0.135287 (W 0.0355571) | 7.12538 ± 0.425968 (W 0.0119841) | 🔵 tcontract 1.34× faster than `ttgt` | · | `!` between-start range over 5% |
| `ijkl-imnj-nlkm/n1/b1` | 6.76782 ± 0.255908 (W 0.00924436) | 8.71321 ± 0.159984 (W 0.0241553) | 7.11035 ± 0.432866 (W 0.016822) | 🔵 tcontract 1.29× faster than `ttgt` | · | `!` between-start range over 5% |
| `ijkl-imnk-njml/n1/b1` | 6.77174 ± 0.238451 (W 0.00796295) | 8.86102 ± 0.130223 (W 0.0381394) | 7.08693 ± 0.488731 (W 0.0216928) | 🔵 tcontract 1.31× faster than `ttgt` | · | `!` between-start range over 5% |
| `ijkl-minj-nlmk/n1/b1` | 8.37491 ± 0.283228 (W 0.00934238) | 10.6182 ± 0.187382 (W 0.0159447) | 8.75329 ± 0.399629 (W 0.0329076) | 🔵 tcontract 1.27× faster than `ttgt` | · | `!` between-start range over 5% |
| `ijkl-mink-jnlm/n1/b1` | 8.13132 ± 0.25038 (W 0.00710154) | 10.7404 ± 0.0985816 (W 0.0219823) | 8.52111 ± 0.460694 (W 0.0188558) | 🔵 tcontract 1.32× faster than `ttgt` | · | `!` between-start range over 5% |
| `ijkl-minl-njmk/n1/b1` | 8.31197 ± 0.284467 (W 0.00922073) | 10.7041 ± 0.123446 (W 0.0151321) | 8.59345 ± 0.37532 (W 0.0214417) | 🔵 tcontract 1.29× faster than `ttgt` | · | `!` between-start range over 5% |

Repeated process sets describe observed repeatability under the recorded order schedule; they are not a paired baseline/candidate experiment and do not establish equal performance between engines.
