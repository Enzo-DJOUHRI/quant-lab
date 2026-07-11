# Reprise et analyse globale du Quant Lab

Date: 2026-05-03

## 1) Objectif de la reprise

Reprendre le projet apres une pause, verifier l'etat des fichiers, comprendre les ajouts recents et identifier les points a garder en tete avant de relancer le travail pendant les grandes vacances.

Vrai sujet:

- Le Quant Lab est en train de passer d'un backtester equity simple vers une base de recherche plus serieuse.
- Deux ajouts importants sont apparus:
  - une roadmap structuree Hull / Shreve / Quant Lab;
  - des metriques de recherche: `alpha`, `beta`, `tracking_error`, `information_ratio`, avec correction `trading_days` et `risk_free_rate`.

## 2) Inventaire rapide

Fichiers structurants:

- `main.py`: orchestration du backtest mono-actif ou multi-actifs.
- `src/data_loader.py`: chargement mono et multi via CSV cache + yfinance.
- `src/strategy.py`: strategies equity actuelles.
- `src/metrics.py`: metriques de performance et de recherche.
- `src/plots.py`: exports Plotly HTML dans `outputs/plots`.
- `src/config.py`: ticker courant, dates, couts, risk-free, jours de trading.
- `tests/test_momentum_transaction_costs.py`: tests unitaires actuels.

Dossiers de documentation:

- `rapport/`: historique des analyses et changements.
- `road_map/`: plan de progression finance quantitative sur 3-6 mois.

Dossiers de donnees/resultats:

- `data/raw/`: CSV par actif.
- `results/`: CSV de grilles et comparatifs.
- `outputs/plots/`: figures HTML Plotly.

## 3) Etat du code

Strategies implementees:

- `AlwaysLongStrategy`
- `MomentumStrategy`
- `MomentumVolTargetingStrategy`
- `MeanReversionPriceStrategy`
- `MeanReversionReturnStrategy`
- `SpreadMeanReversionStrategy`

Points solides:

- Les strategies calculent toutes `equity`, `peak`, `drawdown`.
- Momentum classique gere maintenant `trade_size` et `transaction_cost_paid`.
- Momentum vol targeting gere:
  - `rolling_vol_annual`;
  - `position_size`;
  - `target_exposure`;
  - `rebal_threshold`;
  - `trade_size`;
  - couts nets via `transaction_cost_paid`.
- `DataLoader` est robuste aux CSV deja presents et aux downloads vides.
- Les plots sont exportes en chemin stable depuis la racine du projet.

Point de structure a garder en tete:

- `src/data_loader_initial.py` reste comme ancienne version historique. Il n'est pas utilise par `main.py`.
- `main.py` reste un script de recherche manuel. Pour la suite, il faudra probablement separer:
  - lancement d'experience;
  - configuration;
  - sauvegarde des resultats.

## 4) Nouvelles metriques de recherche

Ajouts confirmes dans `src/metrics.py`:

- `risk_free_rate`
- `trading_days`
- `benchmark_return`
- `alpha`
- `beta`
- `tracking_error`
- `information_ratio`

Formules codees:

- `sharpe = (mean(r_strat) - rf_daily) / std(r_strat) * sqrt(trading_days)`
- `beta = cov(r_strat, r_bench) / var(r_bench)`
- `alpha = (mean(r_strat) - beta * mean(r_bench)) * trading_days`
- `tracking_error = std(r_strat - r_bench) * sqrt(trading_days)`
- `information_ratio = (annual_return_strat - annual_return_bench) / tracking_error`

Interpretation:

- `Sharpe`: performance absolue ajustee du risque total, apres taux sans risque.
- `Beta`: sensibilite au benchmark.
- `Alpha`: rendement residuel apres retrait de l'exposition benchmark.
- `Tracking error`: volatilite de l'ecart au benchmark.
- `Information ratio`: rendement actif par unite de risque actif.

Point important:

- Ces metriques sont pertinentes pour comparer une strategie a un benchmark clair.
- Ici le benchmark est `data["return"]`, donc buy-and-hold de l'actif sous-jacent.
- Pour BTC, cela rend l'IR tres exigeant, car le buy-and-hold 2015-2024 est extremement performant.

## 5) Verification execution

Commande lancee:

- `python3 -m unittest discover -s tests -p 'test_*.py'`

Resultat:

- `3` tests passent.

Commande lancee:

- `python3 main.py`

Config actuelle:

- `TICKERS = ["BTC-USD"]`
- periode `2015-01-01` a `2024-12-31`
- `trading_days = 365` detecte automatiquement pour BTC
- `RISK_FREE_RATE = 0.02`

Lecture rapide du run BTC:

| Strategie | Annual return | Annual vol | Sharpe | Max drawdown | Alpha | Beta | IR |
|---|---:|---:|---:|---:|---:|---:|---:|
| AlwaysLong | 76.51% | 69.31% | 1.141 | -83.40% | 0.00% | 1.000 | n/a |
| Momentum20 | 88.77% | 48.87% | 1.502 | -52.63% | 35.08% | 0.497 | 0.248 |
| MomentumVolTarget20 | 35.96% | 16.11% | 1.864 | -23.03% | 19.86% | 0.150 | -0.674 |
| MeanRevPrice20 | -18.39% | 30.09% | -0.587 | -89.52% | -14.97% | -0.009 | -1.248 |
| MeanRevReturn20 | 2.49% | 21.86% | 0.133 | -36.25% | 4.52% | 0.005 | -1.024 |

Lecture:

- `Momentum20` reste le plus fort en rendement brut sur BTC.
- `MomentumVolTarget20` est beaucoup plus propre en risque: Sharpe plus haut et drawdown beaucoup plus contenu.
- L'IR du vol targeting est negatif car il sous-performe le long BTC en rendement brut, meme s'il est meilleur en risque absolu.
- C'est coherent: le vol targeting transforme BTC en profil plus defensif, il ne cherche pas a battre le buy-and-hold dans une phase parabolique.

## 6) Point technique corrige: beta du benchmark

Observation:

- `AlwaysLong` compare a `data["return"]` devrait donner:
  - `beta = 1`
  - `alpha = 0`
  - `tracking_error = 0`
  - `information_ratio = NaN`

Run apres correction:

- `beta = 1.0000000000000007`
- `alpha = -4.75e-16`

Cause:

- `np.cov()` utilise par defaut une normalisation en `N-1`.
- `np.var()` utilise par defaut une normalisation en `N`.
- Le ratio donne donc un beta tres legerement au-dessus de 1 quand `strat == bench`.

Correction effectuee:

- Utilisation d'une convention coherente:
  - `np.cov(..., ddof=0)`
  - `np.var(..., ddof=0)`
- Ajout d'un test unitaire sanity:
  - `AlwaysLongStrategy` vs `benchmark_return=data["return"]`

Lecture:

- L'ecart restant (`1.0000000000000007`, `-4.75e-16`) est uniquement du bruit flottant numerique.
- Le benchmark passif sert maintenant bien de test sanity exact a tolerance numerique.

## 7) Roadmap ajoutee

La roadmap est bien structuree dans `road_map/`.

Fichiers principaux:

- `README.md`: index general et usage.
- `00_principes.md`: methode d'apprentissage, anti-patterns, cadence.
- `01_hull.md`: chemin de lecture Hull.
- `02_shreve.md`: chemin de lecture Shreve I.
- `03_quant_lab_modules.md`: modules a coder dans le Quant Lab.
- `04_pont_theorie_pratique.md`: liens Hull / Shreve / code / tests.
- `05_planning.md`: planning 16 semaines.
- `06_apres.md`: suites possibles apres la base.
- `07_lecons_prosperity.md`: retours d'experience Prosperity.

Structure des grandes vacances:

- Semaines 1-4: Black-Scholes, greeks, implied vol, smile.
- Semaines 5-8: binomial, GBM, Monte Carlo.
- Semaines 9-12: backtester options et strategies options.
- Semaines 13-16: risk management, IS/OOS, calibration, polish.

Lecture strategique:

- La roadmap est bonne parce qu'elle force le lien theorie -> code -> test.
- Le premier vrai module a coder sera probablement `src/derivatives/black_scholes.py`.
- Avant d'aller trop loin, il faudra ajouter une structure de dossiers (`derivatives`, `simulation`, `pricing`, `backtest`, `risk`) avec tests.

## 8) Donnees et resultats

CSV valides reperes:

- `SPY.csv`
- `AAPL.csv`
- `GOOGL.csv`
- `GE.csv`
- `GC=F.csv`
- `EURUSD=X.csv`
- `BTC-USD.csv`
- `SPY_QQQ.csv`

CSV a surveiller:

- `CL=F.csv`: seulement 1 ligne.
- `ETH-USD.csv`: seulement 1 ligne.
- `BTC.csv`: 106 lignes, probablement different de `BTC-USD`.

Implication:

- Pour des tests multi-actifs propres, il faudra verifier la validite des CSV avant de conclure.

## 9) Priorites conseillees a la reprise

Priorite 1:

- Mettre a jour les rapports de metriques si la correction change legerement les chiffres.

Priorite 2:

- Preparer la structure de la roadmap:
  - `src/derivatives/`
  - `tests/test_black_scholes.py`
  - premier module Black-Scholes avec tests Hull.

Priorite 3:

- Avant GitHub/publication:
  - creer `.gitignore`;
  - exclure `__pycache__`, `.DS_Store`, gros outputs HTML si non necessaires;
  - decider si les CSV bruts restent versionnes ou non.

## 10) Conclusion

Le projet est dans un bon etat de reprise.

Ce qui est deja solide:

- Backtester equity fonctionnel.
- Couts de transaction integres.
- Vol targeting avec rebalancing.
- Rapports coherents.
- Nouvelles metriques de recherche bien pensees.
- Roadmap claire pour passer vers options, pricing et simulation.

Ce qui manque pour monter d'un cran:

- Tests sur les nouvelles metriques.
- Correction du petit biais `beta`.
- Separation plus propre entre scripts d'experience et librairie.
- Premiere brique de derivatives avec tests numeriques de reference.
