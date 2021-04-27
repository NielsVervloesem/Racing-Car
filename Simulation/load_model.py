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

drawRacetrack =  True
carspeed = 20 * 1
carname = 8
model_path = 'Models\Model.pkl'
config_file = 'Models\Model.txt'
racetrack_file = 'racetracks\\racketrack.pkl'

with open(racetrack_file, "wb") as f:
    pickle.dump(racetrack, f)
    f.close()
    
#Pygame init
background_colour = (0,0,0)
(width, height) = (1500, 1000)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Murphy simulation')
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 20)

screen.fill(background_colour)
pygame.display.flip()
clock = pygame.time.Clock()

racetrack = Racetrack(width, height, random.randint(160,170))
a = 0
if(not drawRacetrack):
    with open(racetrack_file, "rb") as f:
        racetrack = pickle.load(f)

# Unpickle saved winner
with open(model_path, "rb") as f:
    winner = pickle.load(f)

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_file)

winner_model = neat.nn.FeedForwardNetwork.create(winner, config)

nodes = {0:'Speed',1:'Angle'}
visualize.draw_net(config, winner, True,node_names=nodes, filename="test")

if(drawRacetrack):
    racetrack.inner_line = []
    racetrack.outer_line = []
    racetrack.checkpoints = []
    while(drawRacetrack):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                racetrack.inner_line.append(pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    drawRacetrack = False
                if event.key == pygame.K_LEFT:
                    racetrack.inner_line = racetrack.inner_line[:-1]

        if(len(racetrack.inner_line) > 2):
            screen.fill((0,0,0))
            pygame.draw.lines(screen, (255,255,255), False, racetrack.inner_line)
            pygame.display.flip()

    drawRacetrack =  True
    while(drawRacetrack):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                racetrack.outer_line.append(pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    drawRacetrack = False
                if event.key == pygame.K_LEFT:
                    racetrack.outer_line = racetrack.outer_line[:-1]
        if(len(racetrack.outer_line) > 2):
            screen.fill((0,0,0))
            pygame.draw.lines(screen, (255,255,255), False, racetrack.inner_line)
            pygame.draw.lines(screen, (255,255,255), False, racetrack.outer_line)
            pygame.display.flip()

    drawRacetrack =  True
    while(drawRacetrack):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                racetrack.checkpoints.append(pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    drawRacetrack = False
                if event.key == pygame.K_LEFT:
                    racetrack.checkpoints = racetrack.checkpoints[:-1]
            if(len(racetrack.checkpoints) >= 2 and len(racetrack.checkpoints) % 2 == 0):
                for i in range(0,len(racetrack.checkpoints),2):
                    print(i)
                    screen.fill((0,0,0))

                    pygame.draw.lines(screen, (255,255,255), False, racetrack.inner_line)
                    pygame.draw.lines(screen, (255,255,255), False, racetrack.outer_line)
                    p1 = (int(racetrack.checkpoints[i][0]),int(racetrack.checkpoints[i][1]))
                    p2 = (int(racetrack.checkpoints[i+1][0]),int(racetrack.checkpoints[i+1][1]))
                    pygame.draw.line(screen, (0,255,0), p1, p2, 3)                    
                    pygame.display.flip()

    drawRacetrack =  True
    while(drawRacetrack):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                racetrack.start[0] = (pos)
                drawRacetrack = False

with open(racetrack_file, "wb") as f:
    pickle.dump(racetrack, f)
    f.close()

print(racetrack.start)
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
