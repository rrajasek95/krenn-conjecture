# The h=3 occurrence projector first meets the central Eq row after its literal six-term Hasse face

## Exact outcome

At intrinsic response order three, the two coefficient projectors specialize
to

\[
 \Pi_{\rm match}={A+I\over3},\qquad
 \Pi_{\rm end}={(B+2I)(B-2I)(B-4I)\over240}.          \tag{1}
\]

Here `A` switches the two residual matching edges and `B` moves one ordered
endpoint through one residual edge.  On the ninety occurrence coordinates,
`A` and `B` commute and

\[
 (B+2I)(B-2I)(B-4I)(A+I)e_f=8\mathbf1_{90}.          \tag{2}
\]

Since the combined denominator is `720`, (2) gives

\[
 \Pi_{\rm end}\Pi_{\rm match}e_f={1\over90}\mathbf1,
 \qquad e_f-\Pi_{\rm end}\Pi_{\rm match}e_f
       ={1\over90}c_f.                                \tag{3}
\]

Thus the coefficient association algebra is exact.  The physical lift does
not fail on a denominator or an omitted occurrence sector.  Its first
literal principal-parts face is already visible in the matching factor, and
the first remaining cross-summand obstruction is one central Eq incidence.

Checker:
[`verify_h3_centered_projector_literal_first_hasse_eq_incidence_gate.py`](../computations/verify_h3_centered_projector_literal_first_hasse_eq_incidence_gate.py).

## 1. The first literal Hasse face

The marked occurrence is

```text
head/word     11:110000
term          (p1_0_1*s1_1_1) q23:00 q45:00
tag           (p=0,s=1;23|45).
```

The numerator `A+I` sends it to the complete three-matching fibre with the
same ordered endpoints:

\[
 b_{01}=e_{(0,1;23|45)}+e_{(0,1;24|35)}+e_{(0,1;25|34)}. \tag{4}
\]

Its coefficient polynomial is

\[
 (p_0s_1)(q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34}),   \tag{5}
\]

so the exact first PP face is

\[
\begin{aligned}
 (p_0s_1)(&dq_{23}q_{45}+q_{23}dq_{45}
          +dq_{24}q_{35}+q_{24}dq_{35}\\
          &+dq_{25}q_{34}+q_{25}dq_{34}).             \tag{6}
\end{aligned}
\]

All four residual sites have colour zero.  Therefore both matching switches
in (4) are target-safe site permutations, and (6) has target and central Eq
incidence zero.

Equation (6) is source-faithful as a *formula*, but the fixed endpoint fibre
is not an old complete source equation.  The complete response row is the
sum of the thirty ordered-endpoint fibres.  Selecting `b_01` is exactly the
pointed occurrence localization which the construction is meant to prove.
Thus (6) identifies the first face; it does not assume that face is already a
source boundary.

## 2. The endpoint factors and their target normal

From `f`, `B` has eight literal moves: move endpoint `0` or `1` to one of
the residual sites `2,3,4,5` and pair the displaced endpoint with the old
residual mate.  Every move exchanges site colours `1` and `0`.  Its physical
path is the site transposition followed by the two-site signed Weyl path
which restores word `110000`.

The sum of the eight target normals is

\[
 \boxed{
 N_f=\sum_{\substack{x\in\{0,1\}\\t\in\{2,3,4,5\}}}
 \bigl(X_{\{x,t\}=1}+X_{\{x,t\}=0}\bigr)
 -8X_{000000}-8X_{111111}.}                           \tag{7}
\]

The notation in the first term means “ones at exactly `x,t`” and “zeros at
exactly `x,t`”, respectively.  The support of (7) is eighteen.  For example,
`X_101000^*` kills the GHZ line and reads one on (7).

The moving-target Cartan cone can absorb (7).  It does not erase the Hasse
product-rule face.  For a path from an occurrence coefficient `z_i`,

\[
 d(z_iH_{xt})=z_i(g_{xt}-1)+(dz_i)H_{xt}.             \tag{8}
\]

The second term is occurrence- and path-labelled.  All endpoint and matching
versions of (8) stay in the response/bar source summand; their central Eq
input incidence is zero.

## 3. Comparison with `P_f`, the primitive cap, and D4

Give the construction every coefficientwise advantage and suppose the
complete endpoint/matching first-face packet collapses to the desired
pointed conormal shadow `P_f`.  Retain the five independent row types

```text
(P_f, primitive cap p, private occurrence R_E14,
 central Eq input E, shifted ridge gamma).
```

Then the available shadows are

```text
projector first face  (1,0,0,0,0)
primitive cap         (0,1,0,0,0)
orbit D4 top           (0,0,1,0,0).
```

The required central placement is

```text
Phi_orb(E)=R_E14      (0,0,1,1,0).                   (9)
```

The first three vectors have rank three; adjoining (9) raises the rank to
four.  The primitive covector

```text
(0,0,0,1,0)
```

kills every endpoint/matching face, the primitive cap, the orbit-D4 top, and
the horizontal cap graph, but reads one on (9).  This is the exact mismatch:
the D4 top reaches the right occurrence and the projector can have the right
conormal shadow, but neither changes the source-row label to the central Eq
generator.

The grade distinction is literal:

- projector bottom: response head/word `11:110000`;
- primitive cap: `01211222`, fine grade `t*q_(v,N)`, repeated `P3+K2`;
- D4: moving word cube `110000 -> 111111`, with `R_E14=g` on `v04=0`;
- required domain: `E=(H0-u)e_Eq` in the central K-Eq comparison.

Thus `p` and `P_f` remain different homogeneous faces, and agreement of the
coefficient occurrence is not agreement of the source domain.

## 4. Consequence of the new T12 reconciliation

The remaining equality is

\[
 \boxed{\Phi_{\rm orb}((H_0-u)e_{\rm Eq})=R_{E14}}.  \tag{10}
\]

There is no separate `T12` theorem after (10).  The exact certificate is
`C=U`, `Z=0`: adjoining the source-labelled `R_E14` raises the old first-hit
rank `269 -> 270`, and the existing unary row supplies all twelve tails.

The cap and shifted-ridge faces should not be silently identified with (10).
They close downstream only when the same augmented comparison schema carries
their separately typed residue and terminal faces.  In particular, the
primitive cap has Eq incidence zero and cannot manufacture (10).

## 5. Anchor, physical q, and terminal scope

A physical `c_f/P_f` face supplies the sufficient scaled anchor law

\[
                         90[du_f]=[du].               \tag{11}
\]

It does not identify the central Eq source row.  Likewise (6) is a literal
`dq` PP face, not the already normalized physical six-term `q` generator or
separator.

The central-Eq incidence covector is therefore an exact local dual, but not
yet a physical Fredholm terminal.  It measures a source-domain label rather
than a target, anchor, physical-`q`, ridge, `W`, eta, or sigma output.  For
the complete augmented matrix `J`, the valid alternative is only

```text
E -> R lies in im(J)  -> central placement is constructed;
otherwise             -> a full left covector annihilates J and reads it.
```

Promoting the second arm requires extending the local incidence covector
across every literal augmented row.

## Shortest next theorem

Construct one augmented source-labelled totalization whose bottom contains
the fixed-endpoint six-term face (6), whose endpoint target normal (7) is
absorbed by the moving target, and whose mixed face is (10).  This would turn
the coefficient projector into the needed centered comparison.  The old
unary row then closes `T12`; cap, ridge, anchor, and physical `q` are retained
as typed faces of the same schema, not inferred from coefficient equality.

## Scope

This is exact for the canonical h=3 marked `11:110000` packet.  It constructs
the coefficient projector and its first literal product-rule faces, not the
full physical comparison.  It does not promote the central-Eq incidence dual
to a terminal.

Run normally, optimized, and isolated/no-site.  Frozen ledger SHA-256:

```text
6c5c70dab6c3213e8e4c02680b55c4eb1a0180b6c6f85980bb313828466ddff0
```
