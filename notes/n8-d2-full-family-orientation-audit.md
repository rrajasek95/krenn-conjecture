# Independent D2 audit: all census families, endpoint orientations, and signature composition

Date: 2026-08-08.

Checker:
[`computations/verify_n8_d2_full_family_orientation_audit.py`](../computations/verify_n8_d2_full_family_orientation_audit.py).

Audited artifact:
[`notes/n8-d2-kill-and-monochrome-rigidity.md`](n8-d2-kill-and-monochrome-rigidity.md)
and its checker.  The audit pins the checker at SHA-256
`6320c3bdb795df3050952e52bd9c0fb9f4d5f2cdbf9eb543cd3467179630a745`.

## 1. Verdict

The finite orientation and relabelling gaps in the D2 argument are closed.
The 48 census families have \(48\cdot2^3=384\) choices of essential endpoint.
Exactly 288 are incompatible with saturation already from (E1).  The other
96 form two 48-element orbits, distinguished by the orientation of the sole
\(S_b\)--\(S_c\) carrier.  Exact polynomial sweeps of representatives of both
orbits obstruct all \(2\cdot8^3=1024\) named-family branch combinations, with
the same tally in each orientation:

\[
 128\text{ anchor-dead},\qquad
 192\ \Gamma\text{-certificates},\qquad
 192\ c\text{-factor certificates},\qquad
 0\text{ survivors}.
\]

The checker also composes the seven outputs of the Signature Lemma over all
\(7^3=343\) three-carrier signature profiles.  All 343 are obstructed.  Thus
the named-family list is not being treated as exhaustive: the downstream
machine implication is explicitly

\[
 \boxed{\text{Signature Lemma}\Longrightarrow
        \text{every D2 U-system profile is certificate-dead}.}
\]

The Signature Lemma itself remains an ordinary algebraic hand proof over
\(\mathbb C\), reproduced in Section 4.  The checker verifies the complete
Boolean case partition and both two-endpoint cases, but it does not claim
that a finite-field census is a proof over \(\mathbb C\).

## 2. All endpoint orientations

Write the canonical split as

\[
 S_b=\{0,1\},\quad S_c=\{2,3\},\quad S_a=\{4,5,6,7\},
 \qquad \chi=(b,b,c,c,a,a,a,a).
\]

Every D2 family has one \(S_b\)--\(S_c\) carrier and two carriers joining an
uncovered small-part site to \(S_a\).  Orient a carrier as \((u,p)\), with
\(u\) essential and \(p\) its partner.  If an \(S_a\)-endpoint is made
essential, then \(\chi_u=a\).  For the residue
\(R=\{r_0,r_1\}\subset S_a\), (E1) gives

\[
 A_{ur_0}(a,a)=A_{ur_1}(a,a)=0
\]

because neither residue site is \(p\).  The T-part of four-site purity says
that, at the saturating crossing cell,

\[
 -\nu A_{up}(\chi_u,\chi_p)
 =s_e(\chi)
 =A_{ur_0}(a,a)A_{pr_1}(\chi_p,a)
  +A_{ur_1}(a,a)A_{pr_0}(\chi_p,a)=0.
\]

Here \((\chi_u,\chi_p)\ne(a,a)\), so there is no \(m_e\) term.  Saturation
requires this carrier cell to be nonzero, a contradiction.  Consequently
both \(S_a\)-incident carriers must be oriented from the small endpoint into
\(S_a\).  The \(S_b\)--\(S_c\) carrier retains its two orientations.  This is
the uniform \(6+2\) split which the checker obtains separately for every one
of the 48 census families:

\[
 384=288\text{ E1/saturation-dead}+96\text{ viable}.
\]

This is stronger and more precise than the earlier inspection that
orientation should be inert: six orientations do not need an inertness
argument at all.

## 3. Relabelling equivariance

The split-preserving group is \(S_2\times S_2\times S_4\), of order 96.  The
checker constructs it without importing the old orbit table and verifies:

1. every group element preserves \(\chi\);
2. it bijects all 105 perfect matchings, all 252 endpoint-ordered cells, and
   all 6561 colour words;
3. when a site permutation reverses the stored order of an edge, the two
   endpoint colours are transposed rather than symmetrized;
4. the complete label-sensitive schemas of (E1), the U-relations, the
   T-relations, residue purity, and all seven signature types map exactly to
   the schemas built directly on the image geometry.

The two viable canonical orientations are

\[
 ((0,2),(1,4),(3,5)),\qquad ((2,0),(1,4),(3,5)).
\]

Their orbits are disjoint and have size 48 each; their union is exactly the
96 viable oriented census families.  Omitting the second orbit leaves exactly
48 orientations uncovered, which is the negative control.

Because a hafnian coefficient is a sum over perfect matchings of products of
endpoint-ordered cells, items 1--4 transport each polynomial identity and
its certificate words literally.  The first representative uses the pinned
committed sweep.  The checker independently rebuilds the skeleton for the
second representative and verifies all 512 combinations in exact sparse
polynomials over \(\mathbb Q\).  This removes the previous inspection-only
equivariance step.

## 4. Signature Lemma, independently rederived

For one oriented carrier \((u,p)\), put

\[
 x_k=A_{ur_0}(\cdot,k),\quad y_l=A_{ur_1}(\cdot,l),\quad
 z_k=A_{pr_0}(\cdot,k),\quad w_l=A_{pr_1}(\cdot,l).
\]

The U-system is

\[
 x_kw_l^T=-y_lz_k^T\qquad ((k,l)\ne(a,a)),                 \tag{1}
\]

and saturation is

\[
 s=x_aw_a^T+y_az_a^T\ne0.                                 \tag{2}
\]

We use only the elementary field fact that a nonzero outer product has both
factors nonzero, and that equality of two nonzero rank-one outer products
makes the corresponding left and right factors proportional.

Suppose first that \(u\) feeds both residue sites: \(x_k\ne0\) and
\(y_l\ne0\) for some \(k,l\in\{b,c\}\).  If \(z_k=0\), equations
\((k,l')\) force every \(w_{l'}=0\), and then equations \((k',l)\) force
every \(z_{k'}=0\).  Equation (2) is zero, a contradiction.  If \(z_k\ne0\),
equations \((k,a)\) and \((k,l)\) give scalars \(c,c'\), with \(c'\ne0\),
such that

\[
 y_a=cx_k,\quad w_a=-cz_k,\qquad
 y_l=c'x_k,\quad w_l=-c'z_k.
\]

Equation \((a,l)\) then gives \(x_az_k^T=x_kz_a^T\), and substitution makes
\(s=c(-x_az_k^T+x_kz_a^T)=0\), again a contradiction.

If \(u\) feeds \(r_0\) and \(p\) feeds \(r_1\), then some outer product
\(x_kw_l^T\) is nonzero; (1) forces \(y_lz_k^T\) nonzero and reduces to the
preceding case.  The opposite mixed case is symmetric.  The only Boolean
case left is that \(p\) feeds both sites while \(u\) feeds neither.  Then
\((k,a)\) forces \(y_a=0\) and \((a,l)\) forces \(x_a=0\), so (2) again
vanishes.  These four cases cover all \(3\times3=9\) nonempty two-site feed
patterns; the checker enumerates that partition and requires every class to
be exercised.

Thus a saturated solution feeds at most one residue site.  Its signature is
one of the seven possibilities

\[
 (\varnothing,\varnothing),\quad
 (\{u\},\varnothing),(\{p\},\varnothing),(\{u,p\},\varnothing)
\]

and their \(r_0\leftrightarrow r_1\) mirrors.

It remains to justify the structure used by the c-factor certificate.  If
\(P_{r_0}=\{u,p\}\), then the two-colour columns of \(y_l,w_l\) vanish.
Equation (1) reduces to

\[
 x_kw_a^T=-y_az_k^T\qquad(k=b,c).                            \tag{3}
\]

If \(y_a=0\), the nonzero \(x_k\) forces \(w_a=0\), contradicting (2).
Similarly \(w_a\ne0\).  Hence (3) gives scalars \(c_k\) with

\[
 x_k=-c_ky_a,\qquad z_k=c_kw_a\qquad(k=b,c).                 \tag{4}
\]

This is exactly the extended-exchange structure; the near \(a\)-columns
remain free.  The \(r_1\) case is identical.  Therefore the c-factor
certificate applies to both two-endpoint signatures.

This proof is over \(\mathbb C\) (indeed over any field) and does not use the
GF(2) census.  The finite-field census remains an independent instance-level
check, not the justification for the universal quantifier.

## 5. Downstream signature composition

Conditional on the preceding lemma, each carrier has seven possible
signatures.  The exact \(7^3\) composition table is:

| certificate | profiles |
|---|---:|
| anchor death | 127 |
| \(\Gamma\) | 144 |
| c-factor | 72 |
| survivor | **0** |

This is the same pigeonhole at the signature rather than named-family level:
three carriers feed two residue sites, so one site has zero or one carrier.
Zero gives anchor death.  A singleton endpoint gives \(\Gamma\); two endpoints
from the same carrier give the extended-exchange c-factor.

As a dependency check, the verifier also requires a deliberately forbidden
profile in which every carrier feeds both residue sites to have no downstream
certificate.  Thus the zero-survivor count genuinely consumes the Signature
Lemma instead of following from an accidentally stronger certificate table.

## 6. Scope and remaining dependencies

This audit closes the D2 orientation and relabelling inspections.  It also
separates the universal Signature Lemma from the finite-field evidence and
checks every downstream signature profile.  It does not independently
reprove the census-to-D1/D2 reduction, Lemma F, or the good-crossing results
which supply the D2 skeleton.  Those remain the upstream hand-proof audit
dependencies recorded in the companion artifacts.

Nothing here addresses the residual D1 cell outside \(\Sigma\), and nothing
extends the N=8 census to higher orders.  Krenn's conjecture remains open.

## 7. Verification

~~~text
python3       computations/verify_n8_d2_full_family_orientation_audit.py
python3 -O    computations/verify_n8_d2_full_family_orientation_audit.py
python3 -I    computations/verify_n8_d2_full_family_orientation_audit.py
python3 -S    computations/verify_n8_d2_full_family_orientation_audit.py
python3 -I -S computations/verify_n8_d2_full_family_orientation_audit.py
python3 -m py_compile computations/verify_n8_d2_full_family_orientation_audit.py
~~~

Frozen exact ledger digest:

~~~text
5639dcd6e203759b5f95e3409bc2b5679018d6febbc013ff0b22a1ecb2c7fcb8
~~~
