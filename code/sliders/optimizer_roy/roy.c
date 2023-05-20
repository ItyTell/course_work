#include <stdio.h>
#include <stdlib.h>


float** malloc2d(int dim1, int dim2){
    float** array = (float**)malloc(dim1*sizeof(float*));
    for (int i = 0; i < dim1; i++){
        array[i] = (float*) malloc(dim2 * sizeof(float));
    }
    return array;
}

void free2d(float** array, int dim1){
    for (int i = 0; i< dim1; i++){free(array[i]);}
    free(array);
}


float rnd(float a, float b){return (float)(rand()) / RAND_MAX * (b - a) + a;}


int min_index(float* a, int size){
    int j = 0;float res = a[0];
    for (int i = 1; i < size; i++){if (res > a[i]){j = i; res = a[j];}}
    return j;
}



float* roy(float (*func)(float*), float* A, float* B, float eps, int n, int N, int iteration, float w, float a1, float a2){
    float** X = malloc2d(N, n);
    float** V = malloc2d(N, n);
    float** P = malloc2d(N, n);
    float* res = malloc(N * sizeof(float));


    for (int i = 0; i < N; i++){
        for (int j = 0; j < n; j++){
            X[i][j] = rnd(A[j], B[j]);
            P[i][j] = X[i][j];
            V[i][j] = rnd(-eps, eps);
        }
    }
    for (int i = 0; i < N; i++){res[i] = func(P[i]);}

    int m = min_index(res, N);
    float* b = P[m];
    float* new_res = malloc(N * sizeof(float));

    for (int i = 0; i < N; i++){
        for (int j = 0; j < n; j++){
            X[i][j] = X[i][j] + V[i][j];
        }
    }
    
    for (int k = 0; k < iteration; k++){
        for(int i = 0; i < N; i++){
            new_res[i] = func(X[i]);
            if (new_res[i] < res[i]){res[i] = new_res[i]; P[i] = X[i];}
        }
        m = min(res, N);
        b = P[m];
        for (int i = 0; i < N; i++){
            for (int j = 0; j < n; j++){
                V[i][j] = w * V[i][j] + a1 * rnd(0, 1) * (P[i][j] - X[i][j]) + a2 * rnd(0, 1)*(b[j] - X[i][j]);
                X[i][j] += V[i][j];
                if (X[i][j] < 0){X[i][j] = 0;}
            }
        }

        w = 0.4 + 0.5 / (k + 1);
    }

    return b;

}