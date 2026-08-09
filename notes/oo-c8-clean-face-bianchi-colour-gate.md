# Clean-face Bianchi colour gate on the active OO regressions

The common-word square audit finds 51 clean mixed-target faces with two
nonzero cofactor Hessians.  To place those Hessians in the same literal
vertex recursion or the same power-free Bianchi row, their exclusive
endpoint colours must match the selected direct cells

\[
                d_{02}=E_{10},\qquad d_{04}=E_{11}.       \tag{1}


Thus the `pr` cofactor leader must have colour `0` at site `q=2`, while the
`pq` cofactor leader must have colour `1` at site `r=4`.

## Exact clean-face census

Exhausting all clean distance-one and distance-two faces gives

\[
\begin{array}{c|rrrr}
(q\text{-colour},r\text{-colour})&(0,2)&(2,1)&(0,0)&(2,0)\\ \hline
\text{profiles}&47&1&1&2.
\end{array}                                                \tag{2}


No profile has `(q,r)=(0,1)`.  Equivalently, the selected fixed-label
Bianchi row sees

\[
48\text{ profiles through the }pr\text{ leader only},\qquad
1\text{ through the }pq\text{ leader only},\qquad
2\text{ through neither},\qquad0\text{ through both}.     \tag{3}


The 17 unavoidable target-contaminated faces lie in the additional sectors
`(1,2)` and `(1,0)` and do not repair the simultaneous visibility gate.

## Consequence for the power-free overlap row

For exposed colours `(a,b,c,d)=(1,0,1,0)`, the literal identity is

\[
 Uf+tH-Fg-yN=(At-By)v+(AU-BF)z.                           \tag{4}


The square difference of (4) cannot isolate both chosen cofactor leaders
on any clean regression face: one leader is always in a different
exclusive-colour grade.  The same obstruction prevents the two deleted-star
selectors from placing both leader Hessians in one fixed-colour recursion
at `p`.

This does not invalidate (4), which is a universal source identity.  It
identifies the exact missing provenance term: a full-nine head-column
transport changing `r:2 -> 1` in the 47-profile main branch (or changing
`q:2 -> 0` in the one opposite branch).  Any Bianchi proof must perform
that colour transport before taking the common-word Hessian.  Applying one
fixed-label square directly is not source-faithful.

## Reproduction

```text
python computations/verify_oo_c8_clean_face_vertex_recursion.py
python -O computations/verify_oo_c8_clean_face_vertex_recursion.py
```

The checker reconstructs all clean faces and their exclusive endpoint
colours.  It retains a literal neighbor-by-neighbor hafnian-recursion audit
for any future profile that passes the simultaneous-colour gate; the
current exact census proves that branch is empty.
