import yfinance as yf
import pandas as pd
import os

def download_price_data(ticker, start_date, end_date):

    # vérification et création chemin d'accès Dataset
    file_path = os.path.join("data", "raw", f"{ticker}.csv")

    # Conversion du CSV en Dataframe 
    if os.path.exists(file_path):
        adj_close = pd.read_csv(file_path, index_col=0, parse_dates=True)
        return adj_close

    else: 
        data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)
        # Prendre directement la colonne Close en précisant les deux niveaux
        adj_close = data[("Close", ticker)].copy()
        # Transformer en DataFrame propre
        adj_close = adj_close.to_frame(name="price")

        # calcule le rendement journalier et supprime les lignes Null
        adj_close["return"] = adj_close["price"].pct_change() 
        adj_close.dropna(inplace=True)
        
        os.makedirs("data/raw", exist_ok=True)
        adj_close.to_csv(file_path)
        return adj_close
