# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 15:25:24 2021

@author: jacqu
"""
import pylab as pl
from Ball import *
from Simulation import *
import random
from numpy.random import seed
from numpy.random import randn

# randomly generate the velocity of balls 
# arrange balls spirally 
def random_generate_ball(num): 
    vx= np.random.normal(0,3, size=(num))
    vy= np.random.normal(0,3, size=(num))
    theta= np.linspace(5*np.pi, 20*np.pi, num) # spiral curve
    r= 9*theta/(20*np.pi)
    
    x_= np.array([])
    y_= np.array([])
    
    for i in range(num):
        x= r*np.cos(theta)
        y= r*np.sin(theta)
        x_= np.append(x_,x)
        y_= np.append(y_,y)
    

    balls= []      
    for j in range(num):  
        ball= Ball(x=x_[j], y=y_[j], vx=vx[j], vy=vy[j], radius=0.1, m=0.1)
        balls.append(ball)
        
    return balls




balls= random_generate_ball(200)
container= Ball(x=0, y=0, vx=0, vy=0, radius=-10, m=1e4)
balls.append(container)
i = Simulation(balls, num_frames=10)
dt,r,v, kinetic, p= i.collision(num_frames=10)
i.run(10, animate=True)


# theta= np.linspace(5*np.pi, 20*np.pi, 200)
# r= 9*theta/(20*np.pi)
# plt.plot(r*np.cos(theta), r*np.sin(theta))

# a sigle ball is moving inside a container 

# container= Ball(x=0, y=0, vx=0, vy=0, radius=-10, m=1e5) 
# ball= Ball(x=9, y=0, vx=-1, vy=0, radius=1, m=1)
# balls=[ball, container]
# i = Simulation(balls, num_frames=10)
# # dt,r,v,kinetic, p= i.collision(10)
# vc, t= i.collision_with_con_num(10)
# i.run(10, animate=True)


#%% Plot the histogram of ball distance from container centre

r_= np.array([])
pos= []

for i in range(len(balls)-1):
    ball= balls[i]
    pos.append(ball._r)
    r= sum(ball._r**2)
    r_= np.append(r_, r)

plt.hist(r_, bins= 20, histtype='step', lw=1, color= 'black')
plt.xlabel('Distance each ball extends from the centre')
plt.ylabel('Frequency')
# plt.title('Distance each ball extends from the central position')

#%% Plot the histogram of inter-ball separation.

dis= np.array([])
for i in range(len(pos)):
    r1= pos[i]
    n= i+1
    while n< len(pos):
        r2= pos[n]
        dr= np.sqrt(sum((r2-r1)**2))
        dis= np.append(dis, dr)
        n= n+1

plt.hist(dis, bins= 20, histtype='step', lw=1, color= 'black')
plt.xlabel('Distance between each pair of balls')
plt.ylabel('Frequency')


#%% System kinetic energy versus time

total_time= sum(dt)
min_total_time= min(total_time)

num_frames= 15
time= np.linspace(0, min_total_time, num_frames)
dt_trans= np.transpose(dt)

# summing dt to find out the exact time that collisions are performed 
t= np.array([])

for i in range(len(dt_trans)):
    t_sub= np.array([])
    n=0
    for j in range(len(dt_trans[0])):
       n= n+ dt_trans[i][j]
       t_sub= np.append(t_sub,n)
    t= np.append(t, t_sub)
        
t= np.reshape(t, (len(balls), num_frames))

kinetic_trans= np.transpose(kinetic)
Kinetic= np.array([])
n=0
while n< len(balls):
    for i in range(len(time)):
        T= time[i] 
        delta= t[n]-T
        min_delta= np.where(delta >= 0, delta, np.inf).argmin() 
        k= kinetic_trans[n][min_delta]
        Kinetic= np.append(Kinetic, k)
    n=n+1
    
Kinetic_new= np.reshape(Kinetic, (len(balls), num_frames))
K= sum(Kinetic_new[:-1])
plt.plot(time[:], K[:])
plt.ylim(-100, 100)
plt.xlabel('Time (s)')
plt.ylabel('System Kinetic Energy (J)')

#%%
# num_frames= 101
# time= np.linspace(0, min_total_time, num_frames)

# K_trans= np.transpose(kinetic)
# ave_KE= sum(K_trans)
# plt.plot(time[9:], ave_KE[9:])
# plt.ylim(500, 1000)
# plt.xlabel('Time')
# plt.ylabel('System Kinetic Energy')

#%% Momentum versus time
P_trans= np.transpose(p)
P= np.array([])
n=0
while n< len(balls):
    for i in range(len(time)):
        T= time[i]
        delta= t[n]-T
        min_delta= np.where(delta >= 0, delta, np.inf).argmin() 
        p= P_trans[n][min_delta]
        P= np.append(P, p)
    n=n+1

  
P_new= np.reshape(P, (len(balls), num_frames))
PP= sum(P_new)
plt.plot(time, PP)
plt.xlabel('Time (s)')
plt.ylabel('$Momentum (kg m s^{-1})$')
plt.ylim(-100, 100)


#%% Pressure versus temperature

P_new2= np.transpose(P_new)
i=0
pressure= np.array([])

while i< num_frames-1:
    dp= P_new2[i+1]- P_new2[i] 
    dt= time[i]+time[i+1]
    F= dp/dt
    P= F/(2* np.pi* -container.radius)
    pressure= np.append(pressure, P)
    i= i+1

pressure2= np.transpose(np.reshape(pressure, (num_frames-1, len(balls))))
pressure_new= abs(sum(pressure2))

kb= 1.38*10**-23
Tem= K[1:]/(kb* len(balls))

plt.plot(Tem[2:], pressure_new[2:], 'o')
plt.ylabel('$Pressure (N m^{-2})$')
plt.xlabel('Temperature (K)')
plt.ylim(-0.5,0.5)
fit, cov= np.polyfit(Tem[2:], pressure_new[2:], 1, cov= True)
y=np.poly1d(fit)
plt.plot(Tem[1:],y(Tem[1:]))

#%% Pressure versus temperature with changing the size of the container 

x= np.linspace(1, 10, 200)
G1= 1/400
G2= 1/225
G3= 1/100
# G4= 1/25
plt.plot(x, G1*x, label= 'r=20m')
plt.plot(x, G2*x, label= 'r=15m')
plt.plot(x, G3*x, label= 'r=10m')
# plt.plot(x, G4*x, label= 'r=5m')

plt.xlabel('Temperature (K)')
plt.ylabel('$Pressure (N m^{-2})$')
plt.legend()

ax = plt.gca()
ax.axes.xaxis.set_ticks([])
ax.axes.yaxis.set_ticks([])

#%% Plot the histogram of ball speeds
import scipy.stats as stats


v2= v[10][:]
v_dis= np.array([])
for i in range(201):
    v_= np.sqrt(v2[i]**2+ v2[i+1]**2)
    v_dis= np.append(v_dis, v_)




maxwell = stats.maxwell
data = maxwell.rvs(loc=0, scale=2, size=10000)

params = maxwell.fit(v_dis, floc=0)
plt.hist(v_dis, bins=20, density=True)
x = np.linspace(0, 12, 100)
plt.plot(x, maxwell.pdf(x, *params), lw=1)
plt.xlabel('$speed (m s^{-1})$')
plt.ylabel('frequency')
plt.show()
