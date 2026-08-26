import sys, json
from itertools import permutations, product
sys.dont_write_bytecode = True
from fractions import Fraction
BIJ=tuple(permutations(range(4)))
def per4(vs):
    return sum(vs[0][s[0]]*vs[1][s[1]]*vs[2][s[2]]*vs[3][s[3]] for s in BIJ)
a=(1,1,1,0); b=(0,0,0,1)
V=[a,b]
vals={}
for t in product(range(2),repeat=4):
    vals[t]=per4([V[t[0]],V[t[1]],V[t[2]],V[t[3]]])
print("V = span{(1,1,1,0),(0,0,0,1)} : per on the 16 basis 4-tuples, over Z:")
print("  values:", sorted(set(vals.values())))
print("  vanishes identically over Q?", all(v==0 for v in vals.values()))
print("  vanishes identically mod 3?", all(v%3==0 for v in vals.values()))
print("  vanishes identically mod 5?", all(v%5==0 for v in vals.values()))
print("  4! = 24 = %d mod 3 ; the 3x3 permanent multiplicity 6 = %d mod 3"%(24%3,6%3))
json.dump({"per_values":sorted(set(vals.values())),
           "vanishes_Q":all(v==0 for v in vals.values()),
           "vanishes_mod3":all(v%3==0 for v in vals.values()),
           "vanishes_mod5":all(v%5==0 for v in vals.values())},
          open("results_char3_artifact.json","w"), indent=1)
