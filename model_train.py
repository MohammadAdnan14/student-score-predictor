import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import pickle


df = pd.read_csv("StudentPerformance.csv")

print(" Dataset loaded successfully!")
print(df.head(), "\n")


df["Extracurricular Activities"] = df["Extracurricular Activities"].map({"Yes": 1, "No": 0})


features = [
    "Hours Studied",
    "Previous Scores",
    "Extracurricular Activities",
    "Sleep Hours",
    "Sample Question Papers Practiced"
]
target = "Performance Index"

X = df[features]
y = df[target]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


model = LinearRegression()
model.fit(X_train, y_train)


y_pred = model.predict(X_test)

r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(" Model Evaluation:")
print(f"R² Score: {r2:.3f}")
print(f"MAE: {mae:.3f}")
print(f"RMSE: {rmse:.3f}")


with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("\n Model saved as 'model.pkl'")


sample = np.array([[5, 70, 1, 7, 3]]) 
predicted_score = model.predict(sample)[0]
print(f"\n Sample Prediction: {predicted_score:.2f}")
