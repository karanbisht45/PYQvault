# 🧠 PyQVault — Smart PYQ Management & OCR Analyzer

PyQVault is an intelligent **Previous Year Question (PYQ) Management System** built with **Streamlit** and **OCR-powered text extraction**.  
It allows users to **upload, search, and analyze** question papers by automatically extracting text from PDFs and images — making topic discovery faster than ever!

---

## 🚀 Features

### 🧩 Upload & Extract
- Upload **PDFs or images** of question papers.
- Real-time **OCR (Optical Character Recognition)** extraction using **OCR.Space API**.
- Multi-page PDF text extraction supported.
- Displays “Extracting text…” progress and shows extracted text on success.
- Automatically stores both the file and its extracted text.

### 🔍 Smart Search
- Search by **subject, semester, year, university, course code**, or **tags**.
- Built-in **keyword/sentence frequency search** inside extracted text.
- Instantly find **how many times a topic or question appears** across multiple PYQs.

### 📂 Organized Management
- All uploads are timestamped and stored in a clean folder structure.
- Extracted text is automatically saved as `.txt` beside the uploaded file.
- Metadata (title, subject, semester, etc.) stored in SQLite database.

### 👩‍🏫 User-Friendly Interface
- Built entirely with **Streamlit** for simplicity and interactivity.
- Upload progress feedback: “Extracting text…” → “✅ Text extracted successfully!”
- Download button for each uploaded PYQ.
- Clear separation between uploader and browser sections.

---

## 🛠️ Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend/UI** | Streamlit |
| **Backend** | Python |
| **Database** | SQLite |
| **OCR Engine** | OCR.Space API |
| **Libraries Used** | `streamlit`, `sqlite3`, `os`, `time`, `pathlib` |

---

## ⚙️ Project Structure

PyQVault/
│
├── app.py # Main Streamlit app (upload + browse interface)
├── backend.py # Database handling (insert, search, fetch)
├── utils/
│ ├── ocr_space_api.py # Handles OCR extraction via API
│ └── file_handler.py # Uploads, downloads, and file utilities
├── uploads/ # Auto-created folder for stored files
├── database/ (optional) # SQLite DB file stored here
├── .gitignore # Excludes DB, uploads, and secrets
└── README.md # You're reading this 😎


---

## 🔑 Environment Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/PyQVault.git
   cd PyQVault
2. **Install Dependencies**
  ```bash
  pip install -r requirements.txt
```
3.**Add your OCR API key**
  ```bash
  Open utils/ocr_space_api.py
  Replace your key:
  API_KEY = "YOUR_OCR_SPACE_API_KEY"
```
4.**Run the Streamlit app**
  ```bash
  streamlit run app.py
```

##🧠 HOW IT WORKS

1️⃣  Upload a question paper (.pdf, .jpg, .png, .jpeg)
2️⃣  The app extracts all text using the OCR.Space API
3️⃣  The extracted content is saved and displayed instantly
4️⃣  Use the keyword search box to find topics or even full sentences
5️⃣  The app shows how many times that word/sentence appears across all uploaded question papers

