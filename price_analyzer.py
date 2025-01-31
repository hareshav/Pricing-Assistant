import streamlit as st
import requests
import os
from groclake.vectorlake import VectorLake
from groclake.modellake import ModelLake
import json
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="Product Price Analyzer",
    page_icon="💰",
    layout="wide",
    menu_items={
        'Get Help': 'https://www.example.com/help',
        'Report a bug': "https://www.example.com/bug",
        'About': "# Product Price Analyzer\n This application helps analyze market prices and provides AI-powered recommendations."
    }
)

# Initialize Groclake credentials
# GROCLAKE_API_KEY = "4c56ff4ce4aaf9573aa5dff913df997a"
# GROCLAKE_ACCOUNT_ID = "d2b9d7150a1f6693817d82d4ca9b701d"
os.environ["GROCLAKE_API_KEY"] = os.getenv("GROCLAKE_API_KEY")
os.environ["GROCLAKE_ACCOUNT_ID"] = os.getenv("GROCLAKE_ACCOUNT_ID")

# Initialize VectorLake and ModelLake
vectorlake = VectorLake()
modellake = ModelLake()

st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Clean, minimal styling */
    
    .product-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 4px;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    
    .product-image {
        border-radius: 4px;
    }
    
    .product-details {
        margin-top: 1rem;
    }
    
    .price-tag {
        font-size: 1.2rem;
        font-weight: bold;
        color: #2d2d2d;
    }
    
    .metric-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 4px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def fetch_product_data(query):
    """Fetch product data from multiple sources"""
    url = "https://www.searchapi.io/api/v1/search"
    
    # Amazon search
    amazon_params = {
        "engine": "amazon_search",
        "q": query,
        "amazon_domain": "amazon.in",
        "api_key": "x6PbBGHhLwbv1vXQQZ7qyMYS",
    }
    amazon_response = requests.get(url, params=amazon_params)
    
    # Google Shopping search
    google_params = {
        "engine": "google_shopping",
        "q": query,
        "gl": "in",
        "hl": "en",
        "location": "California,United States",
        "api_key": "x6PbBGHhLwbv1vXQQZ7qyMYS",
    }
    google_response = requests.get(url, params=google_params)
    
    try:
        amazon_data = amazon_response.json().get("organic_results", [])
        google_data = google_response.json().get("shopping_results", [])
        return amazon_data + google_data
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return []

def vectorize_and_search(query, data):
    """Vectorize data and perform search"""
    try:
        vector_create_payload = {"vectorlake_name": query}
        vector_create = vectorlake.create(vector_create_payload)
        print(vector_create)
        vectorlake_id = vector_create.get("vectorlake_id")        
        for item in data:
            document_text = item.get("title", "")
            vector_data = vectorlake.generate(document_text)
            generated_vector = vector_data.get("vector")
            
            payload = {
                "vector": generated_vector,
                "vectorlake_id": vectorlake_id,
                "document_text": document_text,
                "vector_type": "text",
                "metadata": item,
            }
            vectorlake.push(payload)
        
        vector_search_data = vectorlake.generate(query)
        search_vector = vector_search_data.get("vector")
        
        search_payload = {
            "vector": search_vector,
            "vectorlake_id": vectorlake_id,
            "vector_type": "text",
            "top_k": 20,
        }
        
        return vectorlake.search(search_payload)
    except Exception as e:
        st.error(f"Error in vectorization: {str(e)}")
        return None

def get_detailed_analysis(search_results, query):
    """Get detailed analysis using ModelLake"""
    prompt = f"""Analyze the following product details and market context to recommend an optimal price.
    ### Market Context: {search_results}
    ### Product Details: {query}
    Consider factors such as competitor pricing, market demand, and product uniqueness while suggesting a competitive and profitable price in Indian rupees"""
    
    chat_completion_request = {
        "groc_account_id": "c4ca4238a0b923820dcc509a6f75849b",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    }
    
    try:
        response = modellake.chat_complete(chat_completion_request)
        return response["answer"]
    except Exception as e:
        st.error(f"Error getting detailed analysis: {str(e)}")
        return None

def display_product_card(product):
    """Display product information in a card format"""
    with st.container():
        st.markdown("""
        <style>
        .product-card {
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        with st.expander(f"📦 {product.get('title', 'N/A')}", expanded=True):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                if 'thumbnail' in product:
                    st.image(product['thumbnail'], use_column_width=True)
                elif 'image' in product:
                    st.image(product['image'], use_column_width=True)
            
            with col2:
                st.markdown(f"**Price:** {product.get('price', 'N/A')}")
                if 'rating' in product:
                    st.markdown(f"**Rating:** {'⭐' * int(float(product['rating']))} ({product['rating']})")
                
                # Seller information
                if 'seller_name' in product:
                    st.markdown(f"**Seller:** {product['seller_name']}")
                elif 'seller' in product:
                    st.markdown(f"**Seller:** {product['seller']}")
                elif 'shop_name' in product:
                    st.markdown(f"**Shop:** {product['shop_name']}")
                
                # Additional details
                if 'delivery' in product:
                    st.markdown(f"**Delivery:** {product['delivery']}")
                if 'link' in product:
                    st.markdown(f"[View Product]({product['link']})")

# Streamlit UI
st.title("🛍️ Product Price Analyzer")
st.write("Enter a product to analyze market prices and get recommendations")

# User input
query = st.text_input("Enter product name:", "")

if st.button("Analyze"):
    if query:
        with st.spinner("Fetching market data..."):
            product_data = fetch_product_data(query)
            
            if product_data:
                st.subheader("📊 Market Analysis")
                
                df = pd.DataFrame(product_data)
                if 'price' in df.columns:
                    df['price'] = pd.to_numeric(df['price'].str.replace('₹', '').str.replace(',', ''), errors='coerce')
                    
                    st.write("Price Statistics:")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Average Price", f"₹{df['price'].mean():,.2f}")
                    with col2:
                        st.metric("Minimum Price", f"₹{df['price'].min():,.2f}")
                    with col3:
                        st.metric("Maximum Price", f"₹{df['price'].max():,.2f}")
                
                search_results = vectorize_and_search(query, product_data)
                
                if search_results:
                    analysis = get_detailed_analysis(search_results, query)
                    
                    col_products, col_analysis = st.columns([3, 2])
                    
                    with col_products:
                        st.subheader("🏷️ Products")
                        for result in search_results.get("results", []):
                            display_product_card(result["metadata"])
                    
                    with col_analysis:
                        if analysis:
                            st.subheader("📈 Price Analysis")
                            st.markdown(analysis)
    else:
        st.warning("Please enter a product name to analyze")

# Add footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and Groclake API")