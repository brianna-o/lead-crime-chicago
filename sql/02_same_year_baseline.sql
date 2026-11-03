-- One row per neighborhood: childhood lead exposure (2003-2007),
-- violent crime rate (2003-2007), and hardship index.

WITH lead_exposure AS (
    SELECT
        community_area_number,
        ROUND(AVG(percent_elevated), 2) AS lead_2003_2007,
        COUNT(percent_elevated) AS years_with_data
    FROM lead
    WHERE year BETWEEN 2003 AND 2007
    GROUP BY community_area_number
),
crime_rates AS (
    SELECT
        crime.community_area_number,
        total_population,
        SUM(violent_crime_incidents) AS total_violent_crimes,
        ROUND(SUM(violent_crime_incidents) / 5.0 / total_population * 1000, 1) AS violent_crime_rate_2003_2007
    FROM crime
    JOIN population ON crime.community_area_number = population.community_area_number
    WHERE year BETWEEN 2003 AND 2007
    GROUP BY crime.community_area_number, total_population
)
SELECT
    community_area_number,
    socio.community_area_name,
    lead_2003_2007,
    violent_crime_rate_2003_2007,
    hardship_index
FROM lead_exposure
JOIN crime_rates USING (community_area_number)
JOIN socio USING (community_area_number)
ORDER BY violent_crime_rate_2003_2007 DESC