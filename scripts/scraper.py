import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

# Chemin des données
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CANDIDATES_FILE = os.path.join(DATA_DIR, "candidates.json")
RAW_DATA_FILE = os.path.join(DATA_DIR, f"raw_data_{datetime.now().strftime('%Y-%m-%d')}.json")

def load_candidates():
    """Charge la liste des candidats depuis candidates.json"""
    with open(CANDIDATES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)["candidats"]

def scrape_url(url, candidat_id, field_type):
    """Scrape une URL et retourne le texte extrait"""
    try:
        headers = {
            "User-Agent": "Placebot/1.0 (Évaluation politique contre Placebo 1er; https://github.com/OAuber/Placebot)"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Supprimer les éléments indésirables (scripts, styles, nav, footer)
        for element in soup(["script", "style", "nav", "footer", "iframe", "img"]):
            element.decompose()

        # Extraire le texte principal
        text = soup.get_text(separator="\n", strip=True)

        # Nettoyer les espaces multiples
        text = "\n".join(line for line in text.splitlines() if line.strip())

        return {
            "url": url,
            "content": text,
            "scraped_at": datetime.now().isoformat(),
            "status": "success"
        }
    except Exception as e:
        return {
            "url": url,
            "error": str(e),
            "scraped_at": datetime.now().isoformat(),
            "status": "failed"
        }

def scrape_candidate(candidat):
    """Scrape les données d'un candidat"""
    result = {
        "id": candidat["id"],
        "nom": candidat["nom"],
        "parti": candidat["parti"],
        "scraped_at": datetime.now().isoformat(),
        "sources": []
    }

    # Scraper le programme officiel
    if candidat.get("programme_url"):
        programme = scrape_url(
            candidat["programme_url"],
            candidat["id"],
            "programme"
        )
        result["sources"].append({
            "type": "programme",
            "data": programme
        })

    # Scraper les déclarations récentes
    for url in candidat.get("declarations_urls", []):
        declaration = scrape_url(
            url,
            candidat["id"],
            "declaration"
        )
        result["sources"].append({
            "type": "declaration",
            "url": url,
            "data": declaration
        })

    return result

def main():
    """Point d'entrée principal"""
    os.makedirs(DATA_DIR, exist_ok=True)

    candidates = load_candidates()
    scraped_data = []

    for candidat in candidates:
        if candidat.get("actif", True):
            print(f"Scraping {candidat['nom']}...")
            scraped_candidate = scrape_candidate(candidat)
            scraped_data.append(scraped_candidate)

    # Sauvegarder les données brutes
    with open(RAW_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(scraped_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Données scrapées sauvegardées dans {RAW_DATA_FILE}")

if __name__ == "__main__":
    main()
