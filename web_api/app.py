from flask import Flask, jsonify, request
import yaml
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
THRESH_FILE = CONFIG_DIR / "thresholds.yaml"

def load_thresholds():
    with open(THRESH_FILE) as f:
        return yaml.safe_load(f)

def save_thresholds(data):
    with open(THRESH_FILE, "w") as f:
        yaml.safe_dump(data, f)

@app.route("/thresholds", methods=["GET", "POST"])
def thresholds():
    data = load_thresholds()

    if request.method == "POST":
        update = request.json
        data.update(update)
        save_thresholds(data)

    return jsonify(data)

@app.route("/mode/<mode>", methods=["POST"])
def set_mode(mode):
    data = load_thresholds()
    data["simulation_mode"] = mode
    save_thresholds(data)
    return jsonify({"mode": mode})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
