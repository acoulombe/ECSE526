import adversarialSearch
import Dynamic_Connect4
import sys


if __name__ == "__main__":

    for idx in range(1, len(sys.argv)):
        if(sys.argv[idx]=='-c'):
            adversarialSearch.ai_player = sys.argv[idx+1]
        
    if(adversarialSearch.ai_player is None):
        print("Invalid or missing arguments. Usage:\n python3 agent/py -c [colour]")
        exit(0)

    current_game_env = Dynamic_Connect4.init_env
    player_turn = 'white'

    import time
    
    while not adversarialSearch.isTerminal(current_game_env):
        if(player_turn == adversarialSearch.ai_player):
            start_time = time.time()
            # action, value = adversarialSearch.MiniMax(None, current_game_env, 6, True)
            action, value = adversarialSearch.AlphaBetaPruning(None, current_game_env, 4, -float('Inf'), float('Inf'), True)
            print(time.time()-start_time)
            nextMove = action
        else:
            nextMove = input('Enter move:')

        current_game_env = Dynamic_Connect4.playMove(current_game_env, nextMove, True)
        if(player_turn == 'white'):
            player_turn = 'black'
        else:
            player_turn = 'white'
