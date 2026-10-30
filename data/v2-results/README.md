# data/v2-results/

Raw timing-v2 runs, one directory per `(campaign, profile, suite, timestamp)`:

    data/v2-results/<campaign>/<profile>/<suite>/<timestamp>/

Written by `campaign_toolkit.record_run` when one of the two v2 descriptors is selected
(`CAMPAIGN_DESCRIPTOR=benchmarks/campaign-<campaign>.yaml`). The legacy timing-v1 runs
under `data/results/**` are a different tree and are not written here.

Both campaigns have recorded runs on `zen5-cpu`; their pages and indexes are under
`result-v2/<campaign>/` (`INDEX.md` for the pages at the pin, `HISTORY.md` for the rest).
See `docs/v2-layout.md`.
