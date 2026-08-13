# The reduced-Eq frontier is one integral rho comparison

## Master statement

Let (R=k[\beta]), with (2\in k^\times), and let (K_{\rm Eq}) be the
canonical Koszul cell for

\[
 F=H_0-u,\qquad Q=\operatorname{Eq},\qquad
 dK_{\rm Eq}=F e_{\rm Eq}
\]

after relative base change (Q=0).  Adjoin the root involution (\rho).
The source orbit (R[\rho]K_{\rm Eq}) is generated equivariantly by one
object.  Consequently all three currently exposed reduced-Eq shadows are
restrictions of one comparison

\[
 \Phi_\beta:R[\rho]K_{\rm Eq}\longrightarrow
             C_{\rm phys}(\text{word/fine/repeated/augmented}).       \tag{1}
\]

The exact missing theorem is that (1) is a source-labelled (R)-linear
chain map with the following restrictions.

1. Its odd restriction (\Phi_\beta(1-\rho)) is the occurrence-local input
   comparison whose output is the already fixed physical cell
   (O_\alpha-K_\alpha=-M_v).
2. Its generic even restriction (\Phi_\beta(1+\rho)) is the complete
   rho-even product-rule packet: the (v=(B_1+B_4)/2) landing,
   (\delta_+), mixed target (-2D\otimes v), reduced-Eq face
   (+2D(H_0-u)e_{\rm Eq}\otimes v), labelled residue (v), protected
   (W=0), and the literal ridge/word faces.
3. At (\beta=0), naturality of the connecting morphism sends the formal
   proper face to the physical correction (V).  Then (U-V=\rho_0) is
   the selected protected (D0) unit.

Checker:
[`verify_h3_reduced_eq_integral_rho_comparison_master_gate.py`](../computations/verify_h3_reduced_eq_integral_rho_comparison_master_gate.py).

## What is already physical

Two pieces no longer need construction.

- The Koszul/Tate normal cell exists canonically in the derived source.
- The full-alpha odd **output** is physical:
  (O_\alpha-K_\alpha=-M_v).  It has the literal 360-feature lower
  boundary, the correct Eq and eta/sigma rows, and zero labelled residue,
  target, (W), anchor, and physical (q).

The second statement must not be enlarged silently.  It does not prove the
selected input equation

\[
                  J_3(M_v)=A J_{\rm col}(\ell),                         \tag{2}
\]

and it does not produce an objectwise rho-orbit.  Equation (2) is precisely
the odd restriction of (1).

## Why the even and special faces are one theorem

In the orbit basis ((K,\rho K)), the odd and even vectors are

\[
                  K_-=K-\rho K,\qquad K_+=K+\rho K.                    \tag{3}
\]

An equivariant map is determined by (\Phi_\beta(K)).  Conversely, because
two is invertible, compatible images of (3) recover the object images by

\[
 \Phi_\beta(K)={\Phi_\beta(K_+)+\Phi_\beta(K_-)\over2},\qquad
 \Phi_\beta(\rho K)={\Phi_\beta(K_+)-\Phi_\beta(K_-)\over2}.           \tag{4}
\]

Thus the odd output plus one even comparison is the entire regular orbit;
there is no third independent parity cell.

The beta face is likewise not a second generator once (1) is genuinely
(R)-linear.  If (ds=\beta y), then

\[
 d\Phi_\beta(s)=\Phi_\beta(ds)=\beta\Phi_\beta(y),                    \tag{5}
\]

so reduction modulo beta and division by beta commute with the comparison:

\[
 \delta_\beta[\Phi_\beta(s\bmod\beta)]
     =[\Phi_\beta(y\bmod\beta)].                                    \tag{6}
\]

Equation (6) is exactly the demanded (V) face.  This explains the global
pattern: odd, generic even, and beta-special are three functorial shadows of
one source-labelled integral comparison.

## Why the current pieces do not yet give the comparison

Knowing only the odd image leaves an invariant ambiguity.  Replacing an
object image (x) by (x+z), with (\rho z=z), leaves
(x-\rho x) unchanged but changes (x+\rho x) by (2z).  Hence the
physical (M_v) aggregate cannot determine the even face.

This ambiguity is visible in the actual augmented rows.  The known scalar
residue line and placed Cartan line span

\[
 \langle(1,1,1,1,1,1),(1,0,1,-1,0,-1)\rangle.
\]

The required (v=(0,\tfrac12,0,0,\tfrac12,0)) lies outside that span.  The
primitive covector

\[
                  \chi=(0,1,-1,0,1,-1)                                \tag{7}
\]

kills both known lines and reads one on (v).  This is the first generic
full-row obstruction to (1), not an extra terminal obligation.

At beta zero the literal cap matrix has Smith form

\[
                         \operatorname{diag}(1,\beta),                  \tag{8}
\]

so ([\rho_0]) is a genuine beta-torsion class in the known packet.  A
physical (V) with the unary cell's protected defect and zero root output
gives

\[
                         U-V=\rho_0,qquad \det(U,V,Z_1)=-1.             \tag{9}
\]

A generic construction involving (\beta^{-1}) cannot imply (9).  The
comparison must exist over (R), not only after localizing at beta.

## Exact status

The shared master reduction is positive but conditional:

```text
canonical reduced-Eq Koszul core                    CANONICAL DERIVED CORE
full-alpha odd output and terminal                  PHYSICAL (-M_v)
one rho-equivariant k[beta]-linear comparison       OPEN
generic even and beta-special packets               consequences of it
```

The smallest construction target is therefore (1), not separate odd,
even, and beta cells.  Its first odd private discrepancy is the known
`Xi^-`/`xi` face; its first generic augmented discrepancy is (7); its first
special discrepancy is (8).  A proof must make these three readouts commute
inside one literal word/fine/repeated source map.

Run:

```text
python3 computations/verify_h3_reduced_eq_integral_rho_comparison_master_gate.py
python3 -O computations/verify_h3_reduced_eq_integral_rho_comparison_master_gate.py
python3 -I -S computations/verify_h3_reduced_eq_integral_rho_comparison_master_gate.py
```

Frozen ledger SHA-256 is
`7975d9a3441ed532308ff3026a9ce01ffc268df930fd81badb6c76f3c57956d6`.
