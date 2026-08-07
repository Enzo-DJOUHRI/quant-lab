# Performance and Benchmark-Relative Metrics

## Status

Status: **current implementation reference**.

This report explains the formulas currently implemented in
[`../../src/alpha_research/metrics.py`](../../src/alpha_research/metrics.py).
It is a guide to reading the existing outputs, not a claim that the metric
layer is finished. The current public automated suite covers pricing;
dedicated Alpha Research metric tests will be rebuilt when that part of the
project is stabilised.

## Why these definitions matter

Metrics turn a full return path into a few numbers, but those numbers depend
on choices such as annualisation, benchmark, risk-free rate and the definition
of a trade. I keep those choices visible so that two experiments are not
compared under different conventions by mistake.

Let:

- `r_t` be the daily strategy return;
- `b_t` be the daily benchmark return;
- `N` be the annualisation factor;
- `rf` be the annual risk-free-rate input.

The current workflow uses `N = 252` for exchange-traded assets and `N = 365`
for BTC or ETH. The active risk-free rate is a simplified constant 2% annual
input.

## Absolute performance metrics

### Total return

```text
total_return = equity_last / equity_first - 1
```

This is the compounded change between the first and last recorded equity
values. The implementation does not yet prepend an explicit time-zero equity
row. Consequently, the first realised return can be omitted from this ratio
when `equity_first` differs from 1. This is a known measurement debt, not a
financial convention to reproduce in future modules.

### Annual return

```text
years = number_of_rows / N
annual_return = (equity_last / equity_first) ** (1 / years) - 1
```

This is a compound annual growth rate over the observed row count. It should
not be compared across assets unless the annualisation and calendar
conventions are consistent.

### Annual volatility

```text
daily_vol = sample_std(strategy_return)
annual_vol = daily_vol * sqrt(N)
```

Pandas uses sample standard deviation by default (`ddof=1`) here. Volatility
measures dispersion, not downside risk or the probability of loss.

### Sharpe ratio

```text
daily_rf = rf / N
sharpe = (mean(strategy_return) - daily_rf) / daily_vol * sqrt(N)
```

The risk-free rate is converted with a simple linear daily approximation.
Sharpe is undefined when daily volatility is zero. It assumes that mean and
standard deviation are informative summaries and does not account for skew,
tail risk or path dependence.

### Maximum drawdown

```text
running_peak_t = max(equity_0, ..., equity_t)
drawdown_t = equity_t / running_peak_t - 1
max_drawdown = min(drawdown_t)
```

Maximum drawdown records the worst observed peak-to-trough decline. It says
nothing by itself about recovery time or the frequency of smaller drawdowns.

## Execution and exposure metrics

| Metric key | Current calculation | Exact meaning |
| --- | --- | --- |
| `n_trades` | `sum(trade_size > 0)` | Number of exposure-adjustment days |
| `total_cost` | `sum(transaction_cost_paid)` | Sum of modelled return charges |
| `time_in_market` | `mean(signal != 0)` | Fraction of rows with an active directional signal |

`n_trades` is retained as the public metric key, but it is not a count of
completed round trips. For continuously sized strategies, a small rebalance
and a complete entry each count as one adjustment day.

`time_in_market` currently reads `signal`. For volatility targeting this
shows when the directional rule is active, not the magnitude of actual
`exposure`. Average absolute exposure and an exposure-based activity metric
are required for a complete risk interpretation.

## Benchmark-relative metrics

The underlying buy-and-hold return is currently used as benchmark when one is
provided.

### Beta

```text
beta = population_covariance(r_t, b_t)
       / population_variance(b_t)
```

Both covariance and variance use `ddof=0`, which preserves the identity
`beta = 1` when a return series is compared with itself. Beta is undefined
when benchmark variance is zero.

### Benchmark-adjusted alpha

```text
alpha = (mean(r_t) - beta * mean(b_t)) * N
```

This is the formula currently implemented. It does not subtract the
risk-free rate from strategy and benchmark returns, so it should be read as a
simplified benchmark-adjusted mean return rather than a fully specified CAPM
or Jensen alpha.

### Tracking error

```text
tracking_error = sample_std(r_t - b_t) * sqrt(N)
```

Tracking error measures the dispersion of active returns. A strategy can have
low total volatility and high tracking error if it behaves very differently
from its benchmark.

### Information ratio

```text
information_ratio = (annual_return_strategy - annual_return_benchmark)
                    / tracking_error
```

The numerator uses compounded annual returns, while tracking error is based
on daily active returns. The ratio is undefined when tracking error is zero.

## Sanity identities

When always-long returns are compared with the same asset return used as the
benchmark, the expected identities are:

```text
beta = 1
alpha = 0
tracking_error = 0
information_ratio = undefined
```

These identities test accounting consistency. They do not establish that the
benchmark is economically appropriate for every strategy.

## Reading the metrics together

Sharpe and information ratio answer different questions. Sharpe compares
excess return with total volatility; information ratio compares active return
with benchmark deviation. A low-beta strategy can therefore have a high
Sharpe and a negative information ratio when buy and hold dominates during a
strong market trend. There is no mathematical contradiction.

No single metric establishes robustness. I read return together with
volatility, drawdown, exposure, turnover, costs, benchmark sensitivity and
temporal validation.

## Known limitations and next tests

- Prepend and test an explicit initial equity value before the first return.
- Define an exposure-based `time_in_market` convention for continuous sizing.
- Distinguish adjustment count, turnover magnitude and completed round trips.
- Align strategy and benchmark indexes explicitly before relative metrics.
- Decide whether alpha should remain a simple diagnostic or adopt an excess-
  return regression with intercept and standard errors.
- Test zero-variance, missing-data and short-sample cases.
- Add synthetic identities for costs, compounding and annualisation.

Until these tests and conventions are fixed, I will use the metrics for
diagnosis and comparison, not for strong performance claims.
