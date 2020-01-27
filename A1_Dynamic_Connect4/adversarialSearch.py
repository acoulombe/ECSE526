import Dynamic_Connect4

ai_player = None    # either black or white
depth_reached = 0
nodes_eval = 0

def MiniMax(move, state, depth_left, max_player):
    """MiniMax-Decision algorithm for finding the action 
    corresponding to the move that leads to the outcome 
    with the best utility, under the assumption that the
    opponent plays to minimize utility.

    Parameters
    --------
        move: str
            move that generated state
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
    # global nodes_eval           # REMOVE FOR TOURNAMENT
    # global depth_reached        # REMOVE FOR TOURNAMENT
    # nodes_eval = nodes_eval+1   # REMOVE FOR TOURNAMENT
    if depth_left == 0 or isTerminal(state):
        # depth_reached = depth_left  # REMOVE FOR TOURNAMENT
        return move, heuristic(state)
    if max_player:
        value = -float('Inf')
        possibleMoves = generateMoves(state, max_player)
        bestMove = None
        for i in range(0, len(possibleMoves)):
            new_state = Dynamic_Connect4.playMove(state, possibleMoves[i], False)
            action, alt_val = MiniMax(possibleMoves[i], new_state, depth_left-1, False)
            if alt_val > value:
                value = alt_val
                bestMove = possibleMoves[i]
        return bestMove, value

    else:   #min player
        value = float('Inf')
        possibleMoves = generateMoves(state, max_player)
        bestMove = None
        for i in range(0,len(possibleMoves)):
            new_state = Dynamic_Connect4.playMove(state, possibleMoves[i], False)
            action, alt_val = MiniMax(possibleMoves[i], new_state, depth_left-1, True)
            if alt_val < value:
                value = alt_val
                bestMove = possibleMoves[i]
        return bestMove, value

def AlphaBetaPruning(move, state, depth_left, alpha, beta, max_player):
    """MiniMax-Decision algorithm for finding the action 
    corresponding to the move that leads to the outcome 
    with the best utility, under the assumption that the
    opponent plays to minimize utility.

    Parameters
    --------
        move: str
            move that generated state
        state: list(list(str))
            2D matrix representing the game state
        depth_left: int 
            remaining depth of the search that can still be done
        alpha: int
            best value seen for maximizing player
        beta: int
            best value seen for the minimizing player
        max_player: bool
            indicates whether it's our turn (max) or opponent's turn (min)

    Returns
    --------
        action: str
            best action to perform
        value: float
            heuristic value of the best action
    """
    # global nodes_eval           # REMOVE FOR TOURNAMENT
    # global depth_reached        # REMOVE FOR TOURNAMENT
    # nodes_eval = nodes_eval+1   # REMOVE FOR TOURNAMENT
    if depth_left == 0 or isTerminal(state):
        # depth_reached = depth_left  # REMOVE FOR TOURNAMENT
        return move, heuristic(state)
    if max_player:
        value = -float('Inf')
        possibleMoves = generateMoves(state, max_player)
        bestMove = None
        for i in range(0, len(possibleMoves)):
            new_state = Dynamic_Connect4.playMove(state, possibleMoves[i], False)
            action, alt_val = AlphaBetaPruning(possibleMoves[i], new_state, depth_left-1, alpha, beta, False)
            if alt_val > value:
                value = alt_val
                bestMove = possibleMoves[i]
            alpha = max(alpha, alt_val)
            if beta <= alpha:
                break
        return bestMove, value

    else:   #min player
        value = float('Inf')
        possibleMoves = generateMoves(state, max_player)
        bestMove = None
        for i in range(0,len(possibleMoves)):
            new_state = Dynamic_Connect4.playMove(state, possibleMoves[i], False)
            action, alt_val = AlphaBetaPruning(possibleMoves[i], new_state, depth_left-1, alpha, beta, True)
            if alt_val < value:
                value = alt_val
                bestMove = possibleMoves[i]
            beta = min(beta, alt_val)
        return bestMove, value

def generateMoves(state, max_player):
    """Generate list of actions that the agent could choose from

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
    
    # # Sorted by heuristic         # TOO SLOW FOR TOURNAMENT
    # possibleMoves.sort(key=lambda move: sortHeuristic(move, state),reverse=(ai_player == 'white' and max_player))

    return possibleMoves

def sortHeuristic(move, state):
    """heuristic function for the move ordering sort
    Used to sort moves based on the moves that give the best heuristics

    Parameters
    --------
        move: str
            move to be performed
        state: list(list(str))
            current game environment
    
    Returns
    --------
        int
            heuristic value of the move
    """
    new_state = Dynamic_Connect4.playMove(state, move, False)
    return heuristic(new_state)

def isTerminal(state):
    """Checks whether a player has aligned 4 pieces
    
    Parameters
    --------
        state: list(list(str))
            game state being verified
    Returns
    --------
        bool
            is game state terminal
    """
    for y in range(0, len(state)):
        for x in range(0,len(state[0])):
            for player in ['X','O']:
                #Check if horizontal line is formed
                if(
                    x<=3 and         #Don't need to check further (doesn't fit)
                    state[y][x] == player and
                    state[y][x+1]==player and
                    state[y][x+2]==player and
                    state[y][x+3]==player
                ):
                    return True

                #Check if vertical line is formed
                if(
                    y<=3 and         #Don't need to check further (doesn't fit)
                    state[y][x] == player and
                    state[y+1][x]==player and
                    state[y+2][x]==player and
                    state[y+3][x]==player
                ):
                    return True
                
                #Check if diagonal line is formed
                if(
                    x<=3 and y<=3 and #Don't need to check further (doesn't fit)
                    state[y][x]  ==  player and
                    state[y+1][x+1]==player and
                    state[y+2][x+2]==player and
                    state[y+3][x+3]==player
                ):
                    return True

                if(
                    x<=3 and y>=3 and #Don't need to check further (doesn't fit)
                    state[y][x]  ==  player and
                    state[y-1][x+1]==player and
                    state[y-2][x+2]==player and
                    state[y-3][x+3]==player
                ):
                    return True
    return False

position_val=[
[0,0,0,0,0,0,0],
[0,1,1,1,1,1,0],
[0,1,2,2,2,1,0],
[0,1,2,3,2,1,0],
[0,1,2,2,2,1,0],
[0,1,1,1,1,1,0],
[0,0,0,0,0,0,0]
]

def heuristic(state):
    """Ranks alternatives in search algorithms at each
    branching step based on available information to 
    decide which branch to follow

    heuristic based on:
        - how many of your pieces are aligned (+1 for each piece around a piece)
        - how many of the opponent pieces are aligned (-1 for each piece around a piece)
        - how much dominance do you have on the field

    Parameters
    --------
        state: list(list(str))
            state of the game being evaluated
    
    Returns
    --------
        float
            value of the estimated utility of the state
    """
    white_score = 0
    black_score = 0
    for y in range(0, len(state)):
        for x in range(0,len(state[0])):
            if(state[y][x]=='O'):
                white_score = white_score + position_val[y][x]
                
                #Check for alignment
                #Check if horizontal line is formed
                if(x<(len(state[0])-1) and state[y][x+1]==state[y][x]):
                    if(x<(len(state[0])-2) and state[y][x+2]==state[y][x]):
                        if(x<(len(state[0])-3) and state[y][x+3]==state[y][x]):
                            white_score = white_score+1000
                        white_score = white_score+2
                    white_score = white_score+1
                
                #Check if vertical line is formed
                if(y<(len(state)-1) and state[y+1][x]==state[y][x]):
                    if(y<(len(state)-2) and state[y+2][x]==state[y][x]):
                        if(y<(len(state)-3) and state[y+3][x]==state[y][x]):
                            white_score = white_score+1000
                        white_score = white_score+2
                    white_score = white_score+1
                
                #Check if diagonal line is formed
                if(x<(len(state[0])-1) and y<(len(state)-1) and state[y+1][x+1]==state[y][x]):
                    if(x<(len(state[0])-2) and y<(len(state)-2) and state[y+2][x+2]==state[y][x]):
                        if(x<(len(state[0])-3) and y<(len(state)-3) and state[y+3][x+3]==state[y][x]):
                            white_score = white_score+1000
                        white_score = white_score+2
                    white_score = white_score+1

                if(x<(len(state[0])-1) and y>1 and state[y-1][x+1]==state[y][x]):
                    if(x<(len(state[0])-2) and y>2 and state[y-2][x+2]==state[y][x]):
                        if(x<(len(state[0])-3) and y>3 and state[y-3][x+3]==state[y][x]):
                            white_score = white_score+1000
                        white_score = white_score+2
                    white_score = white_score+1


            elif(state[y][x]=='X'):
                black_score = black_score + position_val[y][x]
                
                #Check for alignment
                #Check if horizontal line is formed
                if(x<(len(state[0])-1) and state[y][x+1]==state[y][x]):
                    if(x<(len(state[0])-2) and state[y][x+2]==state[y][x]):
                        if(x<(len(state[0])-3) and state[y][x+3]==state[y][x]):
                            black_score = black_score+1000
                        black_score = black_score+2
                    black_score = black_score+1
                
                #Check if vertical line is formed
                if(y<(len(state)-1) and state[y+1][x]==state[y][x]):
                    if(y<(len(state)-2) and state[y+2][x]==state[y][x]):
                        if(y<(len(state)-3) and state[y+3][x]==state[y][x]):
                            black_score = black_score+1000
                        black_score = black_score+2
                    black_score = black_score+1
                
                #Check if diagonal line is formed
                if(x<(len(state[0])-1) and y<(len(state)-1) and state[y+1][x+1]==state[y][x]):
                    if(x<(len(state[0])-2) and y<(len(state)-2) and state[y+2][x+2]==state[y][x]):
                        if(x<(len(state[0])-3) and y<(len(state)-3) and state[y+3][x+3]==state[y][x]):
                            black_score = black_score+1000
                        black_score = black_score+2
                    black_score = black_score+1

                if(x<(len(state[0])-1) and y>1 and state[y-1][x+1]==state[y][x]):
                    if(x<(len(state[0])-2) and y>2 and state[y-2][x+2]==state[y][x]):
                        if(x<(len(state[0])-3) and y>3 and state[y-3][x+3]==state[y][x]):
                            black_score = black_score+1000
                        black_score = black_score+2
                    black_score = black_score+1
                
    if(ai_player == 'white'):
        return white_score - black_score
    else:
        return black_score- white_score
