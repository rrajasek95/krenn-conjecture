# Independent audit of the cap-condition projective-height obstruction

## Verdict

**PASS.** A clean-room reconstruction found no algebraic, projective,
ideal-theoretic, or scope defect in
[`cap-condition-projective-height-obstruction.md`](cap-condition-projective-height-obstruction.md).
Projective height alone cannot select a zero on which
\(s\kappa_0\kappa_1\kappa_2\ne0\). The exact abstract signature proves this
even after imposing the full linear GHZ contraction identity.

This is a negative result about a proposed proof method, not a counterexample
to the Krenn conjecture. The signature is deliberately abstract: it is not
claimed to be the boundary signature of one realizable common-edge aggregate
source. A positive descent theorem may still follow from the omitted nonlinear
common-edge relations.

## Frozen inputs and independent artifact

The audited primary files had SHA-256 digests

```text
4a4ce688a5835c7d887df86c332bed420e83c7f920768c054a41631465f6fb82  notes/cap-condition-projective-height-obstruction.md
05c0cad18f5d820e025e6c1a93127fe6a288cfa1639bc8509045b3a873a60583  computations/verify_cap_condition_projective_height_obstruction.py
```

The scope comparison used these frozen dependencies:

```text
42393b760c6575e899604502476b9470d61b01ed1cdfd920eb49066b0d3cbb1c  notes/global-cap-span-descent.md
660c682c6b4c6d383e7eed5041e01c0e41c61efb4acc0ddecadf3e561eca96de  notes/cap-adjugate-six-boundary-identity.md
```

The independent checker
[`audit_cap_condition_projective_height_obstruction_independent.py`](../computations/audit_cap_condition_projective_height_obstruction_independent.py)
imports neither primary file. Its SHA-256 digest is

```text
ca633c152e0ee425dfdd8282bef011b15de2dfb62bd4bd84e0c82015f12d67a7
```

and its frozen semantic-ledger digest is

```text
de90db6ab15da34489530cfd9f5ae6f233cb0d01cbba32736a968ae12d5527dd
```

## 1. Denominator clearing

Put \(c_j=C_j/s\). Direct expansion, using commutativity of the even site
degrees, gives

\[
\begin{aligned}
L_6+L_4(x+L_2)
&=c_6-c_2c_4+\frac13c_2^3
 +(c_4-\tfrac12c_2^2)(x+c_2)\\
&=c_6+c_4x-\frac12c_2^2x-\frac16c_2^3.
\end{aligned}
\]

Multiplication by \(6s^3\) therefore gives exactly

\[
D=6s^2(C_6+C_4x)-3sC_2^2x-C_2^3.
\]

Every \(s,C_2,C_4,C_6\) is linear in the cap covector and \(x\) is fixed.
Every monomial of \(D\) consequently has cap degree three. Its values lie in
the six-site boundary tensor space, of dimension \(3^6=729\), so it supplies
at most 729 homogeneous cubic coordinate equations. The formula itself is
polynomial and remains meaningful on \(s=0\); only its derivation used the
temporary chart \(s\ne0\).

Under the contracted GHZ identity

\[
C_6+C_4x+\frac12C_2x^2+\frac16sx^3
 =T:=\sum_{i=0}^2\kappa_iX_i,
\]

substitution gives

\[
\begin{aligned}
D
 &=6s^2T-s^3x^3-3s^2C_2x^2-3sC_2^2x-C_2^3\\
 &=6s^2T-(sx+C_2)^3.
\end{aligned}
\]

The binomial expansion is valid in the square-free boundary algebra because
\(x\) and \(C_2\) have even degree and commute. On \(s\ne0\), \(D=0\) is
equivalent to

\[
\frac1{3!}\left(x+\frac{C_2}{s}\right)^3
 =\sum_i\frac{\kappa_i}{s}X_i.
\]

Thus nonzero \(s,\kappa_0,\kappa_1,\kappa_2\) would indeed give an active
ternary six-site target after a one-site diagonal normalization.

The independent checker verifies these identities twice: symbolically in a
commutative polynomial ring and in a custom six-site square-free tensor
algebra.

## 2. Universal forbidden linear locus and dimension bounds

For

\[
{\cal Z}_0=\ker(s,C_2),
\]

substitution \(s=C_2=0\) kills every displayed monomial of \(D\), independently
of \(C_4,C_6,x\). Hence

\[
{\cal Z}_0\subseteq V(D)\cap V(s).
\]

The degree-two boundary space has

\[
\binom62\cdot3^2=15\cdot9=135
\]

coordinates. The linear map \((s,C_2)\) therefore has rank at most 136. In
an \(N\)-dimensional cap space,

\[
\dim{\cal Z}_0\ge N-136,\qquad
\dim\mathbb P({\cal Z}_0)\ge N-137
\]

whenever the kernel is nonzero.

By the height theorem, 729 homogeneous generators in the \(N\)-variable
affine coordinate ring have height at most 729. Their affine cone has
dimension at least \(N-729\), so its projectivization has the crude lower
bound

\[
\dim V(D)\ge N-730.
\]

For \(N>729\), that affine lower bound is positive and the homogeneous cone
has a nonzero point. At \(|W|=8\), \(N=3^8=6561\), and the two projective
bounds are respectively

\[
6424\qquad\text{and}\qquad5831.
\]

The universal bad linear space therefore has a lower-bound dimension 593
larger than the entire existence guarantee supplied by the generator count.
Height says nothing about whether an irreducible component survives outside
the four forbidden hyperplanes; that is precisely a saturation question.

## 3. Exact abstract GHZ-compatible signature

Choose independent linear forms \(s,\kappa_0,\kappa_1,\kappa_2\), fix any
degree-two boundary element \(x\), and set

\[
C_0=s,\qquad C_2=-sx,\qquad C_4=0,\qquad
C_6=\sum_i\kappa_iX_i+\frac13sx^3.
\]

These are linear maps of the cap covector. Their GHZ residual is

\[
\left(\frac13-\frac12+\frac16\right)sx^3=0.
\]

Moreover \(sx+C_2=0\), so the cube form reduces coefficientwise to

\[
D=6s^2\sum_i\kappa_iX_i.
\]

There is no hidden requirement that \(x^3\) be independent of the three
target directions. The custom square-free audit chooses an \(x\) for which
\(x^3\) has a nonzero component in every \(X_i\) direction, as well as mixed
components. Both the GHZ and \(D\) residuals still vanish identically.

The four cap forms can be instantiated exactly with \(|W|=2\). Take

\[
g_i=e_i\otimes e_i,\qquad h_W=e_0\otimes e_1.
\]

These are four distinct tensor-basis vectors, so
\(\kappa_i(K)=K(g_i)\) and \(s(K)=K(h_W)\) are independent. The independent
checker constructs their \(4\times9\) evaluation matrix, verifies rank four,
and exhibits a covector on which all four values equal one. Extra cap
coordinates are unconstrained dummies.

Since \(X_0,X_1,X_2\) are independent,

\[
D(K)=0\iff s(K)=0
\quad\text{or}\quad
\kappa_0(K)=\kappa_1(K)=\kappa_2(K)=0.
\]

Thus every zero lies in the forbidden union despite the existence of points
outside all four individual hyperplanes.

## 4. Ideal, radical, and saturation certificate

Over characteristic zero the factor 6 is a unit, so the nonzero coordinate
ideal is

\[
I_D=(s^2\kappa_0,s^2\kappa_1,s^2\kappa_2)
    =(s^2)\cap(\kappa_0,\kappa_1,\kappa_2).
\]

Its radical and minimal primes are

\[
\sqrt{I_D}
 =(s)\cap(\kappa_0,\kappa_1,\kappa_2)
 =(s\kappa_0,s\kappa_1,s\kappa_2),
\]

which gives the asserted set-theoretic union. The independent checker derives
the two minimal primes by enumerating the minimal hitting sets of the monomial
supports, and reconstructs both displayed intersections by pairwise least
common multiples.

Let \(h=s\kappa_0\kappa_1\kappa_2\). Then \(h\notin I_D\), but

\[
h^2=(s^2\kappa_0)(\kappa_0\kappa_1^2\kappa_2^2)\in I_D.
\]

Therefore \(h\in\sqrt{I_D}\), \(1\in I_D:h^2\), and

\[
I_D:h^\infty=(1).
\]

There is also an explicit Rabinowitsch unit certificate. With
\(g=s^2\kappa_0\), \(m=\kappa_0\kappa_1^2\kappa_2^2\), and a localization
variable \(t\),

\[
1=(1-th)(1+th)+t^2mg.
\]

Hence \(I_D+(1-th)=(1)\). A separate exact Singular computation returned
\[
\sqrt{I_D}=(s\kappa_0,s\kappa_1,s\kappa_2),
\]
minimal primes \((s)\) and \((\kappa_0,\kappa_1,\kappa_2)\), and localized
standard basis \((1)\). The Python checker independently obtains a Gröbner
basis containing one in a different variable order and with a dummy cap
coordinate present.

On the affine normalization \(s=\kappa_0=\kappa_1=\kappa_2=1\), the three
nonzero coordinates of \(D\) are \((6,6,6)\). The restricted ideal is
therefore the unit ideal, regardless of how many dummy variables are added.

## 5. Exact scope boundary

The countermodel supplies all of the following:

* linear dependence of every \(C_j\) on the cap covector;
* independent \(s,\kappa_0,\kappa_1,\kappa_2\);
* the full top GHZ contraction identity for every cap; and
* the exact denominator-cleared cubic and its unit saturation.

It deliberately does **not** supply:

* one aggregate edge family whose common matching cofactors are all the
  displayed \(C_j\);
* the shared-star product relations among those cofactors; or
* the pair-adjugate identity and related alternating-cycle constraints.

Consequently the construction disproves the inference

> large cap dimension + linear GHZ identity \(\Longrightarrow\) active clean
> cap,

but it neither constructs a realizable counterexample nor proves that an
actual common-edge signature has unit saturation. The remaining positive gate
is exactly to prove

\[
I_D:(s\kappa_0\kappa_1\kappa_2)^\infty\ne(1)
\]

for signatures arising from a common aggregate edge family, using genuinely
nonlinear common-edge identities. This scope distinction is stated correctly
and consistently in the primary note.

## 6. Reproduction

From the repository root:

```bash
.venv/bin/python computations/verify_cap_condition_projective_height_obstruction.py
.venv/bin/python computations/audit_cap_condition_projective_height_obstruction_independent.py
.venv/bin/python -m py_compile \
  computations/verify_cap_condition_projective_height_obstruction.py \
  computations/audit_cap_condition_projective_height_obstruction_independent.py
```

The independent run reports cubic cap degree, zero square-free GHZ and \(D\)
residuals, the \(135/729\) coordinate counts, the \(6424/5831\) projective
bounds, minimal saturation power two, a localized basis containing one, rank
four for the concrete cap forms, the abstract-only scope marker, and `PASS`.

## Promotion recommendation

Safe to promote as a rigorous obstruction to projective-height cap selection.
The conclusion must retain the explicit qualifier “abstract GHZ-compatible
signature, not a realizable common-edge source.” The primary note and checker
were not edited during this audit.
