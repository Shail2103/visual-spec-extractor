<div align="center">

# 🔍 Visual Spec Extractor

**Autonomous Physical, Electrical, and Packaging Specification Extraction Engine**

[![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
[![EasyOCR](https://img.shields.io/badge/OCR-EasyOCR_(CPU)-blue?style=for-the-badge)](https://github.com/JaidedAI/EasyOCR)
[![OpenCV](https://img.shields.io/badge/OpenCV-Headless-5C3EE8?style=for-the-badge&logo=opencv)](https://opencv.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald?style=for-the-badge)](LICENSE)

<p align="center">
  A full-stack computer vision application powered by <b>EasyOCR</b>, <b>OpenCV</b>, and <b>context-aware NLP heuristics</b> to extract technical specifications, physical ratings, and metadata anchors directly from product packaging and rating plates—featuring a modern <b>Streamlit</b> interface with zero GPU dependency.
</p>

<!-- Live Application Launch Banner -->
<p align="center">
  <a href="https://visual-spec-extractor.streamlit.app" target="_blank">
    <img src="https://img.shields.io/badge/🚀_Launch_Live_App-Streamlit_Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Launch Live App" />
  </a>
</p>

[🌐 Live Demo](https://visual-spec-extractor.streamlit.app) · [Report Bug](https://github.com/YOUR_USERNAME/visual-spec-extractor/issues) · [Request Feature](https://github.com/YOUR_USERNAME/visual-spec-extractor/issues)

</div>

---

## 🚀 Live Demo

Try the live application directly in your browser:

> **Web Application:** [https://visual-spec-extractor.streamlit.app](https://your-app-name.streamlit.app)  
> *Upload any sample packaging label or specification sheet to preview live text detection, bounding box visualization, and structured entity extraction.*

---

</div>

---

## ⚡ Overview

Extracting structured engineering data from real-world product packaging images usually introduces optical artifacts, irregular geometries, and conversational noise. **Visual Spec Extractor** handles this through a coordinated, two-tier processing pipeline:

1. **Computer Vision & OCR Layer:** Ingests raw images, localizes text regions using EasyOCR, computes confidence thresholds (filtering out detections below 0.35), and renders clean green polygon overlays on active regions via OpenCV.
2. **Context-Aware NLP & Entity Extraction:** Strips conversational English stopwords using NLTK, applies noise-ratio token filtration, and leverages targeted regex patterns to extract key specifications (`Voltage`, `Power`, `Frequency`, `Weight`, `Dimensions`, `Batch/Lot No`, `Expiry Date`) into structured JSON and tabular formats.

---

## ✨ Features

- 🖥️ **CPU-Optimized Inference:** Runs out-of-the-box on standard CPU environments without requiring CUDA drivers or GPU hardware.
- 🎯 **Confidence Gating & Noise Elimination:** Automatically purges low-confidence optical artifacts and non-alphanumeric noise tokens.
- 📐 **Comprehensive Metric Parsing:**
  - **Electrical Ratings:** Voltage (`V`, `VAC`, `VDC`), Power (`W`, `kW`), Current (`A`, `mA`), Frequency (`Hz`, `kHz`, `MHz`).
  - **Physical Dimensions:** Multi-axis profiles (e.g., `10x20x5 cm`, `120 x 80 mm`).
  - **Mass & Volume:** Weight (`kg`, `g`, `mg`, `oz`, `lbs`), Liquid Volume (`ml`, `l`, `fl oz`).
  - **Metadata Anchors:** Model / Item Number, Batch / Lot codes, Manufacturing and Expiry dates.
- 🎨 **Modern Streamlit Dashboard:** Custom dark-themed layout with responsive metric cards, interactive token tag clouds, side-by-side detection views, and one-click JSON/CSV exports.

---

## 🏗️ Architecture

```text
┌──────────────────────────────────────────────┐
│           Streamlit Frontend (app.py)        │
│  - Image Uploader & Live Preview             │
│  - Custom Styled Metric Cards & Token Cloud  │
│  - CSV / JSON Export Engine                  │
└──────────────────────┬───────────────────────┘
                       │
                       │ POST /extract (Multipart Form)
                       ▼
┌──────────────────────────────────────────────┐
│           FastAPI Backend (backend.py)       │
│  - EasyOCR Text Region Localization (CPU)    │
│  - OpenCV Polyline Bounding Box Overlays     │
│  - NLTK Stopword & Alpha-Numeric Filtering   │
│  - Regex Entity Parser & Metadata Anchors    │
└──────────────────────────────────────────────┘
