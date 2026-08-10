# The one-bad formal guard advances exactly one cofactor layer

## Outcome

For every `h >= 3` there is an explicit actual quadratic `q` with

```text
q^[h] = X0
```

and a symmetric *formal* first/second-cofactor packet `(F,G)` which has all
four one-bad responses

```text
p1 s1 F = X1,   p1 s2 F = 0,
p2 s1 F = 0,    p2 s2 F = X2,
```

retains `p1^[2],p2^[2] != 0`, and satisfies both complete Euler layers

\[
  \sum_e q_eF_e=hq^{[h]},\qquad
  \sum_{f\cap e=\varnothing}q_fG_{e,f}=(h-1)F_e.       \tag{1}
\]

Thus the symmetric Hessian recurrence (1), treated only as a polynomial
identity, does **not** force a square-zero cap or a descent.  The first
unmet source identity is the third-cofactor recurrence

\[
  \sum_{g\cap(e\cup f)=\varnothing}q_gH_{e,f,g}
       =(h-2)G_{e,f}.                                  \tag{2}
\]

There is an essential scope guard.  The displayed `q` is genuine, but the
four corrections in `F` and `G` are not its actual hafnian cofactors.  If
`G` is required to be the genuine second cofactor of this `q`, (1) uniquely
restores the genuine `F`; the one-bad response circuit then disappears.
Accordingly this is a sharp formal tower guard, not a common-`q` source and
not a counterexample.

The exact checker is
`computations/verify_uniform_one_bad_second_cofactor_tower_gate.py`.

## The actual unary-top source

On sites `0,...,2h-1`, start with the unary matching

```text
01 | 23 | 45 | 67 | 89 | ...
```

whose cells all have colours `00` and coefficient one.  Add four coloured
bridges

```text
14:11, 04:11, 35:22, 25:22.                            (3)
```

Each bridge is top-inactive: after using it, the displaced partners cannot
be matched.  Hence the augmented physical source still has the unique
perfect matching above and therefore

\[
                             q^{[h]}=X_0                \tag{4}
\]

for every `h >= 3`.

Let `F^0_e` and `G^0_{e,f}` denote the genuine first and second cofactors
of this `q`.  Replace the first cofactors at the four response holes

```text
05, 15, 24, 34                                           (5)
```

by the exact minimum-response tensors from `9b26452`, leaving all other
first cofactors equal to `F^0`.  Write

\[
                         \Delta F_e=F_e-F^0_e.           \tag{6}
\]

With

\[
\begin{aligned}
p_1&=e_1^{(0)}+e_1^{(1)},&s_1&=e_1^{(5)},\\
p_2&=e_2^{(2)}+e_2^{(3)},&s_2&=e_2^{(4)},
\end{aligned}                                            \tag{7}
\]

these four replacements give exactly `X1,0,0,X2`.  Since every response
hole has `q_e=0`, the corrections do not change the top Euler sum, so the
first identity in (1) remains exact as a full tensor equation.

## Integrating the Hessian recurrence

Pair the response holes with the bridges as follows:

```text
05 <-> 14:11
15 <-> 04:11
24 <-> 35:22
34 <-> 25:22.                                            (8)
```

For each pair `(e,f)`, every word of `Delta F_e` contains the indicated
cell on `f`.  Division by that cell is therefore coefficientwise exact.
Set

\[
 \Delta G_{e,f}=\Delta G_{f,e}
    =(h-1)\,\Delta F_e/q_f,
 \qquad G=G^0+\Delta G.                                  \tag{9}
\]

The response holes themselves carry no `q` cell.  Consequently the
symmetric correction in (9) contributes to the recurrence for `e` through
the single bridge `f`, but contributes nothing to the recurrence for `f`.
All other recurrences remain the genuine ones.  This proves the second
identity in (1) for every physical edge, not merely for the four response
contractions.

This construction is formulaic in `h`; the checker audits it exactly for
`h=3,...,8` as representative instances.

## The next obstruction

Let `H^0` be the genuine third-cofactor family of `q`.  It obeys

\[
 \sum_gq_gH^0_{e,f,g}=(h-2)G^0_{e,f}.                   \tag{10}
\]

Against this genuine next layer, the corrected packet has residual

\[
 (h-2)G_{e,f}-\sum_gq_gH^0_{e,f,g}
                    =(h-2)\Delta G_{e,f}\ne0            \tag{11}
\]

on exactly

```text
05|14, 15|04, 24|35, 34|25.                             (12)
```

Equation (11) is the earliest certified failure of this sharpened guard.
It does not assert that no freely corrected formal `H` could solve (2).
Rather, it identifies the next load-bearing source datum: the third
cofactors must themselves come from the same `q`, or their recurrence must
be integrated into a source-preserving modification.

## Exact theorem boundary

What is proved uniformly:

1. the earlier `9b26452` response circuit can be extended through the full
   top Euler and symmetric first-cofactor Euler equations;
2. those two recurrence layers alone do not imply square-zero response
   rows;
3. for the explicit actual `q`, requiring the second cofactors to be
   genuine excludes the formal correction; and
4. the first remaining tower equation is (2), with the four exact residuals
   in (11)-(12).

What is not proved is a general Hessian-to-cap theorem, a source-preserving
descent, or the emptiness of the one-bad packet.  A theorem-completing next
lemma must use genuine common-`q` provenance beyond the free recurrence
(1): it must turn (2) and its higher common-cofactor tower into either a
square-zero cap or an active clean descent.  No finite support search or
`N=8` face enumeration enters this result.

## Reproduction

```bash
.venv/bin/python computations/verify_uniform_one_bad_second_cofactor_tower_gate.py
.venv/bin/python -O computations/verify_uniform_one_bad_second_cofactor_tower_gate.py
python3.14 computations/verify_uniform_one_bad_second_cofactor_tower_gate.py
python3.14 -O computations/verify_uniform_one_bad_second_cofactor_tower_gate.py
```
