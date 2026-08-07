from math import exp, sqrt

def _compute_crr_parameters(T, sigma, r, n_steps, q=0):
    delta_t = T / n_steps
    u = exp(sigma * sqrt(delta_t))
    d = 1 / u
    p = (exp((r - q) * delta_t) - d) / (u - d)
    if not 0 < p < 1:
        raise ValueError("CRR no-arbitrage condition requires 0 < p < 1")
    discount_factor = exp(-r * delta_t)
    return delta_t, u, d, p, discount_factor

def _validate_crr_inputs(S, K, T, sigma, n_steps):
    if sigma < 0:
        raise ValueError("sigma must be non-negative")

    if T < 0:
        raise ValueError("T must be non-negative")

    if S <= 0:
        raise ValueError("S must be strictly positive")

    if K <= 0:
        raise ValueError("K must be strictly positive")

    if isinstance(n_steps, bool) or not isinstance(n_steps, int) or n_steps <= 0:
        raise ValueError("n_steps must be a strictly positive integer")

def _crr_european_price(S, K, T, sigma, r, n_steps, option_type, q=0):
    _validate_crr_inputs(S, K, T, sigma, n_steps)

    if T == 0:
        if option_type == "call":
            return max(S - K, 0)
        if option_type == "put":
            return max(K - S, 0)

        raise ValueError("option_type must be 'call' or 'put'")

    if sigma == 0:
        if option_type == "call":
            return max(
                S * exp(-q * T) - K * exp(-r * T),
                0,
            )

        if option_type == "put":
            return max(
                K * exp(-r * T) - S * exp(-q * T),
                0,
            )

        raise ValueError("option_type must be 'call' or 'put'")

    _, u, d, p, discount_factor = _compute_crr_parameters(T, sigma, r, n_steps, q)
    option_values = []

    for j in range(n_steps + 1):
        terminal_spot = S * u**j * d ** (n_steps - j)

        if option_type == "call":
            payoff = max(terminal_spot - K, 0)
        elif option_type == "put":
            payoff = max(K - terminal_spot, 0)
        else:
            raise ValueError("option_type must be 'call' or 'put'")

        option_values.append(payoff)

    for i in range(n_steps - 1, -1, -1):
        for j in range(i + 1):
            option_values[j] = discount_factor * (
                (1 - p) * option_values[j]
                + p * option_values[j + 1]
            )

    return option_values[0]

def crr_european_call(S, K, T, sigma, r, n_steps, q=0):
    return _crr_european_price(
        S, K, T, sigma, r, n_steps, "call", q
    )

def crr_european_put(S, K, T, sigma, r, n_steps, q=0):
    return _crr_european_price(
        S, K, T, sigma, r, n_steps, "put", q
    )

def _crr_american_put_engine(S, K, T, sigma, r, n_steps, q=0, collect_nodes=False):
    _validate_crr_inputs(S, K, T, sigma, n_steps)

    if collect_nodes and (T == 0 or sigma == 0):
        raise ValueError("tree diagnostics require T > 0 and sigma > 0")

    if T == 0:
        return max(K - S, 0), None

    if sigma == 0:
        delta_t = T / n_steps
        best_exercise_value = 0

        for i in range(n_steps + 1):
            exercise_time = i * delta_t

            discounted_exercise_value = max(
                K * exp(-r * exercise_time)
                - S * exp(-q * exercise_time),
                0,
            )

            best_exercise_value = max(
                best_exercise_value,
                discounted_exercise_value,
            )

        return best_exercise_value, None

    delta_t, u, d, p, discount_factor = _compute_crr_parameters(T, sigma, r, n_steps, q)
    levels = (
        [[] for _ in range(n_steps + 1)]
        if collect_nodes else None
    )
    option_values = []

    for j in range(n_steps + 1):
        terminal_spot = S * u**j * d ** (n_steps - j)
        payoff = max(K - terminal_spot, 0)
        option_values.append(payoff)

        if levels is not None:
            levels[n_steps].append(
                {
                    "i": n_steps,
                    "j": j,
                    "time": T,
                    "spot": terminal_spot,
                    "exercise_value": payoff,
                    "continuation_value": None,
                    "option_value": payoff,
                    "decision": "maturity",
                }
            )

    for i in range(n_steps - 1, -1, -1):
        for j in range(i + 1):
            node_spot = S * u**j * d ** (i - j)

            continuation_value = discount_factor * (
                (1 - p) * option_values[j]
                + p * option_values[j + 1]
            )

            exercise_value = max(K - node_spot, 0)

            option_value = max(
                exercise_value,
                continuation_value,
            )

            option_values[j] = option_value

            if levels is not None:
                decision = (
                    "exercise"
                    if exercise_value > continuation_value
                    else "continue"
                )

                levels[i].append(
                    {
                        "i": i,
                        "j": j,
                        "time": i * delta_t,
                        "spot": node_spot,
                        "exercise_value": exercise_value,
                        "continuation_value": continuation_value,
                        "option_value": option_value,
                        "decision": decision,
                    }
                )

    return option_values[0], levels

def crr_american_put(S, K, T, sigma, r, n_steps, q=0):
    price, _ = _crr_american_put_engine(S, K, T, sigma, r, n_steps, q, collect_nodes=False)
    return price

def build_crr_american_put_tree(S, K, T, sigma, r, n_steps, q=0):
    price, levels = _crr_american_put_engine(S, K, T, sigma, r, n_steps, q=q, collect_nodes=True)
    return {
        "price": price,
        "levels": levels,
        "parameters": {
            "S": S,
            "K": K,
            "T": T,
            "sigma": sigma,
            "r": r,
            "q": q,
            "n_steps": n_steps,
        },
    }
