-- Table Creation 
CREATE TABLE `course` (
  `CID` int(11) NOT NULL,
  `SID` int(11) DEFAULT NULL,
  `COURSE` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE `grade` (
  `GID` int(11) NOT NULL,
  `SID` int(11) DEFAULT NULL,
  `GRADE` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE `people` (
  `ID` int(4) NOT NULL,
  `NAME` varchar(10) NOT NULL,
  `SURNAME` varchar(10) NOT NULL,
  `AGE` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE `students` (
  `SID` int(4) NOT NULL,
  `PID` int(4) NOT NULL DEFAULT 0,
  `DEGREE` varchar(50) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


-- Adding primary keys + unique keys and indexes
ALTER TABLE `course`
  ADD PRIMARY KEY (`CID`) USING BTREE,
  ADD UNIQUE KEY `SID_COURSE` (`SID`,`COURSE`),
  ADD KEY `COURSE` (`COURSE`) USING HASH,
  ADD KEY `SID` (`SID`) USING BTREE;
  
ALTER TABLE `grade`
  ADD PRIMARY KEY (`GID`) USING BTREE,
  ADD KEY `FSID` (`SID`) USING BTREE,
  ADD KEY `GRADE` (`GRADE`) USING BTREE;
  
ALTER TABLE `people`
  ADD PRIMARY KEY (`ID`) USING BTREE,
  ADD UNIQUE KEY `NAME_SURNAME` (`NAME`,`SURNAME`),
  ADD KEY `Name` (`NAME`) USING HASH,
  ADD KEY `Age` (`AGE`) USING BTREE;
  
ALTER TABLE `students`
  ADD PRIMARY KEY (`SID`) USING BTREE,
  ADD KEY `PID` (`PID`) USING BTREE,
  ADD KEY `DEGREE` (`DEGREE`) USING HASH;
  
-- Adding foreign key constraints
ALTER TABLE `course`
  ADD CONSTRAINT `SID` FOREIGN KEY (`SID`) REFERENCES `students` (`SID`) ON DELETE NO ACTION;

ALTER TABLE `grade`
  ADD CONSTRAINT `FSID` FOREIGN KEY (`SID`) REFERENCES `students` (`SID`) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE `students`
  ADD CONSTRAINT `PID` FOREIGN KEY (`PID`) REFERENCES `people` (`ID`) ON DELETE NO ACTION;
  

-- There are 2 types of indexes: binary tree for comparasion and prefix matching and hash for equality / perfect match
-- I used a python script to insert data into the database and measure the time taken for a select querry for both types of indexes

--Select querry for hash :
-- To not use an index IGNORE INDEX (GRADE) could be added

START TRANSACTION;
RESET QUERY CACHE;
SET @stime:= CURTIME(4);
SELECT * FROM people p,students s,grade g  , course c  where p.id=s.pid and s.sid=g.sid and s.sid=c.sid c.course = 'Drama';
SET @exectime:= TIMEDIFF(CURTIME(4),@stime);
SELECT @exectime;
COMMIT;

--Select querry for binary tree:
-- To not use an index IGNORE INDEX (GRADE) could be added

START TRANSACTION;
RESET QUERY CACHE;
SET @stime:= CURTIME(4);
SELECT * FROM people p,students s,grade g  , course c  where p.id=s.pid and s.sid=g.sid and s.sid=c.sid and g.grade > 5 ;;
SET @exectime:= TIMEDIFF(CURTIME(4),@stime);
SELECT @exectime;
COMMIT;

-- And these are results, as it can be seen the hash produces a larger difference between tabl search and index search, but both show -->
-- almost an exponential difference to the time taken for the entire table search -->

-- Results for binary tree:
/*[{'noindex': '00:00:00.0024', 'index': '00:00:00.0018', 'records': 10},
 {'noindex': '00:00:00.0007', 'index': '00:00:00.0003', 'records': 50},
 {'noindex': '00:00:00.0030', 'index': '00:00:00.0012', 'records': 100}, 
 {'noindex': '00:00:00.0039', 'index': '00:00:00.0018', 'records': 300}, 
 {'noindex': '00:00:00.0120', 'index': '00:00:00.0038', 'records': 500},
 {'noindex': '00:00:00.0546', 'index': '00:00:00.0021', 'records': 1000}, 
 {'noindex': '00:00:00.2899', 'index': '00:00:00.0039', 'records': 2000}, 
 {'noindex': '00:00:00.2635', 'index': '00:00:00.0075', 'records': 4000}]*/
 
-- Results for hash index :
/*[{'noindex': '00:00:00.0002', 'index': '00:00:00.0001', 'records': 10}, 
{'noindex': '00:00:00.0002', 'index': '00:00:00.0002', 'records': 50}, 
{'noindex': '00:00:00.0003', 'index': '00:00:00.0003', 'records': 100}, 
{'noindex': '00:00:00.0006', 'index': '00:00:00.0005', 'records': 300}, 
{'noindex': '00:00:00.0220', 'index': '00:00:00.0009', 'records': 500}, 
{'noindex': '00:00:00.0880', 'index': '00:00:00.0010', 'records': 1000}, 
{'noindex': '00:00:00.0748', 'index': '00:00:00.0014', 'records': 2000}, 
{'noindex': '00:00:00.5755', 'index': '00:00:00.0126', 'records': 4000}]*/

--Querries used to clean the database after each insertion round and select measurement :
DELETE FROM grade;
DELETE FROM course;
DELETE FROM students;
DELETE FROM people;

--Querries with the same result :
EXPLAIN SELECT * FROM people p,course c, grade g,students s WHERE g.SID=s.SID  AND s.SID=c.SID AND p.ID=s.PID ;

SELECT * FROM people p,course c, grade g,students s WHERE g.SID=s.SID  AND s.SID=c.SID AND p.ID=s.PID ;
RESET QUERY CACHE;

EXPLAIN SELECT * FROM people p INNER  JOIN students s ON p.ID=s.PID INNER JOIN  course c ON s.SID=c.SID INNER JOIN  grade g ON g.SID=s.SID;

SELECT * FROM people p INNER  JOIN students s ON p.ID=s.PID INNER JOIN  course c ON s.SID=c.SID INNER JOIN  grade g ON g.SID=s.SID;
RESET QUERY CACHE;

/*
"1"	"SIMPLE"	"g"	"ALL"	"FSID"	\N	\N	\N	"1000"	"Using where"
"1"	"SIMPLE"	"c"	"ref"	"SID_COURSE,SID"	"SID_COURSE"	"5"	"advanced_databases.g.SID"	"1"	"Using index"
"1"	"SIMPLE"	"s"	"eq_ref"	"PRIMARY,PID"	"PRIMARY"	"4"	"advanced_databases.g.SID"	"1"	""
"1"	"SIMPLE"	"p"	"eq_ref"	"PRIMARY"	"PRIMARY"	"4"	"advanced_databases.s.PID"	"1"	""
*/

/*
"1"	"SIMPLE"	"g"	"ALL"	"FSID"	\N	\N	\N	"1000"	"Using where"
"1"	"SIMPLE"	"s"	"eq_ref"	"PRIMARY,PID"	"PRIMARY"	"4"	"advanced_databases.g.SID"	"1"	""
"1"	"SIMPLE"	"c"	"ref"	"SID_COURSE,SID"	"SID_COURSE"	"5"	"advanced_databases.g.SID"	"1"	"Using index"
"1"	"SIMPLE"	"p"	"eq_ref"	"PRIMARY"	"PRIMARY"	"4"	"advanced_databases.s.PID"	"1"	""*/

--Both querries produce the same result an dcontain the same execution plan, using an index for sid on table course and a where on table grade

--Querries with different execution plans but the same results:
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

/*
"1"	"PRIMARY"	"g"	"ref"	"FSID,GRADE"	"GRADE"	"5"	"const"	"1"	"Using where"
"1"	"PRIMARY"	"c"	"ref"	"SID_COURSE,SID"	"SID_COURSE"	"5"	"advanced_databases.g.SID"	"1"	"Using index"
"1"	"PRIMARY"	"p"	"eq_ref"	"PRIMARY"	"PRIMARY"	"4"	"advanced_databases.g.SID"	"1"	""
"1"	"PRIMARY"	"s"	"eq_ref"	"PRIMARY"	"PRIMARY"	"4"	"advanced_databases.g.SID"	"1"	""
"2"	"SUBQUERY"	"g"	"index"	\N	"GRADE"	"5"	\N	"1000"	"Using index"*/

/*"1"	"PRIMARY"	"g"	"ref"	"FSID,GRADE"	"GRADE"	"5"	"const"	"121"	"Using where"
"1"	"PRIMARY"	"p"	"eq_ref"	"PRIMARY"	"PRIMARY"	"4"	"advanced_databases.g.SID"	"1"	""
"1"	"PRIMARY"	"c"	"ref"	"SID_COURSE,SID"	"SID_COURSE"	"5"	"advanced_databases.g.SID"	"1"	"Using index"
"1"	"PRIMARY"	"s"	"eq_ref"	"PRIMARY"	"PRIMARY"	"4"	"advanced_databases.g.SID"	"1"	""
"2"	"SUBQUERY"	\N	\N	\N	\N	\N	\N	\N	"Select tables optimized away"*/

--Both querries use the index on table course for joining on column sid, but the first querry just table searches for the max grade value by sorting the table in decreasing order and limiting to one entry
--The second querry is faster, using the predefined binary index tree on column grade from querry grade which stores the MAX value and can be directly accessed without the need of a table search or even an index search

-- Concurrency support for MariaDB can be exemplified with the use of transactions which let the grouping of querries and their execution as a single atomix entity
-- Transactions allow the operations to be atomised so in case of a concurrent querry to the same table, the latter querry would have to wait for the previous one to complete, providing a locking mechanism for concurrent querry execution
-- The transaction has to be terminated with a COMMIT to the database to load the entire transaction / group of querries
START TRANSACTION;
RESET QUERY CACHE;
SET @stime:= CURTIME(4);
SELECT * FROM people p,students s,grade g  , course c  where p.id=s.pid and s.sid=g.sid and s.sid=c.sid and g.grade > 5 ;;
SET @exectime:= TIMEDIFF(CURTIME(4),@stime);
SELECT @exectime;
COMMIT;

-- The previous querries used to measure the select time on an index are a good example of this 
-- In order to be able to measure only the time taken for the querry a transaction is used to not allow other querries to interrupt the querry execution (or database events)



 