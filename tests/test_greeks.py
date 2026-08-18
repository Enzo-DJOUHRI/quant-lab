import unittest
from math import exp

from src.derivatives import greeks, black_scholes

class TestBlackScholesMertonGreeks(unittest.TestCase):
    def test_call_delta_matches_reference_value(self):
        actual_delta = greeks.bsm_call_delta(42, 40, 0.5, 0.2, 0.1)
        expected_delta = 0.779131290942669

        self.assertAlmostEqual(
            actual_delta,
            expected_delta,
            delta=1e-9,
        )

    def test_call_delta_matches_central_finite_difference(self):
        S = 42
        K = 40
        T = 0.5
        sigma = 0.2
        r = 0.1
        q = 0.03
        h = 1e-4

        analytical_delta = greeks.bsm_call_delta(S, K, T, sigma, r, q)

        numerical_delta = (
            black_scholes.bsm_call(S + h, K, T, sigma, r, q)
            - black_scholes.bsm_call(S - h, K, T, sigma, r, q)
        ) / (2 * h)

        self.assertAlmostEqual(
            analytical_delta,
            numerical_delta,
            delta=1e-8,
        )

    def test_put_delta_matches_reference_value(self):
        actual_delta = greeks.bsm_put_delta(42, 40, 0.5, 0.2, 0.1)
        expected_delta = -0.220868709057331

        self.assertAlmostEqual(
            actual_delta,
            expected_delta,
            delta=1e-9,
        )

    def test_put_delta_matches_central_finite_difference(self):
        S = 42
        K = 40
        T = 0.5
        sigma = 0.2
        r = 0.1
        q = 0.03
        h = 1e-4

        analytical_delta = greeks.bsm_put_delta(S, K, T, sigma, r, q)

        numerical_delta = (
            black_scholes.bsm_put(S + h, K, T, sigma, r, q)
            - black_scholes.bsm_put(S - h, K, T, sigma, r, q)
        ) / (2 * h)

        self.assertAlmostEqual(
            analytical_delta,
            numerical_delta,
            delta=1e-8,
        )

    def test_call_and_put_deltas_respect_put_call_parity(self):
        S = 42
        K = 40
        T = 0.5
        sigma = 0.2
        r = 0.1
        q = 0.03

        actual_delta_call = greeks.bsm_call_delta(S, K, T, sigma, r, q)
        actual_delta_put = greeks.bsm_put_delta(S, K, T, sigma, r, q)

        actual_difference = actual_delta_call - actual_delta_put
        expected_difference = exp(-q * T)

        self.assertAlmostEqual(
            actual_difference,
            expected_difference,
            places=12,
        )

    def test_delta_rejects_zero_maturity(self):
        with self.assertRaisesRegex(
            ValueError,
            "T must be strictly positive",
        ):
            greeks.bsm_call_delta(100, 100, 0, 0.2, 0.05)

    def test_delta_rejects_zero_volatility(self):
        with self.assertRaisesRegex(
            ValueError,
            "sigma must be strictly positive",
        ):
            greeks.bsm_call_delta(100, 100, 1, 0, 0.05)

    def test_gamma_matches_reference_value(self):
        actual_gamma = greeks.bsm_gamma(42, 40, 0.5, 0.2, 0.1)
        expected_gamma = 0.049962670405912

        self.assertAlmostEqual(
            actual_gamma,
            expected_gamma,
            places=12,
        )

    def test_gamma_matches_call_central_finite_difference(self):
        S = 42
        K = 40
        T = 0.5
        sigma = 0.2
        r = 0.1
        q = 0.03
        h = 0.01

        analytical_gamma = greeks.bsm_gamma(S, K, T, sigma, r, q)

        finite_difference_gamma = (
            black_scholes.bsm_call(S + h, K, T, sigma, r, q)
            - 2 * black_scholes.bsm_call(S, K, T, sigma, r, q)
            + black_scholes.bsm_call(S - h, K, T, sigma, r, q)
        ) / h ** 2

        self.assertAlmostEqual(
            analytical_gamma,
            finite_difference_gamma,
            delta=1e-7,
        )

    def test_gamma_matches_put_central_finite_difference(self):
        S = 42
        K = 40
        T = 0.5
        sigma = 0.2
        r = 0.1
        q = 0.03
        h = 0.01

        analytical_gamma = greeks.bsm_gamma(S, K, T, sigma, r, q)

        finite_difference_gamma = (
            black_scholes.bsm_put(S + h, K, T, sigma, r, q)
            - 2 * black_scholes.bsm_put(S, K, T, sigma, r, q)
            + black_scholes.bsm_put(S - h, K, T, sigma, r, q)
        ) / h ** 2

        self.assertAlmostEqual(
            analytical_gamma,
            finite_difference_gamma,
            delta=1e-7,
        )

    def test_vega_matches_reference_value(self):
        actual_vega = greeks.bsm_vega(42, 40, 0.5, 0.2, 0.1)
        expected_vega = 8.813415059602853

        self.assertAlmostEqual(
            actual_vega,
            expected_vega,
            places=12,
        )

    def test_vega_matches_call_central_finite_difference(self):
        S = 42
        K = 40
        T = 0.5
        sigma = 0.2
        r = 0.1
        q = 0.03
        h = 1e-5

        analytical_vega = greeks.bsm_vega(S, K, T, sigma, r, q)

        numerical_vega = (
            black_scholes.bsm_call(S, K, T, sigma + h, r, q)
            - black_scholes.bsm_call(S, K, T, sigma - h, r, q)
        ) / (2 * h)

        self.assertAlmostEqual(
            analytical_vega,
            numerical_vega,
            delta=1e-7,
        )

    def test_vega_matches_put_central_finite_difference(self):
        S = 42
        K = 40
        T = 0.5
        sigma = 0.2
        r = 0.1
        q = 0.03
        h = 1e-5

        analytical_vega = greeks.bsm_vega(S, K, T, sigma, r, q)

        numerical_vega = (
            black_scholes.bsm_put(S, K, T, sigma + h, r, q)
            - black_scholes.bsm_put(S, K, T, sigma - h, r, q)
        ) / (2 * h)

        self.assertAlmostEqual(
            analytical_vega,
            numerical_vega,
            delta=1e-7,
        )

    def test_vega_is_positive_for_long_vanilla_option(self):
        S = 100
        K = 100
        T = 1
        sigma = 0.2
        r = 0.05

        actual_vega = greeks.bsm_vega(S, K, T, sigma, r)

        self.assertGreater(actual_vega, 0)

    def test_call_theta_matches_reference_value(self):
        actual_theta = greeks.bsm_call_theta(42, 40, 0.5, 0.2, 0.1)
        expected_theta = -4.559092194592627

        self.assertAlmostEqual(
            actual_theta,
            expected_theta,
            places=12,
        )

    def test_put_theta_matches_reference_value(self):
        actual_theta = greeks.bsm_put_theta(42, 40, 0.5, 0.2, 0.1)
        expected_theta = -0.7541744965897708

        self.assertAlmostEqual(
            actual_theta,
            expected_theta,
            places=12,
        )

    def test_call_theta_matches_central_finite_difference(self):
        S = 42
        K = 40
        T = 0.5
        sigma = 0.2
        r = 0.1
        q = 0.03
        h = 1e-5

        analytical_theta = greeks.bsm_call_theta(S, K, T, sigma, r, q)

        numerical_theta = (
            black_scholes.bsm_call(S, K, T - h, sigma, r, q)
            - black_scholes.bsm_call(S, K, T + h, sigma, r, q)
        ) / (2 * h)

        self.assertAlmostEqual(
            analytical_theta,
            numerical_theta,
            delta=1e-7,
        )

    def test_put_theta_matches_central_finite_difference(self):
        S = 42
        K = 40
        T = 0.5
        sigma = 0.2
        r = 0.1
        q = 0.03
        h = 1e-5

        analytical_theta = greeks.bsm_put_theta(S, K, T, sigma, r, q)

        numerical_theta = (
            black_scholes.bsm_put(S, K, T - h, sigma, r, q)
            - black_scholes.bsm_put(S, K, T + h, sigma, r, q)
        ) / (2 * h)

        self.assertAlmostEqual(
            analytical_theta,
            numerical_theta,
            delta=1e-7,
        )

    def test_call_and_put_thetas_respect_put_call_parity(self):
        S = 42
        K = 40
        T = 0.5
        sigma = 0.2
        r = 0.1
        q = 0.03

        actual_theta_call = greeks.bsm_call_theta(S, K, T, sigma, r, q)
        actual_theta_put = greeks.bsm_put_theta(S, K, T, sigma, r, q)

        actual_difference = actual_theta_call - actual_theta_put
        expected_difference = q * S * exp(-q * T) - r * K * exp(-r * T)

        self.assertAlmostEqual(
            actual_difference,
            expected_difference,
            places=12,
        )

    def test_call_rho_matches_reference_value(self):
        actual_rho = greeks.bsm_call_rho(42, 40, 0.5, 0.2, 0.1)
        expected_rho = 13.982045913360283

        self.assertAlmostEqual(
            actual_rho,
            expected_rho,
            places=12,
        )

    def test_put_rho_matches_reference_value(self):
        actual_rho = greeks.bsm_put_rho(42, 40, 0.5, 0.2, 0.1)
        expected_rho = -5.0425425766539975

        self.assertAlmostEqual(
            actual_rho,
            expected_rho,
            places=12,
        )

    def test_call_rho_matches_central_finite_difference(self):
        S = 42
        K = 40
        T = 0.5
        sigma = 0.2
        r = 0.1
        q = 0.03
        h = 1e-5

        analytical_rho = greeks.bsm_call_rho(S, K, T, sigma, r, q)

        numerical_rho = (
            black_scholes.bsm_call(S, K, T, sigma, r + h, q)
            - black_scholes.bsm_call(S, K, T, sigma, r - h, q)
        ) / (2 * h)

        self.assertAlmostEqual(
            analytical_rho,
            numerical_rho,
            delta=1e-7,
        )

    def test_put_rho_matches_central_finite_difference(self):
        S = 42
        K = 40
        T = 0.5
        sigma = 0.2
        r = 0.1
        q = 0.03
        h = 1e-5

        analytical_rho = greeks.bsm_put_rho(S, K, T, sigma, r, q)

        numerical_rho = (
            black_scholes.bsm_put(S, K, T, sigma, r + h, q)
            - black_scholes.bsm_put(S, K, T, sigma, r - h, q)
        ) / (2 * h)

        self.assertAlmostEqual(
            analytical_rho,
            numerical_rho,
            delta=1e-7,
        )

    def test_call_and_put_rhos_respect_put_call_parity(self):
        S = 42
        K = 40
        T = 0.5
        sigma = 0.2
        r = 0.1
        q = 0.03

        actual_rho_call = greeks.bsm_call_rho(S, K, T, sigma, r, q)
        actual_rho_put = greeks.bsm_put_rho(S, K, T, sigma, r, q)

        actual_difference = actual_rho_call - actual_rho_put
        expected_difference = K * T * exp(-r * T)

        self.assertAlmostEqual(
            actual_difference,
            expected_difference,
            places=12,
        )

    def test_call_rho_is_positive_and_put_rho_is_negative(self):
        S = 100
        K = 100
        T = 1
        sigma = 0.2
        r = 0.05

        actual_rho_call = greeks.bsm_call_rho(S, K, T, sigma, r)
        actual_rho_put = greeks.bsm_put_rho(S, K, T, sigma, r)

        self.assertGreater(actual_rho_call, 0)
        self.assertGreater(actual_rho_call, 0)