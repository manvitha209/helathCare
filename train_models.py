"""
train_models.py
---------------
Trains RandomForest classifiers for Diabetes and Heart Disease prediction.
Saves models and scalers to the /models directory.

Usage:
    python train_models.py
"""

import os
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.utils import resample

# Create models directory
os.makedirs("models", exist_ok=True)

# ─────────────────────────────────────────────
# DIABETES MODEL  (Pima Indians Diabetes Dataset)
# Features: Pregnancies, Glucose, BloodPressure, SkinThickness,
#           Insulin, BMI, DiabetesPedigreeFunction, Age
# ─────────────────────────────────────────────

print("=" * 60)
print("  Training Diabetes Model")
print("=" * 60)

# Synthetic dataset based on Pima Indians statistical distributions
# (mimics the real Kaggle dataset for hackathon use without file dependency)
np.random.seed(42)

def generate_diabetes_data(n=2000):
    rows = []
    for _ in range(n):
        outcome = np.random.choice([0, 1], p=[0.65, 0.35])
        if outcome == 1:  # Diabetic
            pregnancies = np.random.poisson(4)
            glucose = np.random.normal(141, 31)
            bp = np.random.normal(70, 12)
            skin = np.random.normal(33, 11)
            insulin = np.random.normal(200, 120)
            bmi = np.random.normal(35, 7)
            dpf = np.random.gamma(2, 0.25)
            age = np.random.normal(37, 10)
        else:  # Non-diabetic
            pregnancies = np.random.poisson(2)
            glucose = np.random.normal(109, 26)
            bp = np.random.normal(68, 11)
            skin = np.random.normal(27, 10)
            insulin = np.random.normal(130, 90)
            bmi = np.random.normal(30, 7)
            dpf = np.random.gamma(1.2, 0.2)
            age = np.random.normal(30, 10)

        rows.append([
            max(0, int(pregnancies)),
            np.clip(glucose, 44, 199),
            np.clip(bp, 24, 122),
            np.clip(skin, 0, 99),
            np.clip(insulin, 0, 846),
            np.clip(round(bmi, 1), 0, 67.1),
            round(max(0.078, dpf), 3),
            max(21, int(age)),
            outcome
        ])
    return pd.DataFrame(rows, columns=[
        "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
        "Insulin", "BMI", "DiabetesPedigreeFunction", "Age", "Outcome"
    ])

df_diabetes = generate_diabetes_data(3000)

X_d = df_diabetes.drop("Outcome", axis=1)
y_d = df_diabetes["Outcome"]

X_d_train, X_d_test, y_d_train, y_d_test = train_test_split(
    X_d, y_d, test_size=0.2, random_state=42, stratify=y_d
)

scaler_d = StandardScaler()
X_d_train_sc = scaler_d.fit_transform(X_d_train)
X_d_test_sc  = scaler_d.transform(X_d_test)

diabetes_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)
diabetes_model.fit(X_d_train_sc, y_d_train)

y_d_pred = diabetes_model.predict(X_d_test_sc)
y_d_prob = diabetes_model.predict_proba(X_d_test_sc)[:, 1]

acc_d  = accuracy_score(y_d_test, y_d_pred)
auc_d  = roc_auc_score(y_d_test, y_d_prob)
cv_d   = cross_val_score(diabetes_model, X_d_train_sc, y_d_train, cv=5, scoring="accuracy")

print(f"  Accuracy  : {acc_d:.4f}  ({acc_d*100:.1f}%)")
print(f"  ROC-AUC   : {auc_d:.4f}")
print(f"  CV Mean   : {cv_d.mean():.4f} ± {cv_d.std():.4f}")
print()
print(classification_report(y_d_test, y_d_pred, target_names=["No Diabetes", "Diabetes"]))

with open("models/diabetes_model.pkl", "wb") as f:
    pickle.dump(diabetes_model, f)
with open("models/diabetes_scaler.pkl", "wb") as f:
    pickle.dump(scaler_d, f)
print("  [OK] Diabetes model saved -> models/diabetes_model.pkl")


# ─────────────────────────────────────────────
# HEART DISEASE MODEL  (Cleveland Heart Disease)
# Features: age, sex, cp, trestbps, chol, fbs, restecg,
#           thalach, exang, oldpeak, slope, ca, thal
# ─────────────────────────────────────────────

print()
print("=" * 60)
print("  Training Heart Disease Model")
print("=" * 60)

def generate_heart_data(n=2000):
    rows = []
    for _ in range(n):
        target = np.random.choice([0, 1], p=[0.54, 0.46])
        sex = np.random.choice([0, 1], p=[0.32, 0.68])
        if target == 1:  # Has heart disease
            age = int(np.clip(np.random.normal(56, 9), 29, 77))
            cp = np.random.choice([0, 1, 2, 3], p=[0.47, 0.17, 0.28, 0.08])
            trestbps = int(np.clip(np.random.normal(134, 18), 94, 200))
            chol = int(np.clip(np.random.normal(251, 52), 126, 564))
            fbs = np.random.choice([0, 1], p=[0.84, 0.16])
            restecg = np.random.choice([0, 1, 2], p=[0.46, 0.52, 0.02])
            thalach = int(np.clip(np.random.normal(139, 23), 71, 202))
            exang = np.random.choice([0, 1], p=[0.43, 0.57])
            oldpeak = round(np.clip(np.random.exponential(1.6), 0, 6.2), 1)
            slope = np.random.choice([0, 1, 2], p=[0.35, 0.58, 0.07])
            ca = np.random.choice([0, 1, 2, 3], p=[0.26, 0.37, 0.22, 0.15])
            thal = np.random.choice([0, 1, 2, 3], p=[0.02, 0.08, 0.54, 0.36])
        else:  # No heart disease
            age = int(np.clip(np.random.normal(52, 9), 29, 77))
            cp = np.random.choice([0, 1, 2, 3], p=[0.17, 0.14, 0.43, 0.26])
            trestbps = int(np.clip(np.random.normal(129, 16), 94, 200))
            chol = int(np.clip(np.random.normal(242, 54), 126, 564))
            fbs = np.random.choice([0, 1], p=[0.88, 0.12])
            restecg = np.random.choice([0, 1, 2], p=[0.56, 0.43, 0.01])
            thalach = int(np.clip(np.random.normal(158, 19), 71, 202))
            exang = np.random.choice([0, 1], p=[0.77, 0.23])
            oldpeak = round(np.clip(np.random.exponential(0.7), 0, 6.2), 1)
            slope = np.random.choice([0, 1, 2], p=[0.11, 0.37, 0.52])
            ca = np.random.choice([0, 1, 2, 3], p=[0.59, 0.25, 0.11, 0.05])
            thal = np.random.choice([0, 1, 2, 3], p=[0.02, 0.05, 0.87, 0.06])

        rows.append([age, sex, cp, trestbps, chol, fbs, restecg,
                     thalach, exang, oldpeak, slope, ca, thal, target])
    return pd.DataFrame(rows, columns=[
        "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
        "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"
    ])

df_heart = generate_heart_data(3000)

X_h = df_heart.drop("target", axis=1)
y_h = df_heart["target"]

X_h_train, X_h_test, y_h_train, y_h_test = train_test_split(
    X_h, y_h, test_size=0.2, random_state=42, stratify=y_h
)

scaler_h = StandardScaler()
X_h_train_sc = scaler_h.fit_transform(X_h_train)
X_h_test_sc  = scaler_h.transform(X_h_test)

heart_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)
heart_model.fit(X_h_train_sc, y_h_train)

y_h_pred = heart_model.predict(X_h_test_sc)
y_h_prob = heart_model.predict_proba(X_h_test_sc)[:, 1]

acc_h  = accuracy_score(y_h_test, y_h_pred)
auc_h  = roc_auc_score(y_h_test, y_h_prob)
cv_h   = cross_val_score(heart_model, X_h_train_sc, y_h_train, cv=5, scoring="accuracy")

print(f"  Accuracy  : {acc_h:.4f}  ({acc_h*100:.1f}%)")
print(f"  ROC-AUC   : {auc_h:.4f}")
print(f"  CV Mean   : {cv_h.mean():.4f} ± {cv_h.std():.4f}")
print()
print(classification_report(y_h_test, y_h_pred, target_names=["No Disease", "Heart Disease"]))

with open("models/heart_model.pkl", "wb") as f:
    pickle.dump(heart_model, f)
with open("models/heart_scaler.pkl", "wb") as f:
    pickle.dump(scaler_h, f)
print("  [OK] Heart Disease model saved -> models/heart_model.pkl")

print()
print("=" * 60)
print("  All models trained and saved successfully!")
print("  Run: python app.py  to start the Flask server")
print("=" * 60)

