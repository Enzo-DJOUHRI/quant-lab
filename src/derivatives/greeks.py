from math import exp, sqrt
from scipy.stats import norm

from src.derivatives import black_scholes


def _validate_greek_inputs(S, K, T, sigma):
    black_scholes._validate_inputs(S, K, T, sigma=sigma)

    if T == 0:
        raise ValueError("T must be strictly positive")
    if sigma == 0:
        raise ValueError("sigma must be strictly positive")


def bsm_call_delta(S, K, T, sigma, r, q=0):
    _validate_greek_inputs(S, K, T, sigma=sigma)

    d1, _ = black_scholes._compute_d1_d2(S, K, T, sigma, r, q)

    call_delta = exp(-q * T) * norm.cdf(d1)

    return call_delta


def bsm_put_delta(S, K, T, sigma, r, q=0):
    _validate_greek_inputs(S, K, T, sigma=sigma)

    d1, _ = black_scholes._compute_d1_d2(S, K, T, sigma, r, q)

    put_delta = -exp(-q * T) * norm.cdf(-d1)

    return put_delta


def bsm_gamma(S, K, T, sigma, r, q=0):
    _validate_greek_inputs(S, K, T, sigma=sigma)

    d1, _ = black_scholes._compute_d1_d2(S, K, T, sigma, r, q)

    gamma = (exp(-q * T) * norm.pdf(d1)) / (S * sigma * sqrt(T))

    return gamma


def bsm_vega(S, K, T, sigma, r, q=0):
    _validate_greek_inputs(S, K, T, sigma=sigma)

    d1, _ = black_scholes._compute_d1_d2(S, K, T, sigma, r, q)

    vega = S * exp(-q * T) * norm.pdf(d1) * sqrt(T)

    return vega


def bsm_call_theta(S, K, T, sigma, r, q=0):
    _validate_greek_inputs(S, K, T, sigma=sigma)

    d1, d2 = black_scholes._compute_d1_d2(S, K, T, sigma, r, q)

    diffusion_term = (-S * exp(-q * T) * norm.pdf(d1) * sigma) / (2 * sqrt(T))

    dividend_term = q * S * exp(-q * T) * norm.cdf(d1)

    rate_term = r * K * exp(-r * T) * norm.cdf(d2)

    call_theta = diffusion_term + dividend_term - rate_term

    return call_theta


def bsm_put_theta(S, K, T, sigma, r, q=0):
    _validate_greek_inputs(S, K, T, sigma=sigma)

    d1, d2 = black_scholes._compute_d1_d2(S, K, T, sigma, r, q)

    diffusion_term = (-S * exp(-q * T) * norm.pdf(d1) * sigma) / (2 * sqrt(T))

    dividend_term = q * S * exp(-q * T) * norm.cdf(-d1)

    rate_term = r * K * exp(-r * T) * norm.cdf(-d2)

    put_theta = diffusion_term - dividend_term + rate_term

    return put_theta


def bsm_call_rho(S, K, T, sigma, r, q=0):
    _validate_greek_inputs(S, K, T, sigma=sigma)

    _, d2 = black_scholes._compute_d1_d2(S, K, T, sigma, r, q)

    call_rho = K * T * exp(-r * T) * norm.cdf(d2)

    return call_rho


def bsm_put_rho(S, K, T, sigma, r, q=0):
    _validate_greek_inputs(S, K, T, sigma=sigma)

    _, d2 = black_scholes._compute_d1_d2(S, K, T, sigma, r, q)

    put_rho = -K * T * exp(-r * T) * norm.cdf(-d2)

    return put_rho