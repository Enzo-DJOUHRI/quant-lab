# Momentum With Volatility Targeting

## Research question

Can dynamic position sizing improve the risk profile of a momentum
signal, and how much turnover does that improvement require?

## Method

The direction remains the same long/flat momentum signal. Position
size changes with estimated annualised volatility:

```text
momentum_t = price_t / price_(t-horizon) - 1
annual_vol_t = rolling_std(returns, vol_window) * sqrt(trading_days)
position_size_t = min(target_vol / annual_vol_t, max_leverage)
target_exposure_t = signal_t * position_size_t
```

The direction and risk budget are therefore separate decisions. The
signal determines whether the strategy is invested, while volatility
targeting determines how much risk is taken.

Transaction costs are based on the change in executed exposure:

```text
trade_size_t = abs(exposure_t - exposure_(t-1))
transaction_cost_t = cost_rate * trade_size_t
```

## Parameter study

The first sweep tested 81 volatility-targeting configurations per
asset:

- momentum horizon: 10, 20 or 50 days;
- volatility window: 20, 60 or 120 days;
- target volatility: 10%, 15% or 20%;
- maximum leverage: 1.0, 1.5 or 2.0;
- transaction cost: 5 basis points.

The raw experiment table is available in
[`momentum_vol_targeting_grid_spy_btc.csv`](../../results/momentum_vol_targeting_grid_spy_btc.csv).

These CSV values are historical research snapshots generated before
the final risk-free-rate and crypto annualisation corrections. They
remain useful for comparing configurations within the same snapshot,
but should not be mixed with current README metrics.

## SPY findings

Historical representative configurations:

| Configuration | Annual return | Annual volatility | Maximum drawdown | Position adjustments |
| --- | ---: | ---: | ---: | ---: |
| Momentum, horizon 20 | 8.54% | 10.53% | -14.20% | 210 |
| Target 10%, window 20, leverage cap 2 | 9.18% | 8.12% | -12.63% | 1,791 |
| Target 20%, window 20, leverage cap 2 | 13.90% | 14.61% | -22.62% | 1,134 |
| Target 10%, window 60, leverage cap 1 | 5.61% | 6.87% | -9.76% | 1,358 |

Volatility targeting reduced risk for defensive targets and could
improve the historical return/risk ratio. The cost was much more
frequent rebalancing because exposure changed even when the directional
signal stayed constant.

## BTC findings

On the highly volatile BTC sample, targeting a 10% or 20% risk budget
cut exposure substantially. The strategy captured less of the large
uptrend but reduced volatility and drawdown. Under the current metric
convention, the default BTC experiment reports:

| Strategy | Annual return | Annual volatility | Sharpe | Maximum drawdown |
| --- | ---: | ---: | ---: | ---: |
| Momentum, horizon 20 | 88.77% | 48.87% | 1.50 | -52.63% |
| Momentum with 20% volatility target | 35.96% | 16.11% | 1.86 | -23.03% |

The comparison demonstrates the objective of volatility targeting: it
reshapes risk rather than necessarily maximising raw return.

## No-trade band

Daily volatility estimates create many small changes in target
exposure. A no-trade band was introduced:

```text
if abs(target_exposure_t - exposure_(t-1)) < threshold:
    exposure_t = exposure_(t-1)
else:
    exposure_t = target_exposure_t
```

The threshold was varied from 0 to 0.10. Raw results are stored in
[`momentum_vol_targeting_rebal_threshold_spy_btc.csv`](../../results/momentum_vol_targeting_rebal_threshold_spy_btc.csv).

For the SPY 10% target configuration, increasing the threshold from 0
to 0.10 reduced position-adjustment days from 1,791 to 461, while the
historical annual return remained close to 9.2% and drawdown remained
close to -12.6%. On BTC, turnover also fell sharply, but large
thresholds weakened volatility control more visibly.

This is an operational trade-off: a wider band reduces unnecessary
trading but allows actual exposure to drift further from its target.

## Main conclusions

- Volatility targeting can stabilise the risk taken by a directional
  strategy.
- The same target has very different economic effects on SPY and BTC.
- Parameter evaluation must include turnover and transaction costs.
- A no-trade band can remove many small rebalances without changing the
  directional signal.
- The best in-sample configuration is not automatically the most robust
  configuration.

## Limitations and next validation steps

- The parameter grid and evaluation use the same sample.
- Rolling volatility is backward-looking and can react after a shock.
- The cost model is fixed and linear.
- Leverage financing and execution constraints are omitted.
- Volatility floors, caps and smoother estimators such as EWMA remain
  to be studied.
- The next material step is a strict out-of-sample or walk-forward
  experiment with cost and parameter-stability stress tests.
