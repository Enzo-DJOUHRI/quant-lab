# Quant Lab

Quant Lab is my personal research repository for learning quantitative
finance by connecting theory, implementation and empirical testing.

The current code focuses on systematic strategy research. Pricing,
risk management and portfolio construction will be added progressively
as the corresponding mathematical foundations are studied. This is an
evolving laboratory, not a finished trading product.

## Current scope

Implemented:

- market data loading and local caching with `yfinance`;
- single-asset and multi-asset workflows;
- always-long benchmark;
- time-series momentum;
- momentum with volatility targeting;
- price- and return-based mean reversion;
- ratio/z-score spread mean reversion;
- linear transaction costs for the momentum strategies;
- performance, risk and benchmark-relative metrics;
- interactive Plotly equity and drawdown charts;
- unit tests for momentum transaction costs and selected metrics.

Research roadmap:

| Axis | Status | Main topics |
| --- | --- | --- |
| Alpha research | Active | Robust backtesting, sensitivity, out-of-sample validation, pairs trading |
| Option pricing | Planned | Binomial trees, Black-Scholes-Merton, Greeks, implied volatility |
| Simulation | Planned | Geometric Brownian motion and Monte Carlo |
| Risk | Planned | VaR, Expected Shortfall and stress testing |
| Portfolio | Planned | Markowitz, ETF diversification and risk contributions |
| Machine learning | Later | Financial applications with time-aware validation |

## Current research example

The current default configuration runs a historical experiment on
`BTC-USD` from 2015 to 2024. Momentum strategies use a simplified cost
of 5 basis points per position change, daily crypto data are annualized
over 365 days, and the risk-free rate is fixed at 2%.

| Strategy | Annualized return | Annualized volatility | Sharpe | Maximum drawdown |
| --- | ---: | ---: | ---: | ---: |
| Always long | 76.5% | 69.3% | 1.14 | -83.4% |
| Momentum, 20-day horizon | 88.8% | 48.9% | 1.50 | -52.6% |
| Momentum with volatility targeting | 36.0% | 16.1% | 1.86 | -23.0% |

These figures are in-sample diagnostic results from the current local
configuration. They are not live performance, investment advice or an
estimate of future returns. Parameter selection is not yet validated
out of sample, the risk-free rate is simplified, and the transaction
cost model does not yet include dynamic spread, slippage or market
impact.

The [`rapport/`](rapport/) directory records the research process and
the [`results/`](results/) directory contains experiment tables. Older
research snapshots may use earlier assumptions and should not be
compared mechanically with the current run.

## Run the project

Python 3 is required.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 main.py
```

The active tickers, dates and simplified market assumptions are defined
in [`src/config.py`](src/config.py). If cached data are unavailable, the
loader downloads adjusted market data through `yfinance`. Interactive
charts are generated under `outputs/plots/`.

Run the current tests with:

```bash
python3 -m unittest discover -s tests -v
```

## Repository structure

```text
Quant_Lab/
|-- main.py                 # Current end-to-end research workflow
|-- src/                    # Data, strategies, metrics and plots
|-- tests/                  # Current unit tests
|-- results/                # Experiment and sensitivity tables
|-- rapport/                # Dated research notes
`-- requirements.txt
```

The structure will evolve only when new modules are actually developed.
Planned axes are intentionally not represented by empty directories.

## Known limitations and next research steps

- introduce strict in-sample/out-of-sample or walk-forward evaluation;
- study parameter sensitivity and data-snooping risk;
- improve market assumptions and transaction cost modelling;
- broaden unit tests as the research workflow grows;
- separate ratio-based spread mean reversion from a future
  cointegration-based pairs trading study;
- regenerate or label historical reports when assumptions change.

The objective is not to manufacture attractive backtests. It is to
understand which assumptions drive a result, how it can fail and what
evidence is still missing.
