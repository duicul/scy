import sys
import re
import math
print((sys.version_info))
import tkinter
from tkinter import Frame, Canvas, Label, Button, LEFT, RIGHT,  Tk
from tkinter import *
import random
import numpy
awidth=500
aheight=500

class NNetwork:

    def __init__(self,inp,hid,out,lr):
        self.inp=inp
        self.hid=hid
        self.out=out
        self.lr=lr
        self.WH=2*numpy.random.rand(hid,inp)-1
        self.WO=2*numpy.random.rand(out,hid)-1
        self.bH=2*numpy.random.rand(hid)-1
        self.bO=2*numpy.random.rand(out)-1 
        
    def func_activ(self,x):
        return 1/(1+numpy.exp(-x))

    def grad(self,x):
        return x*(1-x)
    
    def calc(self,inval):
        #inval.append(1)
        i=numpy.mat(inval).getT()
        H=numpy.matmul(self.WH,i)
        H=numpy.matrix(H)
        for i in range(len(self.bH)):
            H[i,0]+=self.bH[i]
        H=self.func_activ(H)
        #H=numpy.append(H,[[1]],axis=0)
        self.Hid=H
        O=numpy.matmul(self.WO,H)
        O=numpy.matrix(O)
        for i in range(len(self.bO)):
            O[i,0]+=self.bO[i]
        O=self.func_activ(O)
        return O

    def adjust(self,inp,out):
         guess=self.calc(inp)
         ans=numpy.matrix(out).getT()
         #output error 
         OE=ans-guess
         #hidden layer error
         HE=numpy.matmul(numpy.matrix(self.WO).getT(),OE)
         #gradient
         Hg=[self.grad(self.Hid[i,0]) for i in range(len(self.Hid))]
         Og=[self.grad(guess[i,0]) for i in range(len(guess))]
         #gradient multiplied by error  
         OEg=[self.lr*OE[i,0]*Og[i] for i in range(len(Og))]
         HEg=[self.lr*HE[i,0]*Hg[i] for i in range(len(Hg))]
         #adjust bias    
         self.bH=[self.bH[i]+HEg[i] for i in range(len(HEg))]
         self.bO=[self.bO[i]+OEg[i] for i in range(len(OEg))]
         #variation
         dWHO=numpy.matrix(OEg).getT()*self.Hid.getT()
         dWIH=numpy.matrix(HEg).getT()*numpy.matrix(inp)
         self.WO+=dWHO
         self.WH+=dWIH

class Pointalt:

   def __init__(self):
        self.x=random.randint(0,awidth)
        self.y=random.randint(0,aheight)
        self.var=1 if self.x>self.y else 0

nn=NNetwork(2,3,1,0.8)
nn1=NNetwork(2,8,1,0.8)
val1=nn.calc([1,3])
inputs=[[0,0],[1,0],[0,1],[1,1]]
outputs=[[0],[1],[1],[0]]
a=[0,0,0,0]
for i in range(3000):
    aux=random.randint(0,3)
    a[aux]+=1
    nn1.adjust(inputs[aux],outputs[aux])
for i in range(4):
    print(inputs[i])
    print(nn1.calc(inputs[i]))
print("\n\r")
print(a)

p=Pointalt()
window2 = tkinter.Tk()
window2.title("After adjust")
window3 = tkinter.Tk()
window3.title("Before")
frame2 = Frame(window2)
frame2.pack(fill="both", expand=True)
frame3 = Frame(window3)
frame3.pack(fill="both", expand=True)
canvas2 = Canvas(frame2, width=awidth, height=aheight)
canvas2.pack(fill="both", expand=True)
canvas3 = Canvas(frame3, width=awidth, height=aheight)
canvas3.pack(fill="both", expand=True)
canvas3.create_line(0,0,awidth,aheight)
ptab2=[Pointalt() for i in range (20000)]
ptab3=[Pointalt() for i in range (500)]
rate=0
for paux in ptab3:
    t=nn.calc([paux.x/awidth,paux.y/aheight])
    color2="green" if (t[0,0]<=0.5 and paux.var==0) or (t[0,0]>=0.5 and paux.var==1) else "red"
    rate=rate if (t[0,0]<=0.5 and paux.var==0) or (t[0,0]>=0.5 and paux.var==1) else rate+1
    color3="white" if paux.var==1 else "black"
    canvas3.create_oval(paux.x-8,paux.y-8,paux.x+8,paux.y+8,fill=color3)
    canvas3.create_oval(paux.x-5,paux.y-5,paux.x+5,paux.y+5,fill=color2)
print("Initial error rate ",rate/len(ptab3))
for paux in ptab2:
    nn.adjust([paux.x/awidth,paux.y/aheight],[paux.var])
canvas2.create_line(0,0,awidth,aheight,fill="blue")
print("\r\n")
rate=0
for paux in ptab3:
    t=nn.calc([paux.x/awidth,paux.y/aheight])
    #print([paux.x,paux.y,paux.var],t)
    color2="green" if (t[0,0]<=0.5 and paux.var==0) or (t[0,0]>=0.5 and paux.var==1) else "red"
    rate=rate if (t[0,0]<=0.5 and paux.var==0) or (t[0,0]>=0.5 and paux.var==1) else rate+1
    color3="white" if paux.var==1 else "black"
    canvas2.create_oval(paux.x-8,paux.y-8,paux.x+8,paux.y+8,fill=color3)
    canvas2.create_oval(paux.x-5,paux.y-5,paux.x+5,paux.y+5,fill=color2)
print("After training error rate ",rate/len(ptab3))
window2.mainloop()
window3.mainloop()
