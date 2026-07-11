# Corrections et ajout de metriques de recherche

Date: 2026-04-07

## 1) Corrections apportees

### 1.1 `trading_days` parametrable (correction BTC)

Probleme:

- `TRADING_DAYS = 252` etait utilise partout, y compris pour BTC qui trade 365 jours/an.
- Consequence: vol annualisee sous-estimee d'environ 20% (`sqrt(365/252) ~ 1.20`), Sharpe sur-estime d'autant.

Correction:

- `compute_metrics()` accepte maintenant `trading_days` en parametre (defaut `252`).
- `MomentumVolTargetingStrategy` accepte aussi `trading_days` pour le calcul de `rolling_vol_annual`.
- `TRADING_DAYS_CRYPTO = 365` ajoute dans `config.py`.
- L'appelant (`main.py`) choisit la valeur correcte selon l'actif.

Impact attendu:

- Sur SPY: aucun changement (252 reste le defaut).
- Sur BTC: la vol annualisee augmente, le Sharpe baisse. C'est la valeur correcte.

### 1.2 Risk-free rate dans le Sharpe

Probleme:

- Le Sharpe etait calcule comme `mean(r) / std(r) * sqrt(T)`, sans soustraire le taux sans risque.
- `RISK_FREE_RATE = 0.02` existait dans config mais n'etait jamais utilise.

Correction:

- `daily_rf = risk_free_rate / trading_days`
- `sharpe = (mean(r) - daily_rf) / std(r) * sqrt(trading_days)`

Pourquoi c'est important:

- Le Sharpe mesure le rendement **excessif** par unite de risque. Le rendement excessif, c'est ce qu'on gagne au-dela du placement sans risque (obligations d'etat court terme).
- Sans cette soustraction, une strategie qui rapporte 2%/an avec 1% de vol aurait un Sharpe de 2.0, alors qu'elle ne fait que repliquer le taux sans risque. Avec la correction (rf = 2%), son Sharpe tombe a 0: elle n'apporte aucun edge.
- Sur la periode 2015-2024, les taux sont montes au-dessus de 5%. Utiliser rf = 2% est un placeholder conservateur.

Note technique:

- `std(r - rf_daily) = std(r)` car `rf_daily` est une constante. Le denominateur ne change pas, seul le numerateur bouge.

---

## 2) Nouvelles metriques de recherche

### 2.1 Beta

Formule:

- `beta = cov(r_strat, r_bench) / var(r_bench)`

Ce que c'est:

- Le beta mesure la **sensibilite** de la strategie aux mouvements du benchmark.
- `beta = 1`: la strategie bouge exactement comme le benchmark.
- `beta = 0.5`: la strategie capture la moitie des mouvements du benchmark.
- `beta = 0`: la strategie est decorrellee du benchmark.

Intuition financiere:

- Le beta quantifie quelle part du rendement de la strategie est "gratuite" (simple exposition au marche) et quelle part est un vrai travail de la strategie.
- Un hedge fund qui annonce 15%/an avec un beta de 1 sur le S&P ne fait rien de plus que du long marche avec du levier. Un fonds qui fait 8%/an avec un beta de 0.2 apporte un vrai alpha.

Calcul concret dans le code:

- `np.cov(strat, bench)[0, 1]` donne la covariance entre les deux series de returns journaliers.
- `np.var(bench)` donne la variance du benchmark.
- C'est la pente de la regression lineaire `r_strat = alpha + beta * r_bench + epsilon`.

Pour nos strategies:

- Momentum simple devrait avoir un beta < 1 (on est flat une partie du temps).
- Vol targeting devrait avoir un beta encore plus bas (exposition variable).
- AlwaysLong a beta = 1 par definition (c'est le benchmark).

### 2.2 Alpha

Formule:

- `alpha_daily = mean(r_strat) - beta * mean(r_bench)`
- `alpha_annual = alpha_daily * trading_days`

Ce que c'est:

- L'alpha mesure le **rendement residuel** de la strategie, une fois qu'on a retire la part expliquee par le benchmark.
- C'est la reponse a la question: "est-ce que cette strategie fait mieux que simplement etre expose au marche avec le meme beta?"

Intuition financiere:

- Si `alpha > 0`: la strategie genere du rendement au-dela de ce que son exposition marche explique. C'est la **valeur ajoutee** du gerant ou du signal.
- Si `alpha = 0`: la strategie ne fait que repliquer une fraction du marche.
- Si `alpha < 0`: la strategie detruit de la valeur par rapport a une exposition passive equivalente.

Attention:

- Un alpha positif in-sample ne prouve rien sans validation out-of-sample.
- L'alpha depend du choix du benchmark. Changer de benchmark change l'alpha.
- L'alpha est souvent contamine par les frais de gestion et les couts de transaction (d'ou l'importance de le calculer net de couts, ce qu'on fait ici).

### 2.3 Tracking Error

Formule:

- `tracking_error = std(r_strat - r_bench) * sqrt(trading_days)`

Ce que c'est:

- Le tracking error mesure la **volatilite de la difference** entre la strategie et le benchmark.
- C'est la dispersion autour du rendement relatif.

Intuition financiere:

- Un TE de 0%: la strategie replique parfaitement le benchmark (ETF indiciel).
- Un TE de 5%: la strategie s'ecarte moderement du benchmark.
- Un TE de 20%: la strategie fait quelque chose de tres different du benchmark.

Pour nos strategies:

- AlwaysLong: TE = 0 par definition.
- Momentum: TE modere (flat une partie du temps, donc s'ecarte du benchmark).
- Vol targeting: TE potentiellement plus eleve (exposition variable entre 0 et max_leverage).

### 2.4 Information Ratio

Formule:

- `information_ratio = (annual_return_strat - annual_return_bench) / tracking_error`

Ce que c'est:

- L'information ratio mesure le **rendement actif par unite de risque actif**.
- C'est le Sharpe du "pari" qu'on prend en s'ecartant du benchmark.

Intuition financiere:

- IR > 0: on est recompense pour s'etre ecarte du benchmark.
- IR < 0: on aurait mieux fait de rester sur le benchmark.
- IR > 0.5: considere comme bon dans l'industrie.
- IR > 1.0: exceptionnel (rarement soutenu sur longue periode).

Relation avec le Sharpe et l'alpha:

- Le Sharpe mesure la performance absolue ajustee du risque total.
- L'IR mesure la performance **relative** ajustee du risque **actif** (l'ecart au benchmark).
- Une strategie peut avoir un bon Sharpe (parce qu'elle est longue sur un marche qui monte) mais un mauvais IR (parce qu'elle ne bat pas le benchmark).

Cas particulier important:

- Si `tracking_error = 0` (la strategie est identique au benchmark), l'IR est indefini (`np.nan`).

---

## 3) Benchmark utilise

Le benchmark choisi est `data["return"]`, c'est-a-dire le buy-and-hold de l'actif sous-jacent.

- Pour SPY: le rendement journalier de SPY (equivalent a `AlwaysLongStrategy`).
- Pour BTC: le rendement journalier de BTC-USD.

Pourquoi ce choix:

- C'est le benchmark naturel: on teste si le signal momentum apporte quelque chose vs simplement etre long.
- En pratique, pour un actif unique, la question est: "est-ce que timer le marche fait mieux que ne pas timer?"

Limite:

- Ce benchmark ne tient pas compte du risk-free rate comme alternative (on pourrait aussi comparer vs cash).
- Pour du cross-sectional momentum (plusieurs actifs), le benchmark serait un portefeuille equi-pondere ou cap-weighted.

---

## 4) Synthese: ce qu'on sait mesurer maintenant

| Metrique | Question a laquelle elle repond |
|---|---|
| total_return | Combien la strategie a gagne au total? |
| annual_return | Combien par an en moyenne? |
| annual_vol | Quel risque (dispersion des rendements)? |
| sharpe | Rendement excessif (vs cash) par unite de risque total? |
| max_drawdown | Pire perte depuis un sommet? |
| n_trades | Combien de fois on a trade? |
| total_cost | Combien les frictions ont coute? |
| time_in_market | Quelle fraction du temps on est investi? |
| beta | Quelle sensibilite au benchmark? |
| alpha | Quel rendement en plus de l'exposition marche? |
| tracking_error | Quelle volatilite de l'ecart au benchmark? |
| information_ratio | Rendement actif par unite de risque actif? |

---

## 5) Modifications techniques effectuees

### `src/config.py`

- Ajout `TRADING_DAYS_CRYPTO = 365`

### `src/metrics.py`

- Suppression de `from src.config import TRADING_DAYS`
- Signature: `compute_metrics(result, risk_free_rate=0.0, trading_days=252, benchmark_return=None)`
- Annualisation (vol, return, Sharpe) via le parametre `trading_days`
- Sharpe corrige: `(daily_mean - daily_rf) / daily_vol * sqrt(trading_days)`
- Bloc conditionnel alpha/beta/TE/IR si `benchmark_return` est fourni

### `src/strategy.py`

- Suppression de `from src.config import TRADING_DAYS`
- `MomentumVolTargetingStrategy`: nouveau parametre `trading_days=252`
- `rolling_vol_annual` utilise `self.trading_days` au lieu du global

### `main.py`

- Import de `RISK_FREE_RATE` depuis config
- Detection automatique: `trading_days = 365` si ticker contient "BTC" ou "ETH", sinon `252`
- `benchmark = data["return"]` (buy & hold de l'actif)
- `trading_days` passe a `MomentumVolTargetingStrategy`
- Tous les appels `compute_metrics()` recoivent `risk_free_rate`, `trading_days`, `benchmark_return`

---

## 6) Correction du calcul de beta

Date: 2026-05-03

Probleme repere:

- Quand `AlwaysLongStrategy` est comparee a son propre benchmark (`data["return"]`), on doit obtenir exactement:
  - `beta = 1`
  - `alpha = 0`
  - `tracking_error = 0`
  - `information_ratio = NaN`

Avant correction:

- `beta` sortait tres legerement au-dessus de `1` (`1.00027...` sur BTC).
- `alpha` sortait tres legerement negatif.

Cause:

- `np.cov()` utilisait une normalisation en `N-1`.
- `np.var()` utilisait une normalisation en `N`.
- Les deux estimateurs n'avaient donc pas exactement la meme convention.

Correction:

- `beta = np.cov(strat, bench, ddof=0)[0, 1] / np.var(bench, ddof=0)`
- Ajout d'un garde-fou si la variance du benchmark vaut `0`.

Test ajoute:

- `AlwaysLongStrategy` vs `benchmark_return=data["return"]` doit donner:
  - `beta` proche de `1`;
  - `alpha` proche de `0`;
  - `tracking_error` proche de `0`;
  - `information_ratio = NaN`.

Lecture:

- Ce fix ne change pas la logique financiere.
- Il rend surtout la metrique plus propre et verifiable: le benchmark passif devient un test sanity exact.
