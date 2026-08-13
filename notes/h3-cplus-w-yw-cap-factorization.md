# The final C-plus W equation is the old Yw-to-W cap law

## Result

The last physical `W` compatibility in the conditional generic `C_plus`
core is not a fourth source-generator theorem.  It is exactly the
previously isolated comparison

\[
                         Yw\longmapsto W              \tag{1}
\]

on the literal cap top `B=r0-T`.  Once the final P2/pointed-`K_Eq` repair
is constructed in the complete augmented grade and is dark in both `Yw`
and `W`, the old cap supplies (1) and the final `W` row cancels together
with the derived `Yw` row.

Checker:
[`verify_h3_cplus_w_yw_cap_factorization.py`](../computations/verify_h3_cplus_w_yw_cap_factorization.py).

## The exact root-even table

Put

\[
 v={B_1+B_4\over2},\qquad
 E=2D_{\rm root}\otimes v,\qquad
 D_{\rm root}=(-1,1,-1,1).
\]

The packet `E` has eight nonzero root-word labels and augmentation zero.
The conditional core gives the net P2 target/Eq signature

\[
                 (\operatorname{Eq},\operatorname{target})=(-E,-E).
                                                               \tag{2}
\]

Its literal full-Hasse top contains the physical cap

\[
 B_E=(r_0-T)_E,qquad
 (\operatorname{Eq},Yw,W,\operatorname{target})(B_E)
                        =(E,E,E,0).                    \tag{3}
\]

Extracting (3) from (2) leaves the Cartan/Spencer remainder

\[
 C_E=(-2E,0,0,-E).                                   \tag{4}
\]

The endpoint target path and the clean pointed Eq repair are

\[
 T_E=(0,-E,-E,E),\qquad K_{Eq,E}=(E,0,0,0).          \tag{5}
\]

Therefore

\[
 \boxed{T_E+B_E+C_E+K_{Eq,E}=0}                      \tag{6}
\]

simultaneously in `Eq`, derived `Yw`, physical `W`, and target.  The
anchor of `B_E` is `-sum(E)=0`, so (6) does not alter the already correct
`ainc=-1` carrier.  The pure `d_even` residue section and the labelled
Kähler ridge are also `Yw/W`-dark.

Equation (6) refines the target/Eq triangle in `649b7eb`.  After combining
(3)--(4), its P2 entry is exactly

```text
Eq=-E, Yw=+E, W=+E, target=-E.
```

Thus the previously unresolved scalar equation is precisely the equality
of the middle two entries.

## Why the map is source-provenant

The complete Hasse/Koszul totalization constructs all proper faces.  In
each of its fifteen denominator cubes, its top coefficient is literally

\[
                         r_0-T,                       \tag{7}
\]

not a newly declared cap column.  Under the original physical differential,

\[
                   d(r_0-T)=(H_0-u)e_{Eq}+Yw.         \tag{8}
\]

The pointed `K_Eq` comparison removes the first term of (8).  The physical
cap presentation assigns the same coefficient to the derived boundary and
the cap readout:

\[
                         Yw(r_0-T)=W(r_0-T)=1.         \tag{9}
\]

Multiplying (7) by `E` gives (3).  No new occurrence, target, residue, or
anchor column is introduced.

The same factorization is stable under the inactive normal/Rees jets.
At order `k`, both rows are the identical Hasse convolution

\[
               \sum_{i=0}^k h_i\,Yw[k-i]
       \quad\longmapsto\quad
               \sum_{i=0}^k h_i\,W[k-i].             \tag{10}
\]

The committed factorization checks (10) at orders zero through three.  The
full weighted-normal theorem supplies every derived convolution; it does
not require a new cap generator type.

## The sharp projection guard

Physical `W` remains a load-bearing augmented row.  Keep every value of
`B_E` except change

```text
Yw(B_E)=E,     W(B_E)=E
```

to

```text
Yw(B_E)=E,     W(B_E)=0.
```

All Eq, source-boundary, target, anchor, word, residue, q, and terminal
rows are unchanged.  The derived totalization still closes, but the final
physical core acquires the sole debt

\[
                             W=-E.                    \tag{11}
\]

On any nonzero root-label coordinate of `E`, the primitive covector

\[
                             W-Yw                     \tag{12}
\]

kills the correctly typed cap and reads `-1` on the mutated one.  The same
coordinate of `W` detects (11).  Hence a comparison theorem which forgets
physical `W` cannot imply (6).

## Frontier consequence

The strongest exact conclusion is conditional but constructive:

> Build the already-required source-labelled P2/pointed-`K_Eq` comparison
> with its repair dark in `Yw` and `W`.  Then use the existing literal
> `r0-T` cap.  It maps `Yw_E` identically to `W_E`, so the final C-plus `W`
> equation closes without another generator.

Combined with the q dichotomy, the only augmented datum not supplied by
this cap factorization is the labelled shifted Kähler ridge.  The separate
beta-zero `D0`/Bockstein clause is unchanged.

Run:

```text
python3 computations/verify_h3_cplus_w_yw_cap_factorization.py
python3 -O computations/verify_h3_cplus_w_yw_cap_factorization.py
python3 -I -S computations/verify_h3_cplus_w_yw_cap_factorization.py
```

Frozen ledger SHA-256:

```text
5d8ecff55e53cfb0430bcbc0784f981c2bef1efea1d350e3455df5ee40170b1e
```
