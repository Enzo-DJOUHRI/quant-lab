# Momentum Transaction Costs

## Research question

How much does a simple execution-cost assumption change the historical
performance of a 20-day long/flat momentum strategy?

## Setup

- Asset: `SPY`.
- Sample: January 2015 to December 2024, 2,514 observations.
- Signal: long when 20-day momentum is positive, otherwise flat.
- Execution delay: the signal is shifted by one day.
- Cost assumption: 5 basis points per unit change in position.

## Cost model

For a binary position `signal_t`:

```text
trade_size_t = abs(signal_t - signal_(t-1))
transaction_cost_t = 0.0005 * trade_size_t
net_return_t = signal_t * asset_return_t - transaction_cost_t
```

Moving from cash to long, or from long to cash, has a trade size of 1.
The model charges costs directly against strategy return on each
position change.

## Historical result

| Metric | Before costs | After costs |
| --- | ---: | ---: |
| Total return | 151.63% | 126.56% |
| Annual return | 9.69% | 8.54% |
| Annual volatility | 10.53% | 10.53% |
| Maximum drawdown | -13.34% | -14.20% |

Additional execution diagnostics after costs:

| Diagnostic | Value |
| --- | ---: |
| Position changes | 210 |
| Approx. position changes/year | 21 |
| Sum of charged costs | 0.1050 |
| Time in market | 68.38% |

The cost assumption removed approximately 25 percentage points from
the cumulative return over the sample. Even a moderate-frequency rule
was therefore materially affected by execution frictions.

## Interpretation

- Reporting only gross performance would overstate the value of the
  signal.
- Turnover is part of the strategy, not an implementation detail to be
  added after parameter selection.
- A slower signal can reduce costs but may react too late to market
  regime changes.
- The result motivates evaluating parameter sensitivity after costs,
  rather than selecting the best gross backtest first.

## Limitations

The current model is deliberately simple. It assumes a fixed linear
cost and does not model:

- time-varying bid-ask spreads;
- slippage conditional on volatility or liquidity;
- nonlinear market impact;
- delayed or partial execution;
- financing and borrowing costs;
- asset-specific fee schedules.

The 5-basis-point value is a modelling assumption, not an estimate of
the exact historical cost of trading this rule.
