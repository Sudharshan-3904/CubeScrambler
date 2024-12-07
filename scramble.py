import time
import random
import keyboard

class CubeType:
    def __init__(self):
        self.moves = None
        self.fru_moves = None
        self.generated = []
        self.fru_only = False
        self.seperete = True
        self.sepLen = 5
        self.fru_only = False
        self.length = 25

    def list_to_str(self, ipList=[]):
        resultString = ""
        for i in ipList:
            resultString += str(i)
            resultString += " "
        
        return resultString
    
    def generate_moves(self):
        if not self.fru_only:
            for _ in range(self.length):
                self.generated.append(random.choice(self.moves))
        
        else:
            for _ in range(self.length):
                self.generated.append(random.choice(self.fru_moves))
        
        if self.seperete:
            for i in range(0, self.length, (self.sepLen + 1)):
                self.generated.insert(i, "-")
            self.generated.pop(0)
        
        return_data = self.generated.copy()
        self.generated = []
        return self.list_to_str(return_data)

class Cube_3x3(CubeType):
    def __init__(self):
        super().__init__()
        self.moves = ("F", "B", "R", "L", "U", "D", "F'", "B'", "R'", "L'", "U'", "D'", "F2", "B2", "R2", "L2", "U2", "D2")
        self.fru_moves = ("F", "R", "U", "F'", "R'", "U'", "F2", "R2", "U2", "F2'", "R2'", "U2'")

    def new_moves(self) -> str:
        return super().generate_moves()

class Cube_4x4(CubeType):
    def __init__(self):
        super().__init__()
        self.moves = ("F", "B", "R", "L", "U", "D", "F'", "B'", "R'", "L'", "U'", "D'", "F2", "B2", "R2", "L2", "U2", "D2", "f", "b", "r", "l", "u", "d", "f'", "b'", "r'", "l'", "u'", "d'")
        self.fru_moves = ("F", "R", "U", "F'", "R'", "U'", "F2", "R2", "U2", "F2'", "R2'", "U2'")
        self.length=40
    
    def new_moves(self) -> str:
        return super().generate_moves()

class Cube_5x5(CubeType):
    def __init__(self):
        super().__init__()
        self.moves = ("F", "B", "R", "L", "U", "D", "F'", "B'", "R'", "L'", "U'", "D'", "F2", "B2", "R2", "L2", "U2", "D2", "f", "b", "r", "l", "u", "d", "f'", "b'", "r'", "l'", "u'", "d'")
        self.fru_moves = ("F", "R", "U", "F'", "R'", "U'", "F2", "R2", "U2", "F2'", "R2'", "U2'")

    def new_moves(self) -> str:
        new_data = super().generate_moves()
        super().generated = list()
        return new_data
