# start.ps1 (repo root)

$ErrorActionPreference = "Stop"

# 1) Venv (ha nincs)
if (-not (Test-Path ".\.venv")) {
  python -m venv .venv
}

# 2) Pip upgrade + deps
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\pip.exe install -r requirements.txt

# 3) Backend (FastAPI)
Start-Process powershell -ArgumentList "-NoExit", "-Command", ".\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000"

# 4) Frontend (Streamlit)
Start-Process powershell -ArgumentList "-NoExit", "-Command", ".\.venv\Scripts\python.exe -m streamlit run frontend\app.py --server.port 8501"

# 5) Worker (automation) - opcionális, de beadandóhoz kell
Start-Process powershell -ArgumentList "-NoExit", "-Command", ".\.venv\Scripts\python.exe scripts\worker.py"

Write-Host "Indítva: backend (8000), frontend (8501), worker."
