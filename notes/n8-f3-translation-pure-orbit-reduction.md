# The ordinary translation-invariant F3 slice has four pure branches

This note closes the pure-diagonal branch enumeration for the ordinary
translation-invariant `n=8` search over `F3`.  It is only a finite-field
symmetry slice.  In particular, it neither proves the unrestricted complex
problem nor permits an `F3` solution to be read as a characteristic-zero
solution.

## Scalar normalization

Write the vertices as `F2^3` and let the edge matrix at `{u,v}` depend only
on the nonzero difference `d=u xor v`.  On a pure colour, its seven diagonal
entries form a row

\[
 b=(b_d)_{d\ne0}\in F_3^7.
\]

Direct enumeration of all `3^7=2187` rows gives exactly 882 whose scalar
translation-invariant hafnian is one.  Under `GL(3,2)` these form exactly the
18 orbits listed as `PURE_ORBIT_REPS` in the production search.  Their orbit
sizes are

```text
7 7 21 42 21 28 28 84 84 84 84 28 28 42 84 84 84 42
```

and sum to 882.  Thus branching on those 18 rows is exhaustive.

## Coefficient-preserving gauge

For `epsilon in F2`, a character `h in F2^3`, and `M in GL(3,2)`, define

\[
 (T_{\epsilon,h,M}B)_d
   =(-1)^{\epsilon+h\mathbin\cdot Md}B_{Md}.             \tag{1}
\]

The linear map merely relabels the eight vertices.  The global sign occurs
four times in every perfect matching.  The character part contributes

\[
 \prod_{\{u,v\}\in P}(-1)^{h\cdot M(u+v)}
 =\prod_{u\in F_2^3}(-1)^{h\cdot Mu}=1                 \tag{2}
\]

to every perfect-matching monomial.  Hence (1) preserves every coefficient,
not just its zero/nonzero status, and maps the full 42-entry search instance
bijectively to itself.

The 18 `GL(3,2)` branches collapse under (1) into four classes:

```text
{0,1}
{2,3,4}
{5,6,7,8,9,10,11,12}
{13,14,15,16,17}
```

Exact CaDiCaL runs had already returned UNSAT for representatives 0, 2, 5,
and 13 (as well as several redundant representatives).  One representative
therefore lies in every gauge class, so all 18 pure branches are UNSAT.  In
particular, the formerly unrun branches

```text
3 4 6 7 8 9 10 11 12 17
```

require no additional SAT calls.

For transparency, the following table gives explicit witnesses from every
formerly unrun branch to its solved class representative.  Integers encode
three-bit vectors.  `M=id` means the identity; otherwise the tuple lists
`(M1,...,M7)`.

| source | target | epsilon | h | M |
|---:|---:|---:|---:|---|
| 3 | 2 | 0 | 1 | id |
| 4 | 2 | 0 | 2 | id |
| 6 | 5 | 0 | 7 | id |
| 7 | 5 | 1 | 1 | id |
| 8 | 5 | 1 | 6 | id |
| 9 | 5 | 0 | 3 | id |
| 10 | 5 | 0 | 4 | id |
| 11 | 5 | 1 | 7 | id |
| 12 | 5 | 1 | 0 | id |
| 17 | 13 | 0 | 4 | `(1,4,5,6,7,2,3)` |

## Exact audit

Run the solver-free exhaustive checker with

```sh
.venv/bin/python computations/verify_f3_translation_pure_orbits.py
```

It enumerates all scalar rows, reconstructs the 18 `GL(3,2)` orbits,
checks all 168 linear maps, checks the gauge factor on all 105 matchings,
reconstructs the four augmented gauge classes, and verifies an explicit map
from each representative to its class base.  Its terminal line is

```text
PASS scalar_solutions=882 gl_orbits=18 gauge_classes=4 matching_gauge_checks=282240 residual_branches=0
```

To rerun the four production UNSAT instances rather than reuse their prior
solver results, append `--solve-bases`.  Individual branches can be checked
with `--solve-orbit I`; a returned SAT model is independently tested against
all `3^8` colourings before the checker reports it.
