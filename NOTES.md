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

**Using one name for the community area number**
Each source named it differently: `community_area_number` (lead), `community_area` (crime), `ca` (socioeconomic), and `area_numbe` (lookup). Renamed all of them to `community_area_number` so every cleaned file joins on the same column name.

**Keeping only community areas 1-77**

Chicago has 77 community areas, numbered 1-77. The lead data has two extra rows. Row 0 is the citywide total labeled 'chicago', and row 99 is labeled 'unknown', for the kids whose address couldn't be matched to a neighborhood. The citywide row would act as a large neighborhood and distort every average, and the unknown row can't be tied to a location. The crime data also uses 0, but it means no neighborhood was recorded. The Unknown row also showed 75.3% elevated in 2005, far above any real neighborhood (max 9.0%). Dropping it removes that outlier too.

**Treating zero screenings as missing data**

Riverdale (#54) shows zero kids screened in 2003 and 2005. Riverdale is a real neighborhood with families, so this is almost certainly missing data, not a true zero. Left as 0, it would distort Riverdale's lead average.

**Cleaning the socioeconomic data**
The socioeconomic data has a citywide "CHICAGO" row with no community area number or hardship index. Dropped it, then converted `ca` from decimal to integer to match the other datasets (pandas stores the column as decimals when any value is missing). Renamed `per_capita_income_` to remove the trailing underscore left over from the original column name.

**Cleaning the population data**
Merged population with the lookup table on neighborhood name to attach area numbers. Renamed both name columns to `community_area_name` first, so the merge could match on one shared column. Converted `total_population` from decimal to integer, since it's a count of people. Kept only the area number and population. Every row is the 2023 ACS estimate (2019-2023), which lines up with the crime window.

**Matching population names to the lookup table**
Checked population names against the lookup table in both directions. All 77 match exactly, so the join needs no name fixes.

**Dropping 2001 and 2002 crime data**
After cleaning, four neighborhoods (Forest Glen, North Park, Armour Square, Hegewisch) had no violent crime in 2001. All four were missing the same year, which pointed to a data issue rather than no violent crime committed. Checking the source showed community area was missing for about 99% of 2001 crimes and 27% of 2002 crimes, compared with under 250 per year from 2003 on. Their 2001 crimes just weren't tagged with a neighborhood. Dropped both years, so cleaned crime data covers 2003-2025.

**Filtering to violent crime and adding it up**
Kept only the violent crime codes (see Analysis), then added up incidents per neighborhood per year. The cleaned crime file has one row per neighborhood per year: 77 neighborhoods x 23 years = 1,771 rows.

**Keeping all crime years in the cleaned file**
Didn't filter to 2019-2023 during cleaning. Choosing a time window is an analysis decision, and the same-year baseline needs earlier years too.

**Checking each output**
Each cleaning function checks its result before returning it: 77 rows for socioeconomic and population, and 77 neighborhoods and 1,771 rows for crime. If the source data ever changes and breaks an assumption, the script stops with a message instead of saving bad data.


## Analysis

**Defining violent crime**

Used the FBI's index crime codes: 01A (murder), 02 (criminal sexual assault), 03 (robbery), 04A (aggravated assault), 04B (aggravated battery). Used `fbi_code` instead of `primary_type` because the same type can span severities (assault appears as both aggravated 04A and simple 08A), and type labels changed over time. Excluded 01B (involuntary manslaughter, no intent) and 08A/08B (simple assault and battery).

**Focusing on violent crime**

The lead hypothesis centers on aggression and impulsivity, so violent crime is what it predicts lead should affect. Property crime may be added later as a comparison. 

**Same-year baseline window**
Originally planned to compare lead 1999-2003 with crime 2001-2003. Since usable crime data starts in 2003, the baseline will use lead 2003-2007 vs. crime 2003-2007 instead. That still compares the same years, which is all the baseline needs.


# Limitations

**Timing of the socioeconomic data**
The hardship index is from 2008-2012, between the lead period (1999-2003) and the crime period (2019-2023). It's a reasonable snapshot of conditions while those kids were growing up, but neighborhoods may have changed before and after.

**Crime data starts in 2003**
Community area wasn't recorded reliably in 2001-2002, so crime by neighborhood is only usable from 2003 on.