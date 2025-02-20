import os
import json
import requests
from urllib.parse import urlparse

# Nom du fichier JSON d'entrée et sortie
input_json = "prices.json"
output_json = "updated_prices.json"


def download_and_replace_images(json_data, save_dir="products", base_url="http://localhost:3000/products/"):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"Dossier '{save_dir}' créé pour stocker les produits.")

    def process_value(value, product_id):
        if isinstance(value, str) and value.startswith("https://cdn"):
            parsed_url = urlparse(value)
            filename = os.path.basename(parsed_url.path)
            product_dir = os.path.join(save_dir, str(product_id))
            file_path = os.path.join(product_dir, filename)

            print(f"Traitement de l'URL : {value}")

            if not os.path.exists(product_dir):
                os.makedirs(product_dir)
                print(f"Dossier '{product_dir}' créé pour ce produit.")

            if not os.path.exists(file_path):
                print(f"Téléchargement de {filename}...")
                response = requests.get(value, stream=True)
                if response.status_code == 200:
                    with open(file_path, 'wb') as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)
                    print(f"Image sauvegardée sous {file_path}")
                else:
                    print(f"Échec du téléchargement de {filename}")
            else:
                print(f"Fichier {filename} déjà existant, téléchargement ignoré.")

            return f"{base_url}{product_id}/{filename}"
        return value

    def process_dict(d, product_id=None):
        if "product_id" in d:
            product_id = d["product_id"]  # Mettre à jour le product_id si trouvé
            print(f"Produit ID trouvé : {product_id}")

        for key, value in d.items():
            if isinstance(value, dict):
                print(f"Traitement du dictionnaire pour la clé: {key}")
                process_dict(value, product_id)
            elif isinstance(value, list):
                print(f"Traitement de la liste pour la clé: {key}")
                d[key] = [process_dict(v, product_id) if isinstance(v, dict) else process_value(v, product_id) for v in value]
            else:
                d[key] = process_value(value, product_id)
        return d

    print("Début du traitement du JSON...")
    result = process_dict(json_data)
    print("Traitement du JSON terminé.")
    return result

# Charger le JSON depuis un fichier
print(f"Chargement du fichier JSON : {input_json}...")
with open(input_json, "r", encoding="utf-8") as f:
    data = json.load(f)

# Modifier les liens et télécharger les images
print("Modification des liens et téléchargement des images...")
updated_data = download_and_replace_images(data)

# Sauvegarder le JSON modifié
print(f"Sauvegarde du fichier JSON mis à jour : {output_json}...")
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(updated_data, f, indent=4, ensure_ascii=False)
print("Processus terminé avec succès !")
