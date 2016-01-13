//Alexander Chatron-Michaud, 260611509

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "fast_filter.h"

int main ( int argc, char *argv[] ) {
	
	//Prepare 1st argument (img data)
	char *arg1 = argv[1]; 
	FILE* input = fopen(arg1, "rb");
	fseek(input, 0, SEEK_END); // seek to end of file
	int size = ftell(input); // get current file pointer (finding the size)
	fseek(input, 0, SEEK_SET); //seek back to beginning
	unsigned char *img_data = (unsigned char *) malloc(size);
	fread(img_data, 1, size, input);
	fclose(input);

	//Prepare 2nd argument (out img data)
	unsigned char *out_img_data = (unsigned char *) malloc(size);

	//Prepare 3rd argument (filter width)
	char *arg3 = argv[3];	
	int filter_width = atoi(arg3); 
	
	//Prepare 4th-last arguments(filter weights)
	int temp = filter_width * filter_width; 
	float filter_weights[temp];
	for (int i = 4; i<argc; i++) {
		filter_weights[i-4] = atof(argv[i]); 
	}

	//do the filtering
	doFiltering(img_data, filter_weights,filter_width,out_img_data); 

	//now we need to put the data in out_img_data into the .bmp file
	char *arg2 = argv[2];
	FILE* output = fopen(arg2, "wb");
	fwrite(out_img_data, 1, size, output);
	fclose(output);

	//print done (debugging purposes)
	printf("Done!\n");
}