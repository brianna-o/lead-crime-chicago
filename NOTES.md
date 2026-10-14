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

## Cleaning

**Keeping only community areas 1-77**

Chicago has 77 community areas, numbered 1-77. The lead data has two extra rows. Row 0 is the citywide total labeled 'chicago', and row 99 is labeled 'unknown', for the kids whose address couldn't be matched to a neighborhood. The citywide row would act as a large neighborhood and distort every average, and the unknown row can't be tied to a location. The crime data also uses 0, but it means no neighborhood was recorded. 

**Treating zero screenings as missing data**

Riverdale (#54) shows zero kids screened in 2003 and 2005. Riverdale is a real neighborhood with families, so this is almost certainly missing data, not a true zero. Left as 0, it would distort Riverdale's lead average. 