#include <stdio.h>
#include <stdlib.h>


float* seir(int size, float beta, float a, float gama, int N, float dt){

    float* S = malloc(size * sizeof(float));
    float* E = malloc(size * sizeof(float));
    float* I = malloc(size * sizeof(float));
    float* R = malloc(size * sizeof(float));
    float* answer = malloc((int)(size*dt) * sizeof(float));

    S[0] = N - 1;
    I[0] = 1;
    R[0] = 0;
    answer[0] = 1;

    int step = (int)(1 / dt);

    float sum = 1;

    for (int i = 0; i < size - 1; i++){
        S[i + 1] = S[i] - beta * S[i] * I[i] * dt / N; 
        E[i + 1] = E[i] + (beta * S[i] * I[i] / N - a * E[i]) * dt;
        I[i + 1] = I[i] + (a * E[i] - gama * I[i]) * dt;
        R[i + 1] = R[i] + gama * I[i] * dt;
        sum += I[i + 1];
        if(i%step == 0){
            answer[(int)(i/step)] = sum;
        }
    }

    free(S);
    free(E);
    free(I);
    free(R);
    return answer;
}

void free_memory(float* answer){
    free(answer);
}