"""A7 TASK 4b: WHICH of the (R) conditions does a per-site colour permutation
break?  Exhaustive decomposition of the 6^8 sweep into the (SC) failure mode and
the constant-word failure mode, for three templates known to be in (R).

Also records the shape of the 576-element survivor set.
"""

import itertools
import json
import os
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a7_core as C
from a7_task4_s3hazard import S3, S3_INV, W19_WITNESS, thin_data, direct_in_R_sigma

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results_A7_TASK4B.json")


def main():
    res = {}
    for name, T in [("W8_m26", C.W8_M26), ("W8_m28", C.W8_M28),
                    ("W19_stratum_i", W19_WITNESS)]:
        assert C.in_R(T)
        cnt = C.fibre_counts(T)
        const_cnt = [int(cnt[c]) for c in C.CONST_WORDS]
        td = thin_data(T)
        by_p = {p: [(q, c) for (pp, q, c) in td if pp == p] for p in range(8)}
        pow3 = [3 ** p for p in range(8)]
        t0 = time.time()
        n_sc = n_const = n_mixed = n_both = 0
        survivors = []
        for sig in itertools.product(range(6), repeat=8):
            perms = [S3[k] for k in sig]
            sc = True
            for p in range(8):
                s = set()
                for (q, c) in by_p[p]:
                    s.add(perms[q][c])
                if len(s) != 3:
                    sc = False
                    break
            inv = [S3_INV[k] for k in sig]
            pre = [sum(inv[p][r] * pow3[p] for p in range(8)) for r in range(3)]
            constok = all(int(cnt[w]) >= 1 for w in pre)
            preset = set(pre)
            mixedok = all(C.CONST_WORDS[s] in preset or const_cnt[s] >= 3 for s in range(3))
            n_sc += sc
            n_const += constok
            n_mixed += mixedok
            if sc and constok and mixedok:
                n_both += 1
                survivors.append(sig)
        assert n_both == len(survivors)
        # shape of the survivor set
        dev = Counter()
        for s in survivors:
            base = Counter(s).most_common(1)[0][0]
            dev[sum(1 for x in s if x != base)] += 1
        # is it a union of global-S3 cosets?
        S = set(survivors)
        coset_ok = True
        for s in survivors:
            for g in range(6):
                # right-multiply every site by the same global g
                t = tuple(S3.index(tuple(S3[s[p]][S3[g][c]] for c in range(3)))
                          for p in range(8))
                if t not in S:
                    coset_ok = False
                    break
            if not coset_ok:
                break
        res[name] = {
            "group_order": 6 ** 8,
            "n_sc_ok": n_sc,
            "n_constant_words_nonempty": n_const,
            "n_mixed_condition_ok": n_mixed,
            "n_preserving_in_R": n_both,
            "n_breaking_in_R": 6 ** 8 - n_both,
            "n_breaking_via_SC_only": n_both and None,
            "const_fibres_of_T": const_cnt,
            "survivor_deviation_histogram": {str(k): v for k, v in sorted(dev.items())},
            "survivors_form_union_of_global_S3_right_cosets": coset_ok,
            "n_global_survivors": sum(1 for s in survivors if len(set(s)) == 1),
            "seconds": round(time.time() - t0, 1),
        }
        # exact breakdown of failures
        res[name]["n_breaking_via_SC_only"] = None
        res[name]["failure_breakdown"] = {
            "SC_fails": 6 ** 8 - n_sc,
            "constant_word_fails": 6 ** 8 - n_const,
            "mixed_fails": 6 ** 8 - n_mixed,
        }
        print(name, json.dumps({k: v for k, v in res[name].items()
                                if k != "survivor_deviation_histogram"}), flush=True)
        print("   deviation histogram:", res[name]["survivor_deviation_histogram"], flush=True)
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main()
