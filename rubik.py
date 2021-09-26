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

ULB, URB, URF, ULF, DLF, DRF, DRB, DLB = 0, 1, 2, 3, 4, 5, 6, 7
GOAL_POSITION = [ULB, URB, URF, ULF, DLF, DRF, DRB, DLB]
GOAL_ORIENTATION = [0]*8
COLOR = [['W', 'G', 'O'],['W', 'O', 'B'],['W', 'B', 'R'],['W', 'R', 'G'],['Y', 'G', 'R'],['Y', 'R', 'B'],['Y', 'B', 'O'],['Y', 'O', 'G']]

DB = json.load(open('db.json')) 

class Rubik:
    def __init__(self, p = GOAL_POSITION, o = GOAL_ORIENTATION):
        self.p = copy(p)
        self.o = copy(o)
        self.route = str()
        self.heuristic = 0

    def isGoalState(self):
        return self.p == GOAL_POSITION and self.o == GOAL_ORIENTATION
    
    def isGoalHeuristic(self, index):
        return self.p[index] == index and self.o[index] == 0

    def getHeuristic(self):
        if self.heuristic == 0: 
            # self.heuristic = sum([o != 0 for o in self.o]) + sum([i != self.p[i] for i in range(8)]) / 4 + len(self.route)
            self.heuristic = sum([DB[self.p[i]][str(self.o[i]*10+i)] for i in range(8)]) / 4 + len(self.route)
        return self.heuristic

    def __hash__(self) -> int:
        return hash((tuple(self.p), tuple(self.o)))
    
    def __eq__(self, o: object) -> bool:
        return self.p == o.p and self.o == o.o

    def __gt__(self, o):
        return self.getHeuristic() > o.getHeuristic()

    def __lt__(self, o):
        return self.getHeuristic() < o.getHeuristic()

    def __repr__(self):
        s = f"   {COLOR[self.p[0]][self.o[0]]}{COLOR[self.p[1]][self.o[1]]}\n"
        s += f"   {COLOR[self.p[3]][self.o[3]]}{COLOR[self.p[2]][self.o[2]]}\n"
        s += f"{COLOR[self.p[0]][self.o[0] - 2]}{COLOR[self.p[3]][self.o[3] - 1]} {COLOR[self.p[3]][self.o[3] - 2]}{COLOR[self.p[2]][self.o[2] - 1]} {COLOR[self.p[2]][self.o[2] - 2]}{COLOR[self.p[1]][self.o[1] - 1]} {COLOR[self.p[1]][self.o[1] - 2]}{COLOR[self.p[0]][self.o[0] - 1]}\n"
        s += f"{COLOR[self.p[7]][self.o[7] - 1]}{COLOR[self.p[4]][self.o[4] - 2]} {COLOR[self.p[4]][self.o[4] - 1]}{COLOR[self.p[5]][self.o[5] - 2]} {COLOR[self.p[5]][self.o[5] - 1]}{COLOR[self.p[6]][self.o[6] - 2]} {COLOR[self.p[6]][self.o[6] - 1]}{COLOR[self.p[7]][self.o[7] - 2]}\n"
        s += f"   {COLOR[self.p[4]][self.o[4]]}{COLOR[self.p[5]][self.o[5]]}\n"
        s += f"   {COLOR[self.p[7]][self.o[7]]}{COLOR[self.p[6]][self.o[6]]}"
        return s

    def U(self):
        self.p[ULB], self.p[URB], self.p[URF], self.p[ULF] = self.p[ULF], self.p[ULB], self.p[URB], self.p[URF]
        self.o[ULB], self.o[URB], self.o[URF], self.o[ULF] = self.o[ULF], self.o[ULB], self.o[URB], self.o[URF]

    def u(self):
        self.p[ULB], self.p[URB], self.p[URF], self.p[ULF] = self.p[URB], self.p[URF], self.p[ULF], self.p[ULB]
        self.o[ULB], self.o[URB], self.o[URF], self.o[ULF] = self.o[URB], self.o[URF], self.o[ULF], self.o[ULB]

    def D(self):
        self.p[DLB], self.p[DRB], self.p[DRF], self.p[DLF] = self.p[DRB], self.p[DRF], self.p[DLF], self.p[DLB]
        self.o[DLB], self.o[DRB], self.o[DRF], self.o[DLF] = self.o[DRB], self.o[DRF], self.o[DLF], self.o[DLB]

    def d(self):
        self.p[DLB], self.p[DRB], self.p[DRF], self.p[DLF] = self.p[DLF], self.p[DLB], self.p[DRB], self.p[DRF]
        self.o[DLB], self.o[DRB], self.o[DRF], self.o[DLF] = self.o[DLF], self.o[DLB], self.o[DRB], self.o[DRF]

    def R(self):
        self.p[URF], self.p[URB], self.p[DRB], self.p[DRF] = self.p[DRF], self.p[URF], self.p[URB], self.p[DRB]
        self.o[URF], self.o[URB], self.o[DRB], self.o[DRF] = (self.o[DRF] + 1) % 3, (self.o[URF] + 2) % 3, (self.o[URB] + 1) % 3, (self.o[DRB] + 2) % 3

    def r(self):
        self.p[URF], self.p[URB], self.p[DRB], self.p[DRF] = self.p[URB], self.p[DRB], self.p[DRF], self.p[URF]
        self.o[URF], self.o[URB], self.o[DRB], self.o[DRF] = (self.o[URB] + 1) % 3, (self.o[DRB] + 2) % 3, (self.o[DRF] + 1) % 3, (self.o[URF] + 2) % 3
    
    def L(self):
        self.p[ULF], self.p[ULB], self.p[DLB], self.p[DLF] = self.p[ULB], self.p[DLB], self.p[DLF], self.p[ULF]
        self.o[ULF], self.o[ULB], self.o[DLB], self.o[DLF] = (self.o[ULB] + 2) % 3, (self.o[DLB] + 1) % 3, (self.o[DLF] + 2) % 3, (self.o[ULF] + 1) % 3

    def l(self):
        self.p[ULF], self.p[ULB], self.p[DLB], self.p[DLF] = self.p[DLF], self.p[ULF], self.p[ULB], self.p[DLB]
        self.o[ULF], self.o[ULB], self.o[DLB], self.o[DLF] = (self.o[DLF] + 2) % 3, (self.o[ULF] + 1) % 3, (self.o[ULB] + 2) % 3, (self.o[DLB] + 1) % 3

    def F(self):
        self.p[ULF], self.p[URF], self.p[DRF], self.p[DLF] = self.p[DLF], self.p[ULF], self.p[URF], self.p[DRF]
        self.o[ULF], self.o[URF], self.o[DRF], self.o[DLF] = (self.o[DLF] + 1) % 3, (self.o[ULF] + 2) % 3, (self.o[URF] + 1) % 3, (self.o[DRF] + 2) % 3
    
    def f(self):
        self.p[ULF], self.p[URF], self.p[DRF], self.p[DLF] = self.p[URF], self.p[DRF], self.p[DLF], self.p[ULF]
        self.o[ULF], self.o[URF], self.o[DRF], self.o[DLF] = (self.o[URF] + 1) % 3, (self.o[DRF] + 2) % 3, (self.o[DLF] + 1) % 3, (self.o[ULF] + 2) % 3

    def B(self):
        self.p[ULB], self.p[URB], self.p[DRB], self.p[DLB] = self.p[URB], self.p[DRB], self.p[DLB], self.p[ULB]
        self.o[ULB], self.o[URB], self.o[DRB], self.o[DLB] = (self.o[URB] + 2) % 3, (self.o[DRB] + 1) % 3, (self.o[DLB] + 2) % 3, (self.o[ULB] + 1) % 3

    def b(self):
        self.p[ULB], self.p[URB], self.p[DRB], self.p[DLB] = self.p[DLB], self.p[ULB], self.p[URB], self.p[DRB]
        self.o[ULB], self.o[URB], self.o[DRB], self.o[DLB] = (self.o[DLB] + 2) % 3, (self.o[ULB] + 1) % 3, (self.o[URB] + 2) % 3, (self.o[DRB] + 1) % 3

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
    
    def printSolution(self, route: str):
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
            sleep(0.5)
            system('cls')
            print(self)
        
    
    def getChildStates(self):
        states = []
        for c in "UuDdRrLlFfBb":
            copy = self.copy()
            copy.moves(c)
            states.append(copy)
        return states

    def copy(self):
        o = Rubik()
        o.p = copy(self.p)
        o.o = copy(self.o)
        o.route = copy(self.route)
        return o

def Search(initState: Rubik, queue: Queue): 
    stateQueue = queue
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

def BFS(initState: Rubik, index): 
    stateQueue = Queue()
    visited = set()
    stateQueue.put(initState)
    visited.add(initState)
    initState.route = ""
    if initState.isGoalHeuristic(index):
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



def randomMove(n):
    S = "UuDdRrLlFfBb"
    s = ""
    for i in range(n):
        s += S[random.randrange(12)]
    return s

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
        goal, nodeCreated, nodeVisited = Search(init, PriorityQueue())
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

def run1(str):
    a = Rubik()
    a.moves(str)
    s = time()
    goal, nodeCreated, nodeVisited = Search(a, PriorityQueue())
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
    goal, nodeCreated, nodeVisited = Search(a, PriorityQueue())
    input("Enter to continue")
    a.printSolution(goal.route)
  
    

