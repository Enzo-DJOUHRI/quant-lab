# Momentum With Volatility Targeting

## Status

Status: **historical parameter study with a later local diagnostic**.

The saved CSV grids predate the final crypto annualisation and risk-free-rate
corrections. I therefore compare rows only within the same snapshot instead
of mixing their Sharpe ratios with later outputs. The BTC table below records
the active local configuration as of 2026-08-07 and states its conventions
separately.

Related files:

- [`momentum_vol_targeting_grid_spy_btc.csv`](../../results/momentum_vol_targeting_grid_spy_btc.csv)
- [`momentum_vol_targeting_rebal_threshold_spy_btc.csv`](../../results/momentum_vol_targeting_rebal_threshold_spy_btc.csv)
- [`../../src/alpha_research/strategy.py`](../../src/alpha_research/strategy.py)

No result in this report is out of sample.

## Strategy definition

| Field | Definition |
| --- | --- |
| Name | Momentum with volatility targeting |
| Family | Long/flat time-series momentum with dynamic risk sizing |
| Assets studied | `SPY` and `BTC-USD` |
| Main comparison | Classic long/flat momentum with the same horizon |
| Direction | Long after positive lagged momentum; flat otherwise |
| Size | Target volatility divided by estimated annual volatility, capped by maximum leverage |
| Costs | Linear charge based on the change in executed exposure |

Hypothesis: momentum determines when directional exposure is desirable, while
volatility targeting can keep the amount of risk more stable through time.

## Mechanics

### Directional signal

```text
momentum_t = price_t / price_(t-horizon) - 1
raw_signal_t = 1 if momentum_t > 0 else 0
signal_t = raw_signal_(t-1)
```

The one-period shift prevents the current close from both creating the signal
and earning the same period's return.

### Volatility estimate and target size

```text
rolling_vol_t = rolling_std(asset_return, vol_window)
rolling_vol_annual_t = rolling_vol_t * sqrt(trading_days)
position_size_t = min(target_vol / rolling_vol_annual_t, max_leverage)
target_exposure_t = signal_t * position_size_t
```

If estimated volatility is above the target, exposure falls below one. If it
is below the target, the strategy can lever up until `max_leverage`. The
direction and the risk budget are therefore separate decisions.

### Rebalancing and costs

```text
if abs(target_exposure_t - exposure_(t-1)) < rebal_threshold:
    exposure_t = exposure_(t-1)
else:
    exposure_t = target_exposure_t

trade_size_t = abs(exposure_t - exposure_(t-1))
transaction_cost_paid_t = cost_rate * trade_size_t
strategy_return_t = exposure_t * asset_return_t
                    - transaction_cost_paid_t
```

The no-trade band acts on exposure, not on the momentum signal. It accepts a
small deviation from the target to avoid paying for every minor volatility
update.

## Why volatility targeting can improve Sharpe

Suppose conditional asset volatility is `sigma_t` and exposure is
approximately `target_vol / sigma_t`. Ignoring caps and estimation error, the
conditional volatility of the scaled return is then approximately the target:

```text
vol(exposure_t * return_t | information_t)
approximately target_vol
```

This can improve risk-adjusted performance when volatility clusters and high-
volatility periods are not compensated by proportionally higher expected
returns. Reducing exposure during turbulent regimes can also reduce
drawdowns and volatility drag. For small returns, geometric growth is roughly
arithmetic mean minus one half of variance, which explains why controlling
variance can matter even without increasing average raw return.

There is no guaranteed Sharpe improvement. The estimate is backward-looking,
can de-risk only after a shock, can increase leverage before volatility rises
and can remove exposure during a profitable rebound.

## Why turnover can increase

Classic binary momentum trades only when the directional state changes.
Volatility targeting changes desired exposure whenever the rolling volatility
estimate changes. It can therefore rebalance on many days even while the
signal remains long.

The number of adjustment days and the cost paid need not move one-for-one. A
volatility-targeted rule can make more frequent but smaller trades, producing
more `n_trades` while accumulating less `total_cost` than a binary strategy.

## Historical parameter study

The first sweep tested 81 configurations per asset:

- momentum horizon: 10, 20 or 50 observations;
- volatility window: 20, 60 or 120 observations;
- target volatility: 10%, 15% or 20%;
- maximum leverage: 1.0, 1.5 or 2.0;
- cost rate: 5 basis points.

This grid is exploratory. Because all configurations use the same evaluation
sample, selecting the best row would create in-sample selection bias.

## SPY snapshot

Representative rows from the historical grid:

| Configuration | Annual return | Annual volatility | Maximum drawdown | Adjustment days |
| --- | ---: | ---: | ---: | ---: |
| Momentum, horizon 20 | 8.54% | 10.53% | -14.20% | 210 |
| Target 10%, window 20, leverage cap 2 | 9.18% | 8.12% | -12.63% | 1,791 |
| Target 20%, window 20, leverage cap 2 | 13.90% | 14.61% | -22.62% | 1,134 |
| Target 10%, window 60, leverage cap 1 | 5.61% | 6.87% | -9.76% | 1,358 |

The defensive 10% target reduced realised volatility and drawdown in this
sample, but it required many more exposure adjustments. The 20% target raised
risk and historical return; it did not simply create a safer version of the
classic rule.

## BTC diagnostic under the active convention

The active local configuration uses:

```text
horizon = 20
vol_window = 20
target_vol = 20%
max_leverage = 2.0
rebal_threshold = 0.05
cost_rate = 5 basis points
annualisation = 365 observations
risk_free_rate = 2% annual placeholder
```

Diagnostic output on the local 2015-2024 BTC cache:

| Metric | Classic momentum | Volatility targeting |
| --- | ---: | ---: |
| Annual return | 88.77% | 35.96% |
| Annual volatility | 48.87% | 16.11% |
| Sharpe | 1.50 | 1.86 |
| Maximum drawdown | -52.63% | -23.03% |
| Exposure-adjustment days (`n_trades`) | 330 | 602 |
| Sum of return costs (`total_cost`) | 0.1650 | 0.0898 |
| Active signal fraction (`time_in_market`) | 57.74% | 57.74% |

The dynamic strategy gave up much of BTC's raw upside because its exposure
was usually below one, but it reduced realised volatility and drawdown enough
to increase historical Sharpe. It adjusted exposure more often, yet paid a
smaller sum of modelled costs because many adjustments were smaller than the
full entries and exits of binary momentum.

The raw data cache is excluded from Git and the data source can revise
history, so this table is a dated diagnostic rather than a permanently frozen
market-data result.

## No-trade-band study

The historical threshold sweep varied `rebal_threshold` from 0 to 0.10. For
the SPY 10% target configuration, the number of adjustment days fell from
1,791 to 461 while annual return remained near 9.2% and maximum drawdown near
-12.6% in that snapshot. BTC turnover also fell materially, but wider bands
allowed realised exposure and risk to drift further from target.

The trade-off is straightforward:

- a narrow band follows the volatility estimate closely but trades often;
- a wide band lowers turnover but weakens volatility targeting;
- the appropriate threshold depends on cost, liquidity and acceptable risk
  drift, not only on the highest in-sample Sharpe.

## A note on the metrics

The current `time_in_market` metric reads the binary `signal`, so both BTC
strategies report the same 57.74% active fraction. This does not mean they took
the same risk. Volatility targeting held a smaller and continuously varying
`exposure`. Average absolute exposure and exposure-based activity must be
reported in the next version.

Similarly, `n_trades` counts adjustment days, not completed trades or round
trips. `total_cost` is the sum of return charges, not a currency amount.

## Strengths and weaknesses

Strengths:

- separates directional conviction from risk sizing;
- responds to volatility clustering with an explicit risk budget;
- makes leverage, turnover and implementation cost observable;
- the no-trade band introduces a practical control rather than changing the
  signal after seeing returns.

Weaknesses:

- rolling volatility is lagged and estimation-sensitive;
- leverage and financing are simplified;
- the fixed linear cost omits spread, slippage and market impact;
- all parameter comparisons are in sample;
- annualisation conventions differ between frozen grids and the later BTC
  diagnostic;
- the current exposure metric is incomplete.

## Verdict and next step

Verdict: **Orange**.

The risk-sizing idea is coherent and it materially changed the return path,
especially on BTC. The result is interesting, but it is not evidence of a
stable edge because the parameters and the evaluation use the same history.
The next step is a pre-specified walk-forward comparison with classic
momentum, fixed cost scenarios, exposure-based diagnostics and a parameter-
stability analysis.
