# Centered restriction is exact but retains a lower centered carrier

## Outcome

There is an exact, uniform restriction--insertion law for the centered
occurrence projector.  It gives the coefficient shadow of the desired
oriented four-cut map and also exposes its first unavoidable obstruction.

Let \(\Omega_r(V)\) be the occurrence set on \(|V|=2r\) sites:

\[
 \Omega_r(V)=\{(p,s,R):p\ne s,\ R\text{ a perfect matching of }
                         V\setminus\{p,s\}\},
\]

and put

\[
 N_r=|\Omega_r|=2r(2r-1)(2r-3)!!,
 \qquad c_{f,r}=N_re_f-{\bf1}_r.                       \tag{1}
\]

For a site edge \(e\), let \(D_e\) keep the occurrences in which \(e\)
is a residual matching edge and delete \(e\).  Let \(I_e\) reinsert it.
Then

\[
                     D_e{\bf1}_r={\bf1}_{r-1},
 \qquad
 {1\over r-1}\sum_e I_eD_e=1.                         \tag{2}
\]

Thus restriction followed by insertion reconstructs every coefficient
family exactly; no support search is involved.  But on a centered marked
class the component formula is

\[
 D_ec_{f,r}=\begin{cases}
 \alpha_r c_{f/e,r-1}+(\alpha_r-1){\bf1}_{r-1},
       &e\in R_f,\\[2mm]
 -{\bf1}_{r-1},&e\notin R_f,
 \end{cases}
 \qquad
 \alpha_r={N_r\over N_{r-1}}={r(2r-1)\over r-1}.       \tag{3}
\]

At \(r=3\), \(N_3=90\), \(N_2=12\), and

\[
 D_ec_{f,3}=\begin{cases}
 {15\over2}c_{f/e,2}+{13\over2}{\bf1}_2,&e\in R_f,\\
 -{\bf1}_2,&e\notin R_f.
 \end{cases}                                           \tag{4}
\]

There are exactly two marked residual edges.  On either marked component,
the primitive coordinate difference
\(e_{f/e}^*-e_g^*\) kills the constant carrier and reads \(90\) on
\(D_ec_{f,3}\).  Therefore the endpoint projector cannot be sent to copies
of one common \(H_0\) merely by restriction and common-tail insertion.  A
physical chain map must fill the two lower centered classes and transport
the component constants through one complete word/fine/repeated-grade
base-change.

Companion checker:
[verify_uniform_centered_occurrence_restriction_insertion_gate.py](../computations/verify_uniform_centered_occurrence_restriction_insertion_gate.py).

## 1. Proof of the restriction law

Fix \(e\subset V\).  Adding \(e\) is a bijection

\[
 \Omega_{r-1}(V\setminus e)
 \longleftrightarrow
 \{(p,s,R)\in\Omega_r(V):e\in R\}.                    \tag{5}
\]

This proves the first identity in (2).  Every occurrence contains exactly
\(r-1\) residual matching edges, proving the second identity.

Apply \(D_e\) to \(c_{f,r}=N_re_f-{\bf1}_r\).  If \(e\notin R_f\), the
marked term disappears and the result is \(-{\bf1}_{r-1}\).  If
\(e\in R_f\),

\[
 D_ec_{f,r}=N_re_{f/e}-{\bf1}_{r-1}.                   \tag{6}
\]

Using

\[
 {N_r\over N_{r-1}}
 ={2r(2r-1)(2r-3)!!
    \over2(r-1)(2r-3)(2r-5)!!}
 ={r(2r-1)\over r-1}                                  \tag{7}
\]

in (6) gives (3).  The proof is uniform and integral before the harmless
normalization by \(N_{r-1}\).

The primitive dual assertion is equally direct.  Choose any lower
occurrence \(g\ne f/e\).  The covector
\(e_{f/e}^*-e_g^*\) kills \({\bf1}_{r-1}\), while

\[
 (e_{f/e}^*-e_g^*)D_ec_{f,r}=N_r.                     \tag{8}
\]

Thus the lower centered summand is not a normalization artifact.

## 2. Relation to the oriented four-cut action

Formula (2) is the underlying incidence identity for an oriented
restriction--replacement operator.  On the residual \(q\)-tail sector,
replace \(I_e\) by insertion of the corresponding oriented curvature
coefficient \(K_e^\rightarrow\) or \(K_e^\leftarrow\).  The normalized sum

\[
 {1\over r-1}\sum_e I_e^{K,{\rm or}}D_e               \tag{9}
\]

is the coefficientwise Euler replacement of one residual edge by the
oriented curvature.  This is the correct coefficient shadow of the global
four-cut action.  It is not yet a physical chain map on the full
Hilbert--Cauchy carrier: the latter also desuspends the ordered star roles,
mixes the \(q/r\) carrier grades, and must preserve every augmented row.

Equation (3) says exactly what a lift of (9) must do before those additional
operations are allowed.  The lower centered terms cannot be relabelled as
\(H_0\), since (8) kills every constant carrier.  Nor do they cancel under
global reattachment: (2) reconstructs the original centered class rather
than annihilating it.

This sharpens the common-carrier hypothesis.  A successful physical map
must provide, in one complex,

1. a relative filler or accepted physical dual for every lower centered
   class in the marked restriction components;
2. a base-change identifying all component constant lines with one common
   \(H_0\) before evaluation;
3. the two ordered curvature insertions with the exact signs
   \(K^\rightarrow=q-x\) and \(K^\leftarrow=q-r+x\); and
4. word, fine, repeated, target, anchor, terminal, physical-\(q\), residue,
   eta/sigma, and \(W\) naturality.

Only after these clauses hold does dark--dark imply
\((r-2q)H_0=0\).  Formula (3) proves that clause 2 alone is insufficient.

## 3. The exact \(h=3\) physical boundary

The coefficient result is stronger than a word-specific failure: the
lower centered class survives after forgetting all physical labels.  Hence
any complete word/fine/repeated-grade map must contain a correction which
is already visible in this coarse quotient.

The local cap totalization currently lives in

```text
word                 01211222
fine grade           Q_(v,N)=t_v q_(v,N)
repeated-site type   P3+K2
```

and its primitive projected companion has

\[
                         Q_{v,N}=-1,
 \qquad                  \operatorname {ores}=-1.      \tag{10}
\]

No pinned theorem identifies (10) with either of the two 12-coordinate
lower centered classes in (4).  The complete same-grade audit in fact has
only the all-90-term sum in its coarse occurrence image.  Thus the
restriction law does not silently follow from the primitive cap
projection.

The first known cross-word construction is the degree-four mixed/pure
Koszul reset.  Its universal Hasse totalization descends physically only up
to

\[
                       h_v(H_0-u)e_{\rm Eq}.            \tag{11}
\]

The five \(h_v\) form a complete intersection, so denominator-only
Bianchi/Koszul cells cannot remove the primitive conormal in (11).  This
does not prove that the desired map is impossible.  It sharply locates the
first current physical repair: a source-labelled reduced-Eq/cross-word cell
must simultaneously lift the lower centered restriction debts and cancel
(11), or transport their augmented dual to an accepted terminal.

The coordinate-difference dual in (8) is not itself a physical terminal.
It becomes one only after comparison with the complete augmented source
quotient.

## 4. Uniform prolongation law

Uniformity is not fixed-spectator multiplication.  The output family must
satisfy (3) for every \(r\), while its coefficient projector is constructed
directly at order \(r\) from the order-\((r-1)\) association scheme.

Put \(k=r-1\).  The uniform integral numerator is

\[
\begin{aligned}
 L_r={}&\bigl(A_k-(r^2-5r+5)I\bigr)
          (B_k+2I)\\
      &\cdot(B_k-(2r-4)I)(B_k-(2r-2)I),                \tag{12}
\end{aligned}

with rational normalization

\[
                    (2r-3)\,8(r-1)r(2r-1).            \tag{13}
\]

For \(r=3\), (12) is

\[
               (A_2+I)(B_2+2I)(B_2-2I)(B_2-4I),       \tag{14}
\]

and (13) is \(720\), agreeing with the pinned cubic endpoint projector.

A uniform physical lift is therefore a family \(\widetilde L_r\), not a
tensor power of \(\widetilde L_3\), with coherent restriction data
realizing (3).  Equivalently, its spectator product must be a module over
the full Hasse coalgebra so that every Leibniz face is totalized.  Multiplying
an \(h=3\) cell by a fixed tail gives

\[
 d(TJ)=T\,dJ+(dT)J,                                    \tag{15}
\]

and omits the second term.  Equations (3), (12), and (15) are the exact
uniform prolongation law: direct association projection at each order,
restriction coherence on every residual edge, and shuffle-compatible
totalization of every tail face.

## Scope

Proved here are the complete coefficient restriction/insertion identity,
the centered restriction formula, its primitive lower dual, the exact
\(h=3\) coefficients, and the direct all-order association normalization.
These use no support enumeration.

Not proved is a filler for the lower centered classes, the complete
word/fine/repeated-grade base-change, the reduced-Eq correction, or the
physical terminal promotion.  Thus the result is a sharp obstruction and a
precise construction interface, not a proof of \(c_0\).

## Verification

Run

```text
python3 computations/verify_uniform_centered_occurrence_restriction_insertion_gate.py
python3 -O computations/verify_uniform_centered_occurrence_restriction_insertion_gate.py
python3 -I -S computations/verify_uniform_centered_occurrence_restriction_insertion_gate.py
```

The checker pins the association projector, primitive cap gate, same-grade
occurrence obstruction, physical reset, and common-carrier theorem.  It
verifies (1)--(8) at orders two through four and (12)--(14) through order
eight.
