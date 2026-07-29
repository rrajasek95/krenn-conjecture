# Independent audit of the sole-defect packet obstruction

## 1. Verdict

The
[primary packet theorem](sole-defect-nonseparable-packet-common-power-obstruction.md)
is correct at the frozen snapshot below.  A clean-room reconstruction gives
the same support census

\[
                 1284\longrightarrow157=145+12,
\]

and all 145 rational affine ideals and all twelve nonzero-parameter Laurent
ideals are the unit ideal.  The reconstruction found no omitted support,
coefficient orbit, parameter specialization, or logical gap in the response
consequence.

The primary snapshot audited here has SHA-256 identities

~~~text
ea1723d75d9b92296352772bb5c483d98f09d6214cb79371d55ee15ce4f980ba  notes/sole-defect-nonseparable-packet-common-power-obstruction.md
64e60dfc5247775d485fe5d69b6d849037645d53cfeedaff85a4f41fbbfce72f  computations/verify_sole_defect_nonseparable_packet_common_power.py
15a32578d59aa9b6193bb8ba9b89166f9a80a6c53a29962ef50fd31b7d5e07b4  computations/explore_sole_defect_nonseparable_packet_orbits.py
85e41c670bb113bbe7d25beb1114e2f7dd14e1f7cc228147fa64dd19308889f8  computations/verify_sole_defect_nonseparable_normalizable_packets.py
93e5148fd08c16d3d191bead6f4c2e033e8104d5238f3e66aff9527391300ce8  computations/verify_sole_defect_nonseparable_parameter_packets.py
~~~

The primary ledger-only replay reproduces its global digest

~~~text
7e766f3e56aee47b3b623dcbc1c5db60ac145deaa735c543746507a5fe1295f4
~~~

## 2. Selector and packet reduction

The
[independent checker](../computations/audit_sole_defect_nonseparable_packet_common_power_independent.py)
exhausts all (15\cdot14\cdot13=2730) labelled triples of distinct selected
pairs.  For each selected field pair (P_r), it tests all fifteen candidate
pairs (P) and recovers directly

\[
 \Phi(A_r(P))\ne0
 \quad\Longleftrightarrow\quad
 P_r\setminus\{o\}\subseteq P.
\]

Across the three positions in all triples, this gives 5,460 selected
all-good occurrences and 2,730 selected incident occurrences.  Every
all-good occurrence has exactly one survivor, its selected lift.  Every
incident occurrence has exactly five possible survivors: the incident lift
and the four good arms through its anchor.  The checker also verifies that
every good vector killed by the selector is omitted from every survivor, so
restoring that unused vector changes neither the projected multiplier nor
the power equations.

The bad-site separability table is not hard-coded into the support filter.
Using the alternative rational models

\[
 ((1,1),(1,-1),(0,1)),\qquad
 ((1,1),(1,-1),(1,1)),\qquad
 ((-2),(3),(5)),
\]

the checker determines whether the retained vectors avoid the span of the
killed vectors.  It independently recovers exactly

| bad matroid | nonseparable incident-field sets |
|---|---|
| three-line circuit | the three two-subsets |
| fields zero and two coincident | \(\{0\},\{2\},\{0,1\},\{1,2\}\) |
| rank one | every nonempty proper subset |

Thus the reduction to packet systems for which every SDR is locally
nonseparable is exhaustive.

## 3. Independent orbit and coefficient census

The clean-room quotient uses descending edge encodings, **maximal** rather
than minimal representatives, reversed enumeration, and the residual
stabilizer of each normalized selected-SDR slice.  It tests local
separability by enumerating every SDR, rather than using the primary's
closed-form arm filter.  The result is

| normalized slice | initial orbits | no separable SDR | normalizable | one parameter |
|---|---:|---:|---:|---:|
| circuit \(K_2\) | 294 | 6 | 6 | 0 |
| coincident \(K_1\) | 85 | 14 | 14 | 0 |
| coincident \(K_2\) | 560 | 64 | 58 | 6 |
| rank-one \(K_1\) | 51 | 9 | 9 | 0 |
| rank-one \(K_2\) | 294 | 64 | 58 | 6 |
| **total** | **1284** | **157** | **145** | **12** |

Coefficient normalization is checked as an integer-lattice calculation.
For every active pair (P), the good-axis rescaling character is

\[
             \chi_P(v)={\bf1}_{v\notin P},\qquad v\in G.
\]

For every isolated lift and every packet with at most three arms, the
character rows have full row rank and contain a determinant-(\pm1)
maximal minor.  Hence arbitrary nonzero coefficients normalize to one on a
unimodular torus chart, without root extraction.

For a full packet, the five character rows have rank four, a
determinant-(\pm1) four-row chart, and the primitive relation

\[
             -3\chi_{\{o,a\}}+
             \sum_{w\in G\setminus\{a\}}\chi_{\{a,w\}}=0.
\]

Consequently its sole invariant is exactly

\[
       \mu=\frac{\prod_{w\ne a}\lambda_{\{a,w\}}}
                    {\lambda_{\{o,a\}}^3}\in\mathbb C^*.
\]

The checker verifies that every exceptional support has exactly one full
packet and that the four coefficients other than its independently chosen
parameter arm have a determinant-(\pm1) normalization chart.  This gives
the twelve one-parameter cases and no additional coefficient strata.

## 4. Independent common-power ideals

The rational calculation uses the alternate local coordinates above,
reversed good axes, cells, target terms, matching equations, and variables,
rightmost-pivot exact RREF, sparse monomial dictionaries, and Singular's
`Dp` order.  It imports no primary packet checker or primary ledger.  For
each case it literally collects equal six-site words in (qF=0), substitutes
a complete kernel into every coordinate of (q^{[2]}-F), and checks the
resulting unsaturated affine ideal over \(\mathbb Q\).

All 145 rational ideals are unit ideals.  The independent rank census is

| slice and class | \(\operatorname{rank}(qF)\), with multiplicity |
|---|---|
| circuit \(K_2\), normalized | \(21:6\) |
| coincident \(K_1\), normalized | \(24:14\) |
| coincident \(K_2\), normalized | \(21:9,27:17,33:20,39:12\) |
| coincident \(K_2\), parameter | \(39:3,45:3\) |
| rank-one \(K_1\), normalized | \(21:9\) |
| rank-one \(K_2\), normalized | \(15:6,21:17,23:3,27:20,33:12\) |
| rank-one \(K_2\), parameter | \(33:3,39:3\) |

For the twelve parameter cases, elimination is performed over
\(\mathbb Q[\mu,\mu^{-1}]\), and every division is audited before it occurs.
Across all twelve matrices the only pivot values are

\[
                     1,-2,5,\mu,-2\mu.
\]

Thus every inverted element is a rational unit times a power of \(\mu\).
In particular, no factor such as \(\mu-1\), and no other exceptional
polynomial, is inverted.  The checker embeds the Laurent system into

\[
             \mathbb Q[\mu,\eta]/(\mu\eta-1)
\]

and all twelve resulting ideals are the unit ideal.  This covers every
specialization \(\mu\in\mathbb C^*\), not merely a generic parameter.
Singular 4.4.1 returned all (145+12=157) unit results.

The frozen independent combined ledgers are

| class | slice | independent SHA-256 |
|---|---|---|
| normalized | circuit \(K_2\) | `01930f27cbf9199d81364104ca353b40b9b224cbb8869b7e64791b7ab7436a28` |
| normalized | coincident \(K_1\) | `b64fbcecc520945b18f3b16710dd132a42247415c2f299242fe7b3e190b5b510` |
| normalized | coincident \(K_2\) | `12a0378f8dfcf2211eaabd423ca79d7111de0f8a690d70ccf4f71a5fd7a8e907` |
| normalized | rank-one \(K_1\) | `5865f563370fbbb03a2769164589d92dd1638bac714d157132a8b7c93332de99` |
| normalized | rank-one \(K_2\) | `5f944b4d6da9bd2e0f4ec66455fc3cb27e7cac59fcf2c855aba2561139136522` |
| parameter | coincident \(K_2\) | `3d326aede259c83dcffba26fac1544e6af39642c754a01f1b5ad9c35f8558dbb` |
| parameter | rank-one \(K_2\) | `6eb3b36f984366ae470da827ee36fa3b6b26485f13b0d2979a8b82e5dd85c1c8` |

Their independently ordered global stream has SHA-256

~~~text
6d021a3534732e8815b6931a88664862f9b910a6cfa1dd7fdbd009403224022c
~~~

## 5. Audit of the response implication

Section 6 of the primary note has the correct dependency chain.

1. With exactly one deficient frame, the other five good frames split the
   field modules, and the degenerate response normal form proves every
   active family (H_r) is nonempty.
2. The response singleton lemma excludes two equal singleton families.
3. If the three nonempty families had no SDR, Hall failure on two families
   would be exactly such an equal-singleton collision.  Hence failure must
   occur on all three and their total union has size at most two.  A
   one-pair union again creates equal singleton families, so the union has
   exactly two pairs.  Its only profiles are
   \((2,2,2),(2,2,1),(2,1,1)\), with distinct singleton pairs in the last
   profile.
4. The independently audited two-pair theorem rules out all those
   no-SDR systems, so an ordinary SDR exists.
5. The packet theorem audited here rules out every system possessing such
   an SDR: a locally separable choice reduces to the distinct-lift theorem,
   and a nonseparable choice reduces to one of the 157 packet ideals.

Therefore the sole-defect response branch is empty.  Axial and bridge
normal forms both enter this argument only through three nonempty active
families, so no bridge-specific premise is missing.

The conclusion is deliberately limited to exactly one deficient site.  It
does not extend the packet selector, the five-good-site module split, or the
local separability census to two or more deficient sites.

## 6. Reproduction

Run the complete clean-room calculation with

    uv run python computations/audit_sole_defect_nonseparable_packet_common_power_independent.py

or rebuild and check every frozen ledger without the 157 Singular calls:

    uv run python computations/audit_sole_defect_nonseparable_packet_common_power_independent.py --ledger-only

