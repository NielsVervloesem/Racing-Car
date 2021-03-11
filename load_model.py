import pickle
import neat
import pygame
from racetrack import Racetrack
from car import Car
import random
import sys
import time
import math

model_path = 'models\\model6_reg.pkl'
config_file = 'models\\model6_config.txt'

# Unpickle saved winner
with open(model_path, "rb") as f:
    winner = pickle.load(f)

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_file)

winner_model = neat.nn.FeedForwardNetwork.create(winner, config)


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

racetrack = Racetrack(width, height, random.randint(160,170))

car_x = racetrack.checkpoints[0][0]
car_y = racetrack.checkpoints[0][1]
car = Car(1,car_x, car_y)

prevAngle = 0

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
        output = winner_model.activate(car.radar.calculate_distance(racetrack))
        car.velocity[0] = output[0] % 20
        bla = output[1] % 360

        if(bla > 180+45):
            bla = 180+45
        if(bla < 180-45):
            bla = 180-45
        car.steering = bla

        car.update(dt)

        #Kill off bad cars
        if (racetrack.hit(car)):
            car.is_alive = False

        if(car.checkpoint_passed == 25):
            car.is_alive = False
            run = False
        
        #Draw each cars (no radar lines because of lag)
        for line in car.radar.radar_lines:
            pygame.draw.line(screen, (0,0,255), line[0], line[1], 1)
        
        pygame.draw.circle(screen, (255,0,0), (int(car.position.x), int(car.position.y)), car.length)

    textsurface = myfont.render(("Best car"), False, (255, 255, 255))
    screen.blit(textsurface,(0,40))

    textsurface = myfont.render(("Speed"+str(output[0] % 20)), False, (255, 255, 255))
    screen.blit(textsurface,(0,60))
    
    textsurface = myfont.render(("Steering angle: "+str(bla-180)), False, (255, 255, 255))
    screen.blit(textsurface,(0,80))
    
    
    textsurface = myfont.render(("Steering diff: "+str(abs(prevAngle - bla))), False, (255, 255, 255))
    screen.blit(textsurface,(0,100))

    prevAngle = bla
    
    #update screen
    pygame.display.update()
    screen.fill(background_colour)
    clock.tick(60)
    time.sleep(0.1)
