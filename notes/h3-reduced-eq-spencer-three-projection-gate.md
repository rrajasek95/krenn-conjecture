# One reduced-Eq Spencer cone has odd, even, and beta-Bockstein shadows

## Result

The odd quiver/Kähler cylinder, the generic even product-rule orbit, and the
beta-zero cap Bockstein contain the same monic physical conormal

\[
                         E=(H_0-u)e_{\rm Eq}.                  \tag{1}
\]

Their coefficient modules differ, but their missing physical descent can be
stated as one theorem.

* The odd underived cylinder leaves `+E`, so its correction needs `-E`.
* The full generic even orbit needs

  \[
                 +2D\,E\otimes v,
  \quad D=(-1,1,-1,1),
  \quad v={B_1+B_4\over2}.                                  \tag{2}
  \]

* At beta zero, the correction `V` must carry the same primitive `E` defect
  as the unary top and zero selected/complementary root output.  Then

  \[
                         U-V=\rho_0=[D_0]                     \tag{3}
  \]

  is protected.  The cap identity `J(s)=beta*rho0` identifies (3) as the
  special beta-Bockstein face.

Formally these are exactly three coefficient projections of the two-term
Spencer cone

\[
                    K_{\rm Eq}\longrightarrow R E,
                    \qquad dK_{\rm Eq}=E.                    \tag{4}
\]

This is not yet a physical construction.  The three shadows live in
different parity, word, endpoint, and repeated-label grades.  The only
current common proper-face candidate is explicitly non-descending: it
retains the primitive endpoint ridge and misses the selected midpoint word.

The strongest uniform source theorem is therefore one integral
`k[beta]`-linear, source-labelled reduced-Eq/Spencer mapping cone whose odd,
generic-even, and beta-Bockstein projections are the three packets above.
It would remove one obstruction in Interface I and both the generic and
collision reduced-Eq obstructions in Interface III.

## 1. The three pinned appearances of `E`

The odd quiver/Kähler construction is a genuine derived principal-parts
cylinder.  Its first-jet matrix is

\[
                       J_1(U)=\begin{pmatrix}U&0\\dU&U\end{pmatrix},
                       \qquad U=u/t.                          \tag{5}
\]

The horizontal Cartan operator commutes with both `U` and `dU`, so no extra
mixed diagonal appears.  Projection from the derived cylinder to the
literal underived source leaves exactly

\[
                                +E.                           \tag{6}
\]

This is the pinned q-zero-top commutator; it is not a generic unspecified
Eq row.

On the generic even side, the normalized adjacent-target construction
requires the relative correction

\[
                              +2D E.                          \tag{7}
\]

The unique missing fixed label is `v=(B1+B4)/2`, so the full labelled face is
exactly (2).  This is one load-bearing projection of the full even orbit,
alongside `delta+`, mixed target, labelled ordinary residue, and `W=0`.

At beta zero, the full third-cofactor totalization has formal proper-face
boundary

\[
                              -E.                             \tag{8}
\]

The sign in (8) is the opposite face convention of the same mapping cone.
The unary top and its correction therefore have the normal form, in rows
`(E,rho0,rho2)`,

\[
                       U=(1,1,0),\qquad V=(1,0,0).             \tag{9}
\]

Subtracting gives (3).  The beta-Rees cap calculation independently proves
that `[rho0]` is the Bockstein torsion class, so (9) is the correct special
coefficient projection rather than an analogy based only on names.

## 2. Universal coefficient projection

Let `C` be any coefficient module on which the Spencer differential is
trivial.  Tensoring (4) with `c in C` gives

\[
                    d(K_{\rm Eq}\otimes c)=E\otimes c.        \tag{10}
\]

Take successively

\[
 c_{\rm odd}=-1,qquad
 c_{\rm even}=2D\otimes v,qquad
 c_{\rm sp}=1.                                             \tag{11}
\]

Equations (10)--(11) give exactly `-E`, (2), and the `E` coordinate of `V`.
The checker expands `2D tensor v`: it has eight nonzero coefficients, all
`+1` or `-1`, and zero augmentation, agreeing with the root-even full-orbit
packet.

This proves that no new algebraic Eq identity is needed in the three
branches.  The remaining issue is descent and source typing of one universal
identity.

## 3. Why the formal common face is insufficient

The full even/product-rule audit records for its current proper-face tail:

```text
source-valid                         false
endpoint-ridge space rank            6
primitive Omega rank                 5
selected midpoint source-word hits   0.
```

Those failures are exactly the data suppressed by (4).  Likewise, the odd
cylinder is derived and quiver-valued; collapsing its two endpoint objects
to one scalar grade is singular at `u=0`.  Thus the equality of conormal
polynomials does not permit moving a source column between sectors.

In particular, the beta-zero `V` is the special projection of the same
**formal** cone, but it is not yet proved to be the beta-zero projection of
a physical generic orbit.  That stronger assertion requires one integral
family before a full physical Bockstein is even defined.

## 4. Single physical descent theorem

The exact common theorem is:

> **Reduced-Eq/Spencer three-projection theorem.**  Over `k[beta]`, construct
> a Rees-linear source-labelled mapping cone `K_Eq(beta)` in the complete
> augmented word/fine/repeated physical complex such that:
>
> 1. its rho-odd projection cancels (6), retains the pq/xv objectwise
>    Kähler terminal, and makes the physical q defect a protected row;
> 2. its generic rho-even projection is (2) inside the one full orbit with
>    the prescribed `delta+`, mixed target, labelled residue, ridge/word,
>    and `W=0` faces; and
> 3. its beta-zero proper-face Bockstein is the complete column `V` of (9),
>    matching every protected row of `U` except the selected `D0` output.

All three clauses must use the actual source labels.  A bare copy of (1), a
formal Hasse top, or an occurrence coefficient does not satisfy the theorem.

If it holds, the odd projection removes the last underived Eq residual from
the quiver cylinder.  The even projection supplies the missing reduced-Eq
face of the generic Interface-III orbit.  The special projection gives
`U-V`, removes the explicit beta torsion, and proves
`1 in theta_0(ker P_0)`.  Hence the generic and beta-zero Interface-III
branches close by one integral cell rather than two independent repairs.

This theorem does not by itself construct the remaining odd physical label
comparison or settle a nonzero physical q quotient defect; it unifies their
reduced-Eq descent component.

## Verification

Run:

```text
python3 computations/verify_h3_reduced_eq_spencer_three_projection_gate.py
python3 -O computations/verify_h3_reduced_eq_spencer_three_projection_gate.py
python3 -I computations/verify_h3_reduced_eq_spencer_three_projection_gate.py
python3 -S computations/verify_h3_reduced_eq_spencer_three_projection_gate.py
```

All modes print ledger digest
`8e8ec3291d0682b04bf5eb300d7dde2792209846b1e64920aec24410b556199f`.
