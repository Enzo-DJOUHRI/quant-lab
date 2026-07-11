# Verification Momentum avec couts de transaction

Date: 2026-03-20

## 1) Objet et perimetre

- Strategie verifiee: `MomentumStrategy` (horizon 20 jours) sur `SPY`
- Periode: 2015-01-05 -> 2024-12-30 (`2514` observations)
- Cout de transaction teste: `0.0005` (5 bps par changement unitaire de position)

## 2) Calculs implementes (net de couts)

### `trade_size`

Formule:

- `trade_size_t = abs(signal_t - signal_{t-1})`

Intuition economique:

- `trade_size` mesure la taille du changement de position entre deux jours.
- Si on passe de `0` a `1` (ou de `1` a `0`), `trade_size = 1`: un trade.
- Plus la strategie change souvent d'etat, plus elle paie de couts.

### `transaction_cost_paid`

Formule:

- `transaction_cost_paid_t = transaction_cost * trade_size_t`

Intuition economique:

- Chaque ajustement de position consomme du PnL (frais/slippage simplifie).
- Cout proportionnel au volume de rebalance simplifie.

### `strategy_return` net

Formule:

- `strategy_return_net_t = signal_t * return_t - transaction_cost_paid_t`

Intuition economique:

- On part du rendement brut genere par l'exposition (`signal * return`).
- On retire le cout de passage d'ordres pour obtenir un rendement net plus realiste.

## 3) Nouvelles metriques

Definitions:

- `n_trades`: nombre de jours avec `trade_size > 0`
- `total_cost`: somme des `transaction_cost_paid`
- `time_in_market`: part du temps avec `signal != 0`

Resultats observes (Momentum 20 avec couts):

| Metrique | Valeur |
|---|---:|
| total_return | 126.56% |
| annual_return | 8.54% |
| annual_vol | 10.53% |
| sharpe | 0.831 |
| max_drawdown | -14.20% |
| n_trades | 210 |
| total_cost | 0.1050 |
| time_in_market | 68.38% |

## 4) Pourquoi ces metriques rendent le backtest plus realiste

- `n_trades`:
  - quantifie directement l'intensite d'execution;
  - evite de surestimer des strategies qui "sur-tradent".
- `total_cost`:
  - montre le poids cumule des frictions de marche;
  - rend visible un drag de performance souvent cache dans les backtests sans couts.
- `time_in_market`:
  - caracterise l'exposition effective au risque de marche;
  - utile pour distinguer une strategie "toujours investie" d'une strategie de timing.

## 5) Limites de cette modelisation simple des couts

- Cout lineaire fixe:
  - ne capture pas la microstructure (spread dynamique, impact de marche non lineaire).
- Pas de dependance a la liquidite/volatilite:
  - en pratique, les couts montent quand le marche est tendu.
- Pas de latence ni de slippage conditionnel:
  - execution supposee immediate au prix theorique.
- Pas de distinction entree/sortie partielle:
  - modele simplifie a taille de trade unitaire sur signal discret.

## 6) Interpretation courte des resultats Momentum apres couts

- Frequence de trading:
  - `210` trades sur `2514` jours, soit environ `21` trades/an.
  - activite moderee, pas du HFT.
- Impact des couts:
  - `total_cost = 0.105` (10.5 points de retour "arithmetique" cumule).
  - le `total_return` passe de `151.63%` (sans couts) a `126.56%` (avec couts), soit `-25.07` points.
  - les couts degradent aussi le Sharpe (`0.931 -> 0.831`).
- Temps passe investi:
  - `time_in_market = 68.38%`, coherent avec une logique de filtre de regime.
- Interet de la strategie apres couts:
  - reste positive et exploitable sur l'echantillon;
  - mais la rentabilite est sensiblement sensible aux frictions d'execution.

## 7) Verification technique et tests

Actions realisees:

- Clarification du nommage: `transaction_cost_paid` est la seule colonne de cout conservee.
- Ajout de tests unitaires:
  - fichier `tests/test_momentum_transaction_costs.py`
  - verification des formules `trade_size`, `transaction_cost_paid`, `strategy_return` net
  - verification des metriques `n_trades`, `total_cost`, `time_in_market`
- Execution tests:
  - `python3 -m unittest discover -s tests -v`
  - resultat: `3 tests`, tous `OK`.
