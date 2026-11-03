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

**Cleaning the socioeconomic data**
The socioeconomic data has a citywide "CHICAGO" row with no community area number or hardship index. Dropped it, then converted the area number from decimal to integer to match the other datasets (pandas stores the column as decimals when any value is missing, so the row has to be dropped first). Renamed `per_capita_income_` to remove the trailing underscore left over from the original column name.

**Cleaning the population data**
Merged population with the lookup table on neighborhood name to attach area numbers. Renamed both name columns to `community_area_name` first, so the merge could match on one shared column. Converted `total_population` from decimal to integer, since it's a count of people. Kept only the area number and population. Every row is the 2023 ACS estimate (2019-2023), which lines up with the crime window.

**Matching population names to the lookup table**
Checked population names against the lookup table in both directions. All 77 match exactly, so the join needs no name fixes.

**Dropping 2001 and 2002 crime data**
After cleaning, four neighborhoods (Forest Glen, North Park, Armour Square, Hegewisch) had no violent crime in 2001. All four were missing the same year, which pointed to a data issue rather than no violent crime committed. Checking the source showed community area was missing for about 99% of 2001 crimes and 27% of 2002 crimes, compared with under 250 per year from 2003 on. Their 2001 crimes just weren't tagged with a neighborhood. Dropped both years, so cleaned crime data covers 2003-2025.

**Filtering to violent crime and adding it up**
Kept only the violent crime codes (see Analysis), then added up incidents per neighborhood per year. The cleaned crime file has one row per neighborhood per year: 77 neighborhoods x 23 years = 1,771 rows.

**Reshaping the lead data**
Kept only `screened_for_lead_in` and `percent_elevated` for each year, since the screening rates and confidence intervals aren't used in the analysis. Reshaped from one row per neighborhood with 30 year columns to one row per neighborhood per year (77 x 15 = 1,155 rows), matching the crime data's grain. Built the column names with code instead of filtering by prefix, because the confidence interval columns share the same prefix.

**Riverdale has no lead data after 2002**
Riverdale (#54) has zero screenings recorded for every year from 2003-2013. Converted these zeros to missing in both measures. Its 1999-2003 average uses four years (1999-2002). It has no lead data in 2003-2007, so it's excluded from the same-year baseline, which covers 76 neighborhoods.

**Data types after reshaping**
The year pulled from column names came out as text, so converted it to integer to match the crime data. Otherwise joins on year would fail. Used `Int64` (capital I) for kids screened, which allows whole numbers and missing values.

**Keeping all lead years in the cleaned file**
Didn't average 1999-2003 during cleaning. Like crime, the time window is an analysis decision, and the same-year baseline needs 2003-2007.

**Checking each output**
Each cleaning function checks its result before returning it: 77 rows for socioeconomic and population, 77 neighborhoods and 1,771 rows for crime, and 77 neighborhoods and 1,155 rows for lead. If the source data ever changes and breaks an assumption, the script stops with a message instead of saving 
bad data.


## Loading

**Using DuckDB**
Loaded the four cleaned CSVs into a DuckDB database so the analysis could be written in SQL. DuckDB runs from a single file in the project, with no server to set up.

**Checking types after loading**
`read_csv_auto` guesses column types, so checked them with `DESCRIBE`. Year is an integer in both lead and crime, so they join correctly, and Riverdale's 11 missing values came through as NULL.

**Opening the database read-only in the notebook**
The analysis notebook connects with `read_only=True`, so analysis can't accidentally change the data.


## Analysis

**Defining violent crime**

Used the FBI's index crime codes: 01A (murder), 02 (criminal sexual assault), 03 (robbery), 04A (aggravated assault), 04B (aggravated battery). Used `fbi_code` instead of `primary_type` because the same type can span severities (assault appears as both aggravated 04A and simple 08A), and type labels changed over time. Excluded 01B (involuntary manslaughter, no intent) and 08A/08B (simple assault and battery).

**Focusing on violent crime**

The lead hypothesis centers on aggression and impulsivity, so violent crime is what it predicts lead should affect. Property crime may be added later as a comparison. 

**Crime rate per 1,000 residents per year**
Divided total violent crimes for 2019-2023 by 5 years, then by population, times 1,000. Dividing by exactly 5 works because every neighborhood has all five years of crime data, confirmed by the 1,771-row check in cleaning. Used 5.0 instead of 5 so the division keeps decimals in any SQL database.

**Averaging lead exposure**
Averaged percent elevated over 1999-2003 per neighborhood. SQL's `AVG()` skips NULLs, so Riverdale is averaged over its 4 years with data. Also counted the years with data per neighborhood to confirm it.

**Combining everything in one query**
Used CTEs (`WITH`) to build lead exposure and crime rates as separate steps, then joined them with the hardship index into one row per neighborhood. Saved the query in `sql/01_neighborhood_summary.sql` instead of leaving it in a notebook cell.

**Checking the result with Spearman's correlation**
The scatter plot fans out, and Fuller Park sits at the extreme. Pearson's correlation can be pulled by extreme values, so also ran Spearman's, which only uses rank order. Both gave 0.89, so the result isn't driven by a few neighborhoods.

**Testing within hardship groups**
Split neighborhoods into three equal-sized groups by hardship index (26, 25, and 26 neighborhoods) and calculated the lead-crime correlation within each, using Spearman because each group is small. If poverty explained the relationship, it should weaken a lot among neighborhoods with similar hardship. It stayed strong (0.83-0.87).

**Same-year baseline window**
Originally planned to compare lead 1999-2003 with crime 2001-2003. Since usable crime data starts in 2003, the baseline uses lead 2003-2007 vs. crime 2003-2007 instead. A later window like 2009-2013 would align better with the hardship index, but lead levels fell so much by then that many neighborhoods are near 0%, which leaves less variation to compare.

**Dropping Riverdale from the baseline**
Riverdale has no lead data from 2003 on, so its 2003-2007 average is NULL. Dropped it before calculating correlations, since `pearsonr` returns nothing useful when given a missing value. No window works for Riverdale: its lead data ends in 2002, and crime data starts in 2003.


# Limitations

**Timing of the socioeconomic data**
The hardship index is from 2008-2012, between the lead period (1999-2003) and the crime period (2019-2023). It's a reasonable snapshot of conditions while those kids were growing up, but neighborhoods may have changed before and after.

**Crime data starts in 2003**
Community area wasn't recorded reliably in 2001-2002, so crime by neighborhood is only usable from 2003 on.

**Small populations make some rates unstable**
Some neighborhoods have very few residents. Fuller Park has the highest violent crime rate (51.0) but only about 2,200 people, so a few incidents move its rate a lot.

**Population timing in the baseline**
The only population data by community area is the 2019-2023 estimate, so the 2003-2007 baseline divides older crime counts by more recent population. Neighborhood populations shifted somewhat over those years.

**Riverdale's lead data**
Riverdale's lead data ends after 2002, and it's also the biggest exception to the pattern (low lead, high crime, highest hardship). Its exposure value is less certain than other neighborhoods'.

**What the hardship index doesn't measure**
The hardship index covers income, poverty, unemployment, education, crowding, and age. It doesn't capture housing age and condition, historical segregation, or long-term disinvestment, which are closely tied to where lead exposure was highest. Lead may partly be standing in for those factors.

**Neighborhood stability over time**
The same neighborhoods had high lead and high crime in 2003-2007 and still had high crime in 2019-2023. Comparing neighborhoods can't separate a delayed effect of childhood lead exposure from places that stayed disadvantaged across decades.