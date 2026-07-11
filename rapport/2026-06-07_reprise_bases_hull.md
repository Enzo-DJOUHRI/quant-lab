# Reprise bases Hull - forwards, futures, taux, options

Date : 2026-06-07

## 1) Contexte

Premier week-end de la roadmap ete 2026.

Le samedi 2026-06-06 n'a pas ete utilise. On ne rattrape pas violemment :
la session du dimanche sert a relancer proprement le projet.

Point de depart reel :

- Hull : arbres binomiaux deja termines.
- Arret actuel Hull : avant le chapitre GBM / Ito.
- Choix pedagogique : consolider Shreve I en temps discret avant de
  passer au continu, a BSM, aux greeks et a la volatilite.

Objectif de la session :

- reprendre rapidement les bases Hull utiles ;
- verifier les conventions et formules essentielles ;
- preparer la transition vers Shreve I chap 1.

## 2) Plan de session conseille

Charge cible aujourd'hui : 2h30 a 3h.

1. Reprise rapide des taux et discounting - 25 min.
2. Forwards / futures / cost of carry - 35 min.
3. Options, payoffs, moneyness, parite put-call - 55 min.
4. Strategies options de base - 30 min si energie.
5. Synthese + questions pour Shreve I - 15 min.

Regle : si l'energie baisse, on coupe apres la parite put-call. Les
strategies options peuvent attendre.

## 3) Taux et actualisation

Notions a revoir :

- taux discret vs taux compose continu ;
- facteur d'actualisation `exp(-rT)` ;
- valeur future `S * exp(rT)` ;
- maturite `T` exprimee en annees dans les modeles.

Formules utiles :

```text
PV = FV * exp(-rT)
FV = PV * exp(rT)
```

Questions de controle :

- Pourquoi une formule BSM attend-elle `T` en annees et pas en jours ?
- Que se passe-t-il si on utilise `T = 30` au lieu de `T = 30 / 365` ?
- Quelle convention de taux utilise-t-on dans BSM ?

## 4) Forwards et futures

Notions a revoir :

- un forward est un contrat d'achat/vente a terme ;
- payoff long forward a maturite : `S_T - K` ;
- prix forward sans dividende : `F_0 = S_0 * exp(rT)` ;
- avec dividende continu : `F_0 = S_0 * exp((r - q)T)`.

Intuition no-arbitrage :

- si le forward est trop cher, on achete le sous-jacent finance par
  emprunt et on vend le forward ;
- si le forward est trop bas, on short le sous-jacent, on place le cash,
  et on achete le forward.

Questions de controle :

- Quelle difference entre prix forward `F_0` et valeur du contrat
  forward au temps 0 ?
- Pourquoi le forward converge-t-il vers le spot a maturite ?
- Quel est l'effet d'un dividende continu `q` sur le prix forward ?

Mini-exercice :

```text
S0 = 100
r = 5%
q = 0%
T = 0.5

Calculer F0.
```

Checkpoint attendu :

```text
F0 = 100 * exp(0.05 * 0.5) ~= 102.53
```

## 5) Options vanilla

Notions a revoir :

- call europeen : droit d'acheter a `K` ;
- put europeen : droit de vendre a `K` ;
- payoff call : `max(S_T - K, 0)` ;
- payoff put : `max(K - S_T, 0)` ;
- valeur intrinseque vs valeur temps ;
- ITM / ATM / OTM ;
- option europeenne vs option americaine.

Questions de controle :

- Pourquoi une option a une valeur temps positive avant maturite ?
- Pourquoi un call europeen sans dividende ne devrait-il pas etre
  exerce avant maturite ?
- Pourquoi un put americain peut-il valoir plus qu'un put europeen ?

## 6) Parite put-call

Formule sans dividende :

```text
C - P = S - K * exp(-rT)
```

Avec dividende continu :

```text
C - P = S * exp(-qT) - K * exp(-rT)
```

Interpretation :

- long call + cash actualise du strike reproduit long put + action ;
- si la relation est violee, il existe une strategie d'arbitrage.

Mini-exercice :

```text
S = 100
K = 100
r = 5%
T = 1
C = 10

Quel doit etre P par parite put-call ?
```

Checkpoint attendu :

```text
P = C - S + K * exp(-rT)
P ~= 10 - 100 + 95.12
P ~= 5.12
```

## 7) Strategies options de base

A revoir rapidement :

- covered call : long stock + short call ;
- protective put : long stock + long put ;
- bull call spread : long call bas strike + short call haut strike ;
- bear put spread : long put haut strike + short put bas strike ;
- straddle : long call + long put meme strike ;
- strangle : long call OTM + long put OTM ;
- butterfly : pari sur faible mouvement autour d'un strike central.

Questions de controle :

- Quelle strategie gagne si le sous-jacent bouge beaucoup, peu importe
  le sens ?
- Quelle strategie vend de l'upside contre une prime ?
- Quelle strategie protege une position long stock contre une baisse ?

## 8) Lien avec Shreve I

Ce que Shreve I va formaliser :

- le no-arbitrage ;
- la replication ;
- la probabilite neutre au risque ;
- le prix comme esperance actualisee ;
- la martingale du prix actualise ;
- les options americaines comme probleme d'arret optimal.

La bonne question pour la suite :

```text
Dans un arbre binomial, pourquoi le prix obtenu par replication est-il
egal au prix obtenu par esperance sous probabilite neutre au risque ?
```

## 9) Bilan de session

A completer en fin de session :

- Concepts vraiment compris :
- Concepts encore flous :
- Formule(s) a memoriser :
- Mini-exercice(s) reussis :
- Prochaine etape :

Prochaine etape conseillee :

- Shreve I chap 1 ;
- arbre binomial 1-step a refaire a la main ;
- implementation `src/derivatives/binomial.py` en v0.
