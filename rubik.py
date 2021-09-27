from copy import copy
from time import sleep, time
from queue import Queue, PriorityQueue
import random
import json
from os import system

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
# Color corresponding to each cubie
COLOR = [['W', 'G', 'O'],['W', 'O', 'B'],['W', 'B', 'R'],['W', 'R', 'G'],['Y', 'G', 'R'],['Y', 'R', 'B'],['Y', 'B', 'O'],['Y', 'O', 'G']]

# Pattern database, support heuristic function
DB = json.load(open('db.json')) 

class Rubik:
    def __init__(self, p = GOAL_POSITION, o = GOAL_ORIENTATION):
        self.cube = copy(p)     # Store cubie in order of position from 0 -> 7 according to the above convention
        self.orie = copy(o)     # Store orientation of cubie in order of position from 0 -> 7 according to the above convention
        self.route = str()      # Store moved steps
        self.heuristic = 0      # Store heuristic value

    # Copy constructor
    def copy(self):
        o = Rubik()
        o.cube = copy(self.cube)
        o.orie = copy(self.orie)
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
            # self.heuristic = sum([o != 0 for o in self.o]) + sum([i != self.p[i] for i in range(8)]) / 4 + len(self.route)
            self.heuristic = sum([DB[self.cube[i]][str(self.orie[i]*10+i)] for i in range(8)]) / 4 + len(self.route)
        return self.heuristic

    # Make the position object hashable, i.e. addable to set()
    def __hash__(self):
        return hash((tuple(self.cube), tuple(self.orie)))
    
    # Make the state object comparable, it helps set(), PriorityQueue() to work correctly
    def __eq__(self, o: object) -> bool:
        return self.cube == o.p and self.orie == o.o
    def __gt__(self, o):
        return self.getHeuristic() > o.getHeuristic()
    def __lt__(self, o):
        return self.getHeuristic() < o.getHeuristic()

    # Print current state
    def __repr__(self):
        s = f"   {COLOR[self.cube[0]][self.orie[0]]}{COLOR[self.cube[1]][self.orie[1]]}\n"
        s += f"   {COLOR[self.cube[3]][self.orie[3]]}{COLOR[self.cube[2]][self.orie[2]]}\n"
        s += f"{COLOR[self.cube[0]][self.orie[0] - 2]}{COLOR[self.cube[3]][self.orie[3] - 1]} {COLOR[self.cube[3]][self.orie[3] - 2]}{COLOR[self.cube[2]][self.orie[2] - 1]} {COLOR[self.cube[2]][self.orie[2] - 2]}{COLOR[self.cube[1]][self.orie[1] - 1]} {COLOR[self.cube[1]][self.orie[1] - 2]}{COLOR[self.cube[0]][self.orie[0] - 1]}\n"
        s += f"{COLOR[self.cube[7]][self.orie[7] - 1]}{COLOR[self.cube[4]][self.orie[4] - 2]} {COLOR[self.cube[4]][self.orie[4] - 1]}{COLOR[self.cube[5]][self.orie[5] - 2]} {COLOR[self.cube[5]][self.orie[5] - 1]}{COLOR[self.cube[6]][self.orie[6] - 2]} {COLOR[self.cube[6]][self.orie[6] - 1]}{COLOR[self.cube[7]][self.orie[7] - 2]}\n"
        s += f"   {COLOR[self.cube[4]][self.orie[4]]}{COLOR[self.cube[5]][self.orie[5]]}\n"
        s += f"   {COLOR[self.cube[7]][self.orie[7]]}{COLOR[self.cube[6]][self.orie[6]]}"
        return s

    # Legal moves: U, u ~ u', D, d, R, r, L, l, F, f, B, b
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

    # Help function - moves multi step
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
    
    # Get all child state of current state
    def getChildStates(self):
        states = []
        for c in "UuDdRrLlFfBb":
            copy = self.copy()
            copy.moves(c)
            states.append(copy)
        return states

    # Move and print each step
    def printEachStep(self, route: str):
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
            print(self)

def A_star(initState: Rubik): 
    stateQueue = PriorityQueue()
    visited = set()
    stateQueue.put(initState)
    visited.add(initState)
    initState.route = ""
    cnt = 0
    if initState.isGoalState():
        return initState, len(visited), cnt
    while not stateQueue.empty():
        state: Rubik = stateQueue.get() 
        for nextState in state.getChildStates():
            cnt += 1
            if nextState not in visited:
                if nextState.isGoalState():
                    return nextState, cnt, len(visited)
                stateQueue.put(nextState)
                visited.add(nextState) 
    return None

# Use to calc heuristic value
def BFS(initState: Rubik, index): 
    stateQueue = Queue()
    visited = set()
    stateQueue.put(initState)
    visited.add(initState)
    initState.route = ""
    if initState.isCorrectPositionCube(index):
        return initState
    while not stateQueue.empty():
        state = stateQueue.get() 
        for nextState in state.getChildStates():
            if nextState not in visited:
                if nextState.isGoalHeuristic(index):
                    return nextState
                stateQueue.put(nextState)
                visited.add(nextState) 
    return None

# Create pattern database
def creatDB():
    db = []
    for i in range(8):
        db.append(dict())
        for o in range(3):
            for p in range(8):
                init = Rubik()
                ps = [-1]*8
                os = [0]*8
                ps[p] = i
                os[p] = o
                init.init(ps, os)
                db[i][o * 10 + p] = len(BFS(init, i).route)
    json.dump(db, open('db.json', 'w'))

# Use to test algorithm
def randomMove(n):
    S = "UuDdRrLlFfBb"
    s = ""
    for i in range(n):
        s += S[random.randrange(12)]
    return s

# Randomly run N times
def runN(n):
    maxStep = 0
    caseMax = ""
    for i in range(n):
        init = Rubik()
        shuffle = randomMove(i)

        print("===========================")
        print("N move:", i)
        print(shuffle)
        init.moves(shuffle)
        
        s = time()
        goal, nodeCreated, nodeVisited = A_star(init, PriorityQueue())
        e = time()
       
        if len(goal.route) > maxStep:
            maxStep = len(goal.route)
            caseMax = shuffle

        print("Time:", e - s)
        print("Steps:", len(goal.route))
        print("Node visited", nodeVisited)
        print("Node created:", nodeCreated)
        print(goal.route)
        
    print("Max step:", maxStep)
    print("Case:", caseMax)

# Try once with route designation
def run1(str):
    a = Rubik()
    a.moves(str)
    s = time()
    goal, nodeCreated, nodeVisited = A_star(a, PriorityQueue())
    e = time()
    print(e-s)
    print("Steps:", len(goal.route))
    print("Node visited:", nodeVisited)
    print("Node created:", nodeCreated)
    print(goal.route)


if __name__ == '__main__':
    a = Rubik()
    a.moves("uLrlUFbbDudrl")
    print(a)
    goal, nodeCreated, nodeVisited = A_star(a, PriorityQueue())
    input("Enter to continue")
    a.printEachStep(goal.route)
  
    

