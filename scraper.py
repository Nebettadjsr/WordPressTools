from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv
import os

# Set the correct path to chromedriver
CHROME_DRIVER_PATH = os.path.join(os.getcwd(), "chromedriver.exe")  # Ensure correct path

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in background
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Define the base URL of the category page
base_url = "https://example.com/category-page"
driver.get(base_url)

# Wait for JavaScript to load
time.sleep(5)

# Define CSV file path
csv_file = "products.csv"

# Load existing product names to prevent duplicates
existing_products = set()

if os.path.isfile(csv_file):
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header
        for row in reader:
            if row:
                existing_products.add(row[0])  # Product name is in the first column

def scrape_page():
    """Scrapes products from the current page and avoids duplicates."""
    products = driver.find_elements(By.CLASS_NAME, "product-card")
    product_list = []

    for product in products:
        try:
            name = product.find_element(By.CLASS_NAME, "product-name").text.strip()

            # Skip duplicate products
            if name in existing_products:
                print(f"Skipping duplicate: {name}")
                continue

            # Find correct price (ignore wholesale prompt)
            price_blocks = product.find_elements(By.CLASS_NAME, "pricing")
            price = None
            for block in price_blocks:
                if "€" in block.text:
                    price = block.text.strip()
                    break

            image_url = product.find_element(By.TAG_NAME, "img").get_attribute("src")

            if price:
                product_list.append([name, price, image_url])
                existing_products.add(name)  # Add to existing set to prevent re-adding

        except Exception as e:
            print(f"Error extracting product: {e}")

    # Append only unique products to CSV
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        if not file_exists:
            writer.writerow(["Name", "Price", "Image URL"])  # Write header only if file is new
        
        writer.writerows(product_list)

    print(f"Scraping completed for this page. {len(product_list)} new products added.")

while True:
    scrape_page()

    try:
        # Find all "page-link" elements
        page_links = driver.find_elements(By.CLASS_NAME, "page-link")
        
        next_button = None
        for link in page_links:
            if "Volgende" in link.text:  # Check if the text is "Volgende"
                next_button = link
                break    

        if next_button:
            # Click the "Next" button
            driver.execute_script("arguments[0].click();", next_button)
            print("Navigating to next page...")

            # Wait for the next page to load
            time.sleep(5)
        else:
            print("No more pages found. Scraping finished.")
            break

    except Exception as e:
        print(f"Error navigating pages: {e}")
        break

driver.quit()
