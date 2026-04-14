import streamlit as st
import requests
import datetime
import time

# --- Configuration ---
BASE_URL = "http://localhost:8000" 

st.set_page_config(
    page_title="Premium Travel AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- PREMIUM UI/UX CSS (Glassmorphism & Backgrounds) ---
st.markdown("""
<style>
    /* 1. Full-screen high-res background of the world */
    [data-testid="stAppViewContainer"] {
        background-image: url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* 2. Glassmorphism container for the main app */
    .block-container {
        background: rgba(255, 255, 255, 0.88); 
        backdrop-filter: blur(15px);          
        -webkit-backdrop-filter: blur(15px);
        border-radius: 24px;
        padding: 3rem 4rem !important;
        margin-top: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.2);
        max-width: 1050px; 
    }
    
    /* 3. Dark, sleek Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(10, 15, 28, 0.96) !important; 
    }
    [data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }
    
    .premium-header {
        background: linear-gradient(135deg, #1E40AF 0%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.2rem;
        margin-bottom: 0px;
        text-align: center;
        letter-spacing: -1px;
    }

    /* 4. Chat Bubble Styling */
    [data-testid="stChatMessage"] {
        background-color: #ffffff;
        border-radius: 18px;
        padding: 18px 22px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.04);
        margin-bottom: 15px;
        border: 1px solid #f1f5f9;
    }
    [data-testid="stChatMessage"][data-testid="user"] {
        background-color: #F1F5F9;
        border-left: 5px solid #3B82F6;
    }
    [data-testid="stChatMessage"][data-testid="assistant"] {
        border-left: 5px solid #10B981;
    }

    /* 5. Image Grid Styling - FORCED UNIFORM SIZE */
    .stImage > img {
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        /* These two lines force all images to be the same landscape size */
        aspect-ratio: 3 / 2;
        object-fit: cover; 
        width: 100%;
    }
    .stImage > img:hover {
        transform: translateY(-5px) scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/870/870143.png", width=70)
    st.markdown("## 🌐 Global Agent")
    st.caption("AI-Powered Itinerary Architect")
    st.divider()
    st.markdown("### 🛠️ System Status")
    st.success("NLP Core: Online")
    st.success("Routing Engine: Stable")
    st.divider()
    st.markdown("<small style='opacity: 0.5;'>Atriyo's Intelligence Lab © 2026</small>", unsafe_allow_html=True)

# --- MAIN HEADER ---
st.markdown("<h1 class='premium-header'>Compute Your Next Adventure</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#475569; font-size:19px; font-weight:500; margin-bottom:40px;'>Intelligent planning for the modern traveler.</p>", unsafe_allow_html=True)

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- TRENDING GRID (With Goa, Uniformly Sized) ---
if len(st.session_state.messages) == 0:
    st.markdown("### 📸 Trending This Season")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    # Added &h=400 to the Unsplash URLs to fetch them in a more uniform shape before CSS crops them
    with col1:
        st.image("https://images.unsplash.com/photo-1499856871958-5b9627545d1a?q=80&w=600&h=400&auto=format&fit=crop", caption="Paris, France")
    with col2:
        st.image("https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?q=80&w=600&h=400&auto=format&fit=crop", caption="Tokyo, Japan")
    with col3:
        st.image("https://images.unsplash.com/photo-1512757776214-26d36777b513?q=80&w=600&h=400&auto=format&fit=crop", caption="Goa, India")
    
    st.markdown("<br><hr style='border: 1px solid #f1f5f9; opacity: 0.5;'>", unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": "Welcome. I am initialized and ready to chart your next journey. Where shall we begin?"})

# --- CHAT DISPLAY ---
for message in st.session_state.messages:
    # Skip welcome message in history once interaction starts
    if message["role"] == "assistant" and "Welcome." in message["content"] and len(st.session_state.messages) > 1:
        continue 
        
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT INPUT & LOGIC ---
if prompt := st.chat_input("Specify coordinates... (e.g., A 5-day cultural trip to Goa)"):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        st.toast("Accessing global travel nodes...", icon="🌍")
        
        with st.spinner("Synthesizing your bespoke itinerary..."):
            try:
                payload = {"question": prompt}
                response = requests.post(f"{BASE_URL}/query", json=payload)
                
                if response.status_code == 200:
                    answer = response.json().get("answer", "No answer returned.")
                    
                    markdown_content = f"""
#### 🗺️ Bespoke Travel Sequence
*Verified on: {datetime.datetime.now().strftime('%d %B %Y')}*

---
{answer}
---
<small style='color: #94A3B8;'>⚠️ *AI synthesized data. Verify operational hours and travel requirements locally.*</small>
                    """
                    st.markdown(markdown_content, unsafe_allow_html=True)
                    st.session_state.messages.append({"role": "assistant", "content": markdown_content})
                    st.toast("Processing complete.", icon="✅")
                    
                else:
                    st.error(f"⚠️ **Interface Error:** Backend returned status `{response.status_code}`")
                    
            except requests.exceptions.ConnectionError:
                st.error("🔌 **Fatal Error:** Could not connect to the local processing node (localhost:8000).")