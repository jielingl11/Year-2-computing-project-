# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 15:01:26 2021

@author: jacqu
"""
import pylab as pl
import matplotlib.pyplot as plt

# try to plot out circles and play with the animation 

f = pl.figure()
patch1 = pl.Circle([0., 0.], 4, fc='r')
patch2 = pl.Circle([5., 2.], 4, fc='b')
ax = pl.axes(xlim=(-10, 10), ylim=(-10, 10))
ax.add_patch(patch1)
ax.add_patch(patch2)
ax.set_aspect("equal")
pl.show()

#%%

f = pl.figure()
patch = pl.Circle([0., 0.], 10, ec='b', fill=False, ls='solid')
ax = pl.axes(xlim=(-10, 10), ylim=(-10, 10))
ax.add_patch(patch)
ax.set_aspect("equal")
plt.show()

#%%
f = pl.figure()
patch = pl.Circle([-4., -4.], 3, fc='r')
ax = pl.axes(xlim=(-10, 10), ylim=(-10, 10))
ax.set_aspect("equal")
ax.add_patch(patch)

pl.pause(1)
patch.center = [4, 4]
pl.pause(5)
pl.show()

#%%

f = pl.figure()
patch = pl.Circle([-10., -10.], 1, fc='r')
ax = pl.axes(xlim=(-10, 10), ylim=(-10, 10))
ax.set_aspect("equal")
ax.add_patch(patch)


for i in range(-10, 10):
    patch.center = [i, i]
    pl.pause(0.001)
pl.show()