import mysql.connector
import random
import string

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="advanced_databases"
)

print(mydb)

def randomString(stringLength):
    """Generate a random string of letters and digits """
    return ''.join(random.choice(string.ascii_letters) for i in range(stringLength))

def insert_student(name,surname,age,degree,subject,grade):
    mycursor = mydb.cursor()
    sql = "INSERT INTO people (NAME,SURNAME,AGE) VALUES (%s, %s, %s)"
    val = (name,surname,age)
    mycursor.execute(sql, val)
    mydb.commit()
    
    mycursor.execute("SELECT * FROM people WHERE NAME='"+name+"' AND SURNAME='"+surname+"'")
    myresult = mycursor.fetchall()
    #print(myresult)

    pid=myresult[0][0]
    
    sql = "INSERT INTO students (PID,DEGREE) VALUES (%s, %s)"
    val = (pid,degree)
    mycursor.execute(sql, val)
    mydb.commit()
    
    mycursor.execute("SELECT * FROM students WHERE PID="+str(pid))
    myresult = mycursor.fetchall()
    #print(myresult)

    sid=myresult[0][0]

    sql = "INSERT INTO course (SID,COURSE) VALUES (%s, %s)"
    val = (sid,subject)
    mycursor.execute(sql, val)
    mydb.commit()
    
    mycursor.execute("SELECT * FROM course WHERE SID="+str(sid)+" AND COURSE='"+subject+"'" )
    myresult = mycursor.fetchall()
    #print(myresult)

    cid=myresult[0][0]

    sql = "INSERT INTO grade (SID,GRADE) VALUES (%s, %s)"
    val = (sid,grade)
    mycursor.execute(sql, val)
    mydb.commit()
    
    mycursor.execute("SELECT * FROM grade WHERE SID="+str(sid))
    myresult = mycursor.fetchall()
    #print(myresult)
    mycursor.close()

names=['John','Tom','Elliot','Alex','Joe','Rob','Pete','Bob','Dean','Sam','Jack','Michael']
surnames=['Smith','Winchester','Biden','Peterson','Jackson','Carlson','Odinson']
degree=["Mathology","Literature","MD","IT"]
subject=[["Math","Algebra","Analysis"],["Comedy","Drama","Classics"],["Biology","Anatomy","Chemistry"],["Programming","DB","Math","Structures"]]

def measure_select(index):
    index_opt="" if index == False else " IGNORE INDEX (GRADE) "
    mycursor = mydb.cursor()
    querry="START TRANSACTION;"
    querry+="RESET QUERY CACHE;"
    querry+="SET @stime:= CURTIME(4);"
    querry+="SELECT * FROM people p,students s,grade g "+index_opt+" ,course c  where p.id=s.pid and s.sid=g.sid and s.sid=c.sid and g.grade > 5 ;"
    querry+="SET @exectime:= TIMEDIFF(CURTIME(4),@stime);"
    querry+="SELECT @exectime;"
    querry+="COMMIT;"
    myresult=""
    data=mycursor.execute(querry, multi=True)
    #print(data)
    try:
        result=next(data)
        while result:
            #print(result)
            if result.with_rows:
                myresult=result.fetchall()
            result=next(data)
            #print(result)
    except Exception:
        pass
    #print(myresult)
    mycursor.close()
    return myresult

def measure_select_hash(index):
    index_opt="" if index == False else " IGNORE INDEX (GRADE) "
    mycursor = mydb.cursor()
    querry="START TRANSACTION;"
    querry+="RESET QUERY CACHE;"
    querry+="SET @stime:= CURTIME(4);"
    querry+="SELECT * FROM people p,students s,grade g "+index_opt+" , course c  where p.id=s.pid and s.sid=g.sid and s.sid=c.sid and c.course = 'Drama';"
    querry+="SET @exectime:= TIMEDIFF(CURTIME(4),@stime);"
    querry+="SELECT @exectime;"
    querry+="COMMIT;"
    myresult=""
    #print(querry)
    data=mycursor.execute(querry, multi=True)
    #print(data)
    try:
        result=next(data)
        while result:
            #print(result)
            if result.with_rows:
                myresult=result.fetchall()
            result=next(data)
            #print(result)
    except Exception:
        pass
    mycursor.close()
    #print(myresult)
    return myresult
    

def show_data():
    mycursor = mydb.cursor()
    querry="RESET QUERY CACHE;"
    mycursor.execute(querry)
    mycursor.execute("SELECT p.name,p.surname,p.age,s.degree,c.course,g.grade FROM people p,students s,grade g,course c where p.id=s.pid and s.sid=g.sid and s.sid=c.sid" )
    myresult = mycursor.fetchall()
    mycursor.close()
    return myresult

def insert_data(size):
    for i in range(size):
        name=randomString(random.randint(6,10))
        surname=randomString(random.randint(6,10))
        #print(name+" "+surname)
        deg=random.randint(0,len(degree)-1)
        subj=random.randint(0,len(subject[deg])-1)
        insert_student(name,surname,random.randint(18,25),degree[deg],subject[deg][subj],random.randint(2,10))

#insert_student("Popa1","Vasi",16,"Math","Meth",3)
sizes=[10,40,50,200,200,500,1000,2000]
file=open("result_max.txt","w")
slist=[]
reg_no=0
for size in sizes:
    reg_no+=size
    insert_data(size)
    no_index=measure_select(False)[0][0]
    index=measure_select(True)[0][0]
    print(no_index)
    print(index)
    slist.append({"noindex":no_index,"index":index,"records":reg_no})
file.write(str(slist))
file.close()
#insert_data(40)
#for reg in show_data():
#    print(reg)
#print(measure_select(False))
#print(measure_select(True))
#insert_data()

