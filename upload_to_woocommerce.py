import requests
import pandas as pd
import random
import string
import re

# WooCommerce API Credentials
WC_API_URL = "https://yourwordpresssite.com/wp-json/wc/v3/"
WC_CONSUMER_KEY = "your_consumer_key"
WC_CONSUMER_SECRET = "your_consumer_secret"

AUTH = (WC_CONSUMER_KEY, WC_CONSUMER_SECRET)

# Load CSV Data
CSV_FILE = "products_with_ai_categories.csv"  # Change this to your actual file
df = pd.read_csv(CSV_FILE)


# Function to generate a new SKU
def generate_sku():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# Function to fetch all products and map them by name
def get_existing_products():
    url = f"{WC_API_URL}products?per_page=100"
    products_dict = {}

    while url:
        response = requests.get(url, auth=AUTH)
        if response.status_code == 200:
            products = response.json()
            for product in products:
                products_dict[product["name"].lower()] = {
                    "id": product["id"],
                    "sku": product["sku"] if product["sku"] else None
                }
            url = response.links.get("next", {}).get("url", None)  # Pagination support
        else:
            print(f"Error fetching products: {response.text}")
            break

    return products_dict

# Function to get existing categories
def get_existing_categories():
    url = f"{WC_API_URL}products/categories"
    response = requests.get(url, auth=AUTH)
    if response.status_code == 200:
        return {category["name"].lower(): category["id"] for category in response.json()}
    else:
        print(f"Error fetching categories: {response.text}")
        return {}

# Function to create a new category
def create_category(category_name):
    url = f"{WC_API_URL}products/categories"
    data = {"name": category_name}
    response = requests.post(url, json=data, auth=AUTH)
    if response.status_code == 201:
        return response.json()["id"]
    else:
        print(f"Error creating category {category_name}: {response.text}")
        return None

# Function to get or create category IDs
def get_category_ids(categories):
    category_ids = []
    existing_categories = get_existing_categories()

    for category in categories:
        category = category.strip().lower()
        if category in existing_categories:
            category_ids.append(existing_categories[category])
        else:
            new_category_id = create_category(category)
            if new_category_id:
                category_ids.append(new_category_id)
    
    return category_ids

# Function to clean price format (convert from "€ 18,99" to "18.99")
def clean_price(price):
    if isinstance(price, str):
        price = re.sub(r"[^\d,]", "", price)  # Remove currency symbols and extra characters
        price = price.replace(",", ".")  # Convert comma to dot
    try:
        return str(float(price))  # Ensure it's a valid number
    except ValueError:
        return "0.00"

# Function to create a new product
def create_product(name, sku, price, categories, tags, height, width):
    url = f"{WC_API_URL}products"

    category_ids = get_category_ids(categories)

    product_data = {
        "name": name,
        "sku": sku,
        "regular_price": price,
        "categories": [{"id": cat_id} for cat_id in category_ids],
        "tags": [{"name": tag.strip()} for tag in tags if tag.strip()],
        "dimensions": {"height": str(height), "width": str(width)}
    }

    response = requests.post(url, json=product_data, auth=AUTH)

    if response.status_code == 201:
        product_id = response.json().get("id")
        print(f"✅ Created new product: {name} (ID: {product_id})")
        return product_id
    else:
        print(f"❌ Failed to create product {name}: {response.text}")
        return None

# Fetch all existing products
existing_products = get_existing_products()

# Process CSV and update/create products
for _, row in df.iterrows():
    product_name = str(row["Name"]).strip().lower()
    
    if product_name in existing_products:
        product_info = existing_products[product_name]
        product_id = product_info["id"]
        sku = product_info["sku"] if product_info["sku"] else generate_sku()

        # Update SKU if missing
        if not product_info["sku"]:
            update_data = {"sku": sku}
            requests.put(f"{WC_API_URL}products/{product_id}", json=update_data, auth=AUTH)
            print(f"🔹 Assigned new SKU {sku} to {product_name}")

        # Process categories
        categories = str(row["AI Category"]).split(",")
        category_ids = get_category_ids(categories)

        # Process tags
        tags = set(str(row["Tags"]).split(",") + str(row["AI Tags"]).split(","))

        # Clean price
        price = clean_price(str(row["Price"]))

        # Update product
        update_data = {
            "sku": sku,
            "regular_price": price,
            "categories": [{"id": cat_id} for cat_id in category_ids],
            "tags": [{"name": tag.strip()} for tag in tags if tag.strip()],
            "dimensions": {
                "height": str(row["Height"]),
                "width": str(row["Diameter"])
            }
        }

        requests.put(f"{WC_API_URL}products/{product_id}", json=update_data, auth=AUTH)
        print(f"✅ Updated product: {product_name}")

    else:
        print(f"⚠️ Product '{product_name}' not found! Creating new product...")

        sku = generate_sku()  # Generate a new SKU for the new product
        price = clean_price(str(row["Price"]))
        categories = str(row["AI Category"]).split(",")
        tags = set(str(row["Tags"]).split(",") + str(row["AI Tags"]).split(","))
        height = str(row["Height"])
        width = str(row["Diameter"])

        product_id = create_product(product_name, sku, price, categories, tags, height, width)

        if product_id:
            existing_products[product_name] = {"id": product_id, "sku": sku}  # Add new product to tracking
            print(f"✅ New product created: {product_name}")

print("🎉 Product processing complete!")
