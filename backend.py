# backend.py
import io
import re
import base64
import cv2
import numpy as np
from PIL import Image
import easyocr
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import nltk
from nltk.corpus import stopwords

# Download NLTK stopwords quietly
nltk.download('stopwords', quiet=True)
STOP_WORDS = set(stopwords.words('english'))

app = FastAPI(title="Visual Spec Extractor API")

# Enable Cross-Origin Resource Sharing (CORS) so the React frontend can talk to it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("[*] Initializing EasyOCR on CPU...")
READER = easyocr.Reader(['en'], gpu=False)
print("[*] EasyOCR Ready.")


def is_meaningful_token(word: str) -> bool:
    """Filters out noise tokens, OCR artifacts, single-letter junk, and stopwords."""
    clean = re.sub(r'[^\w\s]', '', word).strip()

    # Eliminate empty or single random non-numeric characters
    if len(clean) <= 1 and not clean.isdigit():
        return False

    # Eliminate words that have no alphanumeric characters
    if not any(c.isalnum() for c in clean):
        return False

    # Eliminate conversational English stopwords
    if clean.lower() in STOP_WORDS:
        return False

    # Eliminate tokens with excessive punctuation or garbled symbols
    alpha_num_ratio = sum(c.isalnum() for c in word) / max(len(word), 1)
    if alpha_num_ratio < 0.6:
        return False

    return True


def extract_meaningful_specifications(text_lines: list[str]) -> dict:
    """Extracts physical and electrical specifications using context and unit rules."""
    full_text = " ".join(text_lines)
    clean_text = full_text.lower()
    specs = {}

    # Weight / Mass (e.g., 500g, 2.5 kg, 16 oz)
    weight = re.search(r'(\b\d+(?:\.\d+)?)\s*(kg|kilograms?|g|grams?|mg|oz|lbs?|pounds?)\b', clean_text)
    if weight:
        specs["Weight"] = f"{weight.group(1)} {weight.group(2)}"

    # Volume / Capacity (e.g., 750ml, 1.5 l, 12 fl oz)
    volume = re.search(r'(\b\d+(?:\.\d+)?)\s*(ml|milliliters?|l|liters?|fl\s*oz)\b', clean_text)
    if volume:
        specs["Volume"] = f"{volume.group(1)} {volume.group(2)}"

    # Dimensions (e.g., 10x20x5 cm, 120 x 80 mm)
    dimensions = re.search(r'(\b\d+(?:\.\d+)?\s*[xX*×]\s*\d+(?:\.\d+)?(?:\s*[xX*×]\s*\d+(?:\.\d+)?)?\s*(cm|mm|m|inch|inches|in)\b)', clean_text)
    if dimensions:
        specs["Dimensions"] = dimensions.group(1).strip()

    # Voltage (e.g., 220v, 5v, 240 vac)
    voltage = re.search(r'(\b\d+(?:\.\d+)?)\s*(v|volts?|kv|vac|vdc)\b', clean_text)
    if voltage:
        specs["Voltage"] = f"{voltage.group(1)} {voltage.group(2)}"

    # Frequency (e.g., 50hz, 60 hz)
    freq = re.search(r'(\b\d+(?:\.\d+)?)\s*(hz|khz|mhz)\b', clean_text)
    if freq:
        specs["Frequency"] = f"{freq.group(1)} {freq.group(2)}"

    # Power (e.g., 100w, 1500 watts, 2.5 kw)
    power = re.search(r'(\b\d+(?:\.\d+)?)\s*(w|watts?|kw)\b', clean_text)
    if power:
        specs["Power Rating"] = f"{power.group(1)} {power.group(2)}"

    # Current (e.g., 2a, 500 ma)
    current = re.search(r'(\b\d+(?:\.\d+)?)\s*(a|amps?|ma)\b', clean_text)
    if current:
        specs["Current"] = f"{current.group(1)} {current.group(2)}"

    # Anchor metadata (Model, Batch, Expiry, Manufacturing)
    anchors = {
        "Model": r'(?:model|item\s*no|mod)\s*[:#-]?\s*([a-zA-Z0-9\-_]{3,15})',
        "Batch/Lot": r'(?:batch|lot|b\.no)\s*[:#-]?\s*([a-zA-Z0-9\-_]{3,12})',
        "Expiry Date": r'(?:exp|expiry|use\s*by)\s*[:#-]?\s*([0-9]{1,2}[/\-\.][0-9]{2,4}|[a-zA-Z]{3}\s*\d{2,4})',
        "Mfg Date": r'(?:mfd|mfg|pkd|pack\s*date)\s*[:#-]?\s*([0-9]{1,2}[/\-\.][0-9]{2,4}|[a-zA-Z]{3}\s*\d{2,4})'
    }

    for key, pattern in anchors.items():
        match = re.search(pattern, clean_text)
        if match:
            specs[key] = match.group(1).upper()

    return specs


@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('RGB')
    img_np = np.array(image)
    img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    # OCR step
    raw_results = READER.readtext(img_np)

    meaningful_lines = []
    meaningful_keywords = []

    for bbox, text, confidence in raw_results:
        # Ignore poor detections
        if confidence < 0.35:
            continue

        raw_tokens = text.split()
        valid_tokens = [tok for tok in raw_tokens if is_meaningful_token(tok)]

        if valid_tokens:
            cleaned_line = " ".join(valid_tokens)
            meaningful_lines.append(cleaned_line)
            meaningful_keywords.extend(valid_tokens)

            # Draw green bounding boxes around detected regions
            pts = np.array(bbox, np.int32).reshape((-1, 1, 2))
            cv2.polylines(img_cv, [pts], isClosed=True, color=(34, 197, 94), thickness=2)

    # Encode annotated image to Base64
    _, buffer = cv2.imencode('.jpg', img_cv)
    annotated_base64 = base64.b64encode(buffer).decode('utf-8')

    # Run spec extraction
    structured_specs = extract_meaningful_specifications(meaningful_lines)
    unique_keywords = list(dict.fromkeys(meaningful_keywords))

    return {
        "annotated_image": f"data:image/jpeg;base64,{annotated_base64}",
        "meaningful_keywords": unique_keywords,
        "specifications": structured_specs
    }