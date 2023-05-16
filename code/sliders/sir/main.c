#include <stdio.h>
#include <stdlib.h>

float* sir(float *answer, int size, float beta, float gama, int N, float dt){
    float* S = malloc(size * sizeof(float));
    float* I = malloc(size * sizeof(float));
    float* R = malloc(size * sizeof(float));

    S[0] = 0;
    I[0] = 1;
    R[0] = 0;
    answer[0] = 1;

    for (int i = 0; i < size - 1; i++){
        S[i + 1] = S[i] - beta * S[i] * I[i] * dt / N; 
        I[i + 1] = I[i] + (beta * S[i] * I[i] / N - gama * I[i]) * dt;
        R[i + 1] = R[i] + gama * I[i] * dt; 
        answer[i + 1] = answer[i] + I[i + 1];
    }

    free(S);
    free(I);
    free(R);
    return answer;
}