/*SET SQL_WARNINGS = 1;*/
/*EXPLAIN SELECT * FROM people p WHERE p.NAME='John';
SHOW WARNINGS;
RESET QUERY CACHE;
EXPLAIN SELECT * FROM people p WHERE p.SURNAME='Smith';
SHOW WARNINGS;
RESET QUERY CACHE;*/

EXPLAIN SELECT * FROM people p,course c, grade g,students s 
WHERE p.ID=s.sid AND c.SID=s.sid AND g.sid=s.sid 
	AND g.GRADE=(SELECT g.grade FROM grade g GROUP BY g.GRADE ORDER BY g.GRADE DESC LIMIT 1);
SHOW WARNINGS;
RESET QUERY CACHE;
SELECT * FROM people p,course c, grade g,students s WHERE p.ID=s.sid AND c.SID=s.sid AND g.sid=s.sid AND g.GRADE=(SELECT g.grade FROM grade g GROUP BY g.GRADE ORDER BY g.GRADE DESC LIMIT 1);

EXPLAIN SELECT * FROM people p,course c, grade g,students s WHERE p.ID=s.sid AND c.SID=s.sid AND g.sid=s.sid AND g.GRADE=(SELECT MAX(g.grade) FROM grade g);
SHOW WARNINGS;
RESET QUERY CACHE;
SELECT * FROM people p,course c, grade g,students s WHERE p.ID=s.sid AND c.SID=s.sid AND g.sid=s.sid AND g.GRADE=(SELECT MAX(g.grade) FROM grade g);