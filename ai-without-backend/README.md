# Backend - AI Research Paper Retrieval System

A Python-based backend system for managing, processing, and retrieving research papers using semantic similarity search and embeddings.

## Overview

This backend implements a document retrieval system that:
- **Ingests PDFs** and extracts their content
- **Generates embeddings** using state-of-the-art language models
- **Stores document metadata** in a JSON database
- **Performs semantic search** using cosine similarity
- **Integrates with AI APIs** (Google Gemini/Gemma) for advanced processing

## Project Structure

```
backend/
├── main.py                    # Entry point - initializes PDFs and runs the main program
├── data_manager.py            # Handles PDF upload, processing, and database management
├── baseline_retriever.py      # Implements semantic search functionality
├── embedder.py                # Manages text embeddings using sentence transformers
├── requirements.txt           # Python dependencies
├── data/                      # Data storage
│   ├── pdfs/                  # Uploaded PDF files
│   ├── database.json          # Metadata for all documents
│   ├── llm_database.json      # LLM-processed content cache
│   └── llm_metadata_cache.json# Cached metadata
├── example_pdfs_to_upload/    # Sample PDFs for initialization
└── experiments/               # Research notebooks and evaluation scripts
    ├── experiment_1_chunking.ipynb
    ├── experiment_2_metadata.ipynb
    ├── experiment_3_metadata_chunks.ipynb
    ├── experiment_4_threshold.ipynb
    └── evaluation_queries.py
```

## Core Components

### 1. **Embedder** (`embedder.py`)
Generates semantic embeddings for text content.

**Key Features:**
- Uses `BAAI/bge-small-en-v1.5` model (superior to MiniLM for semantic accuracy)
- Supports up to 512 tokens per text
- L2-normalized embeddings enable fast cosine similarity computation
- CPU/GPU compatible

**Usage:**
```python
from embedder import Embedder

embedder = Embedder()
embedding = embedder.encode("Your text here")
```

### 2. **Data Manager** (`data_manager.py`)
Handles PDF management and metadata storage.

**Key Features:**
- Extract text from PDFs using PyMuPDF
- Parse PDF content by chapters and pages
- Store documents with metadata (title, researcher, date)
- Integration with Google Gemini/Gemma APIs for content processing
- JSON-based database storage
- Automatic directory creation

**Methods:**
- `upload_pdf()` - Process and store a new PDF
- `search_in_database()` - Find documents by criteria
- `get_document()` - Retrieve document by ID

### 3. **Baseline Retriever** (`baseline_retriever.py`)
Implements semantic search over the document database.

**Key Features:**
- Loads documents from database
- Computes cosine similarity between query and document embeddings
- Configurable similarity threshold (default: 0.45)
- Supports weighted ranking with alpha parameter

**Methods:**
- `search(query, threshold=0.45, alpha=0.5)` - Search with semantic similarity
- `cosine_similarity()` - Compute similarity between two embeddings
- `load_database()` - Load all documents

### 4. **Main** (`main.py`)
Orchestrates the entire pipeline. You can directly run this file in order to see the implementation without the web application.

**Workflow:**
1. Loads up to 20 example PDFs from `example_pdfs_to_upload/`
2. Extracts metadata from filenames (format: `YYYY-MM-DD_Researcher_Title`)
3. Processes PDFs through DataManager
4. Stores results in database
5. Skips already-processed PDFs automatically

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone/Navigate to the project:**
```bash
cd backend
```

2. **Create virtual environment (optional but recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
Create a `.env` file in the backend directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMMA_API_KEY=your_gemma_api_key_here
```

## Dependencies

| Package | Purpose |
|---------|---------|
| `sentence-transformers` | Text embedding generation |
| `torch` | Deep learning framework (required by sentence-transformers) |
| `numpy` | Numerical computations |
| `pymupdf` (fitz) | PDF text extraction |
| `requests` | HTTP requests for APIs |
| `arxiv` | arXiv paper metadata retrieval |
| `python-dotenv` | Environment variable management |

## Usage

### Running the System

```bash
python main.py
```

This will:
1. Check for PDFs in `example_pdfs_to_upload/`
2. Process and add them to the database
3. Generate embeddings for all documents
4. Store metadata in `data/database.json`

### Performing a Search

```python
from baseline_retriever import BaselineRetriever

retriever = BaselineRetriever()
results = retriever.search("quantum computing applications", threshold=0.45)

for result in results:
    print(f"Title: {result['title']}")
    print(f"Similarity: {result['similarity']:.3f}")
    print(f"Researcher: {result['researcher']}")
```

### Adding Custom PDFs

```python
from data_manager import DataManager

dm = DataManager()
dm.upload_pdf(
    file_path="path/to/paper.pdf",
    title="Custom Paper Title",
    day="2024-01-15",
    researcher="Author Name"
)
```

## Data Format

### Database Structure (`data/database.json`)
```json
[
  {
    "id": "uuid-string",
    "title": "Paper Title",
    "researcher": "Author Name",
    "day": "2024-01-15",
    "pdf_name": "2024-01-15_AuthorName_Title.pdf",
    "chapters": [
      {
        "chapter_num": 1,
        "content": "Chapter text...",
        "embedding": [0.1, 0.2, ...],
        "pages": [1, 2, 3]
      }
    ]
  }
]
```

## Configuration

### Embedding Model
Change the model in `embedder.py`:
```python
Embedder(model_name="your-model-name", device="cuda")  # Use "cuda" for GPU
```

### Search Parameters
Adjust in retrieval calls:
- `threshold` (0.0-1.0): Minimum similarity score
- `alpha`: Weighting factor for ranking

## Experiments

The `experiments/` folder contains research notebooks:
- **experiment_1_chunking.ipynb** - Tests different text chunking strategies
- **experiment_2_metadata.ipynb** - Evaluates metadata impact
- **experiment_3_metadata_chunks.ipynb** - Combined chunking and metadata analysis
- **experiment_4_threshold.ipynb** - Threshold optimization
- **evaluation_queries.py** - Benchmark query evaluation

## API Integration

The backend supports integration with:
- **Google Gemini** - Advanced LLM processing
- **Google Gemma** - Lightweight LLM alternative

Configure API keys in `.env` file for automatic content processing.

## Performance Notes

- **Embedding Generation**: ~50-100ms per document using BGE-small
- **Search Query**: <1ms per document in database
- **Memory**: ~500MB for 1000 documents with embeddings
- **Database Size**: Scales linearly with PDF count

## Troubleshooting

| Issue | Solution |
|-------|----------|
| PDF extraction fails | Ensure PDF is not encrypted; check PyMuPDF compatibility |
| Embedding import error | Run `pip install sentence-transformers torch` |
| API key errors | Verify `.env` file exists and contains valid keys |
| Memory issues | Reduce document count or use GPU (`device="cuda"`) |

## Future Enhancements

- [ ] PostgreSQL/MongoDB integration for scalability
- [ ] Batch processing for large document sets
- [ ] Advanced filtering and faceted search
- [ ] Document versioning and updates
- [ ] Multi-language support
- [ ] Custom embedding fine-tuning

## License

This project is part of the GenAI course at TU Wien.


