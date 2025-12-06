#run_queries_baseline.py
import os
import json
import time
import psycopg2
import pandas as pd
from tqdm import tqdm
from config import DB_CONFIG, QUERY_DIR, RESULTS_DIR

# This script serves as the traditional/baseline part of the project

#Connect to database
# Double check you configured the config to work on your end for your local database
def get_connection():
    return psycopg2.connect(**DB_CONFIG)


# Run EXPLAIN: this obtains postgres's estimated plan, before running anything. e.g predicted total cost and row count
# Then EXPLAIN ANALYZE:  execute the given query and collect actual runtime and rows processed
def get_query_stats(cursor, query):

    # Explain: Estimated
    cursor.execute(f"EXPLAIN (FORMAT JSON) {query}")
    plan_est = cursor.fetchone()[0][0]
    est_cost = plan_est["Plan"]["Total Cost"]
    est_rows = plan_est["Plan"]["Plan Rows"]

    # EXPLAIN ANAKLYZE: Actual results
    cursor.execute(f"EXPLAIN (ANALYZE, FORMAT JSON) {query}")
    plan_act = cursor.fetchone()[0][0]
    act_runtime = plan_act["Plan"]["Actual Total Time"]
    act_rows = plan_act["Plan"]["Actual Rows"]

    return est_cost, est_rows, act_runtime, act_rows, json.dumps(plan_act)


# Function to count joins, extra to feed into the ML you're making
def count_joins(query):
    return query.upper().count("JOIN") + query.upper().count(",")


# Main data collection 
def collect_results():
    results = []
    conn = get_connection()
    cursor = conn.cursor()

    # Iterate through all queries in all the folders
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
                    "estimated_cost": est_cost,      # Postgres's internal cost estimate
                    "estimated_rows": est_rows,
                    "actual_runtime_ms": act_runtime,  # Measured runtime
                    "actual_rows": act_rows,
                    "join_count": count_joins(query),
                    "execution_time_sec": duration,
                    "plan_json": plan_json            # Full execution plan
                })

            #Error log
            except Exception as e:
                print(f"Error running {qf}: {e}")
                continue

    conn.close()
    return pd.DataFrame(results)


#Run and save results to csv for you to use
def main():
    df = collect_results()
    os.makedirs(os.path.dirname(RESULTS_DIR), exist_ok=True)
    df.to_csv(RESULTS_DIR, index=False)
    print(f"\nResults saved to {RESULTS_DIR}")

if __name__ == "__main__":
    main()

