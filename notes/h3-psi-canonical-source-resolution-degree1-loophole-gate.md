# Canonical source syzygies do not close the relative degree-one census

## Verdict

The fixed `Gamma_*` source grammar has two different meanings which must not
be conflated.

1. The complete coefficient-equation/Macaulay/Koszul--principal-parts
   presentation can be chosen canonically.  At fixed grade it is finite, and
   its free resolution is exhaustive for the module it presents.
2. The complete **physical augmented comparison** grammar is larger.  It
   contains response-to-cap, operation-changing mapping-cone data which is
   not generated merely by resolving the coefficient equations.

For the first grammar, the higher-syzygy concern is completely settled.  If

\[
 \cdots\longrightarrow C_2
 \mathop{\longrightarrow}^{d_2}C_1
 \mathop{\longrightarrow}^{d_1}C_0                 \tag{1}
\]

is the canonical fixed-grade resolution, then

\[
 d_1d_2=0,\qquad \operatorname {im}d_2\subseteq\ker d_1. \tag{2}
\]

Every still higher differential resolves a kernel upstream.  It cannot add
a column to `d1`, enlarge `im(d1)`, or change whether

\[
 \chi=\delta\cdot(B-Eq),\qquad \delta=(1,1,-1,-1),     \tag{3}
\]

annihilates `im(d1)`.  This remains true for a nonminimal resolution with
arbitrarily many redundant syzygies.

The obstruction left by `629bf8c` is therefore not an ordinary higher
syzygy.  It is a new **relative total-degree-one** generator: a primitive
physical comparison, or a higher source cell shifted into degree one by a
mapping cone/desuspension, whose canonical coefficient/PP shadow may be
zero while its physical `B/Eq` boundary is nonzero.

The eight `kappa_i` are the known instances of exactly this phenomenon.
Choosing a canonical coefficient resolution does not prove that they span
the full relative degree-one quotient.  The precise missing theorem is

\[
 \boxed{
 C^{\rm phys}_{1,\Gamma_*}/
 \bigl(C^{\rm can}_{1,\Gamma_*}+C^{\chi\text{-dark}}_{1,\Gamma_*}\bigr)
   =\langle\kappa_0,\ldots,\kappa_7\rangle.}          \tag{4}
\]

Without (4), an additional primitive `epsilon` with zero canonical shadow
and

\[
 \Pi_{B/Eq}(d\epsilon)=(\delta,0)                     \tag{5}
\]

is not excluded.  It raises the projected rank from seven to eight and has
normalized `Psi=1`.  The checker gives the smallest exact augmented grammar
extension satisfying `d^2=0`, all-zero external rows, and `q=M-ainc`; it is
a logical counterguard, not an asserted physical GHZ cell.

Thus the strongest current result is:

```text
ordinary higher source syzygies                 closed;
declared coefficient/Macaulay/PP grammar        canonically exhaustive;
essential surjectivity onto physical relative C1 open;
only-eight-kappa theorem                         open;
accepted q/Fredholm promotion                    open with the same comparison.
```

Exact checker:
[`verify_h3_psi_canonical_source_resolution_degree1_loophole_gate.py`](../computations/verify_h3_psi_canonical_source_resolution_degree1_loophole_gate.py).

## 1. The canonical fixed-grade presentation

Fix the literal output grade

```text
word        01211222
fine        t*q_(v,N) at the selected six occurrences
repeated    P3+K2
operation   AugP2 cap / mixed orbit
window      2345 with occurrence labels.
```

Call it `Gamma_*`.  Start with the complete, labelled coefficient equations.
The degree-three Macaulay part has only the four relation/multiplier degree
splits

\[
                   (0,3),(1,2),(2,1),(3,0).           \tag{6}
\]

Adjoin the declared Koszul, PP, Hasse, and operation-labelled comparison
atoms whose output has grade `Gamma_*`.  Let `C1_can,Gamma*` be the free
module on every such literal instance and let `d1` be its complete augmented
boundary.  Then recursively choose

```text
C2 free on homogeneous generators of ker(d1),
C3 free on homogeneous generators of ker(d2),
...
```

or use any equivalent Schreyer/Tate construction.  This is an exhaustive
free resolution of the **declared** presentation.  Hasse coproduct and
Koszul identities guarantee that polynomial prolongation and product-rule
faces remain inside it.

This construction is useful because it removes an illusory infinite search:
after `d1` is fixed, no decision about (3) depends on how the higher kernels
are resolved.  It is also presentation-independent in the needed sense.  A
nonminimal resolution can add redundant `C2,C3,...` generators, but their
composite output in `C0` is zero by (2).

The checker freezes this on the actual projected cap matrix.  The eight old
cap columns have rank seven in the eight `B/Eq` coordinates.  Granting eight
dark `kappa` placeholders gives

```text
C1 generators       16
rank d1               7
dim ker d1             9.
```

It then uses eleven deliberately redundant `C2` generators of rank nine.
Their two relations are resolved by `C3`.  Exact multiplication gives

```text
d1*d2 = 0,
d2*d3 = 0,
rank im(d1) after every higher composite = 7,
chi on every d1 output = 0.
```

This is a finite stress test of the structural proof, not the source of the
proof: equations (1)--(2) hold in every resolution length.

## 2. Why this does not exhaust the physical grammar

The canonical construction presents the coefficient ideal together with the
comparison atoms one elected to declare.  It cannot prove that every
physical operation-changing comparison has been elected.  In particular,
the response-to-`AugP2` square is not an ordinary syzygy among complete
coefficient rows.  It is a comparison between two differently labelled
presentations and carries new physical target, residue, anchor, `q`, `W`,
ridge, eta, and sigma data.

This point is already visible in the eight `kappa_i`.  Their source square
boundary can be fixed while their cap augmentation remains

\[
 \Pi_{B/Eq}(d\kappa_i)
   \equiv\lambda_i(\delta,0)
       \pmod {\operatorname {im}d_1^{\rm old}}.        \tag{7}
\]

Ordinary `d^2` puts no condition on `lambda_i`.  Thus `kappa_i` cannot be
recovered merely by taking more syzygies of the old cap matrix.  It must be
included as relative comparison data, with its physical augmentation
computed separately.

The same logic applies to a possible ninth primitive comparison.  Let the
forgetful map retain the canonical coefficient/PP source shadow but forget
the augmented comparison output.  There are two exact extensions with the
same zero shadow:

```text
dark epsilon    B/Eq=0,          all external rows=0;
bright epsilon  B/Eq=(delta,0),  all external rows=0.
```

Both obey

```text
M=ainc=q=0,  hence q=M-ainc,
target=W=ores=ridge=eta=sigma=anchor=0.
```

The dark extension has `Psi=0`; the bright extension has `Psi=1` and raises
rank `7 -> 8`.  Adding either extension does not alter any canonical source
equation or higher syzygy.  Therefore those data cannot decide which physical
relative `C1` generators exist.

The bright extension is not claimed to be source-provenant.  Its purpose is
logical and exact: it identifies the one missing premise needed to exclude
it, namely the essential-surjectivity/generation statement (4).  Saying
“choose the canonical presentation” silently assumes that premise rather
than proving it.

## 3. Higher cells versus cone shifts

In an ordinary first-quadrant bicomplex, total degree one contains only

\[
                         (1,0)\quad\text{and}\quad(0,1). \tag{8}
\]

A resolution syzygy of degree at least two cannot enter the total `C1`
map.  A mapping cone can shift an old `C2` class down by one and place it in
total degree one.  That does not contradict Section 1: after the shift it is
a **new relative `C1` generator**, with a new boundary that must appear in
the `Gamma_*` degree-one census.

This gives the exact classification of the “higher-cell loophole”:

```text
unshifted C2,C3,... of the canonical resolution
    -> relations only; no new chi image;

cone-shifted/desuspended cell with a physical comparison output
    -> new total-degree-one atom; must be one of the kappa_i or added to (4).
```

There is no residual ambiguity from arbitrarily high ordinary syzygies.
There is one bounded relative-degree-one generation question.

## 4. Physical `q` and Fredholm promotion

Extending `Psi=delta.(B-Eq)/4` by zero on `M`, `ainc`, and `q` is compatible
with the exact row law

\[
                             q=M-ainc.                 \tag{9}
\]

Compatibility is not promotion.  The resulting covector neither detects a
physical `q` kernel generator nor identifies the selected balanced face with
the literal final source candidate.  The pinned full known-row dual has this
same property: physical `q` and anchor do not obstruct its local extension,
but they do not make it an accepted separator.

The Fredholm conclusion is valid only after one map and one vector are fixed:

\[
 J_{\rm phys,\Gamma_*}:C^{\rm phys}_{1,\Gamma_*}\longrightarrow
 Y^{\rm phys}_{\Gamma_*},
 \qquad b_{\rm phys}\in Y^{\rm phys}_{\Gamma_*}.       \tag{10}
\]

The codomain must retain every private `B`, reduced `Eq`, target, `W`,
ordinary and labelled residue, `M`, anchor incidence, physical `q`, ridge,
eta, sigma, and protected terminal row.  Once (4), the eight equations
`lambda_i=0`, and the literal comparison identifying `b_phys` are proved,

\[
 \widetilde\Psi J_{\rm phys,\Gamma_*}=0,
 \qquad \widetilde\Psi(b_{\rm phys})=1               \tag{11}
\]

is an accepted finite Macaulay/Fredholm terminal.  If an admitted generator
has nonzero `Psi`, it instead raises the rank and is the physical filler
candidate.  Exact image/cokernel duality then leaves no third branch.

The canonical coefficient resolution supplies neither the relative domain
in (10) nor the physical comparison identifying `b_phys`.  Consequently it
cannot prove (11) by itself.

## 5. Sharp remaining theorem

The global `Gamma_*` problem is now precisely:

> **Relative degree-one exhaustiveness.**  Every primitive or cone-shifted
> physical source generator whose total differential has a `Gamma_*` face
> is, modulo the canonical coefficient/Macaulay/Koszul--PP image and
> `chi`-dark generators, a linear combination of the eight source-labelled
> `kappa_i`.  The comparison retains the complete physical augmented rows
> and identifies the balanced vector with the literal terminal RHS.

Under this theorem, only the eight scalars `lambda_i` matter and ordinary
higher resolutions never re-enter.  Without it, the exact exotic generator
(5) is the unavoidable loophole.

This statement is distinct from symmetry and localization.  No group orbit,
Maschke contraction, support open, denominator, or saturation is used.  It is
solely a theorem about essential surjectivity of one fixed-grade presentation
onto the physical relative degree-one comparison module.

## Scope and verification

This note proves the resolution-theoretic statement and gives the smallest
augmented grammar counterguard.  It does not assert that `epsilon` is an
actual physical cell, construct a complete GHZ source, prove or refute the
eight `lambda_i=0` equations, or promote a local covector before the physical
map (10) is supplied.

Run

```text
python3 computations/verify_h3_psi_canonical_source_resolution_degree1_loophole_gate.py
python3 -O computations/verify_h3_psi_canonical_source_resolution_degree1_loophole_gate.py
python3 -I -S computations/verify_h3_psi_canonical_source_resolution_degree1_loophole_gate.py
```

The checker pins the `629bf8c` source-grade frontier, the mixed-cell
augmentation freedom, the absolute-resolution exhaustivity theorem, the
Hasse coproduct totalization, and the full known-row `q`/terminal separation.
It verifies the canonical rank-seven `d1`, redundant `C2/C3` resolution,
zero higher composite image, primitive exotic rank jump, exact `q=M-ainc`
compatibility, and normalized `Psi` values.

Frozen ledger SHA-256:

```text
6741838df9c2c3e8d9ac5965853240d0004241d72db5422d9727ee338e0ad26f
```
