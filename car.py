from math import sin, cos, radians, degrees, copysign
from pygame.math import Vector2
import pygame
from radar import Radar

class Car:
    def __init__(self, x, y, angle=-90, length=10, max_steering=6, max_acceleration=50.0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 50
        self.brake_deceleration = 20
        self.free_deceleration = 10
        
        w = 5
        h = 10
        self.body = [
        (x, y),
        (x, h),
        (w, h),
        (w, y)
    ]


        self.acceleration = 0.0
        self.steering = 0.0

        self.radar = Radar(x, y, 150, (-45, -15, 0, 15, 45, 180), self.angle)

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


