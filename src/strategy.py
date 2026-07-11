import numpy as np

class Strategy:

    def __init__(self, data):
        self.data = data.copy()

    def run(self):
        raise NotImplementedError


class AlwaysLongStrategy(Strategy):

    def run(self):
        self.data["signal"] = 1
        self.data["strategy_return"] = self.data["signal"] * self.data["return"]
        self.data["equity"] = (1 + self.data["strategy_return"]).cumprod()
        self.data["peak"] = self.data["equity"].cummax()
        self.data["drawdown"] = (self.data["equity"] - self.data["peak"]) / self.data["peak"]
        return self.data

class MomentumStrategy(Strategy):

    def __init__(self, data, horizon, transaction_cost = 0.0):
        super().__init__(data)  #réutiliser le constructeur parent
        self.horizon = horizon
        self.transaction_cost = transaction_cost

    def run(self):
        self.data["momentum"] = self.data["price"] / self.data["price"].shift(self.horizon) - 1
        self.data["raw_signal"] = (self.data["momentum"] > 0).astype(int)
        self.data["signal"] = self.data["raw_signal"].shift(1).fillna(0).astype(int)
        self.data["trade_size"] = self.data["signal"].diff().abs().fillna(0)
        self.data["transaction_cost_paid"] = self.transaction_cost * self.data["trade_size"]
        self.data["strategy_return"] = (
            self.data["signal"] * self.data["return"] - self.data["transaction_cost_paid"]
        )
        self.data["equity"] = (1 + self.data["strategy_return"]).cumprod()
        self.data["peak"] = self.data["equity"].cummax()
        self.data["drawdown"] = (self.data["equity"] - self.data["peak"]) / self.data["peak"]
        return self.data
    
class MomentumVolTargetingStrategy(Strategy):

    def __init__(self, data, horizon, vol_window, target_vol, max_leverage, transaction_cost=0.0, rebal_threshold=0.0, trading_days=252):
        super().__init__(data)  #réutiliser le constructeur parent
        self.horizon = horizon
        self.vol_window = vol_window
        self.target_vol = target_vol
        self.max_leverage = max_leverage
        self.transaction_cost = transaction_cost
        self.rebal_threshold = rebal_threshold
        self.trading_days = trading_days

    def run(self):
        self.data["momentum"] = self.data["price"] / self.data["price"].shift(self.horizon) - 1
        self.data["raw_signal"] = (self.data["momentum"] > 0).astype(int)
        self.data["signal"] = self.data["raw_signal"].shift(1).fillna(0).astype(int)
        self.data["rolling_vol"] = self.data["return"].rolling(self.vol_window).std()
        self.data["rolling_vol_annual"] = self.data["rolling_vol"] * np.sqrt(self.trading_days)
        self.data["position_size"] = self.target_vol / self.data["rolling_vol_annual"]
        self.data["position_size"] = self.data["position_size"].clip(upper=self.max_leverage).fillna(0)
        self.data["target_exposure"] = self.data["signal"] * self.data["position_size"]

        actual_exposure = []
        for i, target in enumerate(self.data["target_exposure"]):
            if i == 0:
                actual_exposure.append(target)
            else:
                previous_exposure = actual_exposure[-1]
                if abs(target - previous_exposure) < self.rebal_threshold:
                    actual_exposure.append(previous_exposure)
                else:
                    actual_exposure.append(target)

        self.data["exposure"] = actual_exposure
        self.data["trade_size"] = self.data["exposure"].diff().abs().fillna(0)
        self.data["transaction_cost_paid"] = self.transaction_cost * self.data["trade_size"]
        self.data["strategy_return"] = self.data["exposure"] * self.data["return"] - self.data["transaction_cost_paid"]
        self.data["equity"] = (1 + self.data["strategy_return"]).cumprod()
        self.data["peak"] = self.data["equity"].cummax()
        self.data["drawdown"] = (self.data["equity"] - self.data["peak"]) / self.data["peak"]
        return self.data

class MeanReversionPriceStrategy(Strategy):

    def __init__(self, data, z_threshold, rolling_days):
        super().__init__(data)  #réutiliser le constructeur parent
        self.z_threshold = z_threshold
        self.rolling_days = rolling_days
    
    def run(self):
        self.data["rolling_mean"] = self.data["price"].rolling(self.rolling_days).mean()
        self.data["rolling_std"] = self.data["price"].rolling(self.rolling_days).std()
        self.data["z_score"] = (self.data["price"] - self.data["rolling_mean"]) / self.data["rolling_std"] 
        self.data["raw_signal"] = np.where(
            self.data["z_score"] < -self.z_threshold, 1, 
            np.where(self.data["z_score"] > self.z_threshold, -1, 0))
        self.data["signal"] = self.data["raw_signal"].shift(1).fillna(0).astype(int)
        self.data["strategy_return"] = self.data["signal"] * self.data["return"]
        self.data["equity"] = (1 + self.data["strategy_return"]).cumprod()
        self.data["peak"] = self.data["equity"].cummax()
        self.data["drawdown"] = (self.data["equity"] - self.data["peak"]) / self.data["peak"]
        return self.data
        
class MeanReversionReturnStrategy(Strategy):

    def __init__(self, data, z_threshold, rolling_days):
        super().__init__(data)  #réutiliser le constructeur parent
        self.z_threshold = z_threshold
        self.rolling_days = rolling_days
    
    def run(self):
        self.data["rolling_mean"] = self.data["return"].rolling(self.rolling_days).mean()
        self.data["rolling_std"] = self.data["return"].rolling(self.rolling_days).std()
        self.data["z_score"] = (self.data["return"] - self.data["rolling_mean"]) / self.data["rolling_std"] 
        self.data["raw_signal"] = np.where(
            self.data["z_score"] < -self.z_threshold, 1, 
            np.where(self.data["z_score"] > self.z_threshold, -1, 0))
        self.data["signal"] = self.data["raw_signal"].shift(1).fillna(0).astype(int)
        self.data["strategy_return"] = self.data["signal"] * self.data["return"]
        self.data["equity"] = (1 + self.data["strategy_return"]).cumprod()
        self.data["peak"] = self.data["equity"].cummax()
        self.data["drawdown"] = (self.data["equity"] - self.data["peak"]) / self.data["peak"]
        return self.data

class SpreadMeanReversionStrategy(Strategy):

    def __init__(self, data, ticker_1, ticker_2, z_threshold, rolling_days):
        super().__init__(data) #réutiliser le constructeur parent
        self.ticker_1 = ticker_1
        self.ticker_2 = ticker_2
        self.z_threshold = z_threshold
        self.rolling_days = rolling_days

    def run(self):
        price_1_col = f"{self.ticker_1}_price"
        price_2_col = f"{self.ticker_2}_price"
        return_1_col = f"{self.ticker_1}_return"
        return_2_col = f"{self.ticker_2}_return"
        self.data["spread"] = self.data[price_1_col] / self.data[price_2_col]
        self.data["rolling_mean"] = self.data["spread"].rolling(self.rolling_days).mean()
        self.data["rolling_std"] = self.data["spread"].rolling(self.rolling_days).std()
        self.data["z_score"] = (self.data["spread"] - self.data["rolling_mean"]) / self.data["rolling_std"] 
        self.data["raw_signal"] = np.where(
            self.data["z_score"] < -self.z_threshold, 1, 
            np.where(self.data["z_score"] > self.z_threshold, -1, 0))
        self.data["signal"] = self.data["raw_signal"].shift(1).fillna(0).astype(int)
        self.data["spread_return"] = self.data[return_1_col] - self.data[return_2_col]
        self.data["strategy_return"] = self.data["signal"] * self.data["spread_return"]
        self.data["equity"] = (1 + self.data["strategy_return"]).cumprod()
        self.data["peak"] = self.data["equity"].cummax()
        self.data["drawdown"] = (self.data["equity"] - self.data["peak"]) / self.data["peak"]
        return self.data
