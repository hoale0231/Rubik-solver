from time import time
from queue import Queue, PriorityQueue
import random
import json
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
                if nextState.isCorrectPositionCube(index):
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
        init.transformToStandard()
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
    init.transformToStandard()
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
    run1("DrUFDRLrfuDFu")
    runN(50)
    #run1("DL")