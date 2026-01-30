SELECT 
    Region,
    SUM(COALESCE(Claims_Paid, 0)) AS Total_Claims,
    SUM(CAST(REPLACE(Premium, '£', '') AS DECIMAL)) AS Total_Premium,
    ROUND(SUM(COALESCE(Claims_Paid, 0)) / SUM(CAST(REPLACE(Premium, '£', '') AS DECIMAL)) * 100, 2) AS Loss_Ratio_Percentage
FROM insurance_table
GROUP BY Region
HAVING Loss_Ratio_Percentage > 20;
