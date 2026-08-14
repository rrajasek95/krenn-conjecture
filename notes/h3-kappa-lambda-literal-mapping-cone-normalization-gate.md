# The standard mixed mapping-cone product has `lambda_i=0`; physical multiplicativity is the missing axiom

## Verdict

For a literal selected response section and the central reduced-`Eq` cone,
the standard Koszul/mapping-cone product has tied private and reduced-`Eq`
occurrence coefficients.  Therefore its balanced charge is zero:

\[
 \boxed{
  \kappa_i^{\rm std}=\epsilon_i\wedge\theta
  \quad\Longrightarrow\quad
  \Pi_{B/Eq}(d\kappa_i^{\rm std})=(v_i,v_i),
  \qquad \lambda_i=\Psi(d\kappa_i^{\rm std})=0. }
 \tag{1}
\]

This conclusion comes from the two individual faces of the literal
differential, not merely from `d^2=0`.

The current physical inventory does not yet prove that a mixed cell is this
standard product.  Objectwise naturality, the four square edges, and all
known target/`q`/anchor/residue/ridge conservation laws permit the twist

\[
 d\kappa_i^{(\lambda)}
 =d\kappa_i^{\rm std}+\lambda_i(\delta,0),
 \qquad \delta=(1,1,-1,-1).                           \tag{2}
\]

Every value in (2) has the same mapping-square boundary and the same known
augmented external faces.  Hence the actual physical value remains free
until one additional source statement is proved.

The minimum useful statement is strict physical multiplicativity: the
selected occurrence comparison must be a normalized module/DGA map over the
physical central `K_Eq` cone, with mixed cell exactly
`epsilon_i wedge theta` and no extra closed balanced cap cocycle.  Its scalar
shadow is simply

\[
                  \delta\cdot B(d\kappa_i)
                    =\delta\cdot Eq(d\kappa_i),       \tag{3}
\]

which forces `lambda_i=0`.  No current physical row forces a fixed nonzero
value.

Checker:
[`verify_h3_kappa_lambda_literal_mapping_cone_normalization_gate.py`](../computations/verify_h3_kappa_lambda_literal_mapping_cone_normalization_gate.py).

## 1. One representative: lower word `0102`

Take the one-root lower object `0102`, obtained from the marked parent
`0112` by changing the third displayed site (physical site `4`) from colour
`1` to colour `0`.  Suppose a source-labelled selected section and central
cone exist in the required totalization:

\[
             d\epsilon_{0102}=b_{0102},
 \qquad      d\theta=F=(H_0-u)e_{Eq}.                 \tag{4}
\]

Both generators are odd in the Koszul presentation.  Their literal product
has differential

\[
 \boxed{
 d(\epsilon_{0102}\wedge\theta)
   =b_{0102}\theta-\epsilon_{0102}(H_0-u)e_{Eq}. }
 \tag{5}
\]

Let `v` be the four-corner occurrence coefficient of `b_0102 theta`.  The
first term of (5) is the private/lower face, so

\[
                              B=v.                    \tag{6}
\]

The algebraic coefficient of the second face is `-v`.  The physical
reduced-`Eq` boundary coordinate is oriented oppositely to that second-face
coefficient.  This is not a new convention: it is the pinned convention in
which the physical `K_Eq` dressing has

```text
(lower/private, Eq, word-resolved ores)=(+E,+E,-E).
```

Consequently

\[
                              Eq=-(-v)=v.              \tag{7}
\]

Equations (6)--(7), rather than their sum, give

\[
        \chi(d\kappa_{0102})
          =\delta\cdot(B-Eq)=0,
 \qquad \lambda_{0102}={\chi\over4}=0.               \tag{8}
\]

Applying `d` again produces `+b_0102 F` from the first term and
`-b_0102 F` from the second, so `d^2=0`.  That cancellation is a check on
(5); it is not the reason (8) holds.  The reason is that the two occurrence
coefficients in the strict Leibniz formula are literally the same `v`.

The checker verifies this coefficientwise on the four corner units, all
four shore-gauged `DQ/PS` signless edges, and `delta`.  Thus the result is
independent of which root-labelled cross-shore face is the proper face of
the representative cell.

## 2. Why the earlier `d^2` freedom remains correct

The older counterguard considered an abstract mixed filler with boundary

\[
                       d\kappa=(z,a),                 \tag{9}
\]

where `z=(1,-1,1,-1)` is the oriented mapping-square cycle and `a` is an
arbitrary terminal `B/Eq` augmentation.  The terminal block has zero
outgoing differential, so `d^2=0` imposes no condition on `a`.

There is no conflict with (1).  Equation (1) adds the stronger statement
that the mixed filler is a particular product in a physical DGA/module.
The derivation law computes its complete boundary and chooses

\[
                         a_{\rm std}=(v,v).            \tag{10}
\]

Equation (9), by contrast, permits replacing (10) by

\[
                         a_{\rm std}+\lambda(\delta,0).
 \tag{11}
\]

Both (10) and (11) obey `d^2=0`; only (10) is the normalized strict product.
Thus the exact logical hierarchy is

```text
four objectwise edges                    -> closed square debt z
derived-square existence                 -> some filler kappa
strict physical multiplicative product   -> the particular filler with lambda=0.
```

## 3. Full augmented conservation does not select the product

Modulo the old cap image, every possible terminal augmentation has the
unique normal form

\[
                         \lambda(\delta,0).            \tag{12}
\]

The old cap image has rank seven in the eight-dimensional `B/Eq` block and
is exactly the kernel of `Psi=delta.(B-Eq)/4`.  Every presently named
augmented row is invisible to `Psi`:

```text
target, W, ordinary and labelled residue,
M, anchor/ainc, physical q=M-ainc,
P_f, primitive cap, ridge, eta, sigma.
```

Adding (12) changes none of those coordinates.  The four Gate-I near-hits
and their shore gauge also remain tied `B=Eq`; their missing correction is
precisely the same unconstructed mixed incidence.  They therefore do not
supply an independent conservation equation for `lambda`.

In particular `sum(delta)=0`, so the balanced twist has zero total private
and `Eq` augmentation and does not disturb the scalar anchor or
`q=M-ainc` conservation law.

It follows that no combination of the currently available augmented rows
forces zero or a nonzero value.  They are compatible with the standard
choice `lambda=0`, but do not certify that the physical source chose it.

## 4. All eight instances without illicit symmetry transport

The eight literal lower words are the one-site ternary neighbours of
`0112`:

```text
0012, 0102, 0110, 0111, 0122, 0212, 1112, 2112.
```

The marked fixed packet has no nontrivial strict stabilizer, so (8) cannot
be transported from `0102` to the other seven by the coarse `V4` word
symmetry.  Instead, a source-provenant conclusion must instantiate the same
multiplicative construction separately at every labelled object:

\[
 d(\epsilon_w\wedge\theta)
     =b_w\theta-\epsilon_wF,
 \qquad
 w\in\{0012,0102,0110,0111,0122,0212,1112,2112\}.     \tag{13}
\]

If one physical natural schema supplies (13) over the full labelled
one-root groupoid, then the argument (6)--(8) applies independently eight
times and gives

\[
               \boxed{\lambda_{0012}=\cdots=\lambda_{2112}=0.} \tag{14}
\]

Without that schema, the eight values remain independent.  The existing
symmetry audit neither identifies nor negates them.

## 5. Minimum additional physical input

There are two equivalent strengths at the selected projection.

The weakest determining row, one instance at a time, is (3).  Since
`lambda_i=delta.(B-Eq)/4`, this single scalar equality forces exactly
`lambda_i=0` and says nothing unnecessary about target or ridge coordinates.

The source-meaningful theorem is stronger but more natural:

> **Physical mixed-product normalization.**  The source-labelled selected
> response/occurrence section is a normalized module/DGA map over the
> physical central reduced-`Eq` cone.  Its response-to-`AugP2` mixed cell is
> the literal product `epsilon_i wedge theta`; its differential is the
> strict Leibniz boundary (5), with no additional closed balanced `B/Eq`
> augmentation.  This holds naturally at all eight labelled one-root
> objects and with their cap, `q`/anchor, `W`, residue, and ridge faces.

This one schema proves (14).  It also makes clear what has not been proved:
the physical selected sections `epsilon_i`, the physical central `theta`,
and their placement through the response, cap, and E14 word/fine/repeated
summands are still missing.

If instead a fixed nonzero value `c` is desired, the minimum row must
explicitly prescribe

\[
                         \delta\cdot(B-Eq)=4c.         \tag{15}
\]

No existing naturality or conservation identity provides such a right-hand
side.  In particular, the canonical literal product predicts zero, not a
primitive bright value.

## Consequence for the terminal fork

Combining the source-operation census with this calculation gives a sharp
conditional terminal theorem:

```text
canonical literal grammar + physical mixed-product normalization
    -> every degree-one generator is Psi-dark
    -> the balanced Psi/4 covector survives the full grammar image.
```

This is not yet an accepted physical terminal because the normalization
theorem itself is the missing source comparison.  Conversely, any physical
construction with `lambda_i != 0` must exhibit precisely the extra balanced
terminal cocycle in (2); it cannot be attributed to the standard
mapping-cone signs or to augmented conservation.

## Scope and verification

This is exact for the canonical rational `h=3` chain calculation with full
literal lower-word separation.  It computes the standard product value and
the complete one-dimensional twist freedom.  It does not construct an exact
finite full GHZ tensor, prove pure-target normalization or all mixed output
words, establish the physical multiplicative comparison, or transport the
result uniformly in `h`.

Run:

```text
python3 computations/verify_h3_kappa_lambda_literal_mapping_cone_normalization_gate.py
python3 computations/verify_h3_kappa_lambda_literal_mapping_cone_normalization_gate.py --mode representative
python3 computations/verify_h3_kappa_lambda_literal_mapping_cone_normalization_gate.py --mode counterguard
python3 -O computations/verify_h3_kappa_lambda_literal_mapping_cone_normalization_gate.py
python3 -I -S computations/verify_h3_kappa_lambda_literal_mapping_cone_normalization_gate.py
```

Frozen ledger SHA-256:

```text
c299de723884e3b9f8053322cd2d8edf8cb016eb767e99c34e59485ce8e308cc
```
