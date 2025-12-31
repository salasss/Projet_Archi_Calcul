#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <immintrin.h> // AVX-512
#include <math.h>

#define N 512 // Doit être un multiple de 16

void init_matrix(float *M, float value) {
    for (int i = 0; i < N * N; i++) {
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

//V AVX-512
void transpose(float *src, float *dst) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            dst[j * N + i] = src[i * N + j];
        }
    }
}

void matmul_avx512(float *A, float *B, float *C) {
    
    float *B_t = (float*)_mm_malloc(N * N * sizeof(float), 64);
    transpose(B, B_t);

    // 2.  vectCalcul
    for (int i = 0; i < N; i++) {       
        for (int j = 0; j < N; j++) {          
            __m512 vsum = _mm512_setzero_ps();

            // here we see Single Instruction Multiple Data
            for (int k = 0; k < N; k += 16) {
                __m512 va = _mm512_loadu_ps(&A[i * N + k]);
                
                __m512 vb = _mm512_loadu_ps(&B_t[j * N + k]);

                // Fused Multiply-Add  vsum + (va * vb)
                vsum = _mm512_fmadd_ps(va, vb, vsum);
            }

            // sum of 16 elem
            float total = _mm512_reduce_add_ps(vsum);
            
            C[i * N + j] = total;
        }
    }

    _mm_free(B_t);
}

int main() {
    printf("Matrice size: %d x %d\n", N, N);

    float *A = (float*)_mm_malloc(N * N * sizeof(float), 64);
    float *B = (float*)_mm_malloc(N * N * sizeof(float), 64);
    float *C_naive = (float*)_mm_malloc(N * N * sizeof(float), 64);
    float *C_avx = (float*)_mm_malloc(N * N * sizeof(float), 64);

    init_matrix(A, 1.0f);
    init_matrix(B, 2.0f);
    set_zero(C_naive);
    set_zero(C_avx);

    // --- Mesure NAÏF ---
    printf("1. Calcul NAIF...\n");
    clock_t start = clock();
    matmul_naive(A, B, C_naive);
    clock_t end = clock();
    double time_naive = (double)(end - start) / CLOCKS_PER_SEC;
    printf("time: %f s\n", time_naive);

    // --- Mesure AVX-512 ---
    printf("2. Calcul AVX-512...\n");
    start = clock();
    matmul_avx512(A, B, C_avx);
    end = clock();
    double time_avx = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Time: %f s\n", time_avx);

    // --- Comparaison ---
    printf("Accelleration : x%.2f\n", time_naive / time_avx);

    // check
    printf("check C[0]: Naif = %f, AVX = %f\n", C_naive[0], C_avx[0]);
    if (fabs(C_naive[0] - C_avx[0]) < 0.1) {
        printf("ok\n");
    } else {
        printf("ERREUR CALCUL\n");
    }

    _mm_free(A); _mm_free(B); _mm_free(C_naive); _mm_free(C_avx);
    return 0;
}