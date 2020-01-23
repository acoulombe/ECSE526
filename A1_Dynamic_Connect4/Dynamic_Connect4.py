import copy

init_env=[
[' ',' ',' ',' ',' ',' ','X'],
['X',' ',' ',' ',' ',' ','O'],
['O',' ',' ',' ',' ',' ','X'],
['X',' ',' ',' ',' ',' ','O'],
['O',' ',' ',' ',' ',' ','X'],
['X',' ',' ',' ',' ',' ','O'],
['O',' ',' ',' ',' ',' ',' ']
]

test_env1=[
[' ',' ',' ',' ',' ',' ',' '],
[' ',' ',' ',' ',' ',' ',' '],
['O',' ','X',' ',' ',' ',' '],
[' ',' ',' ','O',' ',' ','X'],
[' ',' ',' ',' ','O','X','X'],
[' ',' ','O',' ',' ','O','X'],
[' ',' ',' ','X','O',' ',' ']
]

test_env2=[
['O','O',' ',' ',' ',' ',' '],
['X',' ',' ',' ',' ',' ',' '],
[' ',' ','X',' ',' ','O',' '],
[' ',' ','X','O',' ',' ','X'],
[' ',' ',' ',' ','O','X',' '],
[' ','X',' ',' ',' ',' ',' '],
['O',' ',' ',' ',' ',' ',' ']
]

test_env3=[
[' ',' ','O',' ','X',' ',' '],
[' ',' ','O',' ','X',' ',' '],
[' ',' ','X',' ','O',' ',' '],
[' ',' ','X',' ','O',' ',' '],
[' ',' ',' ',' ',' ',' ',' '],
[' ',' ','O',' ','X',' ',' '],
[' ',' ','X',' ','O',' ',' ']
]

def playMove(curr_game_env, move, display):
    """Plays the player's move on the game environment.
    The game environment feed to the function is deepcopied,
    so it is not required to make a backup.
    Prints game board when display is set to True

    Parameters
    --------
        curr_game_env: list(list(str))
            game environment before playing a move

        move: str
            string denoting the coordinates of the piece and
            the direction of movement (eg. 71W)
        display: bool
            toggle whether to print game environment after move
    
    Returns
    --------
        game_env: list(list(str))
            game environment after playing a move
    """
    game_env = copy.deepcopy(curr_game_env)
    old_x = int(move[0])-1
    old_y = int(move[1])-1
    if(move[2]=='N' or move[2]=='n'):
        new_x = old_x
        new_y = old_y-1     
    elif(move[2]=='S' or move[2]=='s'):
        new_x = old_x
        new_y = old_y+1
    elif(move[2]=='E' or move[2]=='e'):
        new_x = old_x+1
        new_y = old_y  
    elif(move[2]=='W' or move[2]=='w'):
        new_x = old_x-1
        new_y = old_y  
    game_env[new_y][new_x]=game_env[old_y][old_x]
    game_env[old_y][old_x]=' '    
    if display:
        print('  1,2,3,4,5,6,7')
        for y_idx in range(0, len(game_env)):
            print(y_idx+1, end=' ')
            for x_idx in range(0, len(game_env[0])):
                print(game_env[y_idx][x_idx], end='')
                if(x_idx==len(game_env[0])-1):
                    print("\n", end='')
                else:
                    print(',',end='')
        print('\n')
    return game_env
    
