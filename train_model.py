"""Train the loan approval pipeline from the notebook's CSV dataset."""
from pathlib import Path
import argparse
import json
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.joblib"
META_PATH = BASE_DIR / "model_metadata.json"
TARGET = "Loan_Approved"


def train(csv_path: str) -> None:
    data = pd.read_csv(csv_path)
    data = data.drop_duplicates().copy()
    data[TARGET] = data[TARGET].map({"Yes": 1, "No": 0}).fillna(data[TARGET]).astype(int)
    X = data.drop(columns=[TARGET])
    y = data[TARGET]
    categorical = X.select_dtypes(include=["object", "string"]).columns.tolist()
    numeric = [column for column in X.columns if column not in categorical]
    preprocessing = ColumnTransformer([
        ("numeric", SimpleImputer(strategy="median"), numeric),
        ("categorical", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]), categorical),
    ])
    pipeline = Pipeline([
        ("preprocessing", preprocessing),
        ("classifier", RandomForestClassifier(
            n_estimators=40,
            max_depth=16,
            min_samples_leaf=2,
            random_state=42,
            class_weight="balanced",
            n_jobs=-1,
        )),
    ])
    stratify = y if y.value_counts().min() >= 2 else None
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=stratify)
    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)
    print(classification_report(y_test, predictions, zero_division=0))
    print(f"Accuracy: {accuracy_score(y_test, predictions):.3f}")
    joblib.dump(pipeline, MODEL_PATH, compress=3)
    META_PATH.write_text(json.dumps({"features": X.columns.tolist(), "rows": len(data), "accuracy": accuracy_score(y_test, predictions)}, indent=2))
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", nargs="?", default=str(BASE_DIR / "loan_approval.csv"))
    train(parser.parse_args().csv)
