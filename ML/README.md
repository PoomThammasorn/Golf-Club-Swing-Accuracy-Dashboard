# FastAPI Application

This is a simple FastAPI application that returns a "Hello World" message. It loads environment variables from a `.env` file, allowing you to configure the port on which the application runs.

## Prerequisites

- Python 3.9.6 or higher
- pip

## Setup

1. **Clone the repository** (if applicable):

   ```bash
   git clone https://github.com/PoomThammasorn/Golf-Club-Swing-Accuracy-Dashboard.git

   cd Golf-Club-Swing-Accuracy-Dashboard/ML
   ```

2. **Create virtual environment**:

   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**:

   - Windows:
     ```cmd
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Run

```bash
python main.py
```

## After install additonal packages

```bash
pip freeze > requirements.txt
```
