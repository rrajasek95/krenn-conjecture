# The spoke rank-two orbit is not unique; the next minimal orbit also exits

## Literal block invariant

Fix the occupied spokes `x=(x1,x2,x3)`.  A target-zero homogeneous
word/head block restricts to

\[
                     F_B(x)=c_B+r_{B1}x_1+r_{B2}x_2+r_{B3}x_3=0.
\]

At the chosen source put `z_Bi=r_Bi*x_i`.  The literal block carries the
projective invariant

\[
             [c_B:z_{B1}:z_{B2}:z_{B3}],\qquad
             c_B+z_{B1}+z_{B2}+z_{B3}=0.             \tag{1}
\]

The allowed grading-preserving operations act as follows.

```text
block rescaling             projectivizes (1);
nonzero source torus change leaves each product r_Bi*x_i unchanged;
residual site relabelling   permutes the three z coordinates;
word/head relabelling       permutes whole blocks.
```

Adding two different word/head rows would change (1), but is not a physical
source/chart operation: it destroys literal word and fine-grade typing.
Thus arbitrary rank-two block packets form configurations of projective
points in the plane `c+sum(z)=0`, modulo the finite spoke permutation group.
There are continuous moduli; no single finite normal form exists.

The two blocks of `a8ef1a4` have profiles

```text
[0:1:-1:0], [0:0:1:-1]
(constant absent, spoke support two).
```

Checker:
[verify_h3_active_coloop_spoke_inequivalent_constant_block_guard_exit.py](../computations/verify_h3_active_coloop_spoke_inequivalent_constant_block_guard_exit.py).

## A smallest inequivalent literal guard

Put

```text
q01[00]=1
x=(q23[00],q24[00],q25[00])=(1,1,-1)
y=(q45[00],q35[00],q34[00])=(-1,1,-1)
q12[00]=q13[00]=1

p1[0,0]=1,
s2[5,1]=s2[4,1]=1,
```

and set the other displayed cells to zero.  Then

\[
                        x\cdot y=-1+1+1=1,
\]

and all three nonzero pure-zero target matchings retain the coloop `01`.
The complete `729`-word/four-response-head scan has exactly two supported
target-zero rows:

\[
\begin{aligned}
 R_{12}[000001]
   &=p_0s_5(q_{12}q_{34}+q_{13}q_{24})=-1+1=0,\\
 R_{12}[000010]
   &=p_0s_4(q_{12}q_{35}+q_{13}q_{25})= 1-1=0.
\end{aligned}                                       \tag{2}
\]

Each block contains one constant occurrence and one spoke occurrence.  Its
spoke restrictions are `e2` and `e3`, so together with
`y=(-1,1,-1)` they have rank three and quotient rank two.  Neither row is
private.  Their invariants are

```text
[-1:0:1:0], [1:0:0:-1]
(constant present, spoke support one),
```

which cannot lie in the `a8ef1a4` orbit.

This guard is size-minimal.  Rank two across scalar blocks needs at least
two blocks.  A one-occurrence block is already private, so a nonprivate
guard needs at least two occurrences in each block: four total.  Both the
old and new guards attain the lower bound, in inequivalent orbits.

All endpoint and `q` cells in (2) are diagonal.  The endpoint holes `05`
and `04` lie in the same closed star at `0`, so neither an offdiagonal nor
outside-shore exit is hidden in the construction.

## First complete-row exit

A complete ternary target supplies nonzero pure-one and pure-two target
terms.  Append one of the fifteen unit perfect matchings in each colour.
The checker exhausts all

```text
15*15=225
```

choices and scans every mixed unary word.  It finds `2286` private nonzero
unary rows.  More importantly, every completed packet has an exit-only
private row.  The number of such witnesses per packet is

| witnesses | packets |
|---:|---:|
| 2 | 2 |
| 3 | 32 |
| 4 | 84 |
| 5 | 76 |
| 6 | 22 |
| 8 | 6 |
| 10 | 3 |

There are `1026` exit-only witnesses in total.  Their mate profiles are
exactly

```text
486 rows: all 14 alternates contain an offdiagonal q edge;
540 rows: 12 alternates are offdiagonal and the two diagonal alternates
          create a nonzero pure-zero matching omitting 01.
```

Thus each chosen witness forces either the physical offdiagonal active-fan
alternative or destruction of the named pure-zero coloop.  No first-mate
recurrence survives for this minimal orbit.

The two exceptional pure-one/pure-two matching pairs that have no private
`2+2+2` rainbow row are included: each has the private rows `001100` and
`002200`; their two diagonal mates are precisely coloop-destroying.

## Remaining general scope

This disproves reduction of arbitrary rank-two blocks to the sole `a8ef`
normal form, while closing the smallest inequivalent orbit.  It does not
reduce a larger packet with additional occurrences in the same word:
additional terms can remove the displayed privacy.

The uniform residual theorem is therefore a projective-block descent:

> From an arbitrary rank-two configuration of points (1), either delete an
> occurrence while preserving the protected fibre, expose a private row or
> typed offdiagonal/outside/terminal exit, or reduce the number of
> occurrences until one of the two four-occurrence minimal guards is
> reached.

The obstruction is no longer a finite recurrence inside either minimal
guard; it is the support-lowering step for larger homogeneous blocks.

Run normally, optimized, and isolated/no-site.  The frozen digest is stored
in the checker.
