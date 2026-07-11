# Data and Experiment Workflow

## Current objective

The current workflow is intentionally small: download adjusted market
prices, cache them locally, run a selected group of strategies, compute
metrics and export interactive charts. It is a research script rather
than a production backtesting engine.

## Data loading

`src/data_loader.py` supports two schemas.

Single asset:

```text
index | price | return
```

Multiple assets:

```text
index | TICKER_A_price | TICKER_B_price | TICKER_A_return | TICKER_B_return
```

The loader first checks a local CSV cache under `data/raw/`. If the file
is missing or does not contain the expected columns, adjusted close data
are downloaded through `yfinance`, converted to returns and cached.
Downloaded data are excluded from Git because they are external,
regenerable artefacts.

## Stable project paths

Data and chart paths are resolved from the project root rather than the
shell's current working directory. This prevents the same command from
creating duplicate `data/` or `outputs/` directories when it is run
from a different folder.

Interactive Plotly charts are written to `outputs/plots/`. They are
also excluded from Git because the HTML files are large and can be
regenerated from the experiment.

## Experiment flow

`main.py` currently performs the following sequence:

1. read tickers, dates and simplified market assumptions from
   `src/config.py`;
2. load one or several assets;
3. run the selected strategy objects;
4. compute absolute and benchmark-relative metrics;
5. print the metric dictionaries;
6. write equity and drawdown charts.

The code currently supports:

- always-long exposure;
- long/flat momentum;
- momentum with volatility targeting and a no-trade band;
- price and return mean reversion;
- ratio-based spread mean reversion.

## Research artefacts

- `results/` stores parameter grids and cross-asset comparison tables;
- `reports/alpha_research/` explains the corresponding experiments;
- `reports/engineering/` records decisions that affect reproducibility;
- local raw data and generated charts remain outside version control.

## Current engineering limits

- `main.py` is manually configured and mixes experiment selection with
  reporting.
- Results are not automatically tagged with a configuration hash or
  code revision.
- Cached data do not yet include a formal data-quality or provenance
  manifest.
- The `yfinance` source is convenient for learning but is not a
  production-grade market data feed.
- Historical CSV outputs can reflect different metric conventions, so
  reports must state their assumptions.

Future restructuring will follow actual research needs. Empty pricing,
risk or portfolio modules are not created before those axes are
implemented.
