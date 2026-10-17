# Migrating this campaign to the timing-v2 system

Status: **proposal** (2026-10-17). This is the plan the independent pre-review reads; nothing here is
implemented yet. The harness side is already done: `tcontract-rs` main `953a2ff9` (PR #127) carries the
v2 evidence contract, so the campaign no longer needs to invent one.

## What exists today

- two suites with different runners: `benchmarks/suites/tcbench.yaml` (the TCCG corpus, 49 cases,
  `sizes_mib`, `features: [tblis]`) and `benchmarks/suites/per-shape.yaml` (21 named contraction cases,
  including MPS chains, run by `lukbench`);
- one measured library (`tprims` = `tcontract-rs`) with engine rows `plan`, `packed` (this library),
  `ttgt` (OpenBLAS), `blas` (system BLAS) and `tblis` (the external baseline, built when the suite asks
  for the `tblis` feature);
- the campaign's own recorder, report and index; the TBLIS identity comes from `$TBLIS_ROOT/PROVENANCE`
  and the pages refuse an unknown revision.

## What the migration has to preserve

The immutable inputs stay where they are: the corpus (which case exists, what it computes, what dtype it
fixes, how many steps it has) is defined by `corpus.rs` in the measured revision. The toolkit gets the
*declared identity* of each case, not another implementation of contraction semantics.

## Plan

1. **Two campaigns, not one.** The toolkit descriptor names a single measured binary per campaign, and
   these two suites run different harnesses. So `benchmarks/campaign.yaml` describes the `tcbench`
   campaign and a second descriptor describes the `lukbench` campaign, each with its own suite and its
   own pages under `result/<host>/<campaign>/`. Splitting is also honest: the two suites measure
   different things.
2. **Generate the declaration from the pinned corpus, once.** The harness now emits a census of its
   declared grid; running the pinned binary's census (with `--rows` for the arm's engine list) is the
   bootstrap that turns the corpus into a committed suite: one family per case id, `n` = the suite's
   size spec verbatim, `order: ['']`, `batch: [1]`, the dtype axis = the union of the dtypes the corpus
   supports, and the engine rows from the campaign's provider mapping. The generated file is committed
   and then frozen; the generator is a script in this repo, not a build step.
3. **Per-case dtype stays a declaration fact, not a runtime filter.** A case whose corpus fixes its
   dtype is declared only at that dtype where the generator can tell, and any declared cell the corpus
   cannot measure is a *skipped* census row (the harness emits it). A requested engine whose feature was
   not built is an **admission failure**, never a skip - the harness itself refuses that configuration,
   and a page with no independent reference is not a page.
4. **Provenance.** Reuse the existing engine/provider mapping and the existing TBLIS collector (commit,
   bundled BLIS revision, artifact hash). That means a small toolkit change: the provider entry has to
   accept the `tag`/`sha256` the collector already records, and the page has to print them.
5. **Recording and verification.** Frozen per campaign, then recorded with `record_run.py` against the
   pinned toolkit: chronological samples, the median statistic, at least two timed calls per row and at
   least two complete process sets with the recorded engine rotation, plus the `verify` census per arm.
   `validate_run.py` must pass before anything is published.
6. **Pages.** Fresh v2 pages per campaign and arm, named for the measured revision, next to the
   historical ones; the historical pages are not rewritten. Both suites are re-pinned to `953a2ff9`
   (or a later commit) in `pins/`.

## Fidelity cost, stated up front

- For `tcbench` the declared `n` is the *size spec*, not a matrix dimension: the corpus resolves
  extents from that knob with rank-dependent rounding, so the identity columns carry the declared spec
  and the resolved extents travel in `case_m`/`case_n`/`case_k`. The pages must say so rather than
  present the spec as geometry.
- A whole-program case (the MPS chain: 65 inputs, 64 pairwise steps, one timed call) has no equivalent
  matrix shape; it keeps its declared sentinel shape with the real extents beside it.
- The two-campaign split means no single TOC lists everything this repository measures; the top-level
  index has to link both.

## Not in this plan

- No change to what the corpus computes, no new engines, no GPU work.
- No re-recording of the historical v1 pages.
- Cpueinsum is a separate campaign in its own repository and is not part of this migration.
