import java.net.*;
import java.io.*;
import java.util.*;
import java.util.logging.*;

/**
 * DC4Server is a very simple TCP server that accepts connections from 
 * players, and automatically matches together the black and white players of 
 * the same gameID. Each line sent to the server corresponds to a move and is 
 * echoed back to both players.
 *
 * @author      Samuel Audet with modifications by Jeremy Cooperstock
 * @version     1.02, 2008-01-21
 */
public class DC4Server {
    public static void main(String args[]) { 
        try {
            logger.addHandler(new FileHandler("DC4Server.log"));
        
            int timeout = 10000;
            int port = 12345;
            if (args.length > 0) {
                timeout = Integer.parseInt(args[0]);
            }
            if (args.length > 1) {
                port = Integer.parseInt(args[1]);
            }
            new DC4Server(timeout, port).run();
        } catch (IOException e) {
            logger.severe(e.getMessage());
            System.exit(1);
        }
    }

    public DC4Server(int timeout, int port) throws IOException {
        this.timeout = timeout;
        this.serverSocket = new ServerSocket(port);
        logger.info("DC4Server on port " + port + " with timeout = " + timeout + " ms is up.");
    }

    public void run() {
        // hash used to find opponents with the same gameID
        HashMap<String,ClientThread> clientHash = new HashMap<String,ClientThread>();
        while (true) {
            try {
                new ClientThread(serverSocket.accept(), clientHash, timeout).start();
            } catch (IOException e) {
                logger.severe(e.getMessage());
            }
        }
    }

    private int timeout;
    private ServerSocket serverSocket = null;
    // private static final Random random = new Random();
    private static final Logger logger = Logger.getLogger("global");

    /**
     * ClientThread is a thread running for each player connected to the server.
     * It is responsible of parsing the messages, validating their contents,
     * and sending back replies to both player, including whether or not the piece
     * played died. It does not keep in memory or validate the state of the game.
     *
     * @author      Samuel Audet
     * @version     1.02, 2008-01-21
     */
    private static class ClientThread extends Thread {

        public ClientThread(Socket socket, HashMap<String,ClientThread> clientHash, int timeout) throws IOException {
            this.socket = socket;
            this.clientHash = clientHash;
            this.timeout = timeout;
            out = new PrintWriter(socket.getOutputStream(), true);
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            state = State.INIT;
            opponent = null;
        }

        public void run() {
            try {
                while (state != State.GAMEOVER) {
                    try {
                        String inputLine = in.readLine();
                        if (inputLine == null) {
                            break;
                        }
                        processLine(inputLine);
                    } catch (Exception e) {
                        out.print(e.getMessage() + "\n"); 
                        out.flush();
                    }
                }
            } catch (Exception e) {
                logger.severe(e.getMessage());
            } finally {
                // client is dying, cleanup
                synchronized (clientHash) {
                    clientHash.put(gameID + " " + color, null);
                }
                if (opponent != null) {
                    synchronized (opponent) {
                        opponent.state = State.GAMEOVER;
                        opponent.opponent = null;
                        opponent.notify();
                        try {
                            opponent.socket.close(); // unblocks blocking IO
                        } catch (IOException e) { }
                    }
                }
                try {
                    socket.close();
                } catch (IOException e) { }
                logger.info(color + " player's client of gameID = \"" + gameID + "\" is disconnected.");
            }
        }

        private Socket socket;
        private HashMap<String,ClientThread> clientHash;
        private int timeout;
        private PrintWriter out; 
        private BufferedReader in; 
        private enum State { INIT, PLAYING, GAMEOVER }
        private State state;
        private boolean myturn;

        private static final String WHITE = "white", BLACK = "black";
        private String gameID, color;
        private ClientThread opponent;

        private synchronized void processLine(String inputLine) throws Exception {
            switch (state) {
            case INIT: {
                String[] ss = inputLine.split(" ");

                if (ss.length != 2) {
                    throw new Exception("Invalid init string. Format: <gameID> <black | white>");
                }
                gameID = ss[0];
                color = ss[1].toLowerCase();
                if (!color.equals(BLACK) && !color.equals(WHITE)) {
                    throw new Exception("Invalid color. Needs to be either \"black\" or \"white\".");
                }
                synchronized (clientHash) {
                    if (clientHash.get(gameID + " " + color) != null) {
                        throw new Exception(color + " player of gameID = \"" + gameID + "\" is already connected.");
                    }
                    clientHash.put(gameID + " " + color, this);
                    opponent = clientHash.get(gameID + " " + (color.equals(BLACK) ? WHITE : BLACK));
                }
                if (opponent == null) {
                    logger.info(color + " player of gameID = \"" + gameID + "\" is waiting for an opponent...");
                    wait(60000);
                    if (opponent == null) {
                        state = State.GAMEOVER;
                        throw new Exception("Waited one minute, but still no opponent: Aborting.");
                    }
                } else {
                    synchronized (opponent) {
                        opponent.opponent = this;
                        opponent.notify();
                    }
                    logger.info("gameID = \"" + gameID + "\" has started!");
                }

                assert (opponent != null && gameID.equals(opponent.gameID));

                // start the game!
                state = State.PLAYING;
                out.print(gameID + " " + color + "\n"); 
                out.flush();

                // white moves first
                if (color.equals(WHITE)) {
                    myturn = true;
                } else {
                    waitForOpponent();
                }

                break;
            }

            case PLAYING: {
                assert (opponent != null);

                String outputLine = inputLine + "\n"; // add this for elegance of echo ouptut
		int op;
		   
		int x, y = -1;
		op = inputLine.charAt(2);
		if (op!='N' && op!='S' && op!='W' && op !='E') {
		    throw new Exception("operator must be one of N, S, E, W");
		}

                x = inputLine.charAt(0)-48;
                y = inputLine.charAt(1)-48;

		if (x < 1 || x > 7) {
		    throw new Exception(x + " is not a valid column number. Needs to be between 1 and 7.");
		}
                
		if (y < 1 || y > 7) {
			throw new Exception(y + " is not a valid row number. Needs to be between 1 and 7.");
		}

		out.print(outputLine);
                out.flush();
                synchronized (opponent) {
                    opponent.out.print(outputLine);
                    opponent.out.flush();
                    opponent.myturn = true;
                    opponent.notify();
                }
                waitForOpponent();
                break;
            }

            case GAMEOVER:
            default:
                break;
            }
        }

        private void waitForOpponent() throws InterruptedException {
            myturn = false;
            wait(timeout);
            if (!myturn) {
                String s = "Timeout of " + timeout + " ms triggered: Game over.\n";

                state = State.GAMEOVER;
                out.print(s); 
                out.flush();

                synchronized (opponent) {
                    opponent.state = State.GAMEOVER;
                    opponent.out.print(s);
                    opponent.out.flush();
                    opponent.notify();
                }
                logger.info("gameID = \"" + gameID + "\" has timed out.");
            }
        }
    }
    

}
