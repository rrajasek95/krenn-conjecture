/* Optional exact seven-site stress certificate; no external libraries.
 * cc -O3 -std=c99 seven_site.c -o /tmp/krenn-exterior-seven
 * /tmp/krenn-exterior-seven
 *
 * This target has a product vector in its exterior kernel by construction.
 * The test asks whether the full matching-layer bound is strictly stronger.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

enum { N = 2187, OMIT = 3, D = N - OMIT, P = 101 };

static int mod(int x) { x %= P; return x < 0 ? x + P : x; }
static int inverse(int x) {
    int r = 1, e = P - 2;
    while (e) {
        if (e & 1) r = r * x % P;
        x = x * x % P;
        e >>= 1;
    }
    return r;
}

int main(void) {
    uint16_t *a = calloc((size_t)D * D, sizeof(*a));
    if (!a) return 2;
    int t[N], digits[N][7];
    uint32_t state = UINT32_C(1729);
    for (int i = 0; i < N; ++i) {
        int x = i, zero = 0;
        for (int k = 6; k >= 0; --k) {
            digits[i][k] = x % 3; x /= 3;
            zero |= digits[i][k] == 0;
        }
        state ^= state << 13;
        state ^= state >> 17;
        state ^= state << 5;
        t[i] = zero ? 1 + (int)(state % 100) : 0;
    }
    for (int i = OMIT; i < N; ++i) {
        for (int bits = 0; bits < 128; ++bits) {
            int b = 0, c = 0, sign = 1;
            for (int k = 0; k < 7; ++k) {
                int step = 1 + ((bits >> k) & 1);
                b = 3 * b + (digits[i][k] + step) % 3;
                c = 3 * c + (digits[i][k] + 3 - step) % 3;
                if (step == 2) sign = -sign;
            }
            if (b >= OMIT) a[(size_t)(i - OMIT) * D + b - OMIT] = mod(sign * t[c]);
        }
    }
    int pf = 1;
    for (int k = 0; k < D; k += 2) {
        int partner = k + 1;
        while (partner < D && a[(size_t)k * D + partner] == 0) ++partner;
        if (partner == D) { pf = 0; break; }
        if (partner != k + 1) {
            for (int j = 0; j < D; ++j) {
                uint16_t tmp = a[(size_t)(k + 1) * D + j];
                a[(size_t)(k + 1) * D + j] = a[(size_t)partner * D + j];
                a[(size_t)partner * D + j] = tmp;
            }
            for (int i = 0; i < D; ++i) {
                uint16_t tmp = a[(size_t)i * D + k + 1];
                a[(size_t)i * D + k + 1] = a[(size_t)i * D + partner];
                a[(size_t)i * D + partner] = tmp;
            }
            pf = mod(-pf);
        }
        int pivot = a[(size_t)k * D + k + 1];
        pf = pf * pivot % P;
        int inv = inverse(pivot);
        const uint16_t *r0 = a + (size_t)k * D;
        const uint16_t *r1 = a + (size_t)(k + 1) * D;
        for (int i = k + 2; i < D; ++i) {
            int u = r0[i] * inv % P, v = r1[i] * inv % P;
            for (int j = i + 1; j < D; ++j) {
                int value = mod(a[(size_t)i * D + j] - u * r1[j] + v * r0[j]);
                a[(size_t)i * D + j] = value;
                a[(size_t)j * D + i] = mod(-value);
            }
        }
    }
    printf("{\"sites\":7,\"prime\":101,\"seed\":1729,\"omitted_indices\":[0,1,2],"
           "\"minor_order\":2184,\"pfaffian\":%d,\"determinant\":%d,"
           "\"matching_rank_bound\":2182}\n", pf, pf * pf % P);
    free(a);
    return pf ? 0 : 1;
}
