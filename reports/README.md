# Research Reports

The root README explains what I want to build with Quant Lab. This folder
contains the work behind it: the theory I used, the experiments I ran, the
results I obtained and the limits I found.

Each report is linked to working code, a saved experiment or a clearly defined
method. Future ideas appear only when they help explain what is still missing.

## What each report should explain

A useful report should make the following points clear:

- the research question and the status of the work;
- the data, conventions and assumptions used;
- the method or implementation being evaluated;
- the source of numerical evidence;
- the interpretation of the result;
- the known limitations and what still needs to be checked before a stronger
  claim.

The right checks depend on the subject. Pricing reports use identities,
reference values and convergence. Alpha reports need causal signals,
transaction costs and eventually out-of-sample evidence. Engineering reports
explain data formats, reproducibility and known technical debt.

## Status labels

I use three labels to avoid presenting every document as equally mature:

| Label | Meaning |
| --- | --- |
| Validated module | The implementation is linked to explicit automated tests and numerical references |
| Current implementation reference | The document describes the current code behaviour, including untested or deferred parts |
| Historical research snapshot | The values are frozen exploratory outputs and may use earlier conventions |

These labels describe how the work was checked. They say nothing about future
returns or investment quality.

## Report index

| Axis | Report | Status | Purpose |
| --- | --- | --- | --- |
| Alpha research | [Strategy comparison](alpha_research/strategy_comparison.md) | Historical research snapshot | Compare passive, momentum and mean-reversion diagnostics without treating the initial ratio spread as pairs trading |
| Alpha research | [Momentum transaction costs](alpha_research/momentum_transaction_costs.md) | Historical research snapshot | Explain the linear cost model and measure its effect on a fixed momentum rule |
| Alpha research | [Momentum volatility targeting](alpha_research/momentum_volatility_targeting.md) | Historical research snapshot | Study dynamic exposure, turnover, costs and no-trade bands on SPY and BTC |
| Alpha research | [Performance metrics](alpha_research/performance_metrics.md) | Current implementation reference | Define the metric formulas, code semantics and known measurement caveats |
| Engineering | [Data and experiment workflow](engineering/data_and_experiment_workflow.md) | Current implementation reference | Document data schemas, caching, outputs, reproducibility and technical limits |
| Option pricing | [Vanilla option pricing](pricing/vanilla_option_pricing.md) | Validated module | Explain the Black-Scholes-Merton European call and put implementation |
| Option pricing | [Binomial option pricing](pricing/binomial_option_pricing.md) | Validated module | Explain CRR pricing, American early exercise, convergence and stopping diagnostics |
| Option sensitivities | [Black-Scholes-Merton Greeks](pricing/black_scholes_greeks.md) | Validated module | Derive, test and visualise Delta, Gamma, Vega, Theta and Rho |
| Option volatility | [Implied volatility, smiles and surfaces](pricing/implied_vol_smile_surface.md) | Current implementation reference | Validate IV inversion and synthetic volatility structures; preserve the market-data stage as the next checkpoint |

## How to read the numerical results

The CSV files in [`../results/`](../results/) preserve historical experiment
outputs. Some predate later corrections to crypto annualisation, the
risk-free-rate convention or the current package structure. A comparison is
valid only when the report identifies a common snapshot and common
conventions.

In particular:

- an in-sample result is a diagnostic, not evidence of a stable edge;
- a high Sharpe ratio does not repair data leakage or parameter selection;
- `n_trades` currently counts exposure-adjustment days, not completed round
  trips;
- pricing test counts describe software validation, not agreement with live
  option markets.

## Where to find the code and outputs

- [`../src/`](../src/) contains the implementations.
- [`../tests/`](../tests/) contains the current automated validation.
- [`../scripts/`](../scripts/) contains reproducible public entry points.
- [Data and experiment workflow](engineering/data_and_experiment_workflow.md)
  contains the current commands and artefact policy.

These backtests are research exercises, not live performance, investment
advice or forecasts. I will not draw a stronger Alpha Research conclusion
until the same ideas have passed a strict out-of-sample or walk-forward test.
