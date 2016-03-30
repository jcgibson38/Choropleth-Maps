import numpy as np

def foo(x):
    return min(int(256*x),255)

def f(ratio,fullcolor,emptycolor):
    return (1-ratio)*emptycolor + ratio*fullcolor

def tohex(rgbcolor):
    r,g,b = rgbcolor
    s = '#'
    s +=  hex(foo(r))[2:].zfill(2)
    s +=  hex(foo(g))[2:].zfill(2)
    s +=  hex(foo(b))[2:].zfill(2)
    return s

def colormered(ratio):
    red = np.array([1,0,0],dtype=float)
    white = np.array([1,1,1],dtype=float)
    return tohex(f(ratio,red,white))

def colormeblue(ratio):
    blue = np.array([0,0,1],dtype=float)
    white = np.array([1,1,1],dtype=float)
    return tohex(f(ratio,blue,white))

def colormegreen(ratio):
    green = np.array([0,1,0],dtype=float)
    white = np.array([1,1,1],dtype=float)
    return tohex(f(ratio,green,white))

def colormeredgreen(ratio):
    green = np.array([0,1,0],dtype=float)
    red = np.array([1,0,0],dtype=float)
    return tohex(f(ratio,green,red))
