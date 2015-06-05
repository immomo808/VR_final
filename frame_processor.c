#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>

const int buffsize = 720/4 * 1280/4 * 3;
char buff[buffsize];

int main(){
	int temp;
	FILE *fin = freopen(NULL, "rb", stdin);
	FILE *fout = freopen(NULL, "wb", stdout);
	while(fread(buff, buffsize, 1, fin)){

		/* this part is only for testing: shift H by 180 degree */
		for (int i = 0; i < buffsize/3 ; i++){
			temp = ((int)(buff[i*2+1])*256 + buff[i*2] + 180) % 360;
			buff[i*2] = temp % 256;
			buff[i*2+1] = temp / 256;
		}
		/* this part is only for testing: shift H by 180 degree */

		fwrite(buff, buffsize/3*2, 1, fout);
		fflush(fout);
	}
	return 0;
}
