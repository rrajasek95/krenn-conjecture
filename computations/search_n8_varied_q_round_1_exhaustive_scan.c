/* Independent exhaustive scan for round 1 of the four-extra-cell varied-q
 * search at the fixed polarized seed (see
 * search_n8_varied_q_round_1_census.py for the region).
 *
 * The scan re-derives every debt vector from the raw cell data and walks
 * all C(243,4) = 141,722,460 quadruples of outside-support cells.  For each
 * quadruple it decides two support-level questions:
 *
 * 1. polarized: can z*(q + sum t_i e_i)^[3] = Delta_{8,3} hold with all
 *    t_i nonzero?  Laurent monomials are the fourteen masks t^S, |S|<=3;
 *    every debt coefficient is one (asserted while building), so a word hit
 *    by exactly one mask kills the quadruple, no hit words at all makes it
 *    identically compatible, and everything else is a support survivor.
 *
 * 2. aggregate: can (q + sum t_i e_i)^[4] = Delta_{8,3} hold with all t_i
 *    nonzero?  The base contributes q^[4] = e_11000000 + e_22212111, so
 *    both padding words need a tagged hit, all three pure words need a
 *    tagged hit, and every other hit word needs at least two distinct
 *    Laurent masks t^S, |S|<=4 (a single mask c*t^S never vanishes on the
 *    torus).
 *
 * Survivor quadruples of either census are written to <outdir> for exact
 * re-verification and Groebner follow-up in Python; the class counts are
 * printed for comparison with the constructive census.  Compile with
 *   cc -O2 -o scan search_n8_varied_q_round_1_exhaustive_scan.c
 * and run  scan <outdir> <i_start> <i_end>  (outer-loop slice on the first
 * index; slices are merged by the driver).
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static const int BASEQ[9][4] = {
    {2, 3, 0, 0}, {4, 5, 0, 0}, {6, 7, 0, 0},
    {0, 1, 1, 1}, {3, 6, 1, 1}, {5, 7, 1, 1},
    {0, 2, 2, 2}, {1, 4, 2, 2}, {5, 6, 2, 2},
};
static const int ZCELLS[3][4] = {{0, 1, 0, 0}, {2, 4, 1, 1}, {3, 7, 2, 2}};

static int p3[8];
static int exl[243], exr[243], exlc[243], exrc[243];
static int exmask[243], exwinc[243];
static int bqmask[9], bqwinc[9];
static int zmask[3], zwinc[3];

static int pure_word[3], pad_word[2];

/* polarized debts */
static int psingle_w[243][2], psingle_n[243];
static int16_t *pcross;                     /* 243*243, word or -1 */

/* aggregate debts, flattened variable-length lists of (word, mult) */
static int asingle_off[244];
static int32_t *asingle_w;
static int across_off[29404];
static int32_t *across_w;
static int pair_slot[243][243];

#define MAXROW 96

/* Distinct-monomial bit layout over the quadruple positions {0,1,2,3}:
 * bits 0..3   single t_a
 * bits 4..9   cross  t_a*t_b in order (0,1),(0,2),(0,3),(1,2),(1,3),(2,3)
 * bits 10..13 triple t_a*t_b*t_c in order (0,1,2),(0,1,3),(0,2,3),(1,2,3)
 * bit  14     quadruple t_1*t_2*t_3*t_4 (aggregate census only)
 */
static const int CROSS_BIT[4][4] = {
    {-1, 4, 5, 6}, {4, -1, 7, 8}, {5, 7, -1, 9}, {6, 8, 9, -1},
};
static const int TRIPLE_BIT_BASE = 10;      /* triple (0,1,2) of the prefix */
static const int TRIPLE_BIT_WITH_L[3][3] = {/* triple (a,b,l) by prefix a<b */
    {-1, 11, 12}, {11, -1, 13}, {12, 13, -1},
};
static const int QUAD_BIT = 14;

static long long pol_compat = 0, pol_reject = 0, pol_surv = 0;
static long long agg_reject = 0, agg_surv = 0;

static int is_word_special(int w)
{
    if (w == pure_word[0] || w == pure_word[1] || w == pure_word[2]) return 1;
    if (w == pad_word[0] || w == pad_word[1]) return 2;
    return 0;
}

static void fail(const char *message)
{
    fprintf(stderr, "FATAL: %s\n", message);
    exit(1);
}

typedef struct { int n; int w[MAXROW]; uint32_t m[MAXROW]; } Row;

static inline void row_add(Row *row, int word, uint32_t mask)
{
    for (int index = 0; index < row->n; index++) {
        if (row->w[index] == word) { row->m[index] |= mask; return; }
    }
    if (row->n >= MAXROW) fail("row overflow");
    row->w[row->n] = word;
    row->m[row->n] = mask;
    row->n++;
}

int main(int argc, char **argv)
{
    if (argc != 4) fail("usage: scan <outdir> <i_start> <i_end>");
    const char *outdir = argv[1];
    int i_start = atoi(argv[2]), i_end = atoi(argv[3]);

    p3[7] = 1;
    for (int site = 6; site >= 0; site--) p3[site] = 3 * p3[site + 1];

    /* enumerate the 252 cells in the census order and drop supp(q) */
    int count = 0;
    for (int left = 0; left < 8; left++)
        for (int right = left + 1; right < 8; right++)
            for (int lc = 0; lc < 3; lc++)
                for (int rc = 0; rc < 3; rc++) {
                    int is_base = 0;
                    for (int b = 0; b < 9; b++)
                        if (BASEQ[b][0] == left && BASEQ[b][1] == right &&
                            BASEQ[b][2] == lc && BASEQ[b][3] == rc) is_base = 1;
                    if (is_base) continue;
                    exl[count] = left; exr[count] = right;
                    exlc[count] = lc; exrc[count] = rc;
                    exmask[count] = (1 << left) | (1 << right);
                    exwinc[count] = lc * p3[left] + rc * p3[right];
                    count++;
                }
    if (count != 243) fail("extras count");
    for (int b = 0; b < 9; b++) {
        bqmask[b] = (1 << BASEQ[b][0]) | (1 << BASEQ[b][1]);
        bqwinc[b] = BASEQ[b][2] * p3[BASEQ[b][0]] + BASEQ[b][3] * p3[BASEQ[b][1]];
    }
    for (int zi = 0; zi < 3; zi++) {
        zmask[zi] = (1 << ZCELLS[zi][0]) | (1 << ZCELLS[zi][1]);
        zwinc[zi] = ZCELLS[zi][2] * p3[ZCELLS[zi][0]] + ZCELLS[zi][3] * p3[ZCELLS[zi][1]];
    }
    for (int colour = 0; colour < 3; colour++) {
        int word = 0;
        for (int site = 0; site < 8; site++) word += colour * p3[site];
        pure_word[colour] = word;
    }
    pad_word[0] = p3[0] + p3[1];                                    /* 11000000 */
    pad_word[1] = 2 * (p3[0] + p3[1] + p3[2] + p3[4]) + p3[3] + p3[5] + p3[6] + p3[7];

    /* polarized single debts: z * e * q^[2] */
    for (int e = 0; e < 243; e++) {
        psingle_n[e] = 0;
        for (int zi = 0; zi < 3; zi++) {
            if (zmask[zi] & exmask[e]) continue;
            for (int b1 = 0; b1 < 9; b1++) {
                int m1 = zmask[zi] | exmask[e] | bqmask[b1];
                if (m1 != (zmask[zi] | exmask[e]) + bqmask[b1]) continue;
                for (int b2 = b1 + 1; b2 < 9; b2++) {
                    if (m1 & bqmask[b2]) continue;
                    if (psingle_n[e] >= 2) fail("polarized single support");
                    psingle_w[e][psingle_n[e]++] =
                        zwinc[zi] + exwinc[e] + bqwinc[b1] + bqwinc[b2];
                }
            }
        }
    }

    /* polarized cross debts: z * e * f * q */
    pcross = malloc(sizeof(int16_t) * 243 * 243);
    for (int e = 0; e < 243; e++)
        for (int f = 0; f < 243; f++) pcross[e * 243 + f] = -1;
    for (int e = 0; e < 243; e++)
        for (int f = e + 1; f < 243; f++) {
            if (exmask[e] & exmask[f]) continue;
            int pair_mask = exmask[e] | exmask[f], hits = 0, word = -1;
            for (int zi = 0; zi < 3; zi++) {
                if (zmask[zi] & pair_mask) continue;
                for (int b = 0; b < 9; b++) {
                    if (bqmask[b] & (pair_mask | zmask[zi])) continue;
                    hits++;
                    word = zwinc[zi] + exwinc[e] + exwinc[f] + bqwinc[b];
                }
            }
            if (hits > 1) fail("polarized cross support");
            if (hits == 1) {
                pcross[e * 243 + f] = (int16_t)word;
                pcross[f * 243 + e] = (int16_t)word;
            }
        }

    /* aggregate single debts: e * q^[3] */
    int32_t scratch[4096];
    int total = 0;
    asingle_w = malloc(sizeof(int32_t) * 243 * 64);
    for (int e = 0; e < 243; e++) {
        asingle_off[e] = total;
        int n = 0;
        for (int b1 = 0; b1 < 9; b1++) {
            if (bqmask[b1] & exmask[e]) continue;
            for (int b2 = b1 + 1; b2 < 9; b2++) {
                int m2 = exmask[e] | bqmask[b1];
                if (m2 & bqmask[b2]) continue;
                for (int b3 = b2 + 1; b3 < 9; b3++) {
                    if ((m2 | bqmask[b2]) & bqmask[b3]) continue;
                    scratch[n++] = exwinc[e] + bqwinc[b1] + bqwinc[b2] + bqwinc[b3];
                }
            }
        }
        for (int a = 0; a < n; a++) asingle_w[total++] = scratch[a];
    }
    asingle_off[243] = total;

    /* aggregate cross debts: e * f * q^[2] */
    across_w = malloc(sizeof(int32_t) * 29403 * 32);
    total = 0;
    int slot = 0;
    for (int e = 0; e < 243; e++)
        for (int f = e + 1; f < 243; f++) {
            pair_slot[e][f] = slot;
            across_off[slot] = total;
            slot++;
            if (!(exmask[e] & exmask[f])) {
                int pair_mask = exmask[e] | exmask[f];
                for (int b1 = 0; b1 < 9; b1++) {
                    if (bqmask[b1] & pair_mask) continue;
                    for (int b2 = b1 + 1; b2 < 9; b2++) {
                        if ((pair_mask | bqmask[b1]) & bqmask[b2]) continue;
                        across_w[total++] =
                            exwinc[e] + exwinc[f] + bqwinc[b1] + bqwinc[b2];
                    }
                }
            }
        }
    across_off[slot] = total;

    char path[1024];
    snprintf(path, sizeof path, "%s/pol_survivors_%03d_%03d.txt", outdir, i_start, i_end);
    FILE *pol_out = fopen(path, "w");
    snprintf(path, sizeof path, "%s/agg_survivors_%03d_%03d.txt", outdir, i_start, i_end);
    FILE *agg_out = fopen(path, "w");
    if (!pol_out || !agg_out) fail("cannot open output files");

    Row pol_row, agg_row, pol_base, agg_base;
    for (int i = i_start; i < i_end; i++) {
        for (int j = i + 1; j < 243; j++) {
            for (int k = j + 1; k < 243; k++) {
                /* entries shared by every quadruple (i,j,k,*) */
                pol_base.n = 0;
                agg_base.n = 0;
                const int trip[3] = {i, j, k};
                for (int a = 0; a < 3; a++) {
                    int cell = trip[a];
                    uint32_t mask = 1u << a;
                    for (int s = 0; s < psingle_n[cell]; s++)
                        row_add(&pol_base, psingle_w[cell][s], mask);
                    for (int s = asingle_off[cell]; s < asingle_off[cell + 1]; s++)
                        row_add(&agg_base, asingle_w[s], mask);
                }
                for (int a = 0; a < 3; a++)
                    for (int b = a + 1; b < 3; b++) {
                        uint32_t mask = 1u << CROSS_BIT[a][b];
                        int word = pcross[trip[a] * 243 + trip[b]];
                        if (word >= 0) row_add(&pol_base, word, mask);
                        int sl = pair_slot[trip[a]][trip[b]];
                        for (int s = across_off[sl]; s < across_off[sl + 1]; s++)
                            row_add(&agg_base, across_w[s], mask);
                    }
                int mask_ijk = exmask[i] | exmask[j] | exmask[k];
                int winc_ijk = exwinc[i] + exwinc[j] + exwinc[k];
                int disjoint_ijk =
                    !(exmask[i] & exmask[j]) &&
                    !((exmask[i] | exmask[j]) & exmask[k]);
                if (disjoint_ijk) {
                    for (int zi = 0; zi < 3; zi++)
                        if (!(zmask[zi] & mask_ijk))
                            row_add(&pol_base, zwinc[zi] + winc_ijk,
                                    1u << TRIPLE_BIT_BASE);
                    for (int b = 0; b < 9; b++)
                        if (!(bqmask[b] & mask_ijk))
                            row_add(&agg_base, bqwinc[b] + winc_ijk,
                                    1u << TRIPLE_BIT_BASE);
                }

                for (int l = k + 1; l < 243; l++) {
                    pol_row = pol_base;
                    agg_row = agg_base;
                    for (int s = 0; s < psingle_n[l]; s++)
                        row_add(&pol_row, psingle_w[l][s], 1u << 3);
                    for (int s = asingle_off[l]; s < asingle_off[l + 1]; s++)
                        row_add(&agg_row, asingle_w[s], 1u << 3);
                    for (int a = 0; a < 3; a++) {
                        uint32_t mask = 1u << CROSS_BIT[a][3];
                        int word = pcross[trip[a] * 243 + l];
                        if (word >= 0) row_add(&pol_row, word, mask);
                        int e = trip[a] < l ? trip[a] : l;
                        int f = trip[a] < l ? l : trip[a];
                        int sl = pair_slot[e][f];
                        for (int s = across_off[sl]; s < across_off[sl + 1]; s++)
                            row_add(&agg_row, across_w[s], mask);
                    }
                    for (int a = 0; a < 3; a++)
                        for (int b = a + 1; b < 3; b++) {
                            int mask_abl = exmask[trip[a]] | exmask[trip[b]] | exmask[l];
                            if (exmask[trip[a]] & exmask[trip[b]]) continue;
                            if ((exmask[trip[a]] | exmask[trip[b]]) & exmask[l]) continue;
                            uint32_t mask = 1u << TRIPLE_BIT_WITH_L[a][b];
                            int winc = exwinc[trip[a]] + exwinc[trip[b]] + exwinc[l];
                            for (int zi = 0; zi < 3; zi++)
                                if (!(zmask[zi] & mask_abl))
                                    row_add(&pol_row, zwinc[zi] + winc, mask);
                            for (int b2 = 0; b2 < 9; b2++)
                                if (!(bqmask[b2] & mask_abl))
                                    row_add(&agg_row, bqwinc[b2] + winc, mask);
                        }
                    if (disjoint_ijk && !(mask_ijk & exmask[l]))
                        row_add(&agg_row, winc_ijk + exwinc[l], 1u << QUAD_BIT);

                    /* polarized classification */
                    if (pol_row.n == 0) {
                        pol_compat++;
                    } else {
                        int singleton = 0;
                        for (int s = 0; s < pol_row.n; s++) {
                            uint32_t m = pol_row.m[s];
                            if (!(m & (m - 1))) { singleton = 1; break; }
                        }
                        if (singleton) pol_reject++;
                        else {
                            pol_surv++;
                            fprintf(pol_out, "%d %d %d %d\n", i, j, k, l);
                        }
                    }

                    /* aggregate classification */
                    int pure_hit[3] = {0, 0, 0}, pad_hit[2] = {0, 0}, bad = 0;
                    for (int s = 0; s < agg_row.n && !bad; s++) {
                        int word = agg_row.w[s];
                        uint32_t m = agg_row.m[s];
                        if (word == pure_word[0]) pure_hit[0] = 1;
                        else if (word == pure_word[1]) pure_hit[1] = 1;
                        else if (word == pure_word[2]) pure_hit[2] = 1;
                        else if (word == pad_word[0]) pad_hit[0] = 1;
                        else if (word == pad_word[1]) pad_hit[1] = 1;
                        else if (!(m & (m - 1))) bad = 1;
                    }
                    if (!bad && pure_hit[0] && pure_hit[1] && pure_hit[2] &&
                        pad_hit[0] && pad_hit[1]) {
                        agg_surv++;
                        fprintf(agg_out, "%d %d %d %d\n", i, j, k, l);
                    } else {
                        agg_reject++;
                    }
                }
            }
        }
    }
    fclose(pol_out);
    fclose(agg_out);
    printf("slice %d %d polarized compatible %lld reject %lld survivors %lld\n",
           i_start, i_end, pol_compat, pol_reject, pol_surv);
    printf("slice %d %d aggregate reject %lld survivors %lld\n",
           i_start, i_end, agg_reject, agg_surv);
    return 0;
}
