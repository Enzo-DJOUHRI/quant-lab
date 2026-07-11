# Rapport compare - Strategies `AlwaysLong` vs `Momentum 20`

Date: 2026-03-10

## 1. Perimetre de comparaison

- Univers: `SPY`
- Fenetre: 2015-01-05 -> 2024-12-30 (2514 jours de bourse)
- Strategies:
  - `AlwaysLong`: exposition 100% en permanence
  - `Momentum 20`: position longue uniquement si momentum 20j > 0 (avec decalage d'1 jour)
- Courbes utilisees:
  - `outputs/plots/equity_curve_comparison.html`
  - `outputs/plots/drawdown_curve_comparison.html`

## 2. Metriques quantitatives (performance et risque)

| Metrique | AlwaysLong | Momentum 20 | Lecture rapide |
|---|---:|---:|---|
| Total return | 247.08% | 151.63% | `AlwaysLong` gagne plus en absolu |
| Rendement annualise | 13.28% | 9.69% | Avantage `AlwaysLong` |
| Volatilite annualisee | 17.62% | 10.53% | `Momentum 20` nettement moins volatil |
| Sharpe | 0.786 | 0.931 | Avantage `Momentum 20` (meilleur rendement/risque) |
| Max drawdown | -33.72% | -13.34% | Avantage fort `Momentum 20` |
| Calmar (CAGR/|MDD|) | 0.394 | 0.727 | Avantage `Momentum 20` |
| Exposition moyenne | 100.00% | 68.38% | `Momentum 20` filtre le risque de marche |
| Win rate journalier global | 54.61% | 37.71% | Biais par les jours flat de `Momentum 20` |
| Win rate quand investi | 54.61% | 55.15% | Leger avantage `Momentum 20` |

## 3. Comparaison qualitative des courbes d'equity

- `AlwaysLong`:
  - Courbe d'equity plus pentue sur le long terme (performance finale plus elevee).
  - Profil plus "agressif": progression avec des phases de baisse plus profondes.
- `Momentum 20`:
  - Courbe plus reguliere, moins violente.
  - Sous-performe en rendement brut, mais avec un trajet de performance plus defendable en gestion du risque.

Lecture synthese equity:

- Si l'objectif prioritaire est la **croissance absolue**, `AlwaysLong` domine.
- Si l'objectif prioritaire est la **stabilite du parcours de capital**, `Momentum 20` est plus robuste.

## 4. Comparaison qualitative des courbes de drawdown

- `AlwaysLong`:
  - Drawdowns plus profonds (jusqu'a -33.72%).
  - Episode le plus long sous le peak: 488 jours.
- `Momentum 20`:
  - Drawdowns beaucoup moins profonds (min a -13.34%).
  - Episode le plus long sous le peak: 298 jours.
  - Temps total sous le peak eleve (~89%), signe de drawdowns plus frequents mais moins severes.

Lecture synthese drawdown:

- `Momentum 20` controle beaucoup mieux le **risque de perte severe**.
- `AlwaysLong` accepte des creux plus durs pour chercher plus de performance brute.

## 5. Conclusion operationnelle (etat actuel)

- `AlwaysLong` = benchmark simple, utile comme reference de performance max "beta marche".
- `Momentum 20` = version deja plus "quant" (filtrage regime), meilleure qualite de risque mais rendement inferieur.
- Pour la suite du lab:
  - conserver les 2 en baseline;
  - comparer la prochaine courbe/strategie a ces deux references avec la meme grille (return, Sharpe, MDD, Calmar, drawdown duration).

---

## 6. Extension - Momentum multi-horizons (5, 10, 20, 50, 100)

Execution realisee le 2026-03-10 sur les horizons:

- `Momentum 5`
- `Momentum 10`
- `Momentum 20`
- `Momentum 50`
- `Momentum 100`

Plots generes:

- `outputs/plots/price_signal_momentum_5.html`
- `outputs/plots/price_signal_momentum_10.html`
- `outputs/plots/price_signal_momentum_20.html`
- `outputs/plots/price_signal_momentum_50.html`
- `outputs/plots/price_signal_momentum_100.html`
- `outputs/plots/equity_curve_comparison.html`
- `outputs/plots/drawdown_curve_comparison.html`

### 6.1 Metriques comparees (vs benchmark `AlwaysLong`)

| Strategie | Total return | Annual return | Annual vol | Sharpe | Max DD | Calmar | Exposition | Switches/an |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| AlwaysLong | 247.08% | 13.28% | 17.62% | 0.786 | -33.72% | 0.394 | 100.00% | 0.0 |
| Momentum 5 | 52.86% | 4.35% | 10.94% | 0.444 | -16.31% | 0.266 | 61.50% | 50.6 |
| Momentum 10 | 135.43% | 8.96% | 10.46% | 0.873 | -15.14% | 0.592 | 64.96% | 30.5 |
| Momentum 20 | 151.63% | 9.69% | 10.53% | 0.931 | -13.34% | 0.727 | 68.38% | 21.1 |
| Momentum 50 | 106.20% | 7.52% | 11.13% | 0.708 | -21.08% | 0.357 | 74.50% | 11.5 |
| Momentum 100 | 119.73% | 8.21% | 11.78% | 0.729 | -18.95% | 0.433 | 75.02% | 7.9 |

### 6.2 Lecture qualitative des plots `price_and_signal`

- Horizon 5:
  - Signal tres nerveux, changements frequents (beaucoup de whipsaws).
  - Bonne reduction du risque, mais trop de bruit et de rotations; performance faible.
- Horizon 10:
  - Compromis deja plus propre; moins de bruit que h=5.
  - Qualite risque/performance solide.
- Horizon 20:
  - Le meilleur equilibre du lot: signal encore reactif sans sur-trader.
  - C'est l'horizon qui domine sur Sharpe et Calmar.
- Horizon 50:
  - Signal plus lisse mais plus retard; re-entre plus tard apres creux.
  - Drawdown plus profond que h=10/h=20.
- Horizon 100:
  - Signal le plus lent (lag important), peu de switches.
  - Mieux que h=50 en perf/risque globale, mais reste en dessous de h=20.

### 6.3 Lecture qualitative des courbes equity / drawdown

- Equity:
  - `AlwaysLong` garde la meilleure performance finale.
  - Cote momentum, ordre de performance: `20` > `10` > `100` > `50` > `5`.
- Drawdown:
  - Le plus defendable cote momentum: `20` (MDD le plus faible, -13.34%).
  - `5` limite aussi bien le drawdown, mais sacrifie trop de rendement.
  - `50` et `100` deviennent trop lents en regime change, d'ou un risque qui remonte.

### 6.4 Conclusion pratique (etat actuel)

- Si l'objectif principal est rendement absolu: `AlwaysLong` reste devant.
- Si l'objectif est un meilleur couple rendement/risque en momentum:
  - meilleur candidat actuel: `Momentum 20`;
  - second candidat robuste: `Momentum 10`.

---

## 7. Extension - Mean Reversion 20 (tests z-threshold)

Date: 2026-03-12

Tests demandes:

- `MeanReversion 20` avec `z_threshold` = `1.0`, `1.5`, `2.0`, `2.5`
- contrainte respectee: aucun test au-dela de `3` ecarts-types

Plots generes:

- `outputs/plots/price_signal_meanrev20_z1_0.html`
- `outputs/plots/price_signal_meanrev20_z1_5.html`
- `outputs/plots/price_signal_meanrev20_z2_0.html`
- `outputs/plots/price_signal_meanrev20_z2_5.html`
- `outputs/plots/equity_curve_comparison.html`
- `outputs/plots/drawdown_curve_comparison.html`

### 7.1 Comparaison quantitative (vs `AlwaysLong` et `Momentum 20`)

| Strategie | Total return | Annual return | Annual vol | Sharpe | Max DD | Calmar |
|---|---:|---:|---:|---:|---:|---:|
| AlwaysLong | 247.08% | 13.28% | 17.62% | 0.786 | -33.72% | 0.394 |
| Momentum 20 | 151.63% | 9.69% | 10.53% | 0.931 | -13.34% | 0.727 |
| MeanRev20 z1.0 | -13.76% | -1.47% | 13.67% | -0.040 | -43.95% | -0.034 |
| MeanRev20 z1.5 | 34.25% | 3.00% | 10.25% | 0.339 | -11.51% | 0.260 |
| MeanRev20 z2.0 | 49.45% | 4.11% | 6.51% | 0.650 | -8.19% | 0.502 |
| MeanRev20 z2.5 | 3.15% | 0.31% | 3.07% | 0.117 | -8.19% | 0.038 |

### 7.2 Pourquoi le return Mean Reversion 20 est faible

Cause principale (structurelle sur SPY 2015-2024):

- Le marche est globalement haussier sur la periode.
- Une strategie mean reversion price-only prend regulierement des positions **short** contre la tendance de fond.

Constats mesures sur les tests:

- `z=1.0`: trop de trading + trop de short
  - exposition 59.35%, dont 43.28% de jours short;
  - 61.4 changements de regime/an;
  - retour moyen des jours short negatif (`-0.000366`), ce qui plombe la perf;
  - resultat final negatif et max drawdown tres eleve.
- `z=1.5`: moins de bruit, mais short encore penalise
  - short ~21.88% des jours;
  - retour moyen short encore negatif (`-0.000501`);
  - perf positive mais modeste.
- `z=2.0`: meilleur compromis de la grille
  - short reduit (~4.42% des jours);
  - faible drawdown et Sharpe correct;
  - mais exposition totale tres faible (~8.91%), donc rendement absolu limite.
- `z=2.5`: quasi pas de positions
  - exposition ~1.79% seulement;
  - risque faible mais return presque nul.

Lecture qualitative des courbes:

- Plus `z_threshold` est bas, plus le signal est nerveux et contre-tendance (beaucoup de whipsaws).
- Plus `z_threshold` est haut, plus la strategie devient selective, mais finit trop souvent flat pour generer du return.
- Au final, `MeanRev20` ameliore parfois le risque, mais n'arrive pas a battre `Momentum 20` ni `AlwaysLong` en performance brute sur cet echantillon.

### 7.3 Conclusion rapide pour la suite

- Meilleur seuil actuel pour `MeanReversion 20`: `z=2.0`.
- Meme dans ce cas, la strategie reste en dessous des deux baselines sur le rendement.
- Hypothese a tester ensuite pour relever la perf:
  - version long-only (sans shorts);
  - filtre regime (activer mean reversion seulement en marche range);
  - sortie plus fine que le simple retour a `z=0`.

---

## 8. Extension - Multi-actifs (comparatif 3 strategies)

Date: 2026-03-12 / 2026-03-13

Perimetre:

- Strategies comparees:
  - `AlwaysLong`
  - `Momentum20`
  - `MeanReversionPrice20 (z=2)`
- Actifs testables avec CSV valides:
  - `SPY`, `AAPL`, `GOOGL`, `EURUSD=X`, `GC=F`, `BTC-USD`
- CSV encore vides:
  - `CL=F`, `ETH-USD`

Resultats:

| Actif | AlwaysLong return | Momentum20 return | MeanRev20(z=2) return | AlwaysLong Sharpe | Momentum20 Sharpe | MeanRev20 Sharpe | AlwaysLong maxDD | Momentum20 maxDD | MeanRev20 maxDD |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| SPY | 247.08% | 151.63% | 49.45% | 0.786 | 0.931 | 0.650 | -33.72% | -13.34% | -8.19% |
| AAPL | 965.88% | 634.19% | 6.07% | 0.966 | 1.165 | 0.108 | -38.52% | -25.42% | -24.78% |
| GOOGL | 638.97% | 112.06% | 63.05% | 0.840 | 0.465 | 0.498 | -44.32% | -40.93% | -21.37% |
| EURUSD=X | -13.73% | -11.43% | 1.34% | -0.143 | -0.192 | 0.061 | -23.29% | -22.43% | -5.30% |
| GC=F | 116.47% | -11.03% | -17.01% | 0.612 | -0.047 | -0.362 | -20.87% | -27.25% | -20.86% |
| BTC-USD | 29307.55% | 67788.42% | -86.90% | 0.972 | 1.310 | -0.432 | -83.40% | -51.41% | -89.52% |

Lecture rapide:

- Rendement brut:
  - `AlwaysLong` gagne 4 actifs sur 6 (`SPY`, `AAPL`, `GOOGL`, `GC=F`).
  - `Momentum20` gagne sur `BTC-USD`.
  - `MeanReversionPrice20` gagne sur `EURUSD=X`.
- Qualite rendement/risque (Sharpe):
  - `Momentum20` domine sur `SPY`, `AAPL`, `BTC-USD`.
  - `AlwaysLong` domine sur `GOOGL`, `GC=F`.
  - `MeanReversionPrice20` domine sur `EURUSD=X`.
- Protection drawdown:
  - `MeanReversionPrice20` est souvent le plus defensif, sauf sur `BTC-USD` (ou `Momentum20` est meilleur).

---

## 9. Nouvelle strategie - Mean Reversion Return 20 (multi-actifs)

Date: 2026-03-13

Parametres testes:

- `MeanReversionReturnStrategy`
- `rolling_days = 20`
- `z_threshold = 2`

Comparatif 4 strategies:

| Actif | AlwaysLong return | Momentum20 return | MeanRevPrice20 return | MeanRevReturn20 return | AlwaysLong Sharpe | Momentum20 Sharpe | MeanRevPrice20 Sharpe | MeanRevReturn20 Sharpe | AlwaysLong maxDD | Momentum20 maxDD | MeanRevPrice20 maxDD | MeanRevReturn20 maxDD |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| SPY | 247.08% | 151.63% | 49.45% | 45.92% | 0.786 | 0.931 | 0.650 | 0.624 | -33.72% | -13.34% | -8.19% | -10.77% |
| AAPL | 965.88% | 634.19% | 6.07% | 22.25% | 0.966 | 1.165 | 0.108 | 0.290 | -38.52% | -25.42% | -24.78% | -23.77% |
| GOOGL | 638.97% | 112.06% | 63.05% | -20.57% | 0.840 | 0.465 | 0.498 | -0.269 | -44.32% | -40.93% | -21.37% | -25.16% |
| EURUSD=X | -13.73% | -11.43% | 1.34% | 4.53% | -0.143 | -0.192 | 0.061 | 0.247 | -23.29% | -22.43% | -5.30% | -3.08% |
| GC=F | 116.47% | -11.03% | -17.01% | -5.59% | 0.612 | -0.047 | -0.362 | -0.161 | -20.87% | -27.25% | -20.86% | -11.26% |
| BTC-USD | 29307.55% | 67788.42% | -86.90% | 27.86% | 0.972 | 1.310 | -0.432 | 0.186 | -83.40% | -51.41% | -89.52% | -36.25% |

Lecture strategique de `MeanReversionReturn20`:

- Par rapport a `MeanReversionPrice20`:
  - meilleure perf sur `AAPL`, `EURUSD=X`, `GC=F`, `BTC-USD`;
  - moins bonne sur `SPY`, `GOOGL`.
- Forces:
  - profil drawdown souvent solide (meilleur max drawdown sur 4 actifs sur 6).
  - comportement tres pertinent sur `EURUSD=X` (meilleur return + Sharpe + maxDD des 4 strategies).
- Limites:
  - ne devient pas la meilleure strategie globale sur actifs fortement trend (`SPY`, `AAPL`, `GOOGL`, `BTC`).
  - peut rester trop defensive en rendement absolu.

Conclusion:

- `MeanReversionReturn20` est un bon candidat "defensif/range".
- Pour actifs directionnels, `Momentum20` et/ou `AlwaysLong` restent dominants selon l'objectif (Sharpe vs return brut).

Trace des resultats bruts:

- `results/multi_asset_strategy_comparison.csv`
- `results/multi_asset_strategy_comparison_with_mr_return.csv`

---

## 10. Premiere strategie multi-actifs - Mean Reversion sur Spread

Date: 2026-03-14

Contexte:

- Premiere strategie multi-actifs du projet.
- Setup actuel (sans comparaison aux autres strategies multi pour l'instant):
  - paire: `SPY` / `QQQ`
  - signal: `SpreadMeanReversionStrategy`
  - parametres: `z_threshold = 2`, `rolling_days = 20`
  - periode: 2015-01-05 -> 2024-12-30 (`2514` observations)

Metriques:

| Metrique | Valeur |
|---|---:|
| Total return | 1.28% |
| Annual return | 0.13% |
| Annual vol | 3.11% |
| Sharpe | 0.057 |
| Max drawdown | -8.47% |

Indicateurs de regime (diagnostic rapide):

| Indicateur | Valeur |
|---|---:|
| Jours long spread | 5.85% |
| Jours short spread | 4.26% |
| Jours flat | 89.90% |
| Switches de signal | 278 |
| Switches/an | 27.87 |
| Win rate quand en position | 52.76% |

Lecture initiale:

- Strategie tres selective (beaucoup de temps flat).
- Profil risque contenu (vol faible, drawdown modere), mais rendement encore faible a ce stade.

Idee future a investiguer (correlation inter-actifs):

- Evaluer le facteur de correlation entre actifs avant de choisir une paire spread:
  - corrélation historique (globale et rolling);
  - stabilite de la corrélation dans le temps.
- Hypothese: un spread mean reversion a plus de chances d'etre pertinent sur des paires avec relation structurelle forte (corrélation stable), et moins sur des paires dont la relation se degrade.

---

## 11. Lecture rapide - Courbe d'equity BTC (run actuel)

Date: 2026-03-22

Contexte du plot regarde:

- actif: `BTC-USD`
- fichier: `outputs/plots/equity_curve_comparison.html`
- strategies tracees: `AlwaysLong`, `Momentum20`, `MomentumVolTarget(h=20,vw=20,tv=0.20,lev=2.0,theta=0.05)`, `MeanRevPrice20(z=2)`, `MeanRevReturn20(z=2)`

Metriques cle (meme run):

| Strategie | Equity finale | Annual return | Annual vol | Sharpe | Max drawdown |
|---|---:|---:|---:|---:|---:|
| Momentum20 | 575.49x | 55.06% | 40.61% | 1.282 | -52.63% |
| AlwaysLong | 294.81x | 48.04% | 57.59% | 0.972 | -83.40% |
| MomentumVolTarget tv20 | 37.58x | 28.44% | 15.94% | 1.650 | -26.53% |
| MeanRevReturn20 z=2 | 1.28x | 1.71% | 18.17% | 0.186 | -36.25% |
| MeanRevPrice20 z=2 | 0.13x | -13.09% | 25.00% | -0.432 | -89.52% |

Pourquoi la courbe peut paraitre "etrange" vs intuition:

- Si tu attendais que le vol targeting batte le momentum en rendement brut, ce n'est pas son but principal.
- Le vol targeting cible un budget de risque; sur BTC il coupe fortement l'exposition moyenne, donc il lisse la courbe mais limite l'explosion haussiere.
- Ici l'exposition moyenne de la version vol-target est proche de `0.30` (donc bien en dessous d'un long "plein pot" la plupart du temps), ce qui explique la pente plus faible de l'equity.
- En contrepartie, le profil risque est beaucoup plus propre (`maxDD -26.53%` vs `-52.63%` sur momentum).

Point de lecture visuelle important:

- Le graphe d'equity est en echelle lineaire.
- Avec une courbe qui finit a `575x` et une autre a `37x`, la courbe a `37x` peut paraitre "plate" alors qu'elle reste tres performante en absolu.
- Pour lire proprement BTC, il faut regarder aussi:
  - les metriques (Sharpe, max drawdown),
  - et idealement une vue en echelle log pour comparer les pentes relatives.

Conclusion courte:

- Resultat coherent avec la theorie:
  - `Momentum20`: performance brute tres elevee mais risque extremement eleve.
  - `MomentumVolTarget`: moins de perf brute, mais meilleur compromis risque/rendement.
