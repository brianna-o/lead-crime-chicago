## Childhood Lead Exposure and Crime in Chicago

Does childhood lead exposure in a Chicago neighborhood predict higher crime there about 20 years later, once you account for poverty?

## Questions

1. Do community areas with higher rates of elevated levels of lead in kids (1999-2003) have higher crime rates in 2019-2023?
2. Does that relationship hold after controlling for the hardship index?
3. How does the 20-year lagged relationship compare to a same year baseline?

## Data

All data from the [Chicago Data Portal](https://data.cityofchicago.org), listed on data.gov:

- Blood lead screening, kids 0-6, by community area, 1999-2013
- Crimes, 2001 to present
- Socioeconomic indicators and hardship index, 2008-2012

## Setup

'''bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
'''

## Limitations

- Only 77 community areas, so the sample is small.
- Area-level data can't say anything about the individuals
- People move, so kids tested in a neighborhood in 2000 don't all live there in 2020. 
- "Elevated" meant 10 µg/dl in this data. The CDC threshold is now 3.5.
- Crime data reflects reported crime, which depends partly on where police patrol.


## Findings

In progress.