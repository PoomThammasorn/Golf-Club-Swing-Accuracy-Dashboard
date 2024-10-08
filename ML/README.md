# ML Service

## Prerequisites

- Python 3.9.6 or higher
- pip
- mqtt broker

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
uvicorn main:app --host localhost --port 9000
```

## After install additonal packages

```bash
pip freeze > requirements.txt
```
