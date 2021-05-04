import pickle
import neat
import pygame
from racetrack import Racetrack
from car import Car
import random
import sys
import time
import math
import visualize
import os
def get_coords(x,y,rand, r):
    #BOTTOM
    if(rand == 0):
        return x, y + r * math.sqrt(3)
    #TOP
    if(rand == 1):
        return x, y - r * math.sqrt(3)
    #TOP RIGHT
    if(rand == 2):
        return x + r * 2 * 3/4, y - r * math.sqrt(3) / 2,
    #TOP LEFTR
    if(rand == 3):
        return x - r * 2 * 3/4, y - r * math.sqrt(3) / 2
    #BOTTEM LEFT
    if(rand == 4):
        return x - r * 2 * 3/4, y + r * math.sqrt(3) / 2
    #BOTTOM RIGHT
    if(rand == 5):
        return x + r * 2 * 3/4, y + r * math.sqrt(3) / 2

def draw_regular_polygon(surface, color, vertex_count, radius, position):
    n, r = vertex_count, radius
    x, y = position
    bla = []
    for i in range(n):
        bla.append((int(x + r * math.cos(2 * math.pi * i / n)), int(y + r * math.sin(2 * math.pi * i / n))))

    pygame.draw.polygon(surface, color, [
        (x + r * math.cos(2 * math.pi * i / n), y + r * math.sin(2 * math.pi * i / n))
        for i in range(n)
    ],1)


    return bla

#Pygame init
background_colour = (0,0,0)
(width, height) = (800, 800)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Murphy simulation')
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 20)

screen.fill(background_colour)
pygame.display.flip()
clock = pygame.time.Clock()

multi = 5
big = 50 * multi

inner_line = []
outer_line = []

corners = (draw_regular_polygon(screen, (50,50,50), 6, big, (400,400)))
x,y = get_coords(400,400,0, big)
corners0 = (draw_regular_polygon(screen, (50,50,50), 6, big, (x,y)))

pygame.display.flip()
line = []

def save(line1, line2, file, name):
    for line in line1:
        line[0] = int((line[0] - 400)/multi)
        line[1] = int((line[1] - 400)/multi)
    for line in line2:
        line[0] = int((line[0] - 400)/multi)
        line[1] = int((line[1] - 400)/multi)
    racetrack = []

    racetrack.append(line1)
    racetrack.append(line2)

    racetrack_file = 'pieces\\'+str(file)+'\\racketrack' + str(name)+'.pkl'

    with open(racetrack_file, "wb") as f:
        pickle.dump(racetrack, f)
        f.close()
'''
line1 = []
line2 = []

file = 14
line1.append([corners[4][0], corners[4][1]])
line2.append([corners[5][0], corners[5][1]])


for i in range(len(line1)-1):
    pygame.draw.line(screen, (255,0,0), line1[i],line1[i+1], 1)

for i in range(len(line2)-1):
    pygame.draw.line(screen, (255,0,0), line2[i],line2[i+1], 1)   
pygame.display.flip()
time.sleep(2)
save(line2, line1, file,1)

corner = 3
file = 20
#smooth circle
#+210
for a in range(525,420, -1):
    width = big
    r = big*2
    x1 = r * math.cos(a/100)
    y1 = r * math.sin(a/100)
    line1.append([x1 + x , y1 + y])

for i in range(len(line1)-1):
    pygame.draw.line(screen, (255,0,0), line1[i],line1[i+1], 1)

for a in range(525, 420, -1):
    width = big
    r = big
    x1 = r * math.cos(a/100)
    y1 = r * math.sin(a/100)
    line2.append([x1 + x , y1 + y])

for i in range(len(line2)-1):
    pygame.draw.line(screen, (255,0,0), line2[i],line2[i+1], 1)   

#line2.append([corners[corner][0], corners[corner][1]])
pygame.display.flip()
time.sleep(2)

save(line2, line1, file,1)
line1 = []
line2 = []
'''



drawRacetrack = True
while(drawRacetrack):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = list(pygame.mouse.get_pos())
            print(type(pos))

            print(pos)
            inner_line.append(pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                drawRacetrack = False
            if event.key == pygame.K_LEFT:
                inner_line = inner_line[:-1]

    if(len(inner_line) > 2):
        screen.fill((0,0,0))
        pygame.draw.lines(screen, (255,255,255), False, inner_line)
        corners = (draw_regular_polygon(screen, (50,50,50), 6, big, (400,400)))

        pygame.display.flip()
drawRacetrack =  True
while(drawRacetrack):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = list(pygame.mouse.get_pos())
            outer_line.append(pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                drawRacetrack = False
            if event.key == pygame.K_LEFT:
                outer_line = outer_line[:-1]
    if(len(outer_line) > 2):
        screen.fill((0,0,0))
        pygame.draw.lines(screen, (255,255,255), False, inner_line)
        pygame.draw.lines(screen, (255,255,255), False, outer_line)
        corners = (draw_regular_polygon(screen, (50,50,50), 6, big, (400,400)))

        pygame.display.flip()



save(inner_line, outer_line, 34,2)
