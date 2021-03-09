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
global generation

def run(genomes, config):
    networks = []
    cars = []
    racetrack = Racetrack(width, height, random.randint(75,150))

    car_x = racetrack.checkpoints[0][0]
    car_y = racetrack.checkpoints[0][1]

    for id, genome in genomes:
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(network)
        genome.fitness = 0
        cars.append(Car(id,car_x, car_y))

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

        for checkpoint in racetrack.checkpoints:
            pygame.draw.circle(screen, (0,255,0), checkpoint, 3)

        #Loop cars and make them drive
        for index, car in enumerate(cars):
            if(car.is_alive):
                output = networks[index].activate(car.radar.calculate_distance(racetrack))
                car.velocity[0] = output[0] * 15
                car.steering = output[1] * 15
                car.update(dt)

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
                '''
                pygame.draw.circle(screen, (255,0,0), (int(car.position.x), int(car.position.y)), car.length)

        #Update car fitness
        remain_cars = 0
        best_car_score = genomes[0][1].fitness
        best_car_index = 0
        for i, car in enumerate(cars):
            if(car.is_alive):
                remain_cars += 1
                score = car.check_passed(racetrack)
                genomes[i][1].fitness += car.update_score() + score
                if(genomes[i][1].fitness > best_car_score):
                    best_car_score = genomes[i][1].fitness
                    best_car_index = i
        
        output = networks[best_car_index].activate(cars[best_car_index].radar.calculate_distance(racetrack))

        #update screen with best car information
        textsurface = myfont.render(("Generation: "+str(generation)), False, (255, 255, 255))
        screen.blit(textsurface,(0,0))

        textsurface = myfont.render(("Cars alive: "+str(remain_cars)), False, (255, 255, 255))
        screen.blit(textsurface,(0,20))

        textsurface = myfont.render(("Best car"), False, (255, 255, 255))
        screen.blit(textsurface,(0,40))

        textsurface = myfont.render(("Speed"+str(output[0])), False, (255, 255, 255))
        screen.blit(textsurface,(0,60))
        
        textsurface = myfont.render(("Steering angle: "+str(output[1])), False, (255, 255, 255))
        screen.blit(textsurface,(0,80))

    
        #if all cars are dead, break out loop and go to next generation
        if remain_cars == 0:
            break
        
        #update screen
        pygame.display.update()
        screen.fill(background_colour)
        clock.tick(60)

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

#NEAT init
config_path = "./config-feedforward.txt"
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
                           
population = neat.Population(config)

population.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
population.add_reporter(stats)

population.add_reporter(neat.Checkpointer(5, 3600, "models/checkpoint"))
generation = 0

#Run NEAT
model = population.run(run, 10)

with open("models/" + time.strftime("%d%m%Y-%H%M%S") + ".pkl", "wb") as f:
    pickle.dump(model, f)
    f.close()
