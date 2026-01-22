# 🧠 Collaborative Research Intelligence Platform

---

## 📌 Project Overview

This project aims to build a **collaborative web platform for academic research teams**, designed to help researchers manage large collections of textual documents.

Research projects typically generate a high volume of unstructured text, such as papers, notes, annotations, and meeting documents. As this information grows, it becomes increasingly difficult to retrieve previously seen ideas or references.

To address these challenges, the platform leverages **Generative AI techniques** to support retrieval.

### ✂️ Intelligent Segmentation:

Uses the Gemma-3-276 model to perform semantic chunking based on subtopic detection rather than fixed token lengths.

### 🧾 Metadata Enrichment:

Automatically extracts authors, years, keywords, and summaries using Gemini-2.5-flash to improve search context.

### 🔍 Semantic Retrieval:

Employs a dual-embedding strategy with a score, that combines raw text and metadata for high-precision results.

### 🚀 Optimized Performance:

Features a tuned cosine similarity threshold of 0.45 to maximize retrieval accuracy while minimizing noise6.

---

## 🏗️ Project Structure

The repository is organized into three main components:

- ai-with-frontend/ (React.JS web app with firebase integration)
- ai-without-frontend/ (Python development for GenAI Functionalities)
  - experiments/ (Jupyter notebooks detailing model optimization and evaluation metrics)
- .gitignore 
- README.md
