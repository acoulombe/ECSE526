# Dynamic Connect 4 - Artificial Intelligence Agent

This project consits of an AI agent capable of playing the game Dynamic Connect 4. The goal of the game is to align 4 pieces of your colour in a line (either horizontal, vertical or diagonal). Each player takes turns to move one of their pieces in one of the cardinal directions. First player to achieve the goal is victorious.

### Project Content

The agent has 4 files in order to function. The file **agent.py** runs the AI agent playing the game. The other files are its dependencies. **gserver_sock.py** manages the communication with the game server. **Dynamic_Connect4.py** manages the game state that the AI can use for its adversarial search algorithm. **adversarialSearch.py** contains the adversarial search algorithms Minimax and alpha beta pruning that the AI can use to play the game.

### Running the agent

The agent can be run from the command line using the Python 3.6 interpreter or newer. To run the agent, a game server must be running and the server information, _address and port_, must be provided to the script. The game information must also be provided in the arguments so that the agent knows which player it is, _game ID and player colour_.

```
python3 <path-to-project>/agent.py -c [colour] -h [server host address] -p [port] -g [gameID]
```

The order of the information doesn't matter as long as the indicators (-c, -h, -p, -g) are preceding the designated information. Also, **all** the information must be provided. The agent will not start if information is missing.