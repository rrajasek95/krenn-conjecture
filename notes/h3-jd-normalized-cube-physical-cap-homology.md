# The normalized seven-cube leaves a five-dimensional physical word/ridge homology

## Outcome

The `126` proper faces of a seven-occurrence top can be packaged without
enumeration.  The reduced Boolean-Hasse cobar is the ordered-set-partition
complex.  Eilenberg--Zilber gives a canonical homotopy

\[
                 dh+hd=1-\operatorname{sh}\operatorname{AW}.   \tag{1}
\]

Thus every summand contracts except the one alternating Koszul line.  The
chain dimensions and differential ranks are

```text
C_k:  1, 126, 1806, 8400, 16800, 15120, 5040
d_k:  1, 125, 1681, 6719, 10081, 5039.
```

The only homology is the top sign class

\[
 \operatorname{Alt}_7=
 \sum_{\pi\in S_7}\operatorname{sgn}(\pi)
       \{\pi_1\}|\cdots|\{\pi_7\}.                  \tag{2}
\]

So the fully augmented cubical chains are contractible, but the normalized
proper-face complex is not literally acyclic: it retains (2).  This is the
precise meaning of the cube contracting homotopy in the present problem.

The physical word/ridge caps retain more homology.  A source-valid bar which
cancels the endpoint ridge `Omega_v` has a compulsory all-derivation response
companion `q_(v,N)`.  Its column is

\[
                         b_{v,N}=-\Omega_v+q_{v,N}.     \tag{3}
\]

For five deleted faces and three matchings per face, (3) is an injective map

\[
 \mathbb Z^{15}\longrightarrow
 \mathbb Z^5_{\Omega}\oplus\mathbb Z^{15}_{q}.
\]

Its cokernel, hence the first relative physical cap homology after shifting
degrees, is

\[
                  \boxed{H_{\rm cap}\simeq\mathbb Z^5},        \tag{4}
\]

with primitive duals

\[
            \lambda_v=\Omega_v+\sum_Nq_{v,N}.          \tag{5}
\]

The checker is
[`verify_h3_jd_normalized_cube_physical_cap_homology.py`](../computations/verify_h3_jd_normalized_cube_physical_cap_homology.py).

## Structural proof of the abstract contraction

For a fixed seven-element set, the degree-`k` cobar basis consists of its
ordered partitions into `k` nonempty blocks, so

\[
                 \dim C_k=k!\,S(7,k).                 \tag{6}
\]

The Boolean coalgebra is the tensor product of the seven one-occurrence
coalgebras.  Alexander--Whitney and shuffle identify its multilinear cobar
with the tensor product of their normalized complexes.  Each factor has one
primitive generator, so the tensor product has only the alternating top
class (2).  Equation (1) contracts the complement.

At the top, this can be seen without invoking a dimension calculation.  A
codimension-one ordered partition has one two-element block.  Splitting it
in the two orders imposes

```text
e_pi + e_(pi s_i) = 0
```

for an adjacent transposition `s_i`.  The adjacent-transposition Cayley
graph of `S_7` is connected and bipartite by permutation sign.  Its quotient
is exactly the one-dimensional sign line (2).

This source-side theorem packages all `126` faces, and its formula is valid
for every number of spectator occurrences.  No further support enumeration
is needed.

## Why the physical contraction fails

If the response companion is forgotten, the columns (3) project to
`-Omega_v`, and every ridge is contractible.  This is the abstract
bar-level cancellation.

Physical source covariance forces the companion back in.  The full physical
word is `01211222`; deleting exposed `x=0` gives the all-derivation word
`1211222`, while deleting the two endpoint sites gives the residual word
`012112`.  Therefore the previously isolated wrong-word obstruction and the
ridge obstruction are not two independent homology classes.  They are the
two coordinates of the same source-valid column (3), coupled by (5).

Every Bianchi shuffle or matching switch is a difference of columns (3) and
is killed by every `lambda_v`.  The matrix has fifteen unit companion pivots,
so (4) is integral and torsion-free, not just a rational rank defect.

## Consequence for `J_D`

Let the proper ridge face of a proposed selected totalization have
coefficients `gamma_v`.  Choose route coefficients `beta_(v,N)`.  Cancelling
the ridge forces

\[
                        \sum_N\beta_{v,N}=\gamma_v.    \tag{7}
\]

The surviving word face is then

\[
                       \sum_{v,N}\beta_{v,N}q_{v,N},  \tag{8}
\]

and its homology coordinates are exactly `lambda_v=gamma_v`.  Thus the old
bar/Bianchi inventory closes the physical cap if and only if every
`gamma_v` vanishes.  Merely having `sum_v gamma_v=0`, as an even or
augmentation-zero aggregate may, is insufficient.

For the one selected rho-even `J_D` line, one new aggregate reduced response
cell cancelling (8) is minimal.  For a natural theorem over all five
deleted faces, the five independent classes (5) require five primitive
reduced cells, or one equivariant family with five labelled components.
This is the first exact homology/dual behind the word/ridge caps.

This does not split the proof into five conjecture-level theorems.  The five
components, the earlier `J_D` top, and the pointed `P_f` cell are pieces of
one pointed comparison resolution.

## Uniform monoidal scope

Eilenberg--Zilber does solve the abstract spectator Leibniz problem.  The
source-side Hasse resolution is monoidal, so shuffle packages every `dT`
face of a spectator matching tail in every order.

It does not kill (4).  All groups in (4) and the spectator top Koszul line
are free, so Kunneth gives

\[
       \mathbb Z^5\otimes H_{\rm top}(C_{\rm spectator})
                         \simeq\mathbb Z^5.            \tag{9}
\]

The physical obstruction persists under every spectator shuffle.  In
addition, the full GHZ target is not the tensor product of the eight-site
GHZ target with independent pair colours; arbitrary tails do not preserve
the labelled residue/Kähler law; and a fixed spectator-divisible sector does
not exhaust the intrinsic order-`h` Macaulay block.

The shortest uniform positive target is therefore:

> Make the five reduced ridge/response augmentations a module over the
> spectator Hasse coalgebra, with shuffle-compatible physical word, ridge,
> `q`, GHZ-target, and terminal/Macaulay descent.

That would upgrade the already universal source-side shuffle to the needed
physical `PAComp(h)`.  The shuffle alone does not.

## Verification

Run:

```text
python3 computations/verify_h3_jd_normalized_cube_physical_cap_homology.py
python3 -O computations/verify_h3_jd_normalized_cube_physical_cap_homology.py
python3 -I -S computations/verify_h3_jd_normalized_cube_physical_cap_homology.py
```

The checker prints its frozen ledger SHA-256.

```text
d382402c00c00b81bcb9add09c7e7aab09a90ccc199d2cc6c547a0860110e2c3
```
