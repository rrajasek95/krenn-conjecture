# The dependent `q^[3]` branches reduce to palette descent or one non-pure zero-top jet

## Result

Retain the literal six-residual-site equations

\[
 a_{ij}q^{[3]}+p_i s_jq^{[2]}=\delta_{ij}X_i,
 \qquad 0\leq i,j\leq2,                              \tag{1}
\]

and a fixed off-diagonal selected pair `(a,b)`.  Put

\[
 \alpha=a_{ab}\ne0,\qquad \tau=\operatorname {tr}a,
 \qquad K_*=\tau E_{ab}-\alpha I,                    \tag{2}
\]

and assume the usual scalar-zero/rootless conditions

\[
 \langle K_*,a\rangle=0,
 \qquad \det K_*=(-\alpha)^3\ne0,
 \qquad r(K_*)^{[3]}\ne0.                            \tag{3}
\]

The two degeneracies left outside the independent-`q^[3]` recovery theorem
have the following exact classification.

1. If
   \[
       0\ne q^{[3]}=\lambda _0X_0+\lambda _1X_1+
                    \lambda _2X_2,                   \tag{4}
   \]
   then its nonzero support is intrinsic and no quotient or generic-rank
   chart is needed.  Support one is a unary six-site source, support two is
   a binary six-site source, and support three is impossible by the proved
   arbitrary-complex six-site theorem.  Thus these branches route exactly
   to smaller-palette descent or the terminal six-site contradiction.
2. If `q^[3]=0`, the pure-lift part of `q^[2]` is impossible by the uniform
   private-pair common-power theorem.  The first branch not covered by that
   theorem is therefore precisely
   \[
   \boxed{
   \begin{gathered}
       q^{[3]}=0,\qquad q^{[2]}\notin
       \operatorname {span}\{E_c(P):c=0,1,2,\ |P|=2\},\\
       p_i s_jq^{[2]}=\delta_{ij}X_i,\\
       \det K_*\ne0,\qquad r(K_*)^{[3]}\ne0.
   \end{gathered}}                                    \tag{5}
   \]
   This is a non-pure four-site common-power jet.  It is the smallest
   literal boundary, not a constructed source and not an ordinary six-site
   target.

The exact checker is
[`verify_h3_degenerate_q3_fullnine_scalarzero_routing.py`](../computations/verify_h3_degenerate_q3_fullnine_scalarzero_routing.py).

## 1. Unquotiented full-nine slices

Write `Q=q^[3]` and suppose first that `Q` lies in the labelled target
space as in (4), allowing all `lambda_c` to vanish.  Taking the coefficient
of `X_c` in (1) gives the literal cross-slice matrix

\[
             B_c=E_{cc}-\lambda_ca.                  \tag{6}
\]

Equation (6) is before quotienting by `Q`.  In particular it remains valid
when the four vectors `Q,X_0,X_1,X_2` are dependent, and it assumes neither
the rank-one quotient criterion nor
`rank(Q,X_0,X_1,X_2)=4`.  Adding `lambda_c a` back to `B_c` restores
`E_cc` coefficientwise.  The direct block is part of the physical source
datum even when it cannot be recovered from a quotient presentation.

Contracting (1) by `K_*` gives

\[
 \langle K_*,a\rangle q^{[3]}
       +r(K_*)q^{[2]}=\sum_i(K_*)_{ii}X_i.
\]

The first term is zero and every diagonal entry of `K_*` is `-alpha`, so

\[
                 \boxed{r(K_*)q^{[2]}=-\alpha\Delta_{6,3}.} \tag{7}
\]

This identity holds in all four support cases, including `q^[3]=0`.
Rootlessness says that the response in (7) has a nonzero third matching
power; it does not turn the polarized identity (7) into an ordinary
six-site hafnian value.  This agrees with the pinned scalar-zero
nonreduction theorem.

## 2. Unary, binary, and ternary support

If exactly one `lambda_c` is nonzero, (4) is a literal unary residual
matching source.  If exactly two are nonzero, it is binary.  One invertible
local diagonal change normalizes their nonzero amplitudes, so these are
genuine smaller-palette objects rather than failures of coefficient
normalization.  They do not contradict the ternary six-site theorem by
themselves.

If all three coefficients are nonzero, apply at one residual site the
diagonal map

\[
       e_c\longmapsto\lambda_c^{-1}e_c.               \tag{8}
\]

It sends (4) to `Delta_(6,3)` and merely replaces the incident aggregate
edge matrices by other arbitrary complex matrices.  This contradicts
[`six-site-arbitrary-complex-obstruction.md`](../proofs/six-site-arbitrary-complex-obstruction.md).
Using sixth roots at all six sites gives the equivalent symmetric
normalization.

The exact kernel trichotomy is also visible without a generic chart.  For
any physical response-product relation

\[
                 r(M)=\sum_{ij}M_{ij}p_is_j=0,         \tag{9}
\]

contracting (1) gives

\[
      \sigma(M)q^{[3]}=\sum_iM_{ii}X_i,
      \qquad \sigma(M)=\sum_{ij}M_{ij}a_{ij}.          \tag{10}
\]

Consequently

\[
                       M_{cc}=\sigma(M)\lambda_c.      \tag{11}
\]

Any failure of (11) is a literal pure-target unit.  If `sigma(M)=0`, then
`diag(M)=0` and the relation is a dark boundary.  If `sigma(M)` is nonzero,
support one or two again gives unary/binary descent; support three makes

\[
                 \sigma(M)M_{00}M_{11}M_{22}\ne0,
\]

so `M` is an active clean cap (and its top is independently forbidden by
the six-site theorem).  These kernel exits are conditional extra exits;
the full-rank six-star branch need not contain an ordinary product kernel.

## 3. What is special about zero top

For `q^[3]=0`, equations (1) reduce to

\[
                         p_i s_jq^{[2]}=\delta_{ij}X_i. \tag{12}
\]

The direct matrix has disappeared from (12).  Equation (10) forces
`diag(M)=0` for every response kernel, but it does not force `sigma(M)=0`.
Thus such a kernel is either fully dark (`sigma=0`) or direct-bright but
target-dark (`sigma!=0`); neither is active because all three target
diagonals vanish.  Scalar-zero and rootlessness do not repair this loss:
they retain (7), but impose no purity condition on `q^[2]`.

There is, however, a complete theorem on the pure-lift subspace

\[
 {cal P}=\operatorname {span}\{E_c(P):0\le c\le2,
                                      P\in\tbinom{[6]}2\}.       \tag{13}
\]

If `q^[2]` belongs to (13), the nine equations (12) force a private missing
pair for every colour.  The private-pair degeneration then contradicts
`q^[3]=0`.  This is exactly the uniform theorem in
[`uniform-pure-lift-private-edge-degeneration.md`](uniform-pure-lift-private-edge-degeneration.md),
and it allows arbitrary complex coefficients and arbitrary endpoint blocks
of `q`.

What it does not prove is that the nine rows place an arbitrary `q^[2]` in
`P`.  Mixed four-site words can occur in `q^[2]`, and the filtration in the
same theorem leaves their lower jets.  Hence (5), rather than an empty
zero-top branch, is the exact current conclusion.

## 4. Sharp three-term response-shadow guard

The checker freezes why no theorem using only the nine response products
can close the zero-top branch.  On sites `0,...,5`, take

```text
P0=01,  P1=23,  P2=45,
p_i=e_i at the first site of P_i,
s_i=e_i at the second site of P_i,
F=E_0(P0)+E_1(P1)+E_2(P2).
```

Then `P+S` has rank six and exact square-zero multiplication gives

\[
                         p_i s_jF=\delta_{ij}X_i       \tag{14}
\]

for all nine ordered rows.  Choose the direct block

\[
                    a_{01}=a_{10}=-1,
                    \qquad a_{ij}=0\text{ otherwise}. \tag{15}
\]

For the selected pair `(0,1)`, one has `alpha=-1`, `tau=0`, and

\[
             K_*=I,qquad \langle K_*,a\rangle=0,
             \qquad r(K_*)^{[3]}=e_0e_0e_1e_1e_2e_2\ne0. \tag{16}
\]

Thus rank six, scalar zero, rootlessness, and all nine response products
coexist exactly.  But the three terms of `F` have distinct private missing
pairs, so the pure-lift theorem proves that there is no physical `q` with

\[
                         q^{[2]}=F,\qquad q^{[3]}=0.    \tag{17}
\]

This is a response-shadow guard, not a counterexample to (1).  It pins the
load-bearing missing statement exactly: a positive closure must control the
non-pure four-site part of the common power, rather than extract more matrix
rank from (12).

## Scope and reproduction

The classification assumes literal target labels and a fixed selected
off-diagonal pair.  It uses no target `GL_3`, no quotient by `q^[3]`, and no
generic rank assumption on `(q^[3],X_0,X_1,X_2)`.  It does not claim that
the unary or binary residual sources are themselves contradictions, and it
does not promote the formal guard (14)--(16) to a common-power source.

```text
python3 computations/verify_h3_degenerate_q3_fullnine_scalarzero_routing.py --mode structural
python3 -O computations/verify_h3_degenerate_q3_fullnine_scalarzero_routing.py --mode full
python3 -I -S computations/verify_h3_degenerate_q3_fullnine_scalarzero_routing.py --mode exhaustive
```

All modes return the same frozen ledger digest.
