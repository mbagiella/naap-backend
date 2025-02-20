import json
import re

# Charger le fichier JSON
file_path = "prepare2.json"  # Remplace par le bon chemin

print("📂 Chargement du fichier JSON...")
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

print(f"✅ {len(data['variations'])} variations chargées.\n")

# Expression régulière pour extraire le nom de l'image
pattern = re.compile(r"https:\/\/cdn\.naap\.ch\/prod\/.+?\/([^\/]+\.webp)")

modifications = 0  # Compteur de modifications

# Parcourir chaque variation et ses produits
for variation in data["variations"]:
    if "products" in variation:
        for product in variation["products"]:
            print(f"🔍 Traitement du produit ID: {product.get('product_id', 'N/A')}")

            if "product_id" in product and "product_image" in product:
                original_image = product["product_image"]
                match = pattern.search(original_image)

                if match:
                    image_name = match.group(1)  # Récupérer le nom du fichier image
                    new_url = f"http://localhost:3000/products/{product['product_id']}/{image_name}"
                    
                    print(f"   🖼 Ancienne image: {original_image}")
                    print(f"   🔄 Nouvelle image: {new_url}\n")

                    product["product_image"] = new_url
                    modifications += 1
                else:
                    print("   ⚠️ Aucun changement nécessaire.\n")

# Sauvegarder les modifications dans le fichier JSON
print(f"💾 Enregistrement des modifications ({modifications} mises à jour)...")
with open(file_path, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2)

print("✅ Fichier JSON mis à jour avec succès ! 🎉")
