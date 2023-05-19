#include <stdio.h>
#include <stdlib.h>


float* roy(float (*func)(float*), float* A, float* B, float eps, int n, int N, int iteration, float w, float a1, float a2){
    float** X;
    float** V;



    for (int i = 0; i < N; i++){
        for (int j = 0; j < n; j++){
            X[i][j] = rnd(A[j], B[j]);
            V[i][j] = rnd(-eps, eps);
        }
    }

    vector<vector<float>> P;
    P = X;
    vector<float> res(N);

    for (int i = 0; i < N; i++){res[i] = func(P[i]);}

    pair<int, float> m = min(res);
    vector<float> b = P[m.first];
    vector<float> new_res(N);

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
        m = min(res);
        if (k % 300 == 0){cout<< m.second << endl;}
        b = P[m.first];
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