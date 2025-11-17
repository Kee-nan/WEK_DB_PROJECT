"""Generate candidate plans per query, score them with the LCM, and
serialize the chosen plan for comparison with the baseline.

This script does not modify the original data files — it writes outputs
into `results/generated_plan_choices.csv`, `results/generated_plan_choices_rich.csv`,
and `results/chosen_plans/`.
"""
import os
import sys
import json

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT)

import pandas as pd

from models.lcm import PlanScorer, load_model, train_and_save


DATA_CSV = os.path.join(ROOT, 'results', 'query_metrics.csv')
OUT_CSV = os.path.join(ROOT, 'results', 'generated_plan_choices.csv')
OUT_RICH = os.path.join(ROOT, 'results', 'generated_plan_choices_rich.csv')
CHOSEN_DIR = os.path.join(ROOT, 'results', 'chosen_plans')
OUT_SQL_DIR = os.path.join(ROOT, 'results', 'generated_sql_alternatives')


def synthesize_candidates(row):
    """Create a small set of candidate plan summaries for a query.

    This is a lightweight enumerator that creates three candidates:
    - the original (baseline) plan (if plan_json exists)
    - a cheaper-cost hypothetical plan (cost * 0.6)
    - a more expensive plan (cost * 1.3)

    Each candidate is a dict containing keys the PlanScorer expects
    (join_count, estimated_cost, estimated_rows) and a short textual tag.
    """
    candidates = []
    try:
        est_cost = float(row.get('estimated_cost', 0) or 0)
    except Exception:
        est_cost = 0.0
    try:
        est_rows = float(row.get('estimated_rows', 0) or 0)
    except Exception:
        est_rows = 0.0
    join_count = int(row.get('join_count') or 0)

    # Baseline candidate (best-effort extract from plan_json if available)
    base = {
        'tag': 'baseline',
        'join_count': join_count,
        'estimated_cost': est_cost,
        'estimated_rows': est_rows
    }
    candidates.append(base)

    # Cheaper candidate
    cheap = {
        'tag': 'cheap_variant',
        'join_count': join_count,
        'estimated_cost': max(1.0, est_cost * 0.6),
        'estimated_rows': max(1.0, est_rows * 0.9)
    }
    candidates.append(cheap)

    # More expensive candidate
    expensive = {
        'tag': 'expensive_variant',
        'join_count': max(0, join_count),
        'estimated_cost': est_cost * 1.3,
        'estimated_rows': est_rows * 1.1
    }
    candidates.append(expensive)

    return candidates


def main():
    if not os.path.exists(DATA_CSV):
        raise FileNotFoundError(f"Data CSV missing at {DATA_CSV}. Run query collection first.")

    df = pd.read_csv(DATA_CSV)

    # Ensure a model exists; if not, train quickly using the data we have
    try:
        m = load_model()
    except Exception:
        print("No LCM found — training a quick model from available data...")
        train_and_save(DATA_CSV, overwrite=True)
        m = load_model()

    scorer = PlanScorer(m)

    # Prepare outputs
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    if os.path.exists(OUT_CSV):
        os.remove(OUT_CSV)
    if os.path.exists(OUT_RICH):
        os.remove(OUT_RICH)
    os.makedirs(CHOSEN_DIR, exist_ok=True)

    # Iterate queries
    for _, row in df.iterrows():
        qname = row.get('query_name') or row.get('name') or 'unknown'
        candidates = synthesize_candidates(row)
        res = scorer.pick_and_serialize(qname, candidates, OUT_CSV, chosen_dir=CHOSEN_DIR)

        # Compose rich row with baseline actual runtime and whether chosen plan
        # is predicted to be faster than baseline (using baseline's actual_runtime_ms)
        chosen_pred = res.get('chosen_pred_ms')
        try:
            baseline_actual = float(row.get('actual_runtime_ms'))
        except Exception:
            baseline_actual = None

        rich = {
            'query_name': qname,
            'chosen_pred_ms': chosen_pred,
            'baseline_actual_ms': baseline_actual,
            'would_be_faster_than_baseline': (chosen_pred is not None and baseline_actual is not None and chosen_pred < baseline_actual)
        }

        # append row to rich CSV
        import pandas as _pd
        _df = _pd.DataFrame([rich])
        if os.path.exists(OUT_RICH):
            _df.to_csv(OUT_RICH, mode='a', header=False, index=False)
        else:
            _df.to_csv(OUT_RICH, index=False)

        print(f"Processed {qname}: chosen_pred_ms={chosen_pred}")

        # Create an SQL variant file representing the LCM-chosen candidate.
        chosen_plan = res.get('chosen_plan')
        try:
            os.makedirs(OUT_SQL_DIR, exist_ok=True)
            # locate original SQL file in queries/ folders
            orig_path = None
            for sub in ('small', 'medium', 'large'):
                p = os.path.join(ROOT, 'queries', sub, qname)
                if os.path.exists(p):
                    orig_path = p
                    break

            def create_variant_sql(orig_sql_text, chosen, qname):
                # Header comment describing the LCM suggestion
                header = f"-- LCM suggested variant for {qname}\n-- tag: {chosen.get('tag')}\n-- chosen_pred_ms: {res.get('chosen_pred_ms')}\n\n"
                # Naive heuristic: try to reorder JOIN clauses if present
                import re
                m = re.search(r"FROM\s+(.*?)(WHERE|GROUP|ORDER|LIMIT|$)", orig_sql_text, flags=re.IGNORECASE | re.S)
                if not m:
                    return header + orig_sql_text
                from_block = m.group(1)
                tail = orig_sql_text[m.end(1):]
                # split by JOIN keywords
                parts = re.split(r"\bJOIN\b", from_block, flags=re.IGNORECASE)
                if len(parts) <= 1:
                    return header + orig_sql_text
                # trim and reconstruct
                parts = [p.strip() for p in parts if p.strip()]
                # If cheap_variant, reverse join order to encourage different join order
                if chosen.get('tag') == 'cheap_variant':
                    parts = list(reversed(parts))
                new_from = (' JOIN ').join(parts)
                # rebuild SQL
                new_sql = re.sub(re.escape(from_block), new_from, orig_sql_text, count=1)
                return header + new_sql

            if orig_path:
                with open(orig_path, 'r', encoding='utf-8') as f:
                    orig_sql = f.read()
                variant_sql = create_variant_sql(orig_sql, chosen_plan or {}, qname)
            else:
                # no original SQL found; make a small SQL file containing a note
                variant_sql = f"-- Original SQL for {qname} not found in queries/; LCM chosen plan summary:\n{json.dumps(chosen_plan, indent=2)}\n"

            safe_name = qname.replace('/', '_').replace('\\', '_')
            out_sql_path = os.path.join(OUT_SQL_DIR, f"{safe_name}.lcm_variant.sql")
            with open(out_sql_path, 'w', encoding='utf-8') as f:
                f.write(variant_sql)
        except Exception:
            # do not fail the whole run for SQL writing errors; just continue
            pass

    print(f"Wrote generated plan choices to {OUT_CSV} and rich CSV to {OUT_RICH}")


if __name__ == '__main__':
    main()
