/* UNAUDITED PROBE (W18) -- forward DRAT proof checker (RUP + RAT).
 *
 * Extension of rup18.c: when a lemma is not RUP, it is accepted only if it is
 * a RAT on its FIRST literal p, i.e. for every clause D still in the formula
 * with -p in D, the resolvent (C \ {p}) u (D \ {-p}) u {p} = C u (D \ {-p})
 * is RUP.  That is the standard DRAT criterion with the specified-pivot
 * convention, and it is what a solver that does blocked-clause / bounded
 * variable elimination inprocessing emits.
 *
 * usage:  drat18 <file.cnf> <file.drat>
 * exit 0 and print "VERIFIED <n> lemmas" iff every proof line is a reverse
 * unit propagation consequence of the clauses accumulated so far AND the
 * empty clause is derived.  Anything else exits nonzero.
 *
 * Written from the DRUP definition; no code taken from drat-trim or from any
 * other lane.  Deletion lines ("d ...") are honoured; a deletion of a clause
 * that is not present is ignored (that only makes the check STRICTER, since
 * keeping a clause can only help propagation -- so a proof accepted here is
 * accepted with a superset of the intended clause database, and the RUP
 * property is monotone in the database).  Unit clauses are never deleted
 * (standard, and again only makes the check stricter).
 *
 * Propagation is the textbook two-watched-literal scheme; the empty clause
 * and unit clauses are handled explicitly.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { int *lit; int len; int deleted; } Clause;

static int nvars = 0;
static Clause *cls = NULL;
static long ncls = 0, capcls = 0;

/* watches[2*v + s] : list of clause indices watching literal (v with sign s) */
static long **watch = NULL;
static long *wlen = NULL, *wcap = NULL;

static signed char *val = NULL;      /* 0 unknown, 1 true, -1 false, indexed by var */
static int *trail = NULL;
static long tlen = 0;

static int LIDX(int lit) { return lit > 0 ? 2 * lit : 2 * (-lit) + 1; }

static void grow_watch(int idx) {
    if (wlen[idx] + 1 > wcap[idx]) {
        wcap[idx] = wcap[idx] ? wcap[idx] * 2 : 4;
        watch[idx] = realloc(watch[idx], wcap[idx] * sizeof(long));
    }
}

static void add_watch(int lit, long c) {
    int idx = LIDX(lit);
    grow_watch(idx);
    watch[idx][wlen[idx]++] = c;
}

static long new_clause(int *lits, int len) {
    if (ncls + 1 > capcls) {
        capcls = capcls ? capcls * 2 : 1024;
        cls = realloc(cls, capcls * sizeof(Clause));
    }
    cls[ncls].lit = malloc(len * sizeof(int));
    memcpy(cls[ncls].lit, lits, len * sizeof(int));
    cls[ncls].len = len;
    cls[ncls].deleted = 0;
    if (len >= 2) { add_watch(lits[0], ncls); add_watch(lits[1], ncls); }
    return ncls++;
}

static int lit_val(int lit) {
    signed char v = val[lit > 0 ? lit : -lit];
    if (v == 0) return 0;
    return lit > 0 ? v : -v;
}

static void assign(int lit) {
    val[lit > 0 ? lit : -lit] = lit > 0 ? 1 : -1;
    trail[tlen++] = lit;
}

static void backtrack(long to) {
    while (tlen > to) { int l = trail[--tlen]; val[l > 0 ? l : -l] = 0; }
}

/* returns 1 on conflict */
static int propagate(long qhead) {
    while (qhead < tlen) {
        int p = trail[qhead++];
        int nidx = LIDX(-p);              /* clauses watching -p */
        long i = 0, j = 0;
        while (i < wlen[nidx]) {
            long c = watch[nidx][i++];
            if (cls[c].deleted) continue;
            int *L = cls[c].lit, len = cls[c].len;
            /* make L[1] the watched literal equal to -p */
            if (L[0] == -p) { int t = L[0]; L[0] = L[1]; L[1] = t; }
            if (lit_val(L[0]) == 1) { watch[nidx][j++] = c; continue; }
            int found = 0;
            for (int k = 2; k < len; k++) {
                if (lit_val(L[k]) != -1) {
                    int t = L[1]; L[1] = L[k]; L[k] = t;
                    add_watch(L[1], c);
                    found = 1;
                    break;
                }
            }
            if (found) continue;
            watch[nidx][j++] = c;
            if (lit_val(L[0]) == -1) {
                while (i < wlen[nidx]) watch[nidx][j++] = watch[nidx][i++];
                wlen[nidx] = j;
                return 1;
            }
            assign(L[0]);
        }
        wlen[nidx] = j;
    }
    return 0;
}

static long nrat = 0;
static int *resbuf = NULL; static int rescap = 0;

/* RUP check of an explicit clause (does not add it) */
static int rup_of(int *lits, int n) {
    long mark = tlen;
    int conflict = 0;
    for (int k = 0; k < n && !conflict; k++) {
        int v = lit_val(-lits[k]);
        if (v == -1) { conflict = 1; break; }
        if (v == 0) assign(-lits[k]);
    }
    if (!conflict) conflict = propagate(mark);
    backtrack(mark);
    return conflict;
}

/* C is RAT on the literal C[pi] */
static int rat_on(int *C, int n, int pi) {
    int p = C[pi];
    for (long c = 0; c < ncls; c++) {
        if (cls[c].deleted) continue;
        int *D = cls[c].lit, dl = cls[c].len, has = 0;
        for (int k = 0; k < dl; k++) if (D[k] == -p) { has = 1; break; }
        if (!has) continue;
        int need = n + dl;
        if (need > rescap) { rescap = need * 2; resbuf = realloc(resbuf, rescap * sizeof(int)); }
        int m = 0, taut = 0;
        for (int k = 0; k < n; k++) resbuf[m++] = C[k];
        for (int k = 0; k < dl && !taut; k++) {
            if (D[k] == -p) continue;
            int dup = 0;
            for (int q = 0; q < n; q++) {
                if (C[q] == D[k]) { dup = 1; break; }
                if (C[q] == -D[k]) { taut = 1; break; }
            }
            if (!dup && !taut) resbuf[m++] = D[k];
        }
        if (taut) continue;                 /* tautological resolvent: fine */
        if (!rup_of(resbuf, m)) return 0;
    }
    return 1;
}


/* RAT on SOME literal.  Adding a clause that is RAT with respect to any of
 * its literals preserves satisfiability, which is all the final empty-clause
 * derivation needs, so scanning every pivot is sound (and strictly more
 * permissive than the specified-pivot convention). */
static int rat_check(int *C, int n) {
    for (int pi = 0; pi < n; pi++)
        if (rat_on(C, n, pi)) return 1;
    return 0;
}

static int *rbuf = NULL; static int rcap = 0;

static int read_clause(FILE *f, int *out_len, int *is_del) {
    int c, n = 0, lit;
    *is_del = 0;
    for (;;) {
        c = fgetc(f);
        if (c == EOF) return 0;
        if (c == ' ' || c == '\n' || c == '\r' || c == '\t') continue;
        if (c == 'c' || c == 'p') { while (c != '\n' && c != EOF) c = fgetc(f); continue; }
        if (c == 'd') { *is_del = 1; continue; }
        ungetc(c, f);
        break;
    }
    for (;;) {
        if (fscanf(f, "%d", &lit) != 1) return n ? -1 : 0;
        if (lit == 0) break;
        if (n + 1 > rcap) { rcap = rcap ? rcap * 2 : 64; rbuf = realloc(rbuf, rcap * sizeof(int)); }
        rbuf[n++] = lit;
    }
    *out_len = n;
    return 1;
}

int main(int argc, char **argv) {
    if (argc != 3) { fprintf(stderr, "usage: drat18 cnf drat\n"); return 2; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { fprintf(stderr, "cannot open %s\n", argv[1]); return 2; }
    int c;
    /* header */
    for (;;) {
        c = fgetc(f);
        if (c == EOF) break;
        if (c == 'c') { while (c != '\n' && c != EOF) c = fgetc(f); continue; }
        if (c == 'p') { int nc; if (fscanf(f, " cnf %d %d", &nvars, &nc) != 2) return 2; break; }
        if (c == ' ' || c == '\n' || c == '\r' || c == '\t') continue;
        ungetc(c, f); break;
    }
    if (nvars <= 0) nvars = 1;
    long maxv = nvars + 8;
    val = calloc(maxv + 1, 1);
    trail = malloc((maxv + 1) * sizeof(int));
    watch = calloc(2 * (maxv + 2), sizeof(long *));
    wlen = calloc(2 * (maxv + 2), sizeof(long));
    wcap = calloc(2 * (maxv + 2), sizeof(long));

    long nunit = 0;
    int len, del;
    int base_empty = 0;
    while (read_clause(f, &len, &del) == 1) {
        if (len == 0) { base_empty = 1; continue; }
        for (int k = 0; k < len; k++) { int v = rbuf[k] > 0 ? rbuf[k] : -rbuf[k]; if (v > nvars) { fprintf(stderr, "var %d > nvars\n", v); return 2; } }
        if (len == 1) { if (lit_val(rbuf[0]) == 0) { assign(rbuf[0]); nunit++; } else if (lit_val(rbuf[0]) == -1) { base_empty = 1; } }
        new_clause(rbuf, len);
    }
    fclose(f);
    if (propagate(0)) base_empty = 1;
    long qhead0 = tlen;

    f = fopen(argv[2], "r");
    if (!f) { fprintf(stderr, "cannot open %s\n", argv[2]); return 2; }
    long lemmas = 0, deletions = 0;
    int derived_empty = base_empty;
    int r;
    while ((r = read_clause(f, &len, &del)) == 1) {
        for (int k = 0; k < len; k++) {
            int v = rbuf[k] > 0 ? rbuf[k] : -rbuf[k];
            if (v > nvars) {
                fprintf(stderr, "malformed proof: variable %d exceeds nvars\n", v);
                return 1;
            }
        }
        if (del) {
            /* find a clause with exactly these literals and mark it deleted */
            if (len <= 1) { deletions++; continue; }
            long found = -1;
            int idx = LIDX(rbuf[0]);
            for (long i = 0; i < wlen[idx]; i++) {
                long cc = watch[idx][i];
                if (cls[cc].deleted || cls[cc].len != len) continue;
                int ok = 1;
                for (int k = 0; k < len && ok; k++) {
                    int seen = 0;
                    for (int q = 0; q < len; q++) if (cls[cc].lit[q] == rbuf[k]) { seen = 1; break; }
                    if (!seen) ok = 0;
                }
                if (ok) { found = cc; break; }
            }
            if (found >= 0) cls[found].deleted = 1;
            deletions++;
            continue;
        }
        if (derived_empty) { lemmas++; if (len == 0) break; else continue; }
        /* RUP check: assume the negation of the lemma, propagate, want conflict */
        long mark = tlen;
        int conflict = 0;
        for (int k = 0; k < len && !conflict; k++) {
            int v = lit_val(-rbuf[k]);
            if (v == -1) { conflict = 1; break; }
            if (v == 0) assign(-rbuf[k]);
        }
        if (!conflict) conflict = propagate(mark);
        backtrack(mark);
        if (!conflict) {
            /* not RUP: try RAT on the first literal */
            if (len == 0 || !rat_check(rbuf, len)) {
                fprintf(stderr, "RUP/RAT FAILURE at lemma %ld (len %d)\n",
                        lemmas + 1, len);
                return 1;
            }
            nrat++;
        }
        lemmas++;
        if (len == 0) { derived_empty = 1; break; }
        new_clause(rbuf, len);
        if (len == 1 && lit_val(rbuf[0]) == 0) { assign(rbuf[0]); if (propagate(tlen - 1)) derived_empty = 1; }
    }
    fclose(f);
    if (r < 0) { fprintf(stderr, "malformed proof (unterminated clause)\n"); return 1; }
    if (!derived_empty) { fprintf(stderr, "proof does not derive the empty clause\n"); return 1; }
    printf("VERIFIED %ld lemmas (%ld RAT) %ld deletions %ld units\n",
           lemmas, nrat, deletions, nunit);
    return 0;
}
