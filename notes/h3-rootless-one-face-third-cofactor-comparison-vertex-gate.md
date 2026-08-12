# The one-face third-cofactor tail is formally perfect but does not descend

## The coarse half-sum

Fix face \(v=1\), the selected complement matching

\[
                         N=23\mid45,
\]

and the physical mixed word `01211222`.  The marked four-cube uses

\[
 a_{67}^{22},\quad a_{01}^{01},\quad
 a_{23}^{21},\quad a_{45}^{12}.                       \tag{1}
\]

The genuine third cofactor is the scalar top

\[
 \Psi_I(H_m)=
 \partial_{a_{67}^{22},a_{01}^{01},a_{23}^{21},a_{45}^{12}}H_m=1. \tag{2}
\]

Its complete proper-face Hasse tail has coarse rows

\[
 C_{m rel}^{\rm Hasse}=(-1,-1,0,0,0),               \tag{3}
\]

in the order
\((\operatorname{low},\operatorname{ainc},W,
\operatorname{tgt},\operatorname{ores})\).  The target-normalized unary
lift of `c094bbb` is

\[
                         x=(1,-1,0,0,0).               \tag{4}
\]

Therefore, after forgetting source word, Hasse degree, and descent,

\[
 {1\over2}\left(x+C_{m rel}^{\rm Hasse}\right)
                         =(0,-1,0,0,0).                \tag{5}
\]

So there is no remaining coarse sign or target/cap obstruction.  Equation
(5) is the strongest formal candidate for the one comparison vertex.

## The source unit survives unchanged

The same selected operator in (2) kills the pure unary equation underlying
\(x\), because its decorated variables do not occur in that word:

\[
                         \Psi_I(H_0-u)=0.              \tag{6}
\]

Every honest adjacent source square also has zero connecting value.  Hence
the candidate (5) has

\[
                         \Psi_I={1\over2}\ne0.         \tag{7}
\]

It sends the zero class of \(H_m\) to a unit and cannot descend to a
nonempty physical source quotient.  Adding \(x\), a cap, or one adjacent
edge does not alter (7).  This is already a one-face obstruction; no cyclic
averaging is involved.

## The endpoint ridge is transferred, not killed

The zero-endpoint chart has word `00211200` and marked cells

\[
 a_{67}^{00},\quad a_{01}^{00},\quad
 a_{23}^{21},\quad a_{45}^{12}.
\]

The two internal ridges agree, but the endpoint ridges leave

\[
 \Omega_1=(a_{67}^{22}-a_{67}^{00})
          -(a_{01}^{01}-a_{01}^{00}).                 \tag{8}
\]

Even grant the clean adjacent comparison edge from face \(1\) to face
\(3\).  In rows \((\Omega_1,r_1,\Omega_3,r_3)\), it is

\[
 C_1-C_3=(1,-1,-1,1).                                 \tag{9}
\]

The candidate ridge is \((1,0,0,0)\).  Its \(\Omega_1\)-entry forces
coefficient \(-1\) on (9), leaving

\[
                         (0,1,1,-1).                  \tag{10}
\]

Thus one edge only transfers the endpoint defect to face \(3\) and leaves
the rootless difference \(r_1-r_3\).  The literal physical edge also has
its known pure-Eq defect, so (10) is the most favorable possible quotient.

Using the complete local-colour bar instead of (9) does kill (8), but its
literal column is

\[
                 -\Omega_1+q_{1,N},\qquad
                 q_{1,N}=a_{23}^{21}a_{45}^{12}.       \tag{11}
\]

The primitive all-derivation companion in (11) is the already certified
five-ridge cokernel, not a clean comparison vertex.

## Fine degree and word

The marked cube (1) is a squarefree \(4K_2\): every physical site occurs
once.  The adjacent first-Tor comparison has internal type \(P_3\sqcup
K_2\), with odd-site profile

\[
                         (1,2,1,1,1).                 \tag{12}

Polynomial multipliers can homogenize their cell multidegrees.  For
example, multiplying the selected internal matching \(bd\) by \(ace\)
reaches \(abcde\), and multiplying \(x\) by the two endpoint cells reaches
the same cell profile.  This does not change the source equation basis:

\[
 H_m:\ `01211222`,\qquad
 H_{\rm chart}:\ `00211200`,\qquad
 H_0:\ `00000000`.                                   \tag{13}
\]

Hence multiplication/localization does not repair (6)--(8).  A positive
construction needs an actual source-labelled word-change/comparison cell,
not another coefficient multiplier.

## Exact remaining datum

The one-vertex gate is now precise.  It requires a cell in one repeated
\(P_3\sqcup K_2\) component that simultaneously

1. kills the selected-fourth-operator connecting class (7);
2. kills \(\Omega_1\) rather than transferring it to an adjacent face;
3. retains and cancels the all-derivation companion (11); and
4. maps the mixed source word to the physical rootless comparison sector
   with zero target, residue, and unwanted anchor readouts.

The formal Hasse tail plus \(x\) satisfies only the coarse signature.  This
is not an all-resolution no-go; it identifies the first literal word/degree
attachment required for one comparison vertex.

Run:

```text
python3 computations/verify_h3_rootless_one_face_third_cofactor_comparison_vertex_gate.py
python3 -O computations/verify_h3_rootless_one_face_third_cofactor_comparison_vertex_gate.py
python3 -I -S computations/verify_h3_rootless_one_face_third_cofactor_comparison_vertex_gate.py
```

Frozen ledger SHA-256:

```text
21ad8ab579d066f20260df7e7a93dadabd72133a5e16ebe81e70d777465d7f7f
```
