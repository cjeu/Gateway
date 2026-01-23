"""
REST API routes.

Acts as a control plane for the demo.
"""

from flask import Blueprint, request, jsonify
import yaml

api = Blueprint("api", __name__)

THRESHOLD_PATH = "../config/thresholds.yaml"

@api.route("/health")
def health():
    return {"status": "ok"}

@api.route("/mode", methods=["POST"])
def set_mode():
    mode = request.json.get("mode", "normal")
    with open(THRESHOLD_PATH) as f:
        cfg = yaml.safe_load(f)

    cfg["simulation_mode"] = mode

    with open(THRESHOLD_PATH, "w") as f:
        yaml.safe_dump(cfg, f)

    return jsonify({"mode": mode})

@api.route("/thresholds", methods=["POST"])
def set_thresholds():
    updates = request.json
    with open(THRESHOLD_PATH, "r") as f:
        cfg = yaml.safe_load(f)

    for k, v in updates.items():
        cfg[k]["max"] = v

    with open(THRESHOLD_PATH, "w") as f:
        yaml.safe_dump(cfg, f)

    return jsonify(cfg)
