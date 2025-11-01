import streamlit as st
import backend
import os
import time
from pathlib import Path
from utils.ocr_space_api import extract_text_from_image_or_pdf  

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

API_KEY = "YOUR_API_KEY"  

def _safe_filename(name: str):
    """Clean filenames to avoid special characters."""
    return "".join(c for c in name if c.isalnum() or c in (" ", ".", "_", "-")).rstrip().replace(" ", "_")


def upload_pyq(user):
    st.header("📤 Upload PYQ")
    with st.form("upload_form"):
        title = st.text_input("Title (optional)")
        subject = st.text_input("Subject")
        semester = st.text_input("Semester")
        year = st.text_input("Year")
        course_code = st.text_input("Course Code")
        university = st.text_input("University")
        tags = st.text_input("Tags (comma-separated)")
        uploaded_file = st.file_uploader("Choose PDF or Image", type=["pdf", "png", "jpg", "jpeg"])
        submitted = st.form_submit_button("Upload")

        if submitted:
            if not uploaded_file:
                st.error("⚠️ Please choose a file to upload")
                return

            # --- Save file locally ---
            ts = int(time.time() * 1000)
            safe_name = _safe_filename(uploaded_file.name)
            dest_name = f"{ts}_{safe_name}"
            dest_path = os.path.join(UPLOAD_DIR, dest_name)

            with open(dest_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # --- OCR extraction ---
            st.info("🔍 Extracting text from uploaded file... Please wait.")
            text, error = extract_text_from_image_or_pdf(dest_path, API_KEY)

            if error:
                st.error(f"OCR failed ❌: {error}")
                ocr_text = None
            else:
                ocr_text = text.strip()
                if ocr_text:
                    st.success("✅ Text extracted successfully!")
                    st.text_area("Extracted Text Preview:", ocr_text[:3000] + ("..." if len(ocr_text) > 3000 else ""), height=250)

                    # Save extracted text as .txt beside the uploaded file
                    txt_path = dest_path + ".txt"
                    try:
                        with open(txt_path, "w", encoding="utf-8") as txt_file:
                            txt_file.write(ocr_text)
                        st.info(f"📝 Extracted text saved as: {os.path.basename(txt_path)}")
                    except Exception as e:
                        st.warning(f"Couldn't save extracted text file: {e}")
                else:
                    st.warning("No text detected in this file.")

            # --- Store metadata in DB ---
            metadata = {
                "title": title or uploaded_file.name,
                "subject": subject,
                "semester": semester,
                "year": year,
                "course_code": course_code,
                "university": university,
                "tags": tags,
                "file_path": dest_path,
                "ocr_text": ocr_text,
                "uploaded_by": user["user_id"]
            }

            pyq_id = backend.add_pyq(metadata)
            st.success(f"🎉 Uploaded successfully! (ID: {pyq_id})")


def browse_pyqs(user=None):
    st.header("🔎 Browse PYQs")

    # ------------------- FILTERS -------------------
    col1, col2, col3 = st.columns(3)
    with col1:
        subject = st.text_input("Subject")
        semester = st.text_input("Semester")
    with col2:
        year = st.text_input("Year")
        course_code = st.text_input("Course Code")
    with col3:
        university = st.text_input("University")
        tags = st.text_input("Tags")

    # ------------------- SEARCH BY FILTERS -------------------
    if st.button("Search"):
        filters = {
            "subject": subject,
            "semester": semester,
            "year": year,
            "course_code": course_code,
            "university": university,
            "tags": tags,
        }
        results = backend.get_pyqs(filters)
        if not results:
            st.info("No PYQs found for these filters.")
            return
        for p in results:
            with st.expander(f"{p['title']} — {p.get('subject','-')} ({p.get('year','-')})"):
                st.write("Course:", p.get("course_code", "-"))
                st.write("University:", p.get("university", "-"))
                st.write("Tags:", p.get("tags", "-"))
                st.write("Uploaded on:", p.get("upload_date", "-"))
                try:
                    with open(p["file_path"], "rb") as f:
                        st.download_button(
                            label="📥 Download",
                            data=f,
                            file_name=os.path.basename(p["file_path"])
                        )
                except Exception:
                    st.error("File missing or cannot be opened.")

    # ------------------- SEARCH IN OCR TEXT -------------------
    st.divider()
    st.subheader("🔍 Search Keyword or Sentence inside Extracted OCR Text")

    topic = st.text_input("Enter keyword or phrase (case-insensitive)")
    if st.button("Search Topic Frequency"):
        topic = topic.strip().lower()
        if not topic:
            st.warning("⚠️ Please enter a keyword or phrase to search.")
        else:
            all_pyqs = backend.get_pyqs()
            if not all_pyqs:
                st.info("No uploaded files yet.")
            else:
                found = []
                for p in all_pyqs:
                    text = (p.get("ocr_text") or "").lower()
                    count = text.count(topic)
                    if count > 0:
                        found.append((p["title"], count))

                if found:
                    st.success(f"Occurrences of '{topic}':")
                    for title, count in found:
                        st.write(f"📘 {title} — appears **{count} times**")
                else:
                    st.warning(f"No occurrences of '{topic}' found.")

