import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Ensure project root is on sys.path so `models` package can be imported
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT)

from models import lcm, hybrid

# Paths
DATA_CSV = os.path.join(ROOT, "results", "query_metrics.csv")
PLOTS_DIR = os.path.join(ROOT, "results", "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)


def evaluate_predictions(y_true, preds, label):
    mae = mean_absolute_error(y_true, preds)
    rmse = mean_squared_error(y_true, preds, squared=False)
    print(f"{label} — MAE: {mae:.3f} ms, RMSE: {rmse:.3f} ms")
    return mae, rmse


def main():
    if not os.path.exists(DATA_CSV):
        print(f"Data not found at {DATA_CSV}. Run `scripts/run_queries.py` first.")
        return

    df = pd.read_csv(DATA_CSV)
    # Split into train/test so training scripts inside modules can consume same CSV
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    train_csv = os.path.join(os.path.dirname(__file__), "_train_tmp.csv")
    test_csv = os.path.join(os.path.dirname(__file__), "_test_tmp.csv")
    train_df.to_csv(train_csv, index=False)
    test_df.to_csv(test_csv, index=False)

    print("Training LCM and Hybrid selector (baseline = raw PostgreSQL estimate)...")
    # Train LCM and hybrid selector (baseline remains raw PostgreSQL estimated_cost)
    lcm_model = lcm.train_and_save(train_csv, overwrite=True)
    baseline, lcm_model, selector = hybrid.train_hybrid_selector(train_csv)

    # Evaluate on held-out test set
    y_true = test_df["actual_runtime_ms"].fillna(0)

    # Baseline predictions
    base_pred = baseline.predict(test_df[["estimated_cost"]].fillna(0))
    evaluate_predictions(y_true, base_pred, "Baseline (PostgreSQL estimated_cost)")

    # LCM predictions
    lcm_pred = lcm_model.predict(lcm.get_feature_matrix(test_df))
    evaluate_predictions(y_true, lcm_pred, "LCM (RandomForest)")

    # Hybrid predictions
    hybrid_pred = hybrid.predict_hybrid(test_df)
    evaluate_predictions(y_true, hybrid_pred, "Hybrid Selector")

    # Cleanup temp files
    try:
        os.remove(train_csv)
        os.remove(test_csv)
    except Exception:
        pass

    print("Done. Models saved under `models/`. Plots not implemented (kept minimal).")


if __name__ == "__main__":
    main()
