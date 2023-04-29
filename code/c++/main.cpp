#include <iostream>
#include <vector>
#include <math.h>
#include <random>
#include <cstdlib>
#include <ctime>
#include <fstream>
#include <string>

using namespace std;


# define M_PI           3.14159265358979323846 

pair<int, float> min(vector<float> a){
    int size = a.size();
    int j = 0;
    float res = a[j];
    for (int i = 1; i < size; i++){if (res > a[i]){j = i; res = a[j];}}
    return pair<int, float>(j, res);
}

float rnd(float a = 0, float b = 1){return double(rand()) / RAND_MAX * (b - a) + a;}

vector<float> model(vector<float>parameters, float dt){

    float beta = parameters[0];
    float beta1 = parameters[1];
    float l = parameters[2];
    float k = parameters[3];
    float p1 = parameters[4];
    float p2 = parameters[5];
    float gama_a = parameters[6];
    float gama_i = parameters[7];
    float sigma_i = parameters[8];
    float sigma_p = parameters[9];
    float gama_r = parameters[10];
    float sigma_h = parameters[11];

    const  int T = 100;

    vector<float> S(T/dt);
    vector<float> E(T/dt);
    vector<float> I(T/dt);
    vector<float> P(T/dt);
    vector<float> A(T/dt);
    vector<float> H(T/dt);
    vector<float> R(T/dt);
    vector<float> F(T/dt);
    
    int N = int(11000000 / 250);
    S[0] = N - 6;
    I[0] = 1;
    P[0] = 5;

    for (int t = 1; t < int(T / dt); t++){
        S[t] = (-beta * S[t - 1] * I[t - 1] - l * beta * H[t - 1] * S[t - 1] - beta1 * P[t - 1] * S[t - 1] )/ N;
        E[t] = -S[t] - k * E[t - 1];
        I[t] = k * p1 * E[t - 1] - (gama_a + gama_i) * I[t - 1] - sigma_i * I[t - 1];
        P[t] = k * p2 * E[t - 1] - (gama_a + gama_i) * P[t - 1] - sigma_p * P[t - 1];
        A[t] = k * (1 - p1 - p2) * E[t - 1];
        H[t] = gama_a * (I[t - 1] + P[t - 1]) - gama_r * H[t - 1] - sigma_h * H[t - 1];
        R[t] = gama_i * (I[t - 1] + P[t - 1]) + gama_r * H[t - 1];
        F[t] = sigma_i * I[t - 1] + sigma_p * P[t - 1] + sigma_h * H[t - 1];
        

        S[t] = S[t - 1] + S[t] * dt;
        E[t] = E[t - 1] + E[t] * dt;
        I[t] = I[t - 1] + I[t] * dt;
        P[t] = P[t - 1] + P[t] * dt;
        A[t] = A[t - 1] + A[t] * dt;
        H[t] = H[t - 1] + H[t] * dt;
        R[t] = R[t - 1] + R[t] * dt;
        F[t] = F[t - 1] + F[t] * dt;
    }
    return E;


}

vector<float> roy(float (*func)(vector<float>), vector<float> A, vector<float> B,float eps, int n, int N, int iteration, float w, float a1, float a2){
    vector<vector<float>>X(N, vector<float>(n));
    vector<vector<float>>V(N, vector<float>(n));



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
        b = P[m.first];
        for (int i = 0; i < N; i++){
            for (int j = 0; j < n; j++){
                V[i][j] = w * V[i][j] + a1 * rnd(0, 1) * (P[i][j] - X[i][j]) + a2 * rnd(0, 1)*(b[j] - X[i][j]);
                X[i][j] += V[i][j];
            }
        }

        w = 0.4 + 0.5 / (k + 1);
    }

    return b;

}

float f1(vector<float> X){
    float result = 0;
    for (int i = 0; i < X.size(); i++){
        result += X[i] * X[i] - 10 * cos(2 * M_PI * X[i]);
    }
    result += X.size() * 10;
    return result;
}

double Double(string s) {
    int l = 0, k = 10;
    double sum = 0, p = 0;
    int i = 0;
    bool flag = 1;
    size_t size = s.size();
    for (; i < size; i++) {
        l = int(s[i]);
        if (flag) {sum *= 10;}
        if (l >= 48 && l <= 57) {
            p = l - 48;
            if (!flag) { p /= k; k *= 10; }
            sum += p;
        }
        else if (l == 46) {
            if (!flag){ throw std::logic_error("two points"); }
            sum /= 10;
            flag = 0;
        }
        else { throw std::logic_error("not a constant"); }
    }
    return sum;
}




float dist(vector<float> parameters){
    return 1;
}


int main(){
    float dt = 0.0001;
    srand(time(NULL));
    ifstream Data("code\\data.txt");

    vector<int> real_data(100);
    string data;
    for (int i = 0; i < 100; i++){
        getline(Data, data);
        cout << data << endl;
        real_data[i] = int(Double(data));
    }    
    Data.close();

    //vector<float>parameters = {2.55, 1.56, 7.65, 0.25, 0.58, 0.001, 0.94, 0.27, 0.5, 3.5, 1, 0.3};

    //vector<float> I = model(parameters, dt);
    //int j;
    //for (int i = 1; i < 100; i++){
    //    j = int(i / dt);
    //    if (i % 10 == 0){cout << "\n";}
    //    cout << floor(I[j])<<"   ";
    //}

    //vector<float> A(12, 0);
    //vector<float> B(12, 10);

    //vector<float> result = roy(dist, A, B, 0.01, 12, 100, 100000, 0.9, 1.5, 1.7  );

    //for (int i = 0; i < result.size(); i++){cout<< result[i] << endl;}
    //cout << "f1() = " << dist(result) << endl;

    cout<< real_data[30];

    return 0;
}