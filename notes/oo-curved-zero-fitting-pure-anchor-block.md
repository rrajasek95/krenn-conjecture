# A literal pure anchor does not lift a zero-Fitting mixed SCC

## Outcome

There is an exact uniform block formula.  Let (M) be the square coefficient
matrix of a critical mixed source component.  Homogenize the normalized
target value by a column (tau).  Every genuinely mixed full-output row has
zero (tau)-coefficient, while a pure diagonal row has coefficient (-1).
After arbitrary reductions of the pure row into the mixed classes, the
augmented matrix is therefore

\[
 \widetilde M=
 \begin{pmatrix}
     M&0\\ h^T&-1
 \end{pmatrix},
 \qquad
                  \boxed{\det\widetilde M=-\det M}.       \tag{1}
\]

Consequently one literal normalized pure row cannot lift a zero-Fitting
mixed SCC.  This is not a rank heuristic: it is forced by output grading.

The smallest possible nontrivial coupling would have to be

\[
 \widehat M=
 \begin{pmatrix}
     M&g\\ h^T&\alpha
 \end{pmatrix},
 \qquad
 \det\widehat M
   =\alpha\det M-h^T\operatorname {adj}(M)g.              \tag{2}
\]

On the zero-Fitting locus, the exact missing scalar is therefore

\[
                  \boxed{-h^T\operatorname {adj}(M)g}.     \tag{3}
\]

The literal pure row can supply (h) and (alpha), but mixed target grading
sets (g=0).  A proof must construct (g) from an additional source-provenant
word-changing/connection row.  Curvature, goodness, activity, and RR
alignment do not themselves provide that connector.

## 1. The minimal two-cycle formula

For

\[
 M=\begin{pmatrix}A&B\\C&D\end{pmatrix},
\]

the coupled determinant is

\[
 \alpha(AD-BC)
 -h_0(Dg_0-Bg_1)-h_1(-Cg_0+Ag_1).                        \tag{4}
\]

The balanced parallel component from `4e168f4` has (AD=BC).  Equation (4)
then shows exactly what a successful anchor comparison must prove.  Merely
adjoining the anchor gives (g_0=g_1=0), so every term vanishes.

This also separates the result from the minimum active two-row unit in
`726deeb`.  There the mixed row is a one-class monomial pivot (yz=0), not a
zero-Fitting SCC.  Multiplying it by (x) and subtracting the pure row
(xyz-1) gives the unit directly.  The present obstruction begins only after
all such private pivots have failed and a critical mixed component remains.

## 2. Rational same-packet counterguard

The 177-cell packet of `b942209` admits a nonzero rational weighting that
satisfies the requested mixed-plus-pure subsystem.  Give every supported
cell weight (1), except

```text
23:12 = -1,
36:00 = -4.
```

For the two parallel mixed words

```text
20120121,
21120121,
```

the two matching values are respectively (-1,+1).  Both literal mixed
source rows vanish.  Their exponent rectangle still has (AD=BC).

The pure word `00000000` has six live matchings.  Their values are

```text
1, 1, 1, -4, 1, 1,
```

so their sum is exactly (1), the normalized pure-0 diagonal target.
Nevertheless its target-bearing augmented determinant is zero by (1).

At this same rational point the complete local OO ledger remains

```text
direct-arm ranks:        1,1
deleted-star ranks:      3,3,3,3
curvature:              -1
both arm cofactors:      active
target-2 ruling sites:   3 and 2
```

Thus even the literal pure anchor plus curvature, goodness, activity, and
RR alignment does not force the missing Schur scalar (3).

## 3. Exact scope and next theorem

The rational weighting is a counterguard to the three-row augmentation
claim, not a full source: the odd triangle from `b942209` remains on the
same active torus and still has determinant (2K).  Hence the complete mixed
ideal of this packet is the unit ideal.

The exact proof-completing alternative is now sharper.  For every zero
critical SCC reached after signed saturation, one must produce either

1. another mixed SCC with nonzero character/Fitting determinant; or
2. a literal grade-changing connector (g) for which
   (h^T\operatorname {adj}(M)g\ne0); or
3. a source switch lowering the zero component.

A lone pure unary/diagonal anchor is not a fourth alternative.

## 4. Verification

The standard-library checker
[`verify_oo_curved_zero_fitting_pure_anchor_block.py`](../computations/verify_oo_curved_zero_fitting_pure_anchor_block.py)
verifies (1)--(4) as sparse symbolic determinants, reconstructs the two
literal mixed rows and six-term pure row at the rational weighting, and
re-audits every local OO invariant.  It pins the signed-cycle theorem from
`4e168f4` and records that the full-packet odd circuit remains active.

This is a uniform source-graded block lemma plus a sharp rational subsystem
counterguard.  It does not construct a Krenn counterexample.
