# The canonical C6 has one four-tail spoke-to-hole separator

## Result

Continue the canonical first-transgression boundary of `05b22c1` at

```text
z=012111.
```

After the seven offanchor unary competitors are routed, the six
anchor-contained matchings are

```text
01|24|35,
02|13|45, 05|13|24,
02|14|35, 05|14|23,
02|15|34.
```

All six use one physical edge `1-r`, where `r=0,3,4,5`.  Removing that
edge groups their remaining q products into four complete residual classes
with term profile

```text
r=0: 1,   r=3: 2,   r=4: 2,   r=5: 1.                (1)
```

Call those classes `T_r`.  In the no-offanchor associated packet, the
literal unary row and the two response slices through the already selected
port `s1@1:1` are

\[
 H=\sum_r q_{1r}^{1z_r}T_r,
 \qquad
 R_i=\sum_r p_{i,r}^{z_r}T_r\quad(i=1,2).             \tag{2}
\]

Thus the canonical `C6` word-change gate is one common-tail affine/Fitting
module, not six unrelated matching cases.

Checker: `computations/verify_h3_c6_z_spoke_hole_koszul_boundary.py`.

## Literal tail classes

With decorations read from `z`, the four entries of (2) are

\[
\begin{aligned}
T_0={}&q_{24}^{21}q_{35}^{11},\\
T_3={}&q_{02}^{02}q_{45}^{11}+q_{05}^{01}q_{24}^{21},\\
T_4={}&q_{02}^{02}q_{35}^{11}+q_{05}^{01}q_{23}^{21},\\
T_5={}&q_{02}^{02}q_{34}^{11}.
\end{aligned}                                         \tag{3}
\]

Multiplying by `q01:01,q13:11,q14:11,q15:11` respectively expands `H`
to exactly the six anchor-contained unary monomials.  For each fixed
partner there are three possible four-site tails.  After the old `M,N`
terms are removed, every unused tail contains an offdiagonal physical edge
outside the old four-base union.  These account for five of the seven
already-routed unary competitors; the two remaining routed terms have
partner `r=2`.  Hence (1)--(3) retain every term of the genuine residual.

## Exact endpoint labels

Every one of the six terms can enter `G11` or `G21` through the same
selected endpoint component

```text
s1@1:1.
```

The opposite endpoint must be one of

```text
p_i@0:0, p_i@3:1, p_i@4:1, p_i@5:1,    i=1,2.        (4)
```

These are precisely the word-changed endpoint columns missing from the
fixed minimum block.  Its selected entries are `p1@0:1` and `p2@3:2`, so
neither supplies (4).  This is stronger than saying that the four original
response holes are blind to `z`: it lists the complete selected-`s1`
attachment module capable of seeing all six terms.

Terms using another `s` hole are not silently discarded.  Their existence
is exactly the additional endpoint/Hall branch outside the present
selected-port slice.

## The source-valid Koszul identity

For each `i=1,2` and each pivot `r`, (2) gives the literal identity

\[
 q_rR_i-p_{i,r}H
   =\sum_{s\ne r}(q_rp_{i,s}-p_{i,r}q_s)T_s,          \tag{5}
\]

where `q_r=q1r:(1,z_r)` and `p_{i,r}=p_i@r:z_r`.
The checker expands all eight identities as ordinary polynomials.  The
minors

\[
 \Delta^i_{rs}=q_rp_{i,s}-p_{i,r}q_s                 \tag{6}

are therefore the first genuine determinant/Hessian candidates.  A
nonzero minor with a nonzero literal tail has the typing required by the
shared affine carrier theorem, but still must be isolated from the other
summands of (5).  Vanishing minors make the endpoint and unary coefficient
vectors proportional on this four-tail quotient, but not automatically as
complete tensor columns.  Source exhaustivity is required before applying
the exact one-sided modification.  Formula (5) itself does not assert
either landing because the complete `T_s` may cancel and other
endpoint-hole terms may occur.

## Primitive separator

Set every component in (4) to zero while retaining the selected `s1`
port and the six unary monomials.  Both response slices `R_1,R_2` then
vanish identically, while `H` remains a sum of six distinct source
monomials.  On the associated row-label module, the functional

```text
lambda(H)=1,   lambda(R1)=lambda(R2)=0                (7)
```

is primitive.  It is the earliest exact augmented separator: unary top
and the fixed selected response block alone cannot manufacture a
spoke-to-hole attachment.

This is not a full-source counterexample.  A positive proof can defeat
(7) by forcing a component in (4), a response mate using another `s` hole,
or a cross-word/second-cofactor boundary.  Conversely, one of those is
genuinely necessary; separate line-hitting sites do not supply it.

## Consequence and scope

The six-mate problem is reduced to the following exact lemma.

> In a full one-bad packet, the four-tail module (2) either acquires a
> word-changed endpoint component (4), another-hole Hall mate, or a
> cross-word/Hessian boundary killing the primitive class (7).  Once a
> component exists, (5) gives the source-valid Fitting-minor relation; an
> isolation/source-exhaustivity step must then produce a carrier or a
> proportional complete-column reduction.

The checker proves the decomposition, routing counts, endpoint typing,
Koszul identities, and separator.  It does not prove that the full packet
must supply the missing attachment.

## Verification

```text
python3 computations/verify_h3_c6_z_spoke_hole_koszul_boundary.py
python3 -O computations/verify_h3_c6_z_spoke_hole_koszul_boundary.py
python3 -I -S computations/verify_h3_c6_z_spoke_hole_koszul_boundary.py
```

Frozen ledger SHA-256:

```text
6d65dad8ef8a5c4b92ffac320d87e22e3222e9f0d318602f490dba17b7618638
```
