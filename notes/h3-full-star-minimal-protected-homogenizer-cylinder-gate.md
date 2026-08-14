# The protected full-star augmentation has a common 90-term base, but not yet a physical common base

## Verdict

After adjoining the homogenizer carrier and retaining every relative
Taylor--Spencer presentation, the coefficient obstruction disappears.
There is an exact common augmentation

\[
 V=\mathbf Q\{M:M\text{ is a direct-free pure matching}\}
      \cong \mathbf Q^{90}.                           \tag{1}
\]

The normalized full-star response carrier and the literal private `B`
boundary of physical `r0` both map to

\[
                         \mathbf 1_V=\sum_M M.         \tag{2}
\]

Thus it is wrong to obstruct the comparison merely by declaring the two
90-term copies orthogonal.  This is the useful positive part of the audit.

It does **not** yet give the physical cylinder.  Map (1) forgets the source
word, fine/repeated labels, the response/cap operation idempotent, the Eq
row and target normalization.  The current constructors do not prove that
the response and cap complexes are projective resolutions of one object in
that enriched category.  The exact missing datum is a labelled
`K_Eq/AugP2` common augmentation.  If that datum is supplied, ordinary
projective comparison lifts `id_V`, and the pinned linear landing theorem
forces the lift to be the unique root-tied, residual-zero, `B=Eq` solution.

Exact checker:
[`verify_h3_full_star_minimal_protected_homogenizer_cylinder_gate.py`](../computations/verify_h3_full_star_minimal_protected_homogenizer_cylinder_gate.py).

## 1. Homogenized Euler carrier

Let

\[
 G_0=\sum_{i=1}^7x_{0i}\iota_{0i}(e)+u\iota_u(e).    \tag{3}
\]

The first summand has boundary `H`; the homogenizer summand contributes
`-u`, so

\[
                              dG_0=H-u.                \tag{4}
\]

This is an exact response-side carrier.  It does not itself change the
operation parent `response -> response` into `response -> cap`.

## 2. Minimal protected Taylor--Spencer presentation

For the fixed pair `(01),(07)`, retain all 144 ordered matching-parent
pairs.  They collect to 135 squarefree lcms; nine degree-eight lcms have two
presentations.  The minimal deletion to the two four-cell collision branches
has 1,020 deleted-factor restriction squares.

The protected first-stage totalization is:

| family | labelled cells | projected rank |
|---|---:|---:|
| deleted-factor relative cylinders | 1,020 | 24 on the 24 branches |
| ambiguous-lcm presentation cylinders | 9 | 7 paired, 14 with sides separated |

Each deleted-factor cylinder receives a private degree-zero slack.  If its
branch reinserts to parent `M`, the slack also augments to `M`; hence

\[
 \epsilon(dK)=\epsilon(\text{branch})-\epsilon(\text{slack})=M-M=0. \tag{5}
\]

The ambiguity cylinders likewise retain both parent labels and separate
private slacks.  They do not quotient two nonzero `H0` classes merely because
their unlabelled lcms coincide.  This is the presentation-safe meaning of
the cylinders; no branch is declared an absolute boundary.

## 3. Exact common occurrence augmentation

Partition the 90 matchings by their unique site-0 partner.  The sector sizes
are

```text
partner             1   2   3   4   5   6   7
sector size        12  12  15  12  12  15  12
```

For every unordered pair `{i,j}`, trigger reinsertion sends the two collision
branches back to the parent sectors `V_i+V_j`.  Every partner occurs in six
of the 21 pairs.  Therefore, term by term,

\[
 {1\over6}\sum_{1\leq i<j\leq7}(\mathbf 1_{V_i}+\mathbf 1_{V_j})
       =\sum_{i=1}^7\mathbf 1_{V_i}=\mathbf1_V.        \tag{6}
\]

The private full-nine boundary of `r0` is also one copy of every one of the
90 matching parents.  Hence

```text
normalized response augmentation     1_V
physical r0 private-B augmentation   1_V
difference rank                         0.
```

This equality uses literal parent matchings; it is stronger than equality of
one aggregate scalar.

## 4. Why projective comparison is still conditional

The two vertical coefficient polynomials are both `H-u`, but they are
currently attached to different labelled rows:

```text
response side       coefficient/EqSystem row, operation e_R A e_R
cap side            reduced-Eq row of r0, operation e_C A e_C
```

The cap generator also has normalized target one.  Forgetting these labels
produces (1), but it does not construct the horizontal arrow.  The first
remaining square after the relative deletion cylinders is therefore

\[
\begin{array}{ccc}
 G_0 & \dashrightarrow & r_0\\
 \downarrow && \downarrow\\
 (H-u)_{\rm response}&\dashrightarrow&(H-u)_{\rm Eq}.
\end{array}                                             \tag{7}
\]

Both dashed arrows are instances of the same missing mixed operation
corner `e_C A e_R`.  The exact common-base map needed to fill (7) must send

```text
normalized Euler carrier epsilon_AB, epsilon_AC    -> r0_AB, r0_AC
response coefficient c_AB, c_AC                    -> -E_AB, -E_AC
literal seven-dimensional residual                 -> 0
target                                               1 -> 1.
```

The pinned 180-term private landing calculation proves that this is the
unique formal natural solution.  It does not prove that the labelled mixed
operation exists.

After quotienting by the exact common `V` augmentation, the normalized
operation-corner covector is

\[
 \omega_{\rm mix}={1\over2}\left(
       (e_CAe_R)_{AB}^{*}+(e_CAe_R)_{AC}^{*}\right).   \tag{8}
\]

It vanishes on the response/cap diagonal core, all 2,040 two-root
deleted-factor cylinders and all 18 two-root ambiguity cylinders, and has
value one on the desired root-natural comparison.  The rank ladder is

```text
diagonal core                                      6
+ 2 x 1020 protected deleted cylinders          2046
+ 2 x 9 protected ambiguity cylinders           2064
+ one natural mixed comparison schema            2065.
```

This covector detects the operation grade only; it does not re-separate the
already identified 90 coefficient coordinates.

## 5. First raw face and exact scope

Before adding its relative cylinder, the lexicographically first failed
restriction square is

```text
M = (01)(23)(45)(67)
N = (07)(12)(34)(56)
L = M union N
K = (07)(23)(45)(67)
E = (01)(12)(34)(56)
q = (01).
```

Deleting `q` from `L` and then `E\{q}` leaves the nonzero branch `K`, while
`D_q(K)=0` because `q` is absent.  Its private cylinder repairs this face
relative to the parent augmentation as in (5).  After all 1,020 such first
faces and the nine ambiguity presentations are retained, the first
unconstructed face is the operation-labelled square (7).

All counts, ranks, sectors, reinsertion identities and rational covector
values are exact for the canonical `h=3`, direct-free, two-root packet.  The
result proves equality in the common 90-term occurrence base, not an actual
full decorated-source comparison.  No untracked common-augmentation artifact
is imported.

## Verification

```text
python3 computations/verify_h3_full_star_minimal_protected_homogenizer_cylinder_gate.py --mode all
python3 computations/verify_h3_full_star_minimal_protected_homogenizer_cylinder_gate.py --mode cylinders
python3 computations/verify_h3_full_star_minimal_protected_homogenizer_cylinder_gate.py --mode first-face
python3 computations/verify_h3_full_star_minimal_protected_homogenizer_cylinder_gate.py --mode coupling
python3 computations/verify_h3_full_star_minimal_protected_homogenizer_cylinder_gate.py --mode dual
python3 -O computations/verify_h3_full_star_minimal_protected_homogenizer_cylinder_gate.py --mode all
python3 -I -S computations/verify_h3_full_star_minimal_protected_homogenizer_cylinder_gate.py --mode all
```

Frozen ledger SHA-256:

```text
a347b299d41da029470016fc24fa3eeb92cbdeb82149fac32376932d1f6b1e0d
```
