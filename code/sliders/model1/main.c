#include <stdio.h>
#include <stdlib.h>


float* model1(int size, float beta, float beta1, float l, float p1, float p2, float a, 
                float gama_a, float gama_i, float gama_r, float sigma_i, float sigma_p, float sigma_h, int N, float dt){

    float* S = malloc(size * sizeof(float));
    float* E = malloc(size * sizeof(float));
    float* I = malloc(size * sizeof(float));
    float* P = malloc(size * sizeof(float));
    float* A = malloc(size * sizeof(float));
    float* H = malloc(size * sizeof(float));
    float* R = malloc(size * sizeof(float));
    float* F = malloc(size * sizeof(float));
    float* answer = malloc((int)(size*dt) * sizeof(float));

    S[0] = N - 1;
    E[0] = 0;
    I[0] = 1;
    P[0] = 0;
    A[0] = 0;
    H[0] = 0;
    R[0] = 0;
    F[0] = 0;
    answer[0] = 1;

    int step = (int)(1 / dt);

    float sum = 1;

    for (int i = 0; i < size - 1; i++){
        S[i + 1] = S[i] - (beta * I[i] + l*beta*H[i] + beta1 * P[i]) * S[i] * dt / N; 
        E[i + 1] = E[i] + (beta * I[i] + l*beta*H[i]+ beta1 * P[i]) * S[i] * dt / N - a * E[i] * dt;
        I[i + 1] = I[i] + a * p1 * E[i] * dt - (gama_a + gama_i) * I[i] * dt- sigma_i * I[i] * dt;
        P[i + 1] = P[i] + a * p2 * P[i] * dt - (gama_a + gama_i) * P[i] * dt- sigma_p * P[i] * dt;
        A[i + 1] = A[i] + a * (1 - p1 - p2) * E[i] * dt;
        H[i + 1] = H[i] + gama_a * (I[i] + P[i]) * dt - gama_r * H[i] * dt - sigma_h * H[i] * dt;
        R[i + 1] = R[i] + gama_i * (I[i] + P[i]) * dt + gama_r * H[i] * dt;
        F[i + 1] = F[i] + (sigma_i * I[i] + sigma_p * P[i] + sigma_h * H[i]) * dt;
        sum += I[i + 1] + P[i + 1] + H[i + 1];
        if(i%step == 0){
            answer[(int)(i/step)] = sum;
        }
    }

    free(S);
    free(E);
    free(I);
    free(P);
    free(A);
    free(H);
    free(R);
    free(F);
    return answer;
}

void free_memory(float* answer){
    free(answer);
}