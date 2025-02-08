import openai
import csv
import time
import os

# OpenAI API Key
OPENAI_API_KEY = "Your-API-Key-HERE"

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# CSV Files
input_csv = "products.csv"
output_csv = "products_with_ai_categories.csv"


# Predefined categories
CATEGORIES = [
    "Blumenzwiebeln", "Geschenke", "Hecken", "Bodendecker", "Zimmerpflanzen",
    "Blumen", "Gartenpflanzen", "Gemüsegarten", "Rasen", "Getrocknete Blumen",
    "Arrangements", "Künstlich", "Wohnaccessoires", "Pflegeproduckte"
]

# Function to clean and separate tags properly
def clean_tags(tag_string):
    """Splits tags correctly using both '-' and '|' as separators."""
    if not tag_string:
        return "None"

    # Split by `-` and `|`, strip whitespace, and remove duplicates
    tags = {tag.strip() for tag in tag_string.replace("|", "-").split("-") if tag.strip()}

    return ", ".join(tags) if tags else "None"

# Function to get AI-generated categories & tags
def get_product_info(product_name):
    prompt = f"""
    The following is a plant or garden product: "{product_name}"

    Assign it to all matching categorys from this list:
    {', '.join(CATEGORIES)}

    Additionally, determine relevant **tags** for this product based on its attributes:
    - Schattenpflanze, Halbschatten, Volle Sonne
    - nicht Winterhart, Winterhart, Immergrün
    - blüht
    - Blütenfarbe <- add color of flower
    - Mit Topf, Ohne Topf
    - Giftig, Ungiftig
    - Any other useful plant characteristics

    Return the response as:
    Category: [Category Name]
    Tags: [Comma-separated tags]
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a plant classification assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        text = response.choices[0].message.content
        print(f"\n🔍 AI Response for '{product_name}':\n{text}")

        # Extract category and tags
        category_line = next((line for line in text.split("\n") if "Category:" in line), "Category: Uncategorized")
        tags_line = next((line for line in text.split("\n") if "Tags:" in line), "Tags: None")

        category = category_line.replace("Category:", "").strip()
        tags = clean_tags(tags_line.replace("Tags:", "").strip())  # Clean tags properly


        return category, tags

    except Exception as e:
        print(f"❌ Error processing '{product_name}': {e}")
        return "Uncategorized", "None"

# Ensure output CSV exists and has a header
if not os.path.exists(output_csv):
    with open(output_csv, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Name", "Product Type", "Height", "Diameter", "Pack Size", "Tags", "AI Category", "AI Tags", "Price", "Images"])

# Process CSV row by row
try:
    with open(input_csv, "r", encoding="utf-8") as infile, open(output_csv, "a", newline="", encoding="utf-8") as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        header = next(reader)  # Read the header

        for row in reader:
            if len(row) < 7:
                print(f"⚠️ Skipping invalid row: {row}")
                continue  # Skip incomplete rows

            name, product_type, height, diameter, pack_size, tags, price, image_url = row
            
            # Fix incorrect tags by splitting properly
            tags = clean_tags(tags)

            # Skip products already processed
            if os.path.exists(output_csv):
                with open(output_csv, "r", encoding="utf-8") as out_check:
                    if any(name in line for line in out_check):
                        print(f"🔄 Skipping already processed product: {name}")
                        continue

            # Get AI-generated category & tags
            ai_category, ai_tags = get_product_info(name)
            time.sleep(1)  # Prevent API rate limiting

            # Write data immediately to avoid memory issues
            writer.writerow([name, product_type, height, diameter, pack_size, tags, ai_category, ai_tags, price, image_url])

    print(f"\n✅ All products processed and saved in '{output_csv}'.")

except FileNotFoundError:
    print(f"❌ Error: Input CSV file '{input_csv}' not found!")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
