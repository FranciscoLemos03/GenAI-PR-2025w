# GenAI FastAPI Backend

This repository contains the backend API for a GenAI-powered research platform.
The API is built with **FastAPI (Python)** and is responsible for handling
authentication, data processing, and (later) GenAI workflows such as document
analysis and retrieval.

At this stage, the project provides a clean and extensible **API skeleton**
that receives:
- A Firebase Authentication token
- A research theme/topic provided by the user

---

## 🧱 Project Structure

genai-api/
├── app/
│ ├── main.py
│ ├── api/
│ │ └── routes.py
│ ├── models/
│ │ └── schemas.py
│ └── core/
│ └── config.py
├── requirements.txt
├── .env
└── .gitignore

---

## 📂 Folder & File Explanation

### `app/`
Main application package.

#### `app/main.py`
- Application entry point.
- Creates the FastAPI instance.
- Configures CORS (to allow requests from the React frontend).
- Registers API routes.
- Exposes a `/health` endpoint for basic health checks.

---

### `app/api/routes.py`
- Defines API endpoints.
- Currently exposes:
  - `POST /api/generate`
- Receives:
  - `Authorization` header (Firebase ID Token)
  - Request body containing the `theme`
- This file will later orchestrate:
  - Authentication
  - Data retrieval
  - GenAI pipelines (RAG, summarization, etc.)

---

### `app/models/schemas.py`
- Contains **Pydantic models** for request and response validation.
- Ensures type safety and clear API contracts.
- Example:
  - `GenerateRequest`
  - `GenerateResponse`

---

### `app/core/config.py`
- Reserved for configuration logic.
- Will later include:
  - Environment variables
  - Firebase configuration
  - Model / GenAI settings

---

### `requirements.txt`
- Lists all Python dependencies required to run the API.

---

### `.env`
- Optional file for environment variables.
- Not committed to version control.
- Will later store secrets such as:
  - Firebase credentials path
  - API keys
  - Environment flags

---

### `.gitignore`
- Prevents sensitive or unnecessary files from being committed.

---

## 🚀 Running the API Locally

### 1. Create and activate a virtual environment
```bash
python -m venv venv

source venv/bin/activate   # macOS / Linux
venv\Scripts\activate    # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the development server

```bash
uvicorn app.main:app --reload
```

