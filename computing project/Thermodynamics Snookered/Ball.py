# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 23:26:54 2021

@author: jacqu
"""
import pylab as pl
import numpy as np
import matplotlib.pyplot as plt


class Ball:

    def __init__(self, x, y, vx, vy, radius, m):
        self._r = np.array([x, y])
        self.v = np.array([vx, vy])
        self.radius = radius
        self.m = m
        self.patch= pl.Circle([self._r[0], self._r[1]], self.radius, fc='r')

    def pos(self):
        return self._r

    def vel(self):
        return self.v
# move the ball and the patch to the new position
    def move(self, dt):
        # dt= self.time_to_collision(self, other)
        pos_new = self._r + self.v*dt
        self.patch.center= pos_new
        self._r= pos_new
        return pos_new

# set the radius of container as negative
# take the smallest positive value

    def time_to_collision(self, other):
        R = self._r - other._r
        V = self.v - other.v
        Radius = self.radius + other.radius
        

        dis = np.dot(R,V)**2 - np.dot(V,V)* (np.dot(R,R) - Radius**2)

        
        if dis< 1e-10:   # this is to avoid floating point 
            dis=0
        dt1 = (-np.dot(R,V) + np.sqrt(dis))/np.dot(V,V)
        dt2 = (-np.dot(R,V) - np.sqrt(dis))/np.dot(V,V)

        small= 1e-10
        
        if dt1 > small and dt2 > small:
            dt = min(dt1, dt2)
            return dt
        
        elif dt1==0 and dt2>0:
            return dt2
        
        elif dt2==0 and dt1>0:
            return dt1

        elif dt1 < small and dt2 > small:
            return dt2

        elif dt1 > small and dt2 < small:
            return dt1

        else:
            return None

# find the velocity after a collision
    def collide(self, other):
        vf = ((self.m - other.m) * self.v/(self.m + other.m)) + ((2*other.m*other.v)/(self.m + other.m))
        return vf

# create patches for balls and container 
    def get_patch(self):
        if self.radius>0: 
            self.patch= pl.Circle(self.pos(), self.radius, fc='r')
            return self.patch
        else:
            self.patch= pl.Circle(self.pos(), -self.radius, ec='b', fill=False, ls='solid')
            return self.patch

    def kinetic_energy(self):
        KE = 0.5* self.m * sum((self.v)**2) 
        return KE
    
    def momentum(self):
        P= self.m* self.v
        return P