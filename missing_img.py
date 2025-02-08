import requests
import pandas as pd
import csv
import difflib
import re

# WooCommerce API Credentials
WC_API_URL = "https://yourwordpresssite.com/wp-json/wc/v3/"
WC_CONSUMER_KEY = "your_consumer_key"
WC_CONSUMER_SECRET = "your_consumer_secret"


AUTH = (WC_CONSUMER_KEY, WC_CONSUMER_SECRET)

# CSV File with AI Categories and Image URLs
AI_CSV_FILE = "products_with_ai_categories.csv"  # Change to your actual file

# Output CSV File
OUTPUT_CSV = "products_with_missing_images.csv"

# Function to normalize names (removes special characters, converts to lowercase)
def clean_name(name):
    name = name.replace("’", "'")  # Normalize apostrophes
    name = name.replace("term.", "terminalis")  # Replace common abbreviations
    name = re.sub(r"[^a-zA-Z0-9| ]+", "", name)  # Remove special characters
    return name.strip().lower()

# Function to fetch all products from WooCommerce
def get_all_products():
    url = f"{WC_API_URL}products?per_page=100"
    products_list = []

    while url:
        response = requests.get(url, auth=AUTH)
        if response.status_code == 200:
            products = response.json()
            for product in products:
                product_name = clean_name(product["name"])  # Clean product name
                sku = product.get("sku", "").strip()
                images = product.get("images", [])
                img_url = images[0]["src"] if images else None  # First image if available

                products_list.append({
                    "name": product_name,
                    "sku": sku,
                    "img": img_url
                })
            url = response.links.get("next", {}).get("url", None)  # Pagination handling
        else:
            print(f"Error fetching products: {response.text}")
            break

    return products_list

# Load AI CSV data into a dictionary (matching name to image URL)
def load_ai_category_data():
    df = pd.read_csv(AI_CSV_FILE)
    ai_data = {}
    for _, row in df.iterrows():
        product_name = clean_name(str(row["Name"]))  # Clean name before storing
        image_url = str(row["Images"]).strip() if "Images" in row else None  # Use IMG column if available
        ai_data[product_name] = image_url
    return ai_data

# Match missing images and write new CSV
def match_missing_images():
    products = get_all_products()
    ai_data = load_ai_category_data()
    output_data = []

    print("\n🔍 Checking AI CSV Names:")
    print(list(ai_data.keys()))  # Print all available AI product names

    for product in products:
        if not product["img"]:  # Only process products with missing images
            name = product["name"]
            sku = product["sku"]

            # Try exact match first
            img_url = ai_data.get(name)

            # If no exact match, find closest match
            if not img_url:
                closest_matches = difflib.get_close_matches(name, ai_data.keys(), n=1, cutoff=0.2)  # Lower cutoff
                if closest_matches:
                    best_match = closest_matches[0]
                    img_url = ai_data.get(best_match)  # ✅ NOW EXTRACTING IMAGE URL CORRECTLY
                    print(f"🔹 Best match for '{name}': '{best_match}' (Using image {img_url})")

            # ✅ **ALWAYS use closest match if found**
            if img_url:  # Even if from closest match
                output_data.append([name, sku, img_url])
                print(f"✅ Added to CSV: {name} -> {img_url}")
            else:
                print(f"⚠️ No matching image found for '{name}' (Closest match: {closest_matches if closest_matches else 'None'})")

    # Write to new CSV file
    if output_data:
        with open(OUTPUT_CSV, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "SKU", "Images"])
            writer.writerows(output_data)
        print(f"\n🎉 Process complete! CSV saved as {OUTPUT_CSV}")
    else:
        print("\n⚠️ No matches found, CSV is empty!")

# Run the script
match_missing_images()
