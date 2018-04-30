import turtle
import math
def square(myTurtle,x,y): 
   myTurtle.penup()
   myTurtle.setposition(0,0)
   myTurtle.pendown()
   myTurtle.forward(x)
   myTurtle.left(90)
   myTurtle.forward(y)
   myTurtle.left(90)
   myTurtle.forward(x)
   myTurtle.left(90)
   myTurtle.forward(y)
for i in range(0,5):
   square(turtle.Turtle(),30*i,45*i)
def triangle(x,y): 
   dimN=15
   dimP=math.sqrt(math.pow(dimN,2)+math.pow(dimN/2,2))
   myTurtle.penup()
   myTurtle.setposition(x,y)
   myTurtle.pendown()
   myTurtle.forward(dimP)
   myTurtle.left(120)
   myTurtle.forward(dimP)
   myTurtle.left(120)
   myTurtle.forward(dimP)
   turtle.right(150)
myTurtle=turtle.Turtle()
for i in range(0,15,1):
   triangle(i,i+1);
ts=turtle.getscreen();
ts.getcanvas().postscript(file="duck.eps")
