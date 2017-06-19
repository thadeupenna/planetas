#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  planetagame.py
#  
#  Copyright 2016 Thadeu Penna <tjpp@dogfish>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import pygame
import sys
from pygame.locals import * 
import numpy as np
import math 

class Planeta:
	counter=0
	def __init__(self,name,m,x,y,vx,vy):
		self.x=x
		self.y=y
		self.vx=vx
		self.vy=vy
		self.mass=m
		self.name=name
		self.r0=np.sqrt(x**2+y**2)
		Planeta.counter=Planeta.counter+1
		
	def distance(self):
		return np.sqrt(self.x**2+self.y**2) 
		
	def move(self):
		self.ax=-GM*self.x/self.distance()**3
		self.ay=-GM*self.y/self.distance()**3
		self.x=self.x+self.vx*dt+0.5*self.ax*dt**2
		self.y=self.y+self.vy*dt+0.5*self.ay*dt**2
		self.vx=self.vx+self.ax*dt
		self.vy=self.vy+self.ay*dt

	def force(self):
		return GM*self.mass/self.distance()**2
		
	def __sub__(self,other):
		return np.sqrt((self.x-other.x)**2+(self.y-other.y)**2)
		
	def __str__(self):
		return '%s em %f,%f a %f do Sol, a %f AU/year, periodo %f years, força de %f MT*AU/year²\n' \
				% (self.name,self.x,self.y,self.distance(),self.force())	

GM=4*np.pi**2		
dt=4.e-4
terra=Planeta("Terra",1,1,0,0,2*np.pi)
pygame.init()
resolution = 800
screen = pygame.display.set_mode((resolution,resolution),DOUBLEBUF)
myfont = pygame.font.Font(None,60)
pygame.display.set_caption('Sistema Solar')
space = pygame.image.load('milkyway.png').convert()
space = pygame.transform.scale(space,(resolution,resolution))
planet = pygame.image.load("planeta.png").convert_alpha()
sun = pygame.image.load("sun.png").convert_alpha()
sun = pygame.transform.scale(sun,(100,100))
sunw,sunh=sun.get_size()
planw,planh=planet.get_size()
planet = pygame.transform.scale(planet,(50,50))
planw,planh=planet.get_size()
fixedplanet = pygame.transform.rotate(planet,0)
angulo=0

def wrap_angle(angle):
	return angle % 360

	
while True:
	for event in pygame.event.get():
		if event.type in (QUIT, KEYDOWN):
			sys.exit()
	screen.blit(space, (0,0))
	# screen.blit(fixedplanet,(0,0))
	screen.blit(sun, ((resolution-sunw)/2,(resolution-sunh)/2))
	xant,yant=terra.x,terra.y
	terra.move()
	dx = terra.x - xant
	dy = terra.y - yant
	angulo=math.atan2(dy,dx)
	angulo=wrap_angle(-math.degrees(angulo)+90)
	dayplanet = pygame.transform.rotate(planet,angulo)
	screen.blit(dayplanet,(terra.x*(resolution-planw)/2+(resolution-planw)/2,terra.y*(resolution-planw)/2+(resolution-planw)/2))
	pygame.display.update()
