import os
import requests
import json

# Fichier source contenant les détails des produits
PRODUCT_DETAILS_FILE = "prepare.json"
# Fichier de sortie pour stocker les offres
OFFERS_FILE = "prices.json"
# Liste des clés contenant des URLs à récupérer
TAGJSON_LIST = ["product_prices_history_url"]

# Vérifier si le fichier de produits existe
if not os.path.exists(PRODUCT_DETAILS_FILE):
    print(f"Erreur : {PRODUCT_DETAILS_FILE} n'existe pas.")
    exit(1)

# Charger les détails des produits
print("Chargement des détails des produits...")
with open(PRODUCT_DETAILS_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

offers_list = []

# Vérifier si la clé "product-detail" existe
if "product-detail" not in data:
    print("Erreur : Clé 'product-detail' manquante dans le JSON.")
    exit(1)

# Boucler sur chaque produit et récupérer les offres
for product in data["product-detail"]:
    product_id = product.get("product_id")
    if not product_id:
        print("Produit sans 'product_id', passage au suivant...")
        continue

    product_data = {
        "id": product_id,
        "product_id": product_id
    }

    for tag in TAGJSON_LIST:
        offers_url = product.get(tag)
        if not offers_url:
            print(f"Aucune URL '{tag}' pour le produit {product_id}, passage au suivant...")
            continue

        print(f"Récupération des données depuis {offers_url} pour le produit {product_id}...")

        try:
            response = requests.get(offers_url, timeout=10)
            response.raise_for_status()  # Vérifie si la requête est réussie
            product_data.update(response.json())  # Fusionne les nouvelles données

            print(f"Données récupérées pour {tag} du produit {product_id}.")

        except requests.RequestException as e:
            print(f"Erreur lors de la récupération des données '{tag}' pour {product_id}: {e}")

    offers_list.append(product_data)

# Sauvegarde des offres dans le fichier JSON
print(f"Sauvegarde des offres dans {OFFERS_FILE}...")
with open(OFFERS_FILE, "w", encoding="utf-8") as f:
    json.dump({"associations": offers_list}, f, ensure_ascii=False, indent=4)

print("Traitement terminé avec succès ! ✅")
