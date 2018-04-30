# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import mpl_toolkits
import pylab;
import numpy
x=range(0,20)
mpl_toolkits.mplot3d.art3d()
t=numpy.arange(0.,3.14,0.1)
pylab.figure(1)
pylab.plot(t,t-t**3/6+t**5/120,"y")
pylab.figure(2)
pylab.plot(t,t-t**3/6+t**5/120-t**7/(120*6*7),"r")
pylab.figure(3)
pylab.plot(t,t-t**3/6+t**5/120-t**7/(120*6*7)+t**9/(120*6*7*8*9),"g")
pylab.figure(4)
pylab.plot(t,numpy.sin(t))
pylab.show(1,2,3,4)
