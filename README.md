# Quant Lab

Quant Lab is my long-term personal project for learning quantitative finance by
building and testing things myself. I use it to turn ideas from derivatives,
probability, market data and systematic investing into code that I can
understand, challenge and explain.

The aim is not to present a finished trading platform or collect as many
strategies as possible. I want to build a smaller set of solid research
projects with clear assumptions, reproducible results and honest limitations.
Code shows what I implemented, tests show what I checked, and reports explain
what the results do and do not mean.

## Research principles

- Start with a precise financial or statistical question.
- Define data conventions and causality before modelling.
- Compare each method with a simple baseline or reference value.
- Validate assumptions, identities, edge cases and numerical behaviour.
- Separate exploratory results from robust out-of-sample evidence.
- Measure costs, uncertainty and failure modes, not only performance.
- Explain what a result demonstrates and what it does not demonstrate.
- Prefer a small, completed research core to many unfinished extensions.

## Books and theoretical foundations

The project develops alongside my theoretical work. These books guide the
order of the projects, and each one supports a specific part of the code and
its validation.

| Book | Current status | Role in Quant Lab |
| --- | --- | --- |
| John C. Hull, *Options, Futures, and Other Derivatives* | In progress; chapters 14-15 completed | Market conventions, Black-Scholes-Merton, Greeks, volatility, numerical methods and risk |
| Steven E. Shreve, *Stochastic Calculus for Finance I: The Binomial Asset Pricing Model* | Chapters 1-5 completed | No-arbitrage, replication, risk-neutral pricing, conditional expectations and American exercise in discrete time |
| Steven E. Shreve, *Stochastic Calculus for Finance II: Continuous-Time Models* | Planned | Continuous-time stochastic calculus and a more rigorous foundation for advanced pricing models |

These statuses refer only to material I have actually worked through. Shreve
II is included as the next theoretical step; I have not studied it yet.

## Research directions

| Direction | Main purpose | Roadmap position |
| --- | --- | --- |
| Data and research infrastructure | Data provenance, schemas, quality checks, point-in-time causality and reproducible experiments | Cross-cutting foundation |
| Derivatives pricing and volatility | Vanilla and American option pricing, Greeks, implied volatility and numerical methods | Current focus |
| Simulation and risk | GBM, Monte Carlo, uncertainty, variance reduction, VaR, Expected Shortfall and stress testing | Next core |
| Alpha research | Robust backtesting, transaction costs, exposure, sensitivity and out-of-sample validation | Existing research base to stabilise |
| Time series and pairs research | Stationarity, forecasting, cointegration and dependence; pairs trading is a planned extension, not a current implementation | Planned |
| Portfolio construction | ETF diversification, Markowitz baselines, risk contributions and walk-forward evaluation | Planned |
| Machine learning for finance | Time-aware validation, calibrated baselines and economic evaluation beyond prediction scores | Later |
| Market microstructure | Event data, causal as-of lookups, L3/L2 order-book reconstruction, liquidity metrics and RFQ research | Future Python reference branch |
| Market making and execution | Fill models, inventory risk, adverse selection and event-driven evaluation | Future, after the microstructure core |
| C++ quantitative engineering | Order-book replay, matching, market-data pipelines, execution systems and reproducible latency benchmarks | Future, after validated Python references |
| Research interface | A public research console exposing only completed and documented modules | Transversal, built progressively |

These labels describe direction and priority. They are not claims that every
listed module already exists.

## Development sequence

I plan to develop the lab in the following order because each step provides
tools needed by the next one:

1. complete the derivatives path through Greeks, implied volatility and Monte
   Carlo;
2. build the risk and empirical-volatility foundations;
3. stabilise the historical backtester before making new Alpha claims;
4. continue Alpha research, portfolio construction and time-series work with
   proper temporal validation;
5. introduce machine learning only after reliable data, baselines and
   evaluation protocols exist;
6. build market-data cleaning, causal as-of tools, LOB and RFQ references in
   Python;
7. use those Python references to study C++ trading systems, execution and
   market making without sacrificing correctness for premature optimisation.

## Design decisions

### Keep plans separate from evidence

This README explains where the lab is going. Derivations, test plans, figures,
numerical results and limitations belong in the relevant research reports and
modules.

### Use the right validation for each problem

Pricing work needs identities, reference values and numerical convergence.
Strategy research needs correct chronology, costs, benchmarks and
out-of-sample testing. Risk models need coverage analysis and stress tests.
Systems work needs invariants, differential tests, profiling and a documented
latency protocol.

### Use Python as the reference before C++

Python remains the readable reference for pricing and event-driven models. C++
becomes useful when data structures, memory behaviour, throughput or latency
are part of the research question. A faster implementation has little value
until it agrees with a validated reference.

### Put data quality before model complexity

Raw observations, cleaning decisions, quality flags and usable datasets must
remain distinguishable. No future information may enter a decision through a
join, fill or feature calculation. This applies to historical strategies,
risk, machine learning and event-level microstructure research.

### Publish completed work, not empty promises

I do not create empty packages simply to make the project look larger. A module
is presented as completed only when its theory, implementation, validation and
limitations can be inspected together.

## Repository responsibilities

| Location | Responsibility |
| --- | --- |
| [`src/alpha_research/`](src/alpha_research/) | Systematic research code and its data workflow |
| [`src/derivatives/`](src/derivatives/) | Pricing and numerical-finance code |
| [`tests/`](tests/) | Executable validation and regression checks |
| [`reports/`](reports/README.md) | Theory, methodology, experiments, figures, interpretation and limitations |
| [`results/`](results/) | Reproducible experiment tables and research artefacts |
| [`scripts/`](scripts/) | Explicit entry points for regenerating public artefacts |
| [`reports/engineering/`](reports/engineering/) | Data, architecture and reproducibility decisions |

New top-level packages will be introduced only when their corresponding
research axis contains working code.

## Navigation

- Start with the [research report index](reports/README.md) for completed
  analyses and their limitations.
- Read the [data and experiment workflow](reports/engineering/data_and_experiment_workflow.md)
  for the current engineering conventions.
- Inspect [`src/`](src/) for implementation and [`tests/`](tests/) for the
  associated validation.
- Use [`results/`](results/) only together with the report that defines the
  relevant assumptions and conventions.

## Scope and interpretation

Quant Lab is an educational and research repository. It does not execute live
orders, provide investment advice or claim that an in-sample backtest is a
tradable edge. The objective is to understand why a method may work, identify
how it can fail and make the remaining uncertainty explicit.
