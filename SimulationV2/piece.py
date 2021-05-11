import pickle
from random import randrange
import os
import time
from shapely.geometry import LineString, LinearRing

class Piece:
    def __init__(self, center, input):
        self.center = center
        self.input = input
        self.inputcorners = []
        self.outputcorners = []
        self.innerHitLine = []
        self.outerHitLine = []

    def updateinput(self,inp):
        self.inputcorners = inp

    def generateCellTrack(self,outputcorners, output):
        inverse = False
        centerx = self.center[0]
        centery = self.center[1]
        innerline = []
        outerline = []
        output = (output + 3) % 6


        if(self.input == output):
            if(self.input == 0):
                output = 3
            if(self.input == 1):
                output = 4
            if(self.input == 2):
                output = 5
            if(self.input == 3):
                output = 0
            if(self.input == 4):
                output = 1
            if(self.input == 5):
                output = 2

        if(self.input == 0):
            inverse = True
        if(not(output == 0)):
            string = int(str(self.input) +  str(output))
            if(self.input == 2):
                if(string < 22):
                    inverse = True
            if(self.input == 3):
                if(string < 33):
                    inverse = True
            if(self.input == 4):
                if(string < 44):
                    inverse = True
            if(self.input == 5):
                if(string < 55):
                    inverse = True
   
        if(inverse):
            path = r'pieces/' + str(output) + str(self.input)
        else:
            path = r'pieces/' + str(self.input) + str(output)

        files = os.listdir(path)
        racetrack_file = path + r'/' + files[randrange(len(files))-1]
        with open(racetrack_file, "rb") as f:
            racetrack = pickle.load(f)   

        if(inverse):
            outerline.append(self.inputcorners[0])
            for line in racetrack[1]:
                outerline.append((centerx + line[0]*2, centery + line[1]*2))
            outerline.append(outputcorners[0])

            innerline.append(self.inputcorners[1])
            for line in racetrack[0]:
                innerline.append((centerx+line[0]*2, centery + line[1]*2))
            innerline.append(outputcorners[1])

            aaa = []
            bbb = []
            for line in innerline:
                for c in line:
                    aaa.append(c)

            for line in outerline:
                for c in line:
                    bbb.append(c)
            inner_line = LineString(aaa)
            outer_line = LineString(bbb)

            return aaa, bbb, innerline, outerline
        else:
            innerline.append(self.inputcorners[1])
            for line in racetrack[1]:
                innerline.append((centerx + line[0]*2, centery + line[1]*2))
            innerline.append(outputcorners[1])

            self.innerHitLine.append(self.inputcorners[1])
            racetrack[1].reverse()
            for line in racetrack[1]:
                self.innerHitLine.append((centerx + line[0]*2, centery + line[1]*2))
            self.innerHitLine.append(outputcorners[1])
            
            outerline.append((outputcorners[0]))
            for line in racetrack[0]:
                outerline.append((centerx+line[0]*2, centery + line[1]*2))
            outerline.append((self.inputcorners[0]))

            self.outerHitLine.append(self.inputcorners[0])
            racetrack[0].reverse()
            for line in racetrack[0]:
                self.outerHitLine.append((centerx + line[0]*2, centery + line[1]*2))
            self.outerHitLine.append(outputcorners[0])

            aaa = []
            bbb = []
            for line in innerline:
                for c in line:
                    aaa.append(c)

            for line in outerline:
                for c in line:
                    bbb.append(c)
            inner_line = LineString(aaa)
            outer_line = LineString(bbb)

            return aaa, bbb, innerline, outerline
            
