//Jim King
//csopen.c
//w richard stevens program 15.25

#include "open.h"
#include <sys/uio.h> //iovec

/**
 * open the file by sending the "name" and "oflag" to the
 * connection server and reading a file descriptor back
 */
int csopen( char *name, int oflag )
{
  int len;
  char buf[10];
  struct iovec iov[3];
  static int csfd = -1;

  if( csfd < 0 ) { //open connection to conn server
    if( (csfd=cli_conn(CS_OPEN)) < 0 )
      fprintf( stderr, "cli_conn error\n" );
  }

  sprintf( buf, " %d", oflag ); //oflag to ascii
  iov[0].iov_base = CL_OPEN " ";
  iov[0].iov_len = strlen(CL_OPEN) + 1;
  iov[1].iov_base = name;
  iov[1].iov_len = strlen(name);
  iov[2].iov_base = buf;
  iov[2].iov_len = strlen(buf) + 1;

  //null at end of buf always sent
  len = iov[0].iov_len + iov[1].iov_len + iov[2].iov_len;
  if( writev( csfd, &iov[0], 3) != len )
    fprintf(stderr, "writev error\n" );

  //read back descriptor
  //returned errors handled by write

  fprintf( stderr, "get ready to send\n" );
  return( recv_fd( csfd, write ) );
}

