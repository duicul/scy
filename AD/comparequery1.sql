EXPLAIN SELECT * FROM people p,course c, grade g,students s WHERE g.SID=s.SID  AND s.SID=c.SID AND p.ID=s.PID ;

SELECT * FROM people p,course c, grade g,students s WHERE g.SID=s.SID  AND s.SID=c.SID AND p.ID=s.PID ;
RESET QUERY CACHE;

EXPLAIN SELECT * FROM people p INNER  JOIN students s ON p.ID=s.PID INNER JOIN  course c ON s.SID=c.SID INNER JOIN  grade g ON g.SID=s.SID;

SELECT * FROM people p INNER  JOIN students s ON p.ID=s.PID INNER JOIN  course c ON s.SID=c.SID INNER JOIN  grade g ON g.SID=s.SID;
RESET QUERY CACHE;