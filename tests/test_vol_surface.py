import unittest

from src.derivatives import vol_surface


class TestVolatilitySurface(unittest.TestCase):
    def test_build_synthetic_surface_recovers_true_volatilities_across_grid(self):
        S = 100
        strikes = [90, 100, 110]
        maturities = [0.5, 1.0]
        r = 0.05
        q = 0.02
        atm_volatility = 0.25
        reference_maturity = 1.0
        slope = -0.10
        curvature = 0.50
        maturity_slope = 0.02

        surface_rows = vol_surface.build_synthetic_surface(S, strikes, maturities,
            r, atm_volatility, reference_maturity, q=q, slope=slope,
            curvature=curvature, maturity_slope=maturity_slope
        )

        self.assertEqual(
            len(surface_rows),
            len(strikes) * len(maturities),
        )

        for row in surface_rows:
            self.assertAlmostEqual(
                row["true_volatility"],
                row["implied_volatility"],
                delta=1e-8,
            )

    def test_maturity_slope_shifts_flat_surface_from_reference_maturity(self):
        S = 100
        strikes = [100]
        maturities = [0.5, 1.0, 2.0]
        r = 0.05
        q = 0.02
        atm_volatility = 0.25
        reference_maturity = 1.0
        slope = 0.0
        curvature = 0.0
        maturity_slope = 0.02

        expected_volatilities = [0.24, 0.25, 0.27]
        surface_rows = vol_surface.build_synthetic_surface(S, strikes, maturities,
                    r, atm_volatility, reference_maturity, q=q, slope=slope,
                    curvature=curvature, maturity_slope=maturity_slope
                )

        self.assertEqual(len(surface_rows), len(expected_volatilities))

        actual_maturities = [row["maturity"] for row in surface_rows]
        self.assertEqual(actual_maturities, maturities)

        for row, expected_volatility in zip(
            surface_rows, expected_volatilities
        ):
            self.assertAlmostEqual(
                row["true_volatility"],
                expected_volatility,
                places=12,
            )