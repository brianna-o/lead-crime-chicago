import pandas as pd
from pathlib import Path

# Creating input folder (raw data) and output folder (cleaned data) paths.
RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"

# Clean socioeconomic.csv:
# Remove the trailing underscore from per_capita_income, Keep areas 1-77 (drops the citywide row), and convert ca to int to match the other datasets.
def clean_socioeconomic():
    df = pd.read_csv(RAW_DIR / "socioeconomic.csv")
    df = df.rename(columns={"per_capita_income_": "per_capita_income"})
    df = df[df["ca"].between(1, 77)]
    df["ca"] = df["ca"].astype(int)
    return df

# Clean each dataset and save to data/processed. 
if __name__ == "__main__":
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    socio = clean_socioeconomic()
    socio.to_csv(PROCESSED_DIR / "socioeconomic.csv", index=False)
    print(f"Saved socioeconomic: {socio.shape}")