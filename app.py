import re
import cv2
import numpy as np
import easyocr
import gradio as gr
from PIL import Image

# 1. Initialize EasyOCR explicitly for CPU
print("[*] Initializing EasyOCR on CPU...")
READER = easyocr.Reader(['en'], gpu=False)
print("[*] Model loaded successfully.")


# 2. Rule-Based Specification Parsing Engine
def extract_specifications(text: str) -> dict:
    """
    Scans raw OCR text using regex patterns to isolate numerical
    values associated with standard physical/electrical units.
    """
    clean_text = text.lower()
    specs = {}

    # Weight pattern (e.g., 500g, 2.5 kg, 100 grams, 16 oz, 5 lbs)
    weight_match = re.search(r'(\d+(?:\.\d+)?)\s*(kg|kilograms?|g|grams?|oz|ounces?|lbs?|pounds?)', clean_text)
    if weight_match:
        specs["Weight"] = f"{weight_match.group(1)} {weight_match.group(2)}"

    # Volume pattern (e.g., 250ml, 1.5 l, 2 liters, 12 fl oz)
    volume_match = re.search(r'(\d+(?:\.\d+)?)\s*(ml|milliliters?|l|liters?|fl\s*oz)', clean_text)
    if volume_match:
        specs["Volume"] = f"{volume_match.group(1)} {volume_match.group(2)}"

    # Dimensions pattern (e.g., 10x20x5 cm, 15 x 20 mm, 5x10 in)
    dim_match = re.search(r'(\d+(?:\.\d+)?)\s*[xX*]\s*(\d+(?:\.\d+)?)(?:\s*[xX*]\s*(\d+(?:\.\d+)?))?\s*(cm|mm|m|inch|inches|in)', clean_text)
    if dim_match:
        specs["Dimensions"] = dim_match.group(0).strip()

    # Voltage pattern (e.g., 220v, 5v, 12 v, 240 volts, 3.3kv)
    volt_match = re.search(r'(\d+(?:\.\d+)?)\s*(v|volts?|kv)', clean_text)
    if volt_match:
        specs["Voltage"] = f"{volt_match.group(1)} {volt_match.group(2)}"

    # Power rating pattern (e.g., 100w, 15 watts, 2.5 kw)
    power_match = re.search(r'(\d+(?:\.\d+)?)\s*(w|watts?|kw)', clean_text)
    if power_match:
        specs["Power"] = f"{power_match.group(1)} {power_match.group(2)}"

    return specs if specs else {"Status": "No standard specifications detected"}


# 3. Vision & Extraction Pipeline
def process_pipeline(input_image):
    if input_image is None:
        return None, "No image uploaded.", {}

    # Convert PIL Image to OpenCV array (BGR)
    img_np = np.array(input_image.convert('RGB'))
    img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    # Inference on CPU
    results = READER.readtext(img_np)

    extracted_lines = []
    for (bbox, text, confidence) in results:
        extracted_lines.append(text)
        if confidence > 0.2:
            pts = np.array(bbox, np.int32).reshape((-1, 1, 2))
            cv2.polylines(img_cv, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

    # Convert back to RGB for Gradio display
    annotated_img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    
    full_text = " ".join(extracted_lines)
    specs = extract_specifications(full_text)

    return annotated_img, full_text, specs


# 4. Gradio Web Interface
with gr.Blocks(title="Visual Spec Extractor") as demo:
    gr.Markdown("# 🔍 Visual Spec Extractor (CPU Version)")
    gr.Markdown("Extract structured product specifications (weight, dimensions, ratings) from packaging images using **EasyOCR + Regex Parsing**.")

    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type="pil", label="Upload Product / Packaging Image")
            submit_btn = gr.Button("Extract Specifications", variant="primary")

        with gr.Column():
            annotated_output = gr.Image(type="numpy", label="Detected Text Regions (Bounding Boxes)")

    with gr.Row():
        with gr.Column():
            specs_output = gr.JSON(label="Structured Specifications (Extracted JSON)")
        with gr.Column():
            raw_text_output = gr.Textbox(label="Raw Detected OCR Text", lines=8)

    submit_btn.click(
        fn=process_pipeline,
        inputs=image_input,
        outputs=[annotated_output, raw_text_output, specs_output]
    )

# 5. Launch app with clickable public link
if __name__ == "__main__":
    demo.launch(share=True)