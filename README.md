# 🛒 AI-Powered WooCommerce Product Scraper & Uploader

**Fully automated tool for scraping product data, categorizing it using AI, and uploading it to WooCommerce via API.**

---

## 📖 Table of Contents
1. [Introduction](#introduction)  
2. [How It Works](#how-it-works)  
3. [Features](#features)  
4. [Installation & Requirements](#installation--requirements)  
5. [Step-by-Step Usage](#step-by-step-usage)  
6. [Configuration & Adjustments](#configuration--adjustments)  
7. [Legal Disclaimer ⚠️](#legal-disclaimer-)  
8. [Contributions & License](#contributions--license)  

---

## 📌 Introduction
### ❓ The Problem
- Many eCommerce stores need to **import products** from websites **without an API**.  
- Manually copying **product names, images, and prices** is time-consuming.  
- Categorizing products **accurately** is difficult for large inventories.  
- WooCommerce **doesn’t auto-create categories** from CSV uploads.

### ✅ The Solution
This tool **scrapes product data**, uses **AI to generate categories & tags**, and **uploads everything to WooCommerce via API**.

---

## 🚀 How It Works
The project consists of **three major scripts**:  

| Script | Purpose |
|--------|---------|
| **1. Product Scraper (`scraper.py`)** | Extracts product data (name, price, images) from a website and saves it in CSV. |
| **2. AI Categorization (`ai_category.py`)** | Uses ChatGPT to **intelligently categorize** products. |
| **3. WooCommerce API Uploader (`upload_to_woocommerce.py`)** | Uploads processed products to WooCommerce and creates missing categories automatically. |

---

## 🎯 Features
✅ **Automated Product Scraping** – Extracts name, price, images, and descriptions.  
✅ **AI-Powered Categorization** – Uses GPT-4o for **intelligent category mapping**.  
✅ **Tag Optimization** – Splits **complex names into SEO-friendly tags**.  
✅ **Bulk WooCommerce Upload** – Supports **automatic category creation**.  
✅ **Duplicate Prevention** – Avoids adding the same product twice.  
✅ **Scalable** – Works with **thousands of products**.  

---

## 💻 Installation & Requirements
### 🔧 **Requirements**
- **Python 3.10+**
- Required Python Libraries:
  ```sh
  pip install openai requests selenium beautifulsoup4 python-dotenv
  ```
- **WooCommerce Store** (API keys required)
- **OpenAI API Key** for AI categorization  
  - **How to get an OpenAI API Key:** Follow the instructions at [OpenAI API Documentation](https://platform.openai.com/signup/)
  - **Pricing Information:** This is a **paid service**, and as of **February 2025**, using this script to process **1,000 product lines costs approximately ~$1**. OpenAI pricing may change, so check the latest rates at [OpenAI Pricing](https://openai.com/pricing).
- **ChromeDriver** (for Selenium)
  - Download the correct version of **chromedriver.exe** from [Chromedriver Download](https://sites.google.com/chromium.org/driver/downloads)
  - Ensure it matches your **Chrome browser version**
  - Place it in the project root or set the correct **path in `scraper.py`**

### 📂 **Project Structure**
```plaintext
📂 AI-Powered-WooCommerce-Importer
 ├── scraper.py               # Scrapes product data & saves to CSV
 ├── ai_category.py           # Assigns AI categories & tags
 ├── upload_to_woocommerce.py # Uploads products via WooCommerce API
 ├── missing_im.py            # Generates CSV for missing images
 ├── .env                     # API keys & configurations
 ├── requirements.txt         # Required Python packages
 ├── chromedriver.exe         # Chrome WebDriver for Selenium (if using local execution)
 ├── README.md                # Project documentation
```

---

## 📌 Step-by-Step Usage
### **1️⃣ Product Scraping (`scraper.py`)**
➡️ **Extracts products** from a website and saves them to `products.csv`.

#### 🔹 **Run Script**
```sh
python scraper.py
```
#### 🔹 **Adjustments**
- Change `url = "https://example.com/category-page"` in `scraper.py` to **target a different site**.
- Modify CSS selectors inside `scraper.py` if the **website structure differs**.

---

### **2️⃣ AI Categorization (`ai_category.py`)**
➡️ Enhances `products.csv` by **adding intelligent categories & tags using ChatGPT**.

#### 🔹 **Run Script**
```sh
python ai_category.py
```
#### 🔹 **Adjustments**
- Update `CATEGORIES` in `ai_category.py` to **customize category choices**.
- Modify the **AI Prompt** to adjust **how categories & tags are assigned**.
- Add or remove **predefined categories & tag rules** to better fit your product catalog.

---

### **3️⃣ WooCommerce Upload (`upload_to_woocommerce.py`)**
➡️ Uploads **categorized products** to WooCommerce via API.

#### 🔹 **Important Notes**
- **WooCommerce does not allow uploading image URLs through the API**. 
- The script will **check if an item exists by name**, assign or create an SKU, and update all other product details **except**:
  - **Product Type**
  - **Image URL**

#### 🔹 **Run Script**
```sh
python upload_to_woocommerce.py
```

#### 🔹 **Handling Missing Images**
If images are required, run the `missing_im.py` script:
```sh
python missing_im.py
```
This will generate a **CSV file** listing all products that exist in WooCommerce **without images**, with:
- **Name**
- **SKU (from WooCommerce)**
- **Image URL** (from `products_with_ai_categories.csv`)

You can then **manually upload** the CSV "products_with_missing_images.csv" to WooCommerce and match IMG URLs to their products via SKU.

---

## ⚠️ Legal Disclaimer
🚨 **Disclaimer / Hinweis:**  
This tool is intended for **legitimate use only**. Scraping **third-party content without permission** may violate:
- **Website Terms of Service**
- **Intellectual Property Laws**
- **GDPR & Data Privacy Regulations**

**Do not scrape or use images, text, or product descriptions without the legal right to do so.**  
If in doubt, seek permission from the data owner.

**⚠️ Responsibility Disclaimer:**  
The developer **does not take responsibility** for any misuse of this tool.  
Users are **solely responsible** for ensuring compliance with laws and platform policies.

---

## 🤝 Contributions & License
✅ **Contributions Welcome!**  
Want to improve this tool? Submit a **Pull Request** or open an **Issue**.

📜 **License:**  
This project is released under the **MIT License**, meaning you can **freely use and modify** it.

---

## 🚀 Final Thoughts
✅ **Scrape thousands of products automatically.**  
✅ **Use AI to create meaningful categories & tags.**  
✅ **Upload everything to WooCommerce effortlessly.**  
✅ **Save hours of manual work!**  

💡 **Want more features? Let us know!** 😊

