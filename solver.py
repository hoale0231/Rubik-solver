from time import time
from queue import Queue, PriorityQueue
import random
import json
#from rubik import Rubik
from rubik import Rubik  
# Pattern database, support heuristic function


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
        for nextState in state.getFullChild():
            cnt += 1
            if nextState not in visited:
                if nextState.isGoalState():
                    return nextState.route, cnt, len(visited)
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
                if nextState.isCorrectPositionCube(index):
                    return nextState
                stateQueue.put(nextState)
                visited.add(nextState) 
    return None

def BFS2(initState: Rubik, index1, index2): 
    stateQueue = Queue()
    visited = set()
    stateQueue.put(initState)
    visited.add(initState)
    initState.route = ""
    if initState.isCorrectPositionCube(index1) and initState.isCorrectPositionCube(index2):
        return initState
    while not stateQueue.empty():
        state = stateQueue.get() 
        for nextState in state.getFullChild():
            if nextState not in visited:
                if nextState.isCorrectPositionCube(index1) and nextState.isCorrectPositionCube(index2):
                    return nextState
                stateQueue.put(nextState)
                visited.add(nextState) 
    return None

# Create pattern database
def creatDB1():
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
    json.dump(db, open('db2.json', 'w'))


def createDB2():
    db = [dict()]*7
    for c in [(0, 1), (2, 3), (4, 5), (6, 7), (0, 4), (1, 5), (2, 6), (3, 7), (0, 3), (1, 2), (4, 7), (5, 6)]:
        print(c)
        db[c[0]][c[1]] = {}
        for o1 in range(3):
            for p1 in range(8):
                for o2 in range(3):
                    for p2 in range(8):
                        if p1 != p2:
                            ps = [-1]*8
                            os = [0]*8
                            ps[p1] = c[0]
                            os[p1] = o1
                            ps[p2] = c[1]
                            os[p2] = o2
                            init = Rubik(ps, os)
                            new_state = BFS2(init, c[0], c[1])
                            db[c[0]][c[1]][o1*1000+p1*100+o2*10+p2] = len(new_state.route)
                            
    json.dump(db, open('dbPair.json', 'w'))
    
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
        #init.transformToStandard()
        s = time()
        goal, nodeCreated, nodeVisited = A_star(init)
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
    init = Rubik()
    init.moves(str)
    #init.transformToStandard()
    s = time()
    goal, nodeCreated, nodeVisited = A_star(init)
    e = time()
    print(e-s)
    print("Steps:", len(goal.route))
    print("Node visited:", nodeVisited)
    print("Node created:", nodeCreated)
    print(goal.route)
    init.printEachStep(goal.route)


if __name__ == '__main__':
    #run1("DrUFDRLrfuDFu")
    #runN(50)
    createDB2()