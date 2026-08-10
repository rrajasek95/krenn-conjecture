# The nine-cell response point cannot turn on pure `X2` before order 15

## Verdict

At the exact orbit-0 response point of `e3fb47f`, allow arbitrary formal
corrections in **all 135** endpoint-coloured source cells.  If an arc preserves
the four fixed-star response tensors and its six-site top tensor is a scalar
multiple of pure `X2`, then

\[
        \operatorname{ord}_t H_{012345}(q(t))_{222222}\geq 15. \tag{1}
\]

In particular, pure `X2` does not appear in the tangent or at the first
nonlinear order.  This is stronger than the diagonal-`22` specialization:
all tilted/off-diagonal source corrections are retained.

The exact checker is
`computations/verify_n8_one_bad_response_local_artin_jet.py`.

## The local equations

The base source is the nine-cell rational point

```text
01:01 =  1       01:10 =  1
02:00 =  1       03:11 =  1
04:00 =  1       05:11 =  1
13:11 =  1       14:00 =  1
34:10 = -1.
```

It satisfies

\[
H_{0124}=X_0,\quad H_{0135}=X_1,\quad
H_{0125}=H_{0134}=0,\quad H_{012345}=0.       \tag{2}
\]

For a prospective pure-top arc, every mixed top coefficient must vanish.
The checker therefore constructs the literal 324 response coefficient rows
and all 729 top coefficient readouts.  The pure row is not set equal to zero;
it has zero Hasse coefficients at the orders where it is used below, while
the 728 mixed rows are the necessary equations.  At the base point the
combined differential has

```text
rank:             125 of 135
kernel dimension:  10.
```

Every one of the fifteen source coordinates `q_ij(2,2)` is zero on this
ten-dimensional tangent kernel.  Thus even tilted tangent directions cannot
begin to build a pure-`222222` matching.

## Exact second fundamental form

Write the first tangent as

\[
                         q_1=\sum_{i=0}^9 a_i v_i.       \tag{3}
\]

The checker constructs the full symmetric Hasse square of the matching map,
not a numerical Hessian.  Modulo the rank-125 differential image, it has
exactly two nonzero compatibility classes:

\[
                         a_2a_9=0,\qquad a_5a_9=0.       \tag{4}
\]

They occur in the literal cross-response coefficients

```text
H_0125[2,0,0,1] and H_0125[2,1,0,1].
```

Hence the first nonlinear liftable cone is already reducible: it lies in
`a9=0` or in `a2=a5=0`.  This is the source-faithful second fundamental form
of this local packet.

## Artin recursion through source order four

Choose an exact unimodular `125 x 125` Jacobian minor and solve its implicit
equations order by order:

\[
q(t)=q_0+tq_1+t^2q_2+t^3q_3+t^4q_4+O(t^5).             \tag{5}
\]

At every order the arbitrary ten-dimensional kernel correction is retained;
no transverse slice or support restriction is imposed.  The result is

```text
number of nonzero q_ij(2,2) coordinates in q1: 0
number of nonzero q_ij(2,2) coordinates in q2: 0
number of nonzero q_ij(2,2) coordinates in q3: 0
number of nonzero q_ij(2,2) coordinates in q4: 0.
```

These are polynomial identities in all free Artin parameters, before imposing
the extra compatibility equations from the nonpivot rows.  They are therefore
necessary for every actual formal branch.

The pure top coefficient is

\[
 H_{012345}(q)_{222222}
   =\sum_{M\in\operatorname{PM}(6)}\prod_{ij\in M}q_{ij}(2,2). \tag{6}
\]

Each factor in every summand of (6) is `O(t^5)`, proving (1).

## Scope

This closes the tangent and first nonlinear possibilities at the exact
response component represented by `e3fb47f`, and advances the first possible
pure turn-on to order 15.  It does **not** prove all-order local exclusion:
the calculation does not show that the fifteen `22` cells vanish from order
five onward.  It also says nothing about another response component or a
global point of the unrestricted whole-packet ideal.

The next local question, if this component remains strategically relevant,
is structural: prove that the implicit equations preserve the `22=0` ideal,
or find the first nonzero `22` Artin coefficient at order at least five.
Blind global degree-seven elimination is unrelated to that question.

## Reproduction

```bash
.venv/bin/python computations/verify_n8_one_bad_response_local_artin_jet.py
.venv/bin/python -O computations/verify_n8_one_bad_response_local_artin_jet.py
```
