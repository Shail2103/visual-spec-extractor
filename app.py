import streamlit as st
import requests
import base64
import json
import pandas as pd
from io import BytesIO

# --- Page Configuration ---
st.set_page_config(
    page_title="Visual Spec Extractor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling (Modern Dark Tech Theme) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Gradient Header */
    .hero-title {
        font-size: 2.4rem;
        font-weight: 700;
        background: linear-gradient(120deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    /* Card Panels */
    .metric-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.75rem;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .metric-card:hover {
        border-color: #38bdf8;
        transform: translateY(-2px);
    }
    .metric-label {
        color: #94a3b8;
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        color: #f8fafc;
        font-size: 1.25rem;
        font-weight: 700;
        margin-top: 0.2rem;
    }

    /* Keywords Tag Cloud */
    .tag-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        padding: 0.5rem 0;
    }
    .tag-chip {
        background-color: #0f172a;
        color: #38bdf8;
        border: 1px solid #1e293b;
        padding: 0.25rem 0.65rem;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Custom File Uploader & Status styling */
    div[data-testid="stFileUploadDropzone"] {
        border: 2px dashed #38bdf855 !important;
        background-color: #0f172a44 !important;
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)


# --- Helper: Convert Base64 data URL to bytes for display ---
def decode_base64_image(data_url: str) -> bytes:
    if "," in data_url:
        data_url = data_url.split(",")[1]
    return base64.b64decode(data_url)


# --- Sidebar: Configuration & Controls ---
with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")
    backend_url = st.text_input(
        "FastAPI Endpoint",
        value="http://127.0.0.1:8000/extract",
        help="Make sure backend.py is running via uvicorn."
    )
    
    st.markdown("---")
    st.markdown("### 💡 Guidance")
    st.info(
        "Upload packaging images, rating plates, or hardware labels containing clear "
        "electrical or physical ratings (Voltage, Power, Weight, Model, etc.)."
    )
    
    st.markdown("---")
    st.caption("Engine: **EasyOCR + FastAPI**")


# --- Main Dashboard Header ---
st.markdown('<div class="hero-title">Visual Spec Extractor</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">High-precision OCR entity extraction for electrical ratings and hardware specifications</div>', unsafe_allow_html=True)

# --- Upload & Action Area ---
upload_col, preview_col = st.columns([1.2, 1.8], gap="large")

with upload_col:
    uploaded_file = st.file_uploader(
        "Upload Hardware Label / Spec Sheet",
        type=["jpg", "jpeg", "png", "webp"],
        help="Supports JPG, PNG, WEBP files"
    )

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Source Input", use_container_width=True)
        analyze_btn = st.button("⚡ Extract Specifications", use_container_width=True, type="primary")
    else:
        analyze_btn = False

# --- Processing & Results Display ---
with preview_col:
    if uploaded_file is None:
        st.markdown(
            """
            <div style="border: 1px dashed #334155; border-radius: 12px; padding: 3rem 1.5rem; text-align: center; color: #64748b;">
                <p style="font-size: 1.1rem; margin: 0;">Upload an image from the left panel to run extraction.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    elif analyze_btn:
        with st.spinner("Analyzing image contours & parsing technical tokens..."):
            try:
                # Prepare payload
                files = {
                    "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
                }
                response = requests.post(backend_url, files=files, timeout=45)

                if response.status_code == 200:
                    data = response.json()
                    st.session_state["extraction_results"] = data
                    st.success("Extraction completed successfully!")
                else:
                    st.error(f"Backend returned error {response.status_code}: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error(f"Could not connect to FastAPI server at `{backend_url}`. Ensure `uvicorn backend:app --reload` is running.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")

    # Display results if available in session
    if "extraction_results" in st.session_state and uploaded_file is not None:
        res = st.session_state["extraction_results"]
        specs = res.get("specifications", {})
        keywords = res.get("meaningful_keywords", [])
        annotated_b64 = res.get("annotated_image")

        tab_specs, tab_annotated, tab_tokens = st.tabs(["📊 Extracted Metrics", "🎯 Annotated Detections", "🏷️ Filtered Tokens"])

        with tab_specs:
            if specs:
                st.markdown("#### Structured Entity Attributes")
                spec_cols = st.columns(2)
                for idx, (label, val) in enumerate(specs.items()):
                    col = spec_cols[idx % 2]
                    col.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-label">{label}</div>
                            <div class="metric-value">{val}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # Export section
                st.markdown("---")
                dl_col1, dl_col2 = st.columns(2)
                with dl_col1:
                    specs_json = json.dumps(specs, indent=2)
                    st.download_button(
                        label="⬇️ Download JSON",
                        data=specs_json,
                        file_name="extracted_specs.json",
                        mime="application/json",
                        use_container_width=True
                    )
                with dl_col2:
                    df = pd.DataFrame(list(specs.items()), columns=["Specification", "Value"])
                    st.download_button(
                        label="⬇️ Download CSV",
                        data=df.to_csv(index=False),
                        file_name="extracted_specs.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            else:
                st.warning("No structured parameters matched regex criteria. Check the detected tokens tab for raw words.")

        with tab_annotated:
            if annotated_b64:
                annotated_bytes = decode_base64_image(annotated_b64)
                st.image(annotated_bytes, caption="Active Text Region Bounding Boxes", use_container_width=True)

        with tab_tokens:
            st.markdown(f"**Identified Non-Stopword Tokens ({len(keywords)})**")
            if keywords:
                chips_html = "".join([f'<span class="tag-chip">{word}</span>' for word in keywords])
                st.markdown(f'<div class="tag-container">{chips_html}</div>', unsafe_allow_html=True)
            else:
                st.info("No tokens met the noise reduction threshold.")