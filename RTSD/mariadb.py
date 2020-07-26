import mysql.connector
import time,random,string,json
import concurrent.futures
import traceback
import MySQLdb


mydb = MySQLdb.connect(
  host="localhost",
  user="root",
  passwd="",
  database="advanced_databases"
)


def randomString(stringLength):
    """Generate a random string of letters and digits """
    return ''.join(random.choice(string.ascii_letters) for i in range(stringLength))


def create_table():
    conn=MySQLdb.connect(
      host="localhost",
      user="root",
      passwd="",
      database="advanced_databases"
    )
    cursor=conn.cursor()
    try:
        cursor.execute("DROP Table people1;")
        mydb.commit()
    except Exception:
        pass
    print("DROP Table people1;")
    try:
        cursor.execute("DROP Table student1;")
        mydb.commit()
    except Exception:
        pass
    print("DROP Table student1;")
    sql="CREATE TABLE people1("
    sql+="ID int NOT NULL primary key AUTO_INCREMENT ,"
    sql+="NAME text NOT NULL,"
    sql+="SURNAME text NOT NULL,"
    sql+="AGE int NOT NULL);"
    print(sql)
    cursor.execute(sql)
    mydb.commit()
    sql="CREATE TABLE student1 ("
    sql+=" SID int NOT NULL primary key,"
    sql+=" PID int NOT NULL ,"
    sql+="DEGREE text NOT NULL );"
    print(sql)
    cursor.execute(sql)
    mydb.commit()
    cursor.close()

def measure_select():
    conn=MySQLdb.connect(
      host="localhost",
      user="root",
      passwd="",
      database="advanced_databases"
    )
    #print("measure_select")
    initresp = time.time_ns()
    mycursor = conn.cursor()
    querry="START TRANSACTION;"
    mycursor.execute(querry)
    mycursor.fetchall()
    querry="RESET QUERY CACHE;"
    mycursor.execute(querry)
    mycursor.fetchall()
    querry="SET @stime:= CURTIME(4)+0;"
    mycursor.execute(querry)
    mycursor.fetchall()
    querry="SELECT * FROM people1 p inner join student1 s on p.id=s.pid;"
    mycursor.execute(querry)
    mycursor.fetchall()
    querry="SET @exectime:= (CURTIME(4)+0)-@stime;"
    mycursor.execute(querry)
    mycursor.fetchall()
    querry="SELECT @exectime;"
    mycursor.execute(querry)
    #print()
    #querry+="COMMIT;"
    myresult=""
    #data=mycursor.execute(querry)
    conn.commit()
    myresult=mycursor.fetchall()
    """try:
        result=next(data)
        while result:
            #print(result)
            if result.with_rows:
                myresult=result.fetchall()
            result=next(data)
            #print(result)
    except Exception as e:
        print(traceback.format_exc())"""
    timeresp = time.time_ns()-initresp
    #print(myresult[0][0])
    #print(timeresp/1000000)
    #print(myresult)
    timeexec=myresult[0][0]
    mycursor.close()
    return {"exec":float(timeexec*1000),"resp":timeresp/1000000}  

def measure_insert(indrange):
    conn=MySQLdb.connect(
      host="localhost",
      user="root",
      passwd="",
      database="advanced_databases"
    )
    mycursor=conn.cursor()
    querry="START TRANSACTION;"
    mycursor.execute(querry)
    mycursor.fetchall()
    querry="RESET QUERY CACHE;"
    mycursor.execute(querry)
    mycursor.fetchall()
    querry="SET @stime:= CURTIME(4)+0;"
    mycursor.execute(querry)
    mycursor.fetchall()
    #print(init)
    degree=["Math","Algebra","Analysis","Comedy","Drama","Classics","Biology","Anatomy","Chemistry"]
    vals=[]
    for i in indrange:
        #print(i)
        name=randomString(random.randint(6,12))
        surname=randomString(random.randint(6,12))
        age=random.randint(10,90)
        vals.append((i+1,name,surname,age))
    #print(vals)
    sql = """INSERT INTO people1 (id,name,surname,age) VALUES (%s,%s,%s,%s)"""
    initresp = time.time_ns()
    result=mycursor.executemany(sql,vals)
    #succes=len(list(filter(lambda x :x['rowcount']==1,result)))
    #print(sql)
    vals=[]
    for i in indrange:
        #print(i)
        deg=degree[random.randint(0,len(degree)-1)]
        vals.append((i+1,i+1,deg))
    #print(vals)
    sql = """INSERT INTO student1 (sid,pid,degree) VALUES (%s,%s,%s)"""
    result=mycursor.executemany(sql,vals)
    timeresp = time.time_ns()-initresp
    #print(sql)
    querry="SET @exectime:= (CURTIME(4)+0)-@stime;"
    mycursor.execute(querry)
    mycursor.fetchall()
    querry="SELECT @exectime;"
    mycursor.execute(querry)
    myresult=mycursor.fetchall()
    conn.commit()
    
    #succes+=len(list(filter(lambda x :x['rowcount']==1,result)))
    #succes/=2
    timeexec=myresult[0][0]
    #print(timeexec)
    #print(timeresp)
    mycursor.close()
    conn.close()
    #,"succes":succes
    return {"exec":float(timeexec*1000),"resp":timeresp/1000000,"total":len(indrange)}
    
    
def test_select(threads_no):
    timevals=[]
    threads=[]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(threads_no):
            future = executor.submit(measure_select)
            threads.append(future)
        for thread in threads:
            while not thread.done():
                pass
            return_value = thread.result()
            timevals.append(return_value)
    resp_time=0
    exec_time=0
    for val in timevals:
        resp_time+=val["resp"]
        exec_time+=val["exec"]
    #resp_time/=len(timevals)
    #exec_time/=len(timevals)
    print("select execution time "+str(exec_time))
    print("select response time "+str(resp_time))
    return {"exec":exec_time,"resp":resp_time}

def test_insert(datasize,threads_no):
    timevals=[]
    threads=[]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(threads_no):
            start=int(i*(datasize/threads_no))
            end=int((i+1)*(datasize/threads_no)) if int((i+1)*(datasize/threads_no))<datasize else datasize
            print("start"+str(start)+" end "+str(end)+"|")
            future = executor.submit(measure_insert,range(start,end))
            threads.append(future)
        for thread in threads:
            while not thread.done():
                pass
            return_value = thread.result()
            timevals.append(return_value)
    resp_time=0
    exec_time=0
    succes=0
    for val in timevals:
        resp_time+=val["resp"]
        exec_time+=val["exec"]
        #succes+=(val["succes"]/val["total"])
    #succes*=100
    #resp_time/=len(timevals)
    #exec_time/=len(timevals)
    #succes/=len(timevals)
    print("insert execution time "+str(exec_time))
    print("insert response time "+str(resp_time))
    #print("succes rate  "+str(succes)+"% ")
    return {"exec":exec_time,"resp":resp_time}#,"succes":succes}

def test(datasize,threads_no):
    print("test "+str(datasize)+" threadsno "+str(threads_no))
    create_table()
    insert=test_insert(datasize,threads_no)
    select=test_select(threads_no)
    return {"datasize":datasize,"threads":threads_no,"data/thread":datasize/threads_no,"select":select,"insert":insert}

if __name__=="__main__":
    t=[]
    for i in range(100):
        create_table()
        t.append(test_insert(1,1)["resp"])
    average=sum(t)/len(t)
    res={}
    res["average"]=average
    res["jitter%"]=((max(t)-average)/average)*100
    res["data"]=t
    file = open("result_mariadbjitter.txt", "w")
    json.dump(res,file)
    file.write(str(res))
    file.close()
    """threads_no=[1,2,5,10,20,50,100]
    datasize=[10,20,30,50,100,200,300,500,1000,2000,3000,4000,5000,10000]
    tests=[]
    for th in threads_no:
        for ds in datasize :
            if ds>=th:
                retry=0
                succ=False
                while retry<30 and not succ:
                    try:
                        result=test(ds,th)
                        tests.append(result)
                        succ=True
                    except Exception:
                        retry+=1
    file = open("result_mariadb.txt", "w")
    json.dump(tests,file)
    file.close()"""
