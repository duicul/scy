from crate import client
import time,random,string,json
import concurrent.futures

def randomString(stringLength):
    """Generate a random string of letters and digits """
    return ''.join(random.choice(string.ascii_letters) for i in range(stringLength))


def create_table():
    connection = client.connect("http://localhost:4200/", username="crate",error_trace=True)
    cursor=connection.cursor()
    try:
        cursor.execute("DROP Table people;")
    except Exception:
        pass
    print("DROP Table people;")
    try:
        cursor.execute("DROP Table student;")
    except Exception:
        pass
    print("DROP Table student;")
    sql="CREATE TABLE people("
    sql+="ID int NOT NULL primary key ,"
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
    cursor.close()
    connection.close()

def measure_select():
    connection = client.connect("http://localhost:4200/", username="crate",error_trace=True)
    mycursor=connection.cursor()
    
    querry="SELECT current_timestamp;"
    mycursor.execute(querry)
    init=mycursor.fetchone()
    #print(init)
    querry="SELECT * FROM people p inner join student s on p.id=s.pid;"
    initresp = time.time_ns()
    mycursor.execute(querry)
    timeresp = time.time_ns()-initresp
    """result=cursor.fetchall()
    while result!=None:
        print(result)
        result=cursor.fetchone()"""
    querry="SELECT current_timestamp;"
    mycursor.execute(querry)
    final=mycursor.fetchone()
    timeexec=final[0]-init[0] if (not final == None) and (not init == None) else 0
    #print(final)
    
    timeexec=0 if timeexec<0 else timeexec
    mycursor.close()
    connection.close()
    return {"exec":timeexec,"resp":timeresp/1000000}

def measure_insert(indrange):
    connection = client.connect("http://localhost:4200/", username="crate",error_trace=True)
    cursor=connection.cursor()
    querry="SELECT current_timestamp;"
    cursor.execute(querry)
    init=cursor.fetchone()
    #print(init)
    degree=["Math","Algebra","Analysis","Comedy","Drama","Classics","Biology","Anatomy","Chemistry"]
    vals=[]
    for i in indrange:
        #print(i)
        name=randomString(random.randint(6,12))
        surname=randomString(random.randint(6,12))
        age=random.randint(10,90)
        vals.append((i,name,surname,age))
    #print(vals)
    sql = """INSERT INTO people (id,name,surname,age) VALUES (?,?,?,?)"""
    initresp = time.time_ns()
    result=cursor.executemany(sql,vals)
    succes=len(list(filter(lambda x :x['rowcount']==1,result)))
    #print(result)
    vals=[]
    for i in indrange:
        #print(i)
        deg=degree[random.randint(0,len(degree)-1)]
        vals.append((i,i,deg))
    #print(vals)
    sql = """INSERT INTO student (sid,pid,degree) VALUES (?,?,?)"""
    result=cursor.executemany(sql,vals)
    timeresp=time.time_ns()-initresp
    #print(result)
    querry="SELECT current_timestamp;"
    cursor.execute(querry)
    final=cursor.fetchone()
    #print(final)
    succes+=len(list(filter(lambda x :x['rowcount']==1,result)))
    succes/=2
    timeexec=final[0]-init[0] if (not final == None) and (not init == None) else 0
    timeexec=0 if timeexec<0 else timeexec
    cursor.close()
    connection.close()
    return {"exec":timeexec,"resp":timeresp/1000000,"succes":succes,"total":len(indrange)}
    
    
def test_select(threads_no):
    timevals=[]
    threads=[]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(threads_no):
            #rangelimit=range(i*threads_no,(i+1)*threads_no) if (i+1)*threads_no<datasize else range(i*threads_no,datasize)
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
        succes+=(val["succes"]/val["total"])
    succes*=100
    #resp_time/=len(timevals)
    #exec_time/=len(timevals)
    succes/=len(timevals)
    print("select execution time "+str(exec_time))
    print("select response time "+str(resp_time))
    print("succes rate  "+str(succes)+"% ")
    return {"exec":exec_time,"resp":resp_time,"succes":succes}

def test(datasize,threads_no):
    print("test "+str(datasize)+" threadsno "+str(threads_no))
    create_table()
    insert=test_insert(datasize,threads_no)
    select=test_select(threads_no)
    return {"datasize":datasize,"threads":threads_no,"data/thread":datasize/threads_no,"insert":insert,"select":select}

#connection = client.connect("http://localhost:4200/", username="crate",error_trace=True)
#create_table(connection)
#cursor = connection.cursor()
#threads_no=[1,5,10,20,50,100]
#datasize=[10,20,30,50,100,200,300,500,1000,2000,3000,4000,5000,10000]
#tests=[]
#for th in threads_no:
#    for ds in datasize :
#        if ds>=th:
#            tests.append(test(ds,th))
#cursor.close()
if __name__=="__main__":
    t=[]
    for i in range(100):
        create_table()
        t.append(measure_insert(range(1))["resp"])
    average=sum(t)/len(t)
    res={}
    res["average"]=average
    res["jitter%"]=((max(t)-average)/average)*100
    res["data"]=t
    file = open("result_cratedbjitter.txt", "w")
    json.dump(res,file)
    file.write(str(res))
    file.close()
