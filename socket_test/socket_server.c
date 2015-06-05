#include <sys/socket.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <signal.h>

int listfd;
int connfd;

int main(int argc, char *argv[]){

    listfd = socket(AF_UNIX, SOCK_STREAM, 0);
    if(listfd == -1)
        exit(-1);

	struct sockaddr saddr = {AF_UNIX, "tmp"};
	bind(listfd, (struct sockaddr *)&saddr, sizeof(saddr));

    listen(listfd, 10);

    fflush(stdout);
    printf("Running...\n");

    while(1){
        connfd = accept(listfd, NULL, NULL);

		//write(connfd, phrases[r], strlen(phrases[r]));

        close(connfd);
        sleep(1);
    }

    exit(0);
}
