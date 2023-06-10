import math
import random

'''
Author: Sai Manogyana T
G#    : G01377339
'''

'''
Implementation Details:
    Variables:
    pairs
        matrix
        cols = [5,7]
        rows = N 
        phi (frozen factor)
        temperature 
        
    Functions:
        generate_initial_matrix()
        calcFrozenFactor()
'''

pairs = set(((0,0), (0,1), (1,0), (1,1)))
totalIters = []
stopC = []

def generateInitialState(cols, rows = 4):
    '''columns = k 
    k = [5,7]'''
    
    matrix = []
    for i in range(rows):
        t = []
        for j in range(cols):
            t.append(random.randint(0, 1))
        matrix.append(t)
    return matrix


def printState(matrix, cols = 5, rows = 4):
    for i in range(rows):
        print(matrix[i])


def setTemp(currTemp):
    return 0.99 * currTemp
    

def calcFrozenFactor(k):
    '''
        Φ = (v power t) × (k!)/(k-t!)t!
        v = 2
        t = 2
        so, v power t is always 4
    '''
    t = 2
    phi = math.factorial(k) // (math.factorial(k-t) * math.factorial(t))
    return 4 * phi 


def countMissingPairs(matrix, cols, rows = 4):
    ''' 
        Returns the number of missing pairs
    '''
    count = 0
    results = []
    for i in range(cols):
        for j in range(i + 1, cols):
            pairsFound = set()
            
            for k in range(rows):
                pairsFound.add((matrix[k][i], matrix[k][j]))
            
            if pairsFound == pairs:         #might want to remove result array as it is serving no purpose.
                results.append(True)
            else:
                results.append(False)
                count += len(pairs.difference(pairsFound))
    return count
                

def stopCriteria(missingPairs, temp_decr, phi, curr_temp, f_temp):
    if missingPairs == 0:
        return 1
    elif curr_temp <= f_temp:
        return 2
    elif temp_decr >= phi:
        return 3


def getNeighbours(currState, cols, rows = 4):
    possibleStates = []
    randCol = random.randint(0, cols - 1)

    for i in range(rows):
        possibleStates.append({'cost':float('inf'), 'state': [currState[i].copy() for i in range(rows)]})
    
        if (possibleStates[i]['state'][i][randCol]):
            possibleStates[i]['state'][i][randCol] = 0
        else:
            possibleStates[i]['state'][i][randCol] = 1
    return possibleStates


def getBestState(dict_of_states, k, N = 4):
    minMissingPairs = float("inf")
    bestState = []
    for next_state in dict_of_states:
        next_state['cost'] = countMissingPairs(next_state['state'], k, N)
        if minMissingPairs > next_state['cost']:
            minMissingPairs = next_state['cost']
            bestState = next_state['state']
    '''print("POSSIBLE STATES:")
    for next_state in dict_of_states:
        print('Missing:', next_state['cost'])
        printState(next_state['state'])
        print()'''
    return minMissingPairs, bestState
        
        
def SA(initState, k, N = 4):
    currTemp = k
    finalTemp = 0.1
    iters = 0               #to maintain temperature decrements since last best pairs was found.
    totalRuns = 0

    currState = initState
    missingPairs = countMissingPairs(currState, k, N)
    bestSoFar = currState
    leastMissingPairs = missingPairs
    phi = calcFrozenFactor(k)

    while missingPairs != 0 and currTemp > finalTemp and iters < phi:
        totalRuns += 1
        iters += 1
        nextStates = getNeighbours(currState, k, N)
        missingPairsNext, bestState = getBestState(nextStates, k, N)
        
        costD = missingPairs - missingPairsNext
        
        if costD > 0:
            currState = bestState
            missingPairs = missingPairsNext
            if missingPairs < leastMissingPairs:
                leastMissingPairs = missingPairs
                bestSoFar = currState
                iters = 0
        else:
            if random.uniform(0, 1) < math.exp(-costD / currTemp):
                currState = bestState
                missingPairs = missingPairsNext
                
        currTemp = setTemp(currTemp)
    
    #print("TOTAL ITERATIONS: ", totalRuns)
    #totalIters.append(totalRuns)
    #stopC.append(stopCriteria(missingPairs, iters, phi, currTemp, finalTemp))
    return stopCriteria(missingPairs, iters, phi, currTemp, finalTemp), bestSoFar, costD, leastMissingPairs


d = {1:'Solution', 2:'Final Temperature', 3: 'Frozen Factor'}


start = 4
end = 7
kStart = 5
kEnd = 8
runs = 30
def main():
    for N in range(start, end):
        for k in range(kStart, kEnd):
            for i in range(runs):
                print("Run #", i)
                initState = generateInitialState(k, N)
                soln = SA(initState, k, N)
                #print(soln)
                if (soln[0] == 1):
                    print("SOLUTION FOUND!")
                    printState(soln[1], k, N)
                else:
                    print("Solution not found :(")
                    if (soln[0] == 2):
                        print("Final temperature achieved")
                    elif (soln[0] == 3):
                        print("Frozen factor reached")
                print()

if __name__ == "__main__":
    main()





    
