# Project Notes

Descisions I made while building this project, and why.

## Extraction

**Counting crimes on the server**

Crime is counted on the server because the dataset has over 8 million records and I only need totals per neighborhood per year.

**Stopping crime data at 2025**

Crime years stop at 2025 because 2026 is still in progress. Including partial year data would give inaccurate results. 

**Dropping crimes with no community area**

Crimes with no community area were dropped because they can't be matched to a neighborhood. The total number of crimes with no community area made around 7% of the total data. 

**Adding population data**

Population lets me calculate crime per 1,000 residents. Raw counts would make large neighborhoods look worse just because the number of people living there is greater.

**Adding a community area lookup table**

The population data identifies neighborhoods by name, while the other datasets use numbers. The lookup table lists both, so I can connect them.

**Checking row counts**

The crime file totals 7.87 million crimes. That matches the full dataset (8.64 million) minus crimes with no community area (about 614,000) minus 2026 so far, so the filters worked as intended. 

## Cleaning

**Keeping only community areas 1-77**

Chicago has 77 community areas, numbered 1-77. The lead data has two extra rows. Row 0 is the citywide total labeled 'chicago', and row 99 is labeled 'unknown', for the kids whose address couldn't be matched to a neighborhood. The citywide row would act as a large neighborhood and distort every average, and the unknown row can't be tied to a location. The crime data also uses 0, but it means no neighborhood was recorded. The Unknown row also showed 75.3% elevated in 2005, far above any real neighborhood (max 9.0%). Dropping it removes that outlier too.

**Treating zero screenings as missing data**

Riverdale (#54) shows zero kids screened in 2003 and 2005. Riverdale is a real neighborhood with families, so this is almost certainly missing data, not a true zero. Left as 0, it would distort Riverdale's lead average.

**Cleaning the socioeconomic data**
The socioeconomic data has a citywide "CHICAGO" row with no community area number or hardship index. Dropped it, then converted `ca` from decimal to integer to match the other datasets (pandas stores the column as decimals when any value is missing). Renamed `per_capita_income_` to remove the trailing underscore left over from the original column name.

**Cleaning the population data**
Converted `total_population` from decimal to integer, since it's a count of people. Every row has `acs_year` 2023, meaning the 2019-2023 five-year estimate, which lines up with the crime window.

**Matching population names to the lookup table**
Checked population names against the lookup table in both directions. All 77 match exactly, so the join needs no name fixes.


## Analysis

**Defining violent crime**

Used the FBI's index crime codes: 01A (murder), 02 (criminal sexual assault), 03 (robbery), 04A (aggravated assault), 04B (aggravated battery). Used `fbi_code` instead of `primary_type` because the same type can span severities (assault appears as both aggravated 04A and simple 08A), and type labels changed over time. Excluded 01B (involuntary manslaughter, no intent) and 08A/08B (simple assault and battery).

**Focusing on violent crime**

The lead hypothesis centers on aggression and impulsivity, so violent crime is what it predicts lead should affect. Property crime may be added later as a comparison. 

# Limitations

**Timing of the socioeconomic data**
The hardship index is from 2008-2012, between the lead period (1999-2003) and the crime period (2019-2023). It's a reasonable snapshot of conditions while those kids were growing up, but neighborhoods may have changed before and after.