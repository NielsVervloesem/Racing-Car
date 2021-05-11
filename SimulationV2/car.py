from math import sin, radians, degrees
from pygame.math import Vector2
from radar import Radar
import math
import time
from shapely.geometry import LineString, LinearRing, Point
import shapely
from shapely.ops import nearest_points
from random import randrange

def calculate_distance(x1,y1,x2,y2):
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

class Car:
    def __init__(self, x, y):
        #set x,y and orientation posistion
        self.x = x
        self.y = y
        self.orientation = math.radians(-90)

        #set steering and acceleration/speed values
        self.steering_angle = 0.0
        self.previous_steering_angle = 0.0
        self.max_steering_angle = math.radians(30)
        self.acceleration = 0.0
        self.max_acceleration = 5.0
        self.speed = 0.0
        self.max_speed = 5

        #build car body based on the lenght
        self.car_length = 32
        self.car_width = 32 / 4 * 3
        self.wheel_length = 32 / 4
        self.wheel_width = 32 / 16

        #set params used for score calculation
        self.time = 150
        self.time_alive = 200
        self.checkpoint_passed = 2
        self.is_alive = True

        self.radar = Radar(self.x, self.y, 130, (180, -90, -40, -15, 0, 15, 40, 90), math.degrees(self.steering_angle))

    #When passing a checkpoint of the racetrack, reward the car with a bonus
    #First one to pass will get the max bonus, second one will recieve 500 points less
    def check_passed(self, racetrack):
        score = 0   
        check1 = racetrack.checkpoints[self.checkpoint_passed]
        check2 = racetrack.checkpoints[self.checkpoint_passed+1]
        p1 = [self.x-self.car_length/4,self.y-self.car_width/2]
        p2 = [self.x+(0.75*self.car_length),self.y-self.car_width/2]
        p3 = [self.x+(0.75*self.car_length),self.y+self.car_width/2]
        p4 = [self.x-self.car_length/4,self.y+self.car_width/2]

        line1 = LineString([(p1),(p2),(p3),(p4)])
        line2 = LineString([check1, check2])
        intersection1 = (line1.intersection(line2))

        if(isinstance(intersection1, shapely.geometry.multipoint.MultiPoint)):
                intersection1 = intersection1[len(intersection1)-1]

        if(len(intersection1.coords) == 1):
            self.checkpoint_passed = self.checkpoint_passed + 2
            score = self.time_alive + 900
            self.time_alive = self.time
        return score

    #Being alive is good, small reward
    def update_score(self):
        a = self.steering_angle + 45
        b = self.previous_steering_angle + 45

        if(a > b):
            return (a - b) 
        else:
            return (b - a)


    def distanceNextCheckpoint(self, racetrack):
        check = racetrack.checkpoints[self.checkpoint_passed]
        line = LineString(check)

        x = self.position.x
        y = self.position.y
        np = nearest_points(line, Point(x,y))[0]
        return calculate_distance(np.x, np.y,x,y)

    #update the car pos and angle
    def update(self, dt): 
        #dunno yet
        #self.speed += (self.acceleration * dt, 0)
        #self.speed = max(-self.speed, min(self.speed, self.speed))

        theta = self.orientation # initial orientation
        alpha = self.steering_angle # steering angle
        dist = self.speed # distance to be moved
        length = self.car_length # length of the robot
        if abs(alpha) > self.max_steering_angle:
            raise ValueError('Exceeding max steering angle')

        # in local coordinates of robot
        beta = (dist/length)*math.tan(alpha) # turning angle

        _x = _y = _theta = 0.0
        if beta > 0.001 or beta < -0.001:
            radius = dist/beta # turning radius
            cx = self.x - math.sin(theta)*radius # center of the circle
            cy = self.y - math.cos(theta)*radius # center of the circle

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

        self.radar.updateRadar(self.x, self.y, math.degrees(self.orientation))
        self.time_alive -= 1