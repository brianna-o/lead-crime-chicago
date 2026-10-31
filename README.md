## Childhood Lead Exposure and Violent Crime in Chicago

Do Chicago neighborhoods with higher childhood lead exposure have higher violent crime rates?

## Questions

1. Do community areas with higher rates of elevated levels of lead in kids have higher violent crime rates years later, when those kids are young adults?
2. Does that relationship hold with neighborhoods of similar hardship levels?
3. How does the multiple year lagged relationship compare to a same year baseline?

## Data

All data from the [Chicago Data Portal](https://data.cityofchicago.org), listed on data.gov. Every dataset joins on Chicago's 77 community areas. 

| Dataset | ID | Years | Used for |
|---|---|---|---|
| Blood lead screening, kids 0-6 | `v2z5-jyrq` | 1999-2013 | Childhood lead exposure |
| Crimes, 2001 to present | `ijzp-q8t2` | 2001-2025 | Violent crime counts |
| Socioeconomic indicators | `kn9c-c2s2` | 2008-2012 | Hardship index (poverty control) |
| ACS 5-year data by community area | `t68z-cikk` | 2019-2023 | Population, for crime rates |
| Community area boundaries | `igwz-8jzy` | n/a | Matching neighborhood names to numbers |

Crime data before 2003 is excluded because community area was missing for about 99% of 2001 crimes and 27% of 2002 crimes.

Violent crime uses the FBI's index crime codes: murder, criminal sexual assault, robbery, aggravated assault, and aggravated battery.

### Cleaned data

| File | Rows | One row per |
|---|---|---|
| `blood_lead.csv` | 1,155 | neighborhood per year (1999-2013) |
| `crimes_by_area_year.csv` | 1,771 | neighborhood per year (2003-2025) |
| `socioeconomic.csv` | 77 | neighborhood |
| `population.csv` | 77 | neighborhood |

All four use `community_area_number` as the shared key.

## Project structure

```
lead-crime-chicago/
├── data/
│   ├── raw/            # API pulls, untouched (not tracked in git)
│   └── processed/      # cleaned data (not tracked in git)
├── notebooks/
│   ├── 01_explore.ipynb        # data quality checks on all five datasets
│   └── 02_lead_reshape.ipynb   # prototype of the lead reshape
├── sql/
├── src/
│   └── extract.py      # pulls all five datasets from the API
│   └── transform.py    # cleans and standardizes the raw data
├── NOTES.md            # decisions made along the way, and why
├── README.md
└── requirements.txt
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/extract.py
python src/transform.py
```

`extract.py` saves the raw data to `data/raw/`. The crime data is counted by year, neighborhood, and crime type on the API's server, so it downloads about 64,000 summary rows instead of 8 million individual records.

`transform.py` cleans each dataset and saves the results to `data/processed/`.


## Limitations

- **Small sample.** 77 community areas, so results will have wide margins of error.
- **Area-level data.** This can show whether neighborhoods with more lead exposure have more crime. It can't say anything about individuals.
- **People move.** Kids tested in a neighborhood in 2000 don't all live there in 2020.
- **Changing definition of "elevated."** This data uses 10 µg/dL. The CDC reference value is now 3.5 µg/dL.
- **Reported crime.** Police data reflects crimes that were reported and recorded, which depends partly on where police patrol.
- **Timing of the hardship index.** It covers 2008-2012, between the lead and crime periods. Neighborhoods may have changed before and after.
- **Crime data starts in 2003.** Community area wasn't recorded reliably before then, so earlier crime can't be assigned to neighborhoods.
- **Riverdale has no lead data after 2002.** Its 1999-2003 average uses four years, and it's left out of the same-year baseline, which covers 76 neighborhoods.

## Findings

In progress.