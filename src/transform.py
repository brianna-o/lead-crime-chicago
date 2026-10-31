import pandas as pd
from pathlib import Path

# Creating input folder (raw data) and output folder (cleaned data) paths.
RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"

# Clean socioeconomic.csv:
# - Remove the trailing underscore from per_capita_income and standardize community_area_number column name.
# - Keep areas 1-77 (drops the citywide row).
# - Convert community_area_number to int to match the other datasets.
# - Insert script check to alert if dataset is not expected size.
def clean_socioeconomic():
    socio = pd.read_csv(RAW_DIR / "socioeconomic.csv")
    socio = socio.rename(columns={"per_capita_income_": "per_capita_income", "ca": "community_area_number"})
    socio = socio[socio["community_area_number"].between(1, 77)]
    socio["community_area_number"] = socio["community_area_number"].astype(int)
    assert len(socio) == 77, f"Expected 77 rows, got {len(socio)}"
    return socio

# Clean population.csv:
# - Standardize column names to prepare for merge.
# - Population identifies neighborhoods by name, so merge with the lookup table to attach area numbers.
# - Convert total_population to int, since it's a count of people.
# - Keep only the number and population, the two columns needed for crime rates.
# - Insert script check to alert if dataset is not expected size.
def clean_population():
    pop = pd.read_csv(RAW_DIR / "population.csv")
    cal = pd.read_csv(RAW_DIR / "community_area_lookup.csv")
    pop = pop.rename(columns={"community_area": "community_area_name"})
    cal = cal.rename(columns={"community": "community_area_name", "area_numbe": "community_area_number"})
    pop["total_population"] = pop["total_population"].astype(int)
    popcal = pd.merge(pop,cal, on="community_area_name", how ="inner")
    popcal = popcal[["community_area_number", "total_population"]]
    assert len(popcal) == 77, f"Expected 77 rows after merge, got {len(popcal)}"
    return popcal

# Clean crimes_by_area_year.csv:
# - Standardize community_area_number column name.
# - Keep areas 1-77 (drops area 0, crimes with no associated neighborhood).
# - Keep years 2003-2025 (community area was missing for most crimes in 2001-2002).
# - Narrow down data to only violent crimes.
# - Add up violent crimes per neighborhood per year (one row per area-year).
# - Insert script check to alert if dataset is not expected size.
def clean_crimes():
    crimes = pd.read_csv(RAW_DIR / "crimes_by_area_year.csv")
    crimes = crimes.rename(columns={"community_area": "community_area_number"})
    crimes = crimes[crimes["community_area_number"].between(1, 77)]
    crimes = crimes[crimes["year"].between(2003, 2025)]
    violent_crime_codes = ["01A", "02", "03", "04A", "04B"]
    crimes = crimes[crimes["fbi_code"].isin(violent_crime_codes)]
    crimes = crimes.groupby(["community_area_number", "year"])["incidents"].sum().reset_index()
    crimes = crimes.rename(columns={"incidents": "violent_crime_incidents"})
    assert crimes["community_area_number"].nunique() == 77, f"Expected 77 areas, got {crimes['community_area_number'].nunique()}"
    assert len(crimes) == 1771, f"Expected 1771 rows (77 areas x 23 years), got {len(crimes)}"
    return crimes

# Clean blood_lead.csv:
# - Keep areas 1-77 (drops the citywide total #0 and Unknown #99).
# - Keep only kids screened and percent elevated, the two measures the analysis needs.
# - Reshape from one row per neighborhood (one column per year) to one row per neighborhood per year.
# - Convert zero screenings to missing (Riverdale has none recorded 2003-2013).
# - Use Int64 for kids_screened so it can hold whole numbers and missing values.
def clean_lead():
    lead = pd.read_csv(RAW_DIR / "blood_lead.csv")
    lead = lead[lead["community_area_number"].between(1, 77)]
    screened_cols = [f"screened_for_lead_in_{year}" for year in range(1999, 2014)]
    elevated_cols = [f"percent_elevated_{year}" for year in range(1999, 2014)]
    keep_cols = ["community_area_number"] + screened_cols + elevated_cols
    lead = lead[keep_cols]
    long = lead.melt(id_vars=["community_area_number"], var_name="column", value_name="value")
    long["year"] = long["column"].str[-4:].astype(int)
    long["measure"] = long["column"].str[:-5]
    lead_long = long.pivot(index=["community_area_number", "year"], columns="measure", values="value").reset_index()
    lead_long = lead_long.rename(columns={"screened_for_lead_in":"kids_screened"})
    lead_long.columns.name = None
    zero_screened = lead_long["kids_screened"] == 0
    lead_long.loc[zero_screened, ["kids_screened", "percent_elevated"]] = pd.NA
    lead_long["kids_screened"] = lead_long["kids_screened"].astype("Int64")
    assert lead_long["community_area_number"].nunique() == 77, f"Expected 77 areas, got {lead_long['community_area_number'].nunique()}"
    assert len(lead_long) == 1155, f"Expected 1155 rows (77 areas x 15 years), got {len(lead_long)}"
    return lead_long

# Clean each dataset and save to data/processed. 
if __name__ == "__main__":
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    socio = clean_socioeconomic()
    socio.to_csv(PROCESSED_DIR / "socioeconomic.csv", index=False)

    pop = clean_population()
    pop.to_csv(PROCESSED_DIR / "population.csv", index=False)

    crimes = clean_crimes()
    crimes.to_csv(PROCESSED_DIR / "crimes_by_area_year.csv", index=False)

    lead = clean_lead()
    lead.to_csv(PROCESSED_DIR / "blood_lead.csv", index=False)

    print(f"Saved socioeconomic: {socio.shape}")
    print(f"Saved population: {pop.shape}")
    print(f"Saved crimes_by_area_year: {crimes.shape}")
    print(f"Saved blood_lead: {lead.shape}")