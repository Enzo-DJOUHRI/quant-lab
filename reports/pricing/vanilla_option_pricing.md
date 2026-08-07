# Vanilla Option Pricing

## Status

Status: **validated pricing module**.

The Black-Scholes-Merton implementation prices European calls and puts with a
continuous dividend yield. It is covered by 14 unit tests in
[`../../tests/test_black_scholes.py`](../../tests/test_black_scholes.py).

Related code and reports:

- [`../../src/derivatives/black_scholes.py`](../../src/derivatives/black_scholes.py)
- [Binomial option pricing](binomial_option_pricing.md)

European CRR pricing, the American put and early-exercise diagnostics are
covered separately in the binomial report.

## Research question

Under the Black-Scholes-Merton assumptions, what is the no-arbitrage time-zero
value of a European call or put, and which identities and boundary cases must
a correct implementation satisfy?

The module returns a theoretical premium per unit of underlying. It does not
apply an exchange contract multiplier or attempt to predict the future market
price of the option.

## Scope

The current module:

- prices European calls and puts in closed form;
- supports continuous dividend yield `q`, with `q = 0` by default;
- handles maturity and deterministic zero-volatility cases explicitly;
- validates spot, strike, maturity and volatility inputs.

Not implemented here:

- Greeks and finite-difference checks;
- implied-volatility inversion;
- volatility smiles and surfaces;
- American exercise;
- calibration to market option chains.

Public interface:

```python
bsm_call(S, K, T, sigma, r, q=0)
bsm_put(S, K, T, sigma, r, q=0)
```

## Inputs and conventions

| Symbol | Meaning |
| --- | --- |
| `S` | Current spot price of the underlying asset |
| `K` | Strike price |
| `T` | Time to maturity in years |
| `sigma` | Annualised model volatility of the underlying return |
| `r` | Annual continuously compounded risk-free rate |
| `q` | Annual continuous dividend yield |
| `N(x)` | Standard normal cumulative distribution function |

The option price is expressed in the same currency unit as `S` and `K`.
Rates, volatility and maturity must use consistent annual units.

Black-Scholes-Merton does not decide where `sigma` comes from. It can be an
assumed value, a historical estimate or a market-implied input. In practice,
market option pricing often starts from implied volatility, while an implied-
volatility solver inverts this same pricing function from an observed option
price. That inversion is a later module, not hidden inside the current pricer.

## Closed-form model

For positive `S`, `K`, `T` and `sigma`:

$$
d_1 = \frac{\ln(S/K) + \left(r-q+\frac{1}{2}\sigma^2\right)T}
{\sigma\sqrt{T}}
$$

$$
d_2 = d_1 - \sigma\sqrt{T}
$$

The European call value is:

$$
C = Se^{-qT}N(d_1) - Ke^{-rT}N(d_2)
$$

The European put value is:

$$
P = Ke^{-rT}N(-d_2) - Se^{-qT}N(-d_1)
$$

Put-call parity is:

$$
C-P = Se^{-qT} - Ke^{-rT}
$$

This identity is both a no-arbitrage relation and an implementation check.

## Financial interpretation

### Discounting

One monetary unit paid at maturity is worth `exp(-rT)` today under continuous
compounding. This is why the strike appears as `K * exp(-rT)`. The factor
`exp(-qT)` represents the continuous dividend carry associated with the
underlying.

### Why the real expected return does not appear

The option value comes from the cost of replicating its payoff, not from an
investor's forecast of the stock's real expected return `mu`. Delta hedging
removes the local random exposure in the Black-Scholes-Merton argument. By
no-arbitrage, the resulting locally riskless portfolio must earn the
risk-free rate.

Equivalently, valuation is performed under a risk-neutral probability
measure, where the ex-dividend underlying has drift `r - q`. This is a pricing
construction, not a statement that the real-world expected return equals
`r - q`.

### Volatility and maturity

Brownian uncertainty scales with the square root of time, so the standard
deviation of the log return over `T` is proportional to `sigma * sqrt(T)`.
This quantity therefore appears in both `d1` and `d2`.

Higher volatility widens the terminal-price distribution. Because vanilla
option payoffs are convex and cannot be negative, greater dispersion raises
both call and put values under the model, all else equal. Maturity also
changes discounting and dividend carry, so its total effect is not explained
by the square-root term alone.

## Boundary cases and no-arbitrage checks

At maturity:

$$
C = \max(S-K,0),
\qquad
P = \max(K-S,0)
$$

When `sigma = 0`, the discounted payoff is deterministic:

$$
C = \max\left(Se^{-qT}-Ke^{-rT},0\right)
$$

$$
P = \max\left(Ke^{-rT}-Se^{-qT},0\right)
$$

European prices must also satisfy:

$$
\max\left(Se^{-qT}-Ke^{-rT},0\right)
\leq C \leq Se^{-qT}
$$

$$
\max\left(Ke^{-rT}-Se^{-qT},0\right)
\leq P \leq Ke^{-rT}
$$

The lower bounds come from parity and non-negative option values. The upper
bounds follow because a call payoff cannot exceed the underlying payoff and a
put payoff cannot exceed the strike received at maturity.

## Model assumptions

The model assumes:

- no arbitrage;
- frictionless and sufficiently liquid markets;
- continuous trading and continuous price paths;
- geometric Brownian motion for the underlying;
- constant volatility, risk-free rate and dividend yield;
- no jumps;
- European exercise only at maturity.

These assumptions define the model. Passing software tests does not make them
true in observed markets.

## How I validated it

Run the current suite from the repository root:

```bash
python3 -m unittest discover -s tests
```

The 14 Black-Scholes-Merton tests cover:

| Check | What is tested |
| --- | --- |
| Published numerical reference | Hull Example 15.6 call and put |
| Structural identity | Put-call parity with non-zero dividend yield |
| Terminal condition | Intrinsic value at `T = 0` |
| Deterministic limit | Discounted payoff at `sigma = 0` |
| Input contract | Rejection of invalid `S`, `K`, `T` and `sigma` |
| No-arbitrage | European upper and lower bounds |
| Comparative statics | Dividend yield lowers the call and raises the put |

For `S = 42`, `K = 40`, `T = 0.5`, `sigma = 0.20`, `r = 0.10` and
`q = 0`:

| Option | Reference | Implementation |
| --- | ---: | ---: |
| European call | Approximately 4.759 | 4.759422 |
| European put | Approximately 0.808 | 0.808599 |

Together with the 29 binomial tests, the current pricing suite contains 43
passing tests.

## Interpretation and limitations

The module is a validated implementation of one model, not a complete option
valuation system. Real markets exhibit bid-ask spreads, discrete hedging,
jumps, stochastic volatility and volatility smiles or skews. An observed
market price can differ from the output because the assumptions or volatility
input differ, not only because one price is wrong.

The current derivation follows Hull's practitioner intuition. Rigorous
continuous-time foundations such as stochastic integration, equivalent
martingale measures and change of measure remain part of the later Shreve II
study.

## Current conclusion and next step

The European call and put pricer is complete for the scope described here. My
next step is to implement the Greeks and validate them with finite
differences, followed by implied-volatility inversion and volatility-smile
analysis. I will keep those as separate modules instead of quietly expanding
the scope of this one.

## References

- John C. Hull, *Options, Futures, and Other Derivatives*, Chapter 15.
- Black and Scholes (1973), "The Pricing of Options and Corporate
  Liabilities."
- Merton (1973), "Theory of Rational Option Pricing."
