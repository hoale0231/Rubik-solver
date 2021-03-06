from time import time
from queue import Queue, PriorityQueue
import random
import json
from rubik import Rubik, PAIR_CUBES, translateMove

#import timeout library
from func_timeout import func_timeout, FunctionTimedOut

# Queue = BFS
# PriorityQueue = A_Star
# H1: mode = 0
# H2: mode = 1
# H3: mode = 2
# Improve: transform = True
# Not Improve: transform = False
def A_star(initState: Rubik, mode = 0, transform = True, queue = PriorityQueue): 
    Rubik.mode = mode
    routeTranform = ""
    if transform: 
        routeTranform = initState.transformToStandard()
    stateQueue = queue()
    visited = set()
    stateQueue.put(initState)
    visited.add(initState)
    initState.route = ""
    cnt = 0
    if initState.isGoalState():
        return initState, len(visited), cnt
    while not stateQueue.empty():
        state: Rubik = stateQueue.get() 
        for nextState in (state.getChildStates() if transform else state.getFullChild()):
            cnt += 1
            if nextState not in visited:
                if nextState.isGoalState():
                    if transform:
                         nextState.route = translateMove(routeTranform, nextState.route)
                    return nextState, cnt, len(visited)
                stateQueue.put(nextState)
                visited.add(nextState)
    return None

# Use to calc heuristic value H2 
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

# Use to calc heuristic value H3
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

# Create pattern database H2
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

# Create pattern database H3 
def createDB2():
    db = [{} for _ in range(7)]
    for c in PAIR_CUBES:
        print(c)
        db[c[0]+c[1]] = dict()
        for o1 in range(3):
            for p1 in range(8):
                for o2 in range(3):
                    for p2 in range(8):
                        if p1 != p2:
                            ps = [-1]*8
                            os = [0]*8
                            ps[c[0]] = p1
                            os[p1] = o1
                            ps[c[1]] = p2
                            os[p2] = o2
                            init = Rubik(ps, os)
                            new_state = BFS2(init, p1, p2)
                            db[c[0]+c[1]][o1*1000+p1*100+o2*10+p2] = len(new_state.route)
                            

    json.dump(db, open('dbPair.json', 'w'))

# Use to test algorithm
def randomMove(n):
    S = "UuDdRrLlFfBb"
    s = ""
    for i in range(n):
        s += S[random.randrange(12)]
    return s

# make a list of random testcase
randomlist= list()
for i in range(20):
    shuff = randomMove(50)
    randomlist.append(shuff)
print(randomlist)

# Randomly run N times
def runN(n, mode, transform, queue):
    maxStep = 0
    caseMax = ""
    for i in range(n):
        init = Rubik()
        shuffle = randomlist[i]

        print("===========================")
        print("N move:", i)
        print(shuffle)
        init.moves(shuffle)

        s = time()
        # set timeout 300s = 5 minute
        try:
            goal, nodeCreated, nodeVisited = func_timeout(300, A_star, args=(init, mode, transform, queue))
        except FunctionTimedOut:
            continue
        # goal, nodeCreated, nodeVisited = A_star(init, mode, transform, queue)
        e = time()

        if len(goal.route) > maxStep:
            maxStep = len(goal.route)
            caseMax = shuffle
        # memUsed = psutil.Process().memory_info().rss
        print("Time:", e - s)
        print("Steps:", len(goal.route))
        print("Node visited", nodeVisited)
        print("Node created:", nodeCreated)
        # print("Memory: "+ str(memUsed/(1024*1024))+ " MB")
        print(goal.route)

    print("Max step:", maxStep)
    print("Case:", caseMax)

# Try once with route designation
def run1(str, mode, transform):
    init = Rubik()
    init.moves(str)
    s = time()
    goal, nodeCreated, nodeVisited = A_star(init, mode, transform)
    print(goal.getHeuristic())
    e = time()
    print(e-s)
    print("Steps:", len(goal.route))
    print("Node visited:", nodeVisited)
    print("Node created:", nodeCreated)
    print(goal.route)
    #init.printEachStep(goal.route)

if __name__ == '__main__':
      #A* + h1 + improved
    runN(20, 0, True, PriorityQueue)
    print("end 1 test")

    #A* + h1 +  not improved
    runN(20, 0, False, PriorityQueue)
    print("end 2 test")

    #A* + h2 + improved
    runN(20, 1, True, PriorityQueue)
    print("end 3 test")

    #A* + h2 + not improved
    runN(20, 1, False, PriorityQueue)
    print("end 4 test")

    #A* + h3 + improved
    runN(20, 2, True, PriorityQueue)
    print("end 5 test")

    #A* + h3 + not improved
    runN(20, 2, False, PriorityQueue)
    print("end 6 test")

    #BFS + improved
    runN(20, 0, True, Queue)
    print("end all test")