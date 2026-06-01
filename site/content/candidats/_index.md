---
title: "Tous les candidats"
description: "Liste complète des candidats évalués par Placebot."
---

## 📋 Liste des candidats

{{ range readDir "content/candidats" }}
  {{ if ne .Name "_index.md" }}
    {{ $candidat := readFile (path.Join "data/evaluations_2026-06-01.json")   transform.Unmarshal }}
    {{ range $candidat.candidats }}
      {{ if eq .id (replaceRE "\\.md$" "" .Name) }}
        [{{ .nom }}]({{ .id | relURL }}) - {{ .parti }} (Score : {{ .scores.global }}/100)
      {{ end }}
    {{ end }}
  {{ end }}
{{ end }}
