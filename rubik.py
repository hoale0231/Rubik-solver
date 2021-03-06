from copy import copy, deepcopy
from os import pardir
from queue import Queue
import json
import random

'''
        [0] [1]
           U
        [3] [2]

[0] [3] [3] [2] [2] [1] [1] [0]
   L       F       R       B 
[7] [4] [4] [5] [5] [6] [6] [7]

        [4] [5]
           D
        [7] [6]

Orientation:
    0: White, yellow are in face Up or Down
    1: White, yellow 
    2: White, yellow 
'''
# Indexing cubies
ULB, URB, URF, ULF, DLF, DRF, DRB, DLB = 0, 1, 2, 3, 4, 5, 6, 7
# Rubik's cube is solved if each sub-cubie is in the right place and their orientation is 0
GOAL_POSITION = [ULB, URB, URF, ULF, DLF, DRF, DRB, DLB]
GOAL_ORIENTATION = [0]*8
# Color corresponding to each cubie in goal state
COLOR = [['w', 'g', 'o'],['w', 'o', 'b'],['w', 'b', 'r'],['w', 'r', 'g'],['y', 'g', 'r'],['y', 'r', 'b'],['y', 'b', 'o'],['y', 'o', 'g']]
PAIR_CUBES = [(0, 1), (2, 3), (4, 5), (6, 7), (0, 7), (1, 6), (2, 5), (3, 4), (0, 3), (1, 2), (4, 7), (5, 6)]

def getColor(p, o):
    if p == -1: return '_'
    return COLOR[p][o]

DB = json.load(open('db.json')) 
DB2 = json.load(open('dbPair.json'))

class Rubik:
    mode = 3

    def __init__(self, cube = GOAL_POSITION, orie = GOAL_ORIENTATION):
        self.cube = copy(cube)      # Store cube in order of position from 0 -> 7 according to the above convention
        self.orie = copy(orie)      # Store orientation of cubie in order of position from 0 -> 7 according to the above convention
        self.route = str()          # Store moved steps
        self.heuristic = 0          # Store heuristic value

    # Copy constructor
    def copy(self):
        o = Rubik()
        o.cube  = copy(self.cube)
        o.orie  = copy(self.orie)
        o.route = copy(self.route)
        return o

    # Check if rubik's cube solved
    def isGoalState(self):
        return self.cube == GOAL_POSITION and self.orie == GOAL_ORIENTATION
    
    # Check if a sub-cube is correct position and orientation. It's help calc heuristic value
    def isCorrectPositionCube(self, index):
        return self.cube[index] == index and self.orie[index] == 0

    # Calc heuristic value of current state
    def getHeuristic(self):
        if self.heuristic == 0: 
            if self.mode == 0:
                self.heuristic = (sum([o != 0 for o in self.orie]) + sum([i != self.cube[i] for i in range(8)])) / 8 + len(self.route)
            if self.mode == 1:
                self.heuristic = sum([DB[self.cube[i]][str(self.orie[i]*10+i)] for i in range(8)]) /4 + len(self.route)
            if self.mode == 2:
                pos_cubes = [-1] * 8 # Record position of each cube in current state
                for i in range(8):
                    pos_cubes[self.cube[i]] = i
                self.heuristic = sum([DB2[pair[0]][str(pair[1])][str(self.orie[pos_cubes[pair[0]]]*1000 + pos_cubes[pair[0]]*100
                    + self.orie[pos_cubes[pair[1]]]*10 + pos_cubes[pair[1]])] for pair in PAIR_CUBES]) / 6 + len(self.route)
        return self.heuristic

    # Make the position object hashable, i.e. addable to set()
    def __hash__(self):
        return hash((tuple(self.cube), tuple(self.orie)))
    
    # Make the state object comparable, it helps set(), PriorityQueue() to work correctly
    def __eq__(self, o: object) -> bool:
        return self.cube == o.cube and self.orie == o.orie
    def __gt__(self, o):
        return self.getHeuristic() > o.getHeuristic()
    def __lt__(self, o):
        return self.getHeuristic() < o.getHeuristic()

    # Get color of specific face
    def getFaceColor(self, face):
        if face == 'U':
            return [COLOR[self.cube[0]][self.orie[0]], COLOR[self.cube[1]][self.orie[1]], COLOR[self.cube[3]][self.orie[3]], COLOR[self.cube[2]][self.orie[2]]]
        if face == 'L':
            return [COLOR[self.cube[0]][self.orie[0] - 2], COLOR[self.cube[3]][self.orie[3] - 1], COLOR[self.cube[7]][self.orie[7] - 1], COLOR[self.cube[4]][self.orie[4] - 2]]
        if face == 'F':
            return [COLOR[self.cube[3]][self.orie[3] - 2], COLOR[self.cube[2]][self.orie[2] - 1], COLOR[self.cube[4]][self.orie[4] - 1], COLOR[self.cube[5]][self.orie[5] - 2]]
        if face == 'R':
            return [COLOR[self.cube[2]][self.orie[2] - 2], COLOR[self.cube[1]][self.orie[1] - 1], COLOR[self.cube[5]][self.orie[5] - 1], COLOR[self.cube[6]][self.orie[6] - 2]]
        if face == 'B':
            return [COLOR[self.cube[1]][self.orie[1] - 2], COLOR[self.cube[0]][self.orie[0] - 1], COLOR[self.cube[6]][self.orie[6] - 1], COLOR[self.cube[7]][self.orie[7] - 2]]
        if face == 'D':
            return [COLOR[self.cube[4]][self.orie[4]], COLOR[self.cube[5]][self.orie[5]], COLOR[self.cube[7]][self.orie[7]], COLOR[self.cube[6]][self.orie[6]]]

    # Print 2d format current state to console
    def __repr__(self):
        s  = f"   {COLOR[self.cube[0]][self.orie[0]]}{COLOR[self.cube[1]][self.orie[1]]}\n"
        s += f"   {COLOR[self.cube[3]][self.orie[3]]}{COLOR[self.cube[2]][self.orie[2]]}\n"
        s += f"{COLOR[self.cube[0]][self.orie[0] - 2]}{COLOR[self.cube[3]][self.orie[3] - 1]} {COLOR[self.cube[3]][self.orie[3] - 2]}{COLOR[self.cube[2]][self.orie[2] - 1]} {COLOR[self.cube[2]][self.orie[2] - 2]}{COLOR[self.cube[1]][self.orie[1] - 1]} {COLOR[self.cube[1]][self.orie[1] - 2]}{COLOR[self.cube[0]][self.orie[0] - 1]}\n"
        s += f"{COLOR[self.cube[7]][self.orie[7] - 1]}{COLOR[self.cube[4]][self.orie[4] - 2]} {COLOR[self.cube[4]][self.orie[4] - 1]}{COLOR[self.cube[5]][self.orie[5] - 2]} {COLOR[self.cube[5]][self.orie[5] - 1]}{COLOR[self.cube[6]][self.orie[6] - 2]} {COLOR[self.cube[6]][self.orie[6] - 1]}{COLOR[self.cube[7]][self.orie[7] - 2]}\n"
        s += f"   {COLOR[self.cube[4]][self.orie[4]]}{COLOR[self.cube[5]][self.orie[5]]}\n"
        s += f"   {COLOR[self.cube[7]][self.orie[7]]}{COLOR[self.cube[6]][self.orie[6]]}"
        return s

    # Legal moves: U, u ~ U', D, d ~ D', R, r ~ R', L, l ~ L', F, f ! F', B, b ~ B'
    # They rotate a face of rubik's cube, include: swap positions of cubie and set cubie's orientation after rotate. 
    def U(self):
        self.cube[ULB], self.cube[URB], self.cube[URF], self.cube[ULF] = self.cube[ULF], self.cube[ULB], self.cube[URB], self.cube[URF]
        self.orie[ULB], self.orie[URB], self.orie[URF], self.orie[ULF] = self.orie[ULF], self.orie[ULB], self.orie[URB], self.orie[URF]

    def u(self):
        self.cube[ULB], self.cube[URB], self.cube[URF], self.cube[ULF] = self.cube[URB], self.cube[URF], self.cube[ULF], self.cube[ULB]
        self.orie[ULB], self.orie[URB], self.orie[URF], self.orie[ULF] = self.orie[URB], self.orie[URF], self.orie[ULF], self.orie[ULB]

    def D(self):
        self.cube[DLB], self.cube[DRB], self.cube[DRF], self.cube[DLF] = self.cube[DRB], self.cube[DRF], self.cube[DLF], self.cube[DLB]
        self.orie[DLB], self.orie[DRB], self.orie[DRF], self.orie[DLF] = self.orie[DRB], self.orie[DRF], self.orie[DLF], self.orie[DLB]

    def d(self):
        self.cube[DLB], self.cube[DRB], self.cube[DRF], self.cube[DLF] = self.cube[DLF], self.cube[DLB], self.cube[DRB], self.cube[DRF]
        self.orie[DLB], self.orie[DRB], self.orie[DRF], self.orie[DLF] = self.orie[DLF], self.orie[DLB], self.orie[DRB], self.orie[DRF]

    def R(self):
        self.cube[URF], self.cube[URB], self.cube[DRB], self.cube[DRF] = self.cube[DRF], self.cube[URF], self.cube[URB], self.cube[DRB]
        self.orie[URF], self.orie[URB], self.orie[DRB], self.orie[DRF] = (self.orie[DRF] + 1) % 3, (self.orie[URF] + 2) % 3, (self.orie[URB] + 1) % 3, (self.orie[DRB] + 2) % 3

    def r(self):
        self.cube[URF], self.cube[URB], self.cube[DRB], self.cube[DRF] = self.cube[URB], self.cube[DRB], self.cube[DRF], self.cube[URF]
        self.orie[URF], self.orie[URB], self.orie[DRB], self.orie[DRF] = (self.orie[URB] + 1) % 3, (self.orie[DRB] + 2) % 3, (self.orie[DRF] + 1) % 3, (self.orie[URF] + 2) % 3
    
    def L(self):
        self.cube[ULF], self.cube[ULB], self.cube[DLB], self.cube[DLF] = self.cube[ULB], self.cube[DLB], self.cube[DLF], self.cube[ULF]
        self.orie[ULF], self.orie[ULB], self.orie[DLB], self.orie[DLF] = (self.orie[ULB] + 2) % 3, (self.orie[DLB] + 1) % 3, (self.orie[DLF] + 2) % 3, (self.orie[ULF] + 1) % 3

    def l(self):
        self.cube[ULF], self.cube[ULB], self.cube[DLB], self.cube[DLF] = self.cube[DLF], self.cube[ULF], self.cube[ULB], self.cube[DLB]
        self.orie[ULF], self.orie[ULB], self.orie[DLB], self.orie[DLF] = (self.orie[DLF] + 2) % 3, (self.orie[ULF] + 1) % 3, (self.orie[ULB] + 2) % 3, (self.orie[DLB] + 1) % 3

    def F(self):
        self.cube[ULF], self.cube[URF], self.cube[DRF], self.cube[DLF] = self.cube[DLF], self.cube[ULF], self.cube[URF], self.cube[DRF]
        self.orie[ULF], self.orie[URF], self.orie[DRF], self.orie[DLF] = (self.orie[DLF] + 1) % 3, (self.orie[ULF] + 2) % 3, (self.orie[URF] + 1) % 3, (self.orie[DRF] + 2) % 3
    
    def f(self):
        self.cube[ULF], self.cube[URF], self.cube[DRF], self.cube[DLF] = self.cube[URF], self.cube[DRF], self.cube[DLF], self.cube[ULF]
        self.orie[ULF], self.orie[URF], self.orie[DRF], self.orie[DLF] = (self.orie[URF] + 1) % 3, (self.orie[DRF] + 2) % 3, (self.orie[DLF] + 1) % 3, (self.orie[ULF] + 2) % 3

    def B(self):
        self.cube[ULB], self.cube[URB], self.cube[DRB], self.cube[DLB] = self.cube[URB], self.cube[DRB], self.cube[DLB], self.cube[ULB]
        self.orie[ULB], self.orie[URB], self.orie[DRB], self.orie[DLB] = (self.orie[URB] + 2) % 3, (self.orie[DRB] + 1) % 3, (self.orie[DLB] + 2) % 3, (self.orie[ULB] + 1) % 3

    def b(self):
        self.cube[ULB], self.cube[URB], self.cube[DRB], self.cube[DLB] = self.cube[DLB], self.cube[ULB], self.cube[URB], self.cube[DRB]
        self.orie[ULB], self.orie[URB], self.orie[DRB], self.orie[DLB] = (self.orie[DLB] + 2) % 3, (self.orie[ULB] + 1) % 3, (self.orie[URB] + 2) % 3, (self.orie[DRB] + 1) % 3

    # Help function - moves one/multi step
    def moves(self, route: str):
        for c in route:
            if c == 'U': self.U()
            elif c == 'u': self.u()
            elif c == 'R': self.R()
            elif c == 'r': self.r()
            elif c == 'F': self.F()
            elif c == 'f': self.f()
            elif c == 'L': self.L()
            elif c == 'l': self.l()
            elif c == 'D': self.D()
            elif c == 'd': self.d()
            elif c == 'B': self.B()
            elif c == 'b': self.b()
            self.route += c
    
    # Get child states of current state (only need 6 rotation steps after improvement)
    def getChildStates(self):
        states = []
        legalMoves = "UuFfRr"
        for c in legalMoves:
            copy = self.copy()
            copy.moves(c)
            states.append(copy)
        return states

    # Get all possible child of current statte
    def getFullChild(self):
        states = []
        for c in "UuFfRrDdBbLl":
            copy = self.copy()
            copy.moves(c)
            states.append(copy)
        return states

    # Get the route to move the 7th cube (DLB cube) to the right place (Help to improvement search algorithms)
    # This method use Breadth - first search to implement
    def routeTransformToStandard(self): 
        stateQueue = Queue()
        visited = set()
        initState = deepcopy(self)
        stateQueue.put(initState)
        visited.add(initState)
        initState.route = ""
        if initState.isCorrectPositionCube(DLB):
            return initState.route
        while not stateQueue.empty():
            state = stateQueue.get() 
            for nextState in state.getFullChild():
                if nextState not in visited:
                    if nextState.isCorrectPositionCube(DLB):
                        return nextState.route
                    stateQueue.put(nextState)
                    visited.add(nextState) 
        return None

    # Move the 7th cube (DLB cube) to the right place
    def transformToStandard(self):
        route = self.routeTransformToStandard()
        follow = {'U':'d', 'u':'D', 'D':'u', 'd':'U', 'F':'b', 'f':'B', 'B':'f', 'b':'F', 'R':'l', 'r':'L', 'L':'r', 'l':'R'}
        moves = ""
        for move in route:
            moves += move
            moves += follow[move]
        self.moves(moves)
        return route

    # Random face
    def randomMove(self, n):
        S = "UuDdRrLlFfBb"
        route = ""
        for i in range(n):
            route += S[random.randrange(12)]
        self.moves(route)

    # Load state by input color
    # Input is a array of array color of each cube like the COLOR array 
    def loadColor(self, color):
        position = [0]*8
        orientation = [0]*8
        # Check each cube in input and compare it to goal COLOR to indentify it's goal possition
        for iCube in range(8):
            for iPos in range(8):
                if sorted(color[iCube]) == sorted(COLOR[iPos]):
                    position[iCube] = iPos

                    # Indentify cube's orientation
                    for orie in range(3):
                        if color[iCube][0] == COLOR[iPos][orie]:
                            # Check if cube's color is possible
                            if sorted(color[iCube]) == sorted(COLOR[iPos]):
                                orientation[iCube] = orie
                            else:
                                return False
        
        a = sum([o == 1 for o in orientation])
        b = sum([o == 2 for o in orientation])
        
        # Check if exactly 8 cube are correct and the their orientation is correct
        if sorted(position) == GOAL_POSITION and abs(a - b) % 3 == 0 :
            self.cube = position
            self.orie = orientation
            return True
        # Return false if input not valid
        return False

# Translate move table after transform to standard to before
translate = {
    'u' : { 'U' : 'U', 'd' : 'd', 'u' : 'u', 'D' : 'D', 'R' : 'F', 'l' : 'b', 'r' : 'f', 'L' : 'B', 'F' : 'L', 'b' : 'r', 'f' : 'l', 'B' : 'R' },
    'D' : { 'U' : 'U', 'd' : 'd', 'u' : 'u', 'D' : 'D', 'R' : 'F', 'l' : 'b', 'r' : 'f', 'L' : 'B', 'F' : 'L', 'b' : 'r', 'f' : 'l', 'B' : 'R' },
    'U' : { 'U' : 'U', 'd' : 'd', 'u' : 'u', 'D' : 'D', 'R' : 'B', 'l' : 'f', 'r' : 'b', 'L' : 'F', 'F' : 'R', 'b' : 'l', 'f' : 'r', 'B' : 'L' },
    'd' : { 'U' : 'U', 'd' : 'd', 'u' : 'u', 'D' : 'D', 'R' : 'B', 'l' : 'f', 'r' : 'b', 'L' : 'F', 'F' : 'R', 'b' : 'l', 'f' : 'r', 'B' : 'L' },
    'r' : { 'U' : 'B', 'd' : 'f', 'u' : 'b', 'D' : 'F', 'R' : 'R', 'l' : 'l', 'r' : 'r', 'L' : 'L', 'F' : 'U', 'b' : 'd', 'f' : 'u', 'B' : 'D' },
    'L' : { 'U' : 'B', 'd' : 'f', 'u' : 'b', 'D' : 'F', 'R' : 'R', 'l' : 'l', 'r' : 'r', 'L' : 'L', 'F' : 'U', 'b' : 'd', 'f' : 'u', 'B' : 'D' },
    'R' : { 'U' : 'F', 'd' : 'b', 'u' : 'f', 'D' : 'B', 'R' : 'R', 'l' : 'l', 'r' : 'r', 'L' : 'L', 'F' : 'D', 'b' : 'u', 'f' : 'd', 'B' : 'U' },
    'l' : { 'U' : 'F', 'd' : 'b', 'u' : 'f', 'D' : 'B', 'R' : 'R', 'l' : 'l', 'r' : 'r', 'L' : 'L', 'F' : 'D', 'b' : 'u', 'f' : 'd', 'B' : 'U' },
    'f' : { 'U' : 'R', 'd' : 'l', 'u' : 'r', 'D' : 'L', 'R' : 'D', 'l' : 'u', 'r' : 'd', 'L' : 'U', 'F' : 'F', 'b' : 'b', 'f' : 'f', 'B' : 'B' },
    'B' : { 'U' : 'R', 'd' : 'l', 'u' : 'r', 'D' : 'L', 'R' : 'D', 'l' : 'u', 'r' : 'd', 'L' : 'U', 'F' : 'F', 'b' : 'b', 'f' : 'f', 'B' : 'B' },
    'F' : { 'U' : 'L', 'd' : 'r', 'u' : 'l', 'D' : 'R', 'R' : 'U', 'l' : 'd', 'r' : 'u', 'L' : 'D', 'F' : 'F', 'b' : 'b', 'f' : 'f', 'B' : 'B' },
    'b' : { 'U' : 'L', 'd' : 'r', 'u' : 'l', 'D' : 'R', 'R' : 'U', 'l' : 'd', 'r' : 'u', 'L' : 'D', 'F' : 'F', 'b' : 'b', 'f' : 'f', 'B' : 'B' },
}

# Translate moves after transform to standard to before
def translateMove(tranform: str, moves: str):
    result = list(moves)
    for t in tranform[::-1]:
        for i in range(len(result)): 
            result[i] = translate[t][result[i]]
    return ''.join(result)