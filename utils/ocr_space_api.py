import requests
import os

def extract_text_from_image_or_pdf(file_path, api_key):
    """Extract text from image or multi-page PDF using OCR.Space API."""
    url = "https://api.ocr.space/parse/image"
    payload = {
        "apikey": api_key,
        "language": "eng",
        "isOverlayRequired": False,
        "isCreateSearchablePdf": False,
        "isSearchablePdfHideTextLayer": True,
        "scale": True,
        "OCREngine": 2
    }

    try:
        # Determine file type
        filename = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            response = requests.post(url, files={"filename": (filename, f)}, data=payload)

        # Parse the response safely
        if response.status_code != 200:
            return None, f"OCR API error: HTTP {response.status_code}"

        result = response.json() if response.headers.get("Content-Type", "").startswith("application/json") else {}

        if result.get("IsErroredOnProcessing"):
            return None, result.get("ErrorMessage", "Error in OCR processing")

        parsed_results = result.get("ParsedResults", [])
        if not parsed_results:
            return None, "No text found in image/PDF"

        # Combine all pages' text
        full_text = ""
        for page in parsed_results:
            full_text += page.get("ParsedText", "") + "\n"

        return full_text.strip(), None

    except Exception as e:
        return None, f"OCR request failed: {e}"
