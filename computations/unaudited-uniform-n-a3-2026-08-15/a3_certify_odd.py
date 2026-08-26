import sys, json, warnings
sys.path.insert(0,'.')
sys.path.insert(0,'/Users/rishi/workplace/krenn-conjecture/computations/unaudited-witness-splitting-w2-2026-08-15')
warnings.filterwarnings('ignore')
from a3_task1_family_odd import family_odd
import a3_admissibility as AD, a3_task2_reach as R, a3_task1_certify10 as C
import w2_monomial as W2
N, ce = family_odd(5)
ce = [[tuple(sorted(e)) for e in s] for s in ce]
fr = R.Frame(10)
col = [None]*len(fr.edges)
for r in range(3):
    for e in ce[r]:
        col[fr.edges.index(e)] = r
print("built colouring; support", sum(1 for x in col if x is not None), flush=True)
cert = C.certify(col, fr)
print("certify done", flush=True)
ok, bad = AD.sc_admissible(ce); deg = AD.live_degrees(ce)
geo, lab = AD.to_labels(ce)
v = W2.analyse(geo, lab)
print('support', cert['support'], '| pures prod/direct', cert['pures_product'], cert['pures_direct'])
print('singletons prod/direct', cert['singletons_product'], cert['singletons_direct'],
      '| two methods agree', cert['two_methods_agree'])
print('histogram', cert['histogram_product'])
print('(SC)-admissible', ok, 'violations', bad, '| min live degree', min(deg))
print('W2 independent verdict', v['verdict'], '| binomials', cert['binomial_fibres'],
      '| odd circuit', cert['odd_circuit_found'], 'sum odd', cert['odd_circuit_sum_is_odd'])
json.dump(dict(colour_edges=[[list(e) for e in s] for s in ce], cert=cert,
               SC_admissible=ok, min_live_degree=min(deg), W2_verdict=v['verdict']),
          open('results_family_odd_certified.json','w'), indent=1)
print('wrote results_family_odd_certified.json')
