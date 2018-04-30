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
class Neuro:

    def __init__(self,lr):
        self.wx=random.random()*2-1
        self.wy=random.random()*2-1
        self.lr=lr
    def calculate(self,x,y): 
        return 1 if (self.wx*float(x)+self.wy*float(y))>0 else -1

    def adjust(self,x,y,val):
        aux = self.calculate(x,y)
        #print("x "+str(x)+" y "+str(y)+" val "+str(val))
        #print("Aux val: %d" % aux)
        e=val-aux
        #print("Err val: %d" % e)
        self.wx=self.wx+e*x*self.lr
        self.wy=self.wy+e*y*self.lr
        #self.weight()

    def weight(self):
        print(" wx " + str(self.wx) + " wy " + str(self.wy))

class Point:

   def __init__(self):
        self.x=random.randint(0,awidth)
        self.y=random.randint(0,aheight)
        self.var=1 if self.x>self.y else -1

   def __str__(self):
       return str(self.x)+"  "+str(self.y)+"  "+str(self.var)

n=Neuro(0.5)
p=Point()
window = tkinter.Tk()
window.title("After adjust")
window1 = tkinter.Tk()
window1.title("Before")
frame = Frame(window)
frame.pack(fill="both", expand=True)
frame1 = Frame(window1)
frame1.pack(fill="both", expand=True)
canvas = Canvas(frame, width=awidth, height=aheight)
canvas.pack(fill="both", expand=True)
canvas1 = Canvas(frame1, width=awidth, height=aheight)
canvas1.pack(fill="both", expand=True)
canvas1.create_line(0,0,awidth,aheight)
ptab=[Point() for i in range (1000)]
ptab1=[Point() for i in range (400)]
rate=0
for paux in ptab1:
    color="green" if n.calculate(paux.x,paux.y)==paux.var else "red"
    rate=rate if n.calculate(paux.x,paux.y)==paux.var else rate+1
    color1="white" if paux.var==1 else "black"
    canvas1.create_oval(paux.x-8,paux.y-8,paux.x+8,paux.y+8,fill=color1)
    canvas1.create_oval(paux.x-5,paux.y-5,paux.x+5,paux.y+5,fill=color)
print("Initial error rate ",rate/len(ptab1))
for paux in ptab:
    n.adjust(paux.x,paux.y,paux.var)
#n.weight()
#print(n.calculate(p.x,p.y))
#n.adjust(p.x,p.y,p.var)
#print(n.calculate(p.x,p.y))
n.weight()
#print(p)
canvas.create_line(0,0,awidth,aheight,fill="blue")
rate=0
for paux in ptab1:
    color="green" if n.calculate(paux.x,paux.y)==paux.var else "red"
    rate=rate if n.calculate(paux.x,paux.y)==paux.var else rate+1
    color1="white" if paux.var==1 else "black"
    canvas.create_oval(paux.x-8,paux.y-8,paux.x+8,paux.y+8,fill=color1)
    canvas.create_oval(paux.x-5,paux.y-5,paux.x+5,paux.y+5,fill=color)
print("After training error rate ",rate/len(ptab1))
window.mainloop()
window1.mainloop()
