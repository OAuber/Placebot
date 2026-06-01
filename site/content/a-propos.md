---
title: "À propos de Placebot"
description: "Pourquoi et comment Placebot évalue les candidats contre Placebo 1er."
---

## 🤔 Pourquoi Placebot ?

Placebot est né d'une question simple : **et si on évaluait les programmes politiques comme on évalue les médicaments ?**

En médecine, avant de prescrire un traitement, on vérifie :
1. **Son efficacité** (est-ce que ça marche ?)
2. **Ses effets secondaires** (est-ce que ça fait plus de mal que de bien ?)
3. **Son innocuité** (est-ce que c'est sans danger ?)

Or, **aucun programme politique n'a jamais été testé en double aveugle**. Pourtant, leurs effets secondaires sont bien réels :
- Polarisation de la société,
- Anxiété collective,
- Désillusion démocratique.

**Placebot applique donc la méthodologie de la médecine factuelle à la politique** :
- **Placebo 1er** = le groupe témoin (score de toxicité : 0).
- Chaque candidat = un traitement actif à évaluer.

---

## 🔬 Méthodologie

### 1. **Collecte des données**
Placebot récupère automatiquement :
- Les **programmes officiels** des candidats,
- Leurs **dernières déclarations** (via des sources médiatiques fiables),
- Les **analyses d'experts** (économistes, politologues, etc.).

### 2. **Évaluation par Mistral**
Chaque mesure est analysée selon 4 critères :
   Critère | Description | Score Placebo 1er |
 |---------|-------------|-------------------|
 | **Toxicité** | Risque de conflits, polarisation, ou instabilité. | 0 |
 | **Effet nocebo** | Anxiété ou stress collectif généré. | 0 |
 | **Innocuité** | Impact sur la cohésion sociale (100 = neutre). | 100 |
 | **Efficacité prouvée** | Preuves scientifiques ou historiques. | 0 |

### 3. **Score global**
Le score global d'un candidat est calculé ainsi :
Score = (Toxicité × 0.4) + (Effet nocebo × 0.3) + ((100 - Innocuité) × 0.3)

*Plus le score est bas, mieux c'est.*

---

## 🍌 Qui est Placebo 1er ?

**Placebo 1er** est le candidat du [Parti Placebo](https://olivierauber.medium.com/placebo-un-art-politique-561ba040bcf), un laboratoire d'art cognitif dédié à la démocratie factuelle.

Son programme :
- **Ne pas se présenter** à l'élection (Protocole de Non-Candidature Active),
- **Ne proposer aucune mesure** (sauf des mesures placebo comme le Nuage de Points Vide),
- **Être le groupe témoin** contre lequel évaluer tous les autres candidats.

**Pourquoi ?**
Parce que l'histoire montre que :
- Les promesses électorales sont rarement tenues,
- Les réformes ont souvent des effets pervers imprévus,
- L'abstention ou le vote blanc sont rarement comptabilisés comme des choix actifs.

Placebo 1er **assume cette réalité** : son "programme" est de **ne rien faire**, et son score est donc **0 en toxicité**.

---

## 🛠️ Technologies utilisées

Placebot est un projet **open source** utilisant :
- **Python** pour le scraping et l'analyse,
- **Mistral AI** pour les évaluations,
- **Hugo** pour générer le site statique,
- **GitHub Actions** pour l'automatisation.

**Coût** : ~10 €/an (principalement pour les appels à l'API Mistral).

---
## 📜 Licence

Ce projet est sous licence **MIT**. Vous êtes libre de :
- L'utiliser,
- Le modifier,
- Le redistribuer.

**Attribution** : Un lien vers [le dépôt GitHub](https://github.com/OAuber/Placebot) est apprécié.

---
## 📧 Contact

Pour toute question ou suggestion :
- Ouvrez une **issue** sur [GitHub](https://github.com/OAuber/Placebot),
- Ou contactez [Olivier Auber](https://olivierauber.medium.com/).
