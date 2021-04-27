import pickle
from random import randrange
import os
class Piece:
    def __init__(self, center, input):
        self.center = center
        self.input = input
        self.inputcorners = []
        self.outputcorners = []

    def updateinput(self,inp):
        self.inputcorners = inp

    def generateCellTrack(self,outputcorners, output):
        inverse = False
        centerx = self.center[0]
        centery = self.center[1]
        innerline = []
        outerline = []
        output = (output + 3) % 6
        print(self.input, output)

        if(self.input == 0):
            inverse = True
        if(not(output == 0)):
            string = int(str(self.input) +  str(output))
            print(string)
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
                outerline.append((centerx + line[0], centery + line[1]))
            outerline.append(outputcorners[0])

            innerline.append(self.inputcorners[1])
            for line in racetrack[0]:
                innerline.append((centerx+line[0], centery + line[1]))
            innerline.append(outputcorners[1])

            return innerline, outerline
        else:
            innerline.append(outputcorners[1])
            for line in racetrack[1]:
                innerline.append((centerx + line[0], centery + line[1]))
            innerline.append(self.inputcorners[1])
            
            outerline.append(outputcorners[0])
            for line in racetrack[0]:
                outerline.append((centerx+line[0], centery + line[1]))
            outerline.append(self.inputcorners[0])

            return innerline, outerline
