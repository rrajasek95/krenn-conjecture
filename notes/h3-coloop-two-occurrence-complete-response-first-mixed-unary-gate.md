# The first full-row obstruction is a mixed unary mate, not transverse rank

## Literal two-occurrence packet

Take the pure-zero coloop

\[
 \alpha=q_{01}^{00}=1,
 \qquad C_c=q_{23}^{00}q_{45}^{00}=1.                \tag{1}
\]

In the pure-one response coefficient `R11[111111]`, retain precisely

\[
\begin{aligned}
 f&=p_1[0,1]s_1[1,1]q_{23}^{11}q_{45}^{11}=1/2,\\
 g&=p_1[1,1]s_1[4,1]q_{02}^{11}q_{35}^{11}=1/2.     \tag{2}
\end{aligned}
\]

The checker gives all named source factors explicitly and enumerates every
endpoint placement and residual matching.  There are exactly the two
occurrences (2), and the complete pure-one coefficient block is

```text
unary[111111] = 0
R11[111111]   = 1
R12[111111]   = 0
R21[111111]   = 0
R22[111111]   = 0.
```

Thus this is a literal complete-row guard, not a two-column incidence
placeholder.  It also satisfies the normalized pure-zero unary coefficient
through the coloop factorization (1).

Checker:

```text
computations/verify_h3_coloop_two_occurrence_complete_response_first_mixed_unary_gate.py
```

## First occurrence-transverse minors

After localizing the nonzero factors of `f,g`, restrict the adjacent rows to
these two occurrence columns.  Write

```text
a = s2/s1,     b = p2/p1,
c = closing q-edge/(p1*s1).
```

The row restrictions are

\[
 (1,1),\quad(a_f,a_g),\quad(b_f,b_g),
 \quad(a_fb_f,a_gb_g),\quad(c_f,c_g),                \tag{3}
\]

for `R11,R12,R21,R22,unary`.  Therefore the first transverse minors against
the aggregate row are

\[
 a_g-a_f,\quad b_g-b_f,\quad
 a_gb_g-a_fb_f,\quad c_g-c_f.                        \tag{4}

In the literal guard all four vanish.  In particular, the pure-colour
coloop plus the complete unary/four-response equations at the selected word
do not force an occurrence-asymmetric physical row.  This sharpens the
abstract `f -> f+t, g -> g-t` obstruction from `55eed59` without claiming
that the redistribution extends through every word coefficient.

## The first omitted coefficient

The extension fails first in a precise physical row.  Lexicographically,
the first nonzero mixed unary word is

\[
 H_0[000011]supset
 q_{01}^{00}q_{23}^{00}q_{45}^{11}=1/2.             \tag{5}
\]

The GHZ target value of this mixed coefficient is zero.  Hence the complete
equation `H_0[000011]=0` forces at least one of the other fourteen perfect-
matching monomials to be nonzero.  Their exact split is

```text
2  all-diagonal mates: 02|13|45 and 03|12|45
12 mates with two cross-colour edges
   (2 of these retain the coloop edge 01).
```

Thus the full equations first force a literal unary matching mate, not one
of the minors (4) directly.  The next theorem should land that mate through
the existing active/Hall routes or show that its complete response
coefficient has unequal `f,g` restriction.

## Scope

This packet satisfies the coloop normalization and all five GHZ coefficient
equations at `111111`.  It is deliberately not asserted to solve every GHZ
word equation: its smallest failure is the explicit coefficient (5).
Consequently it proves nonimplication from the named complete rows and
identifies the first new physical datum; it is not a counterexample to the
conjecture.

## Verification

Run

```text
python3 computations/verify_h3_coloop_two_occurrence_complete_response_first_mixed_unary_gate.py
python3 -O computations/verify_h3_coloop_two_occurrence_complete_response_first_mixed_unary_gate.py
python3 -I -S computations/verify_h3_coloop_two_occurrence_complete_response_first_mixed_unary_gate.py
```

Frozen ledger SHA-256:

```text
f9834ae5bf043b6875c1b7a24f968fe6a56d956c7b68f7a0267dc59369fdd2f5
```
