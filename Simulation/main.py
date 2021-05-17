import pygame
import os
from racetrack import Racetrack
from randomtrack import RandomRacetrack
from car import Car
from math import sin, radians, degrees, copysign
import math
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

def screen_coordinates(self, point, posistion, scale, focus):
    return (
        int((point.x-position.x)*scale + focus.x),
        int((point.y-position.y)*scale + focus.y)
    )

def draw_rect(center, corners, rotation_angle, color):
    c_x = center[0]
    c_y = center[1]
    delta_angle = rotation_angle
    rotated_corners = []

    for p in corners:
        temp = []
        length = math.sqrt((p[0] - c_x)**2 + (c_y - p[1])**2)
        angle = math.atan2(c_y - p[1], p[0] - c_x)
        angle += delta_angle
        temp.append(c_x + length*math.cos(angle))
        temp.append(c_y - length*math.sin(angle))
        rotated_corners.append(temp)

    # draw rectangular polygon --> car body
    rect = pygame.draw.polygon(screen, color, (rotated_corners[0],rotated_corners[1],rotated_corners[2],rotated_corners[3]))


def run(genomes, config):
    radar_lenght = 130
    counter = 0
    random.seed(10)
    global generation
    generation = generation + 1
    global trackLenght 

    racetrack = RandomRacetrack(width, height, trackLenght ,randrange(90,110))

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

    ticks = 60
    clock = pygame.time.Clock()
    dt = 0.015
    run = True
    bla = 0
    blav = 0
    blas = 0
    blaa = 0
    blaang = 0
    fitt = -99999
    t = 9999
    bestcarindex = 0
                
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_RIGHT]:
                ticks = ticks +1

        if pressed[pygame.K_LEFT]:
                ticks = ticks -1

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
                    car.speed = output[0] * car.max_speed
                    car.steering_angle = output[1] * car.max_steering_angle * 2 - car.max_steering_angle
 
                car.update(dt)
                #Kill off bad cars
                
                if (racetrack.hit(car)):
                    car.is_alive = False

                
                if(car.time_alive == 0):
                    car.is_alive = False

                
                if(car.speed > 9 and abs(math.degrees(car.steering_angle)) > 20):
                    car.is_alive = False
                if(car.speed > 8 and abs(math.degrees(car.steering_angle)) > 25):
                    car.is_alive = False
                if(car.speed > 7 and abs(math.degrees(car.steering_angle)) > 30):
                    car.is_alive = False
                if(car.speed > 6 and abs(math.degrees(car.steering_angle)) > 35):
                    car.is_alive = False
                
                if(car.checkpoint_passed == len(racetrack.checkpoints)-2):
                    trackLenght = trackLenght + 1
                    screen.fill(background_colour)
                    pygame.display.update()
                    random.seed(10)
                    racetrack = RandomRacetrack(width, height, trackLenght, randrange(90,110))
                    
                    for c in cars:
                        if(car.is_alive):
                            c.x = int(racetrack.start[0])
                            c.y = int(racetrack.start[1])
                            c.checkpoint_passed = 2
                            c.radar.x = int(racetrack.start[0])
                            c.radar.y = int(racetrack.start[1])
                            c.steering = 0
                            c.speed = 0
                            c.angle = -90
                            c.orientation =math.radians(-90)

                            c.radar.car_angle = -90
                            c.radar.radar_length = radar_lenght
                            c.radar.updateRadar(int(racetrack.start[0]), int(racetrack.start[1]), -90)
                            c.time = c.time
                            c.time_alive = c.time
                
                #Draw each cars
                
                for line in car.radar.radar_lines:
                    pygame.draw.line(screen, (0,0,255), line[0], line[1], 1)
                
                #pygame.draw.circle(screen, (255,0,0), (int(car.x), int(car.y)), car.car_length)
                            
                car_x = car.x 
                car_y = car.y 
                orientation = car.orientation
                steering_angle = car.steering_angle
                car_length = car.car_length
                car_width = car.car_width
                wheel_length = car.wheel_length
                wheel_width = car.wheel_width

                p1 = [car_x-car_length/4,car_y-car_width/2]
                p2 = [car_x+(0.75*car_length),car_y-car_width/2]
                p3 = [car_x+(0.75*car_length),car_y+car_width/2]
                p4 = [car_x-car_length/4,car_y+car_width/2]
                if(index == bestcarindex):
                    draw_rect([car_x, car_y], [p1, p2, p3, p4], orientation, (255,0,0))
                else:
                    draw_rect([car_x, car_y], [p1, p2, p3, p4], orientation, (0,0,255))


                # heading direction
                h = [car_x+car_length/2,car_y]
                length = car_length/2
                angle = math.atan2(car_y - h[1], h[0] - car_x)
                angle += orientation
                h[0] = car_x + length*math.cos(angle)
                h[1] = car_y - length*math.sin(angle)

                # wheels
                # rotate center of wheel1
                w1_c_x = car_x
                w1_c_y = car_y - car_width/3
                length = math.sqrt((w1_c_x - car_x)**2 + (car_y - w1_c_y)**2)
                angle = math.atan2(car_y - w1_c_y, w1_c_x - car_x)
                angle += orientation
                w1_c_x = car_x + length*math.cos(angle)
                w1_c_y = car_y - length*math.sin(angle)

                # draw corners of wheel1
                w1_p1 = [w1_c_x-wheel_length/2, w1_c_y-wheel_width/2]
                w1_p2 = [w1_c_x+wheel_length/2, w1_c_y-wheel_width/2]
                w1_p3 = [w1_c_x+wheel_length/2, w1_c_y+wheel_width/2]
                w1_p4 = [w1_c_x-wheel_length/2, w1_c_y+wheel_width/2]
                draw_rect([w1_c_x, w1_c_y], [w1_p1, w1_p2, w1_p3, w1_p4], orientation, (255,255,255))


                w2_c_x = car_x + car_length/2
                w2_c_y = car_y - car_width/3
                length = math.sqrt((w2_c_x - car_x)**2 + (car_y - w2_c_y)**2)
                angle = math.atan2(car_y - w2_c_y, w2_c_x - car_x)
                angle += orientation
                w2_c_x = car_x + length*math.cos(angle)
                w2_c_y = car_y - length*math.sin(angle)

                w2_p1 = [w2_c_x-wheel_length/2, w2_c_y-wheel_width/2]
                w2_p2 = [w2_c_x+wheel_length/2, w2_c_y-wheel_width/2]
                w2_p3 = [w2_c_x+wheel_length/2, w2_c_y+wheel_width/2]
                w2_p4 = [w2_c_x-wheel_length/2, w2_c_y+wheel_width/2]
                draw_rect([w2_c_x, w2_c_y], [w2_p1, w2_p2, w2_p3, w2_p4], steering_angle + orientation, (255,255,255))
                #rect = pygame.draw.polygon(screen, (255,255,255), (w2_p1,w2_p2,w2_p3,w2_p4))


                w3_c_x = car_x + car_length/2
                w3_c_y = car_y + car_width/3
                length = math.sqrt((w3_c_x - car_x)**2 + (car_y - w3_c_y)**2)
                angle = math.atan2(car_y - w3_c_y, w3_c_x - car_x)
                angle += orientation
                w3_c_x = car_x + length*math.cos(angle)
                w3_c_y = car_y - length*math.sin(angle)

                w3_p1 = [w3_c_x-wheel_length/2, w3_c_y-wheel_width/2]
                w3_p2 = [w3_c_x+wheel_length/2, w3_c_y-wheel_width/2]
                w3_p3 = [w3_c_x+wheel_length/2, w3_c_y+wheel_width/2]
                w3_p4 = [w3_c_x-wheel_length/2, w3_c_y+wheel_width/2]
                draw_rect([w3_c_x, w3_c_y], [w3_p1, w3_p2, w3_p3, w3_p4], steering_angle + orientation, (255,255,255))
                # rect = pygame.draw.polygon(screen, (255,255,255), (w3_p1,w3_p2,w3_p3,w3_p4))

                w4_c_x = car_x
                w4_c_y = car_y + car_width/3
                length = math.sqrt((w4_c_x - car_x)**2 + (car_y - w4_c_y)**2)
                angle = math.atan2(car_y - w4_c_y, w4_c_x - car_x)
                angle += orientation
                w4_c_x = car_x + length*math.cos(angle)
                w4_c_y = car_y - length*math.sin(angle)

                w4_p1 = [w4_c_x-wheel_length/2, w4_c_y-wheel_width/2]
                w4_p2 = [w4_c_x+wheel_length/2, w4_c_y-wheel_width/2]
                w4_p3 = [w4_c_x+wheel_length/2, w4_c_y+wheel_width/2]
                w4_p4 = [w4_c_x-wheel_length/2, w4_c_y+wheel_width/2]
                draw_rect([w4_c_x, w4_c_y], [w4_p1, w4_p2, w4_p3, w4_p4], orientation, (255,255,255))

                pygame.draw.line(screen, (255,255,0), (h[0], h[1]),(int(car_x), int(car_y)), 1)

                # draw axle
                pygame.draw.line(screen, (255,255,255), (w1_c_x, w1_c_y),(w4_c_x, w4_c_y), 1)

                # draw mid of axle
                pygame.draw.circle(screen, (255,255,0), (int(car_x), int(car_y)), 3)

                if(not cars[bestcarindex].is_alive):
                    fitt = -9999

                if(fitt < genomes[index][1].fitness):
                    fitt = genomes[index][1].fitness
                    bestcarindex = index
                bla = cars[bestcarindex].time_alive
                blav = cars[bestcarindex].speed
                blas = cars[bestcarindex].steering_angle
                blaang = cars[bestcarindex].orientation

        #Update car fitness
        remain_cars = 0
        for i, car in enumerate(cars):
            if(car.is_alive):
                remain_cars += 1
                score = car.check_passed(racetrack)
                genomes[i][1].fitness = genomes[i][1].fitness + score - car.update_score()
                car.previous_steering_angle = car.steering_angle

       
        #update screen with best car information
        textsurface = myfont.render(("Generation: "+str(generation)), False, (255, 255, 255))
        screen.blit(textsurface,(0,0))

        textsurface = myfont.render(("Cars alive: "+str(remain_cars)), False, (255, 255, 255))
        screen.blit(textsurface,(0,20))
       
        textsurface = myfont.render(("time left: "+str(bla)), False, (255, 255, 255))
        screen.blit(textsurface,(0,40))
        textsurface = myfont.render(("score "+str(fitt)), False, (255, 255, 255))
        screen.blit(textsurface,(0,60))

        textsurface = myfont.render(("velocity "+str(blav)), False, (255, 255, 255))
        screen.blit(textsurface,(0,100))
        textsurface = myfont.render(("angle "+str(math.degrees(blaang))), False, (255, 255, 255))
        screen.blit(textsurface,(0,120)) 
        textsurface = myfont.render(("steering "+str(math.degrees(blas))), False, (255, 255, 255))
        screen.blit(textsurface,(0,140))
        #if all cars are dead, break out loop and go to next generation
        if remain_cars == 0:
            break
        
        #update screen
        pygame.display.set_caption('(%d FPS)' % (clock.get_fps()))

        pygame.display.update()
        screen.fill(background_colour)
        clock.tick(20)

        
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

population.add_reporter(neat.Checkpointer(5, 3600, "models/checkpoint"))
global generation
generation = 0

#Run NEAT
global racetrack
racetrack = RandomRacetrack(800, 400, 5, 110)
global radar_lenght
global trackLenght 
trackLenght = 1
model = population.run(run, 200)

with open(name + ".pkl", "wb") as f:
    pickle.dump(model, f)
    f.close()
