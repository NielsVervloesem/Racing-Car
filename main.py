import pygame
import os

from racetrack import Racetrack
from car import Car
from math import sin, radians, degrees, copysign
import time

background_colour = (0,0,0)
(width, height) = (800, 800)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Intersection demo')

screen.fill(background_colour)
pygame.display.flip()

clock = pygame.time.Clock()
racetrack = Racetrack(width, height)
carX = racetrack.checkpoints[0][0]
carY = racetrack.checkpoints[0][1]
car = Car(carX, carY)

ppu = 32
running = True
while running:
    dt = clock.get_time() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_r]:
        racetrack = Racetrack(width, height)
        carX = racetrack.checkpoints[0][0]
        carY = racetrack.checkpoints[0][1]
        car = Car(carX, carY)
        time.sleep(0.5)

    if pressed[pygame.K_UP]:
        if car.velocity.x < 0:
            car.acceleration = car.brake_deceleration
        else:
            car.acceleration += 2 * dt
    elif pressed[pygame.K_DOWN]:
        if car.velocity.x > 0:
            car.acceleration = -car.brake_deceleration
        else:
            car.acceleration -= 2 * dt
    elif pressed[pygame.K_SPACE]:
        if abs(car.velocity.x) > dt * car.brake_deceleration:
            car.acceleration = -copysign(car.brake_deceleration, car.velocity.x)
        else:
            car.acceleration = -car.velocity.x / dt
    else:
        if abs(car.velocity.x) > dt * car.free_deceleration:
            car.acceleration = -copysign(car.free_deceleration, car.velocity.x)
        else:
            if dt != 0:
                car.acceleration = -car.velocity.x / dt
    car.acceleration = max(-car.max_acceleration, min(car.acceleration, car.max_acceleration))

    if pressed[pygame.K_RIGHT]:
        car.steering -= 30 * dt
    elif pressed[pygame.K_LEFT]:
        car.steering += 30 * dt
    else:
        car.steering = 0
    car.steering = max(-car.max_steering, min(car.steering, car.max_steering))

    car.update(dt)

    screen.fill(background_colour)

    pygame.draw.lines(screen, (255,255,255), True, racetrack.outerLine)
    pygame.draw.lines(screen, (255,255,255), True, racetrack.innerLine)

    for checkpoint in racetrack.checkpoints:
        pygame.draw.circle(screen, (0,255,0), checkpoint, 3)

    for line in car.radar.radar_lines:
        pygame.draw.line(screen, (0,0,255), line[0], line[1], 1)

    pygame.draw.circle(screen, (255,0,0), (int(car.position.x), int(car.position.y)), car.length)

    print(car.radar.calculate_distance(racetrack))
    pygame.display.flip()

    clock.tick(60)


pygame.quit()