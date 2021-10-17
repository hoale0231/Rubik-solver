import numpy as np
import random
from copy import copy
WHI, GRE, RED, BLU, ORA, YEL    = 0, 1, 2, 3, 4, 5
U, L, F, R, B, D                = 0, 1, 2, 3, 4, 5

# Face: U, L, F, R, B, D
# [0 1]
# [2 3]

ROTATE = {
    'U': ([F, 0, 1], [R, 0, 1], [B, 0, 1], [L, 0, 1]),
    'u': ([L, 0, 1], [B, 0, 1], [R, 0, 1], [F, 0, 1]),
    'D': ([L, 2, 3], [B, 2, 3], [R, 2, 3], [F, 2, 3]),
    'd': ([F, 2, 3], [R, 2, 3], [B, 2, 3], [L, 2, 3]),
    'F': ([U, 2, 3], [L, 3, 1], [D, 1, 0], [R, 0, 2]),
    'f': ([R, 0, 2], [D, 1, 0], [L, 3, 1], [U, 2, 3]),
    'B': ([R, 1, 3], [D, 3, 2], [L, 2, 0], [U, 0, 1]),
    'b': ([U, 0, 1], [L, 2, 0], [D, 3, 2], [R, 1, 3]),
    'R': ([U, 1, 3], [F, 1, 3], [D, 1, 3], [B, 2, 0]),
    'r': ([B, 2, 0], [D, 1, 3], [F, 1, 3], [U, 1, 3]),
    'L': ([B, 3, 1], [D, 0, 2], [F, 0, 2], [U, 0, 2]),
    'l': ([U, 0, 2], [F, 0, 2], [D, 0, 2], [B, 3, 1]),
}

GOAL_STATE = np.matrix([[WHI, WHI, WHI, WHI], 
                        [GRE, GRE, GRE, GRE],
                        [RED, RED, RED, RED],
                        [BLU, BLU, BLU, BLU],
                        [ORA, ORA, ORA, ORA],
                        [YEL, YEL, YEL, YEL]])

class CRubik:
    def __init__(self) -> None:
        self.color = GOAL_STATE.copy()
        self.route = []
    
    def moves(self, route: str):
        for move in route:
            face1, face2, face3, face4 = ROTATE[move]
            holder1, holder2 = self.color[face1[0], face1[1]], self.color[face1[0], face1[2]]
            self.color[face1[0], face1[1]], self.color[face1[0], face1[2]] = self.color[face2[0], face2[1]], self.color[face2[0], face2[2]]
            self.color[face2[0], face2[1]], self.color[face2[0], face2[2]] = self.color[face3[0], face3[1]], self.color[face3[0], face3[2]]
            self.color[face3[0], face3[1]], self.color[face3[0], face3[2]] = self.color[face4[0], face4[1]], self.color[face4[0], face4[2]]
            self.color[face4[0], face4[1]], self.color[face4[0], face4[2]] = holder1, holder2
            self.route += move

    def getHeuristic(self):   
        return (self.color != GOAL_STATE).sum()

    def copy(self):
        other = CRubik()
        other.color = self.color.copy()
        other.route = copy(self.route)
        return other

    def isGoalState(self):
        return (self.color == GOAL_STATE).all()

    # Make the position object hashable, i.e. addable to
    def __hash__(self) -> int:
        return hash(str(self.color))

    # Make the state object comparable, it helps set(), PriorityQueue() to work correctly
    def __eq__(self, o: object) -> bool:
        print("equal:",(self.color == o.color).all())
        return (self.color == o.color).all()
    def __gt__(self, o):
        return self.getHeuristic() > o.getHeuristic()
    def __lt__(self, o):
        return self.getHeuristic() < o.getHeuristic()

    # Print current state
    def __repr__(self):
        s  = f"   {self.color[0, 0]}{self.color[0, 1]}\n"
        s += f"   {self.color[0, 2]}{self.color[0, 3]}\n"
        s += f"{self.color[1, 0]}{self.color[1, 1]} {self.color[2, 0]}{self.color[2, 1]} {self.color[3, 0]}{self.color[3, 1]} {self.color[4, 0]}{self.color[4, 1]}\n"
        s += f"{self.color[1, 2]}{self.color[1, 3]} {self.color[2, 2]}{self.color[2, 3]} {self.color[3, 2]}{self.color[3, 3]} {self.color[4, 2]}{self.color[4, 3]}\n"
        s += f"   {self.color[5, 0]}{self.color[5, 1]}\n"
        s += f"   {self.color[5, 2]}{self.color[5, 3]}\n"
        s += f"{self.getHeuristic()}\n"
        return s

    def getFullChild(self):
        states = []
        for c in "UuFfRrDdBbLl":
            clone = self.copy()
            clone.moves(c)
            states.append(clone)
        return states
    
    def randomFace(self, n):
        S = "UuDdRrLlFfBb"
        route = ""
        for i in range(n):
            route += S[random.randrange(12)]
        self.moves(route)

if __name__ == "__main__":
    a = CRubik()
    print(a)
    a.moves('lRdl')
    print(a)
    a.moves('LDrL')
    print(a)