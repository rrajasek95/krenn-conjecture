# Augmented homological perturbation and the terminal readout

This is an abstract proved lemma for the proposed path-forest construction.
It does not construct the required contraction in the hafnian source complex
and therefore does not prove the clean-pair bridge.

## 1. Finite filtered contraction

Let \((C,d_0)\) be a chain complex over a field, and suppose there is a
contraction onto \((H,0)\):

\[
 pi=1_H,\qquad d_0h+hd_0=1_C-ip,
 \qquad ph=hi=h^2=0.                                     \tag{1}
\]

Let \(\delta\) raise a bounded filtration and assume
\((d_0+\delta)^2=0\).  Every series below is therefore finite.  Put

\[
 \begin{aligned}
 I&=(1+h\delta)^{-1}i,\\
 P&=p(1+\delta h)^{-1},\\
 h_\delta&=h(1+\delta h)^{-1},\\
 D&=p\delta(1+h\delta)^{-1}i.
 \end{aligned}                                           \tag{2}
\]

With the convention in (1), expansion gives

\[
 D=p\delta i-p\delta h\delta i
     +p\delta h\delta h\delta i-\cdots .                 \tag{3}
\]

The finite homological perturbation lemma gives

\[
 (d_0+\delta)I=ID,\qquad P(d_0+\delta)=DP,
 \qquad D^2=0,                                           \tag{4}
\]

and a contraction of \((C,d_0+\delta)\) onto \((H,D)\).
These identities can also be verified directly by multiplying the finite
geometric series in (2).

## 2. The augmented target formula

Let \(T\) have zero differential and let

\[
                         a:C\longrightarrow T             \tag{5}
\]

be an augmentation of the perturbed complex, meaning

\[
                         a(d_0+\delta)=0.                  \tag{6}
\]

Then the induced physical readout on the contracted complex is

\[
 \boxed{
 a_H=aI=a(1+h\delta)^{-1}i
     =ai-ah\delta i+ah\delta h\delta i-\cdots .}          \tag{7}
\]

Indeed, (4) and (6) give

\[
                         a_HD=aID=a(d_0+\delta)I=0.        \tag{8}
\]

Consequently (7) is constant on \(D\)-homology classes.  In particular, if
a terminal forest representative is changed by a contracted boundary, its
physical target value is unchanged.  Formula (7), rather than the naive
coefficient \(ai\), is the exact zero-indeterminacy statement needed at a
Hamilton cell.

The first correction

\[
                            -ah\delta i                    \tag{9}
\]

records components which leave the chosen forest representative under
\(\delta\), are lifted through the acyclic source directions by \(h\), and
then become visible to the physical cap augmentation.  Thus an off-path spoke
can be invisible to \(ai\) but visible to (9), exactly as in the terminal
chart-26 audit.

## 3. Canonical secondary class

Write \(D=D_1+D_2+\cdots\) by filtration jump.  From (3),

\[
 D_1=p\delta i,qquad D_2=-p\delta h\delta i.              \tag{10}
\]

The first two components of \(D^2=0\) say

\[
 D_1^2=0,qquad D_1D_2+D_2D_1=0.                          \tag{11}
\]

Therefore, for a \(D_1\)-cycle \(x\), the element \(D_2x\) is a
\(D_1\)-cycle.  If \(x\) is changed by \(D_1y\), then

\[
 D_2(x+D_1y)-D_2x=D_2D_1y=-D_1D_2y.                      \tag{12}
\]

Hence

\[
                 \beta[x]=[D_2x]\in H(H,D_1)             \tag{13}
\]

is a well-defined secondary operation on every class for which the earlier
filtration equations have been solved.  This is the precise abstract
zero-indeterminacy property sought for the curvature Bockstein.  Higher
terms of (3) give the subsequent differentials when (13) vanishes.

## 4. Exact consequence for the proposed proof

The two remaining source-specific tasks cannot be replaced by the abstract
lemma:

1. construct (1) in the literal source-labelled hafnian/path-forest complex,
   relative to all three pure anchors and matching-base exchanges; and
2. identify the augmentation (5) with the complete physical clean-cap error,
   not only one terminal monomial coordinate.

Once those are done, no additional argument about lift choices is needed.
Equations (7)--(8) carry every off-path correction to the terminal readout,
and (11)--(13) make the curvature Bockstein canonical.  A nonzero target
pairing can then be used as an obstruction; if all transferred differentials
vanish, the corrected terminal augmentation is the candidate active clean
cap.

## 5. Verification

Run

```text
python3 computations/verify_augmented_hpl_terminal_bockstein_lemma.py
```

The checker verifies a finite contraction, the perturbed differential,
transferred differential, perturbed inclusion, chain-map identities, and an
augmentation for which the naive terminal value is zero but the corrected
value in (7) is nonzero.  It is a dependency-free exact rational audit of the
algebra, not a realization of the hafnian contraction.  Its frozen ledger
digest is
`93f041e93f1e0b6e1968c709a4215600b60358066c46885cec9bea00b228f6e4`.
