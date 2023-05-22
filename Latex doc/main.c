float** sir(int size, float beta, float gama, int N, float dt){
    float* S = malloc(size * sizeof(float));
    float* I = malloc(size * sizeof(float));
    float* R = malloc(size * sizeof(float));
    float** answer = malloc(3 * sizeof(float*));
    answer[0] = S; answer[1] = I; answer[2] = R;
    S[0] = N - 1;I[0] = 1;R[0] = 0;answer[0] = 1;
    int step = (int)(1 / dt);float sum = 1;
    for (int i = 0; i < size - 1; i++){
        S[i + 1] = S[i] - beta * S[i] * I[i] * dt / N; 
        I[i + 1] = I[i] + (beta * S[i] * I[i] / N - gama * I[i]) * dt;
        R[i + 1] = R[i] + gama * I[i] * dt;}
    return answer;
}