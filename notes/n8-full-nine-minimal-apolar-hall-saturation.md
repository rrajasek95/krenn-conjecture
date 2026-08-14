# A one-row Nullstellensatz certificate on the minimal full-nine fibre

## Outcome

The full-nine apolar/Hall bypass closes exactly on the support-minimal
three-pure-matching fibre at (n=8).  In this fibre the three diagonal
anchors already give the contracted identity

\[
                         r q^{[2]}=-\Delta_{6,3},
\]

while the canonical scalar-zero contraction has

\[
                              r^{[3]}=0.
\]

Thus this is the sharp killed-pure-coefficient test for the proposed
cross-word theorem.  Nevertheless one literal off-diagonal word gives a
monomial unit modulo the three anchors.  There is an explicit polynomial
Nullstellensatz certificate, so the packet has no completion to the full
nine rows without leaving this support fibre.

This is a positive saturated-ideal result on the smallest source block, not
the general full-nine kernel-exclusion lemma.  The precise remaining global
equation is the companion-completed (02)-row at the word (010012): outside
the minimal fibre, additional matching paths can cancel its distinguished
monomial, and a general proof must exclude exactly those companions.

## The support-minimal source block

Use residual sites (0,\ldots,5), deleted endpoint labels (0,1,2), and
physical colours (0,1,2).  Keep the following internal cells:

\[
\begin{array}{c|cc}
\text{colour}&\multicolumn{2}{c}{q\text{-edges}}\\ \hline
0&23:a&45:b\\
1&02:c&14:e\\
2&04:f&13:g.
\end{array}
\]

Keep one coefficient in each endpoint star,

\[
 p_0=P_0z_0^0,\quad p_1=P_1z_5^1,\quad p_2=P_2z_2^2,
 \qquad
 s_0=S_0z_1^0,\quad s_1=S_1z_3^1,\quad s_2=S_2z_5^2,
\]

and the off-diagonal direct block (D E_{01}).  The three pure target rows
are exactly

\[
 A_0:=P_0S_0ab=1,\qquad
 A_1:=P_1S_1ce=1,\qquad
 A_2:=P_2S_2fg=1.                                      \tag{1}
\]

These are the three four-edge pure matchings after the deleted endpoints
are reinserted.  No residual pure slice of (q) has a perfect matching.

An exhaustive symbolic replay of all (3^6\cdot9=6561) row coefficients
has only six nonzero polynomials: the three anchor residuals (A_i-1) and

\[
\begin{array}{c|c|c}
\text{word}&\text{row}&\text{residual}\\ \hline
010012&02&P_0S_2ae,\\
200021&10&P_1S_0af,\\
121200&01&Dbcg.
\end{array}                                             \tag{2}
\]

At the unit specialization the anchors are exact and (2) is precisely the
three-entry residual ledger previously seen in the Hamming-two-complete
packet.  The first two words have Hamming distance three from a pure word;
the last has distance four.

## Contracted apolar packet

For (a_{\rm dir}=E_{01}), the canonical scalar-zero matrix is

\[
 \tau E_{01}-\alpha I=-I.
\]

Hence the contracted response is

\[
 r=-(p_0s_0+p_1s_1+p_2s_2).
\]

Its three supported physical edges are (01_0,35_1,25_2).  The last two
meet at site (5), so no three are disjoint and (r^{[3]}=0) on every one
of the 729 words.  Direct matching enumeration also gives

\[
 rq^{[2]}=-A_0X_0-A_1X_1-A_2X_2.                     \tag{3}
\]

Modulo (1), equation (3) is the exact ternary common-power identity.  Thus
common-power apolarity, shared source stars, all three diagonal anchors, and
even total vanishing of the response cube do not themselves find the
contradiction.  An uncontracted off-diagonal row is essential.

## Exact Nullstellensatz certificate

Let

\[
 G_{02}=P_0S_2ae,
 \qquad
 M=(S_0b)(P_2fg)(P_1S_1c).
\]

Then (MG_{02}=A_0A_1A_2), and therefore the following identity holds in
the ordinary polynomial ring over \(\mathbb Z\):

\[
\boxed{
1=MG_{02}-(A_0-1)A_1A_2-(A_1-1)A_2-(A_2-1).}          \tag{4}
\]

Thus the ideal

\[
 (A_0-1,A_1-1,A_2-1,G_{02})
\]

is already the unit ideal; localization or a radical computation is not
needed.  Equivalently, the pure anchors make every factor of (G_{02}) a
unit.  The single (02)-row at (010012) excludes the killed-pure packet.

## Exact boundary of the certificate

In an unrestricted source the same row is

\[
 [010012]\bigl(a_{02}q^{[3]}+p_0s_2q^{[2]}\bigr)=0.    \tag{5}
\]

The term (P_0S_2ae) remains one distinguished matching path, but (5) can
also contain direct matchings, other placements of (p_0,s_2), and other
two-edge (q)-cofactors.  Identity (4) says that any counterpacket must add
at least one such companion and cancel the distinguished path.  It does not
say that the companion is impossible.

Consequently the smallest general gluing lemma is now exact:

> Under the mixed-apolar/Hall hypotheses, transport the three anchor units
> to one (02\)-selector word and prove that all companion paths in (5)
> vanish, or that their sum lies in the already vanishing mixed-Hall ideal.

That companion-exclusion statement is the first genuinely global equation
not supplied by the contracted tangent identity.  Proving it uniformly over
all support fibres would establish the missing-pure part of the desired
full-nine kernel exclusion; the present certificate establishes it only on
the support-minimal fibre.

## Verification

Run

```text
python computations/verify_n8_full_nine_minimal_apolar_hall_saturation.py
python computations/verify_n8_full_nine_minimal_apolar_hall_saturation.py --mode source
python computations/verify_n8_full_nine_minimal_apolar_hall_saturation.py --mode apolar
python computations/verify_n8_full_nine_minimal_apolar_hall_saturation.py --mode certificate
```

The dependency-free checker symbolically replays all 6561 source rows,
enumerates all contracted cube and tangent coefficients, and verifies (4)
as a polynomial identity over \(\mathbb Q\).
