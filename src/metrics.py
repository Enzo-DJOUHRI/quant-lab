import numpy as np

def compute_metrics(result, risk_free_rate=0.0, trading_days=252, benchmark_return=None):
    """
    result: DataFrame containing at least strategy_return, equity and drawdown.
    returns: dictionary of performance and optional benchmark metrics.
    """

    # Total compounded return.
    equity_0 = result["equity"].iloc[0]
    equity_n = result["equity"].iloc[-1]
    final_return = equity_n / equity_0 - 1

    # Annualised compounded return.
    n_days = result.shape[0]
    years = n_days / trading_days
    annual_return = (equity_n / equity_0) ** (1 / years) - 1

    # Daily and annualised volatility.
    daily_vol = result["strategy_return"].std()
    annual_vol = np.sqrt(trading_days) * daily_vol

    # Annualised Sharpe ratio.
    daily_mean = result["strategy_return"].mean()
    if daily_vol == 0:
        annual_sharpe = np.nan
    else:
        daily_rf = risk_free_rate / trading_days
        annual_sharpe = (daily_mean - daily_rf) / daily_vol * np.sqrt(trading_days)


    # Maximum drawdown.
    max_drawdown = result["drawdown"].min()

    metrics = {
        "total_return": final_return,
        "annual_return": annual_return,
        "annual_vol": annual_vol,
        "sharpe": annual_sharpe,
        "max_drawdown": max_drawdown
    }

    # Add execution and exposure diagnostics when available.
    if "trade_size" in result.columns:
        metrics["n_trades"] = int((result["trade_size"] > 0).sum())

    if "transaction_cost_paid" in result.columns:
        metrics["total_cost"] = result["transaction_cost_paid"].sum()

    if "signal" in result.columns:
        metrics["time_in_market"] = (result["signal"] != 0).mean()
    
    if benchmark_return is not None:
        bench = benchmark_return
        strat = result["strategy_return"]

        benchmark_var = np.var(bench, ddof=0)
        if benchmark_var == 0:
            beta = np.nan
            alpha = np.nan
        else:
            beta = np.cov(strat, bench, ddof=0)[0, 1] / benchmark_var
            alpha = (strat.mean() - beta * bench.mean()) * trading_days
        
        tracking_error = (strat - bench).std() * np.sqrt(trading_days)
        
        bench_annual = (1 + bench).prod() ** (1 / years) - 1
        if tracking_error == 0:
            information_ratio = np.nan
        else:
            information_ratio = (annual_return - bench_annual) / tracking_error
        
        metrics["alpha"] = alpha
        metrics["beta"] = beta
        metrics["tracking_error"] = tracking_error
        metrics["information_ratio"] = information_ratio

    return metrics
