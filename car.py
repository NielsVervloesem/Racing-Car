from math import sin, radians, degrees
from pygame.math import Vector2
from radar import Radar
import math
import time

def calculate_distance(x1,y1,x2,y2):
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance


class Car:
    def __init__(self, id, x, y, angle=-90, length=10):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_velocity = 50
        self.brake_deceleration = 20
        self.free_deceleration = 10
        self.acceleration = 0.0
        self.steering = 0.0
        self.id = id

        self.time_alive = 200
        self.checkpoint_passed = 1

        self.radar = Radar(x, y, 120, (-45, -15,-90, 0, 15, 45, 90, 180), self.angle)

        self.is_alive = True
        self.score = 200
    
    #When passing a checkpoint of the racetrack, reward the car with a bonus
    #First one to pass will get the max bonus, second one will recieve 500 points less
    def check_passed(self, racetrack):
        check = racetrack.checkpoints[self.checkpoint_passed % 13]
        current_distance = calculate_distance(self.position.x, self.position.y, check[0], check[1])

        if(current_distance < racetrack.racetrack_width):
            self.checkpoint_passed = self.checkpoint_passed + 1
            score = racetrack.passed[self.checkpoint_passed] + 1
            racetrack.passed[self.checkpoint_passed] -= 500
            self.time_alive += 100
            return score
        return 0

    #Being alive is good, small reward
    def update_score(self):
        return 1

    #update the car pos and angle
    def update(self, dt): 
        self.velocity += (self.acceleration * dt, 0)
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
