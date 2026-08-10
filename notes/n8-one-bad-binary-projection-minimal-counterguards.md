# The one-bad binary projection is feasible in two minimum orbits

## Verdict

The clean binary question left by the anchor-safe one-bad reduction is
feasible.  On six residual sites there are exact rational packets with

\[
 H^{[3]}=0,
 \qquad p_i s_jH^{[2]}=\delta_{ij}X_i
       \quad(i,j\in\{b,c\}).                            \tag{1}
\]

The smallest packets use four decorated cells of `H` and one scalar entry
in each of the four star rows.  A coefficient-complete enumeration gives
`2,160` labelled minimum packets in two orbits under residual-site
permutation, exchange of `b,c`, and simultaneous exchange of the two
selected endpoints.  Thus the binary projection alone cannot contradict
the one-bad packet.

The exact checker is
`computations/verify_n8_one_bad_binary_projection_minimal_counterguards.py`.

## An exact rational guard

Put `(b,c)=(0,1)` on sites `0,...,5` and take

```text
H = 24:00 + 35:00 + 05:11 + 14:11,
p0 = e0@0,   s0 = e0@1,
p1 = e1@2,   s1 = e1@3.
```

The two diagonal responses are the unique monochromatic matchings on their
four-site complements, while both cross responses have no physical
matching.  The four internal edges form two disjoint three-vertex paths,
so they have no three-edge physical perfect matching.  Hence, literally,

\[
 H^{[3]}=0,\qquad
 p_0s_0H^{[2]}=X_0,\quad p_1s_1H^{[2]}=X_1,\quad
 p_0s_1H^{[2]}=p_1s_0H^{[2]}=0.                       \tag{2}
\]

This packet has total scalar support eight.  It is fully
common-provenance inside the binary projection, but it is not a ternary
source and not a Krenn counterexample.

## Correction: the overlapping four-cell packet leaks

The tempting packet

```text
H = 01:00 + 23:00 + 01:11 + 24:11,
p0 = e0@4,   s0 = e0@5,
p1 = e1@5,   s1 = e1@3
```

does have zero cross rows, but it is **not** an exact diagonal packet.  Its
literal matching expansion contains

\[
 [p_0s_0H^{[2]}]_{110000}=1,
 \qquad [p_1s_1H^{[2]}]_{001111}=1.                   \tag{3}
\]

These mixed diagonal leaks are why a support-only test overcounted the
minimum census as `3,150` packets in five classes.  The checker now compares
the complete coefficient tensor in every one of the four response rows.

## Minimality and the two orbit types

A nonzero coefficient of `p_i s_iH^[2]=X_i` selects two distinct star holes
and a two-edge monochromatic matching on their four-site complement.  Thus
each colour requires at least two decorated internal cells and one nonzero
scalar entry in each of `p_i,s_i`.  The two colours use distinct decorated
cells and distinct star-row entries, even when physical sites coincide.
Every packet therefore has at least four internal cells and four star
entries, and (2) attains both bounds.

At equality, enumerate the 30 ordered hole pairs and the three matchings of
each four-site complement for each colour.  Among the resulting `8,100`
labelled channel choices, exactly `2,160` satisfy the complete equation
(1).  Their orbit census is

| common star holes | internal union components | labelled packets |
|---:|---|---:|
| 1 | `P5 + K1` | 1,440 |
| 0 | `P3 + P3` | 720 |

Each row is one orbit.  The guard (2) is in the `P3+P3` orbit.

## The load-bearing `a`-colour coupling

Write a putative ternary lift as `q=H+d`.  Since `H^[3]=0`, the unary top
and four binary response rows become

\[
 \boxed{
 \begin{aligned}
 dH^{[2]}+d^{[2]}H+d^{[3]}&=X_a,\\
 p_i s_j(dH+d^{[2]})&=0
                 &&(i,j\in\{b,c\}).                  \tag{4}
 \end{aligned}}
\]

The first equation forces an all-`a` perfect matching, but it shares the
same source cells with every response equation.  This common provenance is
the load-bearing information absent from the feasible binary projection.

## The sharp seven-cell one-bad boundary is empty

At equality in the internal-cell charge, `q` has exactly one three-edge
all-`a` perfect matching, one two-edge `b` near-perfect matching, and one
two-edge `c` near-perfect matching.  There are
`15*45*45=30,375` labelled decorated support choices.  Literal matching
expansion leaves exactly `3,960` whose top tensor is `X_a`.  After orienting
the response-hole pairs, exactly `1,440` packets also satisfy both diagonal
response tensors.  Up to residual `S_6` and exchange of `b,c`, they form two
source-oriented orbits, each of size 720.

A canonical pair is

```text
Ma = 01|23|45,
Mb = 02|14,       (pb,sb) = (3,5),
Mc = 03|15,       (pc,sc) = (2,4) or (4,2).
```

In every one of the 1,440 packets, **each** ordered off-diagonal response
has exactly one physical matching monomial, with unit coefficient.  It
cannot cancel.  Hence

\[
 \boxed{\text{no seven-cell equality packet satisfies the full }2\times2
        \text{ binary response matrix}.}              \tag{5}
\]

Any one-bad survivor therefore has at least eight internal scalar cells.
The next theorem must control the first cancellation mate of one of the
private cross routes.  The natural source-faithful formulation is a
matching-exchange lemma: an alternate two-matching on the four-site
complement should either create a forbidden mixed top coefficient or give
an anchor-increasing source switch.  This is not another binary projection
question.

## Reproduction

```sh
uv run python computations/verify_n8_one_bad_binary_projection_minimal_counterguards.py
PYTHONOPTIMIZE=1 uv run python computations/verify_n8_one_bad_binary_projection_minimal_counterguards.py
```

Both modes freeze the ledger hash printed by the checker.
