import csv_util
from collections import Counter
# Q-table of the 
Q = [[[]]]

def getQtable(filename):
    """Get the Qtable from the csv file storage

    Parameters
    --------
        filename : str
            name of csv to read Qtable from
    """
    Q = csv_util.read_csv(filename)

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
    grid = [[0 for x in range(20)] for y in range(14)]
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
                    color_key = 3           # Corresponds to pacman

            grid[i][j] = color_key
    return grid