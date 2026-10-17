# Migrating this campaign to the timing-v2 system

Status: **revised after an independent pre-review (2026-10-17); nothing implemented.** The review
(`docs/reviews/20261017-migration-pre-review.md`) rejected the plan below as too small by half and named
five blockers. Read this section first; the reviewed plan is kept underneath as the record.

## Revised plan (what actually has to happen)

The migration is three workstreams, in this order. Each one is finished and merged before the next
starts, because the later ones are only meaningful once the earlier ones hold.

**A. Toolkit prerequisites (nothing in this repository can be recorded without them).**

1. **A no-BLAS-vendor recording path.** Both suites measure `plan`/`packed` plus the external `tblis`
   baseline (and `ttgt`, an OpenBLAS-backed *engine*, not a vendor arm). The recorder today requires a
   selected vendor, requires `info` to name it, and serializes a `vendor` block the schema only accepts
   as an object; with no vendor arm there is nothing to select. `blas` is a *feature*, not an engine row,
   so it cannot serve as the vendor either. The recorder must admit a vendor-less campaign and omit the
   block, and TBLIS must be recorded as an *external provider* rather than mislabelled as a mutually
   exclusive BLAS vendor.
2. **External-provider ingestion.** The toolkit currently manufactures every non-vendor provider as "the
   provider in the measured revision" with a null commit; this campaign's `tblis_identity()` collector
   (commit, bundled BLIS revision, artifact hash) would be discarded, together with the refusal to
   publish an arm whose revision cannot be stated. The collector has to feed the manifest, `tag`/`sha256`
   have to be accepted by both schema copies, and the page has to print the external provider's identity
   independently of Cargo-dependency provenance.
3. **Build features and the loader.** The old recorder exports `BENCH_FEATURES=tblis` for the build and
   puts `$TBLIS_ROOT/{lib,lib64}` on `LD_LIBRARY_PATH`; the toolkit exports only `BENCH_VENDOR` and marks
   `measured.features` unused, while its suite schema rejects the old top-level `features`. A
   deterministic build invocation with the suite's features and the loader path has to be part of the
   campaign contract, or the `tblis` row fails admission or the binary cannot load.
4. **Legacy evidence compatibility.** The historical manifests (`library: tprims`, `sizes_mib`,
   legacy guard fields) are validated by CI and read by the index, and the toolkit's schema rejects
   unknown properties and requires `library`; validation fails at schema checking before any
   declaration-drift handling. Historical evidence and pages stay untouched, so the repository needs an
   explicit read-only legacy route (or compatibility reader) instead of replacing the scripts blindly.

**B. The measured repository: `lukbench`'s v2 contract.** Half of this deliverable is the `per-shape`
suite, and its harness has none of the v2 contract yet: it ignores unknown options, warns (rather than
refuses) about unavailable engines, keeps best/scatter instead of samples, hard-codes the execution order
plan/packed/tblis with no rotation, and writes no census, no status and no thread-budget columns. That is
the same work that landed for `tcbench` in `953a2ff9` and it lands as its own reviewed change, before any
declaration is generated.

**C. This campaign.** Then, and only then:

5. **Declaration.** Generate the suite once from the pinned corpus's census and freeze it, with the
   corrections the review established: **omit `order` entirely** (a literal `''` is invalid in the run
   schema, and the evidence already supplies the empty identity value when the axis is absent); keep
   **singleton size populations** with unique regime labels (the recorder joins `n` values with commas
   while `tcbench` parses a single numeric spec); and emit the **entire rectangular dtype product** for
   `lukbench`, whose cases fix their dtype, marking wrong-dtype cells *skipped* in both the verification
   and the timed census - a suite-level skip summary or silently filtered cases is not enough, because
   validation compares the census to the whole declared grid and then requires identical timed cells,
   statuses and notes. Declaring only native-dtype cells would need dtype-separated suites or an explicit
   toolkit contract change; that is not part of this plan.
6. **Layout and naming.** Two descriptors (one per runner) are supported through `CAMPAIGN_DESCRIPTOR`,
   but a descriptor id does not create a namespace: the raw directory, the page and the index all key off
   the *active* descriptor's `suites_dir`/`result_dir`. So the second campaign gets its own explicitly
   selected descriptor, its own suite directory and its own result/index directory, sharing the
   repository-level admission lock; the top-level index links both rather than trying to union them.
7. **Frozen engine lists and rotation.** `tcbench` exposes `plan,packed[,ttgt][,tblis]` and `lukbench`
   exposes `plan,packed[,tblis]`; the suites select three rows. Validation requires the process-set count
   to be a multiple of the engine-row count, so these campaigns take **3, 6, ...** sets, not two, and the
   rotation must be a complete cycle. `lukbench`'s engine order has to become a real rotated execution
   order as part of workstream B.
8. **`lukbench`'s shape identity** is still undefined: `per-shape` declares no size axis, and the harness
   reports actual/final-step dimensions. The numeric sentinel and its echoing semantics have to be chosen
   and documented in this plan before the declaration is generated.
9. **Then** the records and the pages: `validate_run.py` passing per arm before anything is published,
   fresh v2 pages named for the measured revision, historical pages untouched.

## The reviewed plan (kept as the record)

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
