# Momentum Transaction Costs

## Status

Status: **historical in-sample research snapshot**.

This experiment applies one simple cost model to a fixed SPY sample. I use it
to check the accounting and to see whether a momentum result survives a
reasonable friction assumption. It is not an out-of-sample validation of
momentum. The current implementation is in
[`../../src/alpha_research/strategy.py`](../../src/alpha_research/strategy.py).

## Strategy definition

| Field | Definition |
| --- | --- |
| Name | Momentum 20 with linear transaction costs |
| Family | Long/flat time-series momentum |
| Asset | `SPY` |
| Main comparison | The same momentum rule before and after costs |
| Contextual benchmark | `SPY` buy and hold |
| Signal | Long when the 20-day price momentum is positive; flat otherwise |
| Execution timing | The raw signal is shifted by one day before it earns returns |

Hypothesis: medium-horizon price persistence may justify holding the asset
after positive momentum, but the signal remains useful only if its gross
benefit survives the cost of changing exposure.

Why it could work:

- trends may persist because information and positioning adjust gradually;
- moving to cash can reduce exposure during sustained negative regimes.

Why it can fail:

- short-lived reversals can generate repeated entries and exits;
- the strategy can miss sharp rebounds while flat;
- a result selected on the same sample can be data-mined;
- realistic spread, slippage and market impact can exceed the fixed cost.

## Experimental setup

- Sample: January 2015 to December 2024.
- Observations: 2,514 daily rows.
- Horizon: 20 observations.
- Position set: `{0, 1}`.
- Cost rate: `0.0005`, or 5 basis points per unit change in position.
- Evaluation: in sample.

## Accounting model

Let `signal_t` be the executed position for period `t`.

### Trade size

```text
trade_size_t = abs(signal_t - signal_(t-1))
```

`trade_size` measures the magnitude of the exposure change. For this binary
long/flat rule, entering or leaving the market produces `trade_size = 1` and
keeping the same state produces `0`. It is turnover, not a prediction score.

### Cost paid

```text
transaction_cost_paid_t = cost_rate * trade_size_t
```

The charge is expressed in return units and is deducted on the adjustment
date. Economically, this approximates the friction paid to move the portfolio
from its previous exposure to its new exposure.

### Net strategy return

```text
strategy_return_t = signal_t * asset_return_t
                    - transaction_cost_paid_t
```

The position earns the contemporaneous asset return only after the one-day
signal shift. The cost is then subtracted from that same period. This makes
the reported equity curve net of the modelled friction.

## Execution metrics

| Metric key | Current calculation | Interpretation |
| --- | --- | --- |
| `n_trades` | Number of rows where `trade_size > 0` | Exposure-adjustment days, not completed round trips |
| `total_cost` | Sum of `transaction_cost_paid` | Sum of return charges, not a cash amount unless applied to capital |
| `time_in_market` | Fraction of rows where `signal != 0` | Share of observations carrying directional exposure |

These three diagnostics show the trading activity hidden behind a return
series. Two strategies can have similar gross returns and very different net
results when one changes exposure much more often.

## Historical result

| Metric | Before costs | After costs |
| --- | ---: | ---: |
| Total return | 151.63% | 126.56% |
| Annual return | 9.69% | 8.54% |
| Annual volatility | 10.53% | 10.53% |
| Maximum drawdown | -13.34% | -14.20% |

Additional diagnostics after costs:

| Diagnostic | Value |
| --- | ---: |
| Exposure-adjustment days (`n_trades`) | 210 |
| Approximate adjustments per year | 21 |
| Sum of charged return costs (`total_cost`) | 0.1050 |
| Time in market | 68.38% |

The net row is also preserved in the SPY section of
[`momentum_vol_targeting_rebal_threshold_spy_btc.csv`](../../results/momentum_vol_targeting_rebal_threshold_spy_btc.csv).

## Interpretation

On this sample, trading frequency was moderate for a daily strategy, but 210
position changes still accumulated a material cost. The cumulative return
fell by about 25 percentage points and the annualised return by about 1.15
percentage points. Drawdown also became slightly worse because costs are paid
exactly when the position changes.

The rule remained profitable in this historical sample and was invested
about two thirds of the time. That is not enough to establish an edge: the
same period was used to choose and evaluate the horizon, and the cost rate was
assumed rather than estimated from historical execution data.

## Model limitations

The linear model omits:

- time-varying bid-ask spreads;
- slippage conditional on volatility and liquidity;
- nonlinear market impact and trade size relative to volume;
- delayed, rejected or partial execution;
- financing, borrowing and tax effects;
- asset-specific fees and changing market structure.

It also assumes that the entire desired exposure change occurs at the
observed cost rate. The 5-basis-point input is a stress assumption, not an
estimate of the exact historical implementation shortfall.

## Verdict and next step

Verdict: **Orange**.

The useful lesson is that gross momentum is not the result that matters:
turnover and costs can materially change the conclusion. The next step is a
pre-specified train/test or walk-forward evaluation with several cost levels,
unchanged accounting and no parameter reselection on the test period.
