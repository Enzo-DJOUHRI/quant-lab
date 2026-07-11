import unittest

import numpy as np
import pandas as pd

from src.metrics import compute_metrics
from src.strategy import AlwaysLongStrategy, MomentumStrategy


def build_sample_data():
    prices = [100, 101, 102, 101, 100, 101, 103, 104, 103, 102, 103, 105]
    df = pd.DataFrame({"price": prices})
    df["return"] = df["price"].pct_change().fillna(0.0)
    df.index = pd.date_range("2024-01-01", periods=len(df), freq="D")
    return df


class TestMomentumTransactionCosts(unittest.TestCase):

    def test_trade_and_cost_columns_follow_formulas(self):
        data = build_sample_data()
        transaction_cost = 0.001
        result = MomentumStrategy(data, horizon=2, transaction_cost=transaction_cost).run()

        expected_trade_size = result["signal"].diff().abs().fillna(0)
        expected_cost_paid = transaction_cost * expected_trade_size
        expected_strategy_return = result["signal"] * result["return"] - expected_cost_paid

        np.testing.assert_allclose(result["trade_size"], expected_trade_size, rtol=0, atol=1e-12)
        np.testing.assert_allclose(result["transaction_cost_paid"], expected_cost_paid, rtol=0, atol=1e-12)
        self.assertNotIn("transaction_cost", result.columns)
        np.testing.assert_allclose(result["strategy_return"], expected_strategy_return, rtol=0, atol=1e-12)

    def test_metrics_include_trade_cost_and_time_in_market(self):
        data = build_sample_data()
        result = MomentumStrategy(data, horizon=2, transaction_cost=0.001).run()
        metrics = compute_metrics(result)

        expected_n_trades = int((result["trade_size"] > 0).sum())
        expected_total_cost = float(result["transaction_cost_paid"].sum())
        expected_time_in_market = float((result["signal"] != 0).mean())

        self.assertEqual(metrics["n_trades"], expected_n_trades)
        self.assertAlmostEqual(metrics["total_cost"], expected_total_cost, places=12)
        self.assertAlmostEqual(metrics["time_in_market"], expected_time_in_market, places=12)

    def test_zero_transaction_cost_keeps_net_equal_to_gross(self):
        data = build_sample_data()
        result = MomentumStrategy(data, horizon=2, transaction_cost=0.0).run()

        gross_return = result["signal"] * result["return"]
        np.testing.assert_allclose(result["transaction_cost_paid"], 0.0, rtol=0, atol=1e-12)
        np.testing.assert_allclose(result["strategy_return"], gross_return, rtol=0, atol=1e-12)

    def test_benchmark_metrics_are_exact_for_always_long(self):
        data = build_sample_data()
        result = AlwaysLongStrategy(data).run()
        metrics = compute_metrics(result, benchmark_return=data["return"])

        self.assertAlmostEqual(metrics["beta"], 1.0, places=12)
        self.assertAlmostEqual(metrics["alpha"], 0.0, places=12)
        self.assertAlmostEqual(metrics["tracking_error"], 0.0, places=12)
        self.assertTrue(np.isnan(metrics["information_ratio"]))


if __name__ == "__main__":
    unittest.main()
