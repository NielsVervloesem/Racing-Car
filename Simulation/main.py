import pygame
import os
from racetrack import Racetrack
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

#MODEL PARAMS INIT
name = "ModelZonderRange7"
config_path = "./config-feedforward.txt"
carMaxSpeed = 20 * 1
carSensors = 5

def run(genomes, config):
    networks = []
    cars = []
    racetrack = Racetrack(width, height, random.randint(200,200))
    jump = 10

    car_x = racetrack.checkpoints[0][0]
    car_y = racetrack.checkpoints[0][1]

    invertRandom = random.randrange(2)
    if(invertRandom == 1):
        racetrack.invertCheckpoints()

    for id, genome in genomes:
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(network)
        genome.fitness = 0
        car = Car(carSensors, car_x, car_y)
        if(invertRandom == 1):
            car.switchAngle()
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
        pygame.draw.lines(screen, (255,255,255), True, racetrack.outer_line)
        pygame.draw.lines(screen, (255,255,255), True, racetrack.inner_line)

        colorOffset = 0
        for checkpoint in racetrack.checkpoints:
            colorOffset += 15
            pygame.draw.circle(screen, (colorOffset,255,colorOffset), checkpoint, 3)
        
        #Loop cars and make them drive
        if(invertRandom == 1):
            invertRandom = 0
        else:
            invertRandom = 1
            
        for index, car in enumerate(cars):
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

                #if(int(car.name) > 3):
                    #inputdata.append(sensors[7]) #40
                if(int(car.name) > 5):
                    inputdata.append(sensors[7]) #90
                output = networks[index].activate(inputdata)

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
                    car.steering = output[1] * 90 - 45

                car.update(dt)
                
                #Kill off bad cars
                if (racetrack.hit(car)):
                    car.is_alive = False

                car.check_passed(racetrack)
                if(car.checkpoint_passed == 26):
                    screen.fill(background_colour)

                    racetrack = Racetrack(width, height, random.randint(200 - jump,200 - jump))
                    if(invertRandom == 1):
                        racetrack.invertCheckpoints()
                    jump = jump + jump

                    for c in cars:
                        if(car.is_alive):
                            c.position[0] = racetrack.checkpoints[0][0]
                            c.position[1] = racetrack.checkpoints[0][1]
                            c.checkpoint_passed = 0
                            c.radar.x = racetrack.checkpoints[0][0]
                            c.radar.y = racetrack.checkpoints[0][1]
                            c.steering = 0
                            c.velocity.x = 0
                            c.angle = -90
                            c.radar.car_angle = -90
                            c.time_alive = 100
                            c.radar.updateRadar(racetrack.checkpoints[0][0], racetrack.checkpoints[0][1], -90)
                            
                            if(invertRandom == 1):
                                car.switchAngle()
                                c.radar.updateRadar(racetrack.checkpoints[0][0], racetrack.checkpoints[0][1], 90)
                            for line in c.radar.radar_lines:
                                pygame.draw.line(screen, (0,0,255), line[0], line[1], 1) 
                            pygame.draw.circle(screen, (255,0,0), (int(c.position.x), int(c.position.y)), car.length)
                    pygame.draw.lines(screen, (255,255,255), True, racetrack.outer_line)
                    pygame.draw.lines(screen, (255,255,255), True, racetrack.inner_line)

                    pygame.display.update()

                if(car.time_alive == 0):
                    car.is_alive = False
                
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
                genomes[i][1].fitness += car.update_score() + score
                car.prevSteering = car.steering

        #update screen with best car information
        
        textsurface = myfont.render(("Generation: "+str(generation)), False, (255, 255, 255))
        screen.blit(textsurface,(0,0))

        textsurface = myfont.render(("Cars alive: "+str(remain_cars)), False, (255, 255, 255))
        screen.blit(textsurface,(0,20))

        #if all cars are dead, break out loop and go to next generation
        if remain_cars == 0:
            break
        
        #update screen
        
        pygame.display.update()
        screen.fill(background_colour)
        clock.tick(60)
        
#Pygame init
(width, height) = (800, 800)
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
model = population.run(run, 100)

with open("modelsV3/" + name + ".pkl", "wb") as f:
    pickle.dump(model, f)
    f.close()
