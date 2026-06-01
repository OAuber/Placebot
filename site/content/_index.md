---
title: "Classement Placebot 2027"
description: "Classement des candidats à la présidentielle 2027 évalués contre Placebo 1er."
---

## 🏆 Classement des candidats (vs. Placebo 1er)

*Mis à jour le {{ now.Format "02/01/2006" }}*
   Rang | Candidat | Parti | Score Global | Toxicité | Effet Nocebo | Innocuité |
 |------|----------|-------|--------------|----------|-------------|-----------|
{{ $classement := readFile "data/evaluations_2026-06-01.json" | transform.Unmarshal }}
{{ range $classement.classement }}
 | {{ .rang }} | [{{ .nom }}]({{ if eq .id "placebo1er" }}#{{ else }}candidats/{{ .id }}{{ end }}) | {{ .parti | default "-" }} | {{ .scores.global }} | {{ .scores.toxicite }} | {{ .scores.nocebo }} | {{ .scores.innocuite }} |
{{ end }}

---

## 📌 À propos de Placebot

**Placebot** est un outil d'évaluation des programmes politiques **contre Placebo 1er**, le candidat de référence du [Parti Placebo](https://olivierauber.medium.com/placebo-un-art-politique-561ba040bcf).

### 🎯 Méthodologie
- **Toxicité** : Risque de polarisation, conflits sociaux, ou instabilité.
- **Effet nocebo** : Anxiété collective générée par la mesure.
- **Innocuité** : Impact sur la cohésion sociale (100 = neutre).

**Placebo 1er** a un score de **0** dans toutes les catégories : c'est la référence absolue.

### 🔗 Liens utiles
- [Manifeste du Parti Placebo](https://olivierauber.medium.com/placebo-un-art-politique-561ba040bcf)
- [Protocole de Non-Candidature 2027](https://olivierauber.medium.com/)
- [Code source du projet](https://github.com/OAuber/Placebot)
