from math import exp, isfinite

from src.derivatives import black_scholes, greeks


def _validate_iv_inputs(
    price, S, K, T, r,
    option_type="call", q=0,
    sigma_low=0.0, sigma_high=5.0,
    price_tolerance=1e-8, vol_tolerance=1e-8,
    max_iterations=100,
):
    if not all(isfinite(value) for value in (price, S, K, T, r, q)):
        raise ValueError("price, S, K, T, r and q must be finite")

    black_scholes._validate_inputs(S, K, T, sigma=0)

    if T == 0:
        raise ValueError("T must be strictly positive")

    if price < 0:
        raise ValueError("price must be non-negative")

    if not all(
        isfinite(value)
        for value in (sigma_low, sigma_high, price_tolerance, vol_tolerance)
    ):
        raise ValueError("solver parameters must be finite")

    if sigma_low < 0:
        raise ValueError("sigma_low must be non-negative")

    if sigma_high <= sigma_low:
        raise ValueError("sigma_high must be greater than sigma_low")

    if price_tolerance <= 0:
        raise ValueError("price_tolerance must be strictly positive")

    if vol_tolerance <= 0:
        raise ValueError("vol_tolerance must be strictly positive")

    if (
        isinstance(max_iterations, bool)
        or not isinstance(max_iterations, int)
        or max_iterations <= 0
    ):
        raise ValueError("max_iterations must be a strictly positive integer")

    if option_type == "call":
        pricing_function = black_scholes.bsm_call

    elif option_type == "put":
        pricing_function = black_scholes.bsm_put

    else:
        raise ValueError("option_type must be 'call' or 'put'")

    return pricing_function


def _compute_no_arbitrage_bounds(S, K, T, r, q, option_type):
    discounted_spot = S * exp(-q * T)
    discounted_strike = K * exp(-r * T)
    if option_type == "call":
        lower_bound = max(discounted_spot - discounted_strike, 0)
        upper_bound = discounted_spot
    elif option_type == "put":
        lower_bound = max(discounted_strike - discounted_spot, 0)
        upper_bound = discounted_strike
    return lower_bound, upper_bound


def bsm_implied_vol_bisection(
    price, S, K, T, r,
    option_type="call", q=0,
    sigma_low=0.0, sigma_high=5.0,
    price_tolerance=1e-8, vol_tolerance=1e-8,
    max_iterations=100,
):
    pricing_function = _validate_iv_inputs(
        price,
        S,
        K,
        T,
        r,
        option_type=option_type,
        q=q,
        sigma_low=sigma_low,
        sigma_high=sigma_high,
        price_tolerance=price_tolerance,
        vol_tolerance=vol_tolerance,
        max_iterations=max_iterations,
    )

    lower_bound, upper_bound = _compute_no_arbitrage_bounds(
        S,
        K,
        T,
        r,
        q,
        option_type,
    )

    if abs(price - lower_bound) <= price_tolerance:
        return 0.0

    if price < lower_bound:
        raise ValueError("price is below the no-arbitrage lower bound")

    if price >= upper_bound:
        raise ValueError("price must be strictly below the no-arbitrage upper bound")

    price_at_low = pricing_function(S, K, T, sigma_low, r, q)
    price_at_high = pricing_function(S, K, T, sigma_high, r, q)

    if abs(price_at_low - price) <= price_tolerance:
        return sigma_low

    elif abs(price_at_high - price) <= price_tolerance:
        return sigma_high

    elif price_at_low > price or price_at_high < price:
        raise ValueError("volatility interval does not bracket the implied volatility")

    for _ in range(max_iterations):
        sigma_mid = (sigma_high + sigma_low) / 2
        price_at_mid = pricing_function(S, K, T, sigma_mid, r, q)
        price_residual = price_at_mid - price

        if (
            abs(price_residual) <= price_tolerance
            or (sigma_high - sigma_low) / 2 <= vol_tolerance
        ):
            return sigma_mid
        elif price_residual >= 0:
            sigma_high = sigma_mid
        else:
            sigma_low = sigma_mid

    raise RuntimeError("bisection did not converge within max_iterations")


def bsm_implied_vol_newton(
    price, S, K, T, r,
    option_type="call", q=0,
    initial_sigma=0.20,
    sigma_low=0.0, sigma_high=5.0,
    price_tolerance=1e-8, vol_tolerance=1e-8,
    vega_tolerance=1e-10, max_iterations=100,
):
    pricing_function = _validate_iv_inputs(
        price,
        S,
        K,
        T,
        r,
        option_type=option_type,
        q=q,
        sigma_low=sigma_low,
        sigma_high=sigma_high,
        price_tolerance=price_tolerance,
        vol_tolerance=vol_tolerance,
        max_iterations=max_iterations,
    )

    if not all(isfinite(value) for value in (initial_sigma, vega_tolerance)):
        raise ValueError("Newton parameters must be finite")

    if sigma_low >= initial_sigma or initial_sigma >= sigma_high:
        raise ValueError("initial_sigma must lie strictly inside the volatility interval")

    if vega_tolerance <= 0:
        raise ValueError("vega_tolerance must be strictly positive")

    lower_bound, upper_bound = _compute_no_arbitrage_bounds(
        S,
        K,
        T,
        r,
        q=q,
        option_type=option_type,
    )

    if abs(price - lower_bound) <= price_tolerance:
        return 0.0

    if price < lower_bound:
        raise ValueError("price is below the no-arbitrage lower bound")

    if price >= upper_bound:
        raise ValueError("price must be strictly below the no-arbitrage upper bound")

    price_at_low = pricing_function(S, K, T, sigma_low, r, q)
    price_at_high = pricing_function(S, K, T, sigma_high, r, q)

    if abs(price_at_low - price) <= price_tolerance:
        return sigma_low

    elif abs(price_at_high - price) <= price_tolerance:
        return sigma_high

    elif price_at_low > price or price_at_high < price:
        raise ValueError("volatility interval does not bracket the implied volatility")

    sigma_current = initial_sigma

    for _ in range(max_iterations):
        price_at_current = pricing_function(S, K, T, sigma_current, r, q=q)
        price_residual = price_at_current - price

        if abs(price_residual) <= price_tolerance:
            return sigma_current
        elif price_residual >= 0:
            sigma_high = sigma_current
        else:
            sigma_low = sigma_current

        sigma_mid = (sigma_low + sigma_high) / 2

        if (sigma_high - sigma_low) / 2 <= vol_tolerance:
            return sigma_mid

        vega_at_current = greeks.bsm_vega(S, K, T, sigma=sigma_current, r=r, q=q)

        if vega_at_current > vega_tolerance:
            sigma_candidate = sigma_current - price_residual / vega_at_current
        else:
            sigma_candidate = sigma_mid

        if (
            not isfinite(sigma_candidate)
            or sigma_low >= sigma_candidate
            or sigma_candidate >= sigma_high
        ):
            sigma_candidate = sigma_mid

        if abs(sigma_candidate - sigma_current) <= vol_tolerance:
            return sigma_candidate
        else:
            sigma_current = sigma_candidate

    raise RuntimeError("guarded Newton did not converge within max_iterations")
