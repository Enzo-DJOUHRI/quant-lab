# Rapport Test Strategies - Format Standard

Date: 2026-03-15

Perimetre:

- Donnees principales: `SPY` (single-asset) et `SPY/QQQ` (spread multi-actifs)
- Periode: 2015-01-01 -> 2024-12-31
- Ce document suit le format standard defini pour la gestion/test des strategies.

## 1) AlwaysLong SPY

Nom : AlwaysLong SPY  
Famille : Trend / Buy & Hold passif  
Actif(s) : SPY  
Benchmark : SPY passif (reference de marche)

Hypothese : rester investi en permanence capte la tendance long terme du marche US.  
Signal : constant a 1.  
Pourquoi ca pourrait marcher : prime de risque actions de long terme.  
Pourquoi ca peut echouer : drawdowns profonds en regime baissier.

Metrics :
- Total return : 247.08%
- Annual return : 13.28%
- Annual vol : 17.62%
- Sharpe : 0.786
- Max drawdown : -33.72%

Plots :
- Equity : `outputs/plots/equity_curve_comparison.html`
- Drawdown : `outputs/plots/drawdown_curve_comparison.html`
- Price/Signal : N/A (signal constant)

Lecture :
- points forts : performance brute elevee, baseline claire.
- points faibles : risque de drawdown eleve.
- robustesse apparente : correcte sur cycle long.
- interet reel potentiel : tres bon benchmark de reference.

Verdict :
- Orange
- suite a donner : conserver comme benchmark principal.

---

## 2) Momentum 5 SPY

Nom : Momentum 5 SPY  
Famille : Trend following  
Actif(s) : SPY  
Benchmark : AlwaysLong SPY

Hypothese : la tendance tres courte se prolonge a court terme.  
Signal : long si momentum 5j > 0, sinon flat.  
Pourquoi ca pourrait marcher : filtrage partiel des phases negatives.  
Pourquoi ca peut echouer : bruit court terme / whipsaws.

Metrics :
- Total return : 52.86%
- Annual return : 4.35%
- Annual vol : 10.94%
- Sharpe : 0.444
- Max drawdown : -16.31%

Plots :
- Equity : `outputs/plots/equity_curve_comparison.html`
- Drawdown : `outputs/plots/drawdown_curve_comparison.html`
- Price/Signal : `outputs/plots/price_signal_momentum_5.html`

Lecture :
- points forts : drawdown nettement reduit.
- points faibles : forte perte de rendement.
- robustesse apparente : moyenne (signal nerveux).
- interet reel potentiel : filtre defensif, mais peu attractif seul.

Verdict :
- Orange
- suite a donner : ne pas prioriser sans filtre supplementaire.

---

## 3) Momentum 10 SPY

Nom : Momentum 10 SPY  
Famille : Trend following  
Actif(s) : SPY  
Benchmark : AlwaysLong SPY

Hypothese : un momentum un peu moins court reduit le bruit.  
Signal : long si momentum 10j > 0, sinon flat.  
Pourquoi ca pourrait marcher : meilleur compromis reactivite/stabilite.  
Pourquoi ca peut echouer : retard en retournement rapide.

Metrics :
- Total return : 135.43%
- Annual return : 8.96%
- Annual vol : 10.46%
- Sharpe : 0.873
- Max drawdown : -15.14%

Plots :
- Equity : `outputs/plots/equity_curve_comparison.html`
- Drawdown : `outputs/plots/drawdown_curve_comparison.html`
- Price/Signal : `outputs/plots/price_signal_momentum_10.html`

Lecture :
- points forts : Sharpe eleve, drawdown contenu.
- points faibles : rendement brut sous AlwaysLong.
- robustesse apparente : bonne.
- interet reel potentiel : tres bon candidat "equilibre".

Verdict :
- Vert
- suite a donner : conserver comme variante forte de momentum.

---

## 4) Momentum 20 SPY

Nom : Momentum 20 SPY  
Famille : Trend following  
Actif(s) : SPY  
Benchmark : AlwaysLong SPY

Hypothese : la tendance 1 mois capture mieux les regimes persistants.  
Signal : long si momentum 20j > 0, sinon flat.  
Pourquoi ca pourrait marcher : filtrage drawdown + suivi de tendance stable.  
Pourquoi ca peut echouer : sous-performance lors de rebonds rapides.

Metrics :
- Total return : 151.63%
- Annual return : 9.69%
- Annual vol : 10.53%
- Sharpe : 0.931
- Max drawdown : -13.34%

Plots :
- Equity : `outputs/plots/equity_curve_comparison.html`
- Drawdown : `outputs/plots/drawdown_curve_comparison.html`
- Price/Signal : `outputs/plots/price_signal_momentum_20.html`

Lecture :
- points forts : meilleur Sharpe du lot momentum SPY.
- points faibles : rendement toujours sous AlwaysLong.
- robustesse apparente : tres bonne.
- interet reel potentiel : candidat principal momentum.

Verdict :
- Vert
- suite a donner : prioritaire pour extension multi-actifs.

---

## 5) Momentum 50 SPY

Nom : Momentum 50 SPY  
Famille : Trend following  
Actif(s) : SPY  
Benchmark : AlwaysLong SPY

Hypothese : un horizon long filtre davantage le bruit.  
Signal : long si momentum 50j > 0, sinon flat.  
Pourquoi ca pourrait marcher : moins de faux signaux.  
Pourquoi ca peut echouer : lag important.

Metrics :
- Total return : 106.20%
- Annual return : 7.52%
- Annual vol : 11.13%
- Sharpe : 0.708
- Max drawdown : -21.08%

Plots :
- Equity : `outputs/plots/equity_curve_comparison.html`
- Drawdown : `outputs/plots/drawdown_curve_comparison.html`
- Price/Signal : `outputs/plots/price_signal_momentum_50.html`

Lecture :
- points forts : simplifie le signal.
- points faibles : drawdown remonte, perf baisse vs 10/20.
- robustesse apparente : moyenne.
- interet reel potentiel : secondaire.

Verdict :
- Orange
- suite a donner : garder en reference, pas en priorite.

---

## 6) Momentum 100 SPY

Nom : Momentum 100 SPY  
Famille : Trend following  
Actif(s) : SPY  
Benchmark : AlwaysLong SPY

Hypothese : tres long horizon = filtre maximal.  
Signal : long si momentum 100j > 0, sinon flat.  
Pourquoi ca pourrait marcher : tres peu de bruit.  
Pourquoi ca peut echouer : strategie trop lente.

Metrics :
- Total return : 119.73%
- Annual return : 8.21%
- Annual vol : 11.78%
- Sharpe : 0.729
- Max drawdown : -18.95%

Plots :
- Equity : `outputs/plots/equity_curve_comparison.html`
- Drawdown : `outputs/plots/drawdown_curve_comparison.html`
- Price/Signal : `outputs/plots/price_signal_momentum_100.html`

Lecture :
- points forts : stabilite relative.
- points faibles : compromis moins bon que 10/20.
- robustesse apparente : moyenne.
- interet reel potentiel : limite vs alternatives momentum.

Verdict :
- Orange
- suite a donner : conserver uniquement pour comparaison.

---

## 7) MeanReversion Price 20 z=1.0 SPY

Nom : MeanReversion Price 20 z=1.0  
Famille : Mean reversion  
Actif(s) : SPY  
Benchmark : AlwaysLong SPY

Hypothese : ecarts faibles autour de la moyenne reviennent vite.  
Signal : long si z < -1, short si z > 1.  
Pourquoi ca pourrait marcher : capter des sur-reactions courtes.  
Pourquoi ca peut echouer : contre-tendance en marche haussier.

Metrics :
- Total return : -13.76%
- Annual return : -1.47%
- Annual vol : 13.67%
- Sharpe : -0.040
- Max drawdown : -43.95%

Plots :
- Equity : `outputs/plots/equity_curve_comparison.html`
- Drawdown : `outputs/plots/drawdown_curve_comparison.html`
- Price/Signal : `outputs/plots/price_signal_meanrev20_z1_0.html`

Lecture :
- points forts : reactivite forte.
- points faibles : destruction de performance, drawdown eleve.
- robustesse apparente : faible.
- interet reel potentiel : faible dans ce regime.

Verdict :
- Rouge
- suite a donner : a eviter sous cette forme.

---

## 8) MeanReversion Price 20 z=1.5 SPY

Nom : MeanReversion Price 20 z=1.5  
Famille : Mean reversion  
Actif(s) : SPY  
Benchmark : AlwaysLong SPY

Hypothese : seuil intermediaire limite les faux signaux.  
Signal : long si z < -1.5, short si z > 1.5.  
Pourquoi ca pourrait marcher : moins de bruit que z=1.  
Pourquoi ca peut echouer : encore trop de shorts contre tendance.

Metrics :
- Total return : 34.25%
- Annual return : 3.00%
- Annual vol : 10.25%
- Sharpe : 0.339
- Max drawdown : -11.51%

Plots :
- Equity : `outputs/plots/equity_curve_comparison.html`
- Drawdown : `outputs/plots/drawdown_curve_comparison.html`
- Price/Signal : `outputs/plots/price_signal_meanrev20_z1_5.html`

Lecture :
- points forts : drawdown mieux controle.
- points faibles : rendement encore faible.
- robustesse apparente : moyenne-faible.
- interet reel potentiel : defensif uniquement.

Verdict :
- Orange
- suite a donner : garder comme point intermediaire, sans priorite.

---

## 9) MeanReversion Price 20 z=2.0 SPY

Nom : MeanReversion Price 20 z=2.0  
Famille : Mean reversion  
Actif(s) : SPY  
Benchmark : AlwaysLong SPY

Hypothese : seuil plus strict capte les ecarts extremes.  
Signal : long si z < -2, short si z > 2.  
Pourquoi ca pourrait marcher : moins de bruit, profils plus qualitatifs.  
Pourquoi ca peut echouer : peu de trades, sous-exposition.

Metrics :
- Total return : 49.45%
- Annual return : 4.11%
- Annual vol : 6.51%
- Sharpe : 0.650
- Max drawdown : -8.19%

Plots :
- Equity : `outputs/plots/equity_curve_comparison.html`
- Drawdown : `outputs/plots/drawdown_curve_comparison.html`
- Price/Signal : `outputs/plots/price_signal_meanrev20_z2_0.html`

Lecture :
- points forts : excellent controle du risque.
- points faibles : performance absolue limitee.
- robustesse apparente : bonne cote risque.
- interet reel potentiel : brique defensive complementaire.

Verdict :
- Orange
- suite a donner : utile en combinaison, pas seul.

---

## 10) MeanReversion Price 20 z=2.5 SPY

Nom : MeanReversion Price 20 z=2.5  
Famille : Mean reversion  
Actif(s) : SPY  
Benchmark : AlwaysLong SPY

Hypothese : tres fort filtrage des signaux.  
Signal : long si z < -2.5, short si z > 2.5.  
Pourquoi ca pourrait marcher : signals tres "propres".  
Pourquoi ca peut echouer : quasi aucune exposition.

Metrics :
- Total return : 3.15%
- Annual return : 0.31%
- Annual vol : 3.07%
- Sharpe : 0.117
- Max drawdown : -8.19%

Plots :
- Equity : `outputs/plots/equity_curve_comparison.html`
- Drawdown : `outputs/plots/drawdown_curve_comparison.html`
- Price/Signal : `outputs/plots/price_signal_meanrev20_z2_5.html`

Lecture :
- points forts : risque faible.
- points faibles : rendement quasi nul.
- robustesse apparente : faible economiquement.
- interet reel potentiel : tres limite.

Verdict :
- Rouge
- suite a donner : non prioritaire.

---

## 11) MeanReversion Return 20 z=2 SPY

Nom : MeanReversion Return 20 z=2  
Famille : Mean reversion (returns)  
Actif(s) : SPY  
Benchmark : AlwaysLong SPY

Hypothese : les rendements extremes reviennent vers leur moyenne locale.  
Signal : long si z(return) < -2, short si z(return) > 2.  
Pourquoi ca pourrait marcher : detection plus directe des chocs de rendement.  
Pourquoi ca peut echouer : faux retours a la moyenne en regime trend.

Metrics :
- Total return : 45.92%
- Annual return : 3.86%
- Annual vol : 6.39%
- Sharpe : 0.624
- Max drawdown : -10.77%

Plots :
- Equity : `outputs/plots/equity_curve_comparison.html`
- Drawdown : `outputs/plots/drawdown_curve_comparison.html`
- Price/Signal : Non genere (a ajouter)

Lecture :
- points forts : profil defensif propre.
- points faibles : rendement absolu modeste.
- robustesse apparente : correcte sur SPY.
- interet reel potentiel : interessant en diversification de moteurs.

Verdict :
- Orange
- suite a donner : tester en multi-actifs et en combinaison regime filter.

---

## 12) SpreadMeanReversion SPY/QQQ z=2

Nom : SpreadMeanReversion SPY/QQQ z=2  
Famille : Stat arb / spread mean reversion  
Actif(s) : SPY, QQQ  
Benchmark : benchmark spread passif a construire (et reference SPY/QQQ buy & hold)

Hypothese : le ratio SPY/QQQ revient vers une moyenne locale apres ecart excessif.  
Signal : long spread si z(spread) < -2, short spread si z(spread) > 2.  
Pourquoi ca pourrait marcher : co-mouvement structurel entre indices US larges/tech.  
Pourquoi ca peut echouer : rupture de regime, spread non stationnaire.

Metrics :
- Total return : 1.28%
- Annual return : 0.13%
- Annual vol : 3.11%
- Sharpe : 0.057
- Max drawdown : -8.47%

Plots :
- Equity : `outputs/plots/equity_curve_comparison.html` (comparatif global)
- Drawdown : `outputs/plots/drawdown_curve_comparison.html` (comparatif global)
- Price/Signal : Non genere (a ajouter pour spread + z-score)

Lecture :
- points forts : risque modere, logique de spread coherente.
- points faibles : rendement faible dans ce setup.
- robustesse apparente : encore faible (premier test multi-actifs).
- interet reel potentiel : present, mais depend fortement du choix de paire/regime.

Verdict :
- Orange
- suite a donner : priorite a l'etude de corrélation/cointegration et au filtrage regime avant extension.
