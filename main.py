from math import sin,cos
import pygame
import sys 

class Matrix:
    def __init__(self, contents: list):
        try:
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

    def __add__(self,mat2):
        if self.dimensions == mat2.dimensions:
            return type(self)([[self.contents[i][j] + mat2.contents[i][j] for j in range(self.length)] for i in range(self.height)]) 
        else: 
            return 

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
            
    def __rmul__(self,obj):
        if type(obj) == int:
            return type(self)([[self.contents[i][j] * obj for j in range(self.length)] for i in range(self.height)])
        
    def __str__(self):
        return str(self.contents)
    
    @classmethod
    def rotationMatrix(cls, angle: float,axis: str):
        matrices = {
            "anticlockwise" : Matrix([
                [cos(angle),-sin(angle)],
                [sin(angle),cos(angle)]
            ]),

            "clockwise" : Matrix([
                [cos(angle),-sin(angle)],
                [sin(angle),cos(angle)]
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

    def __init__(self, contents: list):
        for element in contents:
            if type(element) != int and type(element) != float and type(element) != list:
                raise Exception("Invalid Vector")
            elif type(element) == list:
                if len(element) != 1:
                    raise Exception("Invalid Vector")
        if type(contents[0]) == int:
            super().__init__([[i] for i in contents])
        else: 
            super().__init__(contents)
        self.vectorContents = [i[0] for i in self.contents] 
    
    def rotate(self,angle,axis):
        return Matrix.rotationMatrix(angle,axis)*self

class Vector3(Vector):
    def __init__(self, contents: list):
        super().__init__(contents)
    def project(self):
        return Vector2([self.vectorContents[i] for i in range(len(self.vectorContents)-1)])
    
class Vector2(Vector):
    def __init__(self, contents: list):
        super().__init__(contents)

    @property
    def toPygame(self):
        mat = [
            height/2,
            width/2
        ]
        return self+mat


class Circle:
    def __init__(self,coords):
        self.coords = coords

circles = []

pygame.init()

a = [
    [0,3,4],
    [2,5,4]
]

b = [[2],[3],[2]]
a = Matrix(a)
b = Vector(b)
c = Vector([3,4,5])
d = Matrix([
    [3,4,5],
    [2,3,1],
    [4,2,1]
])



width, height = 800, 600
black = 0,0,0
white = 255,255,255
window = pygame.display.set_mode((width, height))

pygame.display.set_caption("Volumes of Revolution")

running = True

circles.append(Circle(Vector([400,400])))

print(type(circles[0].coords))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    window.fill((white))
    for thing in circles:
        pygame.draw.circle(window,black,thing.coords.vectorContents,10)
        thing.coords = thing.coords.rotate(0.001,"anticlockwise")
        print(type(thing.coords.vectorContents))
    pygame.display.flip()

pygame.quit()
sys.exit()

