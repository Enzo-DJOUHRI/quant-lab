# Data and Experiment Workflow

## Status

This page describes how the Python project currently loads data, runs an
experiment and stores its outputs. It reflects the code as of 2026-08-07. The
workflow is suitable for controlled learning experiments, but it is not a
production data platform: dataset versioning, point-in-time metadata and a
complete Alpha Research regression suite are still missing.

Relevant code:

- [`../../src/alpha_research/data_loader.py`](../../src/alpha_research/data_loader.py)
- [`../../src/alpha_research/config.py`](../../src/alpha_research/config.py)
- [`../../main.py`](../../main.py)

## What belongs where

I keep five types of files separate so that a result can be traced back to the
code and assumptions that produced it:

| File type | Location | Responsibility |
| --- | --- | --- |
| Source data cache | `data/raw/` | Local downloaded prices; regenerable and excluded from Git |
| Research code | `src/` | Financial, statistical and data transformations |
| Validation | `tests/` | Executable numerical and regression checks |
| Experiment outputs | `results/` and `outputs/` | Tables and generated visual artefacts |
| Research conclusions | `reports/` | Assumptions, evidence, interpretation and limitations |

A generated table or chart is useful only when its assumptions and meaning are
documented with it.

## Current data formats

The loader supports two tabular schemas.

Single asset:

```text
index | price | return
```

Multiple assets:

```text
index | TICKER_A_price | TICKER_B_price | TICKER_A_return | TICKER_B_return
```

Prices are adjusted close values returned by `yfinance`. Returns are simple
one-period percentage changes computed with `pct_change()`.

For a multi-asset download, rows containing any missing value are removed
after prices and returns are combined. The resulting sample is therefore the
intersection of dates with usable observations for every requested asset.
This is convenient for the current spread diagnostic but can shorten the
sample and must not be treated as a universal multi-asset data policy.

## How loading and caching work

For each requested ticker set, the loader constructs one CSV path under
`data/raw/`.

1. If the cache exists, it is read and accepted when it is non-empty and
   contains the expected columns.
2. Otherwise, prices are downloaded through `yfinance` with adjusted values.
3. Daily simple returns are computed.
4. Rows unusable under the current schema are removed.
5. The resulting dataset is written to the local cache.

The cache check does not currently verify that stored dates match the active
configuration, record the download timestamp, identify the source version or
hash the transformation code. Changing a date range may therefore require a
manual cache refresh. The cache is a convenience layer, not a versioned
research dataset.

## Project paths

Paths are resolved from the repository root rather than from the shell's
current working directory. This prevents execution from another folder from
creating duplicate `data/` or `outputs/` directories.

| Artefact | Location | Git policy |
| --- | --- | --- |
| Downloaded price cache | `data/raw/` | Ignored; external and regenerable |
| Interactive Plotly output | `outputs/plots/` | Ignored; large and regenerable |
| Public pricing figures | `reports/pricing/figures/` | Versioned with their reports |
| Parameter and comparison tables | `results/` | Versioned historical snapshots |
| Private development notes | `rapport/` | Ignored |

Public figures should come from a reproducible script or a documented
experiment. Local HTML files remain useful for exploration, but a chart alone
is not enough to support a conclusion.

## How experiments are run

`main.py` is currently a manual research entry point:

1. read tickers, dates and simplified assumptions from the configuration;
2. load a single-asset or multi-asset dataset;
3. instantiate the selected strategy objects;
4. compute absolute and benchmark-relative metrics;
5. print metric dictionaries for inspection;
6. write equity and drawdown charts.

The current Alpha code contains passive exposure, long/flat momentum,
volatility-targeted momentum, price and return mean reversion, and an initial
ratio-based two-asset spread diagnostic. I do not treat the spread prototype
as cointegration-based pairs trading: it has no estimated hedge ratio,
stationarity test or walk-forward calibration.

## Running the project

Create a local environment and install the declared dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Run the manually configured Alpha workflow:

```bash
python3 main.py
```

Run the current automated suite:

```bash
python3 -m unittest discover -s tests
```

The current public tests validate the derivatives modules. Dedicated Alpha
Research tests were deliberately deferred until that research block is
revisited and should not be implied by the global command.

Regenerate the public pricing figures:

```bash
python3 -m scripts.generate_pricing_figures
```

## Known technical limits

| Area | Current limitation | Consequence |
| --- | --- | --- |
| Experiment control | `main.py` mixes selection, execution and printing | Runs are manual and configurations are easy to overwrite |
| Cache identity | File names encode tickers but not dates or code version | A valid-looking cache can be stale for the requested experiment |
| Provenance | No manifest records source, retrieval time or transformations | A historical dataset cannot yet be reconstructed exactly from metadata alone |
| Multi-asset alignment | Complete-case `dropna()` uses the common date intersection | Missingness can change the effective sample across universes |
| Data source | `yfinance` is convenient but not a production-grade feed | Coverage, revisions and field semantics require caution |
| Result identity | Outputs are not tagged with a configuration hash or Git revision | CSV snapshots can be separated from the code that produced them |
| Metrics | Historical files use more than one annualisation and risk-free-rate convention | Results from different snapshots must not be combined mechanically |
| Alpha validation | No current automated Alpha regression suite | Strategy and metric changes require manual review until tests are rebuilt |

## Planned data improvements

The data branch will be developed before more complex modelling depends on
it. Its intended progression is:

1. immutable raw observations and explicit normalised schemas;
2. source metadata, quality flags and dataset manifests;
3. timezone-aware timestamps and causal point-in-time joins;
4. explicit staleness policies and traceable as-of lookups;
5. train, validation and test datasets tied to experiment configurations;
6. event-level market-data contracts for the future microstructure branch.

This is planned work, not an existing package. I will add new directories only
when there is working code and a clear way to validate it.
