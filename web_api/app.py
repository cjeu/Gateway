"""
Flask entry point for edge gateway control API.

Used to:
- Query latest values
- Change simulation mode
- Update thresholds
"""

from flask import Flask
from routes import api
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR=BASE_DIR/"config"

    
with open(CONFIG_DIR / "thresholds.yaml","r") as f: 
    thresholds = yaml.safe_load(f)


app = Flask(__name__)
app.register_blueprint(api)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
