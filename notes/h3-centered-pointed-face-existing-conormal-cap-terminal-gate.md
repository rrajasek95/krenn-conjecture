# The centered pointed face is neither the old `P_f` nor the cap graph

## Exact verdict

The presentation-safe Maschke cone retains a centered graph coordinate
`U_c` with

\[
 dU_c=\gamma_c=90df-dR.                              \tag{1}
\]

None of the three proposed existing mechanisms consumes (1) without one
new physically typed landing.

1. The old occurrence conormal `P_f=d(z_f-u)` has the wrong normalization.
2. The cap graph `T+rho` is a flat target/residue normalizer in a distinct
   cap word and has zero response-conormal projection.
3. Failure of source-conormal membership gives a tangent, not a physical
   Fredholm output covector.  Terminal duality applies only after (1) has
   been placed in the complete augmented physical codomain.

Checker:
[verify_h3_centered_pointed_face_existing_conormal_cap_terminal_gate.py](../computations/verify_h3_centered_pointed_face_existing_conormal_cap_terminal_gate.py).

## 1. The factor `90` is structural

Let `z_f` be the marked private occurrence graph coordinate, let
`Z=sum_M z_M`, and let `u` be the global central anchor.  The already
symmetric graph normal is

\[
                         B=dZ-du.                     \tag{2}
\]

In coordinates `(dz_f,dZ,du)`, retain

\[
 B=(0,1,-1),\qquad P_f=(1,0,-1),\qquad
 \gamma_c=(90,-1,0).                                 \tag{3}
\]

The first two rows have rank two; adjoining `gamma_c` raises the rank to
three.  The common-scale tangent

\[
                         \xi=(1,1,1)                  \tag{4}
\]

kills both `B` and `P_f` but reads

\[
                         \gamma_c(\xi)=89.            \tag{5}
\]

Equivalently, modulo (2),

\[
                  [\gamma_c]=90[P_f]+89[du].          \tag{6}
\]

Since `89` is a unit in characteristic zero, old `P_f` leaves precisely the
global-anchor scale.  Killing that remainder would kill the common scaling
tangent; it is not a contractible change of presentation.  This is why the
unscaled bridge `[dz_f]=[du]` and the centered bridge
`90[dz_f]=[du]` cannot be silently combined.  Each is anchor-visible, but
they are different conormal identities.

The presentation-safe response graph of `e139847` gives the same result in
mate language: it transports `P_f` to the private slack `-dG`; it does not
make either the slack or (1) zero.

## 2. The cap graph is orthogonal to the missing face

The physical cap graph at normalized `Y=1` is

```text
dT=-w,  d(rho)=w,  Gcap=T+rho,  dGcap=0.
```

In coarse rows

```text
(response centered conormal, target, cap ores, physical q, ridge)
```

its signature is

```text
gamma_c shadow       (1,0,0,0,0)
T+rho                (0,1,1,0,0).
```

The two vectors have rank two.  More importantly, the type separation is
literal:

```text
gamma_c : response head/word 11:110000,
          first PP dc01=30db01-dR;

T+rho   : word 01211222,
          fine t*q_(v,N), repeated P3+K2.
```

The cap graph has zero boundary, `W`, Eq, lower, anchor, physical-q, ridge,
eta, and sigma rows.  It is useful after a cross-word placement: it removes
target/scalar-residue normalization and transports flatly.  It cannot
create the response pointed face or its six-term first-PP image.

## 3. Why the local dual is not yet a terminal

The tangent (4) is an exact nonmembership certificate.  It may be extended
by zero on independent physical-q and shifted-ridge rows while retaining
`gamma_c(xi)=89`.  Thus nonfill of (1) alone does not produce a q generator,
ridge terminal, or Fredholm annihilator.

There is also a variance obstruction.  A missing source conormal is detected
by a vector in the kernel of the source Jacobian.  A Fredholm terminal is a
left covector on a complete physical correction codomain.  No canonical map
between those two objects is supplied by the occurrence graph.

Once a source-labelled comparison places (1) as an actual column `b` in the
complete augmented physical map `J`, finite duality is exhaustive:

```text
b in im(J)      -> the centered attachment is constructed;
b not in im(J)  -> lambda J=0, lambda(b)=1.
```

Only at that point do the existing physical-q kernel/generator versus
Fredholm alternatives type the second arm.  An occurrence-selector dual or
the common-scale tangent before this landing is not an accepted physical
terminal.

## Shortest remaining theorem

Construct one **scaled pointed centered-response attachment** with these
faces:

1. degree zero: `U_c=90e_f-1_90` in response head/word `11:110000`;
2. conormal: `dU_c=90df-dR`, giving the scaled anchor law;
3. matching first PP: `dc01=30db01-dR`, including the six literal `dq`
   terms and their aggregate physical-q typing;
4. fixed-word endpoint paths: the 18-term target normal `N_f` and the
   `B`-natural `C2,C3` faces;
5. cross-word cap: the flat `T+rho` graph and primitive cap placement in
   `01211222 / t*q_(v,N) / P3+K2`;
6. shifted Kähler: `gamma_v=-dOmega_v`, with its unique eta/sigma laws.

Maschke already contracts every nontrivial finite-group character direction
once this section is termwise physical.  The irreducible new content is the
invariant scaled graph/PP attachment and its augmented placement, not
another group-homology calculation.

This is exact for the canonical `h=3` characteristic-zero packet.  It does
not construct that attachment or promote a pre-placement local covector to a
terminal.

Run normally, optimized, and isolated/no-site.  The frozen ledger digest is
recorded by the checker.
