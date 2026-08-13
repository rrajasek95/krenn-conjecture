# Gate I needs two denominator memberships, not the full five-face star

Research reduction only.  This note does not construct the two labelled
ordinary-residue chains, prove a complete full-source relation, or prove
Krenn's conjecture.

## Result

The denominator-Tor requirement for the two Gate-I repairs is strictly
weaker than surjectivity onto all five deletion faces.  Let

\[
 J:X\longrightarrow Y
\]

be the complete source differential in the relevant word, fine, repeated-
site, and Rees grade, and let

\[
 r:X\longrightarrow P
   =S\langle d_{\rm fixed},d_{\rm pair}\rangle                 \tag{1}
\]

be a **physically proved** rank-two readout.  Put \(K=\ker r\), choose a
section \(s:P\to X\), and form

\[
 C=\operatorname {coker}(J|_K),\qquad
 \beta:P\longrightarrow C,\quad p\longmapsto[Js(p)].           \tag{2}
\]

Then the exact identity is

\[
                  \boxed{\ r(\ker J)=\ker\beta.\ }              \tag{3}
\]

Consequently the desired two repairs exist exactly when

\[
 \boxed{\quad
 Js(d_{\rm fixed})\in J(K),\qquad
 Js(d_{\rm pair})\in J(K).
 \quad}                                                          \tag{4}
\]

These are the weakest two full-source memberships.  No other face direction
is required.  Over a field, failure has the exact dual alternative: there is
an output covector \(\lambda\) such that

\[
 \lambda J|_K=0,\qquad
 c=\lambda Js\ne0\ \text{in }P^*,                               \tag{5}
\]

and \(c\) annihilates \(r(\ker J)\).  Thus (4) gives the two chains, while
(5) gives the sharp rank-one-or-zero separator.  Over a general ring the
membership formulation (4) is primary; a scalar covector need not separate
a nonprojective quotient until passing to a residue field or a suitable
constant-rank localization.

Checker:
[`verify_h3_denominator_tor_two_repair_projection_gate.py`](../computations/verify_h3_denominator_tor_two_repair_projection_gate.py).

## Denominator form of the criterion

For the old denominator presentation, split

\[
 X=C_{\rm oth}\oplus F,
 \qquad J=[b_{\rm oth}\ b_{\rm sel}],
 \qquad F=S\langle\omega_1,\ldots,\omega_5\rangle.              \tag{6}
\]

Suppose a chosen quotient \(\pi:F\to P\) really records the two placed
repair chains.  Write \(U=\ker\pi\).  Formula (2) becomes

\[
 C=\operatorname {coker}[b_{\rm oth},b_{\rm sel}|_U],\qquad
 \beta=[b_{\rm sel}s]:P\to C.                                  \tag{7}
\]

Hence each chosen selected section column need only belong to the span of
the ten unselected columns **plus the three selected combinations in
\(U\)**.  Requiring every selected column to belong to
\(\operatorname {im}b_{\rm oth}\), as in full \(S^5\)-surjectivity, is
unnecessary.

On a constant-rank local chart, (4) can be tested by adjoining the two
section columns separately to \([b_{\rm oth},b_{\rm sel}|_U]\): neither
adjoining may raise rank.  Globally, these are module memberships, not just
vanishing of a convenient nonmaximal minor.

## The rank-three and rank-four packets separate rank from placement

For `12112`, the exact packet images are

\[
\begin{aligned}
 I_{\rm df}&=\langle
 \omega_1,\omega_3,-\omega_2+\omega_4,-2\omega_2+\omega_5\rangle,\\
 I_{\rm tilt}&=\langle
 \omega_1,\omega_3,-\omega_2+\omega_4\rangle.
\end{aligned}                                                    \tag{8}
\]

They have total ranks four and three.  Two different projections show why
that total rank is not the theorem.

First take the abstract relabelled-chart seed projection

\[
                  \pi_{12}(y)=(y_1,y_2).                         \tag{9}
\]

Both packets have projected rank two: \(\omega_1\) supplies the first
coordinate and \(-\omega_2+\omega_4\) supplies the second.  The invariant
orbit-sum quotient for
\(A=\{1,3,4\}, B=\{2,5\}\) also has rank two on both packets.  This is
concrete evidence that demanding all five faces is overkill.

But neither quotient has been placed into the six canonical pure multiplier
labels \(B_0,\ldots,B_5\).  The only presently evaluated denominator-tail
placement in the faces-`(3,5)` component sends

```text
face 3 -> B4,       face 5 -> B1
```

after conditional matching-Bianchi transport.  Its coordinate test is

\[
                  \pi_{35}(y)=(y_3,y_5).                         \tag{10}
\]

Here the direct-free packet has rank two, but the tilted packet has rank
one:

\[
 \pi_{35}(I_{\rm df})=S^2,
 \qquad
 \pi_{35}(I_{\rm tilt})=S(1,0).                                 \tag{11}
\]

Equivalently, in the tilted packet the face-3 section satisfies its
membership in (7), while the face-5 section does not.  Thus even rank three
in the five-face image does not force the two **specified** outputs.  One
must prove (4) for the physically placed quotient; an unlabelled rank lower
bound cannot replace it.

The face-3/face-5 tail result is itself conditional and has the protected
target/anchor/residue mismatch recorded in `73ee225`.  Equation (11) does
not promote it to either odd labelled-residue section.

## Hall and active-fan rows do not presently prove (4)

The complete active-fan pivot theorem types a nonzero target or exchange
carrier with its common-\(q\), endpoint, word, and Hall shore.  It explicitly
leaves the trapped-carrier affine/dependence lift open.  None of its
identities says that either selected denominator section column lies in the
image of the full zero-\(r\) source \(K\).  The Hall covector is a downstream
alternative once a physical carrier or dependence exists; it does not
manufacture the two primal memberships in (4).

Likewise, the clean `C5` collision lattice controls an aggregate face
boundary, not the six labelled ordinary-residue outputs.  On the exact clean
slice every denominator kernel has zero face augmentation.  Therefore the
aggregate attachment theorem cannot silently supply a unit fixed or paired
label.

The correct way to include new Hall or active rows is already built into
(2): every newly proved source column with zero \(r\)-readout enlarges
\(J(K)\).  If it makes both memberships (4) true, the gate closes.  No
committed theorem currently proves either required equality in the canonical
fine grade.

## Read-only audit of the unaudited Gate-I REPORT

`computations/unaudited-gate1-phi-probe-2026-08-12/REPORT.md` does not change
this frontier.  Its positive membership is in a 32-row coarse signature
model with four corner rows `R_c`.  The clean inventory is represented
either by one corner-aggregate row or by an explicitly more-generous copy at
every corner.  The probe never defines a readout from literal source columns
to the six multiplier labels \(B_0,\ldots,B_5\), and never constructs
`d_fixed` or `d_pair` in the canonical faces-`(3,5)` grade.  Its own limits
say that augmented signatures of the 576 literal columns are unavailable.

Accordingly its statement that the “residue/private lane is closed” means
only that the coarse corner-residue/private/Eq signature is in the admitted
span after the Cartan prism.  It is compatible with the source-scope audits
`e5eb1fe` and `689909c`, which concern a finer primal section.  The REPORT
may remove a coarse terminal-span obstruction; it supplies neither
membership in (4), and hence does not advance the exact labelled-residue
proof frontier.

The REPORT remains untracked and unaudited, so it is deliberately not an
executable dependency of the checker.

## Frontier

The full five-face surjectivity problem can now be replaced by one precise
rank-two gate:

> Construct a physical rank-two readout (1) in the canonical grade and
> prove the two memberships (4), or descend the covector (5) to an already
> accepted typed terminal/Hall alternative.

There are two separable obligations.  The first is **placement**: identify
which two combinations of the five face coordinates have ordinary residue
exactly one fixed and one paired \(B\)-direction, with zero
`lower/W/target/ainc`.  The second is **membership**: prove that both placed
section columns vanish in the full-source quotient (2).  The abstract
two-seed packet success addresses membership only after an unproved
placement; the evaluated faces-`(3,5)` placement is incomplete and has the
sharp tilted rank-one guard (11).

## Verification

Run:

```text
python3 computations/verify_h3_denominator_tor_two_repair_projection_gate.py
python3 -O computations/verify_h3_denominator_tor_two_repair_projection_gate.py
python3 -I -S computations/verify_h3_denominator_tor_two_repair_projection_gate.py
```

Frozen ledger digest:

```text
4a2abb7eedf6864d349f897059ac318248050242b701ca030e90109f5f3bf354
```
