#!/usr/bin/env python3
"""ANTI-TAUTOLOGY CHECK: does the fast numeric arc really compute the same
thing as the committed SYMBOLIC G.source_graph?

Runs the committed symbolic graph to order 8 with the two extra symbolic
bends r4, r5 (exactly the call used by the committed
verify_n8_p5_generic_L_three_step_bend_recurrence.py), evaluates its
order-7 and order-8 compatibility rows at the committed point with chosen
rational r4, r5, and compares against my independent numeric arc with the
same bends and z46^(6..8) = 0.
"""
from fractions import Fraction as QQ
import importlib.util
import sys
import time
from pathlib import Path

COMP = Path("/Users/rishi/workplace/krenn-conjecture/computations")
sys.path.insert(0, str(Path(__file__).resolve().parent))

from myarc import Arc, collapse, committed_point, load_base  # noqa: E402
from step1_claimA import solve_linear, g_relation  # noqa: E402


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, COMP / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def evaluate(source, values):
    total = QQ(0)
    for monomial, coefficient in source.items():
        term = QQ(coefficient)
        for variable in monomial:
            term *= values[variable]
        total += term
    return total


def main():
    t0 = time.time()
    G = load_module("cross_g", "verify_n8_p5_schur_generic_L_g_center.py")
    F2 = G.F2
    base = F2.audit(return_data=True)
    print(f"[{time.time()-t0:.1f}s] committed F2 base ready", flush=True)
    graph = G.source_graph(base, maximum_order=8, additional_bends=2)
    print(f"[{time.time()-t0:.1f}s] committed SYMBOLIC source_graph done",
          flush=True)

    data = load_base()
    point = committed_point(data)
    a = data["layout_a"]
    z = lambda i: point[a[i]]
    s = solve_linear(data["first_relation"], point, data["first_bend"])
    point[data["first_bend"]] = s
    t = solve_linear(data["second_relation"], point, data["second_bend"])
    r3 = g_relation(data, point, s, t)

    r3v, r4v, r5v = graph["bend_variables"]
    bvar, qvar = graph["b_variable"], graph["inverse_b"]
    print("symbolic variable ids: r3,r4,r5,b,q =",
          r3v, r4v, r5v, bvar, qvar, flush=True)

    R4 = QQ(5, 3)
    R5 = QQ(-9, 2)
    values = dict(point)
    values[data["first_bend"]] = s
    values[data["second_bend"]] = t
    values[r3v] = r3
    values[r4v] = R4
    values[r5v] = R5
    b = z(44) + z(45)
    values[bvar] = b
    values[qvar] = QQ(1) / b

    symbolic7 = [evaluate(row, values) for row in graph["compatibility_orders"][6]]
    symbolic8 = [evaluate(row, values) for row in graph["compatibility_orders"][7]]
    symbolic6 = [evaluate(row, values) for row in graph["compatibility_orders"][5]]

    dynamic = set(data["local_variables"]) | {a[46]}
    normal = [collapse(r, point, dynamic) for r in data["normal"]]
    transverse = [collapse(r, point, dynamic) for r in data["transverse"]]
    targets = [collapse(r, point, dynamic) for r in data["obstruction"]]
    arc = Arc(data, point, 8)
    arc.set_bends([z(46), s, t, r3, R4, R5, QQ(0), QQ(0), QQ(0)])
    numeric = [arc.step(m, normal, transverse, targets) for m in range(1, 9)]
    print(f"[{time.time()-t0:.1f}s] numeric arc done", flush=True)

    ok = True
    for label, sym, num in (("order6", symbolic6, numeric[5]),
                            ("order7", symbolic7, numeric[6]),
                            ("order8", symbolic8, numeric[7])):
        mismatches = [(i + 1, x, y)
                      for i, (x, y) in enumerate(zip(sym, num)) if x != y]
        nz = [i + 1 for i, x in enumerate(sym) if x]
        print(f"{label}: symbolic nonzero rows={nz}; "
              f"mismatches vs numeric = {mismatches[:5]} "
              f"(count {len(mismatches)})", flush=True)
        ok = ok and not mismatches
    print("\nSYMBOLIC/NUMERIC AGREEMENT:", ok)
    print(f"total {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
