#include <stdio.h>
#include <unistd.h>

/*  Yao Fei  feiyao@me.com */
/*
 * some SACD iso usse 2064bytes/sector 
 * convert it to 2048bytes/sector
 *
 * iso2064 < SRC.iso > DST.iso
 *
 * [--12--][+++2048+++][--4--] is the scheme to keep at leadt with the SACD i tested.
 */

typedef struct {
	int head[3];
	int data[2048/4];
	int tail;
} DVD_SEC;

int main(int argc,char* argv[])
{
	DVD_SEC  dvd;
	int n;

	while(n = read(0, &dvd, 2064)) {
		write(1, dvd.data, 2048);
	}
}
