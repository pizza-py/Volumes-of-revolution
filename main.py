import math


class Matrix:
    def __init__(self, contents: list):
        #Verification
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
            return Matrix([[self.contents[i][j] + mat2.contents[i][j] for j in range(self.length)] for i in range(self.height)]) 
        else: 
            return 

    def __mul__(self,obj):
        if type(obj) == int:
            return Matrix([[self.contents[i][j] * obj for j in range(self.length)] for i in range(self.height)])
        
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
                return Matrix(resultMat)
            else:
                return
            
    def __rmul__(self,obj):
        if type(obj) == int:
            return Matrix([[self.contents[i][j] * obj for j in range(self.length)] for i in range(self.height)])
        
    def __str__(self):
        return str(self.contents)
    
    @classmethod
    def fromCoordinates(cls, contents):
        return cls([[i] for i in contents])

'''
class Coordinate(Matrix):
    def __init__(self, contents: list):
        for element in contents:
            print(type(element))
            if type(element) != int and type(element) != float:
                raise Exception("Invalid Coordinate")
        super().__init__([[i] for i in contents])
'''
