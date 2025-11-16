import os
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from .lcm import get_feature_matrix


BASE_MODEL_PATH = os.path.join(os.path.dirname(__file__), "baseline_linreg.pkl")
HYBRID_MODEL_PATH = os.path.join(os.path.dirname(__file__), "hybrid_selector.pkl")


def train_baseline_linear(csv_path):
    df = pd.read_csv(csv_path)
    # Map PostgreSQL's estimated cost to runtime with a simple linear model
    X = df[["estimated_cost"]].fillna(0)
    y = df["actual_runtime_ms"].fillna(0)
    model = LinearRegression()
    model.fit(X, y)
    joblib.dump(model, BASE_MODEL_PATH)
    print(f"Saved baseline linear model to {BASE_MODEL_PATH}")
    return model


def load_baseline():
    if os.path.exists(BASE_MODEL_PATH):
        return joblib.load(BASE_MODEL_PATH)
    raise FileNotFoundError("Baseline model not found. Train it with train_baseline_linear().")


def train_hybrid_selector(csv_path, random_state=42, max_depth=4):
    df = pd.read_csv(csv_path)
    X = get_feature_matrix(df)
    y_true = df["actual_runtime_ms"].fillna(0)

    # Train baseline and LCM predictions on a split so we can label which predictor is better
    X_train, X_val, y_train, y_val, df_train, df_val = train_test_split(
        X, y_true, df, test_size=0.3, random_state=random_state)

    # Baseline linear mapping
    baseline = LinearRegression().fit(df_train[["estimated_cost"]].fillna(0), y_train)
    lcm_model = None
    try:
        from .lcm import RandomForestRegressor  # not normally imported this way
    except Exception:
        pass

    # Use previously trained LCM if exists: try to load
    try:
        from .lcm import load_model as load_lcm
        lcm_model = load_lcm()
    except Exception:
        # fallback: train a small lcm here
        from .lcm import train_and_save
        lcm_model = train_and_save(csv_path, overwrite=True)

    pred_baseline = baseline.predict(df_val[["estimated_cost"]].fillna(0))
    pred_lcm = lcm_model.predict(X_val)

    # Create label: 1 if LCM is better (lower absolute error), else 0
    err_baseline = abs(pred_baseline - y_val)
    err_lcm = abs(pred_lcm - y_val)
    choose_lcm = (err_lcm < err_baseline).astype(int)

    # Train a small decision tree to choose which predictor to use given features
    selector = DecisionTreeClassifier(max_depth=max_depth, random_state=random_state)
    selector.fit(X_val, choose_lcm)

    joblib.dump(baseline, BASE_MODEL_PATH)
    joblib.dump(selector, HYBRID_MODEL_PATH)
    print(f"Saved hybrid selector to {HYBRID_MODEL_PATH} and baseline to {BASE_MODEL_PATH}")
    return baseline, lcm_model, selector


def load_hybrid():
    if not os.path.exists(HYBRID_MODEL_PATH) or not os.path.exists(BASE_MODEL_PATH):
        raise FileNotFoundError("Hybrid components not found. Run train_hybrid_selector().")
    baseline = joblib.load(BASE_MODEL_PATH)
    selector = joblib.load(HYBRID_MODEL_PATH)
    try:
        from .lcm import load_model as load_lcm
        lcm = load_lcm()
    except Exception:
        lcm = None
    return baseline, lcm, selector


def predict_hybrid(df):
    baseline, lcm, selector = load_hybrid()
    X = get_feature_matrix(df)

    base_pred = baseline.predict(df[["estimated_cost"]].fillna(0))
    lcm_pred = lcm.predict(X)

    choose_lcm = selector.predict(X)
    # If choose_lcm==1 use lcm_pred else base_pred
    result = [lcm_pred[i] if choose_lcm[i] == 1 else base_pred[i] for i in range(len(choose_lcm))]
    return result
