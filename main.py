from src.data_loader import DataLoader
import src.strategy as strat
from src.metrics import compute_metrics
from src.plots import BacktestPlotter
from src.config import TICKERS, START_DATE, END_DATE, TRANSACTION_COST, RISK_FREE_RATE

if len(TICKERS) == 1:    
    loader = DataLoader(TICKERS, START_DATE, END_DATE)
    data = loader.load_mono()

    trading_days = 365 if "BTC" in TICKERS[0] or "ETH" in TICKERS[0] else 252

    alwayslong_strategy = strat.AlwaysLongStrategy(data)
    results_long = alwayslong_strategy.run()

    momentum_strategy = strat.MomentumStrategy(data, horizon=20, transaction_cost=TRANSACTION_COST)
    results_mom = momentum_strategy.run()

    momentum_vol_strategy = strat.MomentumVolTargetingStrategy(data,horizon=20,
                                                               vol_window=20,
                                                               target_vol=0.20,
                                                               max_leverage=2.0,
                                                               transaction_cost=TRANSACTION_COST,
                                                               rebal_threshold=0.05,
                                                               trading_days=trading_days)
    results_mom_vol_target = momentum_vol_strategy.run()

    mean_reversion_price_strategy = strat.MeanReversionPriceStrategy(data, z_threshold=2, rolling_days=20)
    results_mean_rev_price = mean_reversion_price_strategy.run()

    mean_reversion_return_strategy = strat.MeanReversionReturnStrategy(data, z_threshold=2, rolling_days=20)
    results_mean_rev_return = mean_reversion_return_strategy.run()

    print(results_mom[["signal", "trade_size", "transaction_cost_paid", "strategy_return"]].tail(10))
    print(results_mom["drawdown"].min())

    metrics_mom = compute_metrics(results_mom, risk_free_rate=RISK_FREE_RATE, trading_days=trading_days, benchmark_return=data["return"])
    metrics_mom_vol_target = compute_metrics(results_mom_vol_target, risk_free_rate=RISK_FREE_RATE, trading_days=trading_days, benchmark_return=data["return"])
    metrics_long = compute_metrics(results_long, risk_free_rate=RISK_FREE_RATE, trading_days=trading_days, benchmark_return=data["return"])
    metrics_mean_rev_price = compute_metrics(results_mean_rev_price, risk_free_rate=RISK_FREE_RATE, trading_days=trading_days, benchmark_return=data["return"])
    metrics_mean_rev_return = compute_metrics(results_mean_rev_return, risk_free_rate=RISK_FREE_RATE, trading_days=trading_days, benchmark_return=data["return"])

    print("=== Performance Metrics Long ===")
    for key, value in metrics_long.items():
        print(f"{key}: {value}")

    print("=== Performance Metrics Momentum ===")
    for key, value in metrics_mom.items():
        print(f"{key}: {value}")
    
    print("=== Performance Metrics Momentum Vol Targeting ===")
    for key, value in metrics_mom_vol_target.items():
        print(f"{key}: {value}")

    print("=== Performance Metrics Mean Reversion Price ===")
    for key, value in metrics_mean_rev_price.items():
        print(f"{key}: {value}")

    print("=== Performance Metrics Mean Reversion Return ===")
    for key, value in metrics_mean_rev_return.items():
        print(f"{key}: {value}")

    results_dict = {
        "Momentum 20": results_mom,
        "Momentum Vol Targeting 20": results_mom_vol_target,
        "AlwaysLong" : results_long,
        "Mean Reversion Price 20" : results_mean_rev_price,
        "Mean Reversion Return 20" : results_mean_rev_return
    }

    plotter = BacktestPlotter(results_dict)
    plotter.plot_equity()
    plotter.plot_drawdown()
    #plotter.plot_price_and_signal("Momentum 20")
    #plotter.plot_price_and_signal("Mean Reversion 20")

else:
    loader = DataLoader(TICKERS, START_DATE, END_DATE)
    data = loader.load_multi()

    print(data.tail(5))

    spread_mean_rev_strat = strat.SpreadMeanReversionStrategy(data, TICKERS[0], TICKERS[1], 2, 20)
    results_spread_mean_rev = spread_mean_rev_strat.run()
    metrics_spread_mean_rev = compute_metrics(results_spread_mean_rev)

    print("=== Performance Metrics Mean Reversion Return ===")
    for key, value in metrics_spread_mean_rev.items():
        print(f"{key}: {value}")
