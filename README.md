<div align="center">

# 🔍 Visual Spec Extractor

**Autonomous Physical, Electrical, and Packaging Specification Extraction Engine**

[![Next.js](https://img.shields.io/badge/Next.js-16%2B-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS_v4-38B2AC?style=for-the-badge&logo=tailwind-css)](https://tailwindcss.com/)
[![EasyOCR](https://img.shields.io/badge/OCR-EasyOCR_(CPU)-blue?style=for-the-badge)](https://github.com/JaidedAI/EasyOCR)
[![Render](https://img.shields.io/badge/Deployed_on-Render-46E3B7?style=for-the-badge&logo=render)](https://render.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald?style=for-the-badge)](LICENSE)

<p align="center">
  A full-stack computer vision web application that leverages <b>EasyOCR</b> and <b>context-aware NLP heuristics</b> to extract technical specifications, physical metrics, and anchor metadata directly from packaging labels and specification plates—with zero GPU dependency.
</p>

[🌐 Live Demo on Render](https://your-service-name.onrender.com) · [Report Bug](https://github.com/YOUR_USERNAME/visual-spec-extractor/issues) · [Request Feature](https://github.com/YOUR_USERNAME/visual-spec-extractor/issues)

</div>

---

## ⚡ Overview

Extracting structured data from raw product packaging photos often results in garbled optical noise, broken layout fragments, and conversational stopwords. **Visual Spec Extractor** addresses this challenge with a dual-tier processing pipeline:

1. **Computer Vision & OCR Layer:** Scans raw product packaging, identifies and marks text regions with bounding boxes, and filters out low-confidence optical artifacts.
2. **Context-Aware NLP Filtering:** Strips conversational English stopwords and applies regex unit mapping with packaging keyword anchors (`Model`, `Batch No`, `Expiry`, `Voltage`, `Weight`, `Dimensions`) to transform unorganized text into clean design tokens and structured JSON.

---

## ✨ Features

- 🖥️ **CPU-Optimized Inference:** Runs entirely on standard CPU instances without requiring CUDA drivers or external GPU dependencies.
- 🎯 **Autonomous Noise Filtration:** Strips conversational stopwords and garbled artifacts while isolating meaningful technical tokens.
- 📐 **Comprehensive Metric Parsing:**
  - **Weight & Mass:** `kg`, `g`, `mg`, `oz`, `lbs`
  - **Volume & Liquids:** `ml`, `l`, `fl oz`
  - **Dimensions:** Multi-axis profiles (e.g., `10x20x5 cm`, `120 x 80 mm`)
  - **Electrical Ratings:** `V`, `VAC/VDC`, `Hz`, `W`, `kW`, `A`, `mA`
  - **Metadata Anchors:** Model numbers, Batch/Lot codes, Manufacturing and Expiry dates.
- 🎨 **Watermelon / shadcn-Style Interface:** Modern dark-mode bento grid layout featuring live bounding-box visualization, token tags, and one-click JSON clipboard export.

---

## 🏗️ Architecture

```text
┌────────────────────────────────────────┐
│      Next.js Frontend (React / TS)     │
│  - Image Upload & Dropzone             │
│  - Annotated Bounding Box Visualizer   │
│  - Bento Spec Cards & JSON View        │
└──────────────────┬─────────────────────┘
                   │ POST /extract
                   ▼
┌────────────────────────────────────────┐
│        FastAPI Backend (Python)        │
│  - EasyOCR Inference (CPU)             │
│  - Confidence Gating & NLTK Cleaning   │
│  - Regex Physical Unit Extractor       │
└────────────────────────────────────────┘


## 🚀 Quick Start (Local Setup)

### Prerequisites

- **Python 3.10+**
- **Node.js 18+**

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/visual-spec-extractor.git
cd visual-spec-extractor
```

### 2. Run the Backend

```bash
# Navigate to backend and install requirements
pip install fastapi uvicorn python-multipart easyocr opencv-python pillow numpy nltk

# Start the FastAPI server
uvicorn backend:app --reload --port 8000
```
*API docs will be available at `http://127.0.0.1:8000/docs`.*

### 3. Run the Frontend

Open a second terminal window:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to interact with the application.

---

## 📦 Docker Deployment (Render)

This project includes a multi-stage `Dockerfile` configured to build both the Next.js frontend and FastAPI backend into a single container for hosting on **Render**:

### Local Docker Test

To test the production container locally using the same configuration:

```bash
# Build the unified container
docker build -t visual-spec-extractor .

# Run container on port 7860
docker run -p 7860:7860 -e PORT=7860 visual-spec-extractor

```

---

## 📂 Project Structure

```text
visual-spec-extractor/
├── backend.py              # FastAPI server & EasyOCR rule engine
├── requirements.txt        # Python backend dependencies
├── Dockerfile              # Container configuration for cloud hosting
├── README.md               # Project documentation
└── frontend/               # Next.js frontend application
    ├── src/
    │   └── app/
    │       ├── layout.tsx  # Global layout & metadata
    │       ├── globals.css # Tailwind theme styling
    │       └── page.tsx    # Interactive extractor dashboard
    ├── package.json
    └── tsconfig.json
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to open an issue or submit a pull request.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
