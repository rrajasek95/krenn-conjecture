/* UNAUDITED (W11, 2026-08-15).  Independent forward DRUP checker.
 *
 * usage:  rupcheck problem.cnf proof.drup
 *
 * For every lemma L of the proof in order, assert the negation of each of its
 * literals, run unit propagation over the clause database (original clauses
 * plus all previously accepted lemmas) and require a conflict.  That is the
 * RUP test; RUP implies DB |= L, so by induction every lemma is a logical
 * consequence of the original formula.  Deriving the empty clause therefore
 * proves the original formula unsatisfiable.
 *
 * 'd' (deletion) lines are IGNORED.  Keeping deleted clauses only enlarges
 * the database, and every clause in it is a consequence of the original
 * formula, so the implication argument above is unaffected.  (It can only
 * make the check accept proofs a deletion-aware checker would also accept.)
 *
 * Exit status 0 = VERIFIED, 1 = FAILED, 2 = usage/IO error.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { int *lits; int size; } Clause;

static Clause *cls = NULL;
static long ncls = 0, capcls = 0;
static int nvars = 0;

static int **watch = NULL;      /* watch[lit_index] -> array of clause ids  */
static int *watch_n = NULL, *watch_cap = NULL;

static signed char *assign = NULL;   /* 0 unknown, 1 true, -1 false */
static int *trail = NULL;
static int trail_n = 0, qhead = 0;

#define LIDX(l) ((l) > 0 ? 2 * (l) : 2 * (-(l)) + 1)   /* literal -> index */

static void die(const char *m) { fprintf(stderr, "rupcheck: %s\n", m); exit(2); }

static void watch_push(int lit, int c) {
    int i = LIDX(lit);
    if (watch_n[i] == watch_cap[i]) {
        watch_cap[i] = watch_cap[i] ? watch_cap[i] * 2 : 4;
        watch[i] = (int *)realloc(watch[i], sizeof(int) * watch_cap[i]);
        if (!watch[i]) die("oom watch");
    }
    watch[i][watch_n[i]++] = c;
}

static inline signed char val(int l) {
    signed char a = assign[l > 0 ? l : -l];
    return l > 0 ? a : (signed char)(-a);
}

static inline void enqueue(int l) {
    assign[l > 0 ? l : -l] = l > 0 ? 1 : -1;
    trail[trail_n++] = l;
}

/* returns 1 on conflict */
static int propagate(void) {
    while (qhead < trail_n) {
        int p = trail[qhead++];         /* p is true; visit watchers of -p */
        int wi = LIDX(-p);
        int i = 0, j = 0, n = watch_n[wi];
        int *ws = watch[wi];
        while (i < n) {
            int c = ws[i++];
            int *L = cls[c].lits;
            int sz = cls[c].size;
            if (L[0] == -p) { L[0] = L[1]; L[1] = -p; }
            if (val(L[0]) == 1) { ws[j++] = c; continue; }
            int k, found = 0;
            for (k = 2; k < sz; k++)
                if (val(L[k]) != -1) {
                    int t = L[1]; L[1] = L[k]; L[k] = t;
                    watch_push(L[1], c);
                    found = 1; break;
                }
            if (found) continue;
            ws[j++] = c;
            if (val(L[0]) == -1) {           /* conflict */
                while (i < n) ws[j++] = ws[i++];
                watch_n[wi] = j;
                return 1;
            }
            enqueue(L[0]);
        }
        watch_n[wi] = j;
    }
    return 0;
}

static void backtrack(int to) {
    while (trail_n > to) {
        int l = trail[--trail_n];
        assign[l > 0 ? l : -l] = 0;
    }
    qhead = trail_n;
}

/* Add a clause under the current (root-level, permanent) assignment.
 * Non-false literals are moved to the front so that the two watched literals
 * are never both already false.  Returns 1 if the clause is falsified by the
 * current assignment (root conflict), else 0. */
static int add_clause(int *lits, int size) {
    if (ncls == capcls) {
        capcls = capcls ? capcls * 2 : 1024;
        cls = (Clause *)realloc(cls, sizeof(Clause) * capcls);
        if (!cls) die("oom cls");
    }
    int *L = (int *)malloc(sizeof(int) * (size ? size : 1));
    if (!L) die("oom lits");
    memcpy(L, lits, sizeof(int) * size);
    int k = 0;
    for (int i = 0; i < size; i++)
        if (val(L[i]) != -1) { int t = L[k]; L[k] = L[i]; L[i] = t; k++; }
    cls[ncls].lits = L;
    cls[ncls].size = size;
    long id = ncls++;
    if (size == 0) return 1;
    if (k == 0) return 1;                       /* every literal false */
    if (size >= 2) { watch_push(L[0], id); watch_push(L[1], id); }
    if (k == 1 && val(L[0]) == 0) enqueue(L[0]);
    return 0;
}

static int *buf = NULL;
static int bufcap = 0;

static int read_clause(FILE *f, int *out_size, int *is_del) {
    int c, sz = 0, lit;
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
        if (fscanf(f, "%d", &lit) != 1) return sz ? -1 : 0;
        if (lit == 0) break;
        if (sz == bufcap) {
            bufcap = bufcap ? bufcap * 2 : 64;
            buf = (int *)realloc(buf, sizeof(int) * bufcap);
            if (!buf) die("oom buf");
        }
        buf[sz++] = lit;
        int v = lit > 0 ? lit : -lit;
        if (v > nvars) nvars = v;
    }
    *out_size = sz;
    return 1;
}

static void grow_to_nvars(int want) {
    static int cap = 0;
    if (want + 1 <= cap) return;
    int newcap = (want + 1) * 2;
    assign = (signed char *)realloc(assign, newcap);
    trail = (int *)realloc(trail, sizeof(int) * newcap);
    watch = (int **)realloc(watch, sizeof(int *) * 2 * newcap);
    watch_n = (int *)realloc(watch_n, sizeof(int) * 2 * newcap);
    watch_cap = (int *)realloc(watch_cap, sizeof(int) * 2 * newcap);
    if (!assign || !trail || !watch || !watch_n || !watch_cap) die("oom grow");
    memset(assign + cap, 0, newcap - cap);
    memset(watch + 2 * cap, 0, sizeof(int *) * 2 * (newcap - cap));
    memset(watch_n + 2 * cap, 0, sizeof(int) * 2 * (newcap - cap));
    memset(watch_cap + 2 * cap, 0, sizeof(int) * 2 * (newcap - cap));
    cap = newcap;
}

int main(int argc, char **argv) {
    if (argc != 3) die("usage: rupcheck problem.cnf proof.drup");
    FILE *f = fopen(argv[1], "r");
    if (!f) die("cannot open cnf");

    /* pass 1: find nvars from the header if present, else grow lazily */
    int maxv = 0, nc = 0;
    { char line[256];
      long pos = ftell(f);
      while (fgets(line, sizeof line, f)) {
          if (line[0] == 'p') { sscanf(line, "p cnf %d %d", &maxv, &nc); break; }
          if (line[0] != 'c') break;
      }
      fseek(f, pos, SEEK_SET);
    }
    grow_to_nvars(maxv > 0 ? maxv + 8 : 1024);

    int sz, del;
    long norig = 0;
    int r;
    while ((r = read_clause(f, &sz, &del)) == 1) {
        grow_to_nvars(nvars + 8);
        int conf = add_clause(buf, sz);
        norig++;
        if (conf) { printf("VERIFIED (formula falsified at root)\n"); return 0; }
    }
    if (r == -1) die("malformed cnf");
    fclose(f);

    if (propagate()) { printf("VERIFIED (formula UP-refutes at level 0)\n"); return 0; }

    f = fopen(argv[2], "r");
    if (!f) die("cannot open proof");
    long nlem = 0, nskip = 0;
    while ((r = read_clause(f, &sz, &del)) == 1) {
        if (del) { nskip++; continue; }
        grow_to_nvars(nvars + 8);
        int base = trail_n;
        int conflict = 0;
        for (int i = 0; i < sz; i++) {
            signed char v = val(buf[i]);
            if (v == 1) { conflict = 0; goto assigned; }   /* lemma satisfied */
            if (v == 0) enqueue(-buf[i]);
        }
        conflict = propagate();
    assigned:
        if (!conflict && sz > 0) {
            /* a literal was already true at level 0: the lemma is implied */
            int sat = 0;
            for (int i = 0; i < sz; i++) if (val(buf[i]) == 1) sat = 1;
            if (!sat) {
                printf("FAILED: lemma %ld is not RUP\n", nlem + 1);
                return 1;
            }
        }
        if (!conflict && sz == 0) {
            printf("FAILED: empty clause is not RUP\n");
            return 1;
        }
        backtrack(base);
        nlem++;
        if (add_clause(buf, sz)) {
            printf("VERIFIED  original=%ld lemmas=%ld deletions_ignored=%ld\n",
                   norig, nlem, nskip);
            return 0;
        }
        if (propagate()) {
            printf("VERIFIED  original=%ld lemmas=%ld deletions_ignored=%ld "
                   "(root conflict)\n", norig, nlem, nskip);
            return 0;
        }
    }
    printf("FAILED: proof ended without deriving the empty clause "
           "(lemmas=%ld)\n", nlem);
    return 1;
}
