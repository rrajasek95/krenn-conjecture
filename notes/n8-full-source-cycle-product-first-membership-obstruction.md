# The first full-source obstruction on the eight-site boundary chart

## Result

Let \(G\) be the first vertex-to-triangle expansion of the six-site prism and
let \(P_G\) be the product of its twelve properly coloured coordinate
variables.  In the **full** ring with all \(28\cdot 9=252\) arbitrary
endpoint-colour variables, let

\[
  I_{\mathrm{mix}}=(H_c:c\in\{0,1,2\}^8\text{ is not pure}),
\]

where \(H_c\) is the eight-site hafnian coefficient with colour word \(c\).
The exact checker proves

\[
  \boxed{P_G\notin I_{\mathrm{mix}}.}
\]

This is an exponent-one statement for this particular \(n=8\) graph.  It
does **not** prove \(P_G\notin\sqrt{I_{\mathrm{mix}}}\), and it gives no
uniform conclusion in \(n\).

## Why the computation is finite and lossless

Give a coordinate \(x_{uv}^{ab}\) degree one at each of the two coloured
ports \((u,a)\) and \((v,b)\).  The target \(P_G\) has degree one at all 24
ports.  Consequently, its entire multigraded Macaulay problem has the
following finite description.

* A target-row monomial is a perfect matching of the 24 coloured ports.
* A source column is \(QH_c\), where \(c\) is any of the \(3^8-3\) mixed
  words and \(Q\) matches the 16 complementary ports.
* The column \(QH_c\) has all 105 eight-site perfect-matching terms.  Neither
  endpoint-colour variables nor extra vertex pairs are suppressed.

Filter rows by the number of variables outside the twelve-variable support
of \(P_G\).  Project through filtration degree four.  The full stabilizer of
the coloured support in \(S_8\times S_3\), reconstructed exhaustively by the
checker, has order four.  Reynolds averaging is lossless in characteristic
zero.  The invariant incidence component containing \(P_G\) has

\[
  5{,}554\text{ row orbits},\qquad
  19{,}676\text{ column orbits}.
\]

Its row-orbit counts in filtration degrees \(0,1,2,3,4\) are respectively

\[
  1,\ 0,\ 35,\ 352,\ 5{,}166.
\]

Columns whose first filtration degree exceeds four cannot meet the dual
below.  Any remaining column that meets it lies in this incidence component
by construction.  Thus the truncation loses no equation relevant to the
certificate.

## The exact dual certificate

Sparse elimination modulo 1009 finds rank \(5{,}551\) and left nullity
three.  One null vector has support on only 24 row orbits, takes only the
values \(+1,-1\), and takes value \(1\) on \(P_G\).  These modular values are
used only to discover the vector.  The checker then:

1. replays the 24 coefficients over the integers against every one of the
   19,676 orbit-sum columns;
2. expands an orbit coefficient \(s\in\{\pm1\}\) to the rational value
   \(s/|\mathcal O|\) on every actual row in that orbit; and
3. replays this expanded functional against every individual column in the
   component over \(\mathbb Q\).

The expanded functional is supported on 93 actual port matchings.  Writing
it as \(\Lambda\), the exact result is

\[
  \Lambda(P_G)=1,
  \qquad
  \Lambda(QH_c)=0
\]

for every balanced source column.  This is a rational separating
functional, hence proves \(P_G\notin I_{\mathrm{mix}}\).  The complete list
of the 24 signed orbit representatives is part of the checker's frozen
SHA-256 ledger rather than copied into this note.

The familiar one-hot identity explains why the obstruction is initially
hard to see: a triangular lift repairs all residuals in filtration degrees
two and three.  The first unavoidable incompatibility appears only when the
degree-four rows are included.

## Why this dual does not automatically prove radical nonmembership

The 24-orbit vector is not a multiplicative edge character in disguise.
The 93 nonzero rows collectively use 60 coordinate edges.  Those same 60
edges admit the following further perfect matching, on which the functional
is zero:

```text
0100  0211  0520  1420  1610  2322
2702  3402  3411  5622  5710  6711
```

Here `uvab` denotes \(x_{uv}^{ab}\).  The nonzero support of any
edge-factorized functional

\[
  M\longmapsto \operatorname{sgn}_{\mathrm{Pf}}(M)
  \prod_{e\in M}w_e
\]

contains every perfect matching made from its nonzero edges.  The displayed
matching therefore rules out every such weighted Pfaffian or monomial
character, independently of the port ordering.  Direct checks also show
that alternating-cycle parity takes both signs and that the natural
Pfaffian-orientation ratio takes both signs on the dual support.

There is a second, stronger counterguard.  Form the most canonical square
in the monomial dual,

\[
  \Lambda^{*2}(M)=
  \sum_{M=R S}\Lambda(R)\Lambda(S).
\]

It has value one on \(P_G^2\).  The checker enumerates every exponent-two
generator column that can pair nontrivially with this finite-support
functional and finds an exact nonzero pairing.  Thus this particular dual
does not extend even to exponent two by convolution.  This failure does not
put \(P_G^2\) in the ideal; it only closes the tempting shortcut from the
degree-twelve circuit to all powers.

## Next exact question

The next balanced target is \(P_G^2\).  It has port multidegree two and
ordinary degree 24; a source multiplier then has ordinary degree 20.  The
exact Macaulay formulation is still finite: rows are multisets of 24
coordinate edges with degree two at every coloured port, while the
multiplier for a word \(c\) has port degree one at \((v,c_v)\) and degree
two at the other two ports of vertex \(v\).  Each column again has 105
outputs, and the same order-four stabilizer acts.  An honest census of its
target incidence component was deliberately not started here.

The two honest next attacks are:

* construct the exponent-two incidence component and look for a new dual;
  or
* localize at the twelve support variables and search directly for a common
  zero of all mixed coefficients, which would prove
  \(P_G\notin\sqrt{I_{\mathrm{mix}}}\) without testing powers one at a time.

The second is probably the faster route to a radical statement.  The
degree-one obstruction is a sparse circuit of the filtered hafnian
coefficient map, not a visible character that can simply be exponentiated.

## Reproduction

```sh
python3 computations/verify_n8_full_source_cycle_product_membership.py
python3 -O computations/verify_n8_full_source_cycle_product_membership.py
python3 -I computations/verify_n8_full_source_cycle_product_membership.py
python3 -S computations/verify_n8_full_source_cycle_product_membership.py
```

All four modes reconstruct the full support stabilizer, rediscover the
sparse vector, replay it exactly, audit the non-character counterexample,
and check the failed convolution square.  The default-prime ledger is
frozen by SHA-256.
