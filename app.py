"""
app.py - MedPredict AI Backend
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Flask REST API for Disease Risk Prediction.

Production-ready features:
  ✓ Error handling & validation
  ✓ Structured logging
  ✓ CORS support
  ✓ Model caching
  ✓ Input sanitization

API Endpoints:
  POST /predict/diabetes     → Diabetes risk assessment
  POST /predict/heart        → Heart disease risk assessment
  GET  /health               → Server & model status

Usage:
  python app.py              # Development mode
  python app.py --prod       # Production mode
"""

import os
import sys
import pickle
import logging
import numpy as np
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Force UTF-8 output on Windows to avoid UnicodeEncodeError with emoji
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# ─────────────────────────────────────────────────────────────────
# LOGGING CONFIGURATION
# ─────────────────────────────────────────────────────────────────

def setup_logging():
    """Configure application logging."""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('app.log', mode='a')
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

# ─────────────────────────────────────────────────────────────────
# APPLICATION SETUP
# ─────────────────────────────────────────────────────────────────

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app, 
     resources={r"/predict/*": {"origins": "*"}, r"/health": {"origins": "*"}},
     allow_headers=['Content-Type'])

app.config['JSON_SORT_KEYS'] = False

# ─────────────────────────────────────────────────────────────────
# MODEL LOADING
# ─────────────────────────────────────────────────────────────────

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")

def load_model(name):
    """Load and cache model files."""
    path = os.path.join(MODELS_DIR, name)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Model file '{path}' not found. "
            "Run: python train_models.py"
        )
    with open(path, "rb") as f:
        return pickle.load(f)

# Load models on startup
try:
    diabetes_model = load_model("diabetes_model.pkl")
    diabetes_scaler = load_model("diabetes_scaler.pkl")
    heart_model = load_model("heart_model.pkl")
    heart_scaler = load_model("heart_scaler.pkl")
    logger.info("[OK] All models loaded successfully.")
    models_ready = True
except FileNotFoundError as e:
    logger.warning(f"[WARN] Model loading failed: {e}")
    diabetes_model = diabetes_scaler = heart_model = heart_scaler = None
    models_ready = False

# ─────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────

def risk_level(pct: float) -> dict:
    """Convert percentage to risk category."""
    if pct < 20:
        return {"level": "Very Low", "color": "#22c55e", "icon": "✅"}
    elif pct < 40:
        return {"level": "Low", "color": "#84cc16", "icon": "🟢"}
    elif pct < 60:
        return {"level": "Moderate", "color": "#f59e0b", "icon": "⚠️"}
    elif pct < 80:
        return {"level": "High", "color": "#f97316", "icon": "🔶"}
    else:
        return {"level": "Very High", "color": "#ef4444", "icon": "🚨"}


def safe_float(val, default=0.0, lo=None, hi=None):
    """Safely convert to float with bounds checking."""
    try:
        v = float(val)
        if lo is not None:
            v = max(lo, v)
        if hi is not None:
            v = min(hi, v)
        return v
    except (TypeError, ValueError):
        return default


# ─────────────────────────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve frontend."""
    return send_from_directory(".", "index.html")


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "models_ready": models_ready,
        "version": "1.0.0"
    })


@app.route("/predict/diabetes", methods=["POST"])
def predict_diabetes():
    """Predict diabetes risk."""
    if not models_ready or diabetes_model is None:
        logger.warning("Diabetes prediction attempted with models not ready")
        return jsonify({
            "error": "Models not loaded",
            "message": "Please train models: python train_models.py"
        }), 503

    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Extract and validate features
        features = np.array([[
            safe_float(data.get("pregnancies"), 0, 0, 20),
            safe_float(data.get("glucose"), 120, 44, 199),
            safe_float(data.get("bloodPressure"), 70, 24, 122),
            safe_float(data.get("skinThickness"), 23, 0, 99),
            safe_float(data.get("insulin"), 79, 0, 846),
            safe_float(data.get("bmi"), 28.0, 1, 67),
            safe_float(data.get("diabetesPedigreeFunction"), 0.47, 0.078, 2.42),
            safe_float(data.get("age"), 30, 21, 81),
        ]])

        # Make prediction
        scaled = diabetes_scaler.transform(features)
        prob = float(diabetes_model.predict_proba(scaled)[0][1])
        pct = round(prob * 100, 1)
        info = risk_level(pct)

        response = {
            "risk_percentage": pct,
            "risk_level": info["level"],
            "color": info["color"],
            "icon": info["icon"],
            "message": _diabetes_message(pct, data),
            "recommendations": _diabetes_recommendations(pct),
        }

        logger.info(f"Diabetes prediction: {pct}% ({info['level']})")
        return jsonify(response)

    except Exception as e:
        logger.error(f"Diabetes prediction error: {str(e)}")
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 400


@app.route("/predict/heart", methods=["POST"])
def predict_heart():
    """Predict heart disease risk."""
    if not models_ready or heart_model is None:
        logger.warning("Heart prediction attempted with models not ready")
        return jsonify({
            "error": "Models not loaded",
            "message": "Please train models: python train_models.py"
        }), 503

    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Extract and validate features
        features = np.array([[
            safe_float(data.get("age"), 50, 29, 77),
            safe_float(data.get("sex"), 1, 0, 1),
            safe_float(data.get("cp"), 1, 0, 3),
            safe_float(data.get("trestbps"), 130, 94, 200),
            safe_float(data.get("chol"), 246, 126, 564),
            safe_float(data.get("fbs"), 0, 0, 1),
            safe_float(data.get("restecg"), 1, 0, 2),
            safe_float(data.get("thalach"), 150, 71, 202),
            safe_float(data.get("exang"), 0, 0, 1),
            safe_float(data.get("oldpeak"), 1.0, 0, 6.2),
            safe_float(data.get("slope"), 1, 0, 2),
            safe_float(data.get("ca"), 0, 0, 3),
            safe_float(data.get("thal"), 2, 0, 3),
        ]])

        # Make prediction
        scaled = heart_scaler.transform(features)
        prob = float(heart_model.predict_proba(scaled)[0][1])
        pct = round(prob * 100, 1)
        info = risk_level(pct)

        response = {
            "risk_percentage": pct,
            "risk_level": info["level"],
            "color": info["color"],
            "icon": info["icon"],
            "message": _heart_message(pct),
            "recommendations": _heart_recommendations(pct),
        }

        logger.info(f"Heart prediction: {pct}% ({info['level']})")
        return jsonify(response)

    except Exception as e:
        logger.error(f"Heart prediction error: {str(e)}")
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 400


# ─────────────────────────────────────────────────────────────────
# MESSAGE GENERATORS
# ─────────────────────────────────────────────────────────────────

def _diabetes_message(pct, data):
    """Generate personalized diabetes message."""
    glucose = safe_float(data.get("glucose"), 120)
    bmi = safe_float(data.get("bmi"), 28)
    
    if pct >= 70:
        return (f"Your glucose level ({glucose:.0f} mg/dL) and BMI ({bmi:.1f}) "
                "indicate elevated risk. Consult a healthcare professional immediately.")
    elif pct >= 40:
        return ("Your results indicate moderate diabetes risk. "
                "Lifestyle changes and regular monitoring are recommended.")
    else:
        return ("Your diabetes risk appears low. "
                "Maintain a healthy diet and regular exercise.")


def _diabetes_recommendations(pct):
    """Generate diabetes recommendations."""
    base = [
        "Monitor blood glucose regularly",
        "Maintain a balanced, low-sugar diet",
        "Exercise at least 30 minutes daily",
    ]
    if pct >= 60:
        base += [
            "Consult an endocrinologist",
            "Consider HbA1c testing",
            "Reduce refined carbohydrate intake",
        ]
    elif pct >= 40:
        base += ["Increase physical activity", "Schedule check-up within 3 months"]
    else:
        base += ["Annual wellness check", "Stay hydrated"]
    return base


def _heart_message(pct):
    """Generate personalized heart message."""
    if pct >= 70:
        return ("Elevated cardiovascular risk detected. "
                "Please seek medical evaluation promptly.")
    elif pct >= 40:
        return ("Moderate heart disease risk identified. "
                "Discuss preventive measures with your doctor.")
    else:
        return ("Your cardiovascular risk appears low. "
                "Keep up with a heart-healthy lifestyle!")


def _heart_recommendations(pct):
    """Generate heart disease recommendations."""
    base = [
        "Monitor blood pressure regularly",
        "Maintain healthy cholesterol levels",
        "Exercise aerobically 150 min/week",
    ]
    if pct >= 60:
        base += [
            "Seek urgent cardiological evaluation",
            "Consider ECG and stress test",
            "Review medications with doctor",
        ]
    elif pct >= 40:
        base += ["Adopt heart-healthy diet (less sodium/fat)", "Manage stress"]
    else:
        base += ["Annual lipid panel screening", "Avoid smoking"]
    return base


# ─────────────────────────────────────────────────────────────────
# ERROR HANDLERS
# ─────────────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    logger.warning(f"404 error: {request.path}")
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    logger.error(f"500 error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500


# ─────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    debug_mode = "--debug" in sys.argv or os.getenv("FLASK_DEBUG") == "True"
    
    print("\n" + "=" * 50)
    print("   MedPredict AI - Disease Risk Prediction")
    print("=" * 50)
    print(f"  Mode   : {'DEBUG' if debug_mode else 'PRODUCTION'}")
    print(f"  URL    : http://127.0.0.1:5000")
    print(f"  Models : {'[OK] Ready' if models_ready else '[!!] Not ready - run: python train_models.py'}")
    print("=" * 50 + "\n")

    logger.info("Starting MedPredict AI application")
    app.run(debug=debug_mode, port=5000, host="127.0.0.1")
