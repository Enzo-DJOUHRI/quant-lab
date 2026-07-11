# Research Reports

This directory contains the public research record for Quant Lab. The
reports are organised by research axis rather than by development date.
Each document separates the research question, implementation,
empirical result and remaining limitations.

## Alpha research

| Report | Purpose |
| --- | --- |
| [Strategy comparison](alpha_research/strategy_comparison.md) | Compare passive exposure, momentum and mean-reversion baselines across assets |
| [Momentum transaction costs](alpha_research/momentum_transaction_costs.md) | Measure how a simple cost model changes a momentum backtest |
| [Momentum volatility targeting](alpha_research/momentum_volatility_targeting.md) | Study dynamic risk sizing, parameter sensitivity and no-trade bands |
| [Performance metrics](alpha_research/performance_metrics.md) | Define the absolute and benchmark-relative metrics used by the lab |

## Engineering

| Report | Purpose |
| --- | --- |
| [Data and experiment workflow](engineering/data_and_experiment_workflow.md) | Explain the current data cache, schemas, experiment outputs and engineering limits |

## Reading the results

The CSV files in [`../results/`](../results/) preserve historical
experiment outputs. Some were generated before later corrections to
crypto annualisation and the risk-free-rate convention. Each report
states which assumptions apply, and figures from different snapshots
should not be compared mechanically.

None of the reported backtests is presented as live performance or as
evidence of future profitability. The current research still lacks a
strict out-of-sample or walk-forward protocol.
