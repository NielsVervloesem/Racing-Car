from shapely.geometry import LineString
import shapely
import math

class Radar:
    def __init__(self, x, y, radar_length, radar_angles, car_angle):
        self.x = x
        self.y = y
        self.radar_length = radar_length
        self.radar_angles = radar_angles
        self.radar_lines = []
        self.car_angle = car_angle
        self.updateRadar(self.x, self.y, self.car_angle)

        '''
        radar_len = 175
        angles = (15, -15 ,45 ,-45 ,180)
        '''
    def updateRadar(self, x, y, car_angle):
        self.car_angle = car_angle
        self.x = x
        self.y = y
        self.radar_lines = []
        for angle in self.radar_angles:
            endpoint = (self.x + math.cos(math.radians(angle - self.car_angle)) * self.radar_length, self.y + math.sin(math.radians(angle - self.car_angle)) * self.radar_length)
            self.radar_lines.append([(self.x, self.y), endpoint])

    def calculate_distance(self, racetrack):
        distances = []

        innerLine = LineString(racetrack.innerLine)
        outerline = LineString(racetrack.outerLine)
        
        for line in self.radar_lines:
            line = LineString(line)
            intersection = (line.intersection(innerLine))
            
            #CLEAN UP SOMEDAY
            if(isinstance(intersection, shapely.geometry.multipoint.MultiPoint)):
                intersection = intersection[len(intersection)-1]

            if (len(intersection.coords) > 0):
                distanceLine = LineString([(self.x, self.y),list(intersection.coords)[0]])
                distances.append(distanceLine.length)
            else:
                distances.append(self.radar_length)

            intersection = (line.intersection(outerline))
            
            if(isinstance(intersection, shapely.geometry.multipoint.MultiPoint)):
                intersection = intersection[len(intersection)-1]

            if (len(intersection.coords) > 0):
                distanceLine = LineString([(self.x, self.y),list(intersection.coords)[0]])
                distances.append(distanceLine.length)
            else:
                distances.append(self.radar_length)

        return distances