# Independent seven-block carrier-closure referee

## Verdict

**REJECT COMPLETE CLOSURE.** The pinned packages rigorously close 8 of the 64 residual records, namely representative 0 and its guard mate across the four A12/A67 zero/nonzero flags. Exactly 56 records remain unproved.

The complete uncovered list is machine-readable in `results_seven_block_closure_referee.json`. It splits as follows:

- 40 records in representatives 1--5 (boundary orbit IDs 12--31): the new analytic proof checks only the fixed-identity cap functional and omits the three diagonal activity functionals.
- 16 records in boundary orbit IDs 0--7: these are eight added supports, each with A12 absent/present and A67 absent, which are not in any of the six representative support pairs.

Representative 0 is accepted across boundary orbit IDs 8--11. Its exact-Q rank <=1 and rank-2 incidence ideals explicitly encode cap failure and a diagonal-incidence failure; color symmetry covers all three diagonal choices, rank 3 is excluded, and the polynomial systems permit A12/A67 coefficient-zero specializations.

## Load-bearing activity defect

For a two-sandwich response row space `P tensor Q`, the four activity functionals are live on the kernel exactly when

1. `A_cap` is not in `P tensor Q`; and
2. for every `i=0,1,2`, it is not the case that `e_i` belongs to both `P` and `Q`.

The identity-pairing sublemma is sound: `I3 in P tensor Q` forces `P=Q=Q^3`, because every element of `P tensor Q` has rank at most `min(dim P,dim Q)`. Its converse is not enough for activity. The hostile case `P=Q=<e0>` has `I3` outside `P tensor Q` while `E00` lies in the response row space, so `K00` vanishes on the entire kernel and the star is inactive. This directly refutes the inference used by the rep1/2/3/4/5 reports: `P proper => identity pairing live => active star`.

The source orientations are otherwise consistent. For `L(K)=(U^T K B_j)_j`, `im(L*)` has column space in `Col(U)` and row space in `ColSpan(B_j)`; the common-right formula is the transpose version.

## Zero-factor branch

- Outside factor nonzero: the guard makes the common factor singular, but this does not exclude coordinate incidence; an incidence or full-X5 argument is still required.
- Outside factor zero and A67 nonzero: the companion is guard-forced zero and `L67=0`; all three diagonal functionals and the nonzero cap functional are live, so this branch is valid.
- Outside factor zero and A67 zero: the cap functional is zero, hence this carrier is inactive. One must explicitly descend to the already-sealed <=6-added-block theorem; it is not an active-carrier branch.

## Consequence

An eight-block induction step cannot cite a complete seven-block base. The minimal next work is (a) restore diagonal-incidence/full-X5 obligations for reps1--5 and (b) construct carriers for the exact 16 records in orbit IDs 0--7.
