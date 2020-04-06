from crate import client
import time,random,string,json
import concurrent.futures

def randomString(stringLength):
    """Generate a random string of letters and digits """
    return ''.join(random.choice(string.ascii_letters) for i in range(stringLength))


def create_table(cursor):
    cursor.execute("DROP Table people;")
    print("DROP Table people;")
    cursor.execute("DROP Table student;")
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

def measure_select(mycursor):
    initresp = time.time_ns()
    querry="SELECT current_timestamp;"
    mycursor.execute(querry)
    init=mycursor.fetchone()
    #print(init)
    querry="SELECT * FROM people p inner join student s on p.id=s.pid;"
    
    mycursor.execute(querry)
    
    """result=cursor.fetchall()
    while result!=None:
        print(result)
        result=cursor.fetchone()"""
    querry="SELECT current_timestamp;"
    mycursor.execute(querry)
    final=mycursor.fetchone()
    timeexec=final[0]-init[0] if (not final == None) and (not init == None) else 0
    #print(final)
    timeresp = time.time_ns()-initresp
    timeexec=0 if timeexec<0 else timeexec
    return {"exec":timeexec,"resp":timeresp/1000000}

def measure_insert(mycursor,indrange):
    initresp = time.time_ns()
    querry="SELECT current_timestamp;"
    mycursor.execute(querry)
    init=mycursor.fetchone()
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
    #print(result)
    mycursor.execute(querry)
    final=mycursor.fetchone()
    #print(final)
    timeresp = time.time_ns()-initresp
    succes+=len(list(filter(lambda x :x['rowcount']==1,result)))
    succes/=2
    timeexec=final[0]-init[0] if (not final == None) and (not init == None) else 0
    timeexec=0 if timeexec<0 else timeexec
    return {"exec":timeexec,"resp":timeresp/1000000,"succes":succes,"total":len(indrange)}
    
    
def test_select(mycursor,threads_no):
    timevals=[]
    threads=[]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(threads_no):
            #rangelimit=range(i*threads_no,(i+1)*threads_no) if (i+1)*threads_no<datasize else range(i*threads_no,datasize)
            future = executor.submit(measure_select,mycursor)
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
    resp_time/=len(timevals)
    exec_time/=len(timevals)
    print("select execution time "+str(exec_time))
    print("select response time "+str(resp_time))
    return {"exec":exec_time,"resp":resp_time}

def test_insert(mycursor,datasize,threads_no):
    timevals=[]
    threads=[]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(threads_no):
            start=int(i*(datasize/threads_no))
            end=int((i+1)*(datasize/threads_no)) if int((i+1)*(datasize/threads_no))<datasize else datasize
            print("start"+str(start)+" end "+str(end)+"|")
            future = executor.submit(measure_insert,mycursor,range(start,end))
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

def test(cursor,datasize,threads_no):
    print("test "+str(datasize)+" threadsno "+str(threads_no))
    create_table(cursor)
    insert=test_insert(cursor,datasize,threads_no)
    select=test_select(cursor,threads_no)
    return {"datasize":datasize,"threads":threads_no,"data/thread":datasize/threads_no,"insert":insert,"select":select}

connection = client.connect("http://localhost:4200/", username="crate",error_trace=True)
#create_table(connection)
cursor = connection.cursor()
threads_no=[1,5,10,20,50,100]
datasize=[10,20,30,50,100,200,300,500,1000,2000,3000,4000,5000,10000]
tests=[]
for th in threads_no:
    for ds in datasize :
        if ds>=th:
            tests.append(test(cursor,ds,th))
cursor.close()
file = open("result_cratedb.txt", "w")
json.dump(tests,file)
#file.write(str(tests))
file.close()
