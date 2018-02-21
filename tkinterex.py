import sys
import re
import math
print((sys.version_info))
import tkinter
from tkinter import Frame, Canvas, Label, Button, LEFT, RIGHT,  Tk
from tkinter import *
import random

class Neuro:

    def __init__(self,wx,wy):
        self.wx=wx
        self.wy=wy

    def calculate(self,x,y): 
        return 1/(1+math.exp(int(self.wx*float(x)+self.wy*float(y))))

    def adjust(self,x,y,val):
        aux = self.calculate(x,y)
        print("x "+str(x)+" y "+str(y)+" val "+str(val))
        print("Aux val: %d" % aux)
        e=val-aux
        print("Err val: %d" % e)
        self.wx=self.wx+e*x
        self.wy=self.wy+e*y
        self.weight()

    def weight(self):
        print(" wx " + str(self.wx) + " wy " + str(self.wy))

def pos(val):
    print(str(val.x) + "  " + str(val.y))
    canvas.create_oval(val.x-25,val.y-50,val.x+25,val.y+50,fill="blue")#a=50 b=100
    canvas.create_oval(val.x-10,val.y-10,val.x+10,val.y+10,fill="red")#cerc r=20
    print(entrytext.get())

def fct1():
    print("hei")

def fct2():
    print("nohei")
try:
    file=open("data.txt")
except IOError:
    print("No such file")
'''
data=[]
for i in file:
    aux=[]
    for j in re.split(" *\n*",i,flags=re.I):
        if len(j)>0:
            aux.append(j)
    if len(aux)>0:
        data.append(aux)
for i in data:
    print(i)
comp = Neuro(random.random(),random.random())
comp.weight()
for j in range(len(data)):
    i=data[j]
    comp.adjust(int(i[0]),int(i[1]),int(i[2]))
    print("calc " + str(comp.calculate(int(i[0]),int(i[1]))))
for j in range(len(data)):
    i=data[j]
    comp.adjust(int(i[0]),int(i[1]),int(i[2]))
    print("calc " + str(comp.calculate(int(i[0]),int(i[1]))))
comp.weight()
'''
maxx = 300
maxy = 300
window = tkinter.Tk()
#window.wm_geometry("500x400")
window.title("Aplication test")
frame = Frame(window)
frame.pack(fill="both", expand=True)
canvas = Canvas(frame, width=maxx, height=maxy)
canvas.pack(fill="both", expand=True)
canvas. create_line( 0, 0, maxx, maxy, width=4, fill="black")
canvas.create_rectangle(10,10,300,300, outline="black")
canvas.bind("<ButtonPress-1>", pos)
label=Label(frame, text='Tic Tac Toe Game', height=3, bg='black', fg='blue')
label.pack(fill="both", expand=True)
frameb=Frame(frame)
frameb.pack(fill="both", expand=True)
Start1=Button(frameb, text='Click here to start\ndouble player', height=4, command=fct1,bg='white', fg='purple')
Start1.pack(fill="both", expand=True, side=RIGHT)
Start2=Button(frameb, text='Click here to start\nsingle player', height=4, command=fct2,bg='purple', fg='white')
Start2.pack(fill="both", expand=True, side=LEFT)
entrytext = tkinter.StringVar()
tkinter.Entry(window, textvariable=entrytext).pack()

window.mainloop()
