# Strategy Comparison

## Research question

How do simple passive, trend-following and mean-reversion rules differ
in return, risk, market exposure and behaviour across asset classes?

This report consolidates the useful results from the first Alpha
Research experiments. It is a baseline study, not a strategy selection
claim.

## Experimental setup

- Main sample: January 2015 to December 2024.
- Main equity benchmark: `SPY` buy and hold.
- Additional assets: `AAPL`, `GOOGL`, `EURUSD=X`, `GC=F` and
  `BTC-USD` where valid cached data were available.
- Daily adjusted prices downloaded through `yfinance`.
- Signals are shifted by one day before being applied to returns.
- Strategies: always long, long/flat time-series momentum, price mean
  reversion and return mean reversion.

The earliest comparison snapshot did not yet subtract the risk-free
rate from Sharpe and used the original annualisation convention.
Therefore, this report emphasises returns, volatility, drawdown and
relative behaviour. Current BTC metrics are reported in the root
README under the corrected 365-day and 2% risk-free-rate convention.

## SPY baseline comparison

The first experiment compared passive exposure with a 20-day
long/flat momentum signal before transaction costs.

| Strategy | Annual return | Annual volatility | Maximum drawdown | Time in market |
| --- | ---: | ---: | ---: | ---: |
| Always long | 13.28% | 17.62% | -33.72% | 100.00% |
| Momentum 20 | 9.69% | 10.53% | -13.34% | 68.38% |

The passive benchmark produced more absolute return, while momentum
reduced volatility and drawdown by moving to cash when its signal was
negative. This makes the comparison a trade-off between market
participation and downside control rather than a simple winner/loser
ranking.

## Momentum horizon sensitivity

The horizon was varied without changing the underlying rule.

| Horizon | Annual return | Annual volatility | Maximum drawdown | Approx. switches/year |
| ---: | ---: | ---: | ---: | ---: |
| 5 days | 4.35% | 10.94% | -16.31% | 50.6 |
| 10 days | 8.96% | 10.46% | -15.14% | 30.5 |
| 20 days | 9.69% | 10.53% | -13.34% | 21.1 |
| 50 days | 7.52% | 11.13% | -21.08% | 11.5 |
| 100 days | 8.21% | 11.78% | -18.95% | 7.9 |

The 5-day signal changed state too frequently and was more exposed to
short-lived reversals. Longer horizons reduced turnover but reacted
more slowly to regime changes. The 20-day horizon was the strongest
in-sample compromise in this particular grid; it has not yet been
validated out of sample.

## Price mean-reversion threshold sensitivity

The price z-score strategy used a 20-day rolling window and entered
long or short positions beyond a chosen threshold.

| Z-score threshold | Annual return | Annual volatility | Maximum drawdown |
| ---: | ---: | ---: | ---: |
| 1.0 | -1.47% | 13.67% | -43.95% |
| 1.5 | 3.00% | 10.25% | -11.51% |
| 2.0 | 4.11% | 6.51% | -8.19% |
| 2.5 | 0.31% | 3.07% | -8.19% |

A low threshold produced frequent counter-trend positions in a
strongly rising equity sample. A high threshold reduced risk but left
the strategy inactive most of the time. The experiment is useful
because it shows why a plausible statistical rule can fail when its
economic setting and directional exposure are ignored.

## Cross-asset observations

The same fixed rules were then applied to several assets. The raw
tables are available in:

- [`multi_asset_strategy_comparison.csv`](../../results/multi_asset_strategy_comparison.csv)
- [`multi_asset_strategy_comparison_with_mr_return.csv`](../../results/multi_asset_strategy_comparison_with_mr_return.csv)

Main observations from this historical snapshot:

- momentum improved the risk profile on `SPY`, `AAPL` and `BTC-USD`;
- passive exposure remained difficult to beat in absolute return on
  strongly trending equities and gold;
- return mean reversion was comparatively more suitable for
  `EURUSD=X` than for directional equity or crypto samples;
- one fixed rule did not transfer uniformly across asset classes;
- empty or incomplete `CL=F` and `ETH-USD` downloads were excluded from
  interpretation.

## Initial spread experiment

The first multi-asset rule used the rolling ratio between `SPY` and
`QQQ`, a 20-day z-score and a threshold of 2.

| Metric | Historical value |
| --- | ---: |
| Total return | 1.28% |
| Annual volatility | 3.11% |
| Maximum drawdown | -8.47% |
| Time flat | 89.90% |
| Signal switches/year | 27.87 |

This is ratio mean reversion, not a cointegration-based pairs-trading
model. Correlation alone does not establish a stationary spread. A
future study must estimate the hedge ratio on training data, test
cointegration, monitor structural breaks and evaluate the rule through
walk-forward validation.

## Limitations

- Results are in sample and parameter choices use the same historical
  period as evaluation.
- The study does not yet control for data snooping across strategies,
  horizons and thresholds.
- Early comparisons do not use the current risk-free-rate convention.
- Transaction costs are treated separately in the dedicated report.
- The asset universe is small and based on available cached data.
- No conclusion should be interpreted as evidence of a persistent
  tradable edge.
