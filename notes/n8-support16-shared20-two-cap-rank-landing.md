# Support 16: the shared-`20` two-cap rank landing

The exact checker is
[`verify_n8_support16_shared20_two_cap_rank_landing.py`](../computations/verify_n8_support16_shared20_two_cap_rank_landing.py).

## Theorem

Consider representative `B` of degree sequence `(6,4^5,3^2)`:

```text
01 02 03 04 05 07 14 16 17 23 25 27 35 36 45 46.
```

Let the directed source block at the degree-four endpoint of `02` be

\[
                       X_{20}=w\otimes e_r,
\]

with `w` noncoordinate.  It is the shared role of the minimum cap-`27`
face, hence invisible to that face's crossed two-term tensor.  Assume the
remaining roles of the exceptional chart are the normalized
mutual-coordinate anchors forced at the degree-four stars.  Then one of the
two independently typed physical caps `23` and `25` has an active clean
covector `K`: its complete homogeneous response vanishes, its direct scalar
is nonzero, and all three diagonal target readouts are nonzero.

No relation identifying `K23` and `K25` is used.  The common source datum is
the single vector `w`; the two caps test two distinct coordinates of it.

## 1. Literal response placement

For a cap `pq`, every residual factor is expanded as

\[
 R_{ij}^{pq}(K)=
 K\mathbin{\lrcorner}(X_{pi}\otimes X_{qj})
 +K\mathbin{\lrcorner}(X_{pj}\otimes X_{qi}).          \tag{1}
\]

The corrected source-placement audit gives the complete factor-level
responses

\[
 E_{23}=x_{14}\bigl(R_{05}R_{67}+R_{06}R_{57}+R_{07}R_{56}\bigr), \tag{2}
\]

\[
 E_{25}=x_{16}\bigl(R_{03}R_{47}+R_{04}R_{37}+R_{07}R_{34}\bigr). \tag{3}
\]

After (1), each has four oriented monomials: two contain `X20`, and two do
not.  Thus merely putting `w` in a kernel does not finish the proof; the two
companion monomials must also cancel.

In the exceptional mutual-anchor chart, let `a` be the direct anchor colour
of the selected cap and let `b,c` be the other two colours.  The two companion
monomials have the same far tensor and their coefficient is precisely

\[
                     P_{bc}(K)=K_{bb}K_{cc}+K_{bc}K_{cb}.       \tag{4}
\]

At cap `23`, `a` is the colour of `X23`; the row anchors are `X25,X27` and
the column anchors are `X30,X36`.  At cap `25`, `a` is the colour of `X25`;
the corresponding pairs are `X23,X27` and `X50,X54`.  The checker enumerates
all 104 anchor completions after fixing the colour of `X23` and verifies
these complementary-colour statements literally.

## 2. Denominator-cleared rank construction

Write the coordinates of `w` in the order `(a,b,c)` as `(A,B,C)` and first
assume `AB != 0`.  In that ordered basis set

\[
K_B=
\begin{pmatrix}
 AB & B(C-B) & -B(B+C)\\
 -A^2 & AB & AB\\
 0 & -AB & AB
\end{pmatrix}.                                             \tag{5}
\]

Direct multiplication gives

\[
 w^TK_B=0,\qquad
 (K_B)_{aa}=(K_B)_{bb}=(K_B)_{cc}=AB,
 \qquad P_{bc}(K_B)=0.                                    \tag{6}
\]

If instead `AC != 0`, use

\[
K_C=
\begin{pmatrix}
 AC & C(C-B) & -C(B+C)\\
 0 & AC & AC\\
 -A^2 & -AC & AC
\end{pmatrix}.                                             \tag{7}
\]

It satisfies the same identities with `AC` in place of `AB`.  Equations
(5) and (7) are denominator-cleared forms of the two localization charts;
the checker proves all polynomial identities for all six orders of
`(a,b,c)`.

The equation `w^TK=0` kills both oriented terms containing the source block
`X20`, irrespective of the common companion block `X35`.  Equation (4)
kills the two-term residue.  The common nonzero diagonal in (6) preserves all
three pure-target cap readouts, and its `aa` entry is the direct scalar.

## 3. Why one of the two caps works

The direct colours on `23` and `25` are distinct because `23,25,27` are the
three normalized anchors at vertex `2`.  If both corresponding coordinates
of `w` vanished, `w` would be supported on only the third coordinate and
would be coordinate—contrary to hypothesis.  Hence one cap has `A != 0`.
Since `w` is noncoordinate, at least one of the remaining `B,C` is also
nonzero, placing that cap in chart (5) or (7).

The checker exhausts the 24 combinations of an ordered pair of distinct
direct colours and a noncoordinate support mask.  Every combination chooses
one of the twelve symbolic rank charts.  Therefore the simultaneous local
failure stratum is empty: no normalized exact guard survives at this orbit.

This theorem is conditional only on the stated mutual-coordinate companion
anchor chart.  A directed-coordinate block with a mismatched far label is a
different scope case, as in the earlier support-16 audit.

## Reproduction

```sh
python3 computations/verify_n8_support16_shared20_two_cap_rank_landing.py
python3 -O computations/verify_n8_support16_shared20_two_cap_rank_landing.py
python3 -I -S computations/verify_n8_support16_shared20_two_cap_rank_landing.py
```

Pinned ledger SHA-256:

```text
a97ff705d10246af9966732fe6e95f3e2b557fbdd1a68271327f80ed16b8f73d
```
