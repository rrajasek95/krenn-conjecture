#include <metal_stdlib>
using namespace metal;

struct Parameters {
    uint output_entities;
    uint width;
    uint prime_kind;
    uint reserved;
};

constant ulong MASK30 = (1ul << 30) - 1ul;
constant uint PRIME_PLUS = 1073741827u;
constant uint PRIME_MINUS = 1073741789u;

inline uint coefficient_residue(int coefficient, uint prime) {
    return coefficient >= 0 ? uint(coefficient) : prime - uint(-long(coefficient));
}

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

kernel void block_spmv(
    device const uint *pointers [[buffer(0)]],
    device const uint *indices [[buffer(1)]],
    device const int *coefficients [[buffer(2)]],
    device const uint *input [[buffer(3)]],
    device uint *output [[buffer(4)]],
    constant Parameters &parameters [[buffer(5)]],
    uint gid [[thread_position_in_grid]]) {
    ulong total_outputs = ulong(parameters.output_entities) * ulong(parameters.width);
    if (ulong(gid) >= total_outputs) return;
    uint entity = gid / parameters.width;
    uint lane = gid - entity * parameters.width;
    uint prime = parameters.prime_kind == 0u ? PRIME_PLUS : PRIME_MINUS;
    uint sum = 0u;
    for (uint edge = pointers[entity]; edge < pointers[entity + 1u]; ++edge) {
        uint value = coefficient_residue(coefficients[edge], prime);
        uint term = product_mod(value, input[indices[edge] * parameters.width + lane],
                                parameters.prime_kind);
        sum += term;
        if (sum >= prime) sum -= prime;
    }
    output[gid] = sum;
}

