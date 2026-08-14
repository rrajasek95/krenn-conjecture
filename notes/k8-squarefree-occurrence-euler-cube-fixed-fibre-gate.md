# The complete K8 Euler cube selects one matching but does not descend to `P_f`

## Outcome

Let

\[
 H=\operatorname {Haf}(K_8)=\sum_{M\in\operatorname {PM}(K_8)}m_M
\]

be the complete `105`-term hafnian, and fix a perfect matching
`f={e_1,e_2,e_3,e_4}`.  The four commuting logarithmic coordinate
derivations

\[
 E_e=x_e\partial_{x_e}
\]

give the exact coefficient selector

\[
                       \prod_{e\in f}E_e(H)=m_f.       \tag{1}
\]

The full four-cube is formally flat, but it is not a physical operation on
the fixed source fibre `H-u=0`.  Its first singleton face is already the
nonzero `15`-term partial hafnian

\[
                E_e(H-u)=H_e=\sum_{M\ni e}m_M,         \tag{2}
\]

and `H_e` is not in the principal source ideal `(H-u)`.  At the top the
corresponding defect is `m_f`.  Thus the order-four Euler cube gives a
relative occurrence Spencer/Kodaira--Spencer carrier.  It does **not** give
the physical pointed conormal `P_f=d(u_f-u)`.

The executable exact audit is
[`verify_k8_squarefree_occurrence_euler_cube_fixed_fibre_gate.py`](../computations/verify_k8_squarefree_occurrence_euler_cube_fixed_fibre_gate.py).

## 1. The complete cubical and Hasse totalizations

For `S subset f`, put `E_S=product_(e in S) E_e`.  The sixteen coefficient
vertices have support sizes

```text
|S|                 0    1    2    3    4
|supp E_S(H)|     105   15    3    1    1
```

Fixing three disjoint edges already forces the fourth.  Hence every
three-edge face and the four-edge top equal `m_f`: the fourth Euler step adds
an operation label but no new coefficient information.

The cube has `16` vertices, `32` edges, `24` squares, `8` three-cells, and
one four-cell.  Every square has zero commutator and all `24` paths from
bottom to top give (1).  Its cellular chain dimensions and ranks are

```text
C_k:       16, 32, 24, 8, 1
rank d_k:      15, 17, 7, 1,
```

so the augmented geometric cube is contractible.

That cellular contraction is not the source descent.  The genuine
squarefree Spencer/Hasse prolongation of the row `r` with
`d r=(H-u)e` has sixteen row generators and

\[
 d r[U]=\sum_{S\subseteq U}E_S(H-u)e[U\setminus S].   \tag{3}
\]

Applying the product rule in any order gives the same packet.  Across all
sixteen rows, (3) has

\[
                     \sum_{U\subseteq f}2^{|U|}=3^4=81
\]

module faces.  The top boundary contains all sixteen terms, from
`(H-u)e[f]` through the proper faces down to `m_f e[empty]`.  Thus (1) is
the scalar face of a full Hasse packet, not an isolated boundary assignment.

## 2. The first nonphysical face is order one, not curvature order two

A derivation descends to the quotient by `H-u` only if it preserves that
ideal.  Give `u` degree four.  Every positive `E_S(H-u)` also has degree
four, so membership in the principal ideal `(H-u)` would force scalar
proportionality.  In the monomial basis consisting of the `105` matchings
and `u`, the checker finds

\[
             \operatorname {rank}(H-u,E_S(H-u))=2
             \qquad(\varnothing\ne S\subseteq f).      \tag{4}
\]

This proves nonmembership for all fifteen positive faces.  The same
support-rank argument works for the zero target equation `H=0`.  On the
literal normalized pure fibre `H=1`, if `H_e=(H-1)q`, highest-degree
comparison in the polynomial domain forces `q` to be constant and constant
terms then force `q=0`, again contradicting `H_e ne 0`.  The checker audits
that normalized support/rank calculation for all fifteen faces as well.

Consequently the first row packet is

\[
                  d r[e]=(H-u)e[e]+H_e e[\varnothing], \tag{5}
\]

and the diagonal projection which forgets positive jets has chain defect
`H_e e[empty]`.  At the fourfold top its defect is `m_f e[empty]`.

There is no hidden two-face curvature: all `24` commutator squares vanish.
The exact diagnosis is a flat formal connection with a nonzero normal
one-form.  Flatness among coefficient directions does not make those
directions tangent to the physical source fibre.

## 3. Why this is not the old `D4`

The pure fourth derivative and the logarithmic Euler composite have
different scalar faces:

\[
                \partial_f H=1,
                \qquad E_fH=m_f.                      \tag{6}
\]

Both require the full Boolean product-rule packet and both fail uncorrected
source-ideal descent.  But the committed `D4` artifact is a special cycle in
a direct-free `90`-term mixed/pure two-row target cone; its diagonal defect
is `(H_0-u)e_0`.  The present object is the raw complete `105`-term pure-row
Euler packet, whose first/top defects are `H_e` and `m_f`.  It supplies
neither the moving-target face nor the mixed-row comparison of `D4`.

Thus the common four-cube shape is not a source-valid identification of the
two cells.

## 4. Exact comparison with `c_f` and `P_f`

Use conormal coordinates `(dz_f,dZ,du)`, where `Z` is the sum of all `105`
matching-occurrence coordinates.  The three relevant normals are

\[
 B=(0,1,-1),\qquad
 c_f=(105,-1,0),\qquad
 P_f=(1,0,-1).                                         \tag{7}
\]

The raw Euler top is `dz_f`, and subtracting the response mean gives
`c_f/105`.  This is exactly the relative centered-occurrence/KS shadow.
However,

\[
 \operatorname {rank}(B,P_f)=2,
 \qquad \operatorname {rank}(B,P_f,c_f)=3,             \tag{8}
\]

with the explicit relation

\[
                         c_f+B=105P_f+104du.            \tag{9}
\]

The common-scale tangent `(1,1,1)` kills `B` and `P_f` but reads `c_f` as
`104`.  Therefore the centered Euler carrier cannot be derived from the
old pointed conormal without one independent global-target normalization.

There is an important but information-losing shadow.  If one first pulls
back to the strict fibre `du=0` and then quotients by `B=dZ`, (9) reduces to

\[
                              c_f=105P_f.               \tag{10}
\]

This explains why the Euler selector can look like `P_f` in a fixed-fibre
coarse quotient.  It does not construct the global pointed cell: the
pullback killed exactly the `-du` face which distinguishes `P_f` in the
source resolution.

## 5. Sharp remaining input and scope

The first possible positive repair is not another resultant or a declaration
that the top is physical.  It is a source-labelled lift of the four
singleton normals `H_e`, totalized through all `81` product-rule faces and
coupled to an independent global target/anchor `-du` face.  If such a lift
exists, its centered quotient is the already known relative KS carrier and
its pointed comparison can then be tested against `P_f`, `D4`, word, ridge,
and physical `q`.

This is exact for one complete `105`-term pure-colour `K8` hafnian row, both
with the moving normalization `H-u` and the literal normalized fibre `H=1`.
It checks all sixteen Hasse rows, all cube edges and squares, and every
product-rule face.  It does not check the other pure-colour targets, the
other `3^8` word equations, construct a full GHZ source tensor, or assign
cap/residue/q readouts.  The negative conclusion is nevertheless
source-valid: an uncorrected operator which fails to preserve even this
defining pure row cannot be an endomorphism of a fuller physical source
quotient.  A new relative physical correction remains viable.

## Verification

Run all three modes:

```text
python3 computations/verify_k8_squarefree_occurrence_euler_cube_fixed_fibre_gate.py
python3 -O computations/verify_k8_squarefree_occurrence_euler_cube_fixed_fibre_gate.py
python3 -I -S computations/verify_k8_squarefree_occurrence_euler_cube_fixed_fibre_gate.py
```

The checker prints its frozen ledger SHA-256.

```text
e54d9752e616c692bbdd2c55c8081f7b9cb7e18282c6a68d099016787fd0cd87
```
