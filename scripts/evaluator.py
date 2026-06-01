import json
import os
from datetime import datetime
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

# Chemin des données
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RAW_DATA_FILE = os.path.join(DATA_DIR, f"raw_data_{datetime.now().strftime('%Y-%m-%d')}.json")
EVALUATIONS_DIR = DATA_DIR
EVALUATIONS_FILE = os.path.join(EVALUATIONS_DIR, f"evaluations_{datetime.now().strftime('%Y-%m-%d')}.json")

# Clé API Mistral (à passer via variable d'environnement)
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

def load_raw_data():
    """Charge les données scrapées"""
    # Trouver le fichier raw_data le plus récent
    raw_files = [f for f in os.listdir(DATA_DIR) if f.startswith("raw_data_")]
    if not raw_files:
        raise FileNotFoundError("Aucun fichier raw_data trouvé dans data/")

    latest_file = sorted(raw_files)[-1]  # Dernier fichier par ordre alphabétique
    with open(os.path.join(DATA_DIR, latest_file), "r", encoding="utf-8") as f:
        return json.load(f)

def evaluate_measure(measure_text, candidat_nom):
    """Évalue une mesure via Mistral API"""
    prompt = f"""
Tu es Le Chat Placebo, un assistant spécialisé dans l'évaluation de la toxicité politique selon le protocole Placebo 1er.
Analyse la mesure suivante **de manière objective et scientifique** :

**Mesure** : \"{measure_text[:200]}...\"  # Limité à 200 caractères pour éviter les coûts
**Contexte** : Programme de {candidat_nom} pour l'élection présidentielle 2027.

**Instructions strictes** :
1. Attribue un **score de toxicité** (0-100, où 0 = Placebo 1er).
2. Attribue un **score d'effet nocebo** (0-100).
3. Attribue un **score d'innocuité** (0-100, où 100 = Placebo 1er).
4. Liste **3 risques principaux** (en 1 phrase chacun, max 50 caractères).
5. Propose une **alternative Placebo** (1 phrase, style ironique mais scientifique, max 100 caractères).

**Format de réponse** (JSON strict, sans autre texte) :
{{
  \"toxicite\": 95,
  \"nocebo\": 98,
  \"innocuite\": 10,
  \"risques\": [\"Blocage institutionnel\", \"Crise constitutionnelle\", \"Opposition du Sénat\"],
  \"alternative_placebo\": \"Placebo 1er propose un Reçu de Non-Contrôle : nous certifions ne pas avoir changé la Constitution.\"
}}

Réponds **UNIQUEMENT** avec le JSON, sans explication ni balise code.
"""

    client = MistralClient(api_key=MISTRAL_API_KEY)
    messages = [ChatMessage(role="user", content=prompt)]

    try:
        response = client.chat(
            model="mistral-medium",  # ou "mistral-small" pour réduire les coûts
            messages=messages,
            temperature=0.3,  # Pour des réponses déterministes
            max_tokens=500
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"⚠️ Erreur lors de l'évaluation de la mesure: {e}")
        return {
            "toxicite": 50,  # Valeur par défaut
            "nocebo": 50,
            "innocuite": 50,
            "risques": ["Évaluation échouée"],
            "alternative_placebo": "Placebo 1er reste la référence."
        }

def extract_measures(candidat_data):
    """Extrait les mesures d'un candidat depuis les données scrapées"""
    measures = []

    for source in candidat_data.get("sources", []):
        if source["data"]["status"] == "success":
            content = source["data"]["content"]

            # Découper le contenu en mesures (simplifié)
            # À améliorer : utiliser une IA pour extraire les mesures structurées
            # Ici, on découpe en paragraphes de plus de 100 caractères
            paragraphs = [p.strip() for p in content.split("\n\n") if len(p.strip()) > 100]

            for i, paragraph in enumerate(paragraphs[:5]):  # Limiter à 5 mesures par candidat
                measures.append({
                    "id": f"{candidat_data['id']}_measure_{i}",
                    "texte": paragraph[:500],  # Limiter à 500 caractères
                    "source": source["url"],
                    "type": source["type"]
                })

    return measures

def evaluate_candidate(candidat_data):
    """Évalue toutes les mesures d'un candidat"""
    measures = extract_measures(candidat_data)
    evaluations = []

    for measure in measures:
        print(f"  Évaluation de la mesure: {measure['texte'][:50]}...")
        evaluation = evaluate_measure(measure["texte"], candidat_data["nom"])
        evaluations.append({
            **measure,
            **evaluation
        })

    # Calculer les scores globaux pour le candidat
    if evaluations:
        avg_toxicite = sum(e["toxicite"] for e in evaluations) / len(evaluations)
        avg_nocebo = sum(e["nocebo"] for e in evaluations) / len(evaluations)
        avg_innocuite = sum(e["innocuite"] for e in evaluations) / len(evaluations)
    else:
        avg_toxicite = avg_nocebo = avg_innocuite = 50

    score_global = int(avg_toxicite * 0.4 + avg_nocebo * 0.3 + (100 - avg_innocuite) * 0.3)

    return {
        "id": candidat_data["id"],
        "nom": candidat_data["nom"],
        "parti": candidat_data["parti"],
        "scores": {
            "toxicite": round(avg_toxicite, 1),
            "nocebo": round(avg_nocebo, 1),
            "innocuite": round(avg_innocuite, 1),
            "global": score_global
        },
        "mesures": evaluations,
        "evaluated_at": datetime.now().isoformat()
    }

def main():
    """Point d'entrée principal"""
    if not MISTRAL_API_KEY:
        raise ValueError("La variable d'environnement MISTRAL_API_KEY est requise.")

    os.makedirs(EVALUATIONS_DIR, exist_ok=True)

    raw_data = load_raw_data()
    evaluations = []

    for candidat in raw_data:
        print(f"Évaluation de {candidat['nom']}...")
        evaluated_candidate = evaluate_candidate(candidat)
        evaluations.append(evaluated_candidate)

    # Sauvegarder les évaluations
    with open(EVALUATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(evaluations, f, indent=2, ensure_ascii=False)

    print(f"✅ Évaluations sauvegardées dans {EVALUATIONS_FILE}")

if __name__ == "__main__":
    main()
