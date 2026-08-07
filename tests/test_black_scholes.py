import unittest
from math import exp

from src.derivatives import black_scholes

class TestBlackScholesMerton(unittest.TestCase):
    def test_hull_example_call(self):
        actual_price = black_scholes.bsm_call(42, 40, 0.5, 0.2, 0.1)
        expected_price = 4.759

        self.assertAlmostEqual(
            actual_price,
            expected_price,
            delta=1e-3,
        )

    def test_hull_example_put(self):
        actual_price = black_scholes.bsm_put(42, 40, 0.5, 0.2, 0.1)
        expected_price = 0.808

        self.assertAlmostEqual(
            actual_price,
            expected_price,
            delta=1e-3,
        )

    def test_put_call_parity(self):
        S = 42
        K = 40
        T = 0.5
        sigma = 0.2
        r = 0.1
        q = 0.03

        call_price = black_scholes.bsm_call(S, K, T, sigma, r, q)
        put_price = black_scholes.bsm_put(S, K, T, sigma, r, q)

        actual_parity = call_price - put_price
        expected_parity = S * exp(-q * T) - K * exp(-r * T)

        self.assertAlmostEqual(
            actual_parity,
            expected_parity,
            places=12,
        )

    def test_call_at_maturity_equals_intrinsic_value(self):
        actual_price = black_scholes.bsm_call(120, 100, 0, 0.2, 0.05)
        expected_price = 20

        self.assertEqual(actual_price, expected_price)

    def test_put_at_maturity_equals_intrinsic_value(self):
        actual_price = black_scholes.bsm_put(80, 100, 0, 0.2, 0.05)
        expected_price = 20

        self.assertEqual(actual_price, expected_price)

    def test_out_of_money_options_expire_worthless(self):
        call_price = black_scholes.bsm_call(80, 100, 0, 0.2, 0.05)
        put_price = black_scholes.bsm_put(120, 100, 0, 0.2, 0.05)

        self.assertEqual(call_price, 0)
        self.assertEqual(put_price, 0)

    def test_call_with_zero_volatility_uses_deterministic_payoff(self):
        actual_price = black_scholes.bsm_call(100, 100, 1, 0, 0.05)
        expected_price = 100 - 100 * exp(-0.05)

        self.assertAlmostEqual(
            actual_price,
            expected_price,
            places=12,
        )

    def test_put_with_zero_volatility_uses_deterministic_payoff(self):
        actual_price = black_scholes.bsm_put(100, 110, 1, 0, 0.05)
        expected_price = 110 * exp(-0.05) - 100

        self.assertAlmostEqual(
            actual_price,
            expected_price,
            places=12,
        )

    def test_negative_volatility_raises_value_error(self):
        with self.assertRaisesRegex(
            ValueError,
            "sigma must be non-negative",
        ):
            black_scholes.bsm_call(100, 100, 1, -0.2, 0.05)

    def test_negative_maturity_raises_value_error(self):
        with self.assertRaisesRegex(
            ValueError,
            "T must be non-negative",
        ):
            black_scholes.bsm_call(100, 100, -1, 0.2, 0.05)

    def test_non_positive_spot_raises_value_error(self):
        with self.assertRaisesRegex(
            ValueError,
            "S must be strictly positive",
        ):
            black_scholes.bsm_call(0, 100, 1, 0.2, 0.05)

    def test_non_positive_strike_raises_value_error(self):
        with self.assertRaisesRegex(
            ValueError,
            "K must be strictly positive",
        ):
            black_scholes.bsm_call(100, 0, 1, 0.2, 0.05)

    def test_prices_respect_no_arbitrage_bounds(self):
        S = 100
        K = 105
        T = 1
        sigma = 0.25
        r = 0.03
        q = 0.01

        call_price = black_scholes.bsm_call(S, K, T, sigma, r, q)
        put_price = black_scholes.bsm_put(S, K, T, sigma, r, q)

        discounted_spot = S * exp(-q * T)
        discounted_strike = K * exp(-r * T)

        call_lower_bound = max(discounted_spot - discounted_strike, 0)
        call_upper_bound = discounted_spot

        put_lower_bound = max(discounted_strike - discounted_spot, 0)
        put_upper_bound = discounted_strike

        self.assertGreaterEqual(call_price, call_lower_bound)
        self.assertLessEqual(call_price, call_upper_bound)
        self.assertGreaterEqual(put_price, put_lower_bound)
        self.assertLessEqual(put_price, put_upper_bound)

    def test_dividend_yield_changes_prices_in_expected_direction(self):
        S = 100
        K = 100
        T = 1
        sigma = 0.2
        r = 0.03
        q = 0.02

        call_without_dividend = black_scholes.bsm_call(S, K, T, sigma, r, 0)
        call_with_dividend = black_scholes.bsm_call(S, K, T, sigma, r, q)

        put_without_dividend = black_scholes.bsm_put(S, K, T, sigma, r, 0)
        put_with_dividend = black_scholes.bsm_put(S, K, T, sigma, r, q)

        self.assertLess(call_with_dividend, call_without_dividend)
        self.assertGreater(put_with_dividend, put_without_dividend)
