import mysql.connector
import time,random,string,json
import concurrent.futures
import traceback
import  sqlite3
from  sqlite3 import OperationalError

def randomString(stringLength):
    """Generate a random string of letters and digits """
    return ''.join(random.choice(string.ascii_letters) for i in range(stringLength))


def create_table():
    conn = sqlite3.connect('measure.db')
    cursor=conn.cursor()
    try:
        cursor.execute("DROP Table people;")
        mydb.commit()
    except Exception:
        pass
    print("DROP Table people1;")
    try:
        cursor.execute("DROP Table student;")
        mydb.commit()
    except Exception:
        pass
    print("DROP Table student;")
    sql="CREATE TABLE people("
    sql+="ID int NOT NULL primary key  ,"
    sql+="NAME text NOT NULL,"
    sql+="SURNAME text NOT NULL,"
    sql+="AGE int NOT NULL);"
    print(sql)
    cursor.execute(sql)
    sql="CREATE TABLE student ("
    sql+=" SID int NOT NULL primary key,"
    sql+=" PID int NOT NULL ,"
    sql+="DEGREE text NOT NULL );"
    print(sql)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def measure_select():
    conn = sqlite3.connect('measure.db')
    #print("measure_select")
    initresp = time.time_ns()
    mycursor = conn.cursor()
    querry="BEGIN TRANSACTION;"
    mycursor.execute(querry)
    mycursor.fetchall()
    querry="SELECT * FROM people p inner join student s on p.id=s.pid;"
    mycursor.execute(querry)
    mycursor.fetchall()
    querry="END TRANSACTION;"
    mycursor.execute(querry)
    mycursor.fetchall()
    conn.commit()
    timeresp = time.time_ns()-initresp
    timeexec=0
    mycursor.close()
    conn.close()
    return {"exec":float(timeexec*1000),"resp":timeresp/1000000}  

def measure_insert(indrange):
    conn = sqlite3.connect('measure.db')
    mycursor=conn.cursor()
    degree=["Math","Algebra","Analysis","Comedy","Drama","Classics","Biology","Anatomy","Chemistry"]
    vals=[]
    for i in indrange:
        #print(i)
        name=randomString(random.randint(6,12))
        surname=randomString(random.randint(6,12))
        age=random.randint(10,90)
        vals.append((i+1,name,surname,age))
    #print(vals)
    querry="BEGIN TRANSACTION;"
    mycursor.execute(querry)
    mycursor.fetchall()    
    sql = """INSERT INTO people (id,name,surname,age) VALUES (?,?,?,?)"""
    initresp = time.time_ns()
    result=mycursor.executemany(sql,vals)
    #print(sql)
    vals=[]
    for i in indrange:
        #print(i)
        deg=degree[random.randint(0,len(degree)-1)]
        vals.append((i+1,i+1,deg))
    #print(vals)
    sql = """INSERT INTO student (sid,pid,degree) VALUES (?,?,?)"""
    result=mycursor.executemany(sql,vals)
    querry="END TRANSACTION;"
    mycursor.execute(querry)
    mycursor.fetchall()
    timeresp = time.time_ns()-initresp
    #print(sql)
    conn.commit()

    timeexec=0
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

if __name__ == "__main__":
    t=[]
    for i in range(100):
        create_table()
        t.append(test_insert(1,1)["resp"])
    print(t)
    average=sum(t)/len(t)
    res={}
    res["average"]=average
    res["jitter%"]=((max(t)-average)/average)*100
    res["data"]=t
    file = open("result_sqlitejitter.txt", "w")
    json.dump(res,file)
    file.write(str(res))
    file.close()
    """threads_no=[1]#,2,5,10,20,50,100]
    datasize=[10,20,30,50,100,200,300,500,1000,2000,3000,4000,5000,10000]
    tests=[]
    for th in threads_no:
        for ds in datasize :
            if ds>=th:
                retry=0
                succ=False
                while retry<5 and not succ:
                    try:
                        result=test(ds,th)
                        tests.append(result)
                        succ=True
                    except sqlite3.OperationalError :
                         retry+=1
                         print(traceback.format_exc())
                         time.sleep(random.randint(10, 30))
    file = open("result_sqlite.txt", "w")
    json.dump(tests,file)
    file.close()
    #create_table()"""
