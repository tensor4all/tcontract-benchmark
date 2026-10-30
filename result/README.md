# result/

The **legacy timing-v1** result tree: the pages recorded before the timing-v2 campaigns,
and the `INDEX.md` the v1 pipeline generated over them. It is frozen history: the v1
scripts that wrote it were removed (tensor4all-meta#76 D10), nothing regenerates it, and
the raw runs behind it stay in `data/results/`. The current campaigns write elsewhere:

- [`../result-v2/tcbench/INDEX.md`](../result-v2/tcbench/INDEX.md)
- [`../result-v2/per-shape/INDEX.md`](../result-v2/per-shape/INDEX.md)

See `docs/v2-layout.md` for which tree owns what.
