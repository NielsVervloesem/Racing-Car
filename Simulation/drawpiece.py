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

racetrack_file = 'pieces/11/'
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
pygame.display.flip()

drawRacetrack = True
while(drawRacetrack):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = list(pygame.mouse.get_pos())
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

for line in inner_line:
    line[0] = int((line[0] - 400)/multi)
    line[1] = int((line[1] - 400)/multi)
for line in outer_line:
    line[0] = int((line[0] - 400)/multi)
    line[1] = int((line[1] - 400)/multi)
racetrack = []
racetrack.append(inner_line)
racetrack.append(outer_line)

racetrack_file = 'pieces\\14\\racketrack3.pkl'

with open(racetrack_file, "wb") as f:
    pickle.dump(racetrack, f)
    f.close()
