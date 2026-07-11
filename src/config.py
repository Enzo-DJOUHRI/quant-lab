# src/config.py

TICKERS = ["BTC-USD"]
START_DATE = "2015-01-01"
END_DATE = "2024-12-31"

INITIAL_CAPITAL = 100_000

TRANSACTION_COST = 0.0005  # 0.05% = 5 bps (coût simple par trade)

TRADING_DAYS = 252  # approx nb de jours d'ouverture des marchés / an
RISK_FREE_RATE = 0.02  # 2% par an (placeholder simple)
TRADING_DAYS_CRYPTO = 365 