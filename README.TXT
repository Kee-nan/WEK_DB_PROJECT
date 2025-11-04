⚙️ Setup Instructions
1. Clone the repository

If hosted on GitHub (after you push it):

git clone https://github.com/<your-username>/WEK_DB_PROJECT.git
cd WEK_DB_PROJECT

2. Install dependencies

Create a virtual environment and install required packages:

python -m venv venv
venv\Scripts\activate      # (Windows)
# or
source venv/bin/activate   # (Mac/Linux)

pip install -r requirements.txt

3. Configure the database

Edit scripts/config.py with your database connection details (e.g., PostgreSQL, SQLite, or MySQL).

If you’re using PostgreSQL:

DB_CONFIG = {
    "driver": "PostgreSQL",
    "host": "localhost",
    "user": "your_username",
    "password": "your_password",
    "database": "wek_db"
}

▶️ Running the Queries

Execute all queries (small, medium, and large) and log results:

python -m scripts.run_queries


You should see progress bars for each query set:

Running small queries: 100%|███████████████████████████| 10/10 [00:08<00:00,  1.17it/s]
Running medium queries: 100%|██████████████████████████| 10/10 [00:07<00:00,  1.36it/s]
Running large queries: 100%|███████████████████████████| 11/11 [00:06<00:00,  1.66it/s]

✅ Results saved to results/query_metrics.csv
You can now use this CSV as input for ML model training.

Phase 2 — Data Collection & Baseline Metrics

Goal: Collect ground truth execution data for each query.

Tasks:

Run Queries & Collect Metrics

Use scripts/run_queries.py to execute all queries and record:

Runtime (actual)

Join count

Query category

Save results to /results/query_metrics.csv.

Integrate PostgreSQL Cost Estimates

Modify the script to execute:

EXPLAIN (FORMAT JSON) <query>;


and extract estimated cost and plan node details.

Append these to the results CSV.

Baseline Evaluation

Analyze runtime vs. estimated cost correlation using a simple notebook or Python script.

This establishes the baseline for PostgreSQL’s traditional model accuracy.

Phase 3 — Machine Learning Model (LCM)

Goal: Train a learned cost model to predict query runtime.

Tasks:

Feature Engineering

Extract features such as:

join_count

operator_count

estimated_cost

rows_estimated

query_category

Optionally derive features from JSON plans.

Model Training

Use scikit-learn to train regression models (e.g., Linear Regression, Random Forest, or XGBoost).

Split data into train/test sets.

Model Evaluation

Measure performance using:

Mean Absolute Error (MAE)

Root Mean Squared Error (RMSE)

Pearson Correlation (r)

Compare prediction accuracy against PostgreSQL’s native estimates.

Phase 4 — Hybrid Model Development

Goal: Combine ML predictions and traditional cost estimates intelligently.

Tasks:

Decision Framework

Design a logic layer that decides which estimate to trust:

Use ML estimate when query complexity exceeds a threshold.

Fall back to PostgreSQL cost model otherwise.

Testing Hybrid Approach

Apply both models to each query.

Compare predicted and actual runtimes.

Count how often the hybrid model’s chosen plan yields faster execution.

Visualization

Plot performance comparison (PostgreSQL vs. ML vs. Hybrid).

Use graphs to show runtime improvement percentages.

Phase 5 — Evaluation & Reporting

Goal: Summarize insights and validate project outcomes.

Tasks:

Comprehensive Evaluation

Aggregate statistics on model accuracy and performance improvement.

Identify where ML or hybrid models outperform PostgreSQL.

Interpretability Analysis

Examine feature importance in the ML model (e.g., SHAP values or coefficient weights).

Documentation

Update README.md with:

Model architectures

Experimental setup

Key results

Prepare slides or a brief paper summarizing findings.

How to load database from zip into PostgreSQL
Create an empty target database
createdb -h localhost -p 5432 -U your_pg_user NBA_copy


Or in psql:

CREATE DATABASE NBA_copy;

Restore the custom dump into the DB
pg_restore -h localhost -p 5432 -U your_pg_user -d NBA_copy -v nba_backup.dump