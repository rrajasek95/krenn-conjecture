# The exact support-15 clean terminal census

Research result on the all-pairs-good eight-site stratum.  This is not a
proof of Krenn's conjecture: the all-pairs-good hypothesis remains stronger
than the currently guaranteed supply of good pairs.

## Outcome

Let `G` be the live aggregate support of an exact ternary eight-site source,
assume all 28 pairs are good, and suppose `|E(G)|=15`.  Then exactly one of
the following happens:

1. `G` has a coefficient-independent active clean edge;
2. `G` has an independent four-shore and is excluded by the proved complete
   mixed rows;
3. `G` has a degree-three--degree-three edge and the forced-anchor
   `2x2`-permanent lemma supplies an active clean cap; or
4. up to relabelling, `G` is the single graph

```text
01 02 03 04  12 13 16  24 27  35 37  45 46  56 57.   (1)
```

The last graph has degree sequence `(4^6,3^2)`; its two cubic vertices `6,7`
are nonadjacent.  It is the exact first unresolved support orbit.  Thus the
support result is a sharp routing theorem:

> An exact all-pairs-good source with at most fourteen support edges cannot
> exist.  At fifteen edges, absence of an active clean cap forces the
> 720-label orbit of (1).

The checker is
[`verify_n8_support15_clean_terminal_census.py`](../computations/verify_n8_support15_clean_terminal_census.py).

## 1. The generalized clean test

For a support edge `pq`, put

\[
 P=N(p)\setminus\{q\},\qquad S=N(q)\setminus\{p\},
 \qquad {\cal R}_{pq}=\{ij:i\in P,j\in S,i\ne j\}.
\]

Every edge of the effective response `r=B^K` lies in `R_pq`.  At eight
sites the homogeneous error is

\[
                       s_Kr^{[2]}x+r^{[3]}.             \tag{2}
\]

If none of the fifteen residual perfect matchings can be tagged `RRX` or
`RRR`, (2) vanishes for every cap and the nonzero direct block lets one
choose an active cap.  This test is coefficient-independent and uses the
literal support of the complete clean error.

At fifteen edges the degree sum is 30.  Above minimum degree three, the six
excess degrees have nine possible partitions.  The exact labelled census is

| degree sequence | labelled graphs | support terminals |
|---|---:|---:|
| `(7,5,3^6)` | 270 | 0 |
| `(7,4,4,3^5)` | 460 | 0 |
| `(6,6,3^6)` | 615 | 0 |
| `(6,5,4,3^5)` | 1,830 | 0 |
| `(6,4,4,4,3^4)` | 3,148 | 96 |
| `(5,5,5,3^5)` | 3,211 | 120 |
| `(5,5,4,4,3^4)` | 5,570 | 168 |
| `(5,4,4,4,4,3^3)` | 9,444 | 540 |
| `(4,4,4,4,4,4,3,3)` | 15,740 | 2,180 |

Thus 3,104 of 40,288 labelled graphs survive support alone.

## 2. Sixteen terminal orbits and fifteen exits

Quotienting by the literal degree-preserving permutation groups gives
sixteen graph orbits.  The following signature table is complete; `alpha4`
is the number of independent four-sets and `RRR edges` counts edges with at
least one cubic response matching.

| degrees | orbit | triangles | squares | `alpha4` | `RRR edges` | route |
|---|---:|---:|---:|---:|---:|---|
| `(6,4^3,3^4)` | 72 | 6 | 14 | 1 | 1 | independent shore |
|  | 24 | 6 | 12 | 1 | 3 | independent shore |
| `(5^3,3^5)` | 120 | 7 | 12 | 1 | 0 | independent shore |
| `(5^2,4^2,3^4)` | 24 | 6 | 11 | 0 | 1 | permanent zero |
|  | 96 | 5 | 15 | 1 | 1 | independent shore |
|  | 48 | 6 | 10 | 1 | 1 | independent shore |
| `(5,4^4,3^3)` | 36 | 6 | 11 | 0 | 0 | permanent zero |
|  | 72 | 7 | 8 | 0 | 0 | permanent zero |
|  | 144 | 6 | 10 | 0 | 1 | permanent zero |
|  | 72 | 4 | 14 | 1 | 1 | independent shore |
|  | 144 | 6 | 9 | 0 | 1 | permanent zero |
|  | 72 | 5 | 12 | 1 | 1 | independent shore |
| `(4^6,3^2)` | 720 | 5 | 10 | 0 | 0 | permanent zero |
|  | 720 | 6 | 9 | 0 | 1 | permanent zero |
|  | 720 | 5 | 9 | 0 | 0 | **unresolved (1)** |
|  | 20 | 0 | 27 | 2 | 9 | independent shore |

The eight independent-shore orbits reduce, after the exact invisibility
zeroing, as follows:

* three become `K4,4` minus a perfect matching, killed by the six unique
  mixed cube fibres;
* four become `K4,4` minus a three-edge matching, killed by the 141 mixed
  rectangle rows; and
* one becomes `K4,4` minus one edge, killed by the same dead-cross rows.

The checker invokes both exact full-row audits.  These are not support-only
claims.

Each of the other seven dispatched orbits has a degree-three--degree-three
support edge.  At such an edge the two external neighbour sets have size
two.  Since the graph is a support terminal, they are disjoint and the two
leftover vertices carry an active `x` edge.  The forced anchors at both cap
endpoints reduce `r^[2]x` to

\[
 (u_0^TKv_0)(u_1^TKv_1)+(u_0^TKv_1)(u_1^TKv_0),       \tag{3}
\]

times a nonzero coordinate tensor.  The rank-case proof in
[`n8-projective-cap-rank-dichotomy-and-minimum-support-clean-theorem.md`](n8-projective-cap-rank-dichotomy-and-minimum-support-clean-theorem.md)
shows that (3) always has a zero with all three diagonal cap readouts and
the direct scalar nonzero.  Hence these seven orbits are actively clean.

## 3. The exact first unresolved quadratic

Graph (1) has five triangles, nine four-cycles, no independent four-set,
and no degree-three--degree-three edge.  More sharply, every support edge has
zero `RRR` count: `r^[3]=0` everywhere.  Its fifteen `RRX` seals split as

| endpoint degrees | `RRX` matchings | edges |
|---|---:|---:|
| `(4,4)` | 3 | 2 |
| `(4,4)` | 6 | 2 |
| `(4,4)` | 8 | 5 |
| `(4,3)` | 4 | 2 |
| `(4,3)` | 2 | 4 |

The smallest map occurs at `37` (and symmetrically at three other
degree-`4`--degree-`3` edges).  Cap the cubic endpoint `7` against `3`.
The external `7`-anchors lie on `72,75`; write them

\[
                 A_{72}=u_0\otimes e_a,
                 \qquad A_{75}=u_1\otimes e_b.         \tag{4}
\]

At the degree-four endpoint retain the complete blocks
`M_0=A_30`, `M_1=A_31` without a rank or coordinate specialization.  The
shared external site `5` makes `r^[3]=0`, and the only two `RRX` matchings
give, up to the fixed coordinates at sites `2,5` and the active multiplier
`A_46`, the nine-component quadratic

\[
 F_{37}(K)=
 (u_0^TKM_0)\otimes(u_1^TKM_1)
 +(u_1^TKM_0)\otimes(u_0^TKM_1).                       \tag{5}
\]

This is the precise point where the scalar permanent proof stops.  If
`M_0,M_1` are invertible, (5) is equivalent to
`x tensor y+y tensor x=0`, which in characteristic zero forces `x=0` or
`y=0`.  For coordinate external anchor vectors, those alternatives can lie
entirely on diagonal inactivity faces.  The checker retains all coefficients
of (5): each of its nine components has 117 formal monomials.  It also pins
the sharp coordinate specialization `u_0=e_0`, `u_1=e_1`, `M_0=M_1=I`.
Writing `a=K_00`, `b=K_01`, `d=K_10`, `e=K_11`, three components are

\[
 F_{00}=2ad,\qquad F_{11}=2be,\qquad F_{01}=ae+bd,
\]

and the exact saturation certificate

\[
       4(ae)^2=4(ae)F_{01}-F_{00}F_{11}               \tag{6}
\]

shows that this local quadratic has no zero with `K_00 K_11 != 0`.  This is
only a local guard, not a full-source counterexample: a degree-four vertex
must itself supply three distinct anchors, and the complete mixed rows may
prevent the offending block placement.

The shortest next attack is therefore finite and source-labelled:

1. enumerate which one of the four incident edges at each degree-four
   vertex may fail to be an anchor;
2. propagate the three colour labels through the five triangles of (1);
3. substitute those forced forms into the four two-matching maps (5); and
4. either find an active common zero at one edge or expose a unique mixed
   fibre/full-row contradiction.

## 4. Reproduction

```sh
python3 computations/verify_n8_support15_clean_terminal_census.py
python3 -O computations/verify_n8_support15_clean_terminal_census.py
python3 -I -S computations/verify_n8_support15_clean_terminal_census.py
```

The frozen ledger digest is
`e2e82232d82107a844c228c9ed0c4a5e2ed072dd814b9736c46ffacb2e8e8b05`.
