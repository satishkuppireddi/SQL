"Standardizing Names and Money "
SELECT 
    UPPER(TRIM(Client_Name)) AS Cleaned_Name,
    Policy_Type,
    -- Remove '£', '$', and ',' then convert to numeric
    CAST(REPLACE(REPLACE(REPLACE(Premium, '£', ''), '$', ''), ',', '') AS DECIMAL(10,2)) AS Premium_Amount
FROM insurance_table;

"Deduplication"
WITH DeDuplicated AS (
    SELECT *,
           ROW_NUMBER() OVER(PARTITION BY Policy_ID ORDER BY Start_Date DESC) as row_num
    FROM insurance_table
)
SELECT * FROM DeDuplicated WHERE row_num = 1;

"The Risk Ratio"

SELECT 
    Region,
    SUM(COALESCE(Claims_Paid, 0)) AS Total_Claims,
    SUM(CAST(REPLACE(Premium, '£', '') AS DECIMAL)) AS Total_Premium,
    ROUND(SUM(COALESCE(Claims_Paid, 0)) / SUM(CAST(REPLACE(Premium, '£', '') AS DECIMAL)) * 100, 2) AS Loss_Ratio_Percentage
FROM insurance_table
GROUP BY Region
HAVING Loss_Ratio_Percentage > 20;
