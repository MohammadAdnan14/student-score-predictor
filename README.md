# Student Performance Predictor (Flask + HTML/CSS/JS)

## What this project contains
- Flask backend (`app.py`) exposing a `/predict` API and a static frontend (`templates/index.html`, `static/`).
- A `model_train.py` script that will train a LinearRegression model from `StudentPerformance.csv` if you place it in the project root.
- If no trained model is found, the backend uses a simple heuristic fallback so the app still functions.

## How to run locally
1. (Optional) Create a virtualenv: `python -m venv venv && source venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. If you have `StudentPerformance.csv` in the project root, run `python model_train.py` to create `model.pkl`.
4. Run the app: `python app.py`
5. Open `http://127.0.0.1:5000` in your browser.

## Notes
- The training script tries to auto-detect columns. If it fails, inspect the CSV and update `model_train.py` variable names.
- This project was generated from your uploaded Jupyter notebook. You can customize the frontend or model behavior further.
