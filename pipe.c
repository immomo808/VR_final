#include<stdio.h>
#include<stdlib.h>
#include <unistd.h>

const int buffsize = 720/4 * 1280/4 * 3;
unsigned char buff[buffsize];

int main(){
	int n;
	int temp;
	while((n = read(0, buff, buffsize)) > 0){
		for (int i = 0; i < buffsize/3 ; i++){
			temp = (int(buff[i*2])*256 + buff[i*2+1] + 180) % 360;
			buff[i*2] = temp / 256;
			buff[i*2+1] = temp % 256;
		}
		write(1, buff, buffsize);
	}
	return 0;
}
