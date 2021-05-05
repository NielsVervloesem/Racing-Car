import pygame
import os
from racetrack import Racetrack
from randomtrack import RandomRacetrack
from car import Car
from math import sin, radians, degrees, copysign
import time
import datetime
import neat
import sys
import pickle
import random
import numpy as np
from neat.math_util import softmax
from random import randrange

#MODEL PARAMS INIT
name = "speed"
config_path = "./config-feedforward.txt"
carMaxSpeed = 20 * 1
carSensors = 8
drawRacetrack = True
racetrack_file = 'modelsV3\\racketrackV1.pkl'

def run(genomes, config):
    global racetrack
    global radar_lenght
    radar_lenght = 50
    counter = 0
    racetrack = RandomRacetrack(width, height, 15)

    networks = []
    cars = []

    car_x = int(racetrack.start[0])
    car_y = int(racetrack.start[1])

    for id, genome in genomes:
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(network)
        genome.fitness = 0
        car = Car(carSensors, car_x, car_y, radar_lenght, racetrack.startAngle)
        cars.append(car)


    global generation
    generation = generation + 1
    
    dt = 0.17
    run = True
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
        
        #Draw racetrack
        for line in racetrack.innerHitLine:
            pygame.draw.lines(screen, (255,0,0), False, line,2)

        for line in racetrack.outerHitLine:
            pygame.draw.lines(screen, (255,0,0), False, line,2)
        
        colorOffset = 0
        for i in range(0,len(racetrack.checkpoints),2):
            p1 = (int(racetrack.checkpoints[i][0]),int(racetrack.checkpoints[i][1]))
            p2 = (int(racetrack.checkpoints[i+1][0]),int(racetrack.checkpoints[i+1][1]))
            pygame.draw.line(screen, (0, 255 - colorOffset,0+colorOffset), p1, p2, 1)    
            colorOffset = colorOffset + 5
        
        for index, car in enumerate(cars):
            if(car.is_alive):
                #180, -90, -40, -15, 0, 15, 40, 90
                sensors = car.radar.calculate_distance(racetrack) 

                '''
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
                '''
                output = networks[index].activate(sensors)

                #TRANSFORM OUTPUT TO MOVEMENT
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
                    car.velocity[0] = output[0] * carMaxSpeed
                    car.steering = output[1] * 30 - 15



                car.update(dt)
         
                #Kill off bad cars
                
                if (racetrack.hit(car)):
                    car.is_alive = False

                if(car.time_alive == 0):
                    car.is_alive = False

                if(car.checkpoint_passed == len(racetrack.checkpoints)):
                    
                    screen.fill(background_colour)
                    pygame.display.update()
                    
                    racetrack = RandomRacetrack(width, height, 30)
                    
                    if(radar_lenght > 120):
                        genomes[i][1].fitness = 999999999
                    
                    for c in cars:
                        if(car.is_alive):
                            c.position[0] = int(racetrack.start[0])
                            c.position[1] = int(racetrack.start[1])
                            c.checkpoint_passed = 2
                            c.radar.x = int(racetrack.start[0])
                            c.radar.y = int(racetrack.start[1])
                            c.steering = 0
                            c.velocity.x = 0
                            c.angle = -90
                            c.radar.car_angle = -90
                            c.radar.radar_length = radar_lenght
                            c.radar.updateRadar(int(racetrack.start[0]), int(racetrack.start[1]), -90)
                            c.time = c.time
                            c.time_alive = c.time
                
                #Draw each cars (no radar lines because of lag)
                for line in car.radar.radar_lines:
                    pygame.draw.line(screen, (0,0,255), line[0], line[1], 1)
                
                pygame.draw.circle(screen, (255,0,0), (int(car.position.x), int(car.position.y)), car.length)
                
        #Update car fitness
        remain_cars = 0
        for i, car in enumerate(cars):
            if(car.is_alive):
                remain_cars += 1
                score = car.check_passed(racetrack)
                genomes[i][1].fitness = genomes[i][1].fitness + score - car.update_score()
                car.prevSteering = car.steering

        ''''
        #update screen with best car information
        textsurface = myfont.render(("Generation: "+str(generation)), False, (255, 255, 255))
        screen.blit(textsurface,(0,0))

        textsurface = myfont.render(("Cars alive: "+str(remain_cars)), False, (255, 255, 255))
        screen.blit(textsurface,(0,20))
        bla = 0
        fitt = -99999
        for index, c in enumerate(cars):
            if c.is_alive:
                if(bla < c.time_alive):
                    bla = c.time_alive
                if(fitt < genomes[index][1].fitness):
                    fitt = genomes[index][1].fitness
        textsurface = myfont.render(("time left: "+str(bla)), False, (255, 255, 255))
        screen.blit(textsurface,(0,40))
        textsurface = myfont.render(("fitt "+str(fitt)), False, (255, 255, 255))
        screen.blit(textsurface,(0,60))
        '''
        #if all cars are dead, break out loop and go to next generation
        if remain_cars == 0:
            break
        
        #update screen
        
        pygame.display.update()
        screen.fill(background_colour)
        
#Pygame init

(width, height) = (1000, 1000)
background_colour = (0,0,0)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Murphy simulation')
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 20)
screen.fill(background_colour)
pygame.display.flip()
clock = pygame.time.Clock()

#NEAT init
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)


population = neat.Population(config)
population.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
population.add_reporter(stats)

#population.add_reporter(neat.Checkpointer(5, 3600, "models/checkpoint"))
global generation
generation = 0

#Run NEAT
global racetrack
racetrack = RandomRacetrack(width, height, 30)
global radar_lenght
model = population.run(run, 200)

with open(name + ".pkl", "wb") as f:
    pickle.dump(model, f)
    f.close()
