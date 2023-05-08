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

vector<int> real_data(100);
float dt = 0.001;

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
    float gama = parameters[1];

    const  int T = 100;

    vector<float> S(T/dt);
    vector<float> I(T/dt);
    vector<float> R(T/dt);
    
    int N = int(647601);
    S[0] = N - 6;
    I[0] = 1;
    R[0] = 0;

    for (int t = 1; t < int(T / dt); t++){
        S[t] = -beta * S[t - 1] * I[t - 1]/ N;
        I[t] = S[t] - gama * I[t - 1];
        R[t] = gama * I[t - 1];
        

        S[t] = S[t - 1] + S[t] * dt;
        I[t] = I[t - 1] + I[t] * dt;
        R[t] = R[t - 1] + R[t] * dt;
    }
    return I;


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
        if (k % 20 == 0){cout<< m.second << endl;}
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
    float result = 0; float r1 = 0;
    vector<float> I = model(parameters, dt);
    for (int i = 0; i < 100; i++){
        r1 = (I[i] - real_data[i]);
        result += r1 * r1;
    }
    return result;
}


int main(){
    srand(time(NULL));
    ifstream Data;
    Data.open("..\\..\\data.txt");

    //vector<float>parameters = {2.55, 1.56, 7.65, 0.25, 0.58, 0.001, 0.94, 0.27, 0.5, 3.5, 1, 0.3};

    int j;
    string data;
    for (int i = 0; i < 100; i++){
        getline(Data, data);
        real_data[i] = int(Double(data));
    }    
    Data.close();

    for (int i = 1; i < 100; i++){
        j = int(i / dt);
        if (i % 10 == 0){cout << "\n";}
        cout << floor(real_data[i])<<"   ";
    }

    cout << endl << endl;
    vector<float>parameters = {76.7341, 363.669};
    cout << dist(parameters) << endl;
    vector<float> I = model(parameters, dt);
    for (int i = 1; i < 100; i++){
        j = int(i / dt);
        if (i % 10 == 0){cout << "\n";}
        cout << floor(I[j])<<"   ";
    }


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

    cout << endl << endl;

    vector<float> A(12, 0);
    vector<float> B(12, 12);
    auto time1 = time(NULL);
    vector<float> res = roy(dist, A, B, 0.01, 2, 100, 100, 0.9, 1.5, 1.7);
    cout << "totla time " << time(NULL) - time1 << endl << endl;
    cout << "engame parameters: " << endl;
    for (int i = 0; i < res.size(); i++){cout<< " \t " << res[i] << endl;}
    cout << "f1() = " << dist(res) << endl;

    return 0;
}