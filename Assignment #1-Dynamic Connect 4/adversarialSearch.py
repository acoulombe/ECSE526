import Dynamic_Connect4

ai_player = None    # either black or white

def MiniMax(state, depth_left, max_player):
    """MiniMax-Decision algorithm for finding the action 
    corresponding to the move that leads to the outcome 
    with the best utility, under the assumption that the
    opponent plays to minimize utility.

    Parameters
    --------
        state: list(list(str))
            2D matrix representing the game state
        depth_left: int 
            remaining depth of the search that can still be done
        max_player: bool
            indicates whether it's our turn (max) or opponent's turn (min)

    Returns
    --------
        action: str
            best action to perform
        value: float
            heuristic value of the best action
    """
    if depth_left == 0 or isTerminal():
        return heuristic()
    if max_player:
        value = -float('Inf')
        possibleMoves, possibleStates = newStates(state, max_player)
        bestMove = None
        for i in range(0, len(possibleStates)):
            action, alt_val = MiniMax(possibleStates[i], depth_left-1, False)
            if alt_val > value:
                value = alt_val
                bestMove = possibleMoves[i]
        return bestMove, value

    else:   #min player
        value = float('Inf')
        possibleMoves, possibleStates = newStates(state, max_player)
        bestMove = None
        for i in range(0,len(possibleStates)):
            action, alt_val = MiniMax(possibleStates[i], depth_left-1, True)
            if alt_val < value:
                value = alt_val
                bestMove = possibleMoves[i]
        return bestMove, value

def newStates(state, max_player):
    """Generate list of actions and consequence states that
    the agent could choose from

    Parameters
    --------
        state: list(list(str))
            state in which the agent is currently in
        max_player: bool
            indicates whether it's our turn (max) or opponent's turn (min)

    Returns
    --------
        possibleMoves: list(str)
            list of possible moves to play
        possibleStates: list(list(list(str)))
            list of game environments associated to moves
    """ 
    player_piece = None
    if(
        (ai_player == 'white' and max_player) or
        (ai_player == 'black' and not max_player)
     ):
        player_piece = 'O'
    else:
        player_piece = 'X'

    possibleMoves = []
    possibleStates = []

    for y in range(0, len(state)):
        for x in range(0,len(state[0])):
            if state[y][x] == player_piece:
                if x<(len(state[0])-1) and state[y][x+1]==' ':
                    possibleMoves.append(f"{x+1}{y+1}E")
                if x>0 and state[y][x-1]==' ':
                    possibleMoves.append(f"{x+1}{y+1}W")
                if y<(len(state)-1) and state[y+1][x]==' ':
                    possibleMoves.append(f"{x+1}{y+1}S")
                if y>0 and state[y-1][x]==' ':
                    possibleMoves.append(f"{x+1}{y+1}N")
    for move in possibleMoves:
        possibleStates.append(Dynamic_Connect4.playMove(state, move, True))
    
    return possibleMoves, possibleStates

def isTerminal():
    pass

def heuristic():
    pass
