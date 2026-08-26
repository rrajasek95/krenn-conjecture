"""UNAUDITED (W11).  Unit tests / mutation controls for the encoding.

The decisive test (`test_word_encoding`) pins all 252 template variables to a
concrete template and asks whether the word constraints are satisfiable.  The
CNF must be SAT exactly when the naive enumeration in krenn_core says the
template has no singleton mixed word.  Random templates, planted-UNSAT
templates (a cell deleted so a singleton appears) and planted-SAT templates
are all exercised.
"""

import random
import sys

from pysat.solvers import Cadical195

import krenn_core as K
import fastcheck as F
import sat_decide as S


def pin(enc, T):
    return [[enc.x(e, c)] if c in T[e] else [-enc.x(e, c)]
            for e in range(K.NE) for c in K.CELLS]


def word_cnf_sat(T, words):
    """SAT iff the encoding of `words` accepts template T."""
    enc = S.Encoder(m=K.support_size(T), derived=False)
    body = []
    for w in words:
        enc.add_word(w, sink=body)
    solver = Cadical195(bootstrap_with=body + pin(enc, T))
    r = solver.solve()
    solver.delete()
    return r


def cube_template():
    T = [set() for _ in range(K.NE)]
    for u in range(8):
        for b in range(3):
            v = u ^ (1 << b)
            if u < v:
                T[K.EIDX[(u, v)]] = {(b, b)}
    return K.template_from_sets(T)


def random_template(rng, kmax=4):
    return K.template_from_sets(
        [set(rng.sample(K.CELLS, rng.randint(0, kmax))) for _ in range(K.NE)])


def test_word_encoding(trials=25, seed=7):
    rng = random.Random(seed)
    cases = [("cube12", cube_template()),
             ("full", [frozenset(K.CELLS)] * K.NE)]
    for t in range(trials):
        cases.append(("rand%d" % t, random_template(rng)))
    bad = 0
    for name, T in cases:
        truth = len(K.singleton_words(T)) == 0
        got = word_cnf_sat(T, K.MIXED_WORDS)
        flag = "ok" if got == truth else "MISMATCH"
        if got != truth:
            bad += 1
        print("  %-8s zero_singleton=%-5s  cnf_sat=%-5s  %s"
              % (name, truth, got, flag))
    return bad == 0


def test_planted_singleton(seed=11):
    """Control 3: take a zero-singleton template, delete one cell of a fibre
    so that a singleton appears, and check both checkers see it."""
    rng = random.Random(seed)
    res = S.decide(28, max_solutions=1, verbose=False, time_budget=300)
    assert res["verdict"] == "SAT", res["verdict"]
    T, a = res["witnesses"][0]
    assert a["n_singletons"] == 0
    print("  base template: support=%d Sigma=%d singletons=%d"
          % (a["support"], a["sigma"], a["n_singletons"]))
    # find a mixed word with a small (>=2) fibre and knock cells out of all
    # but one supporting matching
    sizes = F.fibre_sizes(T)
    order = sorted((s, i) for i, s in enumerate(sizes)
                   if 2 <= s <= 6 and F.IS_MIXED[i])
    made = 0
    for _size, wi in order[:40]:
        w = K.ALL_WORDS[wi]
        fib = K.fibre(T, w)
        keep = fib[0]
        T2 = [set(s) for s in T]
        for mi in fib[1:]:
            for ei in K.MATCHINGS[mi]:
                if ei in K.MATCHINGS[keep]:
                    continue
                u, v = K.EDGES[ei]
                T2[ei].discard((w[u], w[v]))
                break
        T2 = K.template_from_sets(T2)
        f2 = K.fibre(T2, w)
        if len(f2) != 1:
            continue
        made += 1
        naive_ok = w in K.singleton_words(T2)
        fast_ok = w in F.singleton_words(T2)
        cnf_ok = not word_cnf_sat(T2, [w])
        print("  planted singleton on %s: naive=%s fast=%s cnf_rejects=%s"
              % (str(w), naive_ok, fast_ok, cnf_ok))
        if not (naive_ok and fast_ok and cnf_ok):
            return False
        if made >= 3:
            break
    return made >= 1


def test_planted_sc_violation(seed=13):
    """Control 4: a template violating (SC) must be rejected by the (SC)
    clauses (and detected by the standalone checker)."""
    res = S.decide(28, max_solutions=1, verbose=False, time_budget=300)
    T, a = res["witnesses"][0]
    assert not a["sc_failures"]
    ok = True
    # (i) fatten one block so no incident edge can serve some slot at vertex 0
    for p in range(3):
        T2 = [set(s) for s in T]
        for (ei, j) in K.INCIDENT[p]:
            T2[ei] = set(K.CELLS)          # full block serves no column
        T2 = K.template_from_sets(T2)
        fails = K.sc_slots(T2)
        cnf = sc_cnf_sat(T2)
        print("  fattened star at vertex %d: sc_failures=%d (>=3 expected) "
              "cnf_rejects=%s" % (p, len(fails), not cnf))
        ok = ok and len(fails) >= 3 and not cnf
    # (ii) empty one block: (SC) may or may not break.  The base CNF also
    #      enforces nonempty constant fibres and the support count, so compare
    #      against the full base predicate, not against (SC) alone.
    rng = random.Random(seed)
    agree_all = True
    n_break = 0
    for _ in range(20):
        T2 = [set(s) for s in T]
        ei = rng.randrange(K.NE)
        T2[ei] = set()
        T2 = K.template_from_sets(T2)
        base_true = ((not K.sc_slots(T2)) and
                     all(len(K.fibre(T2, K.CONSTANT_WORDS[c])) > 0
                         for c in range(3)))
        got = sc_cnf_sat(T2)
        if not base_true:
            n_break += 1
        if base_true != got:
            agree_all = False
            print("  MISMATCH on deletion of edge %s: base=%s cnf=%s"
                  % (str(K.EDGES[ei]), base_true, got))
    print("  20 random block deletions (%d break the base predicate): "
          "standalone/base-CNF agree = %s" % (n_break, agree_all))
    return ok and agree_all


def sc_cnf_sat(T):
    enc = S.Encoder(m=K.support_size(T), derived=False)
    solver = Cadical195(bootstrap_with=enc.clauses + pin(enc, T))
    r = solver.solve()
    solver.delete()
    return r


def test_constant_and_card(seed=17):
    """The base CNF (no words) must accept a pinned template iff (SC) holds,
    all three constant fibres are nonempty, and the support matches m."""
    rng = random.Random(seed)
    ok = True
    cases = [cube_template(), [frozenset(K.CELLS)] * K.NE]
    for _ in range(20):
        cases.append(random_template(rng))
    for T in cases:
        truth = (not K.sc_slots(T)) and all(
            len(K.fibre(T, K.CONSTANT_WORDS[c])) > 0 for c in range(3))
        enc = S.Encoder(m=K.support_size(T), derived=True)
        solver = Cadical195(bootstrap_with=enc.clauses + pin(enc, T))
        got = solver.solve()
        solver.delete()
        if got != truth:
            print("  MISMATCH base CNF: truth=%s got=%s" % (truth, got))
            ok = False
    print("  base CNF (SC + constant fibres + support) on 22 templates:",
          "ok" if ok else "MISMATCH")
    # support cardinality must bite
    T = cube_template()
    enc = S.Encoder(m=13, derived=True)
    solver = Cadical195(bootstrap_with=enc.clauses + pin(enc, T))
    got = solver.solve()
    solver.delete()
    print("  cube (support 12) pinned into the m=13 CNF -> SAT?", got,
          "(must be False)")
    return ok and not got


if __name__ == "__main__":
    print("fastcheck vs naive selftest:", F.selftest())
    print("\n[T1] word encoding vs naive singleton enumeration")
    t1 = test_word_encoding()
    print("\n[T2] base CNF: (SC) + constant fibres + cardinality")
    t2 = test_constant_and_card()
    print("\n[T3] control 3: planted singleton")
    t3 = test_planted_singleton()
    print("\n[T4] control 4: planted (SC) violation")
    t4 = test_planted_sc_violation()
    print("\nRESULT:", all([t1, t2, t3, t4]))
    sys.exit(0 if all([t1, t2, t3, t4]) else 1)
