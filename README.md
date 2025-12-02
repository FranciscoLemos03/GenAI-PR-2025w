# GenAI-PR-2025w

## 📋 Project Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for version control)

### Step 1: Clone or Download the Repository
```bash
git clone <repository-URL>
cd GenAI-PR-2025w
```

### Step 2: Create a Virtual Environment (Recommended)
```bash
# On Windows (PowerShell)
python -m venv venv
.\venv\Scripts\activate.bat

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Frontend Dependencies (Streamlit)
```bash
cd frontend
pip install -r requirements.txt
```

### Step 4: Run the Streamlit Application
```bash
streamlit run app.py
```

The application will automatically open in your browser at `http://localhost:8501`

### Step 5: Deactivate the Virtual Environment (When Done)
```bash
deactivate
```

## 📁 Project Structure
```
GenAI-PR-2025w/
├── README.md
├── .gitignore
└── frontend/
    ├── app.py                  # Main Streamlit application entry point
    ├── requirements.txt        # Project dependencies
    ├── images/                 # Image assets
    │   ├── Illustration.png
    │   └── logo.png
    ├── pages/                  # Streamlit pages
    │   └── homepage.py         # Homepage/landing page
    └── components/             # Reusable components
        └── button.py           # Custom button component
```

## 📝 Notes
- Make sure Python is installed: `python --version`
- To add more packages: `pip install <package-name>`
- To save updated dependencies: `pip freeze > frontend/requirements.txt`