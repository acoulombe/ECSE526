import socket

class gserver():
    """This is a class to communicate the agent's actions
    to the game server
    
    Attributes
    --------
        address: str
            identification/IP Address of the game server
        port: int 
            port ID for the connection to the game server
        sock: socket
            socket connecting to the game server
    """

    TIMEOUT_msg = 'Timeout of 10000 ms triggered: Game over.'

    def __init__(self, address, port):
        """Constructor for the game server class

        Parameters
        --------
            address: str
                socket string for the game server
            port: int
                port ID to use to connect to the game server
        """
        self.address = address
        self.port = port
    
    def Connect(self, gameID, player, timeout=10000):
        """Connects agent to game server

        Parameters
        --------
            gameID: str
                Name of the game to be played
            player: str
                indicate if white player or black player
            timeout: int
                timeout in ms

        Returns
        --------
        status: boolean 
            Return whether the connection is established
        """
        try:
            self.sock = socket.socket()
            try:
                self.sock.connect((self.address, self.port))
                self.sock.settimeout(timeout/1000)
            except socket.timeout:
                raise TimeoutError                          
            # Receive confirmation of connection
            if self.sock is None:
                raise RuntimeError
            
            request = f"{gameID} {player}"
            self.Send(request)
            answer = self.Receive()
            print(answer)
            print(request)
            if(request==answer[0]):
                return True
            else:
                self.Disconnect()
                return False

        except TimeoutError:
            return False

    def Disconnect(self):
        """Disconnects agent from game server
        """
        if(self.sock is not None):
            self.sock.close()
            self.sock = None   

    def Send(self, action):
        """Sends action to the game server

        Parameters
        --------
            action: str
                action agent wants to perform
        """
        if(self.sock is not None):
            self.sock.send((action+"\n").encode("ascii"))
    
    def Receive(self):
        """Receives data from the game server

        Returns
        --------
            ans_list: list of game states received from game server
        """
        if(self.sock is not None):
            answer = self.sock.recv(1024).decode("ascii")
            ans_list = answer.split('\n')
            ans_list.pop(-1)
            for ans in ans_list:
                if(ans == self.TIMEOUT_msg):
                    print('Timeout of 10000 ms triggered: Game over.')
                    self.Disconnect()      
            return ans_list
        
