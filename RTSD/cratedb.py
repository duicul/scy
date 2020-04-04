from crate import client

def create_table(connection):
    cursor = connection.cursor()
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
    
connection = client.connect("http://localhost:4200/", username="crate",error_trace=True)
#create_table(connection)
cursor = connection.cursor()

#cursor.execute("DELETE from students")
vals=[(1,"Popa","Ion",34),(2,"Maria","Badea",45),(3,"Pitzi","Geo",12)]
print(vals)
sql = """INSERT INTO people (id,name,surname,age) VALUES (?,?,?,?)"""
cursor.executemany(sql,vals)
vals=[(1,1,"Math"),(2,2,"History"),(3,3,"Chemistry")]
print(vals)
sql = """INSERT INTO student (sid,pid,degree) VALUES (?,?,?)"""
cursor.executemany(sql,vals)
cursor = connection.cursor()
cursor.execute("SELECT p.name,p.surname,p.age,s.degree from people p , student s where p.id=s.pid")
result=cursor.fetchone()
while result!=None:
    print(result)
    result=cursor.fetchone()

