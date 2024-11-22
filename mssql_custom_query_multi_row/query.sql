WITH Numbers AS (
    SELECT TOP 5 ROW_NUMBER() OVER (ORDER BY t1.object_id) AS RowNum
    FROM master.sys.all_columns t1
    CROSS JOIN master.sys.all_columns t2
)
SELECT 
    n.RowNum AS ID,
    GETDATE() AS CurrentDateTime,
    RAND(n.RowNum * 100 + DATEPART(SECOND, GETDATE())) AS RandomNumber,
    NEWID() AS UniqueGUID,
    CAST(CAST(GETDATE() AS FLOAT) AS INT) AS UnixTimestamp,
    CASE WHEN n.RowNum % 2 = 0 THEN 1 ELSE 0 END AS IsEven,
    CONVERT(VARCHAR(50), 'Row ' + CONVERT(VARCHAR(10), n.RowNum)) AS Description
FROM Numbers n;
