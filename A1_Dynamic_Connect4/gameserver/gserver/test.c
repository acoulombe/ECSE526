#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <netdb.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/time.h>

#define COLOR_LEN 30
#define DEF_PORT 12345
#define DEF_MSG_SIZE 100
#define BUF_SIZE 10000

void Send (int, char *);

/*
 * This program is simple test of the operation of the game server, which takes text lines terminated by carriage returns
 * from each of two players and relays the moves between them.
 */

void Usage(char *prog)
{
	printf ("Usgae: %s %s\n", prog, "[-c color] [-p port] serverhost");
	exit(0);
}

main (int argc, char *argv[]) {
  extern char *optarg;
  extern int optind, opterr;
  int sock;
  in_addr_t interface_addr = htonl(INADDR_ANY);
  struct sockaddr_in name;
  struct hostent *hp, *gethostbyname();
  int c, i;
  char buf[BUF_SIZE];
  char *serverIP;
  int serverPort = DEF_PORT;
  char color[COLOR_LEN];
  char moves[] = "NSEW";

  strcpy (color, "white");

  /* check command line arguments */
  while ((c = getopt(argc, argv, "c:i:p:")) != -1) {
    switch (c) {
    case 'c':
      strcpy (color, optarg);
      break;
     case 'p':
  	serverPort = atoi(optarg);
	break;
    default:
      Usage(argv[0]);
    }
  }

  if (optind >= argc) {
      Usage(argv[0]);
  }

  serverIP = argv[optind];

  /* Create socket on which to send. */
  sock = socket(AF_INET, SOCK_STREAM, 0);
  if (sock < 0) {
    perror("opening socket");
    exit(1);
  }

  name.sin_family = AF_INET;
  name.sin_port = htons(serverPort);

  if ((hp = gethostbyname(serverIP)) == 0) {
    fprintf (stderr, "unknown host: %s\n", serverIP);
    exit(1);
  }
  memcpy(&name.sin_addr, hp->h_addr, hp->h_length);

  fprintf (stderr, "Connecting to %s on port %d (TCP)\n", 
	   serverIP, serverPort);
  if (connect(sock, (struct sockaddr *)&name, sizeof(name)) < 0) {
    perror("connecting stream socket");
    exit(1);
  }

  /* now run through a pretend game sequence */
  sprintf (buf, "%s %s\n", "mytestgame", color);
  Send(sock, buf);

  while (1) {
    sleep(1);
    /* generate a random move, consisting of two digits and a cardinal direction */
    sprintf (buf, "%d%d%c\n", rand() % 5 + 1, rand() % 4  + 1,  moves[rand() % 3]);
    Send(sock, buf);
  }
}

void Send(int s, char *b) {
  int nread;

  write (s, b, strlen(b));
  if ((nread = read(s, b, BUF_SIZE)) < 0) {
    perror("reading from socket");
    exit (1);
  }
  strtok(b, "\n");  /* string terminates at carriage return */
  printf ("read %s\n", b);
}


