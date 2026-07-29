# Independent audit of the compatible three-cell pair-cap obstruction

## 1. Result and boundary

In the eight-site ternary square-zero algebra, retain

\[
\begin{aligned}
q={}&23_{00}+45_{00}+67_{00}
     +01_{11}+36_{11}+57_{11}\\
   &+02_{22}+14_{22}+56_{22},\\
z={}&01_{00}+24_{11}+37_{22}.
\end{aligned}                                                   \tag{1}
\]

Let \(e<f<g\) be three cells outside the displayed support of \(q\), let
\(t,u,v\in\mathbb C^\times\), and put

\[
                         Q=q+te+uf+vg.                          \tag{2}
\]

The standalone clean-room checker
[`verify_polarized_eight_site_fixed_q_compatible_three_extra_independent.py`](../computations/verify_polarized_eight_site_fixed_q_compatible_three_extra_independent.py)
imports neither fixed-\((q,z)\) three-cell verifier.  It independently finds
exactly \(87,027\) triples for which

\[
                         zQ^{[3]}=\Delta_{8,3}                  \tag{3}
\]

holds identically in \(t,u,v\).  A parameter-safe projective Gram argument
excludes \(86,284\) of them from the pair-cap locus.  Of the \(743\)
projective survivors, the sole triple contained in one physical pair is

\[
                    (17_{00},17_{02},17_{22}).                  \tag{4}
\]

It is a specialization of the separately audited arbitrary full-block
theorem on pair \(17\), and is therefore excluded.  For the residual 742
triples using two or three physical pairs, the checker generates a complete
second set of saturated ideals with reversed variable and generator orders.
Every one of those 742 independently ordered ideals reduces to \([1]\) over
\(\mathbb Q\).  Hence all 87,027 compatible triples miss the pair-cap locus.

Nothing here covers four or more added cells, arbitrary quadratics, or the
missing all-even descent in Krenn's conjecture.

## 2. Clean-room compatible-triple census

There are \(252\) endpoint-colour cells on eight sites and three colours.
After deleting the nine cells of \(q\), the checker constructs directly

\[
 D_e=zeq^{[2]},\qquad D_{ef}=zefq,\qquad D_{efg}=zefg.          \tag{5}
\]

It obtains 99 cells with \(D_e=0\).  Among their
\(\binom{99}{2}\) pairs, exactly 3,960 have \(D_{ef}=0\).  It then enumerates
all triangles in this compatibility graph and checks \(D_{efg}=0\) literally
for every one.  The result is 87,027 compatible triples.  Their physical-pair
census is

| number of distinct physical pairs | compatible triples |
|---:|---:|
| 1 | 924 |
| 2 | 28,512 |
| 3 | 57,591 |
| **total** | **87,027** |

The lexicographically ordered compatible-triple list has SHA-256

```text
47d231f82e3e6bd272e0b440667a06fc6fe110716a916512555330d644e08a22
```

Thus the count does not rely on the earlier exhaustive classification of all
\(\binom{243}{3}\) outside-support triples.

## 3. Independent projective closure

A putative pair-cap preimage would give linear forms \(p,s\) and a scalar
\(a\) satisfying

\[
                  4psQ^{[3]}+4aQ^{[4]}=\Delta_{8,3},            \tag{6}
\]

because \(QQ^{[3]}=4Q^{[4]}\).  For every triple, the checker rebuilds every
coordinate of (6), retaining the exact exponent of \(t,u,v\) on each
contributor.

Write \(x_{i,c}=(p_{i,c},s_{i,c})\), and put

\[
 \beta(x_{i,c},x_{j,d})=p_{i,c}s_{j,d}+s_{i,c}p_{j,d}.          \tag{7}
\]

Only the following implications are used.

1. If a non-target coordinate has no \(aQ^{[4]}\) term and exactly one
   tagged Gram contributor, its coefficient is a nonzero monomial on
   \((\mathbb C^\times)^3\); hence that Gram entry vanishes.
2. If a pure target coordinate has no \(aQ^{[4]}\) term, at least one of its
   Gram contributors is nonzero.  The checker branches over every possible
   Gram edge.
3. Every endpoint of a required-nonzero Gram edge is a nonzero vector.  On
   its projective line, a forced-zero Gram edge applies the involution
   \(L\mapsto L^\perp\).  Therefore an odd zero-edge walk joining the
   endpoints of a required-nonzero edge is contradictory.

The implementation uses a parity-state breadth-first search and explicitly
replays each odd walk.  This differs from the primary checker’s component
bipartiteness implementation.  Zero edges incident with a possibly zero mode
are never used: the graph is restricted to endpoints already known nonzero.

The exact result is

| physical pairs | projectively closed | open branch | pure direct term |
|---:|---:|---:|---:|
| 1 | 923 | 1 | 0 |
| 2 | 28,283 | 165 | 64 |
| 3 | 57,078 | 320 | 193 |
| **total** | **86,284** | **486** | **257** |

The survivor census is therefore

\[
                       1+229+513=743.                           \tag{8}
\]

The canonical survivor ledger agrees exactly with the independent target of
the primary computation:

```text
b481e4abddc0e98e8cbde9486d7d384a821430b15964dde6e9b279367988a57a
```

The separate clean-room closure ledger, which also pins the chosen
odd-walk-certificate signatures, has SHA-256

```text
c3d4eb15e6ad9f53eee400197be8d1e5e68ab7a8b274c5377712935689f6d58a
```

## 4. Why the one-pair survivor is already excluded

The triple (4) gives

\[
 Q=q+t17_{00}+u17_{02}+v17_{22}=q+E_{17}(X),                   \tag{9}
\]

where \(X_{00}=t\), \(X_{02}=u\), \(X_{22}=v\), and the other six entries
of \(X\) are zero.  Pair \(17\) is one of the eleven invisible pairs in the
audited arbitrary-one-block theorem.  That theorem excludes (6) for every
\(X\in\mathbb C^{3\times3}\), with no nonzero-entry assumption.  It therefore
covers the complete torus family (9), not merely a generic point.

Deleting this already-covered triple leaves 742 multi-pair survivors.  They
are ordered lexicographically by their three cells; the checker prints the
exact list with `--print-survivors`.  Its list digest is

```text
025cb3d4d283ef8bab747ccf587eb97bd8741f0bc5bc642b3524b74dc44cbb0b
```

## 5. Independent full-ideal generator

For every residual triple, the checker generates all nonzero coordinate
equations in (6) over \(\mathbb Q\) and adds

\[
                         \rho v u t-1=0                         \tag{10}
\]

to restrict to \(tuv\ne0\).  There are 53 variables: \(\rho,v,u,t,a\) and
the 48 coordinates of \(p,s\).  The independent encoding deliberately uses

- the torus equation first;
- descending top-word order;
- direct \(aQ^{[4]}\) terms before Gram terms;
- descending tagged-term order; and
- reversed colour/site order, with each \(s\)-variable before its
  \(p\)-variable.

Thus its Singular programs are not textual copies of the primary generator.
The 742 systems contain between 223 and 343 nonzero equations (including
the torus equation).  Hashing, in order, each index, triple, equation count,
variable count, and exact program digest gives

```text
ddb50c85a030b693c98d5161a7fcc67ee26f269aaadb07b2013ad0d52d2aab9e
```

A preliminary wiring check ran the first three independently ordered
programs, with respectively 308, 317, and 304 equations.  All reduced to
\([1]\), with stable prefix-result SHA-256

```text
f6e3b857c597de2033e5f79c96ccbc1efb25ab8155d864a1fdf50237da618ef6
```

The subsequent complete replay reduced all 742 systems to \([1]\).  Its
independently ordered full-result SHA-256 is

```text
2e9ecab9ee8a62e41d6e7683bab9731138a137ca9e2662a6ff843a9f901e4e84
```

This full ledger, rather than the diagnostic prefix, certifies the closure.

## 6. Reproduction

From the repository root, reconstruct every finite ledger without launching
Singular:

```sh
python3 computations/verify_polarized_eight_site_fixed_q_compatible_three_extra_independent.py
```

Print all 742 residual triples with `--print-survivors`.  Run only a small
diagnostic prefix with, for example,

```sh
python3 computations/verify_polarized_eight_site_fixed_q_compatible_three_extra_independent.py \
  --ideal-prefix 3 --workers 2
```

The explicit `--all-ideals` option launches the complete heavy batch.  Its
cache is separate from the primary computation:
`/tmp/krenn-compatible-three-extra-independent-ideals`.

The audited full command was

```sh
python3 computations/verify_polarized_eight_site_fixed_q_compatible_three_extra_independent.py \
  --all-ideals --workers 8
```

It ended with 742/742 unit ideals and the frozen full-result digest above.
