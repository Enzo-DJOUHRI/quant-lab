import unittest
from math import exp, log

from src.derivatives import binomial, black_scholes

class TestBinomialPricing(unittest.TestCase):
    def test_one_period_european_call_matches_manual_price(self):
        actual_price = binomial.crr_european_call(
            S=100,
            K=100,
            T=1,
            sigma=log(1.25),
            r=log(1.05),
            n_steps=1,
        )
        expected_price = 2500 / 189

        self.assertAlmostEqual(
            actual_price,
            expected_price,
            places=12,
        )

    def test_one_period_european_put_matches_manual_price(self):
        actual_price = binomial.crr_european_put(
            S=100,
            K=100,
            T=1,
            sigma=log(1.25),
            r=log(1.05),
            n_steps=1,
        )
        expected_price = 1600 / 189

        self.assertAlmostEqual(
            actual_price,
            expected_price,
            places=12,
        )

    def test_european_prices_respect_put_call_parity(self):
        S = 100
        K = 105
        T = 1
        sigma = 0.25
        r = 0.03
        q = 0.01
        n_steps = 100

        call_price = binomial.crr_european_call(
            S, K, T, sigma, r, n_steps, q
        )

        put_price = binomial.crr_european_put(
            S, K, T, sigma, r, n_steps, q
        )

        actual_parity = call_price - put_price
        expected_parity = S * exp(-q * T) - K * exp(-r * T)

        self.assertAlmostEqual(
            actual_parity,
            expected_parity,
            places=10,
        )

    def test_call_at_maturity_equals_intrinsic_value(self):
        actual_price = binomial.crr_european_call(
            S=120,
            K=100,
            T=0,
            sigma=0.20,
            r=0.05,
            n_steps=10,
        )
        expected_price = 20

        self.assertEqual(actual_price, expected_price)

    def test_put_at_maturity_equals_intrinsic_value(self):
        actual_price = binomial.crr_european_put(
            S=80,
            K=100,
            T=0,
            sigma=0.20,
            r=0.05,
            n_steps=10,
        )
        expected_price = 20

        self.assertEqual(actual_price, expected_price)

    def test_out_of_money_options_expire_worthless(self):
        call_price = binomial.crr_european_call(
            S=80,
            K=100,
            T=0,
            sigma=0.20,
            r=0.05,
            n_steps=10,
        )
        put_price = binomial.crr_european_put(
            S=120,
            K=100,
            T=0,
            sigma=0.20,
            r=0.05,
            n_steps=10,
        )

        self.assertEqual(call_price, 0)
        self.assertEqual(put_price, 0)

    def test_call_with_zero_volatility_uses_deterministic_payoff(self):
        actual_price = binomial.crr_european_call(
            S=100,
            K=100,
            T=1,
            sigma=0,
            r=0.05,
            n_steps=10,
        )
        expected_price = 100 - 100 * exp(-0.05)

        self.assertAlmostEqual(
            actual_price,
            expected_price,
            places=12,
        )

    def test_put_with_zero_volatility_uses_deterministic_payoff(self):
        actual_price = binomial.crr_european_put(
            S=100,
            K=110,
            T=1,
            sigma=0,
            r=0.05,
            n_steps=10,
        )
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
            binomial.crr_european_call(
                S=100,
                K=100,
                T=1,
                sigma=-0.20,
                r=0.05,
                n_steps=10,
            )

    def test_negative_maturity_raises_value_error(self):
        with self.assertRaisesRegex(
            ValueError,
            "T must be non-negative",
        ):
            binomial.crr_european_call(
                S=100,
                K=100,
                T=-1,
                sigma=0.20,
                r=0.05,
                n_steps=10,
            )

    def test_non_positive_spot_raises_value_error(self):
        with self.assertRaisesRegex(
            ValueError,
            "S must be strictly positive",
        ):
            binomial.crr_european_call(
                S=0,
                K=100,
                T=1,
                sigma=0.20,
                r=0.05,
                n_steps=10,
            )

    def test_non_positive_strike_raises_value_error(self):
        with self.assertRaisesRegex(
            ValueError,
            "K must be strictly positive",
        ):
            binomial.crr_european_call(
                S=100,
                K=0,
                T=1,
                sigma=0.20,
                r=0.05,
                n_steps=10,
            )

    def test_non_positive_n_steps_raises_value_error(self):
        with self.assertRaisesRegex(
            ValueError,
            "n_steps must be a strictly positive integer",
        ):
            binomial.crr_european_call(
                S=100,
                K=100,
                T=1,
                sigma=0.20,
                r=0.05,
                n_steps=0,
            )

    def test_non_integer_n_steps_raises_value_error(self):
        with self.assertRaisesRegex(
            ValueError,
            "n_steps must be a strictly positive integer",
        ):
            binomial.crr_european_call(
                S=100,
                K=100,
                T=1,
                sigma=0.20,
                r=0.05,
                n_steps=10.5,
            )

    def test_boolean_n_steps_raises_value_error(self):
        with self.assertRaisesRegex(
            ValueError,
            "n_steps must be a strictly positive integer",
        ):
            binomial.crr_european_call(
                S=100,
                K=100,
                T=1,
                sigma=0.20,
                r=0.05,
                n_steps=True,
            )

    def test_invalid_risk_neutral_probability_raises_value_error(self):
        with self.assertRaisesRegex(
            ValueError,
            "CRR no-arbitrage condition requires 0 < p < 1",
        ):
            binomial.crr_european_call(
                S=100,
                K=100,
                T=1,
                sigma=0.10,
                r=1.00,
                n_steps=1,
            )

    def test_negative_risk_neutral_probability_raises_value_error(self):
        with self.assertRaisesRegex(
            ValueError,
            "CRR no-arbitrage condition requires 0 < p < 1",
        ):
            binomial.crr_european_call(
                S=100,
                K=100,
                T=1,
                sigma=0.10,
                r=0,
                n_steps=1,
                q=1,
            )

    def test_european_call_is_close_to_bsm_with_many_steps(self):
        crr_price = binomial.crr_european_call(
            S=42,
            K=40,
            T=0.5,
            sigma=0.20,
            r=0.10,
            n_steps=500,
        )
        bsm_price = black_scholes.bsm_call(
            S=42,
            K=40,
            T=0.5,
            sigma=0.20,
            r=0.10,
        )

        self.assertAlmostEqual(
            crr_price,
            bsm_price,
            delta=1e-3,
        )

    def test_european_put_is_close_to_bsm_with_many_steps(self):
        crr_price = binomial.crr_european_put(
            S=42,
            K=40,
            T=0.5,
            sigma=0.20,
            r=0.10,
            n_steps=500,
        )
        bsm_price = black_scholes.bsm_put(
            S=42,
            K=40,
            T=0.5,
            sigma=0.20,
            r=0.10,
        )

        self.assertAlmostEqual(
            crr_price,
            bsm_price,
            delta=1e-3,
        )

    def test_one_period_american_put_chooses_immediate_exercise(self):
        actual_price = binomial.crr_american_put(
            S=100,
            K=120,
            T=1,
            sigma=log(1.25),
            r=log(1.05),
            n_steps=1,
        )
        expected_price = 20

        self.assertAlmostEqual(
            actual_price,
            expected_price,
            places=12,
        )

    def test_american_put_is_at_least_as_valuable_as_european_put(self):
        european_price = binomial.crr_european_put(
            S=100,
            K=110,
            T=1,
            sigma=0.20,
            r=0.05,
            n_steps=100,
        )
        american_price = binomial.crr_american_put(
            S=100,
            K=110,
            T=1,
            sigma=0.20,
            r=0.05,
            n_steps=100,
        )

        self.assertGreaterEqual(
            american_price,
            european_price,
        )

    def test_american_put_at_maturity_equals_intrinsic_value(self):
        actual_price = binomial.crr_american_put(
            S=80,
            K=100,
            T=0,
            sigma=0.20,
            r=0.05,
            n_steps=10,
        )
        expected_price = 20

        self.assertEqual(
            actual_price,
            expected_price,
        )

    def test_american_put_with_zero_volatility_chooses_best_exercise_date(self):
        actual_price = binomial.crr_american_put(
            S=100,
            K=110,
            T=1,
            sigma=0,
            r=0.05,
            n_steps=10,
        )
        expected_price = 10

        self.assertAlmostEqual(
            actual_price,
            expected_price,
            places=12,
        )

    def test_two_period_american_put_exercises_at_internal_node(self):
        actual_price = binomial.crr_american_put(
            S=100,
            K=120,
            T=2,
            sigma=log(1.25),
            r=log(1.05),
            n_steps=2,
        )
        expected_price = 764800 / 35721

        self.assertAlmostEqual(
            actual_price,
            expected_price,
            places=12,
        )

    def test_one_period_american_put_with_dividend_yield_matches_manual_price(self):
        actual_price = binomial.crr_american_put(
            S=100,
            K=100,
            T=1,
            sigma=log(1.25),
            r=log(1.05),
            n_steps=1,
            q=log(1.02),
        )
        expected_price = 10000 / 1071

        self.assertAlmostEqual(
            actual_price,
            expected_price,
            places=12,
        )

    def test_american_put_tree_records_early_exercise_policy(self):
        result = binomial.build_crr_american_put_tree(
            S=100,
            K=120,
            T=2,
            sigma=log(1.25),
            r=log(1.05),
            n_steps=2,
        )

        levels = result["levels"]

        self.assertEqual(result["parameters"]["K"], 120)
        self.assertAlmostEqual(
            result["price"],
            764800 / 35721,
            places=12,
        )
        self.assertEqual(
            [len(level) for level in levels],
            [1, 2, 3],
        )
        self.assertEqual(levels[0][0]["decision"], "continue")
        self.assertEqual(levels[1][0]["decision"], "exercise")
        self.assertEqual(levels[1][1]["decision"], "continue")
        self.assertEqual(
            [node["decision"] for node in levels[2]],
            ["maturity", "maturity", "maturity"],
        )

    def test_american_put_tree_rejects_degenerate_cases(self):
        error_message = (
            "tree diagnostics require T > 0 and sigma > 0"
        )

        with self.assertRaisesRegex(ValueError, error_message):
            binomial.build_crr_american_put_tree(
                S=100,
                K=100,
                T=0,
                sigma=0.20,
                r=0.05,
                n_steps=10,
            )

        with self.assertRaisesRegex(ValueError, error_message):
            binomial.build_crr_american_put_tree(
                S=100,
                K=100,
                T=1,
                sigma=0,
                r=0.05,
                n_steps=10,
            )

    def test_discounted_stock_is_martingale_under_risk_neutral_measure(self):
        S = 100
        T = 1
        sigma = 0.20
        r = 0.05
        q = 0.02
        n_steps = 4

        delta_t, u, d, p, _ = binomial._compute_crr_parameters(
            T, sigma, r, n_steps, q
        )

        expected_next_spot = (
            (1 - p) * S * d
            + p * S * u
        )

        discounted_expected_spot = (
            exp(-(r - q) * delta_t)
            * expected_next_spot
        )

        self.assertAlmostEqual(
            discounted_expected_spot,
            S,
            places=12,
        )

    def test_american_put_optimal_stopping_time_depends_on_path(self):
        tree = binomial.build_crr_american_put_tree(
            S=100,
            K=120,
            T=2,
            sigma=log(1.25),
            r=log(1.05),
            n_steps=2,
        )

        levels = tree["levels"]

        all_down_path = [
            levels[0][0],
            levels[1][0],
            levels[2][0],
        ]

        all_up_path = [
            levels[0][0],
            levels[1][1],
            levels[2][2],
        ]

        tau_star_down = next(
            node["time"]
            for node in all_down_path
            if node["decision"] in {"exercise", "maturity"}
        )

        tau_star_up = next(
            node["time"]
            for node in all_up_path
            if node["decision"] in {"exercise", "maturity"}
        )

        self.assertEqual(tau_star_down, 1)
        self.assertEqual(tau_star_up, 2)
