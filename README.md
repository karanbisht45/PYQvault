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

