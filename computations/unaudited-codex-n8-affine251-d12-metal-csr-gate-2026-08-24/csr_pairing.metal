#include <metal_stdlib>
using namespace metal;

struct Parameters {
    uint rows;
    uint prime_kind;
};

constant ulong MASK30 = (1ul << 30) - 1ul;
constant uint PRIME_PLUS = 1073741827u;  // 2^30 + 3
constant uint PRIME_MINUS = 1073741789u; // 2^30 - 35

inline uint product_mod(uint left, uint right, uint kind) {
    ulong product = ulong(left) * ulong(right);
    if (kind == 0u) {
        long reduced = long(product & MASK30) - 3l * long(product >> 30);
        if (reduced < 0l) reduced += long(PRIME_PLUS);
        if (reduced < 0l) reduced += long(PRIME_PLUS);
        if (reduced < 0l) reduced += long(PRIME_PLUS);
        if (reduced >= long(PRIME_PLUS)) reduced -= long(PRIME_PLUS);
        return uint(reduced);
    }
    ulong reduced = (product & MASK30) + 35ul * (product >> 30);
    reduced = (reduced & MASK30) + 35ul * (reduced >> 30);
    if (reduced >= ulong(PRIME_MINUS)) reduced -= ulong(PRIME_MINUS);
    if (reduced >= ulong(PRIME_MINUS)) reduced -= ulong(PRIME_MINUS);
    return uint(reduced);
}

kernel void csr_pairing(
    device const uint *row_offsets [[buffer(0)]],
    device const uint *column_indices [[buffer(1)]],
    device const uint *values [[buffer(2)]],
    device const uint *vector [[buffer(3)]],
    device uint *output [[buffer(4)]],
    constant Parameters &parameters [[buffer(5)]],
    uint row [[thread_position_in_grid]]) {
    if (row >= parameters.rows) return;
    uint prime = parameters.prime_kind == 0u ? PRIME_PLUS : PRIME_MINUS;
    uint sum = 0u;
    for (uint edge = row_offsets[row]; edge < row_offsets[row + 1u]; ++edge) {
        uint term = product_mod(values[edge], vector[column_indices[edge]], parameters.prime_kind);
        sum += term;
        if (sum >= prime) sum -= prime;
    }
    output[row] = sum;
}
