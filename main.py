# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 22:37:59 2020

@author: William
"""
from matplotlib import use
use("qt5agg")
from collections import deque
import matplotlib.pyplot as plt
from numpy import *
from subprocess import check_output
from platform import system
plt.style.use(['dark_background'])
x=linspace(0,60,60)

f=plt.figure()
c=1
ax=f.gca()
d=deque([0]*60)

title1 = "running"
title0 = "paused"
  
serv = 'jeuxvideo.com'
plt.ion()

def ping(s):
    global system
    systeme=system()
    if systeme == "Windows":
        ping = check_output(['ping', s, "-n", '1']).decode('cp850', errors="backslashreplace").split(' ')[15].split("=")[1]
    elif systeme == "Linux":
        ping = check_output(['ping', s, "-c", '1']).decode('cp850', errors="backslashreplace").split(' ')[7].split("=")[1] 
    elif systeme == "MacOS":
        pass 
    return int(ping)

def on_press(event):

    global c
    if event.key=="escape":
        c=0
        plt.close()
        
    if event.key==' ':
        c^=1
        if c:
            main() 
        else:
            ax.set_title(title0)

line,= ax.plot(x,d,"g-+",label="ping")
moy, = ax.plot(x,60*[mean([x for x in d if x>0])],"r--",label="average")
ax.set_title(title1)
ax.set_ylabel("ms")
plt.legend()

cz = f.canvas.mpl_connect('key_press_event',on_press)

def main():
    ax.set_title(title1)
    while c: 
        d.popleft()
        try:
            d.append(ping(serv))
        except:
            d.append(0)
        finally: 
            line.set_ydata(d)
            moy.set_ydata(60*[mean([x for x in d if x>0])])
            if any(d):
                ax.set_ylim(min([x for x in d if x>0])-1,max(d)+1)
            plt.gcf().canvas.draw_idle()
            plt.gcf().canvas.start_event_loop(1)

if __name__=="__main__":
    main()
