"""UNAUDITED (W11).  Vectorised fibre-size checker.

Used only to DRIVE the CEGAR loop (it must be fast).  Every verdict that is
finally reported is re-verified by the naive, independent enumeration in
krenn_core.  `selftest()` cross-checks the two on random templates.
"""

import numpy as np

import krenn_core as K

# words as a (6561, 8) int array, in krenn_core.ALL_WORDS order
W = np.array(K.ALL_WORDS, dtype=np.int64)
IS_MIXED = np.array([len(set(w)) > 1 for w in K.ALL_WORDS])

# per-edge, the cell index (0..8) selected by each word
EDGE_CELLIDX = np.zeros((K.NE, len(K.ALL_WORDS)), dtype=np.int64)
for e, (u, v) in enumerate(K.EDGES):
    EDGE_CELLIDX[e] = 3 * W[:, u] + W[:, v]

# per-matching, a 28-bit mask of its edges
MATCH_MASK = np.array([sum(1 << ei for ei in M) for M in K.MATCHINGS],
                      dtype=np.int64)


def block_masks(template):
    """9-bit occupancy mask per edge; bit 3*i+j set iff (i,j) in S_e."""
    return np.array([sum(1 << (3 * i + j) for (i, j) in S) for S in template],
                    dtype=np.int64)


def live_edge_sets(template):
    """28-bit mask L_w per word: which edges are live for that word."""
    bm = block_masks(template)
    L = np.zeros(len(K.ALL_WORDS), dtype=np.int64)
    for e in range(K.NE):
        bit = (bm[e] >> EDGE_CELLIDX[e]) & 1
        L |= bit << e
    return L


def fibre_sizes(template):
    """Array of |fibre(w)| for every word, in krenn_core.ALL_WORDS order."""
    L = live_edge_sets(template)
    cnt = np.zeros(len(K.ALL_WORDS), dtype=np.int32)
    for mm in MATCH_MASK:
        cnt += ((L & mm) == mm)
    return cnt


def singleton_words(template):
    cnt = fibre_sizes(template)
    idx = np.nonzero((cnt == 1) & IS_MIXED)[0]
    return [K.ALL_WORDS[i] for i in idx]


def selftest(trials=40, seed=0):
    import random
    rng = random.Random(seed)
    for t in range(trials):
        T = []
        for e in range(K.NE):
            k = rng.randint(0, 3)
            T.append(frozenset(rng.sample(K.CELLS, k)))
        fast = fibre_sizes(T)
        # naive reference on a random sample of words plus all constants
        idxs = list(rng.sample(range(6561), 60)) + [
            K.ALL_WORDS.index(w) for w in K.CONSTANT_WORDS]
        for i in idxs:
            ref = len(K.fibre(T, K.ALL_WORDS[i]))
            assert ref == fast[i], (t, i, ref, fast[i])
        assert sorted(singleton_words(T)) == sorted(K.singleton_words(T)), t
    return True


if __name__ == "__main__":
    print("fastcheck selftest:", selftest())
