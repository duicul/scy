from crate import client
import time,random,string
import concurrent.futures

def randomString(stringLength):
    """Generate a random string of letters and digits """
    return ''.join(random.choice(string.ascii_letters) for i in range(stringLength))


def create_table(cursor):
    cursor.execute("DROP Table people;")
    cursor.execute("DROP Table student;")
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
    #print(final)
    timeresp = time.time_ns()-initresp
    return {"exec":final[0]-init[0],"resp":timeresp/1000000}

def measure_insert(mycursor,indrange):
    initresp = time.time_ns()
    querry="SELECT current_timestamp;"
    mycursor.execute(querry)
    init=mycursor.fetchone()
    #print(init)
    degree=["Math","Algebra","Analysis","Comedy","Drama","Classics","Biology","Anatomy","Chemistry"]
    vals=[]
    for i in indrange:
        name=randomString(random.randint(6,12))
        surname=randomString(random.randint(6,12))
        age=random.randint(10,90)
        vals.append((i,name,surname,age))
    #print(vals)
    sql = """INSERT INTO people (id,name,surname,age) VALUES (?,?,?,?)"""
    
    cursor.executemany(sql,vals)
    
    vals=[]
    for i in indrange:
        deg=degree[random.randint(0,len(degree)-1)]
        vals.append((i,i,deg))
    #print(vals)
    sql = """INSERT INTO student (sid,pid,degree) VALUES (?,?,?)"""
    cursor.executemany(sql,vals)
    mycursor.execute(querry)
    final=mycursor.fetchone()
    #print(final)
    timeresp = time.time_ns()-initresp
    return {"exec":final[0]-init[0],"resp":timeresp/1000000}
    
    
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
    for val in timevals:
        print("select execution time "+str(val["exec"]))
        print("select response time "+str(val["resp"]))

def test_insert(mycursor,datasize,threads_no):
    timevals=[]
    threads=[]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(threads_no):
            rangelimit=range(i*threads_no,(i+1)*threads_no) if (i+1)*threads_no<datasize else range(i*threads_no,datasize)
            future = executor.submit(measure_insert,mycursor,rangelimit)
            threads.append(future)
        for thread in threads:
            while not thread.done():
                pass
            return_value = thread.result()
            timevals.append(return_value)
    for val in timevals:
        print("insert execution time "+str(val["exec"]))
        print("insert response time "+str(val["resp"]))

def test(cursor,datasize,threads_no):
    create_table(cursor)
    test_insert(cursor,datasize,threads_no)
    test_select(cursor,threads_no)

connection = client.connect("http://localhost:4200/", username="crate",error_trace=True)
#create_table(connection)
cursor = connection.cursor()
test(cursor,2000,2)
