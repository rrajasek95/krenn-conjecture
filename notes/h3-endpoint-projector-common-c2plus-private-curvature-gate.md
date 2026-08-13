# The common endpoint target cone leaves a rank-two private curvature

## Result

For the centered marked occurrence let

\[
 v_0=(A+I)c_f,
 \quad v_1=(B-4I)v_0,
 \quad v_2=(B-2I)v_1.                                  \tag{1}
\]

The three endpoint factors have target normals in the exact ratios

\[
                       1:-{32\over7}:{108\over7}.       \tag{2}
\]

Thus one `B-4/C2+` target cone can cancel every target normal.  But if that
cone is merely rescaled by (2), its protected occurrence/path rows leave

\[
 C_2=v_1+{32\over7}v_0,
 \qquad
 C_3=v_2-{108\over7}v_0.                               \tag{3}
\]

These vectors have rank two.  Each is nonzero on all ninety occurrences,
on all 360 literal first-principal-parts rows, and on all 2880 rows after the
eight endpoint-path labels are retained.  Hence the target compression is
not a flat augmented splitting.

Checker:
[verify_h3_endpoint_projector_common_c2plus_private_curvature_gate.py](../computations/verify_h3_endpoint_projector_common_c2plus_private_curvature_gate.py).

## Exact supports and normalization

The denominator-cleared packets

\[
                       {7C_2\over90},\qquad {7C_3\over90} \tag{4}
\]

are primitive integral occurrence vectors.  Their value profiles are

```text
7 C2 / 90 : -2 on 63 occurrences, +5 on 24, +2 on 3
7 C3 / 90 : -23 on 24, -2 on 3, +2 on 3, +5 on 24, +12 on 36.
```

They have augmentation zero and central-Eq incidence zero.  The common
`C2+` correction makes their target row zero, so their nonzero rank is
entirely in the protected/private source quotient.

Applying the centered matching numerator does not kill them:

\[
                         (A+I)C_i=3C_i.                \tag{5}
\]

Thus the centered relation places both curvatures in the matching-flat
sector; it does not make them boundaries.

## The bare endpoint groupoid is flat

Every occurrence has eight endpoint paths.  Its sixty-four length-two paths
land at forty-five endpoints, with multiplicities

```text
32 endpoints reached once,
12 endpoints reached twice,
 1 endpoint reached eight times.
```

All paths with a common endpoint induce the same site permutation.  Therefore
the site-permutation local system has zero two-step holonomy.  The classes
in (3) are not curvature of the bare endpoint groupoid; they measure failure
of the chosen common target-normal splitting to be horizontal across the
three weighted factor stages.

## Triangle isotropy is the matching switch

Three endpoint moves can return the ordered endpoints while changing the
residual perfect matching.  For each of the two matching-adjacency neighbours
there are eight such triangles.  They induce two residual site flips, each
with multiplicity four, and both act on the occurrence tag as exactly the
same `A` matching switch.

On the symmetric two-edge response product the two flips agree.  On the two
occurrence-local `dq` directions they swap the labels.  If

\[
                           y=e_{left}-e_{right},
\]

then the residual flip `tau` satisfies `tau*y=-y`.  In the action-groupoid
bar complex,

\[
                    d[\tau|y]=\tau y-y=-2y,
 \qquad y=d[-\tfrac12[\tau|y]].                        \tag{6}
\]

Thus this antisymmetric isotropy is automatically contractible in
characteristic zero once a physical residual-flip action is admitted.
Equation (6) is not itself that physical action: a source-labelled section
must make `tau` act on the complete word/fine/repeated, `q`, anchor, cap,
ridge, and eta/sigma object.  Coefficient-level `c_f` naturality alone does
not adjoin the bar generator.

## The rank-two classes are one naturality obligation

Although (3) has rank two, the two packets are not new coefficient
generators.  Direct calculation gives

\[
 C_2=(B+\tfrac47)v_0,
 \qquad
 C_3=(B^2-6B-\tfrac{52}{7})v_0,                       \tag{7}
\]

and the recurrence

\[
 C_3=BC_2-{46\over7}C_2-{180\over49}v_0.             \tag{8}
\]

Consequently one genuinely `B`-natural source schema carrying the initial
`v0/B-4` data carries both higher curvatures automatically.  The coefficient
polynomial identities (7)--(8) do not prove that source naturality.  The
remaining theorem is:

> Extend the `B-4/AugP2/C2+` cell to a target-zero `B`-natural second-Hasse
> totalization on the complete physical source complex.  Its first two
> higher faces must be (3), with the residual matching-flip odd line filled
> by (6).

No new target cone and no independent coefficient generator is required.
What remains is one coherent augmented higher naturality statement.

## Scope

This is exact over the characteristic-zero theorem ring at `h=3`, in the
ninety-occurrence, endpoint-path, literal first-PP, target, and central-Eq
quotients.  It does not construct the physical higher totalization or extend
it through `q`, anchor, cap/ridge, and eta/sigma.  Nor does it promote the
rank-two private quotient to a terminal dual.

## Verification

Run normally, optimized, and isolated/no-site.  Expected headline:

```text
bare endpoint two-step holonomy: 0
common-C2+ protected curvature rank: 2
(A+I) curvature: 3*C (NOT KILLED)
triangle isotropy: A-switch; odd line bar-contractible in char 0
C2,C3: B-polynomials in v0; B-natural physical schema OPEN
```
