# Independent audit of the three-double sole-plane frontier

## Verdict

The claims in
[live-three-zero-sole-plane-fourth-high-three-double-frontier.md](live-three-zero-sole-plane-fourth-high-three-double-frontier.md)
pass an independent audit, with exactly the scope stated there.  The note
produces six necessary parameter equations for the profile
\(2^3 1^7\) and reduces their common projective boundary to two directions.
It does **not** close the affine fibres, either boundary direction, or the
profile itself.

## Row, scale, and exchange checks

Put \(d=x^2-a^2\).  Starting with the earlier order-three row, its cleared
first logarithmic numerator is

\[
                         Pd-x-3a.
\]

If \(R=P^2+W\), adding its square to the cleared second logarithmic
derivative gives

\[
 Rd^2-2Pd(x+3a)
 +(x+3a)^2+(x-a)^2+2(x+a)^2.
\]

The last three terms are exactly
\(4(x^2+2ax+3a^2)\), so this is the displayed \(M_a\).  The second entry is
\(2(Pd-x-3a)d-aM_a\), which is the displayed \(N_a\).  Thus the affine row
agrees term by term with `triple_quadratic_row`, rather than only after a
generic specialization.

Under \(x=cX\), \(a=cA\), \(P=c^{-1}\widehat P\), and
\(R=c^{-2}\widehat R\), one has \(d=c^2(X^2-A^2)\).  Every term of \(M\)
has weight two and every term of \(N\) has weight three.  Hence the pair
determinant has weight five, as claimed.

Changing a selected partner changes the effective logarithmic data by
\(P\mapsto P+\delta\) and \(W\mapsto W+\epsilon\).  Therefore

\[
 (P+\delta)^2+(W+\epsilon)
 =R+2P\delta+\delta^2+\epsilon,
\]

which verifies all four exchange equations in the full system.  The
formulas for \(\delta\) and \(\epsilon\) are exactly the differences of the
two displayed `chi` and `eta` increments.

## Pair identities and equation systems

Each \(F_{ab}=M_aN_b-N_aM_b\) has degree at most eight.  On the putative
counterexample it has the seven singleton roots and the remaining double
value as an eighth distinct root.  If its degree dropped, these eight roots
would make it identically zero.  I also checked the required nonidentity
directly, independently of the earlier localized coefficient-ideal
computation.  If the determinant for anchors \(a,b\) were identically zero,
evaluating at \(x=\pm b\), where the \(b\)-row is a nonzero multiple of
\((1,-b)\), would give \(N_a(\pm b)+bM_a(\pm b)=0\).  Adding and subtracting
these equations gives

\[
 P_a={3a-b\over b^2-a^2},\qquad
 R_a={-2(b-a)(b+3a)\over(b^2-a^2)^2}.
\]

The two evaluations at \(x=\pm a\) give the swapped formulas for
\(P_b,R_b\).  Substitution into the coefficients of \(x^8\) and \(x^7\)
then forces, respectively,

\[
 9a^2+22ab+9b^2=0,qquad a^2+6ab+b^2=0.
\]

Here the omitted common factors are nonzero products of
\(a,b,a-b,a+b\).  Subtracting nine times the second equation from the first
gives \(-32ab=0\), contrary to the structural nonvanishing of the repeated
values.  Thus the determinant cannot be an identity anywhere on the
structural locus.  Consequently its degree is exactly eight and the three
factorizations by the common singleton polynomial follow.  Taking the
ratios of their nonzero leading constants gives the two multiplier
identities \(C_1=C_2=0\).
Allowing \(\lambda\) or \(\mu\) to be zero in the algebraic system only
enlarges that necessary system and therefore cannot create a false
exclusion.

Both cross identities have degree at most nine.  The seven evaluation
nodes

\[
                    v,w,1,-1,-v,-w,0
\]

are distinct under the eight structural factors.  Giving multiplicity two
to \(-v,-w,0\) produces ten confluent evaluation conditions, so the chosen
ten rows are in fact unisolvent for degree-nine polynomials.  In
particular, they are valid necessary rows even without using coefficient
extraction.  The first system has ten rows; adjoining the ten rows for the
second identity and the four exact exchange rows gives twenty-four.

## Lift and specialization audit

The exact checker was rerun from a fresh process:

```text
.venv/bin/python computations/verify_live_three_zero_sole_plane_fourth_high_three_double_frontier.py
```

It returned

```text
EXACT THREE-DOUBLE FRONTIER AUDIT PASS
first lift shape 10 1 34
full lift shape 24 1 48
stripped degrees 30 30 30 48 48 48
infinity gcd v^6 w^6
```

The interpretation of `liftstd` was checked against Singular's defining
matrix identity.  If \(I\) is the input ideal, \(G\) the returned standard
basis, and \(T\) the lift matrix, then

\[
                         \operatorname{matrix}(G)
                 =\operatorname{matrix}(I)T.
\]

Thus the \(10\times1\) and \(24\times1\) matrices really express the one
constant standard-basis element in the original rows.  Auditing every
coefficient of these two columns found 34 and 48 coefficient terms and
denominator lcm one.  Independently factoring every denominator already in
the input rows gives only

\[
             v,\ w,\ v\pm1,\ w\pm1,\ v\pm w.
\]

It follows that clearing the lifted identities loses only structural
divisors.  Removing those divisors is valid because all three double values
are repeated and hence nonzero, distinct, and nonopposite.

For completeness, the two cyclic normalization formulas used by the
checker have the expected homogeneous meaning.  If \(H(t,v,w)\) is the
homogenization of \(h(v,w)\) of degree \(d\), then

\[
 H(v,1,w)=v^d h(1/v,w/v),\qquad
 H(w,1,v)=w^d h(1/w,v/w).
\]

These are precisely the normalizations with the old \(v\)- and old
\(w\)-double values chosen in turn as the unit anchor.  Repeating this for
both lift outputs gives all six necessary polynomials.  After structural
factor removal their exact total degrees are
\(30,30,30,48,48,48\).

## Infinity and modular scope

Homogenizing the six stripped polynomials and taking their binary leading
forms gives gcd \(v^6w^6\) over \(\mathbb Q\).  On the projective parameter
line its zero set is exactly \([1:0]\) and \([0:1]\).  This proves only the
stated boundary reduction; it says nothing about the affine common zero
set and does not exclude either direction.

The finite-field paragraph is also correctly fenced off.  A UNIT after
reduction modulo \(32003\) is explicitly labelled discovery evidence, and
the example \(\langle32003z-1\rangle\) correctly demonstrates why it cannot
be promoted to a characteristic-zero certificate.  No closure credit is
justified by the modular computation.

The audited status of \(2^3 1^7\) therefore remains **open**.
