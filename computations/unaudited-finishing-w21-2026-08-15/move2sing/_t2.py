import sys, json
sys.dont_write_bytecode = True
import m2core as M
DEADROW = {(i,j): M.DEAD[(i,j)][0] for (i,j) in M.DEAD}
def dirty(x):
    return tuple(j for j in M.R if any(DEADROW.get((i,j))==x[M.LPOS[i]] for i in M.L))
four = [x for x in M.LFREE if len(dirty(x))==4]
print("L-free words with ALL FOUR R-sites dirty:", four)
for x in four:
    print(" x=%s" % (x,))
    for j in M.R:
        cells = [(i,d) for i in M.L for d in range(3)]
        dead = [(i,d) for i in M.L for d in range(3) if not M.occ(i,j,x[M.LPOS[i]],d)]
        rows = {i: sum(1 for d in range(3) if M.occ(i,j,x[M.LPOS[i]],d)) for i in M.L}
        cols = {d: sum(1 for i in M.L if M.occ(i,j,x[M.LPOS[i]],d)) for d in range(3)}
        print("   site %d: dead cells in M_j^x at (i,d)=%s ; occupied per row %s ; per col %s"
              % (j, dead, list(rows.values()), list(cols.values())))
# mirror: R-free words with all four L-sites dirty
DEADCOL = {(i,j): M.DEAD[(i,j)][1] for (i,j) in M.DEAD}
def dirtyR(y):
    return tuple(i for i in M.L if any(DEADCOL.get((i,j))==y[M.RPOS[j]] for j in M.R))
fourR = [y for y in M.RFREE if len(dirtyR(y))==4]
print("\nR-free words with ALL FOUR L-sites dirty:", fourR)
json.dump({"L4dirty":[list(x) for x in four],"R4dirty":[list(y) for y in fourR]},
          open("results_4dirty.json","w"), indent=1)
