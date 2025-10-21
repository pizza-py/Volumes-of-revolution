#Imports

from math import sin,cos,tan, pi,e
import pygame
import sys 

#Constants

width, height = 800, 600
black = 0,0,0  #Values for pygame BLACK
white = 255,255,255  #Values for pygame WHITE
rotationsPerWidth = 3  #Measure of Sensitivity - how many times the graph rotates when you move the mouse from the far left to the far right (politics har har)
axisLength = (0.4 * min([width,height]))
graphResolution = 5  #The detail of the actual graph - The smaller this number the higher the resolution (and also the lag)
circleResolution = 50 #The detail of the circles which bound the ends of the shape - The higher this number the higher the resolution (yeah it's confusing but whatever)
numberOfRevolutions = 10  #How many revolution lines are rendered
axisWidth = 2

class Matrix:
    '''
    Matrix module: This is where the magic happens. Every rotation is calculated as the product of the vector matrix and a rotation matrix, but I added a few other operations as well
    '''
    def __init__(self, contents: list):
        try: #Data validation so boring
            if type(contents) != list:
                raise Exception
            presumedLength = len(contents[0])

            for i in range(len(contents)):
                if len(contents[i]) != presumedLength:
                    raise Exception
                elif type(contents[i]) != list:
                    raise Exception
        except:
            raise Exception("Invalid Matrix")

        self.height = len(contents)
        self.length = len(contents[0])
        self.contents = contents
        self.dimensions = str(self.height)+"x"+str(self.length)

    #Takes two matrices and adds them together
    def __add__(self,mat2):
        if self.dimensions == mat2.dimensions:
            return type(self)([[self.contents[i][j] + mat2.contents[i][j] for j in range(self.length)] for i in range(self.height)]) 
        else: 
            return 
        

    #Takes two matrices and multiplies them together
    def __mul__(self,obj): 
        if type(obj) == int:
            return type(self)([[self.contents[i][j] * obj for j in range(self.length)] for i in range(self.height)])
        
        elif issubclass(type(obj),Matrix):
            if self.length == obj.height:
                resultMat = []
                for i in range(self.height):
                    resultMat.append([])
                    for j in range(obj.length):
                        total = 0
                        for k in range(self.length): #Can Be either self.length or obj.height
                            total += self.contents[i][k] * obj.contents[k][j]
                        resultMat[i].append(total)
                return type(obj)(resultMat)
            else:
                return
            
    def __rmul__(self,obj): #Just in case I want to write integer * matrix instead of matrix * integer
        if type(obj) == int:
            return type(self)([[self.contents[i][j] * obj for j in range(self.length)] for i in range(self.height)])
        
    def __str__(self): #Debugging purposes
        return str(self.contents)
    
    #This is important - it returns a fully geared rotation matrix from a bank of "templates" of important matrices.
    @classmethod
    def rotationMatrix(cls, angle: float,axis: str):
        matrices = {
            "anticlockwise" : Matrix([
                [cos(angle),-sin(angle)],
                [sin(angle),cos(angle)]
            ]),

            "clockwise" : Matrix([
                [cos(angle),sin(angle)],
                [-sin(angle),cos(angle)]
            ]),

            "x" : Matrix([
            [1,0,0],
            [0,cos(angle),-sin(angle)],
            [0,sin(angle),cos(angle)]
            ]),

            "y" : Matrix([
            [cos(angle),0,sin(angle)],
            [0,1,0],
            [-sin(angle),0,cos(angle)]
            ]),

            "z" : Matrix([
            [cos(angle),-sin(angle),0],
            [sin(angle),cos(angle),0],
            [0,0,1]
            ])
        }
        return matrices[axis.lower()]

class Vector(Matrix):

    '''
    Vector class: I wanted something different to distinguish between matrices and vectors (essentially coordinates) because they need a few extra properties

    Vectors are a subclass of Matrices so they inherit all of its properties and functions
    '''
    def __init__(self, contents: list):
        if type(contents) == Vector: #More data validation
            contents = contents.vectorContents
        for element in contents:
            if type(element) != int and type(element) != float and type(element) != list:
                raise Exception("Invalid Vector")
            elif type(element) == list:
                if len(element) != 1:
                    raise Exception("Invalid Vector")
        if type(contents[0]) == int or type(contents[0]) == float:
            super().__init__([[i] for i in contents])
        else: 
            super().__init__(contents)
        self.vectorContents = [i[0] for i in self.contents] 
    
    def rotate(self,angle,axis): #Takes a point and rotates it
        return Matrix.rotationMatrix(angle,axis)*self
    
    @property
    def projectToPygame(self): #Takes a multidimensional vector and projects it to 2D
        vec2 = Vector([self.vectorContents[0], -self.vectorContents[1]])
        return (vec2+Vector([width / 2,height / 2])).vectorContents


class obj:
    '''
    Obj class: One last class for handling objects such as the axis or the graph itself

    An obj is a collection of lines in order, and lines themselves are just a double of 2 points (I couldn't be asked to make a line class)
    '''
    objects = []  #An important record of all the object instances
    def __init__(self, lines, lineInfo = {}): #I actually used kwargs for once
        self.lines = [[Vector(point) for point in line] for line in lines]
        self.lineInfo = lineInfo
        obj.objects.append(self)
        

    def draw(self): #Draws all the lines in the object
        for line in self.lines:
            pygame.draw.line(window, black,line[0].projectToPygame,line[1].projectToPygame, **self.lineInfo)

    def rotate(self,angle,axis): #Rotates the entire object by rotating each point in each line
        newObj = []
        for i in range(len(self.lines)):
            newObj.append([point.rotate(angle,axis) for point in self.lines[i]])
        self.lines = [[Vector(point) for point in line] for line in newObj]

    def rotateClone(self,angle,axis): #Core of the project - generates a new object at an angle to the old one (use this to generate revolutions)
        newObj = []
        for i in range(len(self.lines)):
            newObj.append([point.rotate(angle,axis) for point in self.lines[i]])
        return obj(newObj)


#Graph Sketching
#This part is quite messy, I should clean it up

try:
    print("Enter a function in terms of x: ")
    userFunc = input()
    f = lambda x: eval(userFunc) #Actually used lambda as well I'm balling
except:
    print("Invalid python statement.")
    quit()


try: #Believe it or not, more data validation
    print("Enter your lower bound: ")
    userLower = eval(input())
    print("Enter your upper bound: ")
    userUpper = eval(input())
    if userLower >= userUpper:
        raise Exception

    boundRange = userUpper-userLower
    xlim = max(abs(userLower),abs(userUpper))*1.2
    xScaleFactor = axisLength/xlim
except:
    print("Invalid bounds.")
    quit()

#Perhaps x+mousewheel -> Scroll only in x direction
#Press D to return to default scroll
try:
    graph = []
    yvalues = []
    for i in range(0,100, graphResolution):
        x1 = userLower + i*boundRange/100
        if i == range(0,100, graphResolution)[-1]:
            x2 = userUpper
        else:
            x2 = userLower + ((i+graphResolution)*boundRange)/100
        graph.append([[x1,f(x1),0],[x2,f(x2),0]])
        if i == 0:
            yvalues.append(abs(f(x1)))
        yvalues.append(abs(f(x2)))
    ylim = max(yvalues) * 1.2
    yScaleFactor = axisLength/ylim
    for lines in graph:
        for line in lines: #Getting the shape on a readable scale
            line[0] *= xScaleFactor
            line[1] *= yScaleFactor
    graph = obj(graph)
    firstCircle = [[graph.lines[0][0].rotate(num*(pi/(circleResolution/2)),"x"), graph.lines[0][0].rotate((num+1)*(pi/(circleResolution/2)),"x")] for num in range(circleResolution)]
    lastCircle = [[graph.lines[-1][1].rotate(num*(pi/(circleResolution/2)),"x"), graph.lines[-1][1].rotate((num+1)*(pi/(circleResolution/2)),"x")] for num in range(circleResolution)]
    firstCircle = obj(firstCircle)
    lastCircle = obj(lastCircle) #Circles which bound the ends of the shape
    for i in range(numberOfRevolutions):
        graph.rotateClone(i*(pi/(numberOfRevolutions/2)),"x")
except:
    print("Error Occured while trying to calculate values - Maybe your graph is undefined for some value in your range?")
    quit()


#Objects

axis = [
    [[-1 * axisLength, 0,0],[axisLength, 0,0]],
    [[0, -1 * axisLength,0],[0,axisLength,0]],
    [[0, 0, -1 * axisLength],[0,0,axisLength]],
]

axis = obj(axis,{"width": axisWidth})


pygame.init()
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Volumes of Revolution")
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            dist = event.rel
            if pygame.mouse.get_pressed()[0]:
                rotX = rotationsPerWidth * ((pi*dist[1])/width)
                rotY = rotationsPerWidth * ((pi*dist[0])/width)
                for object in obj.objects:
                    object.rotate(rotX, "x")
                    object.rotate(rotY, "y")
    window.fill((white))
    for object in obj.objects:
        object.draw()

    pygame.display.flip()
    pygame.event.pump()

pygame.quit()
sys.exit()

