START TRANSACTION;
RESET QUERY CACHE;
SET @stime:= CURTIME(4);
SELECT * FROM people p,students s,grade g  , course c  where p.id=s.pid and s.sid=g.sid and s.sid=c.sid and g.grade > 5 ;;
SET @exectime:= TIMEDIFF(CURTIME(4),@stime);
SELECT @exectime;
COMMIT;