🛒 AI-Powered WooCommerce Product Scraper & Uploader
Fully automated tool for scraping product data, categorizing it using AI, and uploading it to WooCommerce via API.

📖 Table of Contents
Introduction
How It Works
Features
Installation & Requirements
Step-by-Step Usage
Configuration & Adjustments
Legal Disclaimer ⚠️
Contributions & License
📌 Introduction
❓ The Problem
Many eCommerce stores need to import products from websites without an API.
Manually copying product names, images, and prices is time-consuming.
Categorizing products accurately is difficult for large inventories.
WooCommerce doesn’t auto-create categories from CSV uploads.
✅ The Solution
This tool scrapes product data, uses AI to generate categories & tags, and uploads everything to WooCommerce via API.

🚀 How It Works
The project consists of three major scripts:

Script	Purpose
1. Product Scraper (scraper.py)	Extracts product data (name, price, images) from a website and saves it in CSV.
2. AI Categorization (ai_category.py)	Uses ChatGPT to intelligently categorize products.
3. WooCommerce API Uploader (upload_to_woocommerce.py)	Uploads processed products to WooCommerce and creates missing categories automatically.
🎯 Features
✅ Automated Product Scraping – Extracts name, price, images, and descriptions.
✅ AI-Powered Categorization – Uses GPT-4o for intelligent category mapping.
✅ Tag Optimization – Splits complex names into SEO-friendly tags.
✅ Bulk WooCommerce Upload – Supports automatic category creation.
✅ Duplicate Prevention – Avoids adding the same product twice.
✅ Scalable – Works with thousands of products.

💻 Installation & Requirements
🔧 Requirements
Python 3.10+
Required Python Libraries:
sh
Copy
Edit
pip install openai requests selenium beautifulsoup4 python-dotenv
WooCommerce Store (API keys required)
OpenAI API Key for AI categorization
📂 Project Structure
plaintext
Copy
Edit
📂 AI-Powered-WooCommerce-Importer
 ├── scraper.py               # Scrapes product data & saves to CSV
 ├── ai_category.py           # Assigns AI categories & tags
 ├── upload_to_woocommerce.py # Uploads products via WooCommerce API
 ├── .env                     # API keys & configurations
 ├── requirements.txt         # Required Python packages
 ├── README.md                # Project documentation
📌 Step-by-Step Usage
1️⃣ Product Scraping (scraper.py)
➡️ Extracts products from a website and saves them to products.csv.

🔹 Run Script
sh
Copy
Edit
python scraper.py
🔹 Adjustments
Change url = "https://example.com/category-page" in scraper.py to target a different site.
Modify CSS selectors inside scraper.py if the website structure differs.
2️⃣ AI Categorization (ai_category.py)
➡️ Enhances products.csv by adding intelligent categories & tags using ChatGPT.

🔹 Run Script
sh
Copy
Edit
python ai_category.py
🔹 Adjustments
Update CATEGORIES in ai_category.py to customize category choices.
Modify the AI prompt to generate better tags.
3️⃣ WooCommerce Upload (upload_to_woocommerce.py)
➡️ Uploads categorized products to WooCommerce via API.

🔹 Run Script
sh
Copy
Edit
python upload_to_woocommerce.py
🔹 Adjustments
Configure WooCommerce API keys in .env:
ini
Copy
Edit
WOOCOMMERCE_URL=https://yourshop.com/wp-json/wc/v3/
WOOCOMMERCE_CONSUMER_KEY=your_consumer_key
WOOCOMMERCE_CONSUMER_SECRET=your_consumer_secret
Adjust upload_to_woocommerce.py to:
Map correct WooCommerce fields.
Auto-create categories & attributes.
⚙️ Configuration & Adjustments
Feature	Where to Adjust
Target Website for Scraping	scraper.py (url = "https://example.com")
CSS Selectors for Product Data	scraper.py (find_element() methods)
AI-Generated Categories & Tags	ai_category.py (CATEGORIES & AI prompt)
WooCommerce API Credentials	.env file
Custom Attributes & Variations	upload_to_woocommerce.py
⚠️ Legal Disclaimer
🚨 Disclaimer / Hinweis:
This tool is intended for legitimate use only. Scraping third-party content without permission may violate:

Website Terms of Service
Intellectual Property Laws
GDPR & Data Privacy Regulations
Do not scrape or use images, text, or product descriptions without the legal right to do so.
If in doubt, seek permission from the data owner.

⚠️ Responsibility Disclaimer:
The developer does not take responsibility for any misuse of this tool.
Users are solely responsible for ensuring compliance with laws and platform policies.

🤝 Contributions & License
✅ Contributions Welcome!
Want to improve this tool? Submit a Pull Request or open an Issue.

📜 License:
This project is released under the MIT License, meaning you can freely use and modify it.

🚀 Final Thoughts
✅ Scrape thousands of products automatically.
✅ Use AI to create meaningful categories & tags.
✅ Upload everything to WooCommerce effortlessly.
✅ Save hours of manual work!
