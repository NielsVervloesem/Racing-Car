import math
import random
from car import Car
from shapely.geometry import LineString, LinearRing
import shapely
from random import randrange

class Racetrack:
    def __init__(self, width, height, racetrack_width):
        self.outer_line = []
        self.inner_line = []
        self.checkpoints = []
        self.width = width
        self.height =  height
        self.racetrack_width = racetrack_width

        self.start = [(0,0)]

        x_offset = self.width / 2
        y_offset = self.height / 2

        for a in range(0, 628, 50):
            width = 150
            r = random.randint(250, (height / 2) - 10)

            x1 = r * math.cos(a/100)
            y1 = r * math.sin(a/100)
            self.outer_line.append((x1 + x_offset , y1 + y_offset))

            x2 = (r - width) * math.cos(a/100)
            y2 = (r - width) * math.sin(a/100)

            self.inner_line.append((x2 + x_offset , y2 + y_offset))
            
            x3 = (r - int(width/2)) * math.cos(a/100) + x_offset
            y3 = (r - int(width/2)) * math.sin(a/100) + y_offset
            if(self.start == [(0,0)]):
                self.start[0] = ((x3,y3))

            for a in range(0, 628, 1):
                r = 500
                x1 = r * math.cos(a/100)
                y1 = r * math.sin(a/100)
                self.checkpoints.append([(x1+x_offset,y1+ y_offset),(x2+x_offset,y2+ y_offset)])

    def smaller(self):
        self.racetrack_width = self.racetrack_width - 10
        x_offset = self.width / 2
        y_offset = self.height / 2

        for a in range(0, 628, 50):
            r = random.randint(200, (self.height / 2) - 10)

            x1 = r * math.cos(a/100)
            y1 = r * math.sin(a/100)
            self.outer_line.append((x1 + x_offset , y1 + y_offset))

            x2 = (r - self.racetrack_width) * math.cos(a/100)
            y2 = (r - self.racetrack_width) * math.sin(a/100)

            self.inner_line.append((x2 + x_offset , y2 + y_offset))
            
            x3 = (r - int(self.racetrack_width/2)) * math.cos(a/100)
            y3 = (r - int(self.racetrack_width/2)) * math.sin(a/100)

            self.checkpoints.append((int(x3+x_offset),int(y3+y_offset)))
            print("SMaller worked")

    def invertCheckpoints(self):
        self.checkpoints = self.checkpoints[::-1]
        
    def hit(self, car):
        print('??')
        x = car.position.x *32
        y = car.position.y *32
        print(x,y)
        lenght = car.length

        line1 = LineString([(x-lenght, y-lenght),(x+lenght, y-lenght),(x-lenght, y+lenght),(x+lenght, y+lenght)])
        line2 = LinearRing(self.inner_line)
        line3 = LinearRing(self.outer_line)

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
