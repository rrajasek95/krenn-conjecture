# H3 Hasse-commutator principal-parts saturation gate

## Result

Let (t=H_0-u), let (N) be the literal translated Hasse cap
totalization, and let (pi_{\mathrm{top}}) be its marked top projection.
The pinned cap calculation gives

\[
 [d,\pi_{\mathrm{top}}]N=tE,
 \qquad E=e_{\mathrm{Eq}}.
\]

Thus the smallest target that remembers this defect without introducing the
auxiliary (B/\mathrm{Eq}) split is

\[
 C_{\mathrm{comm}}=\mathbf Q[t]\{E\},
 \qquad
 E=\frac{[d,\pi_{\mathrm{top}}]N}{t}\pmod t.
\]

This first-jet class is invariant under chain homotopy of the projection:
in the Hom complex, replacing (pi) by (pi+\delta h) does not change
(delta\pi), since (delta^2=0).  It is also unchanged by a split
contractible stabilization with its commuting split projection.  This gives
a canonical filtered/principal-parts **target line once the marked pair
((N,\pi_{\mathrm{top}})) is part of the object**.

The result is negative at the next interface.  The complete current fixed
(\Gamma)-grade source has 8,580 order-six columns, supported in words
`11111111` and `11211211`, together with 48 squarefree
Macaulay--Schreyer slots and 72 Hasse edges (and 72 reverse edges).  Its
literal equation, occurrence, fine-degree, and operator-history labels have
no marked-cap or top-projection coordinate.  In particular they do not
canonically define a matrix row

\[
 J_{\mathrm{comm}}:C_1^{\mathrm{phys}}\longrightarrow
 C_{\mathrm{comm}}.
\]

Under the smallest zero extension of those native columns, reduction modulo
(t) has rank zero on the commutator line, while adjoining (E) raises the
rank to one.  Hence in that extension

\[
 E\notin \operatorname{im}J+tC_{\mathrm{comm}}.
\]

The known commutator and a relative cell (dK=tE) both reduce to zero, so
neither is a post-specialization filler.  A filler must have an
(E)-coefficient (a(t)) with (a(0)\ne0), equivalently an absolute/unit
decorated Eq coefficient, together with its protected faces.

## Why this is not yet a physical terminal

The physical terminal right-hand side is specified by equation/occurrence
and protected cap readouts, not by a marked projection.  It has two
extensions to the native target plus (C_{\mathrm{comm}}), with
commutator values zero and one, which agree on every original label.  Split
stabilization invariance does not distinguish them.  Therefore
(E^*(E)=1) is not yet a well-defined observable on the physical RHS or on
all physical primitive boundaries.

The known derived source (N) retains the (q_{23}:21) and
(q_{45}:12) faces and closes the augmented target pair, but it still lacks
the occurrence-local P2 landing.  The (35/72) `0102/dq23` detector is
forced only after granting that landing; complete Eq and labelled residue
faces remain.  These facts do not manufacture the missing comparison row.

The exact next datum is consequently one stabilization-invariant,
source-derived natural transformation from the literal physical
(\Gamma)-presentation to (C_{\mathrm{comm}}).  It must assign explicit
commutator coefficients to the actual RHS and every primitive boundary while
retaining the (q), anchor, target, ores, (W), ridge, eta, sigma, word,
fine, repeated-site, and operation labels.  Once that pairing is defined,
the question becomes the finite exact system

\[
 Jx+ty=E.
\]

This note proves a canonical-commutator and missing-pairing criterion.  It
does **not** prove that a physical post-specialization Tor filler is absent,
does not construct the occurrence-local P2 landing, and does not yield a
Fredholm contradiction for the original EqSystem.

## Reproduction

Run:

```text
python3 computations/verify_h3_hasse_commutator_principal_parts_saturation_gate.py --mode all
python3 computations/verify_h3_hasse_commutator_principal_parts_saturation_gate.py --mode target
python3 computations/verify_h3_hasse_commutator_principal_parts_saturation_gate.py --mode source
python3 computations/verify_h3_hasse_commutator_principal_parts_saturation_gate.py --mode saturation
python3 computations/verify_h3_hasse_commutator_principal_parts_saturation_gate.py --mode rhs
```

Pinned ledger digest:

```text
ce984713b77b86adfd0ebe4045f5d4bd5d413dd934b85c6b258e695ab509a177
```

