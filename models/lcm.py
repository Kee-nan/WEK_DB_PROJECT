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


class PlanScorer:
    """Simple helper to score candidate plans using the trained LCM.

    The class expects a trained model available via `load_model()`.
    It converts a candidate plan dict into the feature vector expected by
    the LCM (join_count, estimated_cost, estimated_rows) and returns
    the model's runtime prediction (ms).
    """

    def __init__(self, model=None):
        self._model = model

    def ensure_model(self):
        if self._model is None:
            self._model = load_model()
        return self._model

    def _features_from_plan(self, plan: dict):
        # plan is expected to contain keys like join_count, estimated_cost, estimated_rows
        return {
            'join_count': float(plan.get('join_count', 0)),
            'estimated_cost': float(plan.get('estimated_cost', 0)),
            'estimated_rows': float(plan.get('estimated_rows', 0))
        }

    def score_candidate(self, candidate: dict):
        m = self.ensure_model()
        feats = self._features_from_plan(candidate)
        import pandas as _pd
        X = _pd.DataFrame([feats])
        # Use existing feature pipeline
        Xf = get_feature_matrix(X)
        pred = m.predict(Xf)[0]
        return float(pred)

    def choose_best(self, candidates: list):
        best = None
        best_pred = None
        for c in candidates:
            try:
                p = self.score_candidate(c)
            except Exception:
                p = None
            if p is None:
                continue
            if best_pred is None or p < best_pred:
                best_pred = p
                best = c
        return best, best_pred

    def pick_and_serialize(self, query_name: str, candidates: list, out_csv: str, chosen_dir: str = None):
        """Choose the best candidate, append a short CSV row and optionally
        write the chosen plan JSON into `chosen_dir/<query_name>.json`.
        Returns a dict with chosen_pred_ms and chosen_plan.
        """
        best, best_pred = self.choose_best(candidates)
        # Append a simple CSV summary for compatibility
        import csv, json
        row = {
            'query_name': query_name,
            'chosen_pred_ms': best_pred if best_pred is not None else '',
            'chosen_plan_summary': json.dumps(best) if best is not None else ''
        }
        os.makedirs(os.path.dirname(out_csv), exist_ok=True)
        write_header = not os.path.exists(out_csv)
        with open(out_csv, 'a', newline='', encoding='utf-8') as fh:
            writer = csv.DictWriter(fh, fieldnames=row.keys())
            if write_header:
                writer.writeheader()
            writer.writerow(row)

        if chosen_dir and best is not None:
            os.makedirs(chosen_dir, exist_ok=True)
            safe = query_name.replace('/', '_').replace('\\', '_')
            target = os.path.join(chosen_dir, f"{safe}.json")
            with open(target, 'w', encoding='utf-8') as f:
                json.dump(best, f, indent=2)

        return {'chosen_plan': best, 'chosen_pred_ms': best_pred}
