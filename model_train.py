# Trains a LinearRegression model if StudentPerformance.csv is present.
import os, pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

DATA_FILE = "StudentPerformance.csv"
MODEL_PATH = "model.pkl"

if not os.path.exists(DATA_FILE):
    print("Data file not found:", DATA_FILE)
    print("Place the CSV in the project root and re-run this script to create model.pkl")
else:
    df = pd.read_csv(DATA_FILE)
    # Expecting columns - adapt if different. We'll try to find reasonable columns.
    # Preferred columns: 'Study Hours', 'Sleep Hours', 'Attendance', 'Extracurricular', 'Performance Index'
    col_map = {}
    cols = [c.lower() for c in df.columns]
    # find candidate columns by name matching
    def find_col(key_options):
        for k in key_options:
            for c in df.columns:
                if k.lower() in c.lower():
                    return c
        return None
    study_col = find_col(["study","study hours","hours studied"])
    sleep_col = find_col(["sleep","sleep hours"])
    attend_col = find_col(["attendance"])
    extra_col = find_col(["extracurricular","extra curricular","activities"])
    target_col = find_col(["performance index","performance","score","marks"])

    required = [study_col, sleep_col, attend_col, extra_col, target_col]
    if any(v is None for v in required):
        print("Could not find all required columns automatically. Detected columns:", required)
        print("Available columns:", list(df.columns))
        raise SystemExit(1)

    # Prepare features
    X = df[[study_col, sleep_col, attend_col, extra_col]].copy()
    # Ensure extracurricular is numeric (map yes/no to 1/0)
    X[extra_col] = X[extra_col].apply(lambda v: 1 if str(v).strip().lower() in ["yes","y","1","true","t"] else 0)
    y = df[target_col]

    pipeline = Pipeline([("scaler", StandardScaler()), ("lr", LinearRegression())])
    pipeline.fit(X, y)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(pipeline, f)
    print("Model trained and saved to", MODEL_PATH)
