# The minimum non-pure zero-top profiles are unit-excluded, but the first contracted common-`q` packet survives two channels

## Result

Work on the six residual sites, project to the three labelled target axes,
and put

\[
                 F=q^{[2]},\qquad q^{[3]}=0.                 \tag{1}
\]

The contracted full-nine consequence in the scalar-zero branch is

\[
                         rF=\Delta _6=X_0+X_1+X_2.           \tag{2}
\]

There is a complete exact classification at the minimum possible decorated
coordinate support of `q`.

1. Equation (2) forces two disjoint pure `cc` cells for each colour, hence
   at least six cells.  At exactly six cells, `q^[3]=0` leaves `37,845`
   labelled parent triples, in `23` orbits under `S_6 x S_3`.
2. A non-pure `F` has at least two mixed four-site words.  The `2,430`
   minimum profiles form exactly two orbits, of sizes `270` and `2,160`.
   Both carry a coefficient-uniform two-word Fredholm unit, so neither can
   satisfy (2), even for an arbitrary response quadratic `r`.
3. The first contracted survivor has four mixed words.  It is the orbit of

   ```text
   M0 = 01|23,   M1 = 02|14,   M2 = 03|15.              (3)
   ```

   This is a literal six-cell common `q`; it satisfies `q^[3]=0`.  Moreover
   it admits both a two-channel contracted response and an invertible,
   scalar-zero, rootful three-channel contracted response.

The last item is a guard, not a full source.  For the displayed three-channel
factorization, seven of the nine separate endpoint rows fail.  Thus the
minimum common-power and two-channel attacks stop exactly at the following
new datum:

> prove that no factorization of the contracted survivor extends to a
> three-by-three endpoint rectangle with
> `p_i s_j F = delta_ij X_i`, or construct such a rectangle.

The exact checker is
[`verify_h3_zero_top_common_q_minimum_parent_gate.py`](../computations/verify_h3_zero_top_common_q_minimum_parent_gate.py).

## 1. Why six cells are forced

If (2) holds, each pure target word `X_c` has a nonzero coefficient.  Some
term of `F=q^[2]` contributing to it is a product of two disjoint pure `cc`
cells of `q`.  Choosing one such parent for each colour gives two cells
`M_c` and a missing pair `P_c`.  Cells belonging to different colours are
distinct, so there are at least six decorated cells.

At support six these chosen cells are all of `q`.  A perfect matching in
their underlying graph produces a nonzero term of `q^[3]`.  Its coloured
word has only one matching parent: for each colour, the two available edges
are already fixed.  Therefore it cannot cancel.  Conversely, without an
underlying perfect matching the top vanishes termwise.  This makes (1) a
finite census of triples of two-matchings on `K_6`.

Every one of the `37,845` zero-top triples has target-fixing diagonal gauge
rank six.  Hence arbitrary nonzero coefficients on its six cells can be
normalized to one without changing `Delta_6`.  No coefficient specialization
is hidden in the orbit census.

The exact mixed-word histogram is

| number of mixed words of `F` | 0 | 2 | 3 | 4 | 5 | 6 |
|---:|---:|---:|---:|---:|---:|---:|
| labelled triples | 90 | 2,430 | 7,200 | 14,040 | 6,480 | 7,605 |

The zero-mixed stratum is the already excluded pure-lift branch.  The two
minimum non-pure representatives are

```text
A: 01|23, 01|23, 02|13       orbit 270
B: 01|23, 02|13, 03|14       orbit 2160.                (4)
```

For each, the checker constructs polynomials `A(q),B(q)` and a mixed word
`w` such that the two catalecticant rows obey

\[
 B(q)\,[w](rF)-A(q)\,[X_c](rF)=0,                       \tag{5}
\]

where `A(q)` is a single nonzero coefficient monomial.  The left side
vanishes for every `r`, while its value on `Delta_6` is `-A(q)`, a unit on
the coefficient torus.  This is stronger than a rank or generic-coefficient
test.

## 2. The first contracted survivor

For (3), take the six unit cells

```text
01:00, 23:00, 02:11, 14:11, 03:22, 15:22.              (6)
```

Then `q^[3]=0` and

```text
F = 0000.. + 111.1. + 22.2.2
  + 121..2 + 21.21. + .1001. + .200.2.                 (7)
```

Put

\[
 r_2=(45{:}00)+(35{:}11)+(24{:}22)+(23{:}21).          \tag{8}
\]

Direct multiplication gives

\[
                         r_2F=\Delta _6.                \tag{9}
\]

This response really has two endpoint-product channels in the square-zero
site algebra.  Set

\[
\begin{aligned}
 u_0&=e_{4,0}+e_{2,2},&v_0&=e_{5,0}+e_{4,2},\\
 u_1&=e_{5,1}+e_{2,2},&v_1&=-e_{5,0}+e_{3,1}.
\end{aligned}                                          \tag{10}
\]

The same-site products disappear, and the remaining cross-site terms give

\[
                         u_0v_0+u_1v_1=r_2.             \tag{11}
\]

Thus the rank-at-most-two replacement supplied by the universal dark plane
does not contradict this packet.  Notice also that `r_2^[3]=0`; the singular
replacement is not required to preserve the root of the original response.

Now add the dark channel

\[
                         u_2=e_{0,0},\qquad v_2=e_{1,0}. \tag{12}
\]

Every term of (7) meets site zero or site one, so `(01:00)F=0`.  Consequently

\[
 r_*=r_2+(01{:}00),\qquad r_*F=\Delta _6,               \tag{13}
\]

while

```text
r_*^[3][002100] = r_*^[3][002121] = 1.                  (14)
```

Take `K_*=I` and the direct block with sole nonzero entry `a_01=-1`.  Then

\[
 K_*=\operatorname {tr}(a)E_{01}-a_{01}I=I,
 \qquad \langle K_*,a\rangle=0.                         \tag{15}
\]

Equations (1), (13)--(15) therefore retain the invertible scalar-zero and
rootful *contracted* data in the exact residual branch.

## 3. The load-bearing failure is the endpoint rectangle

Use (10), (12) as the three displayed `p` forms and the corresponding
`v` forms as `s`.  Their diagonal sum is (13), but their nine separate
products are not the full-nine packet.  The nonzero rows are

```text
00: 000000 + 212210 + 222222
01: -000000 + 121102 - 212210
10: 000021 + 212210 + 222222
11: 111111 - 212210
20: 010010 + 020022
21: -010010
22: 0.                                                        (16)
```

Thus entries `00,01,10,11,20,21,22` fail their required individual values;
only `02` and `12` vanish as desired.  Summing the diagonal entries cancels
`212210` and gives exactly `Delta_6`, which explains why contraction alone
cannot see the defect.

This calculation does **not** prove that every possible factorization of
`r_*` fails full nine.  It freezes the precise next problem: classify
three-dimensional left/right endpoint spaces whose whole product rectangle
lands in the labelled target span.  Any proof using only `q^[3]=0`, the
contracted equation, response root, or the singular two-channel replacement
is refuted by (6)--(15).

## Scope and reproduction

The theorem is exhaustive only at decorated target-coordinate support six.
A general source can first be projected to the three target axes, but a
support-nine-or-higher packet can contaminate every two-word unit and remains
outside this census.  The guard is not asserted to be an exact full-nine
source and hence is not a counterexample to the desired theorem.

```text
python3 computations/verify_h3_zero_top_common_q_minimum_parent_gate.py --mode structural
python3 -O computations/verify_h3_zero_top_common_q_minimum_parent_gate.py --mode full
python3 -I -S computations/verify_h3_zero_top_common_q_minimum_parent_gate.py --mode exhaustive
```

All modes replay the same exact orbit, polynomial-unit, common-power, and
endpoint-row calculations.
