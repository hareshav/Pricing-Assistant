import streamlit as st
import os
from groclake.cataloglake import CatalogLake
from groclake.datalake import DataLake
from groclake.vectorlake import VectorLake
from groclake.modellake import ModelLake

# Set environment variables
GROCLAKE_API_KEY = '3988c7f88ebcb58c6ce932b957b6f332'
GROCLAKE_ACCOUNT_ID = '3230fa44b91997878d450b940b4ac848'

os.environ['GROCLAKE_API_KEY'] = GROCLAKE_API_KEY
os.environ['GROCLAKE_ACCOUNT_ID'] = GROCLAKE_ACCOUNT_ID

# Page configuration with custom theme
st.set_page_config(
    page_title="Groclake Product Pricing Assistant",
    page_icon="💰",
    layout="wide",
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #1E3D59;
        font-size: 2.5rem !important;
        margin-bottom: 2rem !important;
        text-align: center;
    }
    .stTextInput {
        margin: 2rem 0;
    }
    .search-container {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .result-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .suggestion-container {
        background-color: #e3f2fd;
        padding: 2rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize instances
vector = VectorLake()
modellake = ModelLake()

vector_create = vector.create()
vectorlake_id = vector_create.get('vectorlake_id')

# Header with icon and title
st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1>🏪 Groclake Product Pricing Assistant</h1>
        <p style='font-size: 1.2rem; color: #666;'>Intelligent pricing recommendations for your products</p>
    </div>
""", unsafe_allow_html=True)
# Search interface
with st.container():
    st.markdown("<div class='search-container'>", unsafe_allow_html=True)
    search_query = st.text_area(
        "What product would you like to price?",
        placeholder="Enter product name or description...",
    )
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        search_button = st.button("🔍 Analyze Pricing", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

if search_button and search_query:
    with st.spinner("Analyzing market data..."):
        left, right = st.columns(2)
        if not vectorlake_id:
            st.error("⚠️ Failed to create vector lake. Please try again.")
        else:
            vector_search_data = vector.generate(search_query)
            search_vector = vector_search_data.get('vector')
            search_payload = {
                "vector": search_vector,
                "vectorlake_id": vectorlake_id,
                "vector_type": "text",
                "top_k": 20
            }
            search_response = vector.search(search_payload)
            
            if search_response and search_response.get("results"):
                with left:
                    st.markdown("<h3 style='color: #1E3D59;'>📊 Market Analysis</h3>", unsafe_allow_html=True)
                    
                    for result in search_response["results"]:
                        
                        # st.write(result)
                        try:
                            st.markdown("""
                                <div class='result-card'>
                                    <h4 style='color: #1E3D59; margin-bottom: 0.5rem;'>Product Details</h4>
                                    <p>{}</p>
                                    <h4 style='color: #1E3D59; margin-bottom: 0.5rem; margin-top: 1rem;'>Current Market Price</h4>
                                    <p style='font-size: 1.2rem; color: #2E7D32;'>₹{}</p>
                                </div>
                            """.format(
                                result['metadata']['question'].replace('\n\n'," "),
                                result['metadata']['Selling Price']
                            ), unsafe_allow_html=True)
                        except:
                            pass

                
                # Generate pricing recommendation
                prompt = f"""
                Analyze the following product details and market context to recommend an optimal price.
                
                ### Product Details: {search_query}
                
                Consider factors such as competitor pricing, market demand, and product uniqueness while suggesting a competitive and profitable price in Indian Rupees.
                """
                chat_completion_request = {
                    "groc_account_id": "c4ca4238a0b923820dcc509a6f75849b",
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ]
                }
                response = modellake.chat_complete(chat_completion_request)
                
                with right:
                    st.markdown("""
                        <div class='suggestion-container'>
                            <h3 style='color: #1E3D59;'>💡 Pricing Recommendation</h3>
                            <p style='font-size: 1.1rem; line-height: 1.6;'>{}</p>
                        </div>
                    """.format(response['answer']), unsafe_allow_html=True)
            else:
                st.warning("📝 No market data found for this product. Try a different search term.")

# Footer
st.markdown("""
    <div style='text-align: center; margin-top: 3rem; padding: 1rem; background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.1);'>
        <p class='subtitle-text'>Powered by Groclake AI | Built with Streamlit</p>
    </div>
""", unsafe_allow_html=True)