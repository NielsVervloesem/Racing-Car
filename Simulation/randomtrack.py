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

def get_coords(x,y,r,xc,yc):
    rand = random.randrange(6)
    #BOTTOM
    if(rand == 0):
        return x, y + r * math.sqrt(3),xc,yc+1,4
    #TOP
    if(rand == 1):
        return x, y - r * math.sqrt(3),xc,yc-1,1
    #TOP RIGHT
    if(rand == 2):
        return x + r * 2 * 3/4, y - r * math.sqrt(3) / 2,xc+1,yc-1,2
    #TOP LEFTR
    if(rand == 3):
        return x - r * 2 * 3/4, y - r * math.sqrt(3) / 2,xc-1,yc,0
    #BOTTEM LEFT
    if(rand == 4):
        return x - r * 2 * 3/4, y + r * math.sqrt(3) / 2,xc-1,yc+1,5
    #BOTTOM RIGHT
    if(rand == 5):
        return x + r * 2 * 3/4, y + r * math.sqrt(3) / 2,xc+1,yc,3

#Pygame init
background_colour = (0,0,0)
(width, height) = (1000, 1000)

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
    corners = []
    for i in range(n):
        corners.append((int(x + r * math.cos(2 * math.pi * i / n)), int(y + r * math.sin(2 * math.pi * i / n))))

    pygame.draw.polygon(surface, color, [
        (x + r * math.cos(2 * math.pi * i / n), y + r * math.sin(2 * math.pi * i / n))
        for i in range(n)
    ],1)

    returns corners

def isRepeat(grid, x,y):
    threshold = 3
    for point in grid:
        if(point[0] == x and point[1] == y):
            return True

    if(x > threshold or x < -threshold):
        return True

    if(y > threshold or y < -threshold):
        return True

    return False


r = 50
x = 0
y = 0
resetoffset = False

loop = 0
while(loop < 40):
        xCenter, yCenter, gridX, gridY, inp = get_coords(x_offset, y_offset, r,x,y)
        infinity = 0
        while(isRepeat(grid,gridX,gridY)):
            #inf loop problem
            infinity = infinity + 1
            xCenter, yCenter, gridX, gridY, inp = get_coords(x_offset, y_offset, r,x,y)
            if(infinity > 20):
                loop = 0
                grid = []
                grid2 = []
                infinity = 0
                x_offset = 500
                y_offset = 500
                x = 0
                y = 0

        grid.append((gridX,gridY))
        grid2.append(Piece((xCenter,yCenter),inp))
        loop = loop + 1
        x_offset = xCenter
        y_offset = yCenter
        x = gridX
        y = gridY


corners = []
color = 50

for piece in grid2:
    corners = (draw_regular_polygon(screen, (0,0,0), 6, r, piece.center))
    inCorner1 = piece.input
    inCorner2 = inCorner1 + 1
    if(inCorner2 > 5):
        inCorner2 = 0

    pygame.draw.line(screen, (0, 255 - color,0+color), corners[inCorner1], corners[inCorner2], 3)    

    piece.updateinput((corners[inCorner1], corners[inCorner2]))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
innerlines = []
outerlines = []
for i in range(len(grid2)):
    try:
        innerline, outerline = grid2[i].generateCellTrack(grid2[i+1].inputcorners, grid2[i+1].input)
        innerlines.append(innerline)
        outerlines.append(outerline)
    except:
        print("An exception occurred")


while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
    for line in innerlines:
        pygame.draw.lines(screen, (255,0,0), False, line)

    for line in outerlines:
        pygame.draw.lines(screen, (255,0,0), False, line)

    pygame.draw.circle(screen, (255,0,0), (500,500), 5)

    pygame.display.update()

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