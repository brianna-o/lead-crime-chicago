import duckdb
from pathlib import Path

# Define paths for the project directory, processed data, and the DuckDB database file.
PROJECT_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
DB_PATH = PROJECT_DIR / "data" / "lead_crime.duckdb"

# Load each cleaned CSV into its own DuckDB table, then confirm the row counts
if __name__ == "__main__":
    con = duckdb.connect(str(DB_PATH))

    lead_path = PROCESSED_DIR / "blood_lead.csv"
    con.execute(f"CREATE OR REPLACE TABLE lead AS SELECT * FROM read_csv_auto('{lead_path}')")

    crime_path = PROCESSED_DIR / "crimes_by_area_year.csv"
    con.execute(f"CREATE OR REPLACE TABLE crime AS SELECT * FROM read_csv_auto('{crime_path}')")

    socio_path = PROCESSED_DIR / "socioeconomic.csv"
    con.execute(f"CREATE OR REPLACE TABLE socio AS SELECT * FROM read_csv_auto('{socio_path}')")

    population_path = PROCESSED_DIR / "population.csv"
    con.execute(f"CREATE OR REPLACE TABLE population AS SELECT * FROM read_csv_auto('{population_path}')")

    for table in ["lead", "crime", "socio", "population"]:
        count = con.sql(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"{table}: {count} rows")

    con.close()
