# Endpoint polarization constructs the full linear cap evaluation

## Result

The rank-one result for the word `01211222` is not a rank-one limitation of
the full physical source grammar.  It is the expected matrix-coefficient
restriction of one word.  Keep

```text
response word          11110000
internal cap word      012112
physical cap pair      67
direct-free pair       36
```

and vary the ordered endpoint colours through all
$a,b\in\{0,1,2\}$:

\[
                         c_{ab}=012112ab.              \tag{1}
\]

For each pair, apply the four fixed internal roots and, when needed, the
roots $0\to a$ at site 6 and $0\to b$ at site 7.  On every perfect
matching monomial this sends

\[
 M_{11110000}\longmapsto M_{012112ab}                 \tag{2}
\]

with the same matching and coefficient one.  The checker verifies all 945
maps on the 105 complete matchings and all 810 maps on the 90 direct-free
parents.  The number of changed sites is 4, 5, or 6 with coordinate
histogram `(1,4,4)`.

The divided-root rule extends (2) over the complete marked collision
resolution.  Across the nine endpoint coordinates the audit checks

```text
parent-to-trigger squares       4,860
marked P3+K2 deletion faces     9,720
remote cofactor squares         1,755
q23 squares per coordinate          15
q45 squares per coordinate          12
```

Every trigger commutator is zero and every coefficient is one.  Thus the
other eight endpoint coordinates need no new collision generator.  They
are the endpoint-colour polarizations of the already constructed divided
root natural transformation.

The direct sum of (2) has rank nine and is exactly the linear evaluation
natural in a supplied physical covector

\[
                         K=\sum_{a,b}K_{ab}E_{ab}.     \tag{3}
\]

## Common support and the grading caveat

The nine coordinate maps have the same physical pair, direct-free pair,
matching parent, missing-site/reinsertion mark, repeated `P3+K2` type, and
`q23/q45` operation pattern.  Endpoint recolouring changes only cells
incident to sites 6 and 7; the internal matching tail is literally common.
For crossed endpoint matchings the endpoint edge entries vary with $(a,b)$,
as they must in the physical formula for $R(K)$, while their graph support
and residual word do not.

There is therefore no common-tail or common-support obstruction to the
nine-dimensional physical evaluation.

There is an important exact grading qualification.  The coordinates live
in the nine distinct word/colour-fine summands (1).  They assemble in the
total physical word family, where a covector is supposed to mix endpoint
colours.  They do **not** become nine coordinates inside the single fixed
Gamma word `01211222`.  A terminal restricted to that one word still sees
only $K_{22}$; forgetting the other eight word grades into it would be a
new non-conservative operation.  This distinction leaves the single-Gamma
Fredholm lane unchanged while enlarging the constructive physical lane.

## The cyclic diagonal completion

The three diagonal members of (1) now give the formal completion

\[
                  K=\lambda_0E_{00}+\lambda_1E_{11}
                       +\lambda_2E_{22}.               \tag{4}
\]

The activity conditions are exactly

\[
 \lambda_0\lambda_1\lambda_2\ne0,
 \qquad
 s(K)=\sum_c\lambda_c A_{67}[cc]\ne0.                 \tag{5}
\]

The linear marked comparison supplies the three coordinate evaluations; it
does not force either open condition in (5).  In particular, choosing
$\lambda_0=\lambda_1=\lambda_2=1$ gives the identity cap $I$, whose
activity is $\operatorname{tr}A_{67}\ne0$.

The more serious cross-colour condition is cleanliness.  At $h=3$, write

\[
 s(K)=\sum_i\lambda_i s_i,
 \qquad r(K)=\sum_i\lambda_i r_i.
\]

Then

\[
                   6{\cal E}(K)=3s(K)r(K)^2x+r(K)^3.  \tag{6}
\]

The checker expands (6) exactly.  It has ten cubic monomials in the three
$\lambda_i$: three pure cubes, six ordered terms
$\lambda_i^2\lambda_j$, and one
$\lambda_0\lambda_1\lambda_2$.  Coordinatewise cleanliness controls only
the three pure cubes.  For $i\ne j$, the first mixed coefficient is

\[
 [\lambda_i^2\lambda_j]\bigl(6{\cal E}\bigr)
 =3s_jr_i^2x+6s_ir_ir_jx+3r_i^2r_j,                  \tag{7}
\]

and the all-colour coefficient is

\[
 [\lambda_0\lambda_1\lambda_2]\bigl(6{\cal E}\bigr)
 =6\left(s_0r_1r_2+s_1r_0r_2+s_2r_0r_1\right)x
   +6r_0r_1r_2.                                      \tag{8}
\]

Equations (7)--(8), six plus one, are the first exact cross-colour
conditions.  They are nonlinear and are not consequences of the nine
termwise word/collision maps.  For the identity completion they combine to
the single physical condition

\[
                         {\cal E}_{6,7}(I)=0.          \tag{9}
\]

Together with $\operatorname{tr}A_{67}\ne0$, (9) is the known identity-cap
clean bridge, not a formal consequence of endpoint polarization.

## Constructive consequence

The source grammar now supplies the full **evaluation** of an arbitrary
chosen $K$ at the marked-derived level, with the relevant P2 and cofactor
naturality.  It still does not supply a **selection theorem** for $K$.
The shortest remaining constructive statement is therefore:

> On an actual normalized source, choose coefficients $K_{ab}$, common
> across the endpoint-polarized word family, such that
> $s(K)\kappa_0(K)\kappa_1(K)\kappa_2(K)\ne0$ and
> ${\cal E}_{6,7}(K)=0$.

If such a $K$ is produced and checked directly in the physical cap, the
constructive clean descent does not require a quasi-isomorphism to underived
`r0`, an absolute Eq filler, or a fixed-Gamma essential-surjectivity theorem.
Those remain relevant to the terminal lane, not to the physical evaluation.

## Verification and scope

Run:

```text
python3 computations/verify_h3_endpoint_polarized_nine_coordinate_cap_evaluation_gate.py --mode structural
python3 -O computations/verify_h3_endpoint_polarized_nine_coordinate_cap_evaluation_gate.py --mode full
python3 -I -S computations/verify_h3_endpoint_polarized_nine_coordinate_cap_evaluation_gate.py --mode exhaustive
```

This constructs evaluation natural in a supplied $K$; it does not select
$K$, force activity, or prove cleanliness.

Frozen ledger SHA-256:

```text
2aa36b361952f824c0951fd3c4a0e916ecea91ac91b0ba8e9e00cfd8c7b32750
```
