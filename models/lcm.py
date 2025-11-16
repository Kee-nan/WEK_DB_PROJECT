import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error


MODEL_PATH = os.path.join(os.path.dirname(__file__), "lcm.pkl")


def get_feature_matrix(df):
    # Basic features we extract from the collected CSV
    # Keep it simple and robust: join_count, estimated_cost, estimated_rows
    features = df[["join_count", "estimated_cost", "estimated_rows"]].copy()
    # Fill missing values defensively
    features = features.fillna(0)
    return features


def train_and_save(csv_path, overwrite=False, n_estimators=100, random_state=42):
    df = pd.read_csv(csv_path)
    X = get_feature_matrix(df)
    y = df["actual_runtime_ms"].fillna(0)

    # Use a hold-out set internally for quick validation
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=random_state)

    model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
    model.fit(X_train, y_train)

    preds = model.predict(X_val)
    mae = mean_absolute_error(y_val, preds)
    print(f"LCM trained — validation MAE: {mae:.3f} ms")

    # Ensure models directory exists
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    if overwrite or not os.path.exists(MODEL_PATH):
        joblib.dump(model, MODEL_PATH)
        print(f"Saved LCM to {MODEL_PATH}")

    return model


def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    raise FileNotFoundError(f"LCM model not found at {MODEL_PATH}. Run training first.")


def predict(model, df):
    X = get_feature_matrix(df)
    return model.predict(X)
