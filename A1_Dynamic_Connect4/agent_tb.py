import adversarialSearch
import Dynamic_Connect4
import sys


if __name__ == "__main__":

    depth = 6

    for idx in range(1, len(sys.argv)):
        if(sys.argv[idx]=='-c'):
            adversarialSearch.ai_player = sys.argv[idx+1]
        
    if(adversarialSearch.ai_player is None):
        print("Invalid or missing arguments. Usage:\n python3 agent/py -c [colour]")
        exit(0)

    current_game_env = Dynamic_Connect4.init_env
    player_turn = 'white'

    print('  1,2,3,4,5,6,7')
    for y_idx in range(0, len(current_game_env)):
        print(y_idx+1, end=' ')
        for x_idx in range(0, len(current_game_env[0])):
            print(current_game_env[y_idx][x_idx], end='')
            if(x_idx==len(current_game_env[0])-1):
                print("\n", end='')
            else:
                print(',',end='')
    print('\n')
    import time
    quitGame = False
    
    while not adversarialSearch.isTerminal(current_game_env):
        start_time = time.time()
        if(player_turn == adversarialSearch.ai_player):    
            #action, value = adversarialSearch.MiniMax(None, current_game_env, depth, True)
            action, value = adversarialSearch.AlphaBetaPruning(None, current_game_env, depth, -float('Inf'), float('Inf'), True)
            nextMove = action
        else:
            while True:
                try:
                    nextMove = input('Enter move:')
                    if(nextMove in "Qq"):
                        quitGame = True
                        break
                    x = int(nextMove[0])
                    y = int(nextMove[1])
                    if(nextMove[2] in 'NnEeSsWw'):
                        break
                except:
                    print("Invalid Move!")
                    continue
            if(quitGame):
                exit(0)
        # ------------------- Statistics ------------------------
        print(f'Player : {player_turn}\t\tTime : {(time.time()-start_time)} secondes')
        if(player_turn == adversarialSearch.ai_player):
            print(f"Move : {action}\t\tValue : {value}")
            print(f"Depth : {depth - adversarialSearch.depth_reached}\t\tNodes : {adversarialSearch.nodes_eval}")
        else:
            print(f"Move : {nextMove}")
        # ------------------------------------------------------
        current_game_env = Dynamic_Connect4.playMove(current_game_env, nextMove, True)
        if(player_turn == 'white'):
            player_turn = 'black'
        else:
            player_turn = 'white'
