from math import exp, isfinite, log

from src.derivatives import black_scholes, implied_vol


def compute_log_forward_moneyness(S, K, T, r, q=0):
    if not all(isfinite(value) for value in (S, K, T, r, q)):
        raise ValueError("S, K, T, r and q must be finite")

    black_scholes._validate_inputs(S, K, T, sigma=0)

    forward_price = S * exp((r - q) * T)
    log_moneyness = log(K / forward_price)

    return log_moneyness


def compute_synthetic_smile_volatility(
    log_moneyness,
    atm_volatility,
    slope=0.0,
    curvature=0.0,
):
    if not all(
        isfinite(value)
        for value in (log_moneyness, atm_volatility, slope, curvature)
    ):
        raise ValueError(
            "log_moneyness, atm_volatility, slope and curvature must be finite"
        )

    if atm_volatility <= 0:
        raise ValueError("atm_volatility must be strictly positive")

    synthetic_volatility = (
        atm_volatility
        + slope * log_moneyness
        + curvature * (log_moneyness**2)
    )

    if synthetic_volatility <= 0:
        raise ValueError("synthetic volatility must be strictly positive")

    return synthetic_volatility


def build_synthetic_smile(
    S, strikes, T, r, atm_volatility,
    option_type="call", q=0,
    slope=0.0, curvature=0.0,
):
    if option_type == "call":
        pricing_function = black_scholes.bsm_call
    elif option_type == "put":
        pricing_function = black_scholes.bsm_put
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    smile_rows = []

    for K in strikes:
        log_moneyness = compute_log_forward_moneyness(S, K, T, r, q=q)
        true_volatility = compute_synthetic_smile_volatility(
            log_moneyness,
            atm_volatility,
            slope=slope,
            curvature=curvature,
        )
        option_price = pricing_function(S, K, T, true_volatility, r, q=q)
        implied_volatility = implied_vol.bsm_implied_vol_newton(
            option_price, S, K, T, r,
            option_type=option_type, q=q,
            initial_sigma=atm_volatility,
        )
        row = {
            "strike": K,
            "log_moneyness": log_moneyness,
            "true_volatility": true_volatility,
            "option_price": option_price,
            "implied_volatility": implied_volatility,
        }
        smile_rows.append(row)

    return smile_rows
