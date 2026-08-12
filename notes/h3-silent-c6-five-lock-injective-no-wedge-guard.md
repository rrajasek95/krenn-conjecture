# The silent C6 zero fibres admit an injective, crossed-dark five-lock

## Result

The chordless diagonal C6 left by `b80b064` is **not** forced to have a
same-star kernel or a complementary crossed wedge by its unary row and four
displayed response-zero fibres alone.

There is an exact rational common-$q$ specialization with

```text
q13 = q04 = PS = 0,
q^[3] = X0,
G11 = G12 = G21 = G22 = 0
```

in which all five old bases $A,B,K,L,R$, and both diagonal augmented C6
terms $O_{11},O_{22}$, are nonzero. Its four natural same-star attachment
windows have lock rank two and kernel zero. Both crossed lock coordinates
vanish identically in every window.

Thus the exact surviving branch is

\[
\boxed{\text{injective unary/diagonal lock, with no crossed wedge}.} \tag{1}
\]

The first additional input capable of closing it is the bright $X_1,X_2$
diagonal response rows or the endpoint-star completion that realizes them.
Those rows are not contained in the four zero fibres classified by
`b80b064`.

Checker:
`computations/verify_h3_silent_c6_five_lock_injective_no_wedge_guard.py`.

## Rational common-source slice

All nonzero cells are colour `00`. Take

```text
q01=-2  q02= 1  q03= 1  q05= 1
q12= 1  q14=-3  q15= 1
q23=-1  q24=-1  q25= 1
q34= 2  q35= 1  q45= 1.
```

The missing physical edge tables are exactly `q04,q13`. Use the literal
endpoint rows

```text
p1=0:1,   s1=1:1,   p2=3:2,   s2=4:2.
```

The five selected pure-zero matching products are

```text
A=2, B=2, K=2, L=2, R=-3,
```

and direct matching expansion gives

\[
q^{[3]}=X_0.                                             \tag{2}
\]

The four response cofactors are

\[
\begin{aligned}
H_{01}&=q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34}=0,\\
H_{04}&=q_{12}q_{35}+q_{15}q_{23}=0,\\
H_{13}&=q_{02}q_{45}+q_{05}q_{24}=0,\\
H_{34}&=q_{01}q_{25}+q_{02}q_{15}+q_{05}q_{12}=0.
                                                               \tag{3}
\end{aligned}
\]

Therefore the complete literal response tensors in this colour slice vanish,
not just their selected monomials. Nevertheless

```text
O11 term = q25*q34 =  2,
O22 term = q01*q25 = -2,
```

so each displayed diagonal row contains the active C6 term and its
common-$q$ cancellation mates.

## Four exact same-star lock matrices

There are four ways to join an $R$ edge to a diagonal augmented-response
edge at one physical site:

```text
site 0: (q03,q01),       site 1: (q14,q01),
site 3: (q03,q34),       site 4: (q14,q34).
```

In each pair, every linear combination $d$ has $d^{[2]}=0$. Hence the five
finite differences are exactly

\[
dq^{[2]},\qquad p_i s_j d q\quad(i,j\in\{1,2\}),       \tag{4}
\]

with no higher correction.

For `q03` and `q14`, only the unary pure-zero coefficient is nonzero:

```text
q03 -> (-3,0,0,0,0),
q14 -> ( 1,0,0,0,0).
```

For `q01` and `q34`, only one diagonal response coefficient is nonzero:

```text
q01 -> (0,0,0,0,1) in G22[000220],
q34 -> (0,1,0,0,0) in G11[110000].
```

Feature order is `(top,G11,G12,G21,G22)`. Each two-column matrix is
diagonal with nonzero diagonal, hence injective. Moreover every corner edge
meets one selected hole of `G12` and one selected hole of `G21`. Therefore

\[
L_{12}=L_{21}=0                                         \tag{5}
\]

on all four windows, so the complementary crossed-incidence alternative of
the five-lock wedge theorem is also absent.

The checker additionally tests nontrivial rational combinations in every
window against the complete matching expansion of the unary and all four
response tensors. Equation (4) holds exactly.

## Consequence and scope

This is stronger than an abstract lock matrix: all columns come from one
literal common $q$, and (2)--(3) are exact source coefficients. It shows
that neither the chordless C6 topology nor the five frozen zero fibres can
force the desired kernel/wedge dichotomy.

It is deliberately **not** a full one-bad point. The bright response
requirements

\[
p_1s_1q^{[2]}=X_1,\qquad p_2s_2q^{[2]}=X_2             \tag{6}
\]

are absent. Adding the coloured source cells and endpoint-star components
needed for (6) may create a new lock dependence or a crossed carrier. That
is now the smallest load-bearing theorem:

> In the silent C6 chart, the two bright diagonal target rows must couple
> the unary-private $R$ column to one diagonal-private $O$ column, yielding
> a same-star kernel, a complementary crossed wedge, or an already-closed
> cap/unit branch.

No conclusion about a full GHZ packet is drawn from the guard.

## Verification

```text
python3 computations/verify_h3_silent_c6_five_lock_injective_no_wedge_guard.py
python3 -O computations/verify_h3_silent_c6_five_lock_injective_no_wedge_guard.py
python3 -I -S computations/verify_h3_silent_c6_five_lock_injective_no_wedge_guard.py
```

Frozen ledger SHA-256:

```text
cf1f90c7da2a5d3122e27d3b5a264e29df859372ef786d485bb423e12ea9c6ad
```
