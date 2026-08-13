# The physical cubic endpoint projector reduces to one primitive cap cell

## Outcome

At intrinsic response order three, the matching/endpoint association
projector is exact on the ninety occurrence coefficients.  The endpoint
adjacency has constant eigenvalue `8` and nonconstant eigenvalues

```text
-2, 2, 4.
```

Consequently

\[
 P(B)=(B+2I)(B-2I)(B-4I),\qquad P(8)=240.              \tag{1}
\]

Here the endpoint-scheme parameter is `h=2`, because its occurrence set is
the *next* intrinsic response order `h+1=3`, with six selected sites and
`N_3=90`.  The residual-matching projector is `(A+I)/3`, so the combined coefficient
denominator is `720`.  This solves the association algebra, not its physical
source descent.  A source-valid lift of (1) must totalize the endpoint
Cartan product-rule faces, the pairwise second-Hasse faces, the mixed
endpoint/matching faces, and the cubic third-Hasse face.

After projection to the already computed physical word/ridge cap complex,
Cartan closes the saturated rank-four sum-zero lattice.  The only remaining
projected class is one primitive reduced companion

\[
 \boxed{p_{v,N}:\quad Q_{v,N}=-1,\qquad
                     \operatorname {ores}=-1}          \tag{2}
\]

with `Omega`, rootless ridge, `Eq`, `W`, target, anchor incidence, eta, and
sigma zero.  Thus (2), together with the four forced totalization face
families, is the smallest physical source extension behind the cubic
projector.  No such cell is in the current inventory.

Checker:
[verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py](../computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py).

## 1. Why the association calculation reaches the cap gate

The centered occurrence class is

\[
                  c_f=90e_f-\sum_{M=1}^{90}e_M.         \tag{3}
\]

The normalized coefficient projector produces (3), but the raw centered
Euler operation has scalar zero-face

\[
                              90f(x).                   \tag{4}
\]

Equation (4) is not optional: at a normalized trapped source with `f=1`
and complete response zero, it evaluates to `90`.  A physical lift must
therefore carry (4) through its lower Hasse faces rather than discard it.

The source-faithful endpoint bars in that lower packet have boundary

\[
                b_{v,N}=-\Omega_v+Q_{v,N}.              \tag{5}
\]

For five deleted faces and three matchings per face, the cokernel of (5) is
free of rank five, detected by

\[
             \lambda_v=\Omega_v+\sum_NQ_{v,N}.          \tag{6}
\]

The physical Cartan orbit spans the saturated lattice
`ker(sum:Z^5 -> Z)`.  Hence every standard component of the cap face can be
transported away.  A single column with nonzero sum completes the quotient;
the local choice (2) has sum `-1`, so it is primitive integrally.

This is the precise sense in which (2) is the cap shadow of the association
projector.  It is not yet an equality of physical chains: constructing the
augmented lift which sends (4) into (5)--(6) is the missing theorem.

### Incidence/Čech factorization

There is a useful economical factorization of the endpoint cubic.  On the
thirty ordered distinct endpoint pairs, let

```text
U_tail f(p)=sum_(s!=p) f(p,s),
U_head f(s)=sum_(p!=s) f(p,s).
```

Then exactly

\[
 B+2I=U_{\rm tail}^*U_{\rm tail}
       +U_{\rm head}^*U_{\rm head}=:C.                 \tag{7}
\]

The incidence map has rank `11`, and at six sites

\[
                 C(C-4I)(C-6I)=8J_{30}.                \tag{8}
\]

Thus the cubic coefficient projector can indeed be organized as an
incidence/Čech push-pull instead of three unrelated Cartan powers.  This
does not solve the source lift.  An ordinary Čech or group-bar differential
has image `ker(sum)` on its vertices.  Every column of the right side of
(8) has mass `240`, so it is the surviving `H_0` base class, not an
orientation/top boundary.  After physical cap projection, (2) is exactly
the corresponding missing base augmentation.

The same point rules out the diagonal finite-group shortcut.  The endpoint
adjacency is a double-coset/right-incidence correspondence, whereas physical
site symmetry acts diagonally on the complete polynomial.  A rational
Maschke splitting contracts positive group homology, but its bar boundaries
still have coefficient augmentation zero.  It neither turns an individual
marked occurrence into a source equation nor maps the orientation line to
(2).

## 2. Smallest word and multidegree

The local reduced cell must use the same labelled companion as its endpoint
bar.  Its full source word is

```text
01211222
```

and deleting the exposed `x=0` gives the rootless word `1211222`.  The first
common fine degree is

```text
Q_(v,N)=t*q_(v,N),  odd-site type P3+K2.
```

The first scalar Hasse candidate has directions

```text
{q_xv:0m_v, q_pq:22} + N,
```

external/internal order `(2,2)` and total principal-parts order four.  The
corresponding complete literal source component has target weight `14` and
seven-edge boundaries.  The first cyclic homogeneous top has target weight
`18` and nine-edge boundaries.

Thus a local seven-occurrence relative total cell in the labelled repeated
`P3+K2` grade is the first possible source object.  The degree-five cyclic
packaging is coherence for its five translates; it is not a substitute for
the primitive local cell.

## 3. Why the three tempting constructions fail

### Target-normalized unary/response product

The formal half-sum of the Hasse tail and target-normalized unary row has the
desired coarse signature.  It is not source-valid.  The selected fourth
operator reads `1` on the mixed Hasse tail and `0` on both the unary row and
every honest adjacent edge, so the half-sum retains value `1/2`.  Its source
words are also distinct:

```text
mixed 01211222, zero-endpoint chart 00211200, unary 00000000.
```

Polynomial multiplication homogenizes degrees but does not change these
word labels.

### Degree-five Tate top or determinant line

The normalized `C5` Tate top has boundary equal to the sum of the five edge
generators.  Its face image is zero, not the aggregate cap vector.  Likewise
the natural order-forgetting map from the alternating seven-occurrence line
to the ordinary cap module is zero: an adjacent occurrence transposition
acts by `-1` on the source and trivially on the target, imposing `2p_v=0`.

An orientation-twisted physical comparison could escape this argument, but
it would be a new relative cell with its action and readouts specified.  The
ordinary Tate/determinant line does not construct (2).

### Relative Spencer/Chevalley--Eilenberg attempt

Let `w` be the simultaneous root/Weyl move and `s` the endpoint swap.  The
target-safe physical Cartan prism is the odd combination

\[
                         (1-s)H_w.                     \tag{9}
\]

On the four orbit corners `1,w,s,sw`, its boundary is

```text
(-1,+1,+1,-1).
```

It has face augmentation zero.  The endpoint-even companion

\[
                         (1+s)H_w                      \tag{10}
\]

also has augmentation zero, and it is not target-safe:

\[
                (1+s)(w-1)\Delta=2(w-1)\Delta.         \tag{11}
\]

This exposes the exact target-normal obstruction.  In the smallest rows
`(Eq,w,target,ores)`, the old target row, cap target, and ordinary response
have rank three.  The target-zero invisible `w` face raises the rank to four
and is detected by `(1,1,1,-1)` at `Y=1`.  Therefore a target-normal
Koszul correction of (10) still requires one primitive source-normal
attachment.

The CE differential cannot supply it automatically.  Its action/bracket
faces are relative differences and remain in the augmentation-zero image.
The cubic orientation/top face is consequently a relation among standard
faces—the same phenomenon as the degree-five Tate top—not the primitive
base cell (2).

### Complete full-nine rows and chart copies

The complete literal search is already exhaustive in the first two relevant
multidegrees:

```text
five weight-14 components : 288 columns / rank 288 each
weight-18 component       : 4266 columns / rank 4266
natural Tate map           : 1440 -> 1201, kernel 239.
```

Every one-chart component is injective.  Every natural Tate-kernel vector
has zero anchor/target/`W`/ordinary-residue incidence, and the two-chart
kernels are only identical-column chart differences.  They cannot supply a
primitive value of (6).

## 4. Exact positive construction target

The minimal theorem is:

> Construct one source-valid seven-occurrence relative total cell in word
> `01211222` and the labelled repeated `P3+K2` grade.  Its normalized scalar
> face is `90f`; its cap face has primitive `epsilon=+/-1`; its reduced
> companion is (2); and every endpoint, pairwise-Hasse, mixed
> endpoint/matching, cubic-Hasse, word, ridge, `Eq`, `W`, target, anchor,
> physical-`q`, ordinary-residue, eta, and sigma face is either the specified
> packet or a committed physical boundary.

The `C5` Cartan orbit then supplies all face translates and kills their
standard differences.  This is one new source family, not five independent
conjecture-level statements.

The alternative is a covector extending
`epsilon=sum_v lambda_v` through the full physical codomain.  Current eta
compensation is only numerical; no pullback through the 360-feature plus
terminal comparison has been constructed.  Therefore `epsilon` is not yet
a physical terminal.

## 5. Relation to the earlier relative-cap/Tor obstruction

The primitive reduced endpoint (2) and the invisible lift `n_c` from the
derived-base-change cap audit are tightly coupled, but they are not the same
generator.  Normalize the selected labelled cap row `Q` to one and use rows

```text
(Q-boundary, target, ordinary residue).
```

Then

```text
p = (-1,0,-1),
n = (+1,0, 0),
n+p = (0,0,-1).
```

After a source-labelled reset identifies `Q` with `kappa*Y*w`, this reads

\[
 p=-\kappa Y\rho,\qquad
 dn=+\kappa Yw,\quad \operatorname {tgt}(n)
 =\operatorname {ores}(n)=0.                           \tag{12}
\]

Thus `p` is the relative obstruction endpoint, while `n` is the positive
invisible transgression which lifts it; their sum is the desired closed
residue carrier.  Calling `p=n` loses both a sign and the ordinary-residue
row.

This means the existing Tor/transgression framework should be reused.  The
first cross-word candidate for `n` is already known: the degree-four
two-row Koszul cell comparing words `01211222` and `00000000`.  It is an
exact upstairs syzygy, but its reset has five nonzero internal quadratic
denominator faces.  The remaining construction is therefore one higher
reset syzygy/nullhomotopy of those five faces.  An abstract new cubic CE top
would only rename this obligation.

## 6. Relation to the uniform transfer

This cap cell is necessary local input to the proposed uniform
`Tr_h`, but it is not the whole transfer theorem.  `Tr_h` must also be
boundary-independent, land in the clean-line representation, remain
nonzero, and satisfy every common Hankel shift.

Uniformity cannot be obtained by multiplying the h=3 cell by a spectator
matching tail: the Leibniz term `d(q^[h-3])` is nonzero.  The positive
uniform form must make the new cap family a module over the spectator Hasse
coalgebra and totalize all spectator faces with physical GHZ, `q`, and
Macaulay descent.

## Verification

Run:

```text
python3 computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py
python3 -O computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py
python3 -I -S computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py
```

Frozen ledger SHA-256:

```text
1256327676e3a78fd10d121f0af78e52d249e5e57f6633587ab33818c224cd6c
```
