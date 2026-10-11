<div align="center">

# 🔍 Visual Spec Extractor

**Autonomous Physical, Electrical, and Packaging Specification Extraction Engine**

[![Next.js](https://img.shields.io/badge/Next.js-15%2B-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css)](https://tailwindcss.com/)
[![EasyOCR](https://img.shields.io/badge/OCR-EasyOCR_(CPU)-blue?style=for-the-badge)](https://github.com/JaidedAI/EasyOCR)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald?style=for-the-badge)](LICENSE)

<p align="center">
  A streamlined web application that leverages <b>EasyOCR</b> and <b>rule-based NLP heuristics</b> to extract technical specifications, physical metrics, and anchor metadata directly from product packaging and spec plates—with zero GPU dependency.
</p>

</div>

---

## ⚡ Overview

Parsing text from raw packaging photos often results in garbled noise, broken layout fragments, and useless stopwords. **Visual Spec Extractor** addresses this with a two-tier extraction pipeline:

1. **Computer Vision & OCR Layer:** Scans raw product labels, bounding key text regions and filtering out low-confidence optical artifacts.
2. **Context-Aware Rule Extraction:** Uses regex unit mapping and packaging keyword anchors (`Model`, `Batch No`, `Expiry`, `Voltage`, `Weight`, `Dimensions`) to transform unorganized text into clean design tokens and structured JSON.

---

## ✨ Features

- 🖥️ **CPU-Optimized Inference:** Runs fully on local CPU without CUDA drivers or special wheel setups.
- 🎯 **Autonomous Noise Filtration:** Strips out conversational English stopwords and gibberish symbols while isolating meaningful technical tokens.
- 📐 **Comprehensive Metric Parsing:**
  - **Weight & Mass:** `kg`, `g`, `mg`, `oz`, `lbs`
  - **Volume & Liquids:** `ml`, `l`, `fl oz`
  - **Dimensions:** multi-axis physical profiles (e.g., `10x20x5 cm`, `120 x 80 mm`)
  - **Electrical Ratings:** `V`, `VAC/VDC`, `Hz`, `W`, `kW`, `A`, `mA`
  - **Metadata Anchors:** Model numbers, Batch/Lot codes, Manufacturing and Expiry dates.
- 🎨 **Watermelon / shadcn Inspired Interface:** Dark-mode bento grid layout featuring live bounding-box visualization and one-click JSON clipboard export.

---

## 🏗️ Architecture

```
┌────────────────────────────────────────┐
│      Next.js Frontend (React / TS)     │
│  - Image Upload & Dropzone             │
│  - Annotated Bounding Box Visualizer   │
│  - Bento Spec Cards & JSON View        │
└──────────────────┬─────────────────────┘
                   │ POST /extract
                   ▼
┌────────────────────────────────────────┐
│       FastAPI Backend (Python)         │
│  - EasyOCR Inference (CPU)             │
│  - Confidence Gating & NLTK Cleaning   │
│  - Regex Physical Unit Extractor       │
└────────────────────────────────────────┘
```

---

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

## 📦 Docker Deployment (Hugging Face Spaces)

This project contains a multi-stage `Dockerfile` ready for deployment to Docker-based platforms like **Hugging Face Spaces**:

```bash
# Build the unified container
docker build -t visual-spec-extractor .

# Run the container locally on port 7860
docker run -p 7860:7860 visual-spec-extractor
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