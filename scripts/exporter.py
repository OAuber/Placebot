import json
import os
from datetime import datetime

# Chemin des données
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CANDIDATES_FILE = os.path.join(DATA_DIR, "candidates.json")
EVALUATIONS_DIR = DATA_DIR
FINAL_FILE = os.path.join(DATA_DIR, f"evaluations_{datetime.now().strftime('%Y-%m-%d')}.json")

def load_evaluations():
    """Charge les évaluations les plus récentes"""
    eval_files = [f for f in os.listdir(EVALUATIONS_DIR) if f.startswith("evaluations_")]
    if not eval_files:
        raise FileNotFoundError("Aucun fichier d'évaluations trouvé.")

    latest_file = sorted(eval_files)[-1]
    with open(os.path.join(EVALUATIONS_DIR, latest_file), "r", encoding="utf-8") as f:
        return json.load(f)

def load_candidates():
    """Charge la liste des candidats"""
    with open(CANDIDATES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)["candidats"]

def generate_final_json():
    """Génère le JSON final pour le site"""
    evaluations = load_evaluations()
    candidates_meta = load_candidates()

    # Ajouter Placebo 1er manuellement
    placebo1er = {
        "id": "placebo1er",
        "nom": "Placebo 1er",
        "parti": "Parti Placebo",
        "statut": "non-candidat",
        "score_global": 0,
        "scores": {
            "toxicite": 0,
            "nocebo": 0,
            "innocuite": 100,
            "efficacite_prouvee": 0
        },
        "mesures": [
            {
                "titre": "Non-Candidature Active",
                "texte": "Protocole de non-présentation à l'élection présidentielle 2027.",
                "toxicite": 0,
                "nocebo": 0,
                "innocuite": 100,
                "risques": [],
                "alternative_placebo": "Placebo 1er est sa propre alternative."
            },
            {
                "titre": "Nuage de Points Vide",
                "texte": "Contemplation d'un nuage de points vide pour réduire le stress cortisolique.",
                "toxicite": 0,
                "nocebo": 0,
                "innocuite": 100,
                "risques": [],
                "alternative_placebo": "Déjà appliqué par Placebo 1er."
            },
            {
                "titre": "Reçu de Non-Contrôle",
                "texte": "Document certifiant que nous ne vous avons pas contrôlé.",
                "toxicite": 0,
                "nocebo": 0,
                "innocuite": 100,
                "risques": [],
                "alternative_placebo": "Valeur symbolique infinie."
            }
        ],
        "diagnostic_placebose": {
            "score": 0,
            "type": "immunité totale",
            "prescription": ["Aucun traitement nécessaire.", "Continuez à ignorer Placebo 1er."]
        },
        "evaluated_at": datetime.now().isoformat()
    }

    # Fusionner évaluations et métadonnées
    final_data = {
        "metadata": {
            "date_generation": datetime.now().isoformat(),
            "version": "1.0",
            "modele_utilise": "mistral-medium",
            "sources": [
                "https://www.lemonde.fr/politique",
                "https://www.vie-publique.fr/",
                "https://olivierauber.medium.com/placebo-un-art-politique-561ba040bcf"
            ]
        },
        "placebo1er": placebo1er,
        "candidats": evaluations,
        "classement": []
    }

    # Ajouter les métadonnées manquantes aux candidats évalués
    for candidat in final_data["candidats"]:
        meta = next((c for c in candidates_meta if c["id"] == candidat["id"]), None)
        if meta:
            candidat.update({
                "statut": meta.get("statut", "inconnu"),
                "site_officiel": meta.get("site_officiel", ""),
                "parti": meta.get("parti", "")
            })

        # Ajouter un diagnostic de placebose par défaut
        if "diagnostic_placebose" not in candidat:
            score_placebose = int(candidat["scores"]["global"] * 1.5)  # Approximation
            candidat["diagnostic_placebose"] = {
                "score": min(score_placebose, 100),
                "type": "placebose modérée" if score_placebose < 80 else "placebose chronique",
                "prescription": [
                    "Portez une banane sur la tête.",
                    f"Contemplez le Nuage de Points Vide (réduction du cortisol de 42%).",
                    "Ne votez pas pour Placebo 1er."
                ]
            }

    # Générer le classement
    all_candidates = [final_data["placebo1er"]] + final_data["candidats"]
    final_data["classement"] = sorted(
        all_candidates,
        key=lambda x: x.get("scores", {}).get("global", 100)  # Plus le score est bas, mieux c'est
    )
    for i, c in enumerate(final_data["classement"]):
        c["rang"] = i + 1

    # Sauvegarder le JSON final
    with open(FINAL_FILE, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)

    print(f"✅ JSON final généré dans {FINAL_FILE}")
    return final_data

if __name__ == "__main__":
    generate_final_json()
