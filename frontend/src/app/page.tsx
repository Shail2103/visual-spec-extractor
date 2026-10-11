// frontend/src/app/page.tsx
"use client";

import React, { useState } from "react";
import { UploadCloud, CheckCircle2, Cpu, Copy, ArrowRight, Loader2, Sparkles, Tag } from "lucide-react";

interface ExtractionResult {
  annotated_image: string;
  meaningful_keywords: string[];
  specifications: Record<string, string>;
}

export default function SpecExtractorApp() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ExtractionResult | null>(null);
  const [copied, setCopied] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selected = e.target.files[0];
      setFile(selected);
      setPreviewUrl(URL.createObjectURL(selected));
      setResult(null);
    }
  };

  const handleExtract = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/extract", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error("Failed extraction");
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      alert("Error: Cannot connect to FastAPI backend. Ensure uvicorn is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  const copyJSON = () => {
    if (!result) return;
    navigator.clipboard.writeText(JSON.stringify(result.specifications, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 selection:bg-emerald-500/30 font-sans">
      {/* Background Ambient Glow (Watermelon UI theme) */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 left-1/2 -translate-x-1/2 w-[700px] h-[350px] bg-emerald-500/10 blur-[130px] rounded-full" />
      </div>

      <main className="relative max-w-6xl mx-auto px-6 py-12">
        {/* Top Header */}
        <header className="text-center space-y-3 mb-12">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-emerald-500/30 bg-emerald-500/10 text-emerald-400 text-xs font-medium tracking-wide">
            <Sparkles className="w-3.5 h-3.5" /> EasyOCR + Regex Tokenizer Engine
          </div>
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-white">
            Visual Spec <span className="text-emerald-400">Extractor</span>
          </h1>
          <p className="text-slate-400 text-sm md:text-base max-w-xl mx-auto">
            Extract product dimensions, weight, ratings, and voltage directly from packaging labels into structured design tokens and JSON.
          </p>
        </header>

        {/* 2-Column Responsive Workspace */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* Left Column: Upload Dropzone */}
          <section className="lg:col-span-5 space-y-4">
            <div className="border border-slate-800 bg-slate-900/60 backdrop-blur-xl rounded-2xl p-6 shadow-xl relative group">
              <label className="flex flex-col items-center justify-center border-2 border-dashed border-slate-700 hover:border-emerald-500/60 rounded-xl p-8 cursor-pointer transition-all duration-200 bg-slate-950/40">
                <UploadCloud className="w-10 h-10 text-slate-400 group-hover:text-emerald-400 transition-colors mb-3" />
                <span className="text-sm font-semibold text-slate-200">
                  {file ? file.name : "Upload packaging image"}
                </span>
                <span className="text-xs text-slate-500 mt-1">PNG, JPG, or WEBP</span>
                <input type="file" accept="image/*" className="hidden" onChange={handleFileChange} />
              </label>

              {previewUrl && (
                <div className="mt-4 rounded-lg overflow-hidden border border-slate-800">
                  <img src={previewUrl} alt="Preview" className="w-full max-h-56 object-cover" />
                </div>
              )}

              <button
                onClick={handleExtract}
                disabled={!file || loading}
                className="w-full mt-4 flex items-center justify-center gap-2 py-3 px-4 rounded-xl font-medium text-sm text-slate-950 bg-emerald-400 hover:bg-emerald-300 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" /> Processing OCR on CPU...
                  </>
                ) : (
                  <>
                    Extract Specifications <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </div>
          </section>

          {/* Right Column: Extracted Results */}
          <section className="lg:col-span-7 space-y-6">
            {!result ? (
              <div className="border border-slate-800/80 bg-slate-900/40 backdrop-blur-md rounded-2xl p-12 text-center text-slate-500">
                <Cpu className="w-10 h-10 mx-auto mb-3 opacity-40" />
                <p className="text-sm">Upload an image and click extract to see detected regions and structured specs.</p>
              </div>
            ) : (
              <div className="space-y-6">
                {/* Visual Bounding Boxes */}
                <div className="border border-slate-800 bg-slate-900/60 rounded-2xl p-5 shadow-xl">
                  <h3 className="text-sm font-semibold text-slate-300 mb-3 flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" /> Detected Text Regions
                  </h3>
                  <div className="rounded-xl overflow-hidden border border-slate-800 bg-black/40">
                    <img src={result.annotated_image} alt="Annotated OCR" className="w-full object-contain max-h-80" />
                  </div>
                </div>

                {/* Bento Grid: Extracted Specs */}
                <div>
                  <h3 className="text-sm font-semibold text-slate-300 mb-3">Structured Specifications</h3>
                  {Object.keys(result.specifications).length === 0 ? (
                    <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/40 text-xs text-slate-400">
                      No standard unit specifications matched (Dimensions, Weight, Voltage, etc.).
                    </div>
                  ) : (
                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                      {Object.entries(result.specifications).map(([key, value]) => (
                        <div key={key} className="p-4 rounded-xl border border-slate-800 bg-slate-900/80 shadow-md">
                          <span className="text-xs font-medium text-slate-400 block">{key}</span>
                          <span className="text-base font-semibold text-emerald-300 mt-1 block truncate">
                            {value}
                          </span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {/* Filtered Meaningful Words Tag Cloud */}
                {result.meaningful_keywords && result.meaningful_keywords.length > 0 && (
                  <div className="border border-slate-800 bg-slate-900/60 rounded-2xl p-5 shadow-xl">
                    <h3 className="text-sm font-semibold text-slate-300 mb-3 flex items-center gap-2">
                      <Tag className="w-4 h-4 text-emerald-400" /> Filtered Meaningful Tokens
                    </h3>
                    <div className="flex flex-wrap gap-2 max-h-36 overflow-y-auto pr-1">
                      {result.meaningful_keywords.map((word, idx) => (
                        <span
                          key={idx}
                          className="px-2.5 py-1 text-xs font-mono rounded-lg border border-slate-700 bg-slate-800/80 text-emerald-300"
                        >
                          {word}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* JSON Code Viewer */}
                <div className="border border-slate-800 bg-slate-900/60 rounded-2xl p-5 shadow-xl">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-sm font-semibold text-slate-300">Raw JSON Output</h3>
                    <button
                      onClick={copyJSON}
                      className="text-xs inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md border border-slate-700 bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
                    >
                      <Copy className="w-3 h-3" /> {copied ? "Copied!" : "Copy JSON"}
                    </button>
                  </div>
                  <pre className="p-3 bg-slate-950 rounded-xl border border-slate-800/80 text-xs font-mono text-emerald-400 overflow-x-auto max-h-48">
                    {JSON.stringify(result.specifications, null, 2)}
                  </pre>
                </div>
              </div>
            )}
          </section>

        </div>
      </main>
    </div>
  );
}