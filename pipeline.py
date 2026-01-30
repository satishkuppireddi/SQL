import duckdb
import pandas as pd

# --- AGENTIC NOTE ---
# This script was optimized using AI-assisted coding (Cursor/Copilot) 
# to handle schema inference and high-performance Window Functions.

def run_insurance_pipeline():
    print("🚀 Starting Insurance Data Pipeline...")

    # 1. Connect to DuckDB (In-memory)
    con = duckdb.connect(database=':memory:')

    # 2. Load the 'Dirty' CSV
    # DuckDB automatically handles the messy headers
    con.execute("CREATE TABLE raw_insurance AS SELECT * FROM read_csv_auto('dirty_insurance_data.csv')")

    # 3. The Transformation Logic (SQL)
    # We use a CTE to deduplicate and clean in one high-performance step
    transformation_sql = """
    WITH CleanedData AS (
        SELECT 
            UPPER(TRIM(Client_Name)) AS Client_Name,
            Policy_Type,
            CAST(REPLACE(REPLACE(REPLACE(Premium, '£', ''), '$', ''), ',', '') AS DECIMAL(10,2)) AS Premium_Amount,
            strptime(Start_Date, '%d-%b-%Y') AS Policy_Start_Date, -- Standardizing dates
            COALESCE(Claims_Paid, 0) AS Claims_Paid,
            Region,
            ROW_NUMBER() OVER(PARTITION BY Policy_ID ORDER BY Start_Date DESC) as rank
        FROM raw_insurance
    )
    SELECT * EXCLUDE(rank) FROM CleanedData WHERE rank = 1
    """

    # 4. Execute and Export
    print("🧹 Cleaning and Deduplicating data...")
    df_cleaned = con.execute(transformation_sql).df()
    
    # Save to a professional format (Parquet is better than CSV for 2026)
    df_cleaned.to_parquet('cleaned_insurance_data.parquet')
    print("✅ Success! Cleaned data saved to 'cleaned_insurance_data.parquet'.")

if __name__ == "__main__":
    run_insurance_pipeline()