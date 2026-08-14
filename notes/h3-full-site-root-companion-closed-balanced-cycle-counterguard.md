# Full-site/root covariance admits a closed balanced chart cycle

## Verdict

Literal site, port, operation, word and conjugated-root labels do **not** by
themselves force every closed companion cycle to contain an absolute
`DQ↔PS` switch or an active outside fan.  There is a smallest exact physical-
label counterguard: a four-object site-groupoid square on the fixed operation
set `{P,S,0,1}`.

Two such squares give the two required switch types

```text
A=Dq01  <->  B=p0s1,
A=Dq01  <->  C=p1s0.
```

The residual window `{2,3,4,5}` and each of its three matching tails remain
literal constants.  The local `E01` or `E02` root labels conjugate
path-independently around the square.  For a pure word, all port colours are
fixed.  Nevertheless a presentation-safe site comparison has boundary

\[
                       d\beta_e=x_{t(e)}-x_{s(e)}-u_e, \tag{1}
\]

not the absolute switch `x_t-x_s`.  The centered square detector extends to
the retained `u_e` and survives every edge in (1).

Taking both switch squares in each of the three pure colours gives six
disjoint labelled components and 24 complete rows.  The exact assignment

\[
             P_0=P_1=P_2=1,\qquad z_e=-\tfrac12      \tag{2}
\]

kills all 24 rows.  There is no singleton, odd holonomy or outside-tail
edge.  Thus the hoped-for global cycle theorem is false under covariance,
labels and normalization alone.  A positive theorem must use the next
physical boundary: an absolute `L01`/one-hole landing, or a mandatory
collision/PP face that exits the fixed operation four-set.

Exact checker:
[`verify_h3_full_site_root_companion_closed_balanced_cycle_counterguard.py`](../computations/verify_h3_full_site_root_companion_closed_balanced_cycle_counterguard.py).

## 1. Two literal site squares

Use physical site labels `0,1,2,3,4,5,P,S`.  Put

\[
 A=PS|01,qquad B=P0|S1,qquad C=P1|S0.                \tag{3}
\]

### The `A↔B` square

The disjoint transpositions

\[
                     \sigma_B=(S\ 0),\qquad
                     \tau_B=(P\ 1)                  \tag{4}
\]

commute.  On the four groupoid objects

```text
1, sigma_B, sigma_B*tau_B, tau_B
```

the physical core alternates

```text
A, B, A, B.
```

At each object, conjugate the root

\[
                 E_{01}:P0\mapsto PS,qquad
                        01\mapsto-S1.                 \tag{5}
\]

Applying either site transposition to the root signature at one endpoint
gives exactly the stored signature at the adjacent endpoint.  Since (4)
commutes, both routes to the opposite corner agree.

### The `A↔C` square

Similarly,

\[
                     \sigma_C=(P\ 0),\qquad
                     \tau_C=(S\ 1)                  \tag{6}
\]

commute, the core sequence is `A,C,A,C`, and the transported root is

\[
                 E_{02}:P1\mapsto PS,qquad
                        01\mapsto-S0.                 \tag{7}
\]

Every permutation in (4) and (6) is supported on `{P,S,0,1}`.  Therefore
all three tails

```text
23|45, 24|35, 25|34
```

are fixed term by term, and no transition edge touches an outside-tail
port.  The eight-letter pure words `00000000`, `11111111`, and `22222222`
are fixed by every transition.

These facts are stronger than an unlabelled `K2,2` picture: the checker
stores the endpoint roles, all four port sites, physical matching, root
source and target edges, word, and residual tail at every object.

## 2. Complete rows and pure normalization

For one square, label its four vertices cyclically by `v=0,1,2,3` and its
four internal transition companions by `z_e`.  In pure colour `c`, use the
complete rows

\[
                       F_v=P_c+\sum_{e\ni v}z_e.      \tag{8}
\]

Their unique relation is

\[
                     F_0-F_1+F_2-F_3=0.              \tag{9}

The coefficient of `P_c` in (9) is zero.  This is the exact centered charge
`(1,-1,1,-1)` and has holonomy `+1` around the four-cycle.

Use one copy of (8) for each pair

```text
colour c in {0,1,2}, switch family in {A<->B,A<->C}.
```

There are six components, 24 complete rows and 24 internal companions.  The
complete-row matrix has rank 18 and relation dimension six, with one copy
of (9) per component.  The point (2) annihilates every row.  Hence all three
pure normalizations coexist with both labelled switch families.

This is a physical-label refinement of the abstract global centered-`K2,2`
guard: the site and root actions do not destroy centeredness because every
transition merely moves it to another chart object.

## 3. Why a relative groupoid bar is not an absolute switch

For one component, use four object coordinates `x_v` and four carrier
coordinates `u_e`.  The four columns (1) are independent.  On the full six-
component model they have rank 24 in 48 coordinates, leaving `H0=24`.

Put `lambda=(1,-1,1,-1)` and define

\[
 \mu(x_v)=\lambda_v/4,
 \qquad
 \mu(u_e)=(\lambda_{t(e)}-\lambda_{s(e)})/4.          \tag{10}
\]

Then `mu(d beta_e)=0` for every edge, while

\[
                       \mu\!\left(\sum_v\lambda_vx_v\right)=1            \tag{11}
\]

on each component.  Thus the centered detector extends through every
presentation-safe site/root mapping cylinder.

If the carrier is dropped, the putative absolute column `x_t-x_s` has
`mu`-value `+1/2` or `-1/2`.  It is a genuine rank raiser.  Full-site
covariance proves that the two chart objects are isomorphic; it does not
supply this fixed-source rank raiser.

## 4. Minimality

Among connected simple companion graphs with minimum row degree two, flat
unsigned transport requires bipartiteness.  Centeredness requires equal
shore sizes.  Exhaustion through four vertices gives

```text
vertices    labelled candidates
2           0
3           0
4           3
```

The three four-vertex candidates are precisely the three labelled
four-cycles, one isomorphism type `C4=K2,2`.  Hence one four-object square is
the smallest face-complete single-switch guard.  Three monochromatic squares
are the minimum to display all pure targets; six display both required
switch families in all three colours.

## 5. The missing hypothesis exposed by the guard

The guard does not say that a recursively complete decorated-hafnian source
realizes these six abstract row blocks.  It says exactly which hoped-for
implication fails:

```text
full-site covariance
+ conjugated root flatness
+ literal operation/port/window labels
+ P0=P1=P2=1
    does not imply an absolute switch, odd unit, singleton, or outside fan.
```

The first stronger physical laws are already located by the pinned audits:

1. the fixed-source endpoint-chart cylinder has the proper scalar face
   `L01-u01`, rather than a raw chart fold; and
2. the hyperbolic root return needs an occurrence-split collision/PP
   cylinder before its squarefree endpoints become `A+B` and `A+C`.

Therefore the shortest positive global attack is not another action or
normalization invariant.  It is a recursive boundary theorem saying that
at least one retained `u_e` in every closed component acquires an absolute
same-word/fine/root/reinsertion landing, or that its first collision/PP debt
must touch an active site outside `{P,S,0,1}`.  Without that extra clause,
the four-object square above is the terminal counterguard.

## Verification

Run

```text
python3 computations/verify_h3_full_site_root_companion_closed_balanced_cycle_counterguard.py
python3 -O computations/verify_h3_full_site_root_companion_closed_balanced_cycle_counterguard.py
python3 -I -S computations/verify_h3_full_site_root_companion_closed_balanced_cycle_counterguard.py
```

The checker verifies both commuting physical site squares, every conjugated
root edge and pure word, all fixed tails, the exact 24-row normalized point,
the relative-bar rank and detector, and the minimal balanced-graph census.
