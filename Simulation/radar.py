from shapely.geometry import LineString, LinearRing
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

    def updateRadar(self, x, y, car_angle):
        self.car_angle = car_angle
        self.x = x
        self.y = y
        self.radar_lines = []
        for angle in self.radar_angles:
            endpoint = (self.x + math.cos(math.radians(angle - self.car_angle)) * self.radar_length, self.y + math.sin(math.radians(angle - self.car_angle)) * self.radar_length)
            self.radar_lines.append([(self.x, self.y), endpoint])

    #REFACTOR THIS@@
    def calculate_distance(self, racetrack):
        distances = []

        aaa = []
        bbb = []
        for line in racetrack.innerHitLine:
            for c in line:
                aaa.append(c)

        for line in racetrack.outerHitLine:
            for c in line:
                bbb.append(c)
        inner_line = LineString(aaa)
        outer_line = LineString(bbb)
        
        for line in self.radar_lines:
            line = LineString(line)
            intersection = (line.intersection(inner_line))
            
            if(isinstance(intersection, shapely.geometry.multilinestring.MultiLineString)):
                intersection = intersection[0]
            #CLEAN UP SOMEDAY
            if(isinstance(intersection, shapely.geometry.multipoint.MultiPoint)):
                intersection = intersection[len(intersection)-1]

            if (len(intersection.coords) > 0):
                distanceLine = LineString([(self.x, self.y),list(intersection.coords)[0]])
                distances.append(distanceLine.length)
            else:
                distances.append(self.radar_length)

            intersection = (line.intersection(outer_line))
            if(isinstance(intersection, shapely.geometry.multilinestring.MultiLineString)):
                intersection = intersection[0]

            if(isinstance(intersection, shapely.geometry.multipoint.MultiPoint)):
                intersection = intersection[len(intersection)-1]

            if (len(intersection.coords) > 0):
                distanceLine = LineString([(self.x, self.y),list(intersection.coords)[0]])
                distances.append(distanceLine.length)
            else:
                distances.append(self.radar_length)

        realDistances = []

        #ugly code :@
        if(distances[0] > distances[1]):
            realDistances.append(distances[1])
        else:
            realDistances.append(distances[0])

        if(distances[2] > distances[3]):
            realDistances.append(distances[3])
        else:
            realDistances.append(distances[2])

        if(distances[4] > distances[5]):
            realDistances.append(distances[5])
        else:
            realDistances.append(distances[4])

        if(distances[6] > distances[7]):
            realDistances.append(distances[7])
        else:
            realDistances.append(distances[6])

        if(distances[8] > distances[9]):
            realDistances.append(distances[9])
        else:
            realDistances.append(distances[8])
    
        if(distances[10] > distances[11]):
            realDistances.append(distances[11])
        else:
            realDistances.append(distances[10])

        if(distances[12] > distances[13]):
            realDistances.append(distances[13])
        else:
            realDistances.append(distances[12])

        if(distances[14] > distances[15]):
            realDistances.append(distances[15])
        else:
            realDistances.append(distances[14])

        rds = []
        for rd in realDistances:
            rds.append(rd / self.radar_length)
            
        return rds
