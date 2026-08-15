# The scalar-zero packet is a hafnian tangent, not an ordinary six-site source

## Result

The rootless scalar-zero packet

\[
 r_*q^{[2]}=-\alpha\Delta_{6,3},\qquad r_*^{[3]}\ne0       \tag{1}
\]

does not reduce to the proved unrestricted six-site obstruction by literal
polarization, degeneration, finite coefficient extraction, forgetting a
colour marker, or the natural two-vertex pair gadget.

The sharp counterguard already retains the extra hypotheses named in (1):
`r_*` is an invertible pairing of two injective three-dimensional endpoint
stars.  With `alpha=-1`, it satisfies

\[
 r_*q^{[2]}=\Delta_{6,3},\qquad r_*^{[3]}=-X_0\ne0.       \tag{2}

Nevertheless neither `q`, `r_*`, nor any nonzero member of their pencil has
six-site hafnian equal to a nonzero ternary diagonal tensor.  The obstruction
is not merely that a known construction was tried in the wrong chart: (2) is
the first polarization of the cubic hafnian map, while the six-site theorem
concerns a value of that cubic map.

The exact checker is
`computations/verify_h3_scalar_zero_packet_six_site_nonreduction.py`.

## 1. Exact simultaneous counterguard

On sites `0,...,5`, let the response be

\[
\begin{aligned}
r={}&x_{0,0}x_{4,0}+x_{1,0}x_{3,0}-x_{2,0}x_{5,0}\\
   &+x_{0,1}x_{1,1}+x_{0,2}x_{2,2},
\end{aligned}                                               \tag{3}
\]

and let

\[
\begin{aligned}
q={}&x_{0,0}x_{4,0}+x_{2,0}x_{5,0}\\
   &+x_{2,1}x_{4,1}+x_{3,1}x_{5,1}\\
   &+x_{1,2}x_{3,2}+x_{4,2}x_{5,2}.
\end{aligned}                                               \tag{4}
\]

All omitted decorated cells are zero.  Complete replay of all 729 words
gives

\[
 r q^{[2]}=X_0+X_1+X_2,\qquad r^{[3]}=-X_0.             \tag{5}
\]

Thus (2) holds exactly.

The response is not an arbitrary quadratic.  Put

```text
u0=x00+x40,       v0=x01+x11,
u1=x10+x30,       v1=x02+x22,

p0=u0+i v0,       t0=(u0-i v0)/2,
p1=u1+i v1,       t1=(u1-i v1)/2,
p2=x20,            t2=-x50.
```

Then

\[
                         r=p_0t_0+p_1t_1+p_2t_2.        \tag{6}
\]

The port supports of the three `p_i` are pairwise disjoint and nonempty;
the same is true of the `t_i`.  Both endpoint triples are injective.  The
channel matrix in (6) is `I_3`, hence invertible.  The checker reconstructs
(3) from (6) over the exact Gaussian rationals.

This is precisely the contracted scalar-zero hypothesis, including its
physical three-channel provenance.  It is deliberately not asserted to
satisfy the other eight uncontracted physical pair rows.

## 2. The adjacent polarizations are nonzero

The four coefficients of the cubic pencil are

\[
(uq+vr)^{[3]}
 =u^3q^{[3]}+u^2v\,rq^{[2]}+uv^2\,qr^{[2]}+v^3r^{[3]}. \tag{7}
\]

Exact replay gives

```text
q^[3]       = +e_020200,
r q^[2]     = X0+X1+X2,
q r^[2]     = -e_020200+e_202022,
r^[3]       = -X0.                                      (8)
```

In particular, the `202022` coefficient of (7) is `u v^2`.  If a pencil
member has no mixed coefficients, then `u v^2=0`.

* If `u=0`, its cube is `-v^3 X0`, unary rather than ternary.
* If `v=0`, its `020200` coefficient is `u^3`, so `u=0` as well.

Therefore no nonzero pencil member has a pure ternary cube.  This is a
two-coordinate exact counterguard to identifying the tangent in (5) with
an ordinary hafnian value.

## 3. Polarization and finite extraction

Let

\[
                         F(t)=(q+tr)^{[3]}.             \tag{9}
\]

Then `[t]F=rq^[2]=Delta`.  Coefficient extraction is possible as a vector
space operation.  For example the checker verifies, coefficientwise in all
729 words,

\[
 -\frac13F(-1)-\frac12F(0)+F(1)-\frac16F(2)
      =rq^{[2]}=\Delta_{6,3}.                          \tag{10}
\]

Equation (10) is a linear combination of four ordinary hafnian tensors.  It
is not one hafnian tensor.  Aggregating the four edge collections before
taking the hafnian creates the mixed terms in (7), so (10) cannot be
reinterpreted as one decorated six-site source.

This is the categorical failure: `[t]` is linear but not multiplicative.
Its product rule is exactly what selects one distinguished `r` edge among
the three matching edges.  The unrestricted six-site theorem is a statement
about the nonlinear Veronese/hafnian image, not its tangent span.

## 4. Degeneration does not isolate the tangent

At `t=0`, the leading term of (9) is the nonzero mixed tensor
`q^[3]=e_020200`.  Obtaining the tangent requires subtracting that term.
At the other projective end, the leading tensor is
`r^[3]=-X0`.  Hence a rescaled projective limit of individual pencil
members retains one of these two cubes; it does not produce the middle
coefficient `Delta`.

The Veronese image of the finite-dimensional space of quadratics is
projectively closed.  Difference quotients can land in its tangent variety,
but subtraction of two source tensors is not a degeneration of one source.
The explicit nonzero end terms in (8) prevent the only naive loopholes.

## 5. Colour markers only repackage coefficient extraction

Marking an edge as type `q` or type `r` records the four possible numbers
of response edges in a three-edge perfect matching.  Forgetting that marker
evaluates

\[
 (a q+b r)^{[3]}
 =a^3q^{[3]}+a^2b,rq^{[2]}+ab^2,qr^{[2]}+b^3r^{[3]}. \tag{11}

The counterguard makes all four type sectors nonzero.  No scalar evaluation
can kill sectors zero, two, and three while retaining sector one: `a^3=0`
and `b^3=0` already force `a=b=0` over `C`.

One may formally use a dual-number marker `epsilon` with `epsilon^2=0` and
read its `epsilon` coefficient.  But the readout
`epsilon -> 1` is not an algebra homomorphism to `C`; it is again (10).
Keeping the marker instead enlarges the local colour/output space and does
not produce the ordinary ternary six-site target required by the theorem.

## 6. A vertex gadget moves the problem to the full pair rows

Two extra selector vertices can generate a response of the form
`sum K_ij p_i s_j` after contraction.  They do not turn that response into
one six-site edge block.  They create an eight-site physical pair packet,
whose nine colour-pair rows must share the same `q`, endpoint stars, and
direct block.

The guard locates the first missing row exactly.  For the natural `K=I`
factorization, the first channel obeys

```text
q^[3]            = e_020200,
p0*t0*q^[2]      = e_020200 + X1.                       (12)
```

The uncontracted row would require

\[
             a_{00}q^{[3]}+p_0t_0q^{[2]}=X_0.          \tag{13}
\]

Its `X1` coefficient is one for every scalar `a_00`, so (13) is impossible.
Thus the counterguard is not an eight-site source.  More importantly, this
shows why a vertex gadget is not a reduction to the six-site theorem: its
first new obligation is an uncontracted pair equation absent from (1).

## Consequence and scope

The ordinary six-site obstruction cannot be applied directly to (1).  The
packet lies in the tangent space to the hafnian image and the explicit guard
shows that its nonnilpotence and invertible three-channel response do not
move it back into that image.

The smallest remaining positive theorem must use information not present in
the contracted packet—most naturally the other eight physical pair rows,
or an equivalent cross-word cohafnian compatibility.  Such a theorem is not
refuted here.  What is refuted is any reduction using only:

* the scalar-zero common-power equation and `r^[3]!=0`;
* polarization or finite evaluation/extraction on the pencil;
* a colour marker which is later forgotten;
* a projective pencil degeneration; or
* the natural pair/vertex gadget without its full nine shared rows.

## Reproduction

```text
python3 computations/verify_h3_scalar_zero_packet_six_site_nonreduction.py --mode structural
python3 -O computations/verify_h3_scalar_zero_packet_six_site_nonreduction.py --mode full
python3 -I -S computations/verify_h3_scalar_zero_packet_six_site_nonreduction.py --mode exhaustive
```

All modes return the same frozen ledger digest.
