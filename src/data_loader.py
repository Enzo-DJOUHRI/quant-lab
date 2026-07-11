import yfinance as yf
import pandas as pd
from pathlib import Path

class DataLoader:

    def __init__(self, tickers, start_date, end_date):
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        project_root = Path(__file__).resolve().parent.parent
        tickers_name = "_".join(self.tickers)
        self.file_path = project_root / "data" / "raw" / f"{tickers_name}.csv"

    def load_mono(self):
        ticker = self.tickers[0]

        # Conversion du CSV en DataFrame s'il existe
        if self.file_path.exists():
            data = pd.read_csv(self.file_path, index_col=0, parse_dates=True)
            if (not data.empty) and {"price", "return"}.issubset(set(data.columns)):
                return data
            # CSV vide/invalide -> on retente un download propre.

        data = yf.download(
                ticker,
                start=self.start_date,
                end=self.end_date,
                auto_adjust=True
            )

        if data.empty:
            raise ValueError(
                f"No data downloaded for {ticker}. Check ticker/date/network."
            )

        # Prendre la colonne Close (yfinance multi-index ou simple index)
        if isinstance(data.columns, pd.MultiIndex):
            adj_close = data[("Close", ticker)].copy()
        else:
            adj_close = data["Close"].copy()

        # Transformer en DataFrame et renommer close en price
        adj_close = adj_close.to_frame(name="price")

        # calcule le rendement journalier et supprime les lignes Null
        adj_close["return"] = adj_close["price"].pct_change()
        adj_close.dropna(inplace=True)

        if adj_close.empty:
            raise ValueError(
                f"No usable rows for {ticker} after pct_change/dropna."
            )

        # sauvegarder le DataFrame telecharge en CSV pour la suite
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        adj_close.to_csv(self.file_path)

        return adj_close

    def load_multi(self):
        expected_cols = []
        for ticker in self.tickers:
            expected_cols.extend([f"{ticker}_price", f"{ticker}_return"])

        if self.file_path.exists():
            data = pd.read_csv(self.file_path, index_col=0, parse_dates=True)
            if (not data.empty) and set(expected_cols).issubset(set(data.columns)):
                return data

        data = yf.download(
            self.tickers,
            start=self.start_date,
            end=self.end_date,
            auto_adjust=True
        )

        if data.empty:
            raise ValueError(
                f"No data downloaded for {self.tickers}. Check tickers/date/network."
            )

        # Prendre la colonne Close (yfinance multi-index ou simple index)
        if isinstance(data.columns, pd.MultiIndex):
            if "Close" not in data.columns.get_level_values(0):
                raise ValueError(
                    f"Close field not found in downloaded data for {self.tickers}."
                )
            adj_close = data["Close"].copy()
        else:
            # Cas limite (souvent single ticker): une seule colonne Close
            if "Close" not in data.columns:
                raise ValueError(
                    f"Close column not found in downloaded data for {self.tickers}."
                )
            ticker = self.tickers[0]
            adj_close = data["Close"].to_frame(name=ticker)

        # Garantit un DataFrame avec tickers en colonnes
        if isinstance(adj_close, pd.Series):
            ticker = self.tickers[0]
            adj_close = adj_close.to_frame(name=ticker)

        available_tickers = [t for t in self.tickers if t in adj_close.columns]
        missing_tickers = [t for t in self.tickers if t not in adj_close.columns]

        if missing_tickers:
            raise ValueError(
                f"Missing Close data for tickers: {missing_tickers}. "
                "Check ticker symbols and data availability."
            )

        adj_close = adj_close[available_tickers].copy()
        adj_close.dropna(how="all", inplace=True)

        if adj_close.empty:
            raise ValueError(
                f"No usable Close rows for {self.tickers} after cleanup."
            )

        # Transformer en DataFrame et renommer close en price
        adj_close.columns = [f"{ticker}_price" for ticker in adj_close.columns]

        # calcule les rendements journaliers
        returns = adj_close.pct_change()
        returns.columns = [col.replace("_price", "_return") for col in returns.columns]

        # concatène prix et rendements
        data_multi = pd.concat([adj_close, returns], axis=1)
        data_multi.dropna(inplace=True)

        if data_multi.empty:
            raise ValueError(
                f"No usable rows for {self.tickers} after pct_change/dropna."
            )

        # sauvegarder le DataFrame téléchargé en CSV pour la suite
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        data_multi.to_csv(self.file_path)

        return data_multi
