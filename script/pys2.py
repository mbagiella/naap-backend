import os
import requests
import json
from urllib.parse import urlparse

# Chemin du fichier JSON
json_file_path = 'prepare2.json'  # Remplacez par le chemin de votre fichier JSON
print(f"Chargement du fichier JSON depuis : {json_file_path}")

# Dossier de destination pour stocker les images
output_folder = 'products'
print(f"Création du dossier de destination : {output_folder}")
os.makedirs(output_folder, exist_ok=True)  # Crée le dossier s'il n'existe pas

# Charger le fichier JSON
print("Chargement des données JSON...")
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
print("Données JSON chargées avec succès.")

# Parcourir chaque produit dans "product-detail"
print(f"Nombre de produits trouvés : {len(data.get('variations', []))}")
for productVariation in data.get('variations', []):
    productVariation_id = productVariation.get('id')
    products = productVariation.get('products', [])

    print(f"\nTraitement du produit : (ID: {productVariation_id})")
    print(f"Nombre de produit trouvées pour ce produit : {len(products)}")

    for product in products:
        # Créer un sous-dossier pour le produit
        product_id = product.get('product_id')
        product_folder = os.path.join(output_folder, str(product_id))
        print(f"Création du dossier du produit : {product_folder}")
        os.makedirs(product_folder, exist_ok=True)

        # Télécharger chaque image
        image_url = product.get('product_image')
        if image_url:
            print(f"\nTéléchargement de l'image : {image_url}")
            try:
                # Extraire le nom du fichier à partir de l'URL
                parsed_url = urlparse(image_url)
                image_filename = os.path.basename(parsed_url.path)  # Récupère le nom du fichier (ex: 3601434.webp)
                print(f"Nom du fichier extrait : {image_filename}")

                # Télécharger l'image
                response = requests.get(image_url, stream=True)
                response.raise_for_status()  # Vérifier si la requête a réussi
                print("Téléchargement réussi.")

                # Enregistrer l'image dans le dossier du produit
                image_path = os.path.join(product_folder, image_filename)
                print(f"Enregistrement de l'image sous : {image_path}")

                with open(image_path, 'wb') as image_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        image_file.write(chunk)
                print("Image enregistrée avec succès.")
            except Exception as e:
                print(f"Erreur lors du téléchargement de l'image : {e}")
        else:
            print("Aucune URL trouvée pour cette image.")

print("\nTraitement terminé. Toutes les images ont été téléchargées.")