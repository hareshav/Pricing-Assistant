import os
import streamlit as st
from groclake.modellake import ModelLake

# Set environment variables
GROCLAKE_API_KEY = '4c56ff4ce4aaf9573aa5dff913df997a'
GROCLAKE_ACCOUNT_ID = 'd2b9d7150a1f6693817d82d4ca9b701d'

os.environ['GROCLAKE_API_KEY'] = GROCLAKE_API_KEY
os.environ['GROCLAKE_ACCOUNT_ID'] = GROCLAKE_ACCOUNT_ID

# Page configuration
st.set_page_config(
    page_title="Groclake Marketing Content Generator",
    page_icon="✍️",
    layout="wide",
)

# Custom CSS for dark mode
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #FFFFFF !important;
        font-size: 2.5rem !important;
        margin-bottom: 2rem !important;
        text-align: center;
    }
    .input-container {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .output-container {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        margin-top: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .title-text {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    .subtitle-text {
        color: #E0E0E0 !important;
    }
    .content-text {
        color: #FFFFFF !important;
    }
    .help-text {
        color: #B0B0B0 !important;
    }
    
    /* Override Streamlit's default dark mode text colors */
    .stMarkdown, .stMarkdown p, .stText {
        color: #FFFFFF !important;
    }
    div[data-testid="stMarkdownContainer"] > p {
        color: #FFFFFF !important;
    }
    /* Ensure text inputs are visible in dark mode */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        color: #FFFFFF !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    /* Style for input labels */
    .stTextInput label, .stTextArea label {
        color: #E0E0E0 !important;
    }
    /* Style for button text */
    .stButton button {
        color: #FFFFFF !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    .stButton button:hover {
        background-color: rgba(255, 255, 255, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 class='title-text'>✍️ Groclake Marketing Content Generator</h1>
        <p style='font-size: 1.2rem;' class='subtitle-text'>Create compelling marketing content powered by AI</p>
    </div>
""", unsafe_allow_html=True)

# Initialize ModelLake
modellake = ModelLake()

# Input form container
st.markdown("<div class='input-container'>", unsafe_allow_html=True)

st.markdown("<h3 class='title-text'>📝 Content Details</h3>", unsafe_allow_html=True)

data1 = st.text_area(
    'Product/Service Details',
    placeholder="Describe your product/service, key features, benefits, and unique selling points...",
    help="Be specific about what makes your product or service stand out"
)

data2 = st.text_area(
    'Target Audience',
    placeholder="Define your audience's age, interests, pain points, and buying motivations...",
    help="The more specific you are about your audience, the better the content will be"
)

data3 = st.text_input(
    'Marketing Goal',
    placeholder="E.g., lead generation, brand awareness, website traffic, engagement...",
    help="What do you want to achieve with this content?"
)

data4 = st.text_input(
    'Tone & Style',
    placeholder="E.g., professional, casual, witty, inspirational, storytelling...",
    help="How should the content sound to your audience?"
)

st.markdown("</div>", unsafe_allow_html=True)

# Generate button centered
col1, col2, col3 = st.columns([1,1,1])
with col2:
    generate_button = st.button("🚀 Generate Content", use_container_width=True)

# Content generation
if generate_button:
    if not all([data1, data2, data3, data4]):
        st.error("⚠️ Please fill in all fields to generate content")
    else:
        with st.spinner("✨ Generating your marketing content..."):
            prompt = f"""
            You are a marketing expert specializing in AI-driven content generation. Your task is to create compelling, persuasive, and engaging marketing content based on the given product, audience, and goals.

            ### Product Details:
            {data1}

            ### Target Audience:
            {data2}

            ### Marketing Goal:
            {data3}

            ### Preferred Tone & Style:
            {data4}

            ### Content Type:
            Choose from the following:
            - Blog post
            - Social media post (Instagram, LinkedIn, Twitter)
            - Email campaign
            - Ad copy (Google Ads, Facebook Ads)
            - Product description
            - Landing page copy

            📌 **Instructions:**
            - Use attention-grabbing headlines and hooks.
            - Ensure the content is optimized for SEO and engagement.
            - Include a strong CTA (Call-to-Action) to drive action.
            - Make it persuasive, relatable, and easy to read.

            Generate the best-performing marketing content with high conversion potential.
            """
            
            chat_completion_request = {
                "groc_account_id": "c4ca4238a0b923820dcc509a6f75849b",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            }
            
            response = modellake.chat_complete(chat_completion_request)
            
            st.markdown("""
                <div class='output-container'>
                    <h3 class='title-text'>📊 Generated Marketing Content</h3>
                    <div class='content-text' style='font-size: 1.1rem; line-height: 1.6; white-space: pre-wrap;'>{}</div>
                </div>
            """.format(response['answer']), unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style='text-align: center; margin-top: 3rem; padding: 1rem; background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.1);'>
        <p class='subtitle-text'>Powered by Groclake AI | Built with Streamlit</p>
    </div>
""", unsafe_allow_html=True)