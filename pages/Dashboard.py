import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

def fetch_product_data(query):
    url = "https://www.searchapi.io/api/v1/search"

    # Amazon search
    amazon_params = {
        "engine": "amazon_search",
        "q": query,
        "amazon_domain": "amazon.in",
        "api_key": os.get_env('product_api'),
    }
    amazon_response = requests.get(url, params=amazon_params)

    # Google Shopping search
    google_params = {
        "engine": "google_shopping",
        "q": query,
        "gl": "in",
        "hl": "en",
        "location": "California,United States",
        "api_key": os.get_env('product_api'),
    }
    google_response = requests.get(url, params=google_params)

    try:
        amazon_data = amazon_response.json().get("organic_results", [])
        google_data = google_response.json().get("shopping_results", [])
        return amazon_data + google_data
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return []

def process_product_data(products):
    processed_data = []
    for product in products:
        # Extract numeric price
        price_str = product.get('price', '0').replace('₹', '').replace(',', '').strip()
        try:
            price = float(price_str)
        except ValueError:
            price = 0

        processed_data.append({
            'Title': product.get('title', 'N/A'),
            'Price': price,
            'Rating': float(product.get('rating', 0)),
            'Reviews': int(product.get('reviews_count', 0)),
            'Source': 'Amazon' if 'amazon' in product.get('source', '').lower() else 'Google Shopping',
            'Seller': product.get('seller', 'Unknown'),
            'Discount': float(product.get('discount', 0)),
        })
    return pd.DataFrame(processed_data)

def categorize_price(price):
    if price < 1000:
        return 'Budget'
    elif 1000 <= price < 5000:
        return 'Mid-Range'
    else:
        return 'Premium'

def main():
    st.set_page_config(page_title="Advanced Product Analysis Dashboard", layout="wide")

    st.title("📊 Comprehensive Product Analysis Dashboard")

    # Search input
    query = st.text_input("Enter product category:", placeholder="e.g., smartphones, laptops")

    if query:
        # Fetch and display products
        with st.spinner('Fetching product data...'):
            products = fetch_product_data(query)

        if products:
            # Process data
            df = process_product_data(products)

            # Price Categorization
            df['Price Category'] = df['Price'].apply(categorize_price)

            # Visualization Sections
            st.markdown("## 📊 Comprehensive Product Insights")

            # Scatter Plot Insights
            st.markdown("### 🔍 Scatter Plot Insights")
            col1, col2 = st.columns(2)

            with col1:
                # Price vs Ratings Scatter Plot
                plt.figure(figsize=(10,6))
                plt.clf()
                plt.scatter(df['Price'], df['Rating'], alpha=0.6)
                plt.title('Price vs Customer Ratings')
                plt.xlabel('Price (₹)')
                plt.ylabel('Ratings')
                st.pyplot(plt)
                plt.close()

            with col2:
                # Price vs Number of Reviews Scatter Plot
                plt.figure(figsize=(10,6))
                plt.clf()
                plt.scatter(df['Price'], df['Reviews'], alpha=0.6)
                plt.title('Price vs Number of Reviews')
                plt.xlabel('Price (₹)')
                plt.ylabel('Number of Reviews')
                st.pyplot(plt)
                plt.close()

            # Box Plot Insights
            st.markdown("### 📦 Box Plot Insights")
            plt.figure(figsize=(12,6))
            plt.clf()
            df.boxplot(column='Price', by='Price Category')
            plt.title('Price Distribution by Category')
            plt.suptitle('')  # Remove automatic suptitle
            plt.xlabel('Price Category')
            plt.ylabel('Price (₹)')
            st.pyplot(plt)
            plt.close()

            # Relationship Insights
            col3, col4 = st.columns(2)

            with col3:
                # Discount vs Ratings
                plt.figure(figsize=(10,6))
                plt.clf()
                plt.scatter(df['Discount'], df['Rating'], alpha=0.6)
                plt.title('Discount % vs Ratings')
                plt.xlabel('Discount %')
                plt.ylabel('Ratings')
                st.pyplot(plt)
                plt.close()

            with col4:
                # Price Distribution
                plt.figure(figsize=(10,6))
                plt.clf()
                plt.hist(df['Price'], bins=20, edgecolor='black')
                plt.title('Price Distribution')
                plt.xlabel('Price (₹)')
                plt.ylabel('Frequency')
                st.pyplot(plt)
                plt.close()

            # Key Metrics
            st.markdown("## 📈 Key Product Metrics")
            col5, col6, col7 = st.columns(3)
            with col5:
                st.metric("Average Price", f"₹{df['Price'].mean():.2f}")
            with col6:
                st.metric("Median Rating", f"{df['Rating'].median():.2f}")
            with col7:
                st.metric("Total Reviews", f"{df['Reviews'].sum():,}")

            # Detailed Product Analysis
            st.markdown("## 📋 Detailed Product Insights")
            st.dataframe(df, use_container_width=True)

        else:
            st.warning("No products found. Try a different search term.")

if __name__ == "__main__":
    main()