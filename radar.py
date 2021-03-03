from shapely.geometry import LineString
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

    def calculate_distance(self, line1, line2):
        line1 = LineString([radar, endpoint])
        line2 = LineString([(600,0),(600,400)])

        intersection = (line1.intersection(line2))

        if (len(intersection.coords) > 0):
            distanceLine = LineString([radar,list(intersection.coords)[0]])
            print("Angle %d = %f" % (angle, distanceLine.length))
        else:
            print("Angle %d = too far!" % (angle))
