# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 21:12:29 2016

@author: duicul
"""
import math
import numpy
import matplotlib.pyplot as pt
from mpl_toolkits.mplot3d import Axes3D
fig = pt.figure(1)
ax = fig.gca(projection='3d')
X=numpy.arange(0,2*math.pi,0.2)
Y=numpy.arange(0,2*math.pi,0.2)
X, Y = numpy.meshgrid(X,Y)
Z=X+Y
ax.plot_surface(X,Y,-Z,rstride=5,cstride=5)
ax.plot_surface(X,Y,Z,rstride=5,cstride=5,cmap='coolwarm')
x1=numpy.linspace(-1,6.28)
y1=numpy.linspace(-1,6.28)
pt.figure(2)
pt.plot(3*numpy.sin(x1),14*numpy.cos(y1))
pt.show()
