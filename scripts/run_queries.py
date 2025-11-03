import os
import json
import time
import psycopg2
import pandas as pd
from tqdm import tqdm
from config import DB_CONFIG, QUERY_DIR, RESULTS_DIR

# --------------------------------------------------------------------
# Hybrid Optimizer Study - Data Collection Phase
# --------------------------------------------------------------------
# This script represents the "Traditional Model" part of the project.
# It connects to PostgreSQL, runs EXPLAIN and EXPLAIN ANALYZE for each
# query, and logs both the optimizer’s estimated costs and actual runtimes.
# These metrics will later be used to train and evaluate a Learned Cost Model (LCM)
# and a Hybrid Model that decides when to rely on ML vs. PostgreSQL estimates.
# --------------------------------------------------------------------

# -----------------------------
# Connect to PostgreSQL
# -----------------------------
def get_connection():
    """
    Establishes a connection to PostgreSQL using credentials
    defined in config.py. This allows Python to send queries and
    retrieve plan/cost information directly from the optimizer.
    """
    return psycopg2.connect(**DB_CONFIG)

# -----------------------------
# Run EXPLAIN and EXPLAIN ANALYZE
# -----------------------------
def get_query_stats(cursor, query):
    """
    For a single SQL query:
    1. Run EXPLAIN (FORMAT JSON) to obtain PostgreSQL’s *estimated* plan,
       which contains predicted total cost and row count.
    2. Run EXPLAIN (ANALYZE, FORMAT JSON) to execute the query and collect
       the *actual* runtime and rows processed.
    This lets us directly compare the optimizer’s expectations vs. reality.
    """

    # Step 1: Retrieve PostgreSQL's estimated plan (traditional model output)
    cursor.execute(f"EXPLAIN (FORMAT JSON) {query}")
    plan_est = cursor.fetchone()[0][0]  # returns JSON array → extract dict
    est_cost = plan_est["Plan"]["Total Cost"]
    est_rows = plan_est["Plan"]["Plan Rows"]

    # Step 2: Retrieve actual execution time and rows processed
    cursor.execute(f"EXPLAIN (ANALYZE, FORMAT JSON) {query}")
    plan_act = cursor.fetchone()[0][0]
    act_runtime = plan_act["Plan"]["Actual Total Time"]
    act_rows = plan_act["Plan"]["Actual Rows"]

    # Return both estimated and observed values
    return est_cost, est_rows, act_runtime, act_rows, json.dumps(plan_act)

# -----------------------------
# Count number of joins
# -----------------------------
def count_joins(query):
    """
    Simple heuristic to count how many tables are being joined.
    Used later as a feature for the ML model (complexity indicator).
    Counts explicit JOINs and implicit commas in FROM clauses.
    """
    return query.upper().count("JOIN") + query.upper().count(",")

# -----------------------------
# Main Data Collection Routine
# -----------------------------
def collect_results():
    """
    Iterates through all queries in the 'queries/' directory, grouped by category:
        - small (2–3 joins)
        - medium (4–5 joins)
        - large (6+ joins)
    For each query:
        - Collects estimated vs. actual metrics
        - Measures execution duration
        - Stores the full JSON plan for future analysis
    Returns a DataFrame ready for export to CSV.
    """
    results = []
    conn = get_connection()
    cursor = conn.cursor()

    for category in ["small", "medium", "large"]:
        path = os.path.join(QUERY_DIR, category)
        if not os.path.exists(path):
            continue

        query_files = [f for f in os.listdir(path) if f.endswith(".sql")]
        for qf in tqdm(query_files, desc=f"Running {category} queries"):
            query_path = os.path.join(path, qf)
            with open(query_path, "r") as f:
                query = f.read().strip()

            try:
                start = time.time()
                est_cost, est_rows, act_runtime, act_rows, plan_json = get_query_stats(cursor, query)
                duration = time.time() - start

                # Store relevant data for both ML training and baseline analysis
                results.append({
                    "query_name": qf,
                    "category": category,
                    "estimated_cost": est_cost,      # PostgreSQL's internal cost estimate
                    "estimated_rows": est_rows,
                    "actual_runtime_ms": act_runtime,  # Measured runtime (ground truth)
                    "actual_rows": act_rows,
                    "join_count": count_joins(query),
                    "execution_time_sec": duration,
                    "plan_json": plan_json            # Full execution plan for reference
                })

            except Exception as e:
                print(f"❌ Error running {qf}: {e}")
                continue

    conn.close()
    return pd.DataFrame(results)

# -----------------------------
# Save results to CSV
# -----------------------------
def main():
    """
    Executes the data collection process and writes results to a CSV file.
    The CSV will serve as the core dataset for training and evaluating
    Learned Cost Models and the hybrid approach.
    """
    df = collect_results()
    os.makedirs(os.path.dirname(RESULTS_DIR), exist_ok=True)
    df.to_csv(RESULTS_DIR, index=False)
    print(f"\n✅ Results saved to {RESULTS_DIR}")
    print("You can now use this CSV as input for ML model training.")

if __name__ == "__main__":
    main()

