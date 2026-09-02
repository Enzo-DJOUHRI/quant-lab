import unittest
from math import exp

from src.derivatives import vol_smile


class TestVolatilitySmile(unittest.TestCase):
    def test_log_forward_moneyness_is_zero_at_forward_strike(self):
        S = 100
        T = 1.0
        r = 0.05
        q = 0.02
        K = S * exp((r - q) * T)

        actual_moneyness = vol_smile.compute_log_forward_moneyness(S, K, T, r, q=q)
        expected_moneyness = 0.0

        self.assertAlmostEqual(
            actual_moneyness,
            expected_moneyness,
            places=12,
        )

    def test_log_forward_moneyness_has_expected_sign_around_forward(self):
        S = 100
        T = 1.0
        r = 0.05
        q = 0.02

        forward_price = S * exp((r - q) * T)
        strike_below = 0.90 * forward_price
        strike_above = 1.10 * forward_price

        moneyness_below = vol_smile.compute_log_forward_moneyness(S, strike_below, T, r, q=q)
        moneyness_above = vol_smile.compute_log_forward_moneyness(S, strike_above, T, r, q=q)

        self.assertLess(
            moneyness_below,
            0.0,
        )
        self.assertGreater(
            moneyness_above,
            0.0,
        )

    def test_log_forward_moneyness_rejects_non_finite_inputs(self):
        S = 100
        T = 1.0
        r = float("nan")
        q = 0.02
        K = 100

        with self.assertRaisesRegex(
            ValueError,
            "S, K, T, r and q must be finite",
        ):
            vol_smile.compute_log_forward_moneyness(S, K, T, r, q=q)

    def test_synthetic_flat_volatility_is_constant_across_moneyness(self):
        atm_volatility = 0.25
        log_moneyness_values = (-0.30, 0.0, 0.30)
        slope = 0.0
        curvature = 0.0

        expected_volatility = atm_volatility
        for log_moneyness in log_moneyness_values:
            actual_volatility = vol_smile.compute_synthetic_smile_volatility(
                log_moneyness,
                atm_volatility,
                slope=slope,
                curvature=curvature,
            )

            self.assertAlmostEqual(
                actual_volatility,
                expected_volatility,
                places=12,
            )

    def test_synthetic_smile_is_symmetric_around_atm(self):
        atm_volatility = 0.25
        curvature = 0.50
        slope = 0.0
        left_moneyness = -0.20
        right_moneyness = 0.20

        left_volatility = vol_smile.compute_synthetic_smile_volatility(left_moneyness, atm_volatility, slope=slope, curvature=curvature)
        right_volatility = vol_smile.compute_synthetic_smile_volatility(right_moneyness, atm_volatility, slope=slope, curvature=curvature)

        self.assertAlmostEqual(
            left_volatility,
            right_volatility,
            places=12,
        )

        self.assertAlmostEqual(
            left_volatility,
            0.27,
            places=12,
        )

    def test_synthetic_equity_skew_decreases_with_moneyness(self):
        atm_volatility = 0.25
        slope = -0.10
        curvature = 0.0
        left_moneyness = -0.20
        center_moneyness = 0.0
        right_moneyness = 0.20

        left_volatility = vol_smile.compute_synthetic_smile_volatility(left_moneyness, atm_volatility, slope=slope, curvature=curvature)
        center_volatility = vol_smile.compute_synthetic_smile_volatility(center_moneyness, atm_volatility, slope=slope, curvature=curvature)
        right_volatility = vol_smile.compute_synthetic_smile_volatility(right_moneyness, atm_volatility, slope=slope, curvature=curvature)

        self.assertGreater(
            left_volatility,
            center_volatility
        )

        self.assertGreater(
            center_volatility,
            right_volatility
        )

    def test_synthetic_smile_rejects_non_positive_volatility(self):
        log_moneyness = 0.50
        atm_volatility = 0.20
        slope = -0.50
        curvature = 0.0

        with self.assertRaisesRegex(
            ValueError,
            "synthetic volatility must be strictly positive",
        ):
            vol_smile.compute_synthetic_smile_volatility(log_moneyness, atm_volatility, slope, curvature)

    def test_build_synthetic_smile_recovers_true_volatilities(self):
        S = 100
        strikes = [80, 100, 120]
        T = 1.0
        r = 0.05
        q = 0.02
        atm_volatility = 0.25
        slope = -0.10
        curvature = 0.50

        smile_rows = vol_smile.build_synthetic_smile(
            S, strikes, T, r, atm_volatility,
            option_type="call", q=q,
            slope=slope, curvature=curvature,
        )

        self.assertEqual(len(smile_rows), len(strikes))

        actual_strikes = [row["strike"] for row in smile_rows]
        self.assertEqual(actual_strikes, strikes)

        for row in smile_rows:
            self.assertAlmostEqual(
                row["true_volatility"],
                row["implied_volatility"],
                delta=1e-8,
            )

    def test_build_synthetic_put_smile_recovers_true_volatility(self):
        S = 100
        strikes = [110]
        T = 1.0
        r = 0.05
        q = 0.02
        atm_volatility = 0.25
        slope = -0.10
        curvature = 0.50
        option_type = "put"

        smile_rows = vol_smile.build_synthetic_smile(
            S, strikes, T, r, atm_volatility,
            option_type=option_type, q=q,
            slope=slope, curvature=curvature,
        )

        self.assertEqual(len(smile_rows), 1)
        row = smile_rows[0]

        self.assertAlmostEqual(
            row["true_volatility"],
            row["implied_volatility"],
            delta=1e-8,
        )

    def test_build_synthetic_smile_rejects_invalid_option_type(self):
        S = 100
        strikes = [100]
        T = 1.0
        r = 0.05
        atm_volatility = 0.25
        option_type = "straddle"

        with self.assertRaisesRegex(
            ValueError,
            "option_type must be 'call' or 'put'",
        ):
            vol_smile.build_synthetic_smile(S, strikes, T, r, atm_volatility, option_type=option_type)