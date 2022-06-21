# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 10:46:00 2021

@author: jacqu
"""
import pylab as pl
import numpy as np
from Ball import *
import math


class Simulation(Ball):
    def __init__(self, balls, num_frames):
        self.balls= balls #all balls and the container  are saved in a list

# find the minimum time to collision in the list    
    def find_dt(self, no):
        ball= self.balls[no]
        find_dt=np.array([])
        n=0
        while n < len(self.balls): #check the time to collision of one ball with every other ball
            if n != no:
                dt= ball.time_to_collision(self.balls[n])
                find_dt = np.append(find_dt, dt)
                n= n+1
            else:
                n= n+1 
                continue
        min_dt= min(i for i in find_dt if i is not None)
        collide_with_ballno= np.where(find_dt==min_dt)
        return min_dt, collide_with_ballno
            
 # save dt, t, v, KE and p at each frame into arrays        
    def next_collision(self):
        all_dt= np.array([]) # time to collision
        all_r= np.array([]) # position
        all_v= np.array([]) # velocity 
        all_KE= np.array([]) # kinetic energy 
        all_p= np.array([]) # momentum

      
        for no in range(len(self.balls)):
            ball= self.balls[no]
            dt, collide_with_ballno= Simulation.find_dt(self, no) # find which ball is colliding with the ball
            all_dt= np.append(all_dt, dt)
            other_no= collide_with_ballno[0][0]+1
            ball._r= ball.move(dt)  # move the balls to the new position
            ball.v= ball.collide(self.balls[other_no]) # update the new velocity 
            all_r= np.append(all_r, ball._r)
            all_v= np.append(all_v, ball.v)
            all_KE= np.append(all_KE, ball.kinetic_energy())
            all_p= np.append(all_p, ball.momentum())
  
        return all_dt, all_r, all_v, all_KE, all_p
 
# save dt, r, v, KE, p into matrices so that data can be accessed easier 
    def collision(self, num_frames):
        self.dt= np.array([])
        self.r= np.array([])
        self.v= np.array([])
        self.KE= np.array([])
        self.p= np.array([])
        
        for i in range(len(self.balls)):
            self.r= np.append(self.r, self.balls[i]._r)
            self.v= np.append(self.v, self.balls[i].v)
            self.KE= np.append(self.KE, self.balls[i].kinetic_energy())
            self.p= np.append(self.p, np.sqrt((self.balls[i].v* self.balls[i].m)**2))
        
        
        for i in range(num_frames):
            all_dt, all_r, all_v, all_KE, all_p= Simulation.next_collision(self)
            self.dt= np.append(self.dt, all_dt)
            self.r= np.append(self.r, all_r)
            self.v= np.append(self.v, all_v)
            self.KE= np.append(self.KE, all_KE)
            self.p= np.append(self.p, all_p)

            
        self.dt= np.reshape(self.dt, (num_frames, len(self.balls)))
        self.r= np.reshape(self.r, (num_frames+1, 2*(len(self.balls))))
        self.v= np.reshape(self.v, (num_frames+1, 2*(len(self.balls))))
        self.KE= np.reshape(self.KE, (num_frames+1, (len(self.balls))))
        self.p= np.reshape(self.KE, (num_frames+1, (len(self.balls))))
        
        return self.dt, self.r, self.v, self.KE, self.p

    
# find v that the ball collides with the container in order to calculate the pressure 
    def collision_with_con(self):
        con_v= np.array([])
        t= np.array([])
        for no in range(len(self.balls)):
            ball= self.balls[no]
            dt, collide_with_ballno= Simulation.find_dt(self, no)
            other_no= collide_with_ballno[0][0]+1
            if other_no == len(self.balls)-1:
                con_v= np.append(con_v, ball.v)
                con_v= np.append(con_v, ball.collide(self.balls[-1]))
                t= np.append(t, dt)
                
            ball._r= ball.move(dt)
            ball.v= ball.collide(self.balls[other_no])
        return con_v, t
            
    def collision_with_con_num(self, num_frames):
        v= np.array([])
        t= np.array([])
        for i in range(num_frames):
            con_v, dt= Simulation.collision_with_con(self)
            v= np.append(v, con_v)
            t= np.append(t, dt)
        return v, t
                           
        
    def run(self, num_frames, animate=False):
        if animate:
            f = pl.figure()
            ax = pl.axes(xlim=(-10, 10), ylim=(-10, 10))
            ax.set_aspect("equal")
            for ball in self.balls:
                ax.add_patch(ball.get_patch())
        for frame in range(num_frames):
            self.next_collision()
            if animate:
                pl.pause(0.5)
        if animate:
            pl.show()
            

        
        # if animate:
            # f = pl.figure()
            # ax = pl.axes(xlim=(-10, 10), ylim=(-10, 10))
            # plot_ball= ball.plot_ball(num_frames)
            # plot_container= container.plot_container()
            # ax.add_artist(plot_container)
            # ax.add_patch(plot_ball)
            # ax.set_aspect("equal")
            
            # f = pl.figure()
            # ax = pl.axes(xlim=(-10, 10), ylim=(-10, 10))
            # i=0
            # while i < len(self.balls)-1:
            #     ball= self.balls[i]
            #     container= self.balls[-1]
            #     plot_ball= ball.plot_ball(num_frames)
            #     plot_container= container.plot_container()
            #     ax.add_artist(plot_container)
            #     ax.add_patch(plot_ball)
            #     ax.set_aspect("equal")
            #     i=i+1 
                
            
            # for frame in range(num_frames):
            #     n=0
            #     while n< len(self.balls)-1:
            #         ball= self.balls[n]
            #         # vel_all= np.array(ball.vel())
            #         pos_i= ball.pos()
            #         self.next_collision(n)
            #         pos_f= ball.pos()
            #         print(pos_i)
            #         print(pos_f)
            #         dr_hat= (pos_f- pos_i)/np.linalg.norm(pos_f- pos_i)
            #         pos= pos_i
            #         # vel_all= np.append(vel_all, ball.vel())
                    
            #         # while sum((pos-pos_i)**2)< sum((pos_f-pos_i)**2):
            #         #     plot_ball.center = pos+ dr_hat
            #         #     pl.pause(0.001)
            #         #     pos= pos+ dr_hat 
            #         n=n+1   
          
        


        
        # def pressure(self):
        #     i=0
        #     while i< len(vel_all)+1:
        #         v_before= vel_all[i]
        #         v_after= vel_all[i+1]
        #         # dt= (np.sqrt(sum(dr_before**2))/np.sqrt(sum(v_before**2)))+ (np.sqrt(sum(dr_after**2))/np.sqrt(sum(v_after**2)))
        #         dt= time[i]+time[i+1]
        #         dp= ball.m* np.sqrt(sum(v_after- v_before)**2)
        #         F= dp/dt
        #         P= F/(2* np.pi* container.radius)
        #         print('Pressure', P)
        #         print('')
        #         i=i+1
