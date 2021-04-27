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
from piece import Piece
'''
TOP
y_offset = y_offset - r * math.sqrt(3)

TOP LEFT
y_offset = y_offset - r * math.sqrt(3) / 2
x_offset = x_offset + r * 2 * 3/4

BOTTEM LEFT
y_offset = y_offset + r * math.sqrt(3) / 2
x_offset = x_offset + r * 2 * 3/4

BOTTEM
y_offset = y_offset + r * math.sqrt(3)

BOTTEM RIGHT
y_offset = y_offset - r * math.sqrt(3) / 2
x_offset = x_offset + r * 2 * 3/4

TOP RIGHT
y_offset = y_offset - r * math.sqrt(3) / 2
x_offset = x_offset - r * 2 * 3/4
'''


def get_coords(x,y,r,xc,yc):
    rand = random.randrange(6)
    #BOTTOM
    if(rand == 0):
        return x, y + r * math.sqrt(3),xc,yc+1,2
    if(rand == 1):
        return x, y - r * math.sqrt(3),xc,yc-1,5
    #TOP RIGHT
    if(rand == 2):
        return x + r * 2 * 3/4, y - r * math.sqrt(3) / 2,xc+1,yc-1,3
    #TOP LEFTR
    if(rand == 3):
        return x - r * 2 * 3/4, y - r * math.sqrt(3) / 2,xc-1,yc,1
    #BOTTEM LEFT
    if(rand == 4):
        return x - r * 2 * 3/4, y + r * math.sqrt(3) / 2,xc-1,yc+1,6
    #BOTTOM RIGHT
    if(rand == 5):
        return x + r * 2 * 3/4, y + r * math.sqrt(3) / 2,xc+1,yc,5

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

x_offset = width / 2
y_offset = height / 2

outer_line = []
outer_line2 = []

grid = []
grid2 = []

def draw_regular_polygon(surface, color, vertex_count, radius, position):
    n, r = vertex_count, radius
    x, y = position
    pygame.draw.polygon(surface, color, [
        (x + r * math.cos(2 * math.pi * i / n), y + r * math.sin(2 * math.pi * i / n))
        for i in range(n)
    ],1)
def isRepeat(grid, x,y):
    for point in grid:
        if(point[0] == x and point[1] == y):
            return True
    return False

r = 50
x = 0
y = 0

for i in range(1):
        x_offset2, y_offset2, x2, y2,out = get_coords(x_offset, y_offset, r,x,y)
        while(isRepeat(grid,x2,y2)):
            x_offset2, y_offset2, x2,y2,out = get_coords(x_offset, y_offset, r,x,y)

        grid.append((x2,y2))
        grid2.append(Piece((x_offset2,y_offset2),out))

        x_offset = x_offset2
        y_offset = y_offset2
        x = x2
        y = y2
aaa =[]
for a in grid2:
    draw_regular_polygon(screen, (255,255,255), 6, r, a.center)
    aaa.append((a.center[0] + r * math.cos(2 * math.pi * i / a.out), a.center[1] + r * math.sin(2 * math.pi * i / a.out)))
print(len(aaa))
for a in aaa:
    print(a)
while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
    
    pygame.draw.lines(screen, (255,0,0), True, aaa)

    pygame.display.update()
    time.sleep(0.5)

'''
car_x = racetrack.start[0][0]
car_y = racetrack.start[0][1]
car = Car(carname,car_x, car_y,120)

with open(model_path, "rb") as f:
    winner = pickle.load(f)
dt = 0.17
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    #Draw racetrack
    pygame.draw.lines(screen, (255,255,255), True, racetrack.outer_line)
    pygame.draw.lines(screen, (255,255,255), True, racetrack.inner_line)

    for checkpoint in racetrack.checkpoints:
        pygame.draw.circle(screen, (0,255,0), checkpoint, 3)

    #Loop cars and make them drive
    if(car.is_alive):
        #180, -90, -40, -15, 0, 15, 40, 90
        sensors = car.radar.calculate_distance(racetrack)
        inputdata = []

        #Collect the correct amount of sensors data
        if(int(car.name) > 7):
            inputdata.append(sensors[0]) #180
        if(int(car.name) > 5):
            inputdata.append(sensors[1]) #-90
        if(int(car.name) > 3):
            inputdata.append(sensors[2]) #-40

        inputdata.append(sensors[3]) #-15
        inputdata.append(sensors[4]) #0
        inputdata.append(sensors[5]) #15

        if(int(car.name) > 3):
            inputdata.append(sensors[7]) #40
        if(int(car.name) > 5):
            inputdata.append(sensors[7]) #90

        output = winner_model.activate(inputdata)
        print(inputdata)
        print(output)

        if(len(output) > 2):
            softmax_result = softmax(output)
            class_output = np.argmax(((softmax_result / np.max(softmax_result)) == 1).astype(int))
            
            if(class_output == 0):
                car.velocity[0] = car.velocity[0] + 1
                car.steering = 0

            if(class_output == 1):
                car.velocity[0] = car.velocity[0] - 1
                car.steering = 0

            if(class_output == 2):
                if(car.steering < 45):
                    car.steering = car.steering + 5

            if(class_output == 3):
                if(car.steering > -45):
                    car.steering = car.steering - 5

            if(class_output == 4):
                if(car.steering < 45):
                    car.steering = car.steering + 15

            if(class_output == 5):
                if(car.steering > -45):
                    car.steering = car.steering - 15

            if(class_output == 6):
                if(car.steering < 45):
                    car.steering = car.steering + 45

            if(class_output == 7):
                if(car.steering > -45):
                    car.steering = car.steering - 45
        else:
            car.velocity[0] = 0 #output[0] * carspeed
            if(a == 0):
                a = 1
                car.steering = 45#output[1] * 90 - 45            
            if(a == 1):
                a = 0
                car.steering = -45#output[1] * 90 - 45
        car.update(dt)

        #Kill off bad cars
        if (racetrack.hit(car)):
            car.is_alive = False

        #car.check_passed(racetrack)
        if(car.checkpoint_passed == 3):
            car.is_alive = False
            run = False
        
        #Draw each cars (no radar lines because of lag)
        for line in car.radar.radar_lines:
            pygame.draw.line(screen, (0,0,255), line[0], line[1], 1)
        
        pygame.draw.circle(screen, (255,0,0), (int(car.position.x), int(car.position.y)), car.length)
    
    #update screen
    pygame.display.update()
    #screen.fill(background_colour)
    clock.tick(60)
    time.sleep(0.1)
'''