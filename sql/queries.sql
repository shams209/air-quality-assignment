-- Query to find the average AQI per city
SELECT City, AVG(AQI) as avg_aqi 
FROM air_quality 
GROUP BY City 
ORDER BY avg_aqi DESC;