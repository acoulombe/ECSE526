import csv_util
from collections import Counter
import copy
import math
import random

# Agent Parameters
alpha = None
gamma = None
epsilon = None
theta = [1, 1, 1, 1, 1]

def getWeights(filename):
    """Get the prior computed weights from the csv file storage

    Parameters
    --------
        filename : str
            name of csv to read
    """
    global theta
    theta = csv_util.read_csv(filename)

def saveWeights(filename):
    """Save the computed weights to a csv file for later use

    Parameters
    --------
        filename : str
            name of csv to write
    """
    global theta
    csv_util.write_csv(filename, theta)

def convertEnv(env):
    """Convert ALE screen from 1D array to 2D array

    Parameters
    --------
        env : ndarray 1xn
            1D array of the ALE screen where n is 210*160
    Returns
    --------
        list(list(int))
            2D array representation of the game screen
    """
    env_2d = []
    for i in range(210):
        env_2d.append(env[i*160:(i+1)*160].tolist())
    return env_2d

# Memory for game
env_model = [
    [6, 1, 1, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 1, 1, 6],
    [6, 2, 6, 6, 1, 6, 1, 6, 6, 6, 6, 6, 6, 1, 6, 1, 6, 6, 2, 6],
    [6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6],
    [6, 6, 1, 6, 1, 6, 6, 1, 6, 6, 6, 6, 1, 6, 6, 1, 6, 1, 6, 6],
    [0, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 0],
    [6, 6, 1, 6, 6, 6, 6, 1, 6, 6, 6, 6, 1, 6, 6, 6, 6, 1, 6, 6],
    [0, 6, 1, 1, 1, 1, 1, 1, 6, 0, 0, 6, 1, 1, 1, 1, 1, 1, 6, 0],
    [6, 6, 1, 6, 6, 6, 6, 1, 6, 6, 6, 6, 1, 6, 6, 6, 6, 1, 6, 6],
    [0, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 0],
    [6, 6, 1, 6, 1, 6, 1, 6, 1, 6, 6, 1, 6, 1, 6, 1, 6, 1, 6, 6],
    [6, 1, 1, 1, 1, 6, 1, 6, 1, 1, 1, 1, 6, 1, 6, 1, 1, 1, 1, 6],
    [6, 1, 6, 6, 1, 6, 1, 1, 1, 6, 6, 1, 1, 1, 6, 1, 6, 6, 1, 6],
    [6, 2, 6, 6, 1, 6, 6, 6, 1, 6, 6, 1, 6, 6, 6, 1, 6, 6, 2, 6],
    [6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6]
]

blinky_pos = [0, 0, 1]      # Red Ghost last position
pinky_pos = [0, 0, 1]       # Pink Ghost last position
clyde_pos = [0, 0, 1]       # Orange Ghost last position
inky_pos =  [0, 0, 1]       # Blue Ghost last position
pacman_pos = [0, 0]         # Pacman last position

def getState(env):
    """Generates the state from the environment
    In the case of Ms Pacman, the game screen

    Parameters
    --------
        env : list(list(int))
            2D array of pixel values of the environment

    Returns
    --------
        list(list(int))
            2D array representing the state of the game
    """
    global env_model
    global blinky_pos
    global pinky_pos
    global clyde_pos
    global inky_pos
    global pacman_pos

    grid = copy.deepcopy(env_model)
    for i in range(14):
        for j in range(20):
            pixels = []
            for k in range(12):
                for l in range(8):
                    pixels.append(env[i*12+k+2][j*8+l])
            histogram = Counter(pixels)
            color_count = 0
            color_key = None
            for key in histogram:
                # if the tile is empty
                if(key == 144):
                    continue
                if(color_count < histogram[key]):
                    color_count = histogram[key]
                    color_key = key
            # Change dominant color to tile state
            if(color_key is None):          # No majority color
                color_key = 0
            elif(color_key == 74):          # If pink-ish is dominant in tile
                if(color_count == 8):       # Corresponds to a dot, 4x2 pixels of value 74
                    color_key = 1
                elif(color_count == 28):    # Corresponds to a capsule, 4x7 pixels of value 74
                    color_key = 2
                else:                       # Corresponds to a wall
                    color_key = 6
            elif(color_key == 42):          # If yellow is dominant in tile
                pacman_pos.append([i,j])
                continue
            # Corresponds to active ghosts
            elif(color_key == 70):
                blinky_pos.append([i, j, 1])
                continue
            elif(color_key == 184):
                clyde_pos.append([i, j, 1])
                continue
            elif(color_key == 38):
                inky_pos.append([i, j, 1])
                continue
            elif(color_key == 88):
                pinky_pos.append([i, j, 1])
                continue
            elif(color_key == 150):
                if(abs(i-blinky_pos[0])+abs(j-blinky_pos[1]) < 2):
                    blinky_pos.append([i, j, 0])
                elif(abs(i-clyde_pos[0])+abs(j-clyde_pos[1]) < 2):
                    clyde_pos.append([i, j, 0])
                elif(abs(i-inky_pos[0])+abs(j-inky_pos[1]) < 2):
                    inky_pos.append([i, j, 0])
                elif(abs(i-pinky_pos[0])+abs(j-pinky_pos[1]) < 2):
                    pinky_pos.append([i, j, 0])                
                continue

            grid[i][j] = color_key
    
    # Update Pacman positions in memory
    for i in range(2, len(pacman_pos)):
        if(pacman_pos[0] != pacman_pos[i][0] or pacman_pos[1] != pacman_pos[i][1]):
            pacman_pos = [pacman_pos[i][0], pacman_pos[i][1]]
            break
    pacman_pos = [pacman_pos[0], pacman_pos[1]]
    # Update the Ghosts positions in memory
    dist = float('Inf')
    idx = None
    for i in range(3, len(blinky_pos)):
        dx = abs(blinky_pos[i][0]-pacman_pos[0])
        dy = abs(blinky_pos[i][1]-pacman_pos[1])
        delta = 0
        if dx != 0 and dy != 0:
            delta = dx+dy-1
        else:
            delta = dx+dy
        if dist > delta:
            dist = delta
            idx = i
    if(idx is not None):
        blinky_pos = [blinky_pos[idx][0], blinky_pos[idx][1], blinky_pos[idx][2]]
    
    dist = float('Inf')
    idx = None
    for i in range(3, len(inky_pos)):
        dx = abs(inky_pos[i][0]-pacman_pos[0])
        dy = abs(inky_pos[i][1]-pacman_pos[1])
        delta = 0
        if dx != 0 and dy != 0:
            delta = dx+dy-1
        else:
            delta = dx+dy
        if dist > delta:
            dist = delta
            idx = i
    if(idx is not None):
        inky_pos = [inky_pos[idx][0], inky_pos[idx][1], inky_pos[idx][2]]
    
    dist = float('Inf')
    idx = None
    for i in range(3, len(pinky_pos)):
        dx = abs(pinky_pos[i][0]-pacman_pos[0])
        dy = abs(pinky_pos[i][1]-pacman_pos[1])
        delta = 0
        if dx != 0 and dy != 0:
            delta = dx+dy-1
        else:
            delta = dx+dy
        if dist > delta:
            dist = delta
            idx = i
    if(idx is not None):
        pinky_pos = [pinky_pos[idx][0], pinky_pos[idx][1], pinky_pos[idx][2]]

    dist = float('Inf')
    idx = None
    for i in range(3, len(clyde_pos)):
        dx = abs(clyde_pos[i][0]-pacman_pos[0])
        dy = abs(clyde_pos[i][1]-pacman_pos[1])
        delta = 0
        if dx != 0 and dy != 0:
            delta = dx+dy-1
        else:
            delta = dx+dy
        if dist > delta:
            dist = delta
            idx = i
    if(idx is not None):
        clyde_pos = [clyde_pos[idx][0], clyde_pos[idx][1], clyde_pos[idx][2]] 

    # Place last known locations of the entities in the state
    grid[pacman_pos[0]][pacman_pos[1]] = 3
    grid[blinky_pos[0]][blinky_pos[1]] = 4 + blinky_pos[2]
    grid[inky_pos[0]][inky_pos[1]] = 4 + inky_pos[2]
    grid[pinky_pos[0]][pinky_pos[1]] = 4 + pinky_pos[2]
    grid[clyde_pos[0]][clyde_pos[1]] = 4 + clyde_pos[2]

    return grid

# Q-learning constants
prev_state = None
prev_action = None
prev_reward = None

def Q_learn(state, reward):
    """Q learning algorithm using temporal difference

    Parameters
    --------
        state : list(list(int))
            2D array representing the state of the game
        reward : int
            received reward
    
    Returns
    -------
        int
            number representing the next action to perform
    """
    global prev_action
    global prev_reward
    global prev_state
    global alpha
    global gamma
    global theta
    global last_moves

    if isDead():
        reward -= 100

    if prev_state is not None:
        Q = Q_val(prev_state, prev_action)

        # Update last moves
        try: 
            if(prev_action == 4 and prev_state[pacman_pos[0]][(pacman_pos[1]-1)%(len(prev_state[0])+1)] != 6):    # West
                last_moves = [
                    [0] + last_moves[0][:-1],
                    [0] + last_moves[1][:-1],
                    [0] + last_moves[2][:-1]
                ]
            elif(prev_action == 2 and prev_state[(pacman_pos[0]-1)%(len(prev_state[0])+1)][pacman_pos[1]] != 6):  # North
                last_moves = [
                    [0, 0, 0],
                    last_moves[0],
                    last_moves[1]
                ] 
            elif(prev_action == 3 and prev_state[pacman_pos[0]][pacman_pos[1]+1] != 6):  # East
                last_moves = [
                    last_moves[0][1:] + [0],
                    last_moves[1][1:] + [0],
                    last_moves[2][1:] + [0]
                ]
            elif(prev_action == 5 and prev_state[pacman_pos[0]+1][pacman_pos[1]] != 6):  # South
                last_moves = [
                    last_moves[1],
                    last_moves[2],
                    [0, 0, 0]
                ] 
            else:
                prev_state[pacman_pos[0]][pacman_pos[1]] = 3
        except IndexError:
            # Going through tunnel is a legal prev_action
            if(pacman_pos[1] == 0 and prev_action == 4):
                last_moves = [
                    [0] + last_moves[0][:-1],
                    [0] + last_moves[1][:-1],
                    [0] + last_moves[2][:-1]
                ]
            elif(pacman_pos[1] == len(prev_state[0])-1 and prev_action == 3):
                last_moves = [
                    last_moves[0][1:] + [0],
                    last_moves[1][1:] + [0],
                    last_moves[2][1:] + [0]
                ]
        last_moves[1][1] += 1 

        pi, Qmax = maxQ(state)
        food_dist, num_food = findFoodFeatures(state)
        scared_dist, active_dist = findGhostFeatures()
        oscillation = findOscillation(last_moves)

        if(food_dist != 0):
            theta[0] = theta[0] + alpha*(reward + gamma*Qmax - Q)/food_dist
        else:
            theta[0] = theta[0] + alpha*(reward + gamma*Qmax - Q)
        
        if(scared_dist != 0):
            theta[1] = theta[1] + alpha*(reward + gamma*Qmax - Q)/scared_dist
        else:
            theta[1] = theta[1] + alpha*(reward + gamma*Qmax - Q)
        if(active_dist != 0):
            theta[2] = theta[2] + alpha*(reward + gamma*Qmax - Q)/active_dist
        else:
            theta[2] = theta[2] + alpha*(reward + gamma*Qmax - Q)
        if(oscillation != 0):
            theta[3] = theta[3] + alpha*(reward + gamma*Qmax - Q)/oscillation
        else:
            theta[3] = theta[3] + alpha*(reward + gamma*Qmax - Q)
        if(num_food != 0):
            theta[4] = theta[4] + alpha*(reward + gamma*Qmax - Q)/num_food
        else:
            theta[4] = theta[4] + alpha*(reward + gamma*Qmax - Q)

    prev_state = state
    prev_action = explore(state)
    prev_reward = reward
    return prev_action

def Q_val(state, action):
    """Compute the expected Q value of a state action pair

    Parameters
    --------
        state : list(list(int))
            2D array representing the state of the game
    
    Returns
    --------
        float
            Q value
    """
    global blinky_pos
    global pinky_pos
    global clyde_pos
    global inky_pos
    global pacman_pos
    global last_moves

    next_state = copy.deepcopy(state)
    past_moves = copy.deepcopy(last_moves)
    next_state[pacman_pos[0]][pacman_pos[1]] = 0
    tmp = pacman_pos
    try: 
        if(action == 4 and next_state[pacman_pos[0]][(pacman_pos[1]-1)%(len(next_state[0])+1)] != 6):    # West
            next_state[pacman_pos[0]][pacman_pos[1]-1] = 3
            pacman_pos = [pacman_pos[0], pacman_pos[1]-1]
            past_moves = [
                [0] + last_moves[0][:-1],
                [0] + last_moves[1][:-1],
                [0] + last_moves[2][:-1]
            ]
        elif(action == 2 and next_state[(pacman_pos[0]-1)%(len(next_state[0])+1)][pacman_pos[1]] != 6):  # North
            next_state[pacman_pos[0]-1][pacman_pos[1]] = 3
            pacman_pos = [pacman_pos[0]-1, pacman_pos[1]]
            past_moves = [
                [0, 0, 0],
                last_moves[0],
                last_moves[1]
            ] 
        elif(action == 3 and next_state[pacman_pos[0]][pacman_pos[1]+1] != 6):  # East
            next_state[pacman_pos[0]][pacman_pos[1]+1] = 3
            pacman_pos = [pacman_pos[0], pacman_pos[1]+1]
            past_moves = [
                last_moves[0][1:] + [0],
                last_moves[1][1:] + [0],
                last_moves[2][1:] + [0]
            ]
        elif(action == 5 and next_state[pacman_pos[0]+1][pacman_pos[1]] != 6):  # South
            next_state[pacman_pos[0]+1][pacman_pos[1]] = 3
            pacman_pos = [pacman_pos[0]+1, pacman_pos[1]]
            past_moves = [
                last_moves[1],
                last_moves[2],
                [0, 0, 0]
            ] 
        else:
            next_state[pacman_pos[0]][pacman_pos[1]] = 3
    except IndexError:
        # Going through tunnel is a legal action
        if(pacman_pos[1] == 0 and action == 4):
            next_state[pacman_pos[0]][len(next_state[0])-1] = 3
            past_moves = [
                [0] + last_moves[0][:-1],
                [0] + last_moves[1][:-1],
                [0] + last_moves[2][:-1]
            ]
        elif(pacman_pos[1] == len(next_state[0])-1 and action == 3):
            next_state[pacman_pos[0]+1][0] = 3
            past_moves = [
                last_moves[0][1:] + [0],
                last_moves[1][1:] + [0],
                last_moves[2][1:] + [0]
            ]
        else:
            next_state[pacman_pos[0]][pacman_pos[1]] = 3
    
    past_moves[1][1] += 1

    dist_food, num_food = findFoodFeatures(next_state)
    scared_dist, active_dist = findGhostFeatures()
    oscillation = findOscillation(past_moves)
    pacman_pos = tmp

    Q = 0
    try:
        Q += theta[0]/dist_food
    except ZeroDivisionError:
        Q += theta[0]
    try:
        Q += theta[1]/scared_dist
    except ZeroDivisionError:
        Q += theta[1]
    try:
        Q += theta[2]/active_dist
    except ZeroDivisionError:
        Q += theta[2]
    try:
        Q += theta[3]/oscillation
    except ZeroDivisionError:
        Q += theta[3]
    try:
        Q += theta[4]/num_food
    except ZeroDivisionError:
        Q += theta[4]

    return Q

def maxQ(state):
    """Find maximum Q value from Q table when performing actions in state

    Parameters
    --------
        state : list(list(int))
            2D array representing the state of the game
    
    Returns
    --------
        int
            action that has highest Q value
        float
            max Q value attainable
    """
    actions = [4, 2, 3, 5]  # [W, N, E, S]
    Qmax = -float('Inf')
    pi = 0
    for a in actions:
        Q = Q_val(state, a)
        if(Q > Qmax):
            try:
                if(
                    (a == 4 and state[pacman_pos[0]][pacman_pos[1]-1] == 6) or  # West
                    (a == 2 and state[pacman_pos[0]-1][pacman_pos[1]] == 6) or  # North
                    (a == 3 and state[pacman_pos[0]][pacman_pos[1]+1] == 6) or  # East
                    (a == 5 and state[pacman_pos[0]+1][pacman_pos[1]] == 6)     # South
                ):
                    continue    # Reject Movement in walls
                pi = a
                Qmax = Q
            except IndexError:
                continue
    return pi, Qmax

def explore(state):
    """Function to control the exploration of the agent
    using the Epsilon-Greedy Policy
    
    Parameters
    --------
        state : list(list(int))
            2D array representing the state of the game
    
    Returns
    --------
        int
            action to be performed by the agent
    """
    global epsilon

    actions = [4, 2, 3, 5]  # [W, N, E, S]
    # Randomly Select move
    if(random.random() < epsilon):
        return actions[random.randint(0,len(actions)-1)]
    # Select best move
    else:
        pi, Qmax = maxQ(state)
        return pi

def findFoodFeatures(grid):
    """Find the features distance to the nearest
    food position from Ms. Pacman

    Parameters
    --------
        grid : list(list(int))
            grid representation of the Atari screen
    
    Returns
    --------
        int
            sum of distances to all food from Ms. Pacman
        int
            number of food dot on the grid
    """
    global pacman_pos
    
    # dist = float("Inf")
    dist = 0
    num_food = 0
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if grid[i][j] == 1:
                num_food +=1
                dx = abs(pacman_pos[0]-i)
                dy = abs(pacman_pos[1]-j)
                delta = 0
                if dx != 0 and dy != 0:
                    delta = dx+dy-1
                else:
                    delta = dx+dy
                # if(delta < dist):
                #     dist = delta
                dist += delta
    return dist, num_food

def findGhostFeatures():
    """Find the features related to the Ghosts, namely the distance
    to the closest scared ghost and active ghost

    Returns
    --------
        int
            Sum of distance to all scared ghost
        int
            Sum of distance to all active ghost
    """
    global blinky_pos
    global pinky_pos
    global clyde_pos
    global inky_pos
    global pacman_pos
   
    scared_dist = float('Inf')
    active_dist = float('Inf')
    
    dx = abs(pacman_pos[0]-blinky_pos[0])
    dy = abs(pacman_pos[1]-blinky_pos[1])
    delta = 0
    if dx != 0 and dy != 0:
        delta = dx+dy-1
    else:
        delta = dx+dy
    if(blinky_pos[2] == 1):
        # if(active_dist == float('Inf')):
        #     active_dist = 0
        # active_dist += delta
        if(active_dist > delta):
            active_dist = delta
    elif(blinky_pos[2] == 0):
        # if(scared_dist == float('Inf')):
        #     scared_dist = 0
        # scared_dist += delta
        if(scared_dist > delta):
            scared_dist = delta

    dx = abs(pacman_pos[0]-pinky_pos[0])
    dy = abs(pacman_pos[1]-pinky_pos[1])
    delta = 0
    if dx != 0 and dy != 0:
        delta = dx+dy-1
    else:
        delta = dx+dy
    if(pinky_pos[2] == 1):
        # if(active_dist == float('Inf')):
        #     active_dist = 0
        # active_dist += delta
        if(active_dist > delta):
            active_dist = delta
    elif(pinky_pos[2] == 0):
        # if(scared_dist == float('Inf')):
        #     scared_dist = 0
        # scared_dist += delta
        if(scared_dist > delta):
            scared_dist = delta

    dx = abs(pacman_pos[0]-inky_pos[0])
    dy = abs(pacman_pos[1]-inky_pos[1])
    delta = 0
    if dx != 0 and dy != 0:
        delta = dx+dy-1
    else:
        delta = dx+dy
    if(inky_pos[2] == 1):
        # if(active_dist == float('Inf')):
        #     active_dist = 0
        # active_dist += delta
        if(active_dist > delta):
            active_dist = delta
    elif(inky_pos[2] == 0):
        # if(scared_dist == float('Inf')):
        #     scared_dist = 0
        # scared_dist += delta
        if(scared_dist > delta):
            scared_dist = delta

    dx = abs(pacman_pos[0]-clyde_pos[0])
    dy = abs(pacman_pos[1]-clyde_pos[1])
    delta = 0
    if dx != 0 and dy != 0:
        delta = dx+dy-1
    else:
        delta = dx+dy
    if(clyde_pos[2] == 1):
        # if(active_dist == float('Inf')):
        #     active_dist = 0
        # active_dist += delta
        if(active_dist > delta):
            active_dist = delta
    elif(clyde_pos[2] == 0):
        # if(scared_dist == float('Inf')):
        #     scared_dist = 0
        # scared_dist += delta
        if(scared_dist > delta):
            scared_dist = delta

    return scared_dist, active_dist

def isDead():
    """Discover whether Ms. Pacman will is equivalently dead to give the
    reward before the game

    Returns
    -------
        bool
            Is Ms. Pacman equivalently dead
    """
    global blinky_pos
    global pinky_pos
    global clyde_pos
    global inky_pos
    global pacman_pos
    
    dx = abs(pacman_pos[0]-blinky_pos[0])
    dy = abs(pacman_pos[1]-blinky_pos[1])
    delta = 0
    if dx != 0 and dy != 0:
        delta = dx+dy-1
    else:
        delta = dx+dy
    if(delta < 2):
        return True

    dx = abs(pacman_pos[0]-pinky_pos[0])
    dy = abs(pacman_pos[1]-pinky_pos[1])
    delta = 0
    if dx != 0 and dy != 0:
        delta = dx+dy-1
    else:
        delta = dx+dy
    if(delta < 2):
        return True

    dx = abs(pacman_pos[0]-inky_pos[0])
    dy = abs(pacman_pos[1]-inky_pos[1])
    delta = 0
    if dx != 0 and dy != 0:
        delta = dx+dy-1
    else:
        delta = dx+dy
    if(delta < 2):
        return True

    dx = abs(pacman_pos[0]-clyde_pos[0])
    dy = abs(pacman_pos[1]-clyde_pos[1])
    delta = 0
    if dx != 0 and dy != 0:
        delta = dx+dy-1
    else:
        delta = dx+dy
    if(delta < 2):
        return True

    return False

last_moves = [
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
]

def findOscillation(past_moves):
    """Finds the oscillatory behavior of Ms. Pacman

    Parameters
    --------
        past_moves : list(list(int))
            2D array representing the short-term move memory of Ms. Pacman

    Returns:
    --------
        int
            oscillation factor of Ms. Pacman
    """
    oscillations = 0
    for i in range(0, len(past_moves)):
        for j in range(0, len(past_moves[0])):
            oscillations += math.pow(past_moves[i][j], 2)
    return oscillations
