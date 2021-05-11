import pygame
import random
import time
import math
from copy import deepcopy

display_width = 800
display_height = 800

world_size = display_width
red = (200,0,0)
blue = (0,0,255)
green = (0,155,0)
yellow = (200,200,0)
white = (255,255,255)
gray = (67,70,75)

car_lenght = 80.0
car_width = 60.0

wheel_lenght = 20
wheel_width = 6

max_steering_angle = math.pi / 4

origin = (display_width/2, display_height/2)

pygame.init()

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Vehicle Sim")
clock = pygame.time.Clock()

screen.fill(white)

class robot:
    def __init__(self):
        self.x = random.random() * world_size
        self.y = random.random() * world_size
        self.orientation = random.random() * 2.0 * math.pi
        self.steering_angle = 0.0
        self.steering_drift = 0.0

    def set(self, x, y, orientation, steering_angle):
        if x >= world_size or x < 0:
            raise ValueError('X coordinate out of bound')
        if y >= world_size or y < 0:
            raise ValueError('Y coordinate out of bound')
        if orientation >= 2*math.pi or orientation < 0:
            raise ValueError('Orientation must be in [0..2math.pi]')
        if abs(steering_angle) > max_steering_angle:
            raise ValueError('Exceeding max steering angle')
        self.x = x
        self.y = y
        self.orientation = orientation
        self.steering_angle = steering_angle

    def move(self, turn, forward):
        theta = self.orientation # initial orientation
        alpha = turn # steering angle
        dist = forward # distance to be moved
        length = car_length # length of the robot
        if abs(alpha) > max_steering_angle:
            raise ValueError('Exceeding max steering angle')


        # in local coordinates of robot
        beta = (dist/length)*math.tan(alpha) # turning angle
        # print degrees(beta)
        _x = _y = _theta = 0.0
        if beta > 0.001 or beta < -0.001:
            radius = dist/beta # turning radius
            cx = self.x - math.sin(theta)*radius # center of the circle
            cy = self.y - math.cos(theta)*radius # center of the circle

            # Uncomment to see the center of the circle the robot is going about
            pygame.draw.circle(screen, red, (int(cx), int(cy)), 5)
            pygame.display.update()

            # in global coordinates of robot
            _x = cx + math.sin(theta + beta)*radius
            _y = cy + math.cos(theta + beta)*radius
            _theta = (theta + beta)%(2*math.pi)

        else: # straight motion
            _x = self.x + dist*math.cos(theta)
            _y = self.y - dist*math.sin(theta)
            _theta = (theta + beta)%(2*math.pi)

        self.x = _x
        self.y = _y
        self.orientation = _theta
        self.steering_angle = alpha

        self.x %= world_size
        self.y %= world_size

def draw_robot(robot):
    car_x = robot.x 
    car_y = robot.y 
    orientation = robot.orientation
    steering_angle = robot.steering_angle

    p1 = [car_x-car_length/4,car_y-car_width/2]
    p2 = [car_x+(0.75*car_length),car_y-car_width/2]
    p3 = [car_x+(0.75*car_length),car_y+car_width/2]
    p4 = [car_x-car_length/4,car_y+car_width/2]

    # car body
    draw_rect([car_x, car_y], [p1, p2, p3, p4], orientation, yellow)

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
    draw_rect([w1_c_x, w1_c_y], [w1_p1, w1_p2, w1_p3, w1_p4], orientation, black)


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
    draw_rect([w2_c_x, w2_c_y], [w2_p1, w2_p2, w2_p3, w2_p4], steering_angle + orientation, black)
    #rect = pygame.draw.polygon(screen, black, (w2_p1,w2_p2,w2_p3,w2_p4))


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
    draw_rect([w3_c_x, w3_c_y], [w3_p1, w3_p2, w3_p3, w3_p4], steering_angle + orientation, black)
    # rect = pygame.draw.polygon(screen, black, (w3_p1,w3_p2,w3_p3,w3_p4))

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
    draw_rect([w4_c_x, w4_c_y], [w4_p1, w4_p2, w4_p3, w4_p4], orientation, black)

    pygame.draw.line(screen, red, (h[0], h[1]),(int(car_x), int(car_y)), 1)

    # draw axle
    pygame.draw.line(screen, black, (w1_c_x, w1_c_y),(w4_c_x, w4_c_y), 1)

    # draw mid of axle
    pygame.draw.circle(screen, red, (int(car_x), int(car_y)), 3)

robot = robot()
orientation = 90.0
steering_angle = 0.0
#in math.radians
robot.set(50, 400,math.radians(orientation), steering_angle)

exit = False

delta_forward = 0.0
delta_steer = 0.0

while exit == False:

    screen.fill(white)
    # Uncomment following to see the exact racetrack
    draw_track(250, 400, 200, grey)
    draw_path(path, red)

    draw_robot(robot)

    # pygame.draw.line(screen, green, (display_width/2, 0), (display_width/2, display_height), 1)
    # pygame.draw.line(screen, black, (0, display_height/2), (display_width, display_height/2), 1)

    pygame.display.update()
    clock.tick(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                delta_steer = math.radians(30)
            elif event.key == pygame.K_RIGHT:
                delta_steer = -math.radians(30)
            elif event.key == pygame.K_UP:
                delta_forward = 5.0
            elif event.key == pygame.K_DOWN:
                delta_forward = -5.0
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                delta_steer = 0.0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                delta_forward = 0.0

    if steering_angle > max_steering_angle:
        steering_angle = max_steering_angle
    elif(steering_angle < -max_steering_angle):
        steering_angle = -max_steering_angle

    robot.move(random.random(), -delta_forward)