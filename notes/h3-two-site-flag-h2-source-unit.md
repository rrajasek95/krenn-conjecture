# A two-site triangular flag gives a parametric Hamming-two source unit

## Outcome

The three-row unit in
[`h3-h1-nonclean-packet-h2-three-row-unit.md`](h3-h1-nonclean-packet-h2-three-row-unit.md)
is not an isolated numerical cancellation.  It is the specialization of an
ordinary four-row polynomial identity with arbitrary cross-colour internal
cells and arbitrary flag coefficients.

On six residual sites normalize the colour-0 and colour-1 diagonal shadow of
the internal quadratic to the same perfect matching

\[
                         01\mid23\mid45.                 \tag{1}
\]

All other same-colour 0/1 cells vanish; every ordered cross-colour cell is
arbitrary.  For one first endpoint row and two second endpoint rows assume
the two-site triangular flag

\[
\begin{aligned}
 p_0|_{\{0,1\}}&=A z_0^0+B z_1^0+C z_1^1,\\
 s_0|_{\{0,1\}}&=D z_0^1,\\
 s_1|_{\{0,1\}}&=E z_0^0+F z_0^1+G z_1^1,
\end{aligned}                                           \tag{2}
\]

with no other colour-0/1 components.  The coefficients
`A,B,C,D,E,F,G` are arbitrary.  Let `d00,d01` be the two direct entries and
write `Fij(w)` for the literal full-nine source row at the residual word
`w`.  Put

\[
\begin{aligned}
 K_B&=\operatorname {Haf}_{2345}(0011),\\
 K_C&=\operatorname {Haf}_{2345}(1100).
\end{aligned}                                           \tag{3}
\]

Then the following identity holds over the universal integral coefficient
ring:

\[
\boxed{
\begin{aligned}
 &d_{01}F_{00}(001111)
 -d_{00}F_{01}(000011)
 -d_{00}F_{01}(001100)\\
 &\hspace{30mm}
 +d_{00}(K_B+K_C)F_{01}(000000)
 =d_{00}d_{01}.
\end{aligned}}                                          \tag{4}
\]

Thus any physical packet satisfying (1)--(2) is empty on the chart
`d00*d01 != 0`.  This is a literal ordinary source certificate.  It uses no
Hasse, Ward, covariance, cap-codomain, tangent, Gröbner, or finite-field
generator.

## Matching identity behind the certificate

Let

\[
 A=001111,\qquad B=000011,\qquad C=001100.
\]

Direct perfect-matching expansion gives

\[
 H(A)-H(B)-H(C)+K_B+K_C=1.                              \tag{5}
\]

This is valid with every ordered cross-colour cell free.  The diagonal
normalization (1) is the only internal-cell input.  Matchings containing
`01` cancel against the two four-site cofactors except for the normalized
pure matching; the remaining matchings cancel between the three binary
words.

Under the flag (2), the four response rows simplify to

\[
\begin{aligned}
 F_{00}(A)&=d_{00}H(A),\\
 F_{01}(B)&=d_{01}H(B)+BEK_B,\\
 F_{01}(C)&=d_{01}H(C)+BEK_C,\\
 F_{01}(0^6)&=d_{01}+BE.
\end{aligned}                                           \tag{6}
\]

Substituting (6) into the left side of (4) and using (5) proves the
identity.  Notice that the crossed pure row is not assumed in the algebra:
it is included as the fourth physical generator.  On a source it vanishes,
so it also gives `BE=-d01` coefficientwise.

## Relation to the known nonclean packet

The committed `chi=-12` packet has

\[
 d_{00}=d_{01}=1,\qquad B=1,\qquad E=-1.
\]

Hence `F01(000000)=0`, and (4) reduces exactly to

\[
 F_{00}(001111)-F_{01}(000011)-F_{01}(001100)=1,        \tag{7}
\]

recovering the earlier three-row certificate while allowing all thirty
binary ordered cross cells to vary.

## Proof impact and exact remaining gate

Equation (4) supplies a packet-conditioned ordinary source unit of the type
required by the monic-anchor equivalence theorem.  It therefore closes the
rootless attaching problem on every chart admitting the common-matching and
two-site-flag normalization (1)--(2).

It does **not** prove that an arbitrary rootless full-nine packet admits that
normalization.  Both hypotheses are load-bearing: the checker shows that one
additional diagonal cell `24:11`, or one outside flag component
`s1(2,0)`, destroys (4).  The theorem-level next step is consequently a
source-faithful flag extraction dichotomy:

> either the two labelled endpoint rows admit (after physical relabelling
> and allowed coefficient normalization) the common matching and triangular
> two-site flag above, or the extra diagonal/star component itself produces
> an active clean cap or a separately localized ordinary source unit.

This is narrower than constructing a universal attaching nullhomotopy and
has a concrete literal landing certificate.

## Verification

Run

```text
.venv/bin/python computations/verify_h3_two_site_flag_h2_source_unit.py
.venv/bin/python -O computations/verify_h3_two_site_flag_h2_source_unit.py
```

The checker reconstructs the four physical rows from the endpoint-coloured
matching formula, treats all thirty ordered binary cross cells as independent
variables, verifies (5) and (4) in the universal integer polynomial ring,
checks the numerical three-row specialization, and mutation-tests both
load-bearing hypotheses.
