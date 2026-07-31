# Hamming two does not force a tangent orbit: the surviving clean branch

## 1. Outcome

Consider the (h=3) residual full-nine equations

\[
 d_{ij}q^{[3]}+p_i s_jq^{[2]}=\delta_{ij}X_i.
 \tag{1}
\]

For a physical word \(w\), write

\[
 F_{ij}(w):=[w]\bigl(d_{ij}q^{[3]}+p_i s_jq^{[2]}-\delta_{ij}X_i\bigr).
\]

For a selected off-diagonal row \((a,b)\), put \(R=p_as_b\) and
\(Q_j:=R^{[j]}q^{[3-j]}\) for \(0\leq j\leq3\), and define the selected
pure-color clean-tail coefficient

\[
 \chi_c:=[c^6]\bigl(d_{ab}Q_2+Q_3\bigr)
        =[c^6]\bigl(d_{ab}R^{[2]}q+R^{[3]}\bigr).
\]

There is an exact rational packet with good shared stars, all three diagonal
anchors, and every coefficient of all nine rows at Hamming distance at most
two from a pure word, for which the selected data satisfy

\[
 d_{01}=1,\qquad q_{03}=0,\qquad
 (p_0s_1)_{03}\ne0.
 \tag{2}
\]

No collection of site endomorphisms can therefore obey

\[
 (D_x\otimes1+1\otimes D_y)q_{xy}=(p_0s_1)_{xy}
 \quad(x<y).
 \tag{3}
\]

The same packet is already on the clean branch:

\[
 R:=p_0s_1=z_0^0z_3^1,qquad R^{[2]}=0,qquad
 d_{01}R^{[2]}q+R^{[3]}=0.
 \tag{4}
\]

Thus Hamming-two data plus the formerly missing diagonal anchor do **not**
force a global tangent-orbit lift.  They remain compatible with a weaker
``tangent or clean'' theorem.  This note does not prove that theorem: it
isolates the exact surviving branch and rules out tangent necessity.

A second exact packet shows that the unweighted sum of the selected
Hamming-two residuals is not the clean-tail functional.  In that packet

\[
 ([2^6]Q_0,[2^6]Q_1,[2^6]Q_2,[2^6]Q_3)=(1,-1,-12,0),\qquad
 \sum_{\operatorname{dist}(w,2^6)=2}F_{01}(w)=-1.
 \tag{5}
\]

Hence the selected pure-color clean-tail coefficient is \(-12\), whereas
four times the displayed sum is only \(-4\).  The equality seen in the
earlier \((1,-1,-4,0)\) guard was a feature of that packet, not an invariant
unweighted contraction.

## 2. The all-nine Hamming-two packet

Use residual sites (0,\ldots,5) and physical colors (0,1,2).  Put

\[
\begin{aligned}
 q={}&(23)_0+(45)_0+(02)_1+(14)_1+(04)_2+(13)_2,\\
 (p_0,p_1,p_2)={}&(z_0^0,z_5^1,z_2^2),\\
 (s_0,s_1,s_2)={}&(z_1^0,z_3^1,z_5^2),\\
 d={}&E_{01}.
\end{aligned}
\tag{6}
\]

The notation ((xy)_c) means the unit cell (z_x^cz_y^c).  Both star
triples have rank three, and every response is literally the shared product
(p_i s_j), so all Segre rectangles hold before taking coefficients.

The three pure eight-site perfect matchings, with deleted endpoints denoted
by (6,7), are

\[
\begin{aligned}
 M_0&=06\mid17\mid23\mid45,\\
 M_1&=02\mid14\mid37\mid56,\\
 M_2&=04\mid13\mid26\mid57.
\end{aligned}
\tag{7}
\]

Every pairwise union (M_i\cup M_j) is one Hamilton cycle.  Consequently
there is no mixed perfect matching using only two of the three pure factors.
This gives the combinatorial reason that the first extra matchings require
three physical colors.

There are

\[
 3+3\binom61 2+3\binom62 2^2=219
\]

distinct words at minimum Hamming distance at most two from a pure word.
Every one of their nine coefficients satisfies (1), for a total of

\[
                         219\cdot9=1971
\tag{8}
\]

exact row identities.  In particular, the (00,11,22) rows all have their
correct pure anchors.  This is not an (8/9) packet.

The complete all-word residual ledger has only three entries:

\[
\begin{array}{c|c|c|c}
\text{distance}&w&\text{row}&\text{residual}\\ \hline
3&(0,1,0,0,1,2)&02&1\\
3&(2,0,0,0,2,1)&10&1\\
4&(1,2,1,2,0,0)&01&1.
\end{array}
\tag{9}
\]

The last entry is the unique internal perfect matching

\[
                         02\mid13\mid45
\tag{10}
\]

completed by the live direct cell (d_{01}).  The selected response
(p_0s_1=z_0^0z_3^1) has no two-edge cofactor in (q), so

\[
                         p_0s_1q^{[2]}=0
\tag{11}
\]

as a complete all-word polynomial.  The selected row is therefore first
detected at distance four, even though the two companion off-diagonal rows
are first detected at distance three.

## 3. Exact failure of tangent necessity

Any site derivation preserves the site-pair support of a quadratic.  More
precisely, its (03)-block is

\[
 (\partial_Dq)_{03}
 =(D_0\otimes1+1\otimes D_3)q_{03}.
\tag{12}
\]

For (6), (q_{03}=0), so (12) is zero for every (D_0,D_3).  But

\[
                         (p_0s_1)_{03}=z_0^0z_3^1\ne0.
\tag{13}
\]

This is an obstruction to the full tangent system before imposing the still
stronger conditions (Dp_0=Ds_1=0).  It is not a tagged one-ended cokernel
calculation; it excludes the simultaneous global edge system itself.

On the other hand, (13) is a single site-pair edge.  Its divided square is
zero in the site-square-zero algebra, and therefore both higher response
layers vanish.  The packet refutes

\[
 \text{all rows through Hamming two}\Longrightarrow
 \text{global unipotent derivation},
\tag{14}
\]

but it does not refute

\[
 \text{all rows through Hamming two}\Longrightarrow
 \chi_c=0\quad(c=0,1,2).
\tag{15}
\]

The latter is the materially weaker, still-live target.

## 4. What the ninth anchor actually changes

In the earlier all-word (8/9) guard, the third endpoint forms were dead
goodness witnesses and the sole residual was (-X_2).  Here (M_2) supplies
the genuine third pure matching and hence the complete (X_2) anchor.
Adjoining that factor does not repair the unsupported selected block (13).
Instead, shared-star coupling creates the two three-color matchings in the
(02) and (10) rows of (9).

So the ninth row can move the obstruction into a higher Hamming sector
without integrating it into a tangent orbit.  This explains why a proof
based only on solving the global first-derivation equations is stronger than
what their distance-\(\leq2\) truncation forces.

## 5. The unweighted Hamming-two sum is not the tail

For a separate guard, keep the pure matching

\[
 q=\sum_{c=0}^2\bigl((01)_c+(23)_c+(45)_c\bigr)
   +z_0^1z_1^0,qquad d=E_{00}+E_{01},
\tag{16}
\]

and use

\[
\begin{aligned}
 p_0={}&z_0^0+z_1^0+z_1^1+2z_2^2+\tfrac32z_4^2+z_5^2,\\
 p_1={}&z_0^1,\qquad p_2=z_3^2,\\
 s_0={}&-z_0^1-z_3^2+z_4^2,\\
 s_1={}&-z_0^0-z_0^1+z_1^1+z_3^2-2z_5^2,\\
 s_2={}&z_2^2.
\end{aligned}
\tag{17}
\]

Both star triples are good and every one of the (351) pure and
Hamming-one full-nine coefficients is exact.  In the selected (01)-row at
pure color (2), the four response-order layers are

\[
             ([2^6]Q_0,[2^6]Q_1,[2^6]Q_2,[2^6]Q_3)=(1,-1,-12,0).
\tag{18}
\]

Thus the admitted top equation is \(1-1=0\), while the selected pure-color
clean-tail coefficient is \(-12\).  Exactly seven distance-two residuals
around \(2^6\) are nonzero;
their values are

\[
                         -1,-1,-1,-2,-2,3,3,
\tag{19}
\]

whose unweighted sum is (-1).  Therefore

\[
 4\sum_{\operatorname{dist}(w,2^6)=2}F_{01}(w)=-4\ne-12.
\tag{20}
\]

Any successful Hamming-two transgression must consequently use weights
coming from the stars, the physical incidence maps, cofactors, or an actual
Hasse--Schmidt lift.  Plain averaging over the Hamming sphere cannot be the
missing invariant.

## 6. Remaining positive target and scope

The natural next theorem is no longer global tangent necessity.  Two
possible goals are:

1. construct a source-provenant weighted Hamming-two syzygy whose value is
   \(\chi_c\); or
2. prove a tangent-or-clean dichotomy in which either a quotient-level
   two-jet lift extends to the response- and target-compatible Hasse--Schmidt
   data needed to kill the tail, or its obstruction forces the tail to
   vanish directly.

The first packet proves that a full site derivation is not necessary.  The
second proves that the most obvious unweighted syzygy is false.  Neither
packet has a nonzero clean tail while satisfying every Hamming-two row, so
they do not decide (15), and they do not modify the certified spine.

The dependency-free exact checkers are
[the all-nine Hamming-two verifier](../computations/verify_h3_hamming_two_tangent_orbit_boundary.py)
and
[the unweighted-sum verifier](../computations/verify_h3_hamming_two_sum_clean_tail_boundary.py).
