from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os

app = Flask(__name__)

MODEL_PATH = "model.pkl"


if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
else:
    model = None
    print("⚠️ model.pkl not found! Please run model_train.py first.")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        print("Received data:", data)

        hours = float(data.get("hours_studied", 0))
        prev_score = float(data.get("previous_scores", 0))
        sleep = float(data.get("sleep_hours", 0))
        papers = float(data.get("papers_practiced", 0))
        extra_raw = str(data.get("extracurricular", "No")).strip().lower()
        extra = 1 if extra_raw in ["yes", "y", "1", "true"] else 0

        features = np.array([[hours, prev_score, extra, sleep, papers]])
        print("Features:", features)

        if model:
            predicted_score = model.predict(features)[0]
            source = "Trained ML Model"
        else:
        
            predicted_score = (hours * 5) + (prev_score * 0.4) + (sleep * 2) + (papers * 3) + (extra * 5)
            predicted_score = min(100, predicted_score)
            source = "Heuristic Fallback"

      
        if predicted_score >= 85:
            remark = "Excellent Performance!"
        elif predicted_score >= 70:
            remark = "Good Job! Keep it up."
        elif predicted_score >= 50:
            remark = "Average. You can improve!"
        else:
            remark = "Needs Improvement."

        return jsonify({
            "predicted_score": round(predicted_score, 2),
            "remark": remark,
            "source": source
        })
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
