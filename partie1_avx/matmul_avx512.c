#include <stdio.h>
#include <stdlib.h>
#include <immintrin.h> 

int main() {
    // Test
    __m512 a = _mm512_setzero_ps(); 

    printf("Compilation AVX-512 done ! \n");
    
    
    (void)a; 

    return 0;
}