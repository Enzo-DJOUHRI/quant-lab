# Code Fixing Report

Date: 2026-03-09

## 1. Problème observé

En exécutant `main.py`, un dossier `data/raw` était recréé alors qu'il existait déjà.

## 2. Cause racine

Le code utilisait un chemin **relatif**:

- `os.path.join("data", "raw", f"{ticker}.csv")`
- `os.makedirs("data/raw", exist_ok=True)`

Un chemin relatif dépend du dossier courant d'exécution (`cwd`).
Si le script est lancé depuis un autre dossier (ex: `src/`), Python peut créer `src/data/raw` au lieu de `data/raw` à la racine du projet.

## 3. Modifications appliquées

Fichier modifié: `src/data_loader.py`

- Remplacement de `os` par `pathlib.Path`.
- Définition d'un chemin absolu basé sur le fichier:
  - `project_root = Path(__file__).resolve().parent.parent`
  - `self.file_path = project_root / "data" / "raw" / f"{ticker}.csv"`
- Vérification d'existence avec `self.file_path.exists()`.
- Création du dossier cible avec:
  - `self.file_path.parent.mkdir(parents=True, exist_ok=True)`

## 4. Validation

Commande exécutée: `python3 main.py`

Résultat:

- Exécution OK.
- Le CSV existant est bien lu.
- Aucun nouveau dossier parasite `src/data/` n'a été créé.

## 5. Leçon à retenir

Pour les fichiers de projet, préférer des chemins construits depuis `__file__` (ou une racine projet explicite) plutôt que des chemins relatifs au dossier courant.

---

## 6. Ajout - Export des plots en HTML (VSCode terminal)

Contexte:

- Dans le terminal VSCode (hors notebook), `fig.show()` n'ouvre pas l'affichage interactif comme en `.ipynb`.

Modifications appliquées:

- Dossier créé: `outputs/plots/` (avec `.gitkeep`).
- Fichier modifié: `src/plots.py`
  - ajout de `Path` pour gérer le dossier de sortie;
  - `BacktestPlotter` accepte `output_dir="outputs/plots"`;
  - remplacement de `fig.show()` par:
    - création du dossier si besoin;
    - `fig.write_html("outputs/plots/equity_curve_comparison.html", include_plotlyjs="cdn")`;
    - affichage du chemin du fichier généré dans le terminal.

Validation:

- Commande: `python3 main.py`
- Résultat: fichier généré avec succès dans:
  - `outputs/plots/equity_curve_comparison.html`

---

## 7. Correction - FutureWarning pandas (chained assignment)

Date: 2026-03-10

Problème observé:

- Warning à l'exécution sur `self.data["signal"].fillna(0, inplace=True)` dans `src/strategy.py`.

Cause:

- Pattern `inplace=True` sur une sélection de colonne (`self.data["signal"]`) qui peut être vue comme une copie.
- Ce comportement est déprécié et cassera en pandas 3.0.

Modification appliquée:

- Fichier modifié: `src/strategy.py`
- Remplacement par une affectation explicite:
  - `self.data["signal"] = self.data["raw_signal"].shift(1).fillna(0).astype(int)`

Validation:

- Commande: `python3 main.py`
- Résultat: exécution OK, plus de `FutureWarning` lié à `fillna(inplace=True)`.

---

## 8. Correction - Dossier `outputs/plots` indépendant du cwd

Date: 2026-03-10

Problème:

- Si VSCode est ouvert sur un dossier parent, un chemin relatif `outputs/plots` peut être créé au mauvais niveau.

Modification:

- Fichier modifié: `src/plots.py`
- `output_dir` est maintenant résolu par rapport à la racine projet (`Path(__file__).resolve().parent.parent`) quand un chemin relatif est fourni.

Validation:

- Commande: `python3 main.py`
- Résultat: export confirmé dans:
  - `Quant_Lab/outputs/plots/equity_curve_comparison.html`

---

## 9. Durcissement `data_loader` (CSV vides/invalides)

Date: 2026-03-12

Problème:

- Lors de tentatives multi-actifs, certains CSV vides pouvaient être réutilisés silencieusement.

Correction appliquée:

- Fichier modifié: `src/data_loader.py`
- Si le CSV cache est vide ou n'a pas les colonnes attendues (`price`, `return`), il est ignoré.
- Si le téléchargement ne renvoie aucune donnée, une erreur claire est levée.
- Compatibilité ajoutée pour la colonne `Close` en format yfinance multi-index ou simple index.

Validation:

- Lecture `SPY` OK.
- Les actifs sans données exploitables lèvent désormais une erreur explicite au lieu d'un faux résultat.

---

## 10. Ajustement de lisibilité `data_loader`

Date: 2026-03-13

Contexte:

- Demande de revenir à une version plus proche du code initial.

Modification appliquée:

- La structure de `src/data_loader.py` a été simplifiée (flux plus direct, style aligné avec ta version d'origine).
- Les robustesses critiques ont été conservées:
  - contrôle CSV cache vide/invalide;
  - erreur claire si téléchargement vide;
  - gestion `Close` multi-index/single-index.

Validation:

- Test local `SPY` OK (`2514` lignes, colonnes `price`/`return`).

---

## 11. Robustification `load_multi` (DataLoader)

Date: 2026-03-13

Objectif:

- Aligner la robustesse de `load_multi` sur `load_mono`.

Modifications appliquées (`src/data_loader.py`):

- Validation du cache CSV multi-actifs:
  - vérifie que le fichier n'est pas vide;
  - vérifie la présence de toutes les colonnes attendues (`{ticker}_price`, `{ticker}_return`).
- Téléchargement multi-actifs:
  - gère explicitement les formats yfinance multi-index et single-index;
  - vérifie que la colonne `Close` existe;
  - vérifie que tous les tickers demandés sont présents dans les données reçues.
- Qualité des données:
  - suppression des lignes totalement vides;
  - erreur explicite si aucun dataset exploitable;
  - erreur explicite si des tickers manquent.

Validation:

- Compilation Python OK (`py_compile`).
- Test de lecture cache multi (fichier test) OK: structure retournée conforme.

### 11.1 Pourquoi colonnes separées en multi ici (vs Markowitz)

Contexte compare:

- Projet Markowitz (dossier parent):
  - workflow orienté matrice unique de prix (`datas["Close"]`) puis matrice unique de rendements;
  - objectif principal: statistiques portefeuille (moyennes/covariance/Monte Carlo), sans logique signal par actif stockée dans le même tableau.
- Quant_Lab:
  - workflow orienté moteur de stratégie/backtest actif par actif;
  - besoin de conserver dans le même dataset les prix et rendements prêts à l'emploi par ticker, pour enchaîner signaux, équity, drawdown, exports CSV.

Pourquoi le format `{ticker}_price` / `{ticker}_return` a été conservé:

- Lisible dans les CSV de cache.
- Simple à brancher sur des traitements stratégiques qui consomment explicitement prix + return.
- Évite la complexité de colonnes multi-index dans les étapes aval (reporting, debug, merge).

Conclusion:

- Le style Markowitz est plus compact pour l'optimisation de portefeuille pure.
- Le style Quant_Lab (colonnes séparées) est plus pratique pour un moteur de stratégies multi-étapes.

---

## 12. Momentum - Couts de transaction (clarification + tests)

Date: 2026-03-20

Modifications code:

- `src/strategy.py`
  - ajout/clarification de `transaction_cost_paid`;
  - `strategy_return` calcule explicitement en net de `transaction_cost_paid`.
- `src/metrics.py`
  - `total_cost` lit uniquement `transaction_cost_paid`.
- `main.py`
  - affichage mis a jour sur la colonne `transaction_cost_paid`.

Tests ajoutes:

- `tests/test_momentum_transaction_costs.py`
  - coherence de `trade_size`;
  - coherence de `transaction_cost_paid`;
  - coherence de `strategy_return` net;
  - verification de `n_trades`, `total_cost`, `time_in_market`.

Validation:

- Commande: `python3 -m unittest discover -s tests -v`
- Resultat: 3 tests OK.

Rapport d'analyse associe:

- `rapport/2026-03-20_momentum_couts_transaction.md`

---

## 13. Correction - Beta benchmark coherent

Date: 2026-05-03

Probleme:

- `AlwaysLongStrategy` comparee a son propre benchmark devait donner `beta = 1` et `alpha = 0`.
- Le calcul sortait un beta tres legerement superieur a `1`, car `np.cov()` et `np.var()` n'utilisaient pas la meme convention de normalisation.

Correction:

- Fichier modifie: `src/metrics.py`
- `np.cov(strat, bench, ddof=0)` et `np.var(bench, ddof=0)` utilisent maintenant la meme convention.
- Ajout d'un garde-fou si la variance du benchmark vaut `0`.

Test ajoute:

- Fichier modifie: `tests/test_momentum_transaction_costs.py`
- `AlwaysLongStrategy` vs `benchmark_return=data["return"]` verifie:
  - `beta ~= 1`
  - `alpha ~= 0`
  - `tracking_error ~= 0`
  - `information_ratio = NaN`

Validation:

- `python3 -m unittest discover -s tests -p 'test_*.py'` passe (`4` tests).
