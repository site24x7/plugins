SELECT * 
FROM (SELECT sql_text, 
             cpu_time, 
             executions 
      FROM v$sql 
      ORDER BY cpu_time DESC) 
WHERE ROWNUM <= 15
