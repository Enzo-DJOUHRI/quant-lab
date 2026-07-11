# Test Strategie `MomentumVolTargetingStrategy` (SPY)

Date: 2026-03-21

## 1) Objectif et protocole

Objectif:

- Tester `MomentumVolTargetingStrategy` sur un ensemble raisonnable de parametres.
- Comparer au `MomentumStrategy` classique (avec les memes couts de transaction).

Donnees:

- Actif: `SPY`
- Periode: 2015-01-05 -> 2024-12-30 (`2514` jours)
- Cout de transaction: `0.0005` (5 bps)

Grille testee:

- `horizon`: `10`, `20`, `50`
- `vol_window`: `20`, `60`, `120`
- `target_vol`: `0.10`, `0.15`, `0.20`
- `max_leverage`: `1.0`, `1.5`, `2.0`

Total:

- `81` combinaisons vol-target + `3` baselines momentum classique
- Export brut: `results/momentum_vol_targeting_grid.csv`

## 2) Comment fonctionne la strategie (explication simple + rigoureuse)

### `momentum`

- `momentum_t = price_t / price_{t-horizon} - 1`
- Signal directionnel: si `momentum > 0`, on veut etre long; sinon flat.

Intuition:

- On suppose qu'une tendance recente peut se prolonger.

### `rolling_vol`

- `rolling_vol_t = std(returns sur vol_window)`
- puis annualisation: `rolling_vol_annual_t = rolling_vol_t * sqrt(252)`

Intuition:

- C'est une estimation du "niveau de risque instantane" du marche.
- La vol est difficile, car elle est instable, regime-dependante, et clusterisee (periodes calmes / periodes agitees).

### `position_size`

- `position_size_t = target_vol / rolling_vol_annual_t`
- puis clip avec `max_leverage`.

Intuition:

- Si la vol estimee monte, on reduit la taille (de-risking).
- Si la vol estimee baisse, on peut augmenter la taille (re-risking), dans la limite de `max_leverage`.

### `exposure`

- `exposure_t = signal_t * position_size_t`

Intuition:

- `signal` decide la direction (0 ou 1 ici), `position_size` decide l'intensite.
- On separe donc "direction" et "budget de risque".

### `trade_size`

- `trade_size_t = abs(exposure_t - exposure_{t-1})`

Intuition:

- Mesure la quantite effectivement reequilibree.
- Meme si le signal ne change pas, la variation de vol fait bouger `position_size`, donc on retrade.

### `transaction_cost_paid`

- `transaction_cost_paid_t = transaction_cost * trade_size_t`

Intuition:

- Le cout est paye a chaque ajustement d'exposition.
- Plus le rebalancing est frequent (ou ample), plus les couts montent.

## 3) Pourquoi le vol targeting peut ameliorer le Sharpe

Point cle de theorie finance:

- Le Sharpe est un ratio `rendement / risque`.
- Si la volatilite conditionnelle est previsible (au moins partiellement), une regle qui reduit l'exposition en phase de forte vol peut diminuer la variance plus vite qu'elle ne diminue le rendement moyen.
- Sur des actifs avec clustering de volatilite (comme les actions), ce mecanisme peut ameliorer le Sharpe et souvent limiter les drawdowns.

Intuition "math-finance" courte:

- Sans ciblage: rendement de strategie `r_t = signal_t * ret_t`
- Avec ciblage: `r_t = signal_t * (target_vol / sigma_t) * ret_t`
- Si `sigma_t` est une bonne proxie du risque a court terme, on normalise partiellement les chocs de variance.

## 4) Pourquoi le vol targeting peut aussi augmenter turnover et couts

- `position_size` varie quasi quotidiennement via `rolling_vol`.
- Donc `exposure` varie meme a signal constant.
- `trade_size` devient structurellement plus eleve que sur un momentum binaire simple.
- Cout total = somme(`transaction_cost_paid`) peut fortement grignoter le gain theorique du vol targeting.

## 5) Synthese des resultats (avec couts)

### Baseline Momentum classique

| Strategie | Annual return | Annual vol | Sharpe | Max drawdown | n_trades | total_cost | time_in_market |
|---|---:|---:|---:|---:|---:|---:|---:|
| Momentum h=10 | 7.31% | 10.47% | 0.727 | -16.91% | 304 | 0.1520 | 64.96% |
| Momentum h=20 | 8.54% | 10.53% | 0.831 | -14.20% | 210 | 0.1050 | 68.38% |
| Momentum h=50 | 6.91% | 11.13% | 0.656 | -21.64% | 115 | 0.0575 | 74.50% |

### Vol targeting: 3 configs representatifs

| Config | Annual return | Annual vol | Sharpe | Max drawdown | n_trades | total_cost | time_in_market |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Best Sharpe** `h=20, vw=20, tv=0.10, lev=2.0` | 9.18% | 8.12% | **1.122** | -12.63% | 1791 | 0.1127 | 68.38% |
| **Best Annual return** `h=20, vw=20, tv=0.20, lev=2.0` | **13.90%** | 14.61% | 0.964 | -22.62% | 1134 | 0.1742 | 68.38% |
| **Best Drawdown** `h=20, vw=60, tv=0.10, lev=1.0` | 5.61% | 6.87% | 0.828 | **-9.76%** | 1358 | 0.0778 | 68.38% |

### Lecture rapide de la grille

- Par horizon, beaucoup de configs vol-target battent le momentum classique en Sharpe:
  - h=10: `27/27` configs > Sharpe classique
  - h=20: `21/27` configs > Sharpe classique
  - h=50: `26/27` configs > Sharpe classique
- En return annuel, le gain existe mais moins systematique.

## 6) Focus couts: comparaison propre au meilleur Sharpe

Config: `h=20, vw=20, tv=0.10, lev=2.0`

- **Sans couts**: annual return `10.42%`, Sharpe `1.263`
- **Avec couts**: annual return `9.18%`, Sharpe `1.122`
- Cout total: `0.1127` avec `1791` jours de trade (`trade_size > 0`)

Comparatif avec momentum classique h=20:

- Momentum classique h=20: `210` trades
- Vol-target best Sharpe: `1791` trades

Conclusion:

- Le vol targeting apporte bien un gain de qualite risque/rendement ici.
- Mais il le paie par un turnover nettement plus eleve, donc une sensibilite structurelle aux couts.

## 7) Interpretation personnelle (simple)

- Ce qui marche:
  - Le vol targeting est efficace pour stabiliser la prise de risque.
  - Sur SPY, ca peut nettement ameliorer le Sharpe vs momentum classique.
- Ce qui coute:
  - Le mecanisme de rebalancing vol est "mangeur de turnover".
  - Si les couts reels sont plus eleves (spread, impact), la surperformance peut diminuer vite.
- Ce que je retiens:
  - La strategie est interessante, mais il faut la traiter comme une strategie de **risk budgeting dynamique**, pas juste un momentum.
  - Avant passage en "prod recherche", priorite a:
    - stress tests de couts (ex: 5, 10, 15 bps),
    - robustesse out-of-sample,
    - stabilisation de la vol estimee (EWMA, floors/caps, smoothing).

## 8) Mini comparaison SPY vs BTC (les 2 momentum)

Setup compare:

- Momentum classique: `h=20`
- Momentum vol targeting: `h=20, vol_window=20, target_vol=0.10, max_leverage=2.0`
- Cout: `0.0005`

| Actif | Strategie | Annual return | Annual vol | Sharpe | Max drawdown | n_trades | total_cost | time_in_market |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| SPY | Momentum | 8.54% | 10.53% | 0.831 | -14.20% | 210 | 0.1050 | 68.38% |
| SPY | MomentumVolTarget | 9.18% | 8.12% | 1.122 | -12.63% | 1791 | 0.1127 | 68.38% |
| BTC-USD | Momentum | 55.06% | 40.61% | 1.282 | -52.63% | 330 | 0.1650 | 57.74% |
| BTC-USD | MomentumVolTarget | 13.93% | 7.89% | 1.694 | -14.10% | 2273 | 0.0579 | 57.74% |

Lecture courte:

- Sur SPY:
  - vol targeting ameliore le Sharpe et baisse le drawdown;
  - turnover explose (210 -> 1791), donc couts plus frequents.
- Sur BTC:
  - vol targeting ecrase fortement le risque (vol et drawdown) et ameliore le Sharpe;
  - mais il coupe aussi une grosse partie du rendement brut.
- Point important:
  - `time_in_market` ne bouge pas (meme signal directionnel), c'est la **taille d'exposition** qui change.
  - En regime tres volatil (BTC), le ciblage de vol agit comme un gros de-risking structurel.

## 9) Test sur differents parametres (SPY + BTC)

Oui, on a bien teste la strategie sur une grille de parametres et pas sur un seul point.

Grille utilisee:

- `horizon`: `10`, `20`, `50`
- `vol_window`: `20`, `60`, `120`
- `target_vol`: `0.10`, `0.15`, `0.20`
- `max_leverage`: `1.0`, `1.5`, `2.0`

Total:

- `81` configs par actif pour `MomentumVolTargetingStrategy`
- baseline comparee: `Momentum` classique aux memes horizons
- export: `results/momentum_vol_targeting_grid_spy_btc.csv`

### 9.1 SPY - Synthese sweep

- Config qui maximise le Sharpe:
  - `h=20, vw=20, tv=0.10, lev=2.0`
  - annual return `9.18%`, annual vol `8.12%`, Sharpe `1.122`, maxDD `-12.63%`
- Config qui maximise le return:
  - `h=20, vw=20, tv=0.20, lev=2.0`
  - annual return `13.90%`, annual vol `14.61%`, Sharpe `0.964`, maxDD `-22.62%`
- Config la plus defensive (maxDD le moins negatif):
  - `h=20, vw=60, tv=0.10, lev=1.0`
  - annual return `5.61%`, annual vol `6.87%`, Sharpe `0.828`, maxDD `-9.76%`

Dominance vs Momentum classique:

- h=10: Sharpe meilleur sur `27/27` configs vol-target, return meilleur sur `8/27`
- h=20: Sharpe meilleur sur `21/27`, return meilleur sur `13/27`
- h=50: Sharpe meilleur sur `26/27`, return meilleur sur `16/27`

Lecture:

- Sur SPY, vol-target ameliore tres souvent le Sharpe.
- Le gain en return est plus selectif et depend surtout de `target_vol` et `max_leverage`.

### 9.2 BTC - Synthese sweep

- Config qui maximise le Sharpe:
  - `h=20, vw=20, tv=0.10, lev=1.5` (equivalent `lev=2.0` ici)
  - annual return `13.93%`, annual vol `7.89%`, Sharpe `1.694`, maxDD `-14.10%`
- Config qui maximise le return:
  - `h=20, vw=20, tv=0.20, lev=2.0`
  - annual return `28.95%`, annual vol `15.77%`, Sharpe `1.692`, maxDD `-26.56%`
- Config la plus defensive (maxDD le moins negatif):
  - `h=20, vw=120, tv=0.10, lev=1.0`
  - annual return `11.87%`, annual vol `7.81%`, Sharpe `1.474`, maxDD `-12.29%`

Dominance vs Momentum classique:

- h=10: Sharpe meilleur sur `27/27` configs vol-target, return meilleur sur `0/27`
- h=20: Sharpe meilleur sur `27/27`, return meilleur sur `0/27`
- h=50: Sharpe meilleur sur `27/27`, return meilleur sur `0/27`

Lecture:

- Sur BTC, le vol-target domine systematiquement le Sharpe, mais pas le return annuel brut.
- C'est coherent avec un actif tres volatil: la cible de vol reduit fortement l'exposition moyenne, donc protege mieux mais capte moins l'upside brut.

## 10) Effet du `rebal_threshold` (SPY + BTC)

Date ajout: 2026-03-22

Objectif:

- Mesurer l'effet du no-trade band de rebalancing sur le turnover, les couts et la performance.

Setup:

- Actifs: `SPY`, `BTC-USD`
- Cout de transaction: `0.0005` (5 bps)
- Strategie: `MomentumVolTargetingStrategy`
- Grille `rebal_threshold`: `0.00`, `0.01`, `0.02`, `0.05`, `0.10`
- Deux reglages testes:
  - `tv10`: `h=20, vol_window=20, target_vol=0.10, max_leverage=2.0`
  - `tv20`: `h=20, vol_window=20, target_vol=0.20, max_leverage=2.0`
- Export brut: `results/momentum_vol_targeting_rebal_threshold_spy_btc.csv`

### 10.1 Implementation mathematique du rebalancing

On definit d'abord l'exposition cible:

- `e*_t = signal_t * position_size_t`

Puis l'exposition executee avec bande d'inaction:

- si `|e*_t - e_{t-1}| < theta` alors `e_t = e_{t-1}`
- sinon `e_t = e*_t`

Avec:

- `theta = rebal_threshold`

Ensuite:

- `trade_size_t = |e_t - e_{t-1}|`
- `transaction_cost_paid_t = c * trade_size_t`
- `strategy_return_t = e_t * return_t - transaction_cost_paid_t`

Intuition finance-maths:

- `theta` introduit une **zone de non-trade** (hysteresis): on ignore les petites variations de vol estimee.
- Cela reduit le turnover et les couts, mais on suit moins finement la cible de risque (tracking error de l'exposition).
- Plus `theta` monte, plus on filtre le bruit de vol, mais plus on accepte un ecart temporaire entre risque cible et risque reel.

### 10.2 Baseline momentum (reference)

| Actif | Strategie | Annual return | Annual vol | Sharpe | Max drawdown | n_trades | total_cost | time_in_market |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| SPY | Momentum h=20 | 8.54% | 10.53% | 0.831 | -14.20% | 210 | 0.1050 | 68.38% |
| BTC-USD | Momentum h=20 | 55.06% | 40.61% | 1.282 | -52.63% | 330 | 0.1650 | 57.74% |

### 10.3 Sweep `rebal_threshold` - Regime `tv10`

| Actif | theta | Annual return | Annual vol | Sharpe | Max drawdown | n_trades | total_cost | time_in_market |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| SPY | 0.00 | 9.18% | 8.12% | 1.122 | -12.63% | 1791 | 0.1127 | 68.38% |
| SPY | 0.01 | 9.20% | 8.12% | 1.124 | -12.61% | 1197 | 0.1117 | 68.38% |
| SPY | 0.02 | 9.15% | 8.12% | 1.119 | -12.61% | 985 | 0.1106 | 68.38% |
| SPY | 0.05 | 9.11% | 8.14% | 1.112 | -12.60% | 667 | 0.1070 | 68.38% |
| SPY | 0.10 | 9.22% | 8.17% | 1.120 | -12.61% | 461 | 0.1019 | 68.38% |
| BTC-USD | 0.00 | 13.93% | 7.89% | 1.694 | -14.10% | 2273 | 0.0579 | 57.74% |
| BTC-USD | 0.01 | 13.88% | 7.91% | 1.682 | -14.07% | 935 | 0.0565 | 57.74% |
| BTC-USD | 0.02 | 13.74% | 7.96% | 1.657 | -14.25% | 706 | 0.0552 | 57.74% |
| BTC-USD | 0.05 | 14.10% | 8.26% | 1.637 | -14.68% | 499 | 0.0530 | 57.74% |
| BTC-USD | 0.10 | 14.05% | 8.87% | 1.526 | -13.44% | 388 | 0.0500 | 57.74% |

Lecture rapide `tv10`:

- SPY: on reduit fortement `n_trades` (1791 -> 461) avec peu d'impact sur Sharpe (1.122 -> 1.120).
- BTC: la baisse de turnover est massive (2273 -> 388), les couts baissent, mais Sharpe se degrade plus vite quand `theta` devient trop grand.

### 10.4 Sweep `rebal_threshold` - Regime `tv20`

| Actif | theta | Annual return | Annual vol | Sharpe | Max drawdown | n_trades | total_cost | time_in_market |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| SPY | 0.00 | 13.90% | 14.61% | 0.964 | -22.62% | 1134 | 0.1742 | 68.38% |
| SPY | 0.01 | 13.90% | 14.61% | 0.964 | -22.62% | 871 | 0.1737 | 68.38% |
| SPY | 0.02 | 13.93% | 14.61% | 0.966 | -22.59% | 730 | 0.1728 | 68.38% |
| SPY | 0.05 | 13.81% | 14.63% | 0.958 | -22.59% | 542 | 0.1709 | 68.38% |
| SPY | 0.10 | 13.81% | 14.62% | 0.958 | -22.57% | 398 | 0.1673 | 68.38% |
| BTC-USD | 0.00 | 28.95% | 15.77% | 1.692 | -26.56% | 2271 | 0.1151 | 57.74% |
| BTC-USD | 0.01 | 28.91% | 15.78% | 1.689 | -26.47% | 1212 | 0.1138 | 57.74% |
| BTC-USD | 0.02 | 28.82% | 15.82% | 1.680 | -26.52% | 933 | 0.1122 | 57.74% |
| BTC-USD | 0.05 | 28.44% | 15.94% | 1.650 | -26.53% | 637 | 0.1082 | 57.74% |
| BTC-USD | 0.10 | 29.23% | 16.52% | 1.635 | -27.58% | 495 | 0.1051 | 57.74% |

Lecture rapide `tv20`:

- SPY: meme message que `tv10`, forte reduction du turnover avec degradation moderee des ratios.
- BTC: le filtre de rebalance reduit bien les couts, mais la volatilite remonte plus vite car l'exposition devient moins reactive.

### 10.5 Interpretation synthese (SPY vs BTC)

- Sur les deux actifs, `theta` est un levier **operationnel** efficace pour contenir le turnover.
- Sur SPY, la performance est relativement stable quand on monte `theta` (jusqu'a `0.10` dans ce test).
- Sur BTC, l'effet "couts en baisse" est reel, mais la perte de tracking de vol est plus visible sur le Sharpe.
- `time_in_market` ne change pas: la direction vient toujours du meme signal momentum, c'est l'intensite d'exposition qui change.

Choix pratique (sur ce dataset):

- SPY: `theta` entre `0.02` et `0.10` semble un bon compromis robustesse/couts.
- BTC: `theta` plutot modere (`0.01` a `0.05`) pour ne pas trop degrader la qualite du ciblage de risque.

## 11) Nouvelles metriques de recherche (alpha, beta, TE, IR)

Date ajout: 2026-04-07

Contexte:

- Corrections prealables: `trading_days = 365` pour BTC, `risk_free_rate = 0.02` dans le Sharpe.
- Benchmark: buy & hold BTC-USD (`data["return"]`).
- Voir `rapport/2026-04-07_metriques_recherche.md` pour les definitions detaillees.

### 11.1 Resultats: MomentumVolTargetingStrategy sur BTC-USD

Config: `h=20, vol_window=20, target_vol=0.20, max_leverage=2.0, rebal_threshold=0.05, trading_days=365`

| Metrique | Valeur |
|---|---:|
| total_return | 2060.26% |
| annual_return | 35.96% |
| annual_vol | 16.11% |
| sharpe | 1.864 |
| max_drawdown | -23.03% |
| n_trades | 602 |
| total_cost | 0.0898 |
| time_in_market | 57.74% |
| alpha | 19.86% |
| beta | 0.150 |
| tracking_error | 60.19% |
| information_ratio | -0.674 |

### 11.2 Lecture des nouvelles metriques

**Beta = 0.15**

- La strategie ne capture que 15% des mouvements du BTC.
- C'est coherent: vol targeting sur un actif a ~70% de vol annuelle avec une cible a 20% reduit mecaniquement l'exposition moyenne a environ `0.20 / 0.70 ~ 0.29`, et on n'est investi que 58% du temps, donc `0.29 * 0.58 ~ 0.17`. Le beta observe de 0.15 est dans cet ordre de grandeur.
- Un beta aussi bas signifie que la strategie se comporte presque comme un actif independant du BTC: elle est largement decorrellee du benchmark.

**Alpha = 19.86%/an**

- Tres eleve. La strategie genere ~20%/an de rendement qui n'est pas explique par son exposition au BTC.
- Source principale de cet alpha: le signal momentum filtre les phases de bear market (on est flat), et le vol targeting reduit l'exposition en periodes de forte vol (souvent les krachs). Ces deux mecanismes produisent un rendement asymetrique: on capture une part de la hausse en coupant la plupart de la baisse.
- Attention: cet alpha est in-sample. Il inclut potentiellement du fitting sur les cycles bull/bear de BTC 2015-2024, qui etaient tres marques et favorables au momentum.

**Tracking Error = 60.19%**

- Enorme. La strategie fait quelque chose de radicalement different du buy & hold BTC.
- C'est previsible: quand le BTC fait +100% dans une annee et que la strategie est exposee a 15% de ca, l'ecart quotidien est massif.
- Un TE de 60% n'est pas un probleme en soi, mais il signifie que comparer cette strategie au long BTC est presque comparer deux actifs differents. Le benchmark n'est peut-etre pas le plus pertinent pour evaluer le vol targeting.

**Information Ratio = -0.67**

- Negatif. La strategie sous-performe le buy & hold BTC en rendement, ajuste du risque actif.
- C'est le trade-off fondamental du vol targeting sur un actif en forte tendance haussiere: on echange du rendement brut contre de la stabilite.
- Le long BTC fait ~60-70%/an sur cette periode. La strategie fait 36%/an. L'IR dit: "par unite d'ecart au benchmark, tu perds du rendement".
- Un IR negatif ne veut pas dire que la strategie est mauvaise. Il dit que si l'objectif est de battre le buy & hold BTC, le vol targeting n'est pas le bon outil. Si l'objectif est d'avoir un bon rendement absolu avec un risque maitrise (Sharpe de 1.86, drawdown de -23%), c'est une strategie interessante.

### 11.3 Sharpe vs IR: deux questions differentes

| Metrique | Question | Reponse ici |
|---|---|---|
| Sharpe = 1.86 | "Est-ce que le rendement absolu compense le risque total?" | Oui, excellent ratio rendement/risque |
| IR = -0.67 | "Est-ce que s'ecarter du benchmark est recompense?" | Non, le long BTC rapporte plus |

Pourquoi cette contradiction apparente:

- Le Sharpe regarde le rendement absolu (36%/an) vs le risque total (16% de vol). C'est bon.
- L'IR regarde le rendement relatif (36% - 66% = -30%/an) vs le risque actif (60% de TE). C'est mauvais.
- Le vol targeting **transforme le profil de risque** du BTC: moins de rendement, beaucoup moins de risque. C'est une strategie de gestion du risque, pas une strategie de surperformance du benchmark.

### 11.4 Limites et points ouverts

- **Benchmark trop favorable**: le long BTC sur 2015-2024 inclut une appreciation de ~100x. Presque aucune strategie active ne peut battre un buy & hold sur un actif en bulle parabolique. L'IR negatif est donc en partie un artefact de la periode.
- **Alpha in-sample**: les 20%/an d'alpha n'ont pas ete valides hors echantillon. C'est la prochaine etape critique (IS/OOS split).
- **Stationnarite du beta**: le beta de 0.15 est une moyenne sur 10 ans. En realite, il varie dans le temps (plus eleve en marche calme, plus bas en marche agite a cause du vol targeting). Un rolling beta serait plus informatif.
- **TE trop grand pour que l'IR soit tres interpretable**: avec 60% de TE, l'IR capture surtout le fait que la strategie est un actif fondamentalement different du benchmark. L'IR est plus utile quand le TE est modere (5-15%), typiquement pour des strategies qui devient legerement d'un indice.
