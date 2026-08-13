# The first carrier relation is a two-orientation base-change gate

## Outcome

On an intrinsic scalar-unit clean packet, the two endpoint-ordered
curvature factors are

\[
 K^\rightarrow=q-x,
 \qquad K^\leftarrow=q-r+x,
 \qquad K^\rightarrow+K^\leftarrow=2q-r.               \tag{1}
\]

The normal jet constructs the complete first moment

\[
 H_0=\int_0^1(q+tr)^{[h-2]},dt                       \tag{2}
\]

and, on the clean intrinsic packet, proves

\[
                    \Theta=rH_0\ne0.                  \tag{3}
\]

Consequently, if the two physical oriented four-cut rows annihilated the
**same** augmented carrier,

\[
                         K^\rightarrow H_0=0,
 \qquad                  K^\leftarrow H_0=0,           \tag{4}
\]

then adding (4) would give exactly

\[
                  \boxed{c_0=(r-2q)H_0=0}.             \tag{5}
\]

This is the strongest valid route from the oriented four-cut equations to
the first Hilbert--Cauchy carrier relation.  The currently committed
four-cut rows do not have the common-carrier typing required by (4).  They
annihilate two coefficient restrictions (H^\rightarrow,H^\leftarrow)
which can omit different occupied monomials or undergo different evaluated
cancellations.

Writing

\[
 H^\rightarrow=H_0+\delta^\rightarrow,
 \qquad H^\leftarrow=H_0+\delta^\leftarrow,             \tag{6}
\]

the two restricted equations imply the exact mismatch identity

\[
 \boxed{
 c_0=K^\rightarrow\delta^\rightarrow
        +K^\leftarrow\delta^\leftarrow.}                \tag{7}
\]

Thus (5) is neither disproved nor constructed: it is precisely the claim
that the right side of (7) dies after a source-valid common
restriction--insertion/base-change comparison.  Failure leaves a finite
carrier-mismatch cokernel class.

## 1. What the strongest physical four-cut results establish

There are two complementary exact facts.

First, on the essential (2\)-by-(2) endpoint-support packet, cleanliness
and minimum support force a literal nonzero coefficient

\[
                \kappa^{\rm or}_e(H_0)_{\rm comp}\ne0   \tag{8}
\]

in one oriented physical four-cut carrier layer.  This proves that the
actual clean packet is not invisible to every oriented restriction.  It
does not compare the other orientation or insert (8) back into the complete
(H_0) module.

Second, the exact (h=3) localization guard has a nonzero leading
adjacent-(q) curvature coefficient which cancels after replacing the
leading carrier by the full first moment:

\[
 \kappa_e^\rightarrow\nu(efq)=-1,
 \qquad
 \kappa_e^\rightarrow\nu(efH_0)=0.                     \tag{9}
\]

The packet in (9) is not a complete clean ternary source, so it does not
negate (8).  It proves that the transport from a detected restricted
coefficient to a complete carrier class is genuine extra data.  Ordinary
nonzero-curvature selection, occupancy counting, and coefficient
localization do not supply it.

Even granting the stronger global equations (4) would yield carrier
torsion (5), not cancellation of (H_0).  The universal polynomial guard
shows that cleanliness plus (5) alone does not kill the exceptional target.
For the moment-tower programme this is expected: (c_0) is the first
relation, not the entire proof.  At (h=3,4), (c_1) is still required.

## 2. Finite common-carrier membership and dual

Let (P) be the complete physical augmented carrier module in the selected
word/fine/repeated-response grade.  It includes protected target, anchor,
terminal, and physical (q)-cocycle rows.  Let

\[
 B_{\rm com}:P\longrightarrow P^\rightarrow\oplus P^\leftarrow \tag{10}
\]

be the proposed all-label base-change map which restricts one complete
carrier to the two endpoint orientations.  Let (C_{\rm phys}) contain
the already physical zero-shadow correction columns in the two restricted
modules.  The pair of actual restricted carriers descends from one common
augmented class exactly when

\[
 \boxed{
 \operatorname {rank}[B_{\rm com}\ C_{\rm phys}]
 =\operatorname {rank}[B_{\rm com}\ C_{\rm phys}mid
                 (H^\rightarrow,H^\leftarrow)].}       \tag{11}
\]

If (11) holds with a preimage whose two oriented rows vanish, (5) follows.
If it fails, finite-dimensional linear duality gives

\[
 \lambda B_{\rm com}=0,
 \qquad \lambda C_{\rm phys}=0,
 \qquad
 \lambda(H^\rightarrow,H^\leftarrow)\ne0.              \tag{12}
\]

This (lambda) is the carrier-mismatch dual.  In the two-coordinate toy
model, the common carrier is the diagonal and the primitive separator is

\[
                 \lambda=(0,-1;0,+1),                  \tag{13}
\]

which reads the private difference between the two restrictions and kills
every diagonal common carrier.  The companion checker verifies (11)--(13)
and a zero-shadow correction which repairs the mismatch.

Equation (12) becomes a physical Fredholm separator only when (10) and
(C_{\rm phys}) are the complete source-valid augmented maps, including
the terminal and (q) rows.  A covector on two coefficient presentations
is not automatically a physical terminal.  Conversely, once that typing is
present, the existing kernel/separator alternative applies without another
abstract product guard.

## 3. Conditional active-clean alternative

The common-carrier problem can be compressed into one sharp physical
alternative.

> **Oriented (c_0) comparison alternative.**  Construct a source-valid
> augmented lift (Pi_0) of the complete (H_0) carrier whose two
> orientation projections are the literal four-cut classes
> (K^\rightarrow H_0) and (K^\leftarrow H_0).  Identify each nonzero
> projection with the corresponding clean-line coordinate in the physical
> relative quotient.  Then either one projection is nonzero and gives an
> active clean line, or both projections vanish and (5) follows.

The identification in the second sentence is essential.  A nonzero
evaluated coefficient such as (8), without its augmented relative lift, is
not yet an active clean-line class.

The complementary-pivot theorem supplies the nonzero input on its essential
packet.  The missing theorem is exactly the common (Pi_0), not another
curvature existence lemma.  If no such lift exists, the fully typed version
of (12) is the appropriate terminal branch.

## 4. Relation to the centered endpoint projector

The centered endpoint association projector is a natural candidate for
(Pi_0).  Its incidence/Čech factorization has a surviving unweighted
base class, explicitly identified as the (H_0) augmentation.  After
projection to the physical cap complex, all standard face differences are
Cartan boundaries and one primitive reduced companion remains:

\[
 Q_{v,N}=-1,
 \qquad \operatorname {ores}=-1,                       \tag{14}
\]

with the protected rows zero.  A source-valid primitive cap cell realizing
(14), with both oriented four-cut projections, would therefore implement
the alternative of Section 3: nonzero projection lands in the active-clean
branch; two zero projections add to (5).

This is currently conditional.  The coefficient projector is constructed,
but its physical source descent and primitive cap cell are not in the
inventory.  In particular, the endpoint projector may not be used as
(B_{\rm com}) in (11) until its endpoint Cartan, pairwise Hasse, mixed,
cubic Hasse, word, target, terminal, and physical (q) faces have been
totalized.

The same distinction answers whether (c_1) is already the first face of
this construction.  Formally,

\[
 c_1=(r-2q)\int_0^1t(q+tr)^{[h-2]},dt                \tag{15}

is the first **weighted moment** of a polynomial horizontal one-form.  It
is a face of the same family only if the physical lift refines to a
source-valid one-form (E(t)dt) satisfying

\[
 dE(t)dt=(r-2q)(q+tr)^{[h-2]}dt.                       \tag{16}

Then integrating (16) against (1) gives (c_0), and against (t) gives
(c_1).  The committed endpoint projector supplies the unweighted (H_0)
base augmentation, not the affine parameter, density, or horizontal
one-form (16).  Therefore (c_1) remains the first new weighted/Hasse face;
it is not a formal consequence of the cubic endpoint projector.

The based-loop torsor shows why this extra condition is necessary: endpoint
data and the unweighted integral are unchanged by vertical based loops,
while the (t)-weighted moment changes.  A positive construction must
choose a zero-residue horizontal lift or prove the relevant physical
vertical cycle is a boundary.

## 5. Sharp next construction

The shortest proof-advancing source cell is one enriched primitive cap
family, not two unrelated carrier equations:

1. its unweighted projection is the centered endpoint (H_0) base class;
2. its two orientation projections lie in one common augmented module and
   satisfy the alternative of Section 3;
3. it includes the primitive reduced cap (14) and all protected/terminal/
   physical-(q) readouts; and
4. it carries a horizontal affine parameter whose first weighted face is
   (15), with zero based-loop residue.

Items 1--3 decide (c_0) versus active-clean/separator.  Item 4 supplies
the remaining (c_1) needed at both (h=3) and (h=4).  Without item 4,
landing (c_0) is real progress but does not close the Hilbert--Cauchy
moment transfer.

## Verification

Run

```text
python3 computations/verify_scalar_unit_c0_four_cut_common_carrier_gate.py
python3 -O computations/verify_scalar_unit_c0_four_cut_common_carrier_gate.py
python3 -I -S computations/verify_scalar_unit_c0_four_cut_common_carrier_gate.py
```

The checker pins the complete normal jet, carrier-torsion guard,
essential-pair detector, full-carrier cancellation packet, based-loop
torsor, augmented moment gate, and centered endpoint primitive-cap gate.  It
verifies the signs in (1), the mismatch formula (7), and the finite
membership/dual alternative (11)--(13).
