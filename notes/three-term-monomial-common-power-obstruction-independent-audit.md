# Independent audit of the pure \((3,1,1)\) common-power obstruction

## 1. Verdict

The theorem in
[the primary note](three-term-monomial-common-power-obstruction.md) is sound
over \(\mathbb C\).  Let \(U\) be a six-set, let every local space \(V_u\)
contain independent displayed vectors
\(e_0^{(u)},e_1^{(u)},e_2^{(u)}\), and write

\[
 E_i(P)=\bigotimes_{u\notin P}e_i^{(u)},
 \qquad X_i=\bigotimes_{u\in U}e_i^{(u)}.
\]

For three distinct pairs \(A_1,A_2,A_3\), two initially arbitrary pairs
\(C,D\), and five nonzero complex coefficients, put

\[
 F=\lambda_1E_0(A_1)+\lambda_2E_0(A_2)+\lambda_3E_0(A_3)
   +\gamma E_1(C)+\delta E_2(D).                             \tag{A1}
\]

Allow six completely arbitrary multi-site star rows and impose all nine
exact products

\[
 p_i s_jF=\delta_{ij}X_i.                                    \tag{A2}
\]

Then no quadratic \(q\) satisfies

\[
 q^{[2]}=F,\qquad q^{[3]}=0.                                \tag{A3}
\]

The independent audit confirms every load-bearing step:

1. the literal products force all five missing pairs to be distinct;
2. projection to the three displayed local coordinates is lossless;
3. the three colour-zero weights normalize by a rank-three complement
   character map, with an essential but valid square root in the \(3K_2\)
   case;
4. the full weighted kernel of \(qF=0\) is exactly a scalar equation plus
   two copies of the incidence kernel at every used vertex;
5. the \(60{,}060\) labelled supports form \(70\) exact symmetry orbits;
6. all \(70\) independently ordered, unsaturated affine ideals over
   \(\mathbb Q\) have reduced basis \([1]\).

The standalone
[independent checker](../computations/audit_three_one_one_common_power_obstruction_independent.py)
does not import the primary verifier.  It chooses lexicographically maximal
representatives rather than minimal ones, reverses the orbit order, uses a
different weighted incidence parametrization, changes edge, variable,
colour, matching, and generator orders, and reverses the final ring-variable
order.

## 2. Literal product audit

Work in the site-square-zero algebra

\[
 \mathcal R_U=\bigotimes_{u\in U}(\mathbb C\oplus V_u),
 \qquad V_uV_u=0.                                           \tag{A4}
\]

For a missing pair \(P=\{a,b\}\), multiplication by \(E_k(P)\) leaves the
complete two-order response

\[
 B_{ij}(P)=p_{i,a}\otimes s_{j,b}
              +s_{j,a}\otimes p_{i,b}.                     \tag{A5}
\]

After extending the three displayed axes to local bases, the response space
of \(E_k(P)\) is the coordinate subspace whose words are fixed to \(e_k\)
outside \(P\) and arbitrary at the two endpoints.  Response spaces of
different lift colours have disjoint coordinate-word supports: two pairs
occupy at most four sites, leaving at least one site fixed to two different
coordinate axes.

Apply (A2) to row \((1,1)\).  Its colour-one and colour-two components give

\[
 B_{11}(C)=\gamma^{-1}e_1^{\otimes C},
 \qquad B_{11}(D)=0.                                       \tag{A6}
\]

Thus \(C=D\) is impossible because the left sides are then the same literal
tensor.  If \(C=A_r\), the colour-zero response contains the coordinate word
which is \(e_1\) on the two endpoints of \(A_r\) and \(e_0\) elsewhere.
For a different pair \(A_s\), at least one of those two endpoints is outside
\(A_s\), where its response is fixed to \(e_0\).  Therefore no other
colour-zero term can contain that word, so it cannot cancel.  Hence \(C\)
differs from all three \(A_r\)'s.  Row \((2,2)\) gives the same argument for
\(D\) with \(e_2\), proving that all five pairs are distinct.

The checker enumerates the complete initial support set

\[
 \binom{15}{3}15^2=102{,}375
\]

and obtains the following disjoint decision census:

| decision | count |
|---|---:|
| \(C=D\) | 6,825 |
| \(C\in\{A_1,A_2,A_3\}\), after excluding \(C=D\) | 19,110 |
| \(D\in\{A_1,A_2,A_3\}\), after the preceding cases | 16,380 |
| five distinct pairs | 60,060 |

The coordinate-word argument, rather than this finite census, proves the
claim for arbitrary local spaces and arbitrary star rows.  The census audits
that the case split is exhaustive.

## 3. Projection and exact weight normalization

Choose at every site a projection

\[
 V_u\longrightarrow
 \langle e_0^{(u)},e_1^{(u)},e_2^{(u)}\rangle
\]

which fixes the displayed axes.  Extending it by the identity on scalars
gives an algebra homomorphism in (A4).  It preserves (A1)--(A3), so a
solution in larger local spaces would project to a solution with local
dimension three.  No outside-coordinate branch is lost.

For colour zero, scale \(e_0^{(u)}\mapsto t_u e_0^{(u)}\), with
\(t_u\in\mathbb C^*\).  The coefficient of \(E_0(P)\) is multiplied by

\[
 \chi_P(t)=\prod_{u\notin P}t_u.                             \tag{A7}
\]

For a three-edge set \(H=\{A_1,A_2,A_3\}\), let \(M_H\) be the
\(3\times6\) exponent matrix of these complement characters.  There are
five possible graph shapes.  The independent checker evaluates every one
of the \(\binom{15}{3}=455\) labelled three-edge sets and finds:

| shape of \(H\) | labelled sets | rank of \(M_H\) | Smith lattice index |
|---|---:|---:|---:|
| \(K_{1,3}\) | 60 | 3 | 1 |
| \(K_3\) | 20 | 3 | 1 |
| \(P_4\) | 180 | 3 | 1 |
| \(P_3+K_2\) | 180 | 3 | 1 |
| \(3K_2\) | 15 | 3 | 2 |

The index is the greatest common divisor of the nonzero \(3\times3\)
minors.  Smith normal form now makes the normalization precise.  In the
first four rows the character lattice is saturated.  In the last row the
map on character lattices has index two, but the induced map on complex
points is still onto because every nonzero complex number has a square
root.

The root issue is visible directly.  For the matching
\(A_1=01,A_2=23,A_3=45\), put

\[
 x=t_0t_1,\qquad y=t_2t_3,qquad z=t_4t_5,
 \qquad b_r=\lambda_r^{-1}.
\]

The normalization equations are

\[
 yz=b_1,\qquad xz=b_2,qquad xy=b_3.                         \tag{A8}
\]

Choose a square root \(x^2=b_2b_3/b_1\), and then take
\(y=b_3/x\), \(z=b_2/x\).  This is why the field \(\mathbb C\), rather
than merely an arbitrary field, matters in this case.  The checker audits
the same calculation by the half-integral exponent vectors

\[
 \tfrac12(1,-1,-1),\quad
 \tfrac12(-1,1,-1),\quad
 \tfrac12(-1,-1,1).                                       \tag{A9}
\]

The colour-one and colour-two axes scale independently, and each of their
single coefficients is normalized by one factor in the corresponding
four-site complement.  Consequently all five coefficients in (A1) may be
taken to be one.

These local automorphisms need not fix \(X_i\), and they do not need to.
The product table has already served only to force the five supports to be
distinct.  From that point the contradiction concerns (A3) alone, and an
algebra automorphism carries (A3) to the normalized common-power equations.
Thus there is no hidden claim that this torus action fixes the response
normalization.

## 4. The complete weighted incidence kernel

Before normalization, the matching identity

\[
 q q^{[2]}=3q^{[3]}                                       \tag{A10}
\]

shows that (A3) implies \(qF=0\).  Only the edge block \(q_P\) can fill the
two holes of \(E_i(P)\).  Separation by lift colour therefore gives

\[
 q_C=q_D=0.                                                \tag{A11}
\]

Write

\[
 V_u=\mathbb C e_0^{(u)}\oplus W_u
\]

and decompose, for \(e=\{u,v\}\in H\),

\[
 q_e=c_e e_0^{(u)}e_0^{(v)}
       +a_{e,u}e_0^{(v)}+e_0^{(u)}a_{e,v}+Z_e,             \tag{A12}
\]

where \(a_{e,u}\in W_u\) and \(Z_e\in W_u\otimes W_v\).  Coordinate
words with two transverse sites isolate one edge; words with one transverse
site collect exactly the edges incident to that vertex; and the all-
\(e_0\) word collects the scalar parts.  Hence the complete weighted system
is

\[
 Z_e=0,qquad
 \sum_{e\ni u}\lambda_e a_{e,u}=0\quad(u\in U),
 \qquad
 \sum_{e\in H}\lambda_e c_e=0.                            \tag{A13}
\]

There are no other equations on the three colour-zero blocks.  Since every
\(\lambda_e\ne0\), the scalar kernel has dimension two.  At a used vertex
of degree \(d_u\), each of the two transverse coordinates has a
\((d_u-1)\)-dimensional weighted incidence kernel.  As the sum of degrees is
six, if \(v(H)\) vertices are used, the special-block dimension is

\[
 2+2\sum_{u:\,d_u>0}(d_u-1)=2+2(6-v(H)).                  \tag{A14}
\]

The ten physical pairs outside the five target supports contribute
\(90\) unrestricted coordinates.  Thus:

| shape | \(v(H)\) | special-block kernel | full rank in 135 cells | full kernel |
|---|---:|---:|---:|---:|
| \(K_{1,3}\) | 4 | 6 | 39 | 96 |
| \(K_3\) | 3 | 8 | 37 | 98 |
| \(P_4\) | 4 | 6 | 39 | 96 |
| \(P_3+K_2\) | 5 | 4 | 41 | 94 |
| \(3K_2\) | 6 | 2 | 43 | 92 |

The independent checker uses the nonuniform rational weights
\((2,-3,5,7,-11)\), solves every scalar and incidence equation with explicit
weight ratios, constructs the full \(135\)-column matrix of \(qF\), and
checks spanning, independence, and the displayed rank for every orbit.
This is a direct audit of the general weighted formula, not only of its
all-one specialization.

## 5. Support orbits and corrected coefficient stream

After the collision proof, the labelled support count is

\[
 \binom{15}{3}\,12\,11=60{,}060.                           \tag{A15}
\]

The independent program constructs this universe directly.  It treats the
three colour-zero pairs as an unordered set and quotients by site
permutations and by the simultaneous interchange of \(C,D\) and colours
\(1,2\).  Its lexicographically maximal representatives give the following
independent order:

| shape | independent orbit numbers | orbits | labelled supports | variables | equation range |
|---|---|---:|---:|---:|---:|
| \(K_3\) | 1--6 | 6 | 2,640 | 98 | 1,059--1,145 |
| \(K_{1,3}\) | 7--19 | 13 | 7,920 | 96 | 813--1,192 |
| \(P_4\) | 20--41 | 22 | 23,760 | 96 | 987--1,215 |
| \(P_3+K_2\) | 42--66 | 25 | 23,760 | 94 | 915--1,215 |
| \(3K_2\) | 67--70 | 4 | 1,980 | 92 | 991--1,215 |

The \(70\) orbits are disjoint and exhaustive.  The ordered independent
support ledger has SHA-256

```text
3b06effdd4e66804a11c4b66d536cf0a207db5f998ee50fb3d0627e72823470a
```

For every four-set \(S=\{u_0,u_1,u_2,u_3\}\) and every local colour word,
the checker emits the coefficient

\[
\begin{aligned}
 &(q_{u_0u_1})_{c_0c_1}(q_{u_2u_3})_{c_2c_3}
 +(q_{u_0u_2})_{c_0c_2}(q_{u_1u_3})_{c_1c_3}\\
 &\qquad +(q_{u_0u_3})_{c_0c_3}(q_{u_1u_2})_{c_1c_2}
 -[F]_{S,c}.                                               \tag{A16}
\end{aligned}
\]

Endpoint order is retained by transposing the two local indices whenever an
edge is traversed backwards.  The code now contains a structural assertion
that its three four-site matchings are exactly

\[
 \{01,23\},\qquad\{02,13\},\qquad\{03,12\}.                \tag{A17}
\]

This assertion was added after an audit-stage failure caught before the
theorem was accepted.  The first development stream accidentally listed
\(\{02,13\}\) twice and omitted \(\{01,23\}\).  Its anomalous minimum of
612 equations disagreed with the invariant semantic coefficient counts.
All results and hashes from that malformed stream were invalidated and
removed.  The corrected stream has 813--1,215 nonzero coefficient equations,
and the per-orbit tuples

\[
 (\text{shape},\text{orbit size},\text{kernel dimension},
   \text{nonzero coefficient count})
\]

agree with the independently generated primary census.  No primary
generator strings or parameterization were imported into the checker.

## 6. Independent unit ideals

After substituting the complete normalized incidence kernel, each orbit
gives the full affine coefficient ideal of (A16) in \(92\), \(94\), \(96\),
or \(98\) variables.  The program uses no saturation, inverse variable,
nonzero declaration, localization, or generic stratum.  Therefore zero
coordinates, rank drops, and every cancellation branch remain in the ideal.

A fresh post-correction run spawned a separate Singular process for every
orbit.  Over \(\mathbb Q\), all \(70\) reduced bases were \([1]\).  Hence
the ideals have no common zero over \(\mathbb C\).  All \(70\) corrected
generator hashes are frozen in the checker.  The aggregate ledger containing
orbit number, representative, variable count, equation count, and individual
hash is

```text
4f9dbccf21974ce045355a9861c0317a983fd48c6091543a763378d789873961
```

The replay finished with

```text
independent pure (3,1,1) common-power audit: PASS
```

## 7. Scope

The theorem permits arbitrary nonzero complex coefficients, arbitrary local
dimensions, arbitrary multi-site star rows, both endpoint orders, and
arbitrary complex cancellation.  Its restrictive hypothesis is the exact
pure-monomial multiplicity profile \((3,1,1)\).  It does not cover profile
\((2,2,1)\), four or more monomials in one target colour, non-pure four-site
target tensors, or the global descent from arbitrary even order.  Thus this
audit validates the advertised bounded obstruction but is not a proof of
Krenn's conjecture.
