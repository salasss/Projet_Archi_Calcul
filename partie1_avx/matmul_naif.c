#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <immintrin.h> 

#define N 512 // length of matrix (multi 16 for AVX-512)

// init mat with simple var
void init_matrix(float *M, float value) {
    for (int i = 0; i < N * N; i++) {
            
//avoid overly aggressive compiler opti  value + a small epsilon
        M[i] = value + (float)(i % 100) * 0.001f;
    }
}


void set_zero(float *M) {
    for (int i = 0; i < N * N; i++) {
        M[i] = 0.0f;
    }
}


void matmul_naive(float *A, float *B, float *C) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            for (int k = 0; k < N; k++) {
                C[i * N + j] += A[i * N + k] * B[k * N + j];
            }
        }
    }
}

int main() {
    printf("Matrice size: %d x %d\n", N, N);


    float *A = (float*)_mm_malloc(N * N * sizeof(float), 64);
    float *B = (float*)_mm_malloc(N * N * sizeof(float), 64);
    float *C_naive = (float*)_mm_malloc(N * N * sizeof(float), 64);

    // Init
    init_matrix(A, 1.0f);
    init_matrix(B, 2.0f);
    set_zero(C_naive);

    
    printf("Calcul version naive en cours...\n");
    clock_t start = clock();
    
    matmul_naive(A, B, C_naive);
    
    clock_t end = clock();
    double time_naive = (double)(end - start) / CLOCKS_PER_SEC;

    printf("Temps Naif : %f secondes\n", time_naive);
    printf("Check C[0] : %f (devrait être environ %f)\n", C_naive[0], 2.0f * N); // check

    _mm_free(A);
    _mm_free(B);
    _mm_free(C_naive);

    return 0;
}