import adversarialSearch
import gserver_sock
import Dynamic_Connect4
import sys


if __name__ == "__main__":
    port = None
    host = None
    gameID = None
    depth = 5

    for idx in range(1, len(sys.argv)):
        if(sys.argv[idx]=='-c'):
            adversarialSearch.ai_player = sys.argv[idx+1]
        elif(sys.argv[idx]=='-p'):
            try:
                port = int(sys.argv[idx+1])
            except:
                print("Invalid port number, port number must be integer")
        elif(sys.argv[idx]=='-h'):
            host = sys.argv[idx+1]
        elif(sys.argv[idx]=='-g'):
            gameID = sys.argv[idx+1]
        
    if(
        adversarialSearch.ai_player is None or
        port is None or
        host is None or
        gameID is None
    ):
        print("Invalid or missing arguments. Usage:\n python3 agent/py -c [colour] -h [server host address] -p [port] -g [gameID]")
        exit(0)

    gserver = gserver_sock.gserver(host, port)
    gserver.Connect(gameID, adversarialSearch.ai_player)

    current_game_env = Dynamic_Connect4.init_env
    player_turn = 'white'
    
    # import time     # REMOVE FOR TOURNAMENT

    while not adversarialSearch.isTerminal(current_game_env):
        # start_time = time.time()            # REMOVE FOR TOURNAMENT
        if(player_turn == adversarialSearch.ai_player):
            adversarialSearch.depth_reached = 0
            adversarialSearch.nodes_eval = 0
            action, value = adversarialSearch.AlphaBetaPruning(None, current_game_env, depth, -float('Inf'), float('Inf'), True)
            gserver.Send(action)

        try:
            nextMove = (gserver.Receive())[0]
        except TimeoutError:
            exit(0)
        # # REMOVE FOR TOURNAMENT  -------------------------------
        # print(f'Player : {player_turn}\t\tTime : {(time.time()-start_time)} secondes')
        # if(player_turn == adversarialSearch.ai_player):
        #     print(f"Move : {action}\t\tValue : {value}")
        #     print(f"Depth : {depth - adversarialSearch.depth_reached}\t\tNodes : {adversarialSearch.nodes_eval}")
        # else:
        #     print(f"Move : {nextMove}")
        # # ------------------------------------------------------
        current_game_env = Dynamic_Connect4.playMove(current_game_env, nextMove, True)
        if(player_turn == 'white'):
            player_turn = 'black'
        else:
            player_turn = 'white'