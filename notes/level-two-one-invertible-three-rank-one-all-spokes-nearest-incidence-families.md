# Nearest continuous all-spokes incidence families are excluded at L1

Research evidence only. Krenn's conjecture remains open and the certified
spine is unchanged.

## Outcome

The exact `1I+3R+2Z` all-spokes incidence point from the previous follow-up is
not isolated. If all other residual blocks are held fixed and

\[
M_{34}=\begin{pmatrix}a&b\\c&d\end{pmatrix},                \tag{1}
\]

then the rank-53 mixed determinantal germ through the committed point is the
three-dimensional hyperplane

\[
b=d.                                                         \tag{2}
\]

The function-field rank on the full four-parameter block is `55/54`; after
(2) it is `55/53`. Thus (2), away from its rank-drop sublocus, is a continuous
family with both pure L0 targets incident.

The smallest coupled enlargement also survives linear L0. Free the single
additional cell

\[
M_{04}=\begin{pmatrix}x&85\\0&87\end{pmatrix},\qquad
M_{34}=\begin{pmatrix}a&b\\c&b\end{pmatrix}.                \tag{3}
\]

The four-parameter family (3) again has function-field ranks `55/53`, retains
the generic-kernel equation and uniform literal R2, and therefore contains a
nonempty open family passing all unrestricted linear-L0 incidences.

No member of its rank-55 locus passes the full endpoint equations. Both L1
star spaces are constant and two-dimensional. The coefficient span of every
parameter-dependent compatible factored product has rank 13, while adjoining
the pure targets raises rank to 14, 14, and 15. Hence neither pure target lies
in the factored span at any point of (3).

The companion checker is
[`verify_level_two_one_invertible_three_rank_one_all_spokes_nearest_incidence_families.py`](../computations/verify_level_two_one_invertible_three_rank_one_all_spokes_nearest_incidence_families.py).

## 1. Local classification of the arbitrary `M_34` block

Keep the endpoint matrices, potentials, six fixed core blocks, `M_45=0`, and
the seven other core-to-zero spokes from the exact survivor. The
generic-kernel numerator on edge 34 vanishes because
\(\nu_3+\nu_4=0\), so all four entries in (1) are genuinely free.

Exact Singular computation over \(\mathbb Q(a,b,c,d)\) gives

\[
\operatorname{rank}D=55,
\qquad \operatorname{rank}D_{\rm mixed}=54.                 \tag{4}
\]

Thus a general `M_34` perturbation immediately leaves the incidence locus.
At the committed point

\[
(a,b,c,d)=(0,0,29,0),                                      \tag{5}
\]

the mixed matrix has rank 53, right nullity 7, and left nullity 9. Let
\(N\) and \(L\) be exact rational bases of those kernels. For a block
variation \(E(\dot a,\dot b,\dot c,\dot d)\), the standard tangent
obstruction to retaining rank at most 53 is

\[
L^{\mathsf T}E N=0.                                        \tag{6}
\]

The 63 scalar rows in (6) have exact row space

\[
\operatorname{rowspan}(L^{\mathsf T}EN)
 =\langle(0,1,0,-1)\rangle.                                \tag{7}
\]

Consequently the determinantal tangent space is precisely
\(\dot b=\dot d\). Independently, substituting `d=b` makes every 54-minor of
the mixed matrix vanish identically: the function-field rank becomes 53,
while the full differential retains generic rank 55. Since the contained
hyperplane (2) has the full tangent dimension in (7), it is the reduced
rank-53 determinantal germ through (5). This is a local classification of the
nearest component; it does not rule out a remote component elsewhere in the
four-parameter block.

## 2. The smallest coupled cell extension

Now impose (2) and replace the single fixed entry `M_04(0,0)=1` by the
parameter `x`, as in (3). Singular gives the exact function-field ledger

\[
\begin{array}{c|cc}
\text{family}&\operatorname{rank}D&
                    \operatorname{rank}D_{\rm mixed}\\ \hline
M_{34}\text{ arbitrary}&55&54\\
(a,b,c,x)\text{ in (3)}&55&53\\
x=0&53&52\\
M_{34}=0&50&49.
\end{array}                                                  \tag{8}
\]

The input program is generated entirely in memory and pinned by SHA-256

```text
1b968e0d7056d6f18dcb4ec27805d578499579e84f27954a1e6f096da6fc6c51
```

The rank computation is over rational function fields, so the upper bounds
in (8) are polynomial identities for every specialization. At any point of
(3) with rank `D=55`, deleting the two pure rows can reduce rank by at most
two. The mixed upper bound 53 therefore forces equality. Equivalently, the
map from the seven-dimensional mixed kernel onto the two pure rows is
surjective, giving both pure target preimages without choosing a rational
normal form separately at each parameter point.

An exact calibration `(a,b,c,x)=(1,2,3,4)` recomputes

\[
\operatorname{rank}D=55,quad
\operatorname{rank}D_{\rm mixed}=53,quad
\operatorname{rank}[D\mid e_0]
=\operatorname{rank}[D\mid e_1]
=\operatorname{rank}[D\mid e_0,e_1]=55                    \tag{9}
\]

over \(\mathbb Q\), \(\mathbb F_{101}\),
\(\mathbb F_{32003}\), and \(\mathbb F_{1000003}\).

## 3. Generic kernel and uniform R2

Both variable edges join equal-and-opposite potential sites. Their selected
numerators vanish, so changing them preserves every block identity

\[
X_rJX_u^{\mathsf T}=(\nu_r+\nu_u)M_{ru}.                   \tag{10}
\]

The selected equation retains `z=-2` and all 64 rows.

R2 does not depend on a generic noncancellation claim. The checker chooses two
fixed pure-column witnesses for each nonzero root, avoiding both variable
edges, and pins one parameter-independent complementary cofactor for each.
Their values are

\[
2346,3366,2346,28,33,3366,4002,6216,                      \tag{11}
\]

all nonzero. Affineness and every single and pairwise parameter direction are
audited exactly. Sites 4 and 5 still have zero endpoint matrices and preserve
their endpoint witness pair. Thus literal R2 holds on all of (3), including
its rank-55 open subset.

## 4. Uniform L1 systems

For both P/V and Q/U, the committed rational nullspace basis continues to
solve the entire four-parameter coefficient system. Each basis consists of
two genuine core star modes and the sole vacuous `rho_45` direction. The star
components are independent of `a,b,c,x` and vanish at sites 4 and 5.

A parameter-independent subsystem, obtained by omitting the four edge-34
rows and the sole `x`-dependent edge-04 row, has rank 23. Every rank-55 member
has `M_34 != 0` by the last line of (8). Its unique `rho_34` column therefore
raises the rank to at least 24. The three displayed kernel vectors give the
opposite bound, so throughout the rank-55 locus

\[
\operatorname{rank}L_{P/V}
=\operatorname{rank}L_{Q/U}=24,
\qquad \dim\ker=3.                                         \tag{12}
\]

This also rules out a hidden L1 rank jump on a special rank-55 divisor.

## 5. Uniform factored obstruction

Take the four cross-products of the two fixed U modes with the two fixed V
modes. Their output vectors are affine in `a,b,c,x`. Collect the four constant
vectors and all sixteen directional coefficient vectors into one `64 x 20`
matrix. Exact ranks over the four audited fields are

\[
\begin{array}{c|ccccc}
&\text{all coefficients}&+\Psi(M)&+e_0&+e_1&+e_0,+e_1\\ \hline
\operatorname{rank}&13&13&14&14&15.
\end{array}                                                  \tag{13}
\]

The direct vector obeys the pointwise Euler identity

\[
\Psi(M)=2\sum_{i,j=1}^2 d\Psi_M(N_{ij}),                   \tag{14}
\]

for the checker normalization, so it adds no direction. More importantly,
the rank-13 coefficient space contains the four factored outputs for **every**
parameter specialization. Since even this uniform enlargement misses both
pure targets by (13), every genuine bilinear compatible image misses them as
well. The coefficient matrix is pinned by

```text
b64fad8a27c094f6376e220746356656840d473ad00a4dec0a20c820564040d2
```

## 6. Remaining frontier

This closes the entire rank-55 part of the nearest four-parameter coupled
family (3), not the full eight-spoke all-spokes envelope. The next genuinely
new search must deform at least one more independent spoke cell beyond (3),
or free a second full spoke block and recompute the incidence equations. No
point in the families certified here is a full L1/factored survivor.
