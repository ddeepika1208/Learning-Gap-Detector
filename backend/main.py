import json
from pathlib import Path
from fastapi import FastAPI

app = FastAPI()

DATA_DIR = Path(__file__).parent / "data"

def load_json(filename):
    with open(DATA_DIR / filename, encoding="utf-8") as f:
        return json.load(f)

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/concepts")
def get_concepts():
    return load_json("concepts.json")