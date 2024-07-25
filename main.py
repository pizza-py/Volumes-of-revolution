import math

class Matrix:
    def __init__(self, contents: list):
        self.height = len(contents)
        self.length = len(contents[0])
        self.contents = contents
    def __len__(self) -> str:
        return str(self.length)+"x"+str(self.height)
    
def MatMul(mat1: Matrix, mat2: Matrix) -> Matrix:
    if mat1.length != mat2.height:
        return
    else:
        return
def validateMatrix(mat1):
    try:
        if type(mat1) != list:
            return False

        presumedLength = len(mat1[0])
 
        for i in range(len(mat1)):
            if len(mat1[i]) != presumedLength:
                return False
            elif type(mat1[i]) != list:
                return False
    except:
        return False
    return True

matrix = [1,1,1]
print(validateMatrix(matrix))

