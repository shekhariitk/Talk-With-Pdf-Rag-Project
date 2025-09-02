import streamlit as st
from app.ui import pdf_uploader
from app.pdf_utils import extract_text_from_pdf
from app.vectorstore_utils import create_faiss_index, retrive_relevant_docs
from app.chat_utils import get_chat_model, ask_chat_model
from langchain.text_splitter import RecursiveCharacterTextSplitter
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
EURI_API_KEY = os.getenv("EURI_API_KEY")
if not EURI_API_KEY:
    st.error("EURI_API_KEY not found. Please set it in the .env file.")



# ---- App Config & Theme ----
st.set_page_config(
    page_title="Talk with PDF",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "📄 Talk with PDF — Chat with your documents using AI"
    }
)

# ---- Custom Modern UI CSS ----
st.markdown("""
<style>
    /* Main App Container */
    .app-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 1rem;
    }
    /* Hero Section */
    .hero {
        background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);
        border-radius: 1rem;
        padding: 2.5rem 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.06);
        text-align: center;
    }
    .hero-title {
        color: #2b313e;
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.05em;
    }
    .hero-subtitle {
        color: #666;
        font-size: 1.35rem;
        margin: 0.5rem 0 0 0;
    }
    /* Sidebar */
    .sidebar-section {
        background: #f8f9fa;
        border-radius: 1rem;
        padding: 1.25rem;
        margin-bottom: 1.25rem;
    }
    /* Button Styles */
    .stButton>button {
        background: linear-gradient(135deg, #ff4b4b 0%, #e03a3a 100%);
        color: white;
        border: none;
        border-radius: 0.75rem;
        padding: 0.75rem 1.25rem;
        font-weight: bold;
        transition: all 0.2s ease;
        margin: 0.25rem 0;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #ff3333 0%, #cc2828 100%);
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
        transform: translateY(-1px);
    }
    /* Chat Bubbles */
    .chat-message {
        padding: 1.25rem;
        border-radius: 1rem;
        margin: 1rem 0;
        display: flex;
        flex-direction: row;
        align-items: flex-start;
        gap: 0.75rem;
        width: fit-content;
        max-width: 85%;
        animation: slideIn 0.15s ease-out forwards;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    }
    /* User Message */
    .chat-message.user {
        background: linear-gradient(135deg, #2b313e 0%, #1b2027 100%);
        color: white;
        margin-left: auto;
        flex-direction: row-reverse;
    }
    /* Assistant Message */
    .chat-message.assistant {
        background: linear-gradient(135deg, #f0f2f6 0%, #e8ebf0 100%);
        color: #2b313e;
        margin-right: auto;
    }
    /* Avatar */
    .chat-message .avatar {
        width: 2.5rem;
        height: 2.5rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        flex-shrink: 0;
        background: #ff4b4b;
        color: white;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    }
    .chat-message.user .avatar {
        background: #2b313e;
    }
    .chat-message.assistant .avatar {
        background: #2b313e;
    }
    /* Message Content */
    .chat-message .message {
        flex: 1;
        margin: 0 0.75rem;
    }
    .chat-message .timestamp {
        font-size: 0.7rem;
        opacity: 0.7;
        margin-top: 0.25rem;
        text-align: right;
        width: 100%;
    }
    /* Status & Feedback */
    .status-success {
        background: #d4edda;
        color: #155724;
        padding: 0.65rem;
        border-radius: 0.4rem;
        margin: 0.75rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        animation: fadeIn 0.3s ease-out forwards;
    }
    .status-info {
        background: #d1ecf1;
        color: #0c5460;
        padding: 0.65rem;
        border-radius: 0.4rem;
        margin: 0.75rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .status-error {
        background: #f8d7da;
        color: #721c24;
        padding: 0.65rem;
        border-radius: 0.4rem;
        margin: 0.75rem 0;
        animation: shake 0.5s ease;
    }
    /* Chat Input & Progress */
    .stChatInput {
        border-radius: 1rem;
        background: #f8f9fa;
        padding: 0.5rem;
    }
    .stSpinner {
        margin: 0.5rem 0;
    }
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideIn {
        0% { transform: translateY(20px); opacity: 0; }
        100% { transform: translateY(0px); opacity: 1; }
    }
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
        20%, 40%, 60%, 80% { transform: translateX(10px); }
    }
    /* Footer */
    .footer {
        text-align: center;
        color: #666;
        font-size: 0.85rem;
        margin: 2rem 0 0 0;
        padding: 0.5rem 0;
    }
    /* Doc Preview (if you add thumbnails later) */
    .doc-preview {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ---- Session State ----
if "messages" not in st.session_state:
    st.session_state.messages = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "chat_model" not in st.session_state:
    st.session_state.chat_model = None

# ---- Hero Section ----
st.markdown("""
<div class="app-container">
    <div class="hero">
        <h1 class="hero-title">📄 Talk with PDF</h1>
        <p class="hero-subtitle">Chat, search, and extract insights from your documents instantly</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ---- Sidebar: File Upload & Processing ----
with st.sidebar:
    st.markdown("## 🗂️ Your Documents")
    st.markdown("Upload PDFs to start chatting. You can upload multiple files at once.")
    st.markdown("---")
    
    uploaded_files = pdf_uploader()

    with st.expander("ℹ️ How it works", expanded=False):
        st.markdown("1. **Upload your PDFs**\n2. **Click 'Process Documents'**\n3. **Chat with your files**")
        st.markdown("Your documents never leave your device and are processed securely.")

    if uploaded_files:
        st.markdown('<div class="status-success">📄 ' + str(len(uploaded_files)) + ' document(s) ready to process</div>', unsafe_allow_html=True)
        if st.button("Process Documents 🚀", key="process_btn"):
            with st.spinner("Extracting text and preparing for chat..."):
                try:
                    all_texts = [extract_text_from_pdf(file) for file in uploaded_files]
                    text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1000,
                        chunk_overlap=200,
                        length_function=len,
                    )
                    chunks = []
                    for text in all_texts:
                        chunks.extend(text_splitter.split_text(text))
                    vectorstore = create_faiss_index(chunks)
                    st.session_state.vectorstore = vectorstore
                    chat_model = get_chat_model(EURI_API_KEY)
                    st.session_state.chat_model = chat_model
                    st.markdown('<div class="status-success">✅ Documents processed & ready to chat!</div>', unsafe_allow_html=True)
                    st.balloons()
                except Exception as e:
                    st.markdown('<div class="status-error">❌ Error processing documents. Please try again.</div>', unsafe_allow_html=True)
                    st.error(str(e))

    if "vectorstore" in st.session_state and st.session_state.vectorstore:
        st.markdown('<div class="status-success">✅ Ready to chat! You can ask questions now.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-info">ℹ️ Upload and process files to enable chat.</div>', unsafe_allow_html=True)

# ---- Chat Area ----
st.markdown("## 💬 Chat with Your Documents")
st.markdown("Ask anything about your uploaded PDFs. Remember to upload and process documents first.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        st.caption(message["timestamp"])

if prompt := st.chat_input("Ask a question about your files..."):
    timestamp = time.strftime("%H:%M")
    st.session_state.messages.append({"role": "user", "content": prompt, "timestamp": timestamp})
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(timestamp)

    if st.session_state.vectorstore and st.session_state.chat_model:
        with st.chat_message("assistant"):
            with st.spinner("Searching your files..."):
                relevant_docs = retrive_relevant_docs(st.session_state.vectorstore, prompt)
                context = "\n\n".join([doc.page_content for doc in relevant_docs])
                system_prompt = f"""
                You are Talk with PDF, a smart document assistant.
                Based on the user's documents, answer the question clearly and accurately.
                If the information is not in the documents, clearly state that.

                Documents:
                {context}

                Question: {prompt}

                Answer:"""
                response = ask_chat_model(st.session_state.chat_model, system_prompt)
            st.markdown(response)
            st.caption(timestamp)
            st.session_state.messages.append({"role": "assistant", "content": response, "timestamp": timestamp})
    else:
        with st.chat_message("assistant"):
            st.markdown('<div class="status-error">⚠️ Please upload and process documents before asking questions.</div>', unsafe_allow_html=True)
            st.caption(timestamp)

# ---- Footer ----
st.markdown('<div class="footer">🤖 Powered by Euri AI & LangChain</div>', unsafe_allow_html=True)
