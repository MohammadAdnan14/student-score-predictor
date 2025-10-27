from flask import Flask, request, jsonify, render_template
import os, pickle

MODEL_PATH = "model.pkl"

app = Flask(__name__, static_folder='static', template_folder='templates')

def load_model():
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json or {}
    model = load_model()
    # Expected fields: study_hours, sleep_hours, attendance, extracurricular (0 or 1)
    try:
        study = float(data.get("study_hours", 0))
        sleep = float(data.get("sleep_hours", 0))
        attendance = float(data.get("attendance", 0))
        extra = int(data.get("extracurricular", 0))
    except Exception as e:
        return jsonify({"error": "Invalid input types", "details": str(e)}), 400

    if model:
        # model expects a 2D array
        X = [[study, sleep, attendance, extra]]
        pred = model.predict(X)[0]
        source = "trained_model"
    else:
        # fallback heuristic if no model available
        pred = (0.5*study) + (0.2*sleep) + (0.25*(attendance/100)*10) + (0.5*extra)
        source = "heuristic_fallback"
    # Clip prediction to 0-100 range
    pred = max(0, min(100, float(pred)))
    remark = "Excellent" if pred>=75 else ("Good" if pred>=60 else ("Average" if pred>=40 else "Needs Improvement"))
    return jsonify({"predicted_score": round(pred,2), "remark": remark, "source": source})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
