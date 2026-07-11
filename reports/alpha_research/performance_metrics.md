# Performance and Benchmark-Relative Metrics

## Purpose

This report defines the metrics currently produced by Quant Lab and the
questions they answer. Metric definitions are part of the research
method: changing an annualisation factor, benchmark or risk-free-rate
assumption can change the interpretation of a backtest.

## Absolute performance metrics

Let `r_t` be daily strategy returns and `N` the number of observations
per year.

| Metric | Definition | Research question |
| --- | --- | --- |
| Total return | `equity_end / equity_start - 1` | How much did capital change over the full sample? |
| Annual return | Compound growth annualised over the sample | What was the equivalent yearly growth rate? |
| Annual volatility | `std(r_t) * sqrt(N)` | How dispersed were returns? |
| Sharpe ratio | `(mean(r_t) - rf/N) / std(r_t) * sqrt(N)` | Was excess return sufficient for total risk? |
| Maximum drawdown | Minimum of `equity / running_peak - 1` | What was the largest peak-to-trough loss? |

The current convention uses 252 days for exchange-traded assets and
365 days for BTC or ETH. The risk-free rate is currently a constant 2%
placeholder.

## Execution and exposure metrics

| Metric | Definition | Research question |
| --- | --- | --- |
| Number of trades | Days where `trade_size > 0` | How frequently did exposure change? |
| Total cost | Sum of charged transaction costs | How much return was removed by the simplified cost model? |
| Time in market | Fraction of days with a non-zero signal | How often was directional market risk active? |

For continuous position sizing, the number of adjustment days should
not be confused with the number of discrete round trips. Trade size and
turnover magnitude provide additional context.

## Benchmark-relative metrics

Let `b_t` be the return of the underlying buy-and-hold benchmark.

### Beta

```text
beta = cov(r_t, b_t) / var(b_t)
```

Beta estimates the strategy's sensitivity to benchmark movements. A
long/flat timing rule should generally have a beta below one because it
is not continuously invested.

### Alpha

```text
annual_alpha = (mean(r_t) - beta * mean(b_t)) * N
```

Alpha is the annualised residual return after accounting for estimated
benchmark exposure. Positive in-sample alpha is not evidence of a
persistent edge.

### Tracking error

```text
tracking_error = std(r_t - b_t) * sqrt(N)
```

Tracking error measures how differently the strategy behaves from the
benchmark.

### Information ratio

```text
information_ratio = (annual_return_strategy - annual_return_benchmark)
                    / tracking_error
```

The information ratio asks whether active return compensated for active
risk. It is undefined when tracking error is zero.

## Sanity conditions

When always-long returns are compared with the same asset return used
as benchmark, the expected identities are:

```text
beta = 1
alpha = 0
tracking_error = 0
information_ratio = undefined
```

The covariance and variance calculations use the same population
normalisation (`ddof=0`) so that the beta identity holds up to floating
point precision.

## Interpretation example

For the current BTC volatility-targeting experiment:

- Sharpe is positive and high relative to the other current rules;
- beta is low because exposure is reduced and the strategy is often
  flat;
- tracking error is high because the strategy behaves very differently
  from buy and hold;
- information ratio is negative because BTC buy and hold earned a much
  higher raw return over this strongly rising sample.

There is no contradiction. Sharpe evaluates absolute return per unit of
total risk, while information ratio evaluates relative return per unit
of benchmark deviation.

## Limitations

- A constant 2% risk-free rate is only a simplified placeholder for a
  period in which short rates changed materially.
- Alpha and beta are sample estimates and may vary through time.
- The underlying asset is not always the most informative benchmark for
  a dynamically risk-scaled strategy.
- Metrics summarise a return path but do not replace distributional,
  regime and out-of-sample analysis.
