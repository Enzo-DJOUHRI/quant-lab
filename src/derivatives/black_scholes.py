from math import exp, log, sqrt
from scipy.stats import norm

def _validate_inputs(S, K, T, sigma):
    if S <= 0:
        raise ValueError("S must be strictly positive")
    if K <= 0:
        raise ValueError("K must be strictly positive")
    if T < 0:
        raise ValueError("T must be non-negative")
    if sigma < 0:
        raise ValueError("sigma must be non-negative")


def _compute_d1_d2(S, K, T, sigma, r, q):
    period_vol = sigma * sqrt(T)
    d1 = (
        log(S / K) + (r - q + 0.5 * sigma**2) * T
    ) / period_vol
    d2 = d1 - period_vol
    return d1, d2


def bsm_call(S, K, T, sigma, r, q=0):
    """Return the Black-Scholes-Merton price of a European call."""

    _validate_inputs(S, K, T, sigma)

    if T == 0:
        return max(S - K, 0)

    if sigma == 0:
        return max(
            S * exp(-q * T) - K * exp(-r * T),
            0,
        )

    d1, d2 = _compute_d1_d2(S, K, T, sigma, r, q)
    call_price = (
        S * exp(-q * T) * norm.cdf(d1)
        - K * exp(-r * T) * norm.cdf(d2)
    )
    return call_price


def bsm_put(S, K, T, sigma, r, q=0):
    """Return the Black-Scholes-Merton price of a European put."""

    _validate_inputs(S, K, T, sigma)

    if T == 0:
        return max(K - S, 0)

    if sigma == 0:
        return max(
            K * exp(-r * T) - S * exp(-q * T),
            0,
        )

    d1, d2 = _compute_d1_d2(S, K, T, sigma, r, q)
    put_price = (
        K * exp(-r * T) * norm.cdf(-d2)
        - S * exp(-q * T) * norm.cdf(-d1)
    )
    return put_price
