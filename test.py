def permutari(n):
	k=0;
	x=[];
	def perm(k,n):
		if(k==n):
			print(x);
		else:
			for i in range(n):
				if(x.count(i+1)==0):
					x.append(i+1);
					perm(k+1,n);
					x.pop();
	perm(0,n);
def combinatii(n,k):
        q=0;
        x=[];
        def comb(q,k,n):
                    if(k==q): print(x);
                    elif(q==0):
                            for i in range(n):
                                    x.append(i+1);
                                    comb(q+1,k,n);
                                    x.pop();
                    else:
                                  for i in range(n):
                                        if(x.count(i+1)==0 and i+1>x[q-1]):
                                                x.append(i+1);
                                                comb(q+1,k,n);
                                                x.pop();
        comb(0,k,n);
def aranjamente(n,k):
        q=0;
        x=[];
        def aranj(q,k,n):
                    if(k==q): print(x);
                    else:
                                  for i in range(n):
                                        if(x.count(i+1)==0):
                                                x.append(i+1);
                                                aranj(q+1,k,n);
                                                x.pop();
        aranj(0,k,n);
def acker(m,n):
	return n+1 if m<=0 else acker(m-1,1)if (m>0 and n==0) else acker(m-1,acker(m,n-1))
def fib(x):
	return 0 if x==0 else 1 if x==1 else fib(x-1)+fib(x-2)
def fact(x):
	return 1 if(x==0) else x*fact(x-1)
def encriptcaesar(x,a):
  c=""
  x=x%26;
  for i in a:
    if(i!=" "):
     d=ord(i)+x
     if(d>ord('z')or d>ord('Z')):
        d=d-ord('z')+ord('a')-1
     c=c+(chr(d))
    else: c=c+i
  return str(c)
def decriptcaesar(d):
  for c in range(0,ord('z')-ord('a')):
    print(encriptcaesar(c,d))
def funcencr(x,a):
	return "".join(list(map(lambda i:chr(ord(i)+x-ord('z')+ord('a')-1)if(ord(i)+x>ord('z')) else chr(ord(i)+x) if (i!=" ") else i,a)))

def cmmdc (x,y):
  if(x==0): return y
  elif(y==0): return x
  else: return cmmdc(y,x%y)

def citire (f):
  a=[]
  t=open(f,"rt")
  for line in t:
      a.append([int(x) for x in line.split()])
  return a
def suma(a,b):
 return ([[a[i][j]+b[i][j]for j in range(len(a[i]))] for i in range(len(a))])
 '''for i in range(len(a)):
         
         t=[]
         q=[]
         for j in range(len(a[i])):
             print(a[i][j],end=' ')
             print(b[i][j],end="\n\n")
             t.append(a[i][j]+b[i][j]);
         c.append([a[i][j]+b[i][j]for j in range(len(a[i]))])
         return c'''
'''def afis(a):
    [[[print(a[i][j]) for j in range(len(a[i])) ],print()] for i in range(len(a)) ]
'''
def inmultire(a,b):
    c=[]
    if len(a[0])==len(b):
     return ([[sum(a[i][k]*b[k][j] for k in range(len(b[j])) )for j in range(len(a[i])) ]for i in range(len(a))])
     '''for i in range(len(a)):
         t=[]
         for j in range(len(a[i])):
            s=0;
            for k in range(len(b[i])):
              s=s+a[i][k]*b[k][j]
              
            t.append(s)
         c.append(t)
     return c;'''
    else:
      return [0];
def afisare(f,a,cond):
  fis=open(f,cond)
  for i in range(len(a)):
     for j in range(len(a[i])):
       fis.write(str(a[i][j])+" ")
     fis.write("\n")
  fis.write("\n")
#q=str(input("test: "))
#print(q)
permutari(int(input("Permutari n= ")))
combinatii(int(input("Combinatii \nn= ")),int(input("k= ")))
aranjamente(int(input("Aranjamente \nn= ")),int(input("k= ")))
print(cmmdc(int(input("x= ")),int(input("y= "))))

while True:
 try:
  x=""
  x=str(input("Primul fisier: "))
  a1=citire(x)
  break
 except:
   print "Fisier negasit",x
while True:
  try:
   x=input("Al doilea fisier: ")
   a2=citire(x)
   break
  except:
    print("Fisier negasit",x)
print(a1)
afis(a1)
print(a2)
afis(a2)
c=suma(a1,a2)
print(c)
q=inmultire(a1,a2)
s=suma(a1,a2)
print(q)
t=str(input("Fisier iesire: "))
afisare(t,q,"wt")
afisare(t,s,"a")
afisare(t,a1,"a")
afisare(t,a2,"a")
for x in range(1,11):
     print('{0:2d} {1:3d} {2:4d}'.format(x, x*x, x*x*x))
key=int(input("key="))
mess=str(input("Message= "))
print(funcencr(key,mess))
opq=encriptcaesar(key,mess)
decriptcaesar(opq)
for i in range(20):
  print("fib: ",fib(i)," ","fact ",fact(i)," ",i)
