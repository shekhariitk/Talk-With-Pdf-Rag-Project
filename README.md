# 📄 Talk with PDF

**Chat, search, and extract insights from your documents instantly—powered by AI.**

---

## 🚀 Overview

**Talk with PDF** is a modern, interactive Streamlit application that lets you upload PDF documents and chat with them using advanced AI. Ask questions, summarize content, or find specific information—all within a clean, intuitive interface. Your documents are processed securely, with all content staying private and local.

---

## ✨ Features

- **Upload multiple PDFs** and process them in seconds.
- **Intelligent chat interface**—ask natural language questions and get immediate answers from your documents.
- **Document-aware responses**—the AI answers based only on uploaded content.
- **Modern, responsive UI** with smooth animations, status indicators, and clear feedback.
- **Secure processing**—your files are never sent off your device.
- **Powered by LangChain and Euri AI**.

---

## 🛠️ Installation

1. **Clone the repository:**
```bash
git https://github.com/shekhariitk/Talk-With-Pdf-Rag-Project.git
```

2. **Set up the environment (Python 3.9+ recommended):**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Set your Euri AI API key:**
Create a `.env` file in your project root and add:
```
EURI_API_KEY=your_api_key_here
```

4. **Run the app:**
```bash
streamlit run main.py
```

5. **Open your browser** to `http://localhost:8501` and start chatting with your PDFs!

---

## 📦 Project Structure
```
project/
│
├── main.py # Main Streamlit app script
├── app/
│ ├── ui.py # File uploader UI module
│ ├── pdf_utils.py # PDF text extraction utilities
│ ├── vectorstore_utils.py # FAISS vector store utilities
│ ├── chat_utils.py # Chat model utilities
│ └── config.py # Environment config handling
├── requirements.txt # Python dependencies
├── .env.example # Example environment file
└── README.md # This file!
```
---

## 📚 Usage

1. **Upload your PDFs** in the sidebar.
2. **Click "Process Documents"** to extract and index the text.
3. **Ask questions** in the chat—get answers directly from your documents.
4. **Enjoy seamless insights** with a modern, clear interface.

---

## 🖼️ Screenshots

*(Add your own screenshots here for maximum engagement!)*

---

## 💡 Ideas for the Roadmap

- **Support more file formats** (pdf)
- **Document previews** and thumbnail displays
- **Dark mode toggle**
- **Multi-language support**
- **Save and load chat sessions**

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## 📜 License

MIT License. See `LICENSE` for details.

---

## 🗺️ Acknowledgements

- **Streamlit** for the beautiful app framework
- **LangChain** for LLM orchestration
- **Euri AI** for powerful chat models

## Demo app
(https://talk-with-pdf-rag-project-shekhar.streamlit.app)
