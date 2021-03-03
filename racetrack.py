import math
import random
from car import Car
from shapely.geometry import LineString


class Racetrack:
    def __init__(self, width, height):
        self.outerLine = []
        self.innerLine = []
        self.checkpoints = []

        xOffset = width / 2
        yOffset = height / 2

        for a in range(0, 628, 50):
            r = random.randint(200, (height / 2) - 10)

            x1 = r * math.cos(a/100)
            y1 = r * math.sin(a/100)
            self.outerLine.append((x1 + xOffset , y1 + yOffset))

            x2 = (r - 100) * math.cos(a/100)
            y2 = (r - 100) * math.sin(a/100)

            self.innerLine.append((x2 + xOffset , y2 + yOffset))
            
            x3 = (r - 50) * math.cos(a/100)
            y3 = (r - 50) * math.sin(a/100)

            self.checkpoints.append((int(x3+xOffset),int(y3+yOffset)))

    def hit(self, car):
        x = car.position.x
        y = car.position.y
        lenght = car.length
        line1 = LineString([(x-lenght, y-lenght),(x+lenght, y-lenght),(x-lenght, y+lenght),(x+lenght, y+lenght)])
        line2 = LineString(self.innerLine)
        line3 = LineString(self.outerLine)

        intersection1 = (line1.intersection(line2))
        intersection2 = (line1.intersection(line3))

        if (len(intersection1.coords) > 0):
            return True

        if (len(intersection2.coords) > 0):
            return True
        
        return False
