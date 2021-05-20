import pickle
import neat
import pygame
from racetrack import Racetrack
from car import Car
import random
import sys
import time
import math
import visualize
import os
from piece import Piece
import math
import random
from car import Car
from shapely.geometry import LineString, LinearRing
import shapely
from random import randrange

def get_coords_straight(x,y,r,xc,yc):
    return x, y + r * math.sqrt(3),xc,yc+1,4

def get_coords(x,y,r,xc,yc):
    rand = random.randrange(6)
    #BOTTOM
    if(rand == 0):
        return x, y + r * math.sqrt(3),xc,yc+1,4
    #TOP
    if(rand == 1):
        return x, y - r * math.sqrt(3),xc,yc-1,1
    #TOP RIGHT
    if(rand == 2):
        return x + r * 2 * 3/4, y - r * math.sqrt(3) / 2,xc+1,yc-1,2
    #TOP LEFTR
    if(rand == 3):
        return x - r * 2 * 3/4, y - r * math.sqrt(3) / 2,xc-1,yc,0
    #BOTTEM LEFT
    if(rand == 4):
        return x - r * 2 * 3/4, y + r * math.sqrt(3) / 2,xc-1,yc+1,5
    #BOTTOM RIGHT
    if(rand == 5):
        return x + r * 2 * 3/4, y + r * math.sqrt(3) / 2,xc+1,yc,3

class RandomRacetrack:
    def __init__(self, width, height, amount, racewidth):
        self.x_offset = width / 2
        self.y_offset = height / 2

        self.innerlines = []
        self.outerlines = []
        self.checkpoints = []
        self.innerHitLine = []
        self.outerHitLine = []
        self.start = 0
        self.startAngle = -90
        self.racewidth = racewidth
        self.hex = []
        self.generateRacetrack(amount)


    def hit(self, car):
        x = car.x
        y = car.y
        lenght = car.car_length

        p1 = [car.x-car.car_length/4,car.y-car.car_width/2]
        p2 = [car.x+(0.75*car.car_length),car.y-car.car_width/2]
        p3 = [car.x+(0.75*car.car_length),car.y+car.car_width/2]
        p4 = [car.x-car.car_length/4,car.y+car.car_width/2]

        corners = (p1,p2,p3,p4)
        rotated_corners = []

        for p in corners:
            temp = []
            length = math.sqrt((p[0] - car.x)**2 + (car.y - p[1])**2)
            angle = math.atan2(car.y - p[1], p[0] - car.x)
            angle += car.orientation
            temp.append(car.x + length*math.cos(angle))
            temp.append(car.y - length*math.sin(angle))
            rotated_corners.append(temp)

        line1 = LineString((rotated_corners[0],rotated_corners[1],rotated_corners[2],rotated_corners[3]))

        aaa = []
        bbb = []
        for line in self.innerHitLine:
            for c in line:
                aaa.append(c)

        for line in self.outerHitLine:
            for c in line:
                bbb.append(c)


        line2 = LineString(aaa)
        line3 = LineString(bbb)



        intersection1 = (line1.intersection(line2))
        intersection2 = (line1.intersection(line3))

        if(isinstance(intersection1, shapely.geometry.multipoint.MultiPoint)):
                intersection1 = intersection1[len(intersection1)-1]
                
        if(isinstance(intersection2, shapely.geometry.multipoint.MultiPoint)):
            intersection2 = intersection2[len(intersection2)-1]

        if (len(intersection1.coords) > 0):
            return True

        if (len(intersection2.coords) > 0):
            return True
        
        return False

    def generateRacetrack(self, amount):
        loop = 0
        x = 0
        y = 0
        r = self.racewidth
        racetrack = []
        grid = []
        for i in range(2):
            xCenter, yCenter, gridX, gridY, inp = get_coords_straight(self.x_offset, self.y_offset, r,x,y)
            racetrack.append(Piece((xCenter, yCenter),inp))
            self.x_offset = xCenter
            self.y_offset = yCenter
            x = gridX
            y = gridY
            grid.append((x,y))    

        while(loop < amount):
            xCenter, yCenter, gridX, gridY, inp = get_coords(self.x_offset, self.y_offset, r,x,y)
            infinity = 0
            while(isRepeat(grid,gridX,gridY)):
                infinity = infinity + 1
                xCenter, yCenter, gridX, gridY, inp = get_coords(self.x_offset, self.y_offset, r,x,y)
                if(infinity > 20):
                    loop = 0
                    grid = []
                    racetrack = []
                    infinity = 0
                    self.x_offset = 500
                    self.y_offset = 500
                    x = 0
                    y = 0
                    for i in range(2):
                        xCenter, yCenter, gridX, gridY, inp = get_coords_straight(self.x_offset, self.y_offset, r,x,y)
                        racetrack.append(Piece((xCenter, yCenter),inp))
                        self.x_offset = xCenter
                        self.y_offset = yCenter
                        x = gridX
                        y = gridY
                        grid.append((x,y))        

            grid.append((gridX,gridY))
            racetrack.append(Piece((xCenter,yCenter),inp))
            loop = loop + 1
            self.x_offset = xCenter
            self.y_offset = yCenter
            x = gridX
            y = gridY

        for piece in racetrack:
            corners = (get_corners_of_hex(6, r, piece.center))
            inCorner1 = piece.input
            inCorner2 = inCorner1 + 1
            if(inCorner2 > 5):
                inCorner2 = 0

            self.checkpoints.append(corners[inCorner1])
            self.checkpoints.append(corners[inCorner2])

            piece.updateinput((corners[inCorner1], corners[inCorner2]))

            self.hex.append((get_corners_of_hex(6, r, piece.center)))


        self.start = racetrack[0].center
        for i in range(len(racetrack)-1):
                innerline, outerline, inhitline, outhitline = racetrack[i].generateCellTrack(racetrack[i+1].inputcorners, racetrack[i+1].input, self.racewidth)
                self.innerlines.append(innerline)
                self.outerlines.append(outerline)
                self.innerHitLine.append(inhitline)
                self.outerHitLine.append(outhitline)


def get_corners_of_hex(vertex_count, radius, position):
    n, r = vertex_count, radius
    x, y = position
    corners = []
    for i in range(n):
        corners.append((int(x + r * math.cos(2 * math.pi * i / n)), int(y + r * math.sin(2 * math.pi * i / n))))
    return corners

def isRepeat(grid, x,y):
    threshold = 3
    for point in grid:
        if(point[0] == x and point[1] == y):
            return True

    if(x > threshold or x < -threshold):
        return True

    if(y > threshold or y < -threshold):
        return True

    return False


