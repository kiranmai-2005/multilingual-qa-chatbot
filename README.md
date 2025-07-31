# 🌍 Multilingual Q&A Chatbot

A multilingual voice-based chatbot built with **Streamlit**, integrated with **Google's Generative Language API** and **Wikipedia** for answering user queries in various languages. It supports **speech input/output**, **translation**, and **auto-detects language**, making it perfect for users who struggle to communicate confidently in English.

---

## 🚀 Features

- 🌐 Multilingual question-answering
- 🔍 Auto language detection (supports over 50 languages)
- 🎤 Voice input using SpeechRecognition
- 🔊 Voice output using pyttsx3 / gTTS
- 📚 Real-time answers using Wikipedia content
- 🧠 Google Generative Language API for contextual responses
- 🖥️ Clean Streamlit UI with dropdowns and dark mode

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Google Generative Language API
- Wikipedia API
- `SpeechRecognition`, `pyttsx3`, `gTTS`
- `googletrans` / `langdetect`
- `datetime`, `os`, `tempfile`, `sys`, `io`

---

## 📁 Folder Structure

```
multilingual-qa-chatbot/
├── app/
│   ├── __init__.py
│   ├── detect_language.py         # Detects input language
│   ├── qa_pipeline.py             # Generates answers using GenAI and Wiki
│   ├── translate.py               # Handles translation
│   ├── wikipedia_fetcher.py       # Fetches context from Wikipedia
├── streamlit_app.py               # Main Streamlit app
├── main.py                        # Optional runner file
├── requirements.txt               # Python dependencies
├── .streamlit/
│   └── secrets.toml               # API key stored securely
└── README.md
```

---

## 📦 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/kiranmai-2005/multilingual-qa-chatbot.git
cd multilingual-qa-chatbot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your API key
Create a `.streamlit/secrets.toml` file:
```toml
[api_keys]
genai_api = "your_api_key_here"
```

### 4. Run the app
```bash
streamlit run streamlit_app.py
```

---

## 🔐 API Used

- **Google Generative Language API** (for LLM-based answers)
- **Wikipedia API** (for retrieving context in user’s preferred language)

---

## 🎯 Use Case

This chatbot is ideal for:
- Students learning in non-English environments
- People preparing for interviews or oral exams
- Users who understand English but struggle to speak it confidently

It provides an accessible way to get informative, multilingual responses using both voice and text.

---

## 📬 Author

**Bobbireddi Kiranmai**  
GitHub: [@kiranmai-2005](https://github.com/kiranmai-2005)  
Built with 💙 during my learning journey in AI and Web Development

---

## 🌟 Show Your Support

If you like this project, please ⭐ star this repository and share it!
