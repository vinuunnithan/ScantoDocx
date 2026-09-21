# 📝 PNG to Word Converter (Cloud Edition)

A secure, cloud-based web application built with **Streamlit** that utilizes **Google Gemini AI** and **Pandoc** to convert text trapped inside PNG images (OCR) into crisp, well-formatted Markdown, and then compiles it into a downloadable Microsoft Word (`.docx`) document.

🤝 **Developed with the help of Gemini AI:** This application, including its interactive interface layout, cloud file handling backend, and architectural evolution from a desktop script to a web app, was built in active collaboration with Gemini AI.

Designed for non-technical users and coworkers to seamlessly transcribe documents with zero local setup.

---

## ✨ Features

- **AI-Assisted Engineering:** Codebase co-developed, optimized, and prepared for cloud distribution with the help of Gemini AI.
- **No Installation Required:** Runs entirely in any web browser.
- **Drag-and-Drop Interface:** Easily upload multiple PNG files at once.
- **Alphabetical Processing:** Automatically sorts uploaded images by name to preserve correct document ordering.
- **Compliance & Legal Safety:** Built-in disclaimer sidebar with a digital signature requirement to manage operational risks.
- **Privacy-First Design:** Files are processed entirely in temporary memory buffers and are destroyed the moment the browser tab is closed.

---

## 🔑 Getting Started: How to Get Your Gemini API Key

To use this tool, you or your users will need a Google Gemini API key. Getting one takes less than a minute and is completely free for experimental tiers:

1. Go to **[Google AI Studio](https://google.com)** and log in with your Google or Google Workspace account.
2. Click the prominent blue **"Get API key"** button in the top-left corner.
3. Click **"Create API key"**, select a Google Cloud project (or let it generate a new default one), and copy your generated key string.
4. Paste that key directly into the application field to unlock the file processor.

---

## ⚙️ How to Deploy (Streamlit Community Cloud)

You can host this application for free on Streamlit Community Cloud by following these simple steps:

### 1. Structure Your Repository
Ensure your GitHub repository contains these three essential files:
```text
your-repo/
├── app.py          (The main Python application script)
├── requirements.txt (Python library dependencies)
└── packages.txt     (Linux system-level dependencies for Pandoc)
```

### 2. File Configurations

**`requirements.txt`**
```text
google-genai
pypandoc
streamlit
```

**`packages.txt`**
```text
pandoc
```

### 3. Deploy to the Web
1. Go to [share.streamlit.io](https://streamlit.io) and log in using your GitHub account.
2. Click the **"New app"** button.
3. Select your repository, the appropriate branch, and set the main file path to `app.py`.
4. *(Optional)* If you want to bake a shared company API key into the app so your coworkers don't have to input their own, click **Advanced Settings**, navigate to **Secrets**, and paste:
   ```toml
   GEMINI_API_KEY = "your_actual_api_key_here"
   ```
5. Click **Deploy**. Your app will be live and shareable in under two minutes!

---

## ⚠️ Disclaimer
This application is developed strictly for experimental, proof-of-concept, and internal evaluation purposes. Generated text outputs are handled via artificial intelligence and may contain errors, hallucinations, or formatting discrepancies. Use at your own discretion.

***
*Developed in collaboration with Gemini AI.*
