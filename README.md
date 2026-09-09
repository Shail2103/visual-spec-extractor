# SpecLens: Automated Product Specification Extractor

An end-to-end computer vision and NLP pipeline that extracts structured product attributes (weight, volume, dimensions, voltage, and power ratings) from packaging images and spec sheets.

## Architecture & Pipeline
1. **Visual Text Detection (OCR):** Uses EasyOCR to localize and extract text coordinates and bounding boxes from raw packaging images.
2. **Entity & Unit Extraction:** Scans raw text through deterministic regex patterns to capture numerical values linked to standardized physical and electrical units.
3. **Structured Normalization:** Outputs clean, catalog-ready JSON data and overlays bounding boxes onto the source image.
4. **Interface:** Deployed via Gradio for interactive testing.

## Tech Stack
* **Language:** Python
* **OCR & Vision:** EasyOCR, OpenCV, Pillow
* **Interface & Deployment:** Gradio
