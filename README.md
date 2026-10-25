## Childhood Lead Exposure and Violent Crime in Chicago

Do Chicago neighborhoods with higher childhood lead exposure around 2000 have higher violent crime about 20 years later, once you account for poverty?

## Questions

1. Do community areas with higher rates of elevated levels of lead in kids (1999-2003) have higher violent crime rates in 2019-2023, when those kids are young adults?
2. Does that relationship hold with neighborhoods of similar hardship levels?
3. How does the 20-year lagged relationship compare to a same year baseline?

## Data

All data from the [Chicago Data Portal](https://data.cityofchicago.org), listed on data.gov. Every dataset joins on Chicago's 77 community areas. 

| Dataset | ID | Years | Used for |
|---|---|---|---|
| Blood lead screening, kids 0-6 | `v2z5-jyrq` | 1999-2013 | Childhood lead exposure |
| Crimes, 2001 to present | `ijzp-q8t2` | 2001-2025 | Violent crime counts |
| Socioeconomic indicators | `kn9c-c2s2` | 2008-2012 | Hardship index (poverty control) |
| ACS 5-year data by community area | `t68z-cikk` | 2019-2023 | Population, for crime rates |
| Community area boundaries | `igwz-8jzy` | n/a | Matching neighborhood names to numbers |

Violent crime uses the FBI's index crime codes: murder, criminal sexual assault, robbery, aggravated assault, and aggravated battery.

## Project structure

```
lead-crime-chicago/
├── data/
│   ├── raw/            # API pulls, untouched (not tracked in git)
│   └── processed/      # cleaned data (not tracked in git)
├── notebooks/
│   └── 01_explore.ipynb
├── sql/
├── src/
│   └── extract.py      # pulls all five datasets from the API
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
```

`extract.py` saves the raw data to `data/raw/`. The crime data is counted by year, neighborhood, and crime type on the API's server, so it downloads about 64,000 summary rows instead of 8 million individual records.


## Limitations

- **Small sample.** 77 community areas, so results will have wide margins of error.
- **Area-level data.** This can show whether neighborhoods with more lead exposure have more crime. It can't say anything about individuals.
- **People move.** Kids tested in a neighborhood in 2000 don't all live there in 2020.
- **Changing definition of "elevated."** This data uses 10 µg/dL. The CDC reference value is now 3.5 µg/dL.
- **Reported crime.** Police data reflects crimes that were reported and recorded, which depends partly on where police patrol.
- **Timing of the hardship index.** It covers 2008-2012, between the lead and crime periods. Neighborhoods may have changed before and after.

## Findings

In progress.