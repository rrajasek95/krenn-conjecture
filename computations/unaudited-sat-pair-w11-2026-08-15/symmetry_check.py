"""UNAUDITED (W11).  Verify that the decision problem really is S_8 x S_3
equivariant, BEFORE using isomorphism classes of support graphs.

transport(T, sigma, tau) relabels vertices by sigma and recolours by tau.
The audit of the transported template must agree with the original in:
support, Sigma, number of (SC) failures, number of singleton mixed words,
and the multiset of constant-fibre sizes (permuted by tau).
"""

import random

import krenn_core as K


def transport(T, sigma, tau):
    U = [set() for _ in range(K.NE)]
    for e, (u, v) in enumerate(K.EDGES):
        a, b = sigma[u], sigma[v]
        e2 = K.EIDX[(min(a, b), max(a, b))]
        for (i, j) in T[e]:
            ci, cj = tau[i], tau[j]
            U[e2].add((ci, cj) if a < b else (cj, ci))
    return K.template_from_sets(U)


def check(trials=60, seed=3, kmax=4):
    rng = random.Random(seed)
    for t in range(trials):
        T = K.template_from_sets(
            [set(rng.sample(K.CELLS, rng.randint(0, kmax)))
             for _ in range(K.NE)])
        sigma = list(range(8))
        rng.shuffle(sigma)
        tau = list(range(3))
        rng.shuffle(tau)
        U = transport(T, sigma, tau)
        a, b = K.audit(T), K.audit(U)
        assert a["support"] == b["support"], t
        assert a["sigma"] == b["sigma"], t
        assert len(a["sc_failures"]) == len(b["sc_failures"]), t
        assert a["n_singletons"] == b["n_singletons"], t
        assert ({tau[c]: v for c, v in a["constant_fibre_sizes"].items()}
                == b["constant_fibre_sizes"]), t
        # slotwise, not just in aggregate
        assert (sorted((sigma[p], tau[r]) for (p, r) in a["sc_failures"])
                == sorted(b["sc_failures"])), t
        # transport must send the support graph to its image
        eT = set(e for e in range(K.NE) if T[e])
        eU = set(e for e in range(K.NE) if U[e])
        img = set()
        for e in eT:
            u, v = K.EDGES[e]
            a2, b2 = sigma[u], sigma[v]
            img.add(K.EIDX[(min(a2, b2), max(a2, b2))])
        assert img == eU, t
    return True


if __name__ == "__main__":
    print("S_8 x S_3 equivariance check:", check())
