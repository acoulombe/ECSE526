import adversarialSearch
import gserver_sock
import Dynamic_Connect4
import sys


if __name__ == "__main__":
    port = None
    host = None
    gameID = None

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
    
    while not adversarialSearch.isTerminal(current_game_env):
        if(player_turn == adversarialSearch.ai_player):
            action, value = adversarialSearch.AlphaBetaPruning(None, current_game_env, 4, -float('Inf'), float('Inf'), True)
            gserver.Send(action)

        try:
            nextMove = (gserver.Receive())[0]
        except TimeoutError:
            exit(0)
        
        current_game_env = Dynamic_Connect4.playMove(current_game_env, nextMove, True)
        if(player_turn == 'white'):
            player_turn = 'black'
        else:
            player_turn = 'white'