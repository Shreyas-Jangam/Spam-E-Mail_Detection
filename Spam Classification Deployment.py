import streamlit as st
import pickle
from PIL import Image

st.set_page_config(
    page_title="Spam E-Mail Classification",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS styling
st.markdown("""
<style>
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Hide Streamlit default elements */
    .stDeployButton {
        display: none !important;
    }
    
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    .stToolbar {
        display: none !important;
    }
    
    /* Hide file change notification bar */
    .stAlert {
        display: none !important;
    }
    
    .stNotification {
        display: none !important;
    }
    
    div[data-testid="stNotificationContentInfo"] {
        display: none !important;
    }
    
    div[data-testid="stStatusWidget"] {
        display: none !important;
    }
    
    /* Hide main menu and hamburger */
    #MainMenu {
        display: none !important;
    }
    
    .css-1rs6os {
        display: none !important;
    }
    
    .css-17eq0hr {
        display: none !important;
    }
    
    /* Navigation bar styling */
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 1rem 2rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    /* Navigation title styling */
    .nav-title {
        text-align: center;
        color: #2c3e50 !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1) !important;
        display: block !important;
        visibility: visible !important;
    }
    
    /* Navigation subtitle styling */
    .nav-subtitle {
        text-align: center;
        color: #7f8c8d !important;
        font-size: 1rem !important;
        margin: 0.5rem 0 0 0 !important;
        font-style: italic !important;
        display: block !important;
        visibility: visible !important;
    }
    
    /* Add top margin to main content to account for fixed navbar */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        margin: 8rem auto 2rem auto;
        max-width: 800px;
        backdrop-filter: blur(10px);
    }
    
    /* Hide old title and subtitle styles */
    .main-title, .subtitle {
        display: none !important;
    }
    
    /* Input label styling */
    div[class*="stTextInput"] label p {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    /* Input field styling */
    div[class*="stTextInput"] input {
        border: 2px solid #e74c3c;
        border-radius: 10px;
        padding: 0.75rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.9);
    }
    
    div[class*="stTextInput"] input:focus {
        border-color: #667eea;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
        transform: translateY(-2px);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #e74c3c, #c0392b);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1.2rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(231, 76, 60, 0.3);
        width: 100%;
        margin-top: 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(231, 76, 60, 0.4);
        background: linear-gradient(45deg, #c0392b, #a93226);
    }
    
    /* Success message styling */
    .stSuccess {
        background: linear-gradient(45deg, #27ae60, #2ecc71);
        color: white;
        border-radius: 10px;
        padding: 1rem;
        font-size: 1.2rem;
        font-weight: 600;
        text-align: center;
        margin-top: 1rem;
        box-shadow: 0 5px 15px rgba(46, 204, 113, 0.3);
    }
    
    /* Image container */
    .image-container {
        text-align: center;
        margin: 2rem 0;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Footer styling */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: linear-gradient(45deg, #2c3e50, #34495e);
        color: white;
        text-align: center;
        padding: 1rem;
        font-size: 1rem;
        font-weight: 500;
        box-shadow: 0 -5px 15px rgba(0, 0, 0, 0.2);
        z-index: 999;
    }
    
    .footer a {
        color: #3498db;
        text-decoration: none;
        font-weight: 600;
    }
    
    .footer a:hover {
        color: #5dade2;
        text-decoration: underline;
    }
    
    /* Animation for elements */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-fade-in {
        animation: fadeInUp 0.8s ease-out;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        .main-container {
            margin: 1rem;
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Load models
tfidf = pickle.load(open("Pickle Files/feature.pkl", 'rb'))
model = pickle.load(open("Pickle Files/model.pkl", 'rb'))

# Navigation bar
st.markdown("""
<div class="navbar">
    <h1 class="nav-title">📧 Spam E-Mail Classifier</h1>
    <p class="nav-subtitle">Protect your inbox with AI-powered spam detection</p>
</div>
""", unsafe_allow_html=True)

# Main container
st.markdown('<div class="main-container animate-fade-in">', unsafe_allow_html=True)

# Image section
st.markdown('<div class="image-container">', unsafe_allow_html=True)
image = Image.open("Data Source/images.jpg")
st.image(image, caption="Advanced Machine Learning for Email Security", use_column_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Input section
st.markdown("### 🔍 Enter Email Message to Analyze")
input_mail = st.text_input("", placeholder="Paste your email content here...", help="Enter the email message you want to classify as spam or ham")

# Prediction section
if st.button('🚀 Analyze Email'):
    if input_mail.strip():
        with st.spinner('🔄 Analyzing email content...'):
            vector_input = tfidf.transform([input_mail])
            result = model.predict(vector_input)
            
            if result == 0:
                st.error("🚨 **SPAM DETECTED!** This email appears to be spam.")
                st.markdown("""
                <div style='background: linear-gradient(45deg, #e74c3c, #c0392b); color: white; padding: 1rem; border-radius: 10px; margin-top: 1rem;'>
                    <h4>⚠️ Warning: Potential Spam Email</h4>
                    <p>This message has characteristics commonly found in spam emails. Please be cautious and avoid clicking any links or providing personal information.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.success("✅ **LEGITIMATE EMAIL** This email appears to be genuine.")
                st.markdown("""
                <div style='background: linear-gradient(45deg, #27ae60, #2ecc71); color: white; padding: 1rem; border-radius: 10px; margin-top: 1rem;'>
                    <h4>✅ Safe Email Detected</h4>
                    <p>This message appears to be a legitimate email. However, always exercise caution with unknown senders.</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter an email message to analyze.")

# Additional info section
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 1rem; background: rgba(52, 152, 219, 0.1); border-radius: 10px; margin: 1rem 0;'>
    <h4>🛡️ How It Works</h4>
    <p>Our AI model uses advanced machine learning algorithms including:</p>
    <div style='display: flex; justify-content: space-around; flex-wrap: wrap; margin-top: 1rem;'>
        <div style='margin: 0.5rem;'>🧠 <strong>Logistic Regression</strong></div>
        <div style='margin: 0.5rem;'>🌳 <strong>Decision Trees</strong></div>
        <div style='margin: 0.5rem;'>🔍 <strong>K-Nearest Neighbors</strong></div>
        <div style='margin: 0.5rem;'>🌲 <strong>Random Forest</strong></div>
    </div>
    <p style='margin-top: 1rem; font-style: italic;'>Combined with TF-IDF text analysis for maximum accuracy</p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>🚀 Developed with ❤️ by <strong>Shreyas Jangam</strong> | Powered by Machine Learning & Streamlit</p>
</div>
""", unsafe_allow_html=True)