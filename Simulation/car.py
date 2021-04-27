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
    def __init__(self, name, x, y, radar_length, angle=-90, length=10):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_velocity = 60
        self.max_steering = 45
        self.brake_deceleration = 20
        self.free_deceleration = 10
        self.acceleration = 0.0
        self.steering = 0.0
        self.name = name
        self.prevSteering = 0
        self.time = 100

        self.time_alive = self.time
        self.checkpoint_passed = 0

        self.radar = Radar(x, y, radar_length, (180, -90, -40, -15, 0, 15, 40, 90), self.angle)

        self.is_alive = True
        self.score = 0
    
    def switchAngle(self):
        if(self.angle == -90):
            self.angle = 90
            self.radar.car_angle = 90
        else:
            self.angle = -90
            self.radar.car_angle = -90

    #When passing a checkpoint of the racetrack, reward the car with a bonus
    #First one to pass will get the max bonus, second one will recieve 500 points less
    def check_passed(self, racetrack):
        score = 0   

        check1 = racetrack.checkpoints[self.checkpoint_passed % len(racetrack.checkpoints)]
        check2 = racetrack.checkpoints[self.checkpoint_passed % len(racetrack.checkpoints) + 1]

        x = self.position.x
        y = self.position.y
        lenght = self.length
        line1 = LineString([(x-lenght, y-lenght),(x+lenght, y-lenght),(x-lenght, y+lenght),(x+lenght, y+lenght)])
        line2 = LineString([check1, check2])
        intersection1 = (line1.intersection(line2))

        if(isinstance(intersection1, shapely.geometry.multipoint.MultiPoint)):
                intersection1 = intersection1[len(intersection1)-1]

        if(len(intersection1.coords) == 1):
            self.checkpoint_passed = self.checkpoint_passed + 2
            score = self.time_alive + 900
            self.time_alive = 100

        return score

    #Being alive is good, small reward
    def update_score(self):
        a = self.steering + 45
        b = self.prevSteering + 45

        if(a > b):
            return (a - b) 
        else:
            return (b - a)


    def distanceNextCheckpoint(self, racetrack):
        check = racetrack.checkpoints[self.checkpoint_passed % 13]
        line = LineString(check)

        x = self.position.x
        y = self.position.y
        np = nearest_points(line, Point(x,y))[0]
        return calculate_distance(np.x, np.y,x,y)

    #update the car pos and angle
    def update(self, dt): 
        #self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt

        self.radar.updateRadar(self.position.x, self.position.y, self.angle)

        self.time_alive -= 1
