"""Generate per-query comparison between Baseline, LCM and Hybrid and produce a static HTML report."""
import os
import sys
import json
import pandas as pd

# Ensure project root is importable
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT)

from models import lcm as lcm_mod, hybrid as hybrid_mod


DATA_CSV = os.path.join(ROOT, "results", "query_metrics.csv")
OUT_CSV = os.path.join(ROOT, "results", "query_metrics_comparison.csv")
OUT_DIR = os.path.join(ROOT, "results", "website")
OUT_HTML = os.path.join(OUT_DIR, "index.html")
os.makedirs(OUT_DIR, exist_ok=True)


def build_comparison():
    if not os.path.exists(DATA_CSV):
        raise FileNotFoundError(f"Data CSV not found at {DATA_CSV}. Run data collection first.")

    df = pd.read_csv(DATA_CSV)

    # Load models
    # Baseline and selector are loaded via hybrid.load_hybrid(); it will also try to load LCM
    try:
        baseline, lcm_model, selector = hybrid_mod.load_hybrid()
    except Exception:
        # If hybrid components not trained, try to train quickly using train_and_eval approach
        from scripts.train_and_eval import main as train_and_eval_main
        print("Hybrid components not found. Training quick models now...")
        train_and_eval_main()
        baseline, lcm_model, selector = hybrid_mod.load_hybrid()

    # Predictions
    base_pred = baseline.predict(df[["estimated_cost"]].fillna(0))

    # LCM prediction: ensure feature matrix same as LCM expected
    try:
        X_feat = lcm_mod.get_feature_matrix(df)
    except Exception:
        X_feat = df[["join_count", "estimated_cost", "estimated_rows"]].fillna(0)

    lcm_pred = lcm_model.predict(X_feat)
    hybrid_pred = hybrid_mod.predict_hybrid(df)

    # Build comparison DataFrame
    comp = df.copy()
    comp["pred_baseline_ms"] = base_pred
    comp["pred_lcm_ms"] = lcm_pred
    comp["pred_hybrid_ms"] = hybrid_pred

    # Absolute errors
    comp["err_baseline_ms"] = (comp["pred_baseline_ms"] - comp["actual_runtime_ms"]).abs()
    comp["err_lcm_ms"] = (comp["pred_lcm_ms"] - comp["actual_runtime_ms"]).abs()
    comp["err_hybrid_ms"] = (comp["pred_hybrid_ms"] - comp["actual_runtime_ms"]).abs()

    # Which model was closest? (ties pick the model with lowest name by alphabetical order)
    def winner_row(r):
        errs = {"Baseline": r.err_baseline_ms, "LCM": r.err_lcm_ms, "Hybrid": r.err_hybrid_ms}
        return min(errs.items(), key=lambda x: (x[1], x[0]))[0]

    comp["closest_model"] = comp.apply(winner_row, axis=1)

    # Try to merge chosen plan predictions produced by scripts/generate_plans.py
    rich_choices = os.path.join(ROOT, 'results', 'generated_plan_choices_rich.csv')
    if os.path.exists(rich_choices):
      try:
        rc = pd.read_csv(rich_choices)
        # merge on query_name
        comp = comp.merge(rc[['query_name', 'chosen_pred_ms', 'would_be_faster_than_baseline']], on='query_name', how='left')
      except Exception:
        comp['chosen_pred_ms'] = None
        comp['would_be_faster_than_baseline'] = False
    else:
      comp['chosen_pred_ms'] = None
      comp['would_be_faster_than_baseline'] = False

    # Summary metrics
    summary = {
        "mae_baseline": comp["err_baseline_ms"].mean(),
        "mae_lcm": comp["err_lcm_ms"].mean(),
        "mae_hybrid": comp["err_hybrid_ms"].mean(),
      "winner_counts": comp["closest_model"].value_counts().to_dict()
    }

    # Plan-quality metrics: use chosen_pred_ms as the LCM's chosen-plan predicted runtime
    # Average chosen predicted runtime (where available)
    try:
      chosen_mean = comp['chosen_pred_ms'].dropna().astype(float).mean()
    except Exception:
      chosen_mean = None

    # Count where the LCM chosen-plan prediction is (predicted) faster than the
    # baseline actual runtime
    try:
      lcm_better_count = int(comp[comp['would_be_faster_than_baseline'] == True].shape[0])
    except Exception:
      lcm_better_count = 0

    # Count where Hybrid predicted runtime is less than baseline actual runtime
    try:
      hybrid_better_count = int((comp['pred_hybrid_ms'] < comp['actual_runtime_ms']).sum())
    except Exception:
      hybrid_better_count = 0

    # Add plan-quality metrics into summary
    summary['chosen_pred_mean_ms'] = chosen_mean
    summary['lcm_predicted_better_count'] = lcm_better_count
    summary['hybrid_predicted_better_count'] = hybrid_better_count

    comp.to_csv(OUT_CSV, index=False)
    print(f"Wrote comparison CSV to {OUT_CSV}")

    # Write a self-contained HTML report embedding the JSON data
    rows = comp.to_dict(orient="records")
    html = render_html(rows, summary)
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote website to {OUT_HTML}")


def render_html(rows, summary):
    # Escape JSON
    data_json = json.dumps(rows)
    summary_json = json.dumps(summary)

    # Minimal HTML with embedded data and Chart.js for simple plotting
    html_template = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Query Runtime Prediction Comparison</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 20px; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 12px; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; font-size: 13px; }}
    th {{ background: #f4f4f4; }}
    .small {{ font-size: 12px; color: #555; }}
  </style>
</head>
<body>
  <h1>Query Runtime Prediction Comparison</h1>
  <p class="small">This report compares three estimators: Baseline (linear mapping of PostgreSQL estimated cost), LCM (RandomForest), and Hybrid (selector chooses per-query).</p>

  <h2>Summary</h2>
  <div id="summary"></div>

  <h2>MAE by Model</h2>
  <canvas id="maeChart" width="600" height="250"></canvas>

  <h2>Per-query results</h2>
  <table id="results">
    <thead>
      <tr>
        <th>query_name</th>
        <th>category</th>
        <th>actual_runtime_ms</th>
        <th>pred_baseline_ms</th>
        <th>pred_lcm_ms</th>
        <th>pred_hybrid_ms</th>
        <th>chosen_pred_ms</th>
        <th>lcm_would_be_faster</th>
        <th>closest_model</th>
      </tr>
    </thead>
    <tbody></tbody>
  </table>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script>
    const rows = __DATA_JSON__;
    const summary = __SUMMARY_JSON__;

    // Fill summary
    const sDiv = document.getElementById('summary');
    let planLine = '';
    if (summary.chosen_pred_mean_ms != null) {
      planLine = `<p class='small'><strong>LCM chosen-plan predicted mean</strong>: ${summary.chosen_pred_mean_ms.toFixed(2)} ms; <strong>LCM predicted better count</strong>: ${summary.lcm_predicted_better_count}; <strong>Hybrid predicted better count</strong>: ${summary.hybrid_predicted_better_count}.</p>`;
    }
    sDiv.innerHTML = `<p class='small'><strong>MAE</strong> — Baseline: ${summary.mae_baseline.toFixed(2)} ms; LCM: ${summary.mae_lcm.toFixed(2)} ms; Hybrid: ${summary.mae_hybrid.toFixed(2)} ms.</p>`
      + `<p class='small'><strong>Winner counts</strong> — ` + Object.entries(summary.winner_counts).map(kv => `${kv[0]}: ${kv[1]}`).join(', ') + `</p>`
      + planLine;

    // Fill table
    const tbody = document.querySelector('#results tbody');
    rows.forEach(r => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${r.query_name}</td>
        <td>${r.category}</td>
        <td>${Number(r.actual_runtime_ms).toFixed(3)}</td>
        <td>${Number(r.pred_baseline_ms).toFixed(3)}</td>
        <td>${Number(r.pred_lcm_ms).toFixed(3)}</td>
        <td>${Number(r.pred_hybrid_ms).toFixed(3)}</td>
        <td>${r.chosen_pred_ms != null ? Number(r.chosen_pred_ms).toFixed(3) : ''}</td>
        <td>${r.would_be_faster_than_baseline ? 'yes' : 'no'}</td>
        <td>${r.closest_model}</td>`;
      tbody.appendChild(tr);
    });

    // MAE chart
    const ctx = document.getElementById('maeChart').getContext('2d');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Baseline','LCM','Hybrid'],
        datasets: [{
          label: 'MAE (ms)',
          data: [summary.mae_baseline, summary.mae_lcm, summary.mae_hybrid],
          backgroundColor: ['#4e79a7','#f28e2b','#76b7b2']
        }]
      },
      options: { responsive: true }
    });
  </script>
</body>
</html>
"""

    # Replace placeholders with JSON content
    return html_template.replace("__DATA_JSON__", data_json).replace("__SUMMARY_JSON__", summary_json)


if __name__ == '__main__':
    build_comparison()
