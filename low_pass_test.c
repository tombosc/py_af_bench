#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>
#include "low_pass_test.h"

int low_pass(float* x, float* y, int len, float alpha){
	for(int i=0; i<len; i++){
		y[i+1] = (1-alpha) * y[i] + alpha * x[i];
	}
	return 0;
}

// I did not manage to have low_pass_alloc to work with cython
// But it's ok, I just allocate memory in python
/*
float* low_pass_alloc(float* x, int len, float alpha){
	float *y = calloc(4, (len+1));
	for(int i=0; i<len; i++){
		y[i+1] = (1-alpha) * y[i] + alpha * x[i];
	}
	return y;
} 
*/

int main(){
	printf("Hello");
	int n = 500;
	float *x = malloc(4*n);
	for(int i=0; i<n; i++){
		x[i] = rand()/(float)RAND_MAX;
	}
	for(int i=0; i<n; i++){
		printf("%f \n", x[i]);
	}

	float *y = malloc(4*n+1);
	for(int k=0; k < 100000; k++){
		low_pass(x, y, n, 0.9);
		low_pass(x, y, n, 0.9);
		printf("%f\n", y[1]);
		//for(int i=0; i<n; i++){
		//	printf("%f %f \n", x[i], y[i]);
		//}
	}
}
