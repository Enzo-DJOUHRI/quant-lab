# Strategy Comparison

## Status

Status: **historical in-sample research snapshot**.

This report brings together my first systematic-strategy experiments in Quant
Lab. I use it as a baseline comparison, not to select a winning model. The
values predate the current Alpha Research validation rules and are not live,
out-of-sample or investable performance.

Two frozen source tables are available:

- [`multi_asset_strategy_comparison.csv`](../../results/multi_asset_strategy_comparison.csv)
- [`multi_asset_strategy_comparison_with_mr_return.csv`](../../results/multi_asset_strategy_comparison_with_mr_return.csv)

Some early rows use the original Sharpe and annualisation conventions. This
report therefore focuses on comparisons made within the same snapshot and
does not combine those Sharpe ratios with later BTC diagnostics.

## Research question

How do simple passive, trend-following and mean-reversion rules differ in
return, risk, exposure and behaviour across several asset classes?

I am not using this comparison to pick a winner. The useful question is what
each rule assumes about market behaviour and where that assumption breaks.

## Strategies included

| Strategy | Family | Signal or exposure | Role in the study |
| --- | --- | --- | --- |
| Always long | Passive beta | Constant exposure of 1 | Main benchmark for each asset |
| Momentum | Time-series trend | Long when past price change is positive; flat otherwise | Directional timing baseline |
| Price mean reversion | Contrarian | Long below a rolling price z-score threshold, short above it | Test of level-based reversal |
| Return mean reversion | Contrarian | Long or short after an extreme rolling return z-score | Test of short-horizon return reversal |
| Ratio spread diagnostic | Two-asset mean reversion prototype | Trade the z-score of a price ratio | Engineering prototype only; not pairs trading |

## Experimental setup

- Main sample: January 2015 to December 2024.
- Main equity benchmark: `SPY` buy and hold.
- Additional assets: `AAPL`, `GOOGL`, `EURUSD=X`, `GC=F` and `BTC-USD`
  where valid cached data were available.
- Source: daily adjusted close values downloaded through `yfinance`.
- Timing: raw signals are shifted by one day before they earn returns.
- Evaluation: in sample, with parameters inspected on the same period.
- Costs: omitted from the baseline tables and studied separately for
  momentum.

The main hypotheses are intentionally simple:

- momentum assumes price direction can persist over the selected horizon;
- mean reversion assumes deviations from a rolling local centre tend to
  reverse;
- passive exposure assumes no timing rule is required to earn the asset's
  long-run risk premium.

These mechanisms can fail through whipsaw, structural trends, unstable local
means, changing regimes, omitted costs or parameter selection on noise.

## SPY baseline comparison

The first SPY experiment compared passive exposure with a 20-day long/flat
momentum signal before transaction costs.

| Strategy | Annual return | Annual volatility | Maximum drawdown | Time in market |
| --- | ---: | ---: | ---: | ---: |
| Always long | 13.28% | 17.62% | -33.72% | 100.00% |
| Momentum 20 | 9.69% | 10.53% | -13.34% | 68.38% |

Buy and hold produced more absolute return. Momentum reduced volatility and
drawdown by spending about one third of the sample in cash. The economic
comparison is therefore lower participation and lower observed downside
against higher full-market return, not evidence that momentum generated
independent alpha.

## Momentum horizon sensitivity

Only the lookback horizon was varied.

| Horizon | Annual return | Annual volatility | Maximum drawdown | Approx. switches/year |
| ---: | ---: | ---: | ---: | ---: |
| 5 days | 4.35% | 10.94% | -16.31% | 50.6 |
| 10 days | 8.96% | 10.46% | -15.14% | 30.5 |
| 20 days | 9.69% | 10.53% | -13.34% | 21.1 |
| 50 days | 7.52% | 11.13% | -21.08% | 11.5 |
| 100 days | 8.21% | 11.78% | -18.95% | 7.9 |

The 5-day rule changed state most often and was more exposed to short-lived
reversals. Longer horizons reduced turnover but reacted later. The 20-day
horizon was the best in-sample compromise in this small grid. Because the same
data selected and evaluated it, I cannot treat that ranking as evidence that
20 days will remain the best horizon on new data.

## Price mean-reversion threshold sensitivity

The price rule used a 20-day rolling mean and standard deviation.

| Z-score threshold | Annual return | Annual volatility | Maximum drawdown |
| ---: | ---: | ---: | ---: |
| 1.0 | -1.47% | 13.67% | -43.95% |
| 1.5 | 3.00% | 10.25% | -11.51% |
| 2.0 | 4.11% | 6.51% | -8.19% |
| 2.5 | 0.31% | 3.07% | -8.19% |

A low threshold repeatedly took contrarian positions in a strongly rising
equity sample. A high threshold reduced both activity and risk. The weak
return is economically coherent: a rolling z-score does not imply that the
price level is stationary, and a short position against a persistent trend
can dominate many small reversals.

## Cross-asset observations

Within the frozen comparison tables:

- momentum reduced observed risk on `SPY`, `AAPL` and `BTC-USD` but did not
  uniformly beat passive exposure in absolute return;
- passive exposure was difficult to beat on strongly trending equities and
  gold;
- return mean reversion looked comparatively less weak on `EURUSD=X` than on
  directional equity or crypto samples;
- one fixed signal did not transfer consistently across asset classes;
- incomplete `CL=F` and `ETH-USD` downloads were excluded rather than filled
  or interpreted.

These are descriptive observations from a small, hand-selected universe. They
do not establish asset-class-specific edges.

## Initial two-asset spread diagnostic

The first multi-asset prototype used:

```text
ratio_t = SPY_price_t / QQQ_price_t
signal_t = z_score(ratio_t, window=20, threshold=2), shifted by one day
spread_return_t = SPY_return_t - QQQ_return_t
strategy_return_t = signal_t * spread_return_t
```

Historical output:

| Metric | Value |
| --- | ---: |
| Total return | 1.28% |
| Annual volatility | 3.11% |
| Maximum drawdown | -8.47% |
| Time flat | 89.90% |
| Signal switches/year | 27.87 |

I do not treat this prototype as pairs trading. The signal is built from a
price ratio, while PnL uses an equal-weight return difference. There is no
estimated hedge ratio, cointegration test, stationarity gate, structural-
break monitor, transaction cost or walk-forward calibration. The prototype
only verifies that the multi-asset pipeline can form and trade a spread-like
diagnostic.

A future pairs study will be a separate time-series project with training-
sample hedge-ratio estimation, residual diagnostics, cointegration testing
and out-of-sample re-estimation. Correlation alone is insufficient because two
highly correlated non-stationary prices can still drift apart indefinitely.

## What the comparison suggests

| Rule | Apparent strength | Main weakness | Current verdict |
| --- | --- | --- | --- |
| Always long | Transparent benchmark and full participation | Full market drawdown and beta | Baseline |
| Momentum | Lower observed volatility and drawdown on SPY | Missed upside, whipsaw and parameter sensitivity | Orange |
| Price mean reversion | Low activity at conservative thresholds | No stationary-price justification | Red in current form |
| Return mean reversion | Different behaviour from price-level reversal | Weak and inconsistent transfer across assets | Orange as a diagnostic only |
| Ratio spread | Exercises the multi-asset workflow | Not a coherent pairs model or fully specified portfolio | Red as a strategy claim |

## Limitations and next step

- Every strategy and parameter grid is evaluated in sample.
- The study does not control for multiple testing or data snooping.
- Cost and financing assumptions are not common across all rules.
- Early snapshots do not share the latest risk-free-rate convention.
- The universe is small and constrained by locally available data.
- The current metric layer still has documented equity and exposure caveats.
- No public Alpha regression tests currently protect these historical
  results.

Overall verdict: **Orange as a baseline research record**.

The next step is not another signal. I first need a stable backtester with
explicit initial equity, consistent costs and exposure metrics, followed by a
pre-specified train/test or walk-forward momentum study. Pairs trading starts
only after the separate time-series and cointegration foundations are ready.
