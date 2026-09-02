import unittest
from math import exp

from src.derivatives import black_scholes, implied_vol

class TestBlackScholesImpliedVolatility(unittest.TestCase):
    def test_bisection_recovers_synthetic_call_volatility(self):
        S = 42
        K = 40
        T = 0.5
        sigma_true = 0.20
        r = 0.10
        q = 0.0

        observed_price = black_scholes.bsm_call(S, K, T, sigma_true, r, q)
        recovered_sigma = implied_vol.bsm_implied_vol_bisection(observed_price, S, K, T, r, option_type="call", q=q)

        self.assertAlmostEqual(
            sigma_true,
            recovered_sigma,
            delta=1e-8,
        )

    def test_bisection_recovers_synthetic_put_volatility_with_dividend(self):
        S = 95
        K = 100
        T = 1.25
        sigma_true = 0.35
        r = 0.04
        q = 0.02

        observed_price = black_scholes.bsm_put(S, K, T, sigma_true, r, q=q)
        recovered_sigma = implied_vol.bsm_implied_vol_bisection(observed_price, S, K, T, r, option_type="put", q=q)

        self.assertAlmostEqual(
            sigma_true,
            recovered_sigma,
            delta=1e-8,
        )

    def test_bisection_returns_zero_at_call_lower_bound(self):
        S = 100
        K = 100
        T = 1.0
        r = 0.05
        q = 0.02

        observed_price = max(S * exp(-q * T) - K * exp(-r * T), 0)
        recovered_sigma = implied_vol.bsm_implied_vol_bisection(observed_price, S, K, T, r, option_type="call", q=q)

        self.assertEqual(0.0, recovered_sigma)

    def test_bisection_rejects_price_below_call_lower_bound(self):
        S = 100
        K = 100
        T = 1.0
        r = 0.05
        q = 0.02

        lower_bound = max(S * exp(-q * T) - K * exp(-r * T), 0)
        observed_price = lower_bound - 0.01

        with self.assertRaisesRegex(
            ValueError,
            "price is below the no-arbitrage lower bound",
        ):
            implied_vol.bsm_implied_vol_bisection(
                observed_price, S, K, T, r, option_type="call", q=q
            )

    def test_bisection_rejects_call_price_at_upper_bound(self):
        S = 100
        K = 100
        T = 1.0
        r = 0.05
        q = 0.02

        upper_bound = S * exp(-q * T)
        observed_price = upper_bound

        with self.assertRaisesRegex(
            ValueError,
            "price must be strictly below the no-arbitrage upper bound",
        ):
            implied_vol.bsm_implied_vol_bisection(
                observed_price, S, K, T, r, option_type="call", q=q
            )

    def test_bisection_rejects_interval_that_does_not_bracket_root(self):
        S = 100
        K = 100
        T = 1.0
        sigma_true = 0.30
        r = 0.05
        q = 0.02

        observed_price = black_scholes.bsm_call(S, K, T, sigma_true, r, q)

        with self.assertRaisesRegex(
            ValueError,
            "volatility interval does not bracket the implied volatility",
        ):
            implied_vol.bsm_implied_vol_bisection(
                observed_price, S, K, T, r, option_type="call", q=q, sigma_low=0.0, sigma_high=0.20
            )

    def test_bisection_raises_when_max_iterations_is_reached(self):
        S = 100
        K = 100
        T = 1.0
        sigma_true = 0.30
        r = 0.05
        q = 0.02

        observed_price = black_scholes.bsm_call(S, K, T, sigma_true, r, q)

        with self.assertRaisesRegex(
            RuntimeError,
            "bisection did not converge within max_iterations",
        ):
            implied_vol.bsm_implied_vol_bisection(
                observed_price, S, K, T, r,
                option_type="call", q=q,
                sigma_low=0.0, sigma_high=1.0,
                price_tolerance=1e-12, vol_tolerance=1e-12,
                max_iterations=1
            )

    def test_bisection_returns_sigma_at_lower_bracket_endpoint(self):
        S = 100
        K = 105
        T = 0.75
        sigma_true = 0.25
        r = 0.03
        q = 0.01

        observed_price = black_scholes.bsm_call(S, K, T, sigma_true, r, q)
        recovered_sigma = implied_vol.bsm_implied_vol_bisection(
                observed_price, S, K, T, r,
                option_type="call", q=q,
                sigma_low=0.25, sigma_high=1.0,
            )

        self.assertEqual(sigma_true, recovered_sigma)

    def test_bisection_returns_sigma_at_upper_bracket_endpoint(self):
        S = 100
        K = 105
        T = 0.75
        sigma_true = 0.25
        r = 0.03
        q = 0.01

        observed_price = black_scholes.bsm_call(S, K, T, sigma_true, r, q)
        recovered_sigma = implied_vol.bsm_implied_vol_bisection(
                observed_price, S, K, T, r,
                option_type="call", q=q,
                sigma_low=0.0, sigma_high=0.25,
            )

        self.assertEqual(sigma_true, recovered_sigma)

    def test_bisection_rejects_invalid_option_type(self):
        price = 10.0
        S = 100
        K = 100
        T = 1.0
        r = 0.05

        with self.assertRaisesRegex(
            ValueError,
            "option_type must be 'call' or 'put'",
        ):
            implied_vol.bsm_implied_vol_bisection(
                price, S, K, T, r,
                option_type="straddle"
            )

    def test_bisection_rejects_invalid_volatility_interval(self):
        price = 10.0
        S = 100
        K = 100
        T = 1.0
        r = 0.05
        sigma_low = 0.50
        sigma_high = 0.50

        with self.assertRaisesRegex(
            ValueError,
            "sigma_high must be greater than sigma_low",
        ):
            implied_vol.bsm_implied_vol_bisection(
                price, S, K, T, r,
                option_type="call",
                sigma_low=sigma_low, sigma_high=sigma_high
            )

    def test_bisection_rejects_zero_maturity(self):
        price = 10.0
        S = 100
        K = 100
        T = 0.0
        r = 0.05

        with self.assertRaisesRegex(
            ValueError,
            "T must be strictly positive",
        ):
            implied_vol.bsm_implied_vol_bisection(
                price, S, K, T, r,
                option_type="call",
            )

    def test_bisection_rejects_non_positive_tolerances(self):
        price = 10.0
        S = 100
        K = 100
        T = 1.0
        r = 0.05

        with self.assertRaisesRegex(
            ValueError,
            "price_tolerance must be strictly positive",
        ):
            implied_vol.bsm_implied_vol_bisection(
                price, S, K, T, r,
                option_type="call",
                price_tolerance=0.0
            )

        with self.assertRaisesRegex(
            ValueError,
            "vol_tolerance must be strictly positive",
        ):
            implied_vol.bsm_implied_vol_bisection(
                price, S, K, T, r,
                option_type="call",
                vol_tolerance=0.0
            )

    def test_bisection_rejects_invalid_max_iterations(self):
        price = 10.0
        S = 100
        K = 100
        T = 1.0
        r = 0.05

        with self.assertRaisesRegex(
            ValueError,
            "max_iterations must be a strictly positive integer",
        ):
            implied_vol.bsm_implied_vol_bisection(
                price, S, K, T, r,
                option_type="call",
                max_iterations=0
            )

        with self.assertRaisesRegex(
            ValueError,
            "max_iterations must be a strictly positive integer",
        ):
            implied_vol.bsm_implied_vol_bisection(
                price, S, K, T, r,
                option_type="call",
                max_iterations=True
            )

    def test_guarded_newton_recovers_synthetic_call_volatility(self):
        S = 42
        K = 40
        T = 0.5
        sigma_true = 0.27
        r = 0.10
        q = 0.0
        initial_sigma = 0.20

        observed_price = black_scholes.bsm_call(S, K, T, sigma_true, r, q)
        recovered_sigma = implied_vol.bsm_implied_vol_newton(observed_price, S, K, T, r, option_type="call", q=q, initial_sigma=initial_sigma)

        self.assertAlmostEqual(
            sigma_true,
            recovered_sigma,
            delta=1e-8,
        )

    def test_guarded_newton_recovers_synthetic_put_volatility_with_dividend(self):
        S = 95
        K = 100
        T = 1.25
        sigma_true = 0.35
        r = 0.04
        q = 0.02
        initial_sigma = 0.20

        observed_price = black_scholes.bsm_put(S, K, T, sigma_true, r, q)
        recovered_sigma = implied_vol.bsm_implied_vol_newton(observed_price, S, K, T, r, option_type="put", q=q, initial_sigma=initial_sigma)

        self.assertAlmostEqual(
            sigma_true,
            recovered_sigma,
            delta=1e-8,
        )

    def test_guarded_newton_uses_midpoint_when_vega_is_below_tolerance(self):
        S = 100
        K = 100
        T = 1.0
        sigma_true = 0.27
        r = 0.05
        q = 0.02
        initial_sigma = 0.40
        sigma_low = 0.0
        sigma_high = 1.0
        vega_tolerance = 1e6

        observed_price = black_scholes.bsm_call(S, K, T, sigma_true, r, q)
        recovered_sigma = implied_vol.bsm_implied_vol_newton(
            observed_price, S, K, T, r,
            option_type="call", q=q,
            initial_sigma=initial_sigma,
            sigma_low=sigma_low, sigma_high=sigma_high,
            vega_tolerance=vega_tolerance,
        )

        self.assertAlmostEqual(
            sigma_true,
            recovered_sigma,
            delta=1e-8,
        )

    def test_guarded_newton_agrees_with_bisection(self):
        S = 110
        K = 100
        T = 0.75
        sigma_true = 0.32
        r = 0.03
        q = 0.01
        initial_sigma = 0.15
        sigma_low, sigma_high = 0.0, 1.0

        observed_price = black_scholes.bsm_call(S, K, T, sigma_true, r, q)
        bisection_sigma = implied_vol.bsm_implied_vol_bisection(
            observed_price, S, K, T, r,
            option_type="call", q=q,
            sigma_low=sigma_low, sigma_high=sigma_high)
        newton_sigma = implied_vol.bsm_implied_vol_newton(
            observed_price, S, K, T, r,
            option_type="call", q=q,
            initial_sigma=initial_sigma,
            sigma_low=sigma_low, sigma_high=sigma_high)

        self.assertAlmostEqual(
            bisection_sigma,
            newton_sigma,
            delta=1e-8,
        )

    def test_guarded_newton_rejects_initial_sigma_outside_bracket(self):
        S = 100
        K = 100
        T = 1.0
        r = 0.05
        sigma_true = 0.20
        sigma_low = 0.0
        sigma_high = 1.0
        initial_sigma = 1.0

        observed_price = black_scholes.bsm_call(S, K, T, sigma_true, r)
        with self.assertRaisesRegex(
            ValueError,
            "initial_sigma must lie strictly inside the volatility interval",
        ):
            implied_vol.bsm_implied_vol_newton(
                observed_price, S, K, T, r,
                option_type="call",
                initial_sigma=initial_sigma,
                sigma_low=sigma_low, sigma_high=sigma_high
            )

    def test_guarded_newton_rejects_non_positive_vega_tolerance(self):
        S = 100
        K = 100
        T = 1.0
        r = 0.05
        sigma_true = 0.20
        initial_sigma = 0.20
        sigma_low = 0.0
        sigma_high = 1.0
        vega_tolerance = 0.0

        observed_price = black_scholes.bsm_call(S, K, T, sigma_true, r)
        with self.assertRaisesRegex(
            ValueError,
            "vega_tolerance must be strictly positive",
        ):
            implied_vol.bsm_implied_vol_newton(
                observed_price, S, K, T, r,
                option_type="call",
                initial_sigma=initial_sigma,
                sigma_low=sigma_low, sigma_high=sigma_high,
                vega_tolerance=vega_tolerance
            )

    def test_guarded_newton_raises_when_max_iterations_is_reached(self):
        S = 100
        K = 100
        T = 1.0
        r = 0.05
        q = 0.02
        sigma_true = 0.40
        initial_sigma = 0.20
        sigma_low, sigma_high = 0.0, 1.0
        price_tolerance = 1e-14
        vol_tolerance = 1e-14
        max_iterations = 1

        observed_price = black_scholes.bsm_call(S, K, T, sigma_true, r, q=q)
        with self.assertRaisesRegex(
            RuntimeError,
            "guarded Newton did not converge within max_iterations",
        ):
            implied_vol.bsm_implied_vol_newton(
                observed_price, S, K, T, r,
                option_type="call",
                initial_sigma=initial_sigma,
                sigma_low=sigma_low, sigma_high=sigma_high,
                price_tolerance=price_tolerance,
                vol_tolerance=vol_tolerance,
                max_iterations=max_iterations
            )