# Full-family representative 3: exact low-rank carrier closure

Status: **superseded/retracted: representative 3 is closed only in the rank-zero outside-factor branch; nonzero ranks have pairing activity only.** The earlier all-rank claim omitted the three separate diagonal-functionals conditions.

Among the untouched representatives 1, 3, 4, and 5, all have 12 supported perfect matchings and two terms in their smallest two-sandwich star. Representative 3 is the exact tiebreak winner: its 6,561 full-X5 equations have total term load 37,260, versus 38,718, 40,176, and 41,634. Its added support is `{06,14,17,25,26,36,37}`.

At the identity guard the three source-labelled equations are

`A06 A37^T=0`, `A37^T+A17 A36^T=0`, and `A26 A37^T+A36^T=0`.

If `A37=0`, the third equation forces `A36=0`; hence the cap67/triangle012 response map is zero. Since full-family `A67` is nonzero, its pairing is live on the full matrix kernel, so cap67 is active.

If `A37` is nonzero, `A06 A37^T=0` gives a nonzero vector in `ker(A06)`, so `P=Row(A06^T)=Col(A06)` is proper. The independently sealed cap03/star4 map has exactly the two distinct response terms and factors

`A06^T K [A35 | A37]`,

with response row space `P tensor ColSpan(A35,A37)`. Because the cap block `A03=I`, this proves the cap pairing is live. It does **not** prove all three diagonal functionals live: for each `i` one separately needs `not(e_i in P and e_i in Q)`. Properness of `P` excludes at least one basis vector, not every basis vector.

The verifier now includes a compatible exact local countermodel: `A37=E11`, `A36=-E11`, `A06=E00`, `A17=A26=I`, and `A35=E00`. The guard holds and the trace pairing is live, but `E00=A06^T E00 A35` lies in the response row space, so `K00` vanishes on the kernel. The missing lemma is the three-coordinate incidence exclusion above.

Rep2 remains open: its six fixed-base size-seven heuristic charts are exact-Q unit ideals, but that negative result is not a global movable-base theorem. Representatives 1, 4, and 5 and all non-full-family strata remain outside this package.
