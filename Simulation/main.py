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

global generation

def run(genomes, config):
    networks = []
    cars = []
    racetrack = Racetrack(width, height, random.randint(50,180))

    car_x = racetrack.checkpoints[0][0]
    car_y = racetrack.checkpoints[0][1]

    r = random.randrange(2)
    print(r)
    if(r == 1):
        racetrack.invertCheckpoints()

    for id, genome in genomes:
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(network)
        genome.fitness = 0
        car = Car(id, car_x, car_y)
        if(r == 1):
            car.switchAngle()
        cars.append(car)


    global generation
    generation = generation + 1
    
    dt = 0.17
    run = True
    while run:
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
        '''
        #Draw racetrack
        '''
        pygame.draw.lines(screen, (255,255,255), True, racetrack.outer_line)
        pygame.draw.lines(screen, (255,255,255), True, racetrack.inner_line)

        for checkpoint in racetrack.checkpoints:
            pygame.draw.circle(screen, (0,255,0), checkpoint, 3)
        '''
        #Loop cars and make them drive
        for index, car in enumerate(cars):
            if(car.is_alive):
                #180, -90, -40, -15, 0, 15, 40, 90
                bla = car.radar.calculate_distance(racetrack)
                aaa = []
                aaa.append(bla[0])
                aaa.append(bla[1])
                aaa.append(bla[2])
                aaa.append(bla[3])
                aaa.append(bla[4]) #MID
                aaa.append(bla[5])
                aaa.append(bla[6])
                aaa.append(bla[7])

                output = networks[index].activate(aaa)

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
                    car.velocity[0] = output[0] * 20
                    car.steering = output[1] * 90 - 45

                car.update(dt)

                '''
                print(output)
                if(output[0] > 0):
                    car.velocity[0] = car.velocity[0] + 1
                else:
                    car.velocity[0] = car.velocity[0] - 1

                max_steering = 10
                if(output[1] > 0):
                    if(car.steering > max_steering):
                        car.steering = max_steering
                    else:
                        car.steering = car.steering + 1
                else:
                    if(car.steering < -max_steering):
                        car.steering = -max_steering
                    else:
                        car.steering = car.steering - 1
                '''
                #Kill off bad cars
                if (racetrack.hit(car)):
                    car.is_alive = False

                if(car.checkpoint_passed == 27):
                    car.is_alive = False
                    run = False

                if(car.time_alive == 0):
                    car.is_alive = False
                
                #Draw each cars (no radar lines because of lag)
                '''
                for line in car.radar.radar_lines:
                    pygame.draw.line(screen, (0,0,255), line[0], line[1], 1)
                
                pygame.draw.circle(screen, (255,0,0), (int(car.position.x), int(car.position.y)), car.length)
                '''
        #Update car fitness
        remain_cars = 0
        for i, car in enumerate(cars):
            if(car.is_alive):
                remain_cars += 1
                score = car.check_passed(racetrack)
                genomes[i][1].fitness += car.update_score() + score

        
        #update screen with best car information
        '''
        textsurface = myfont.render(("Generation: "+str(generation)), False, (255, 255, 255))
        screen.blit(textsurface,(0,0))

        textsurface = myfont.render(("Cars alive: "+str(remain_cars)), False, (255, 255, 255))
        screen.blit(textsurface,(0,20))

        textsurface = myfont.render(("Best car"), False, (255, 255, 255))
        screen.blit(textsurface,(0,40))

        textsurface = myfont.render(("Speed: "+str(cars[best_car_index].velocity[0])), False, (255, 255, 255))
        screen.blit(textsurface,(0,100))
        
        textsurface = myfont.render(("Angle: "+str(cars[best_car_index].steering)), False, (255, 255, 255))
        screen.blit(textsurface,(0,120)) 
        '''
        #if all cars are dead, break out loop and go to next generation
        if remain_cars == 0:
            break
        
        #update screen
        '''
        pygame.display.update()
        screen.fill(background_colour)
        clock.tick(60)
        '''
#Pygame init
(width, height) = (800, 800)

'''
background_colour = (0,0,0)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Murphy simulation')
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 20)

screen.fill(background_colour)
pygame.display.flip()
clock = pygame.time.Clock()
'''
#NEAT init
config_path = "./config-feedforward.txt"
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
                           
population = neat.Population(config)

population.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
population.add_reporter(stats)

#population.add_reporter(neat.Checkpointer(5, 3600, "models/checkpoint"))
generation = 0

#Run NEAT
model = population.run(run, 1250)

name = "Model821"

with open("modelsV2/" + name + ".pkl", "wb") as f:
    pickle.dump(model, f)
    f.close()
