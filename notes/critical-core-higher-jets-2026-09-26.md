# A full-complex fourth-order onset at the singular monochromatic core

September 26, 2026. **Written proof and exact polynomial identities; awaiting
independent audit. The unrestricted square-root rate law remains open.**

[Guide](../explainers/BOUNDARY-STRUCTURE.md) ·
[Replay](../computations/higher-order-2026-09-26/README.md) ·
[Earlier diagonal exclusion](diagonal-support-rate-exclusions-2026-09-26.md)

## 1. The source and the new conclusion

Use the six-site source \(Q\) from the earlier note: site 5 is isolated;
all ten edges on sites 0 through 4 carry only color \(aa\). Opposite edges
of the first four sites have weights \(1,\omega,\omega^2\), respectively,
and edges to site 4 have weight one, where \(\omega^2+\omega+1=0\).
Every four-site matching tensor vanishes. Thus

\[
 Q^{[2]}=0,\qquad H(Q)=0,\qquad DH(Q)=0.
\]

Here divided powers are taken in the commutative site algebra, in which
using a site twice gives zero. Write \(A=Q+X\), \(\delta=\|X\|\),
and \(H(A)=\lambda\Delta+E\), with \(E\perp\Delta\),
\(\Delta=a^6+b^6+c^6\), and \(\epsilon=\|E\|\).
All 135 complex endpoint-color entries of \(X\) are allowed.

**Theorem.** For every such perturbation,

\[
 \boxed{|\lambda|\le (1+\delta/2)\epsilon+
                         \frac{\delta^4}{2\sqrt{15}}.}       \tag{1}
\]

Consequently, any approach with \(F\to1\) has
\(|\lambda|=O(\delta^4)\). For an analytic source arc with
\(\operatorname{ord}(A-Q)=p\), a nonzero leading GHZ output must have
order at least \(4p\). In particular, cancelling the quadratic error cannot
leave a nonzero cubic GHZ signal, regardless of the higher source jets.

This does not bound error below by the cube of signal. Small signal alone
does not exclude still smaller error. The theorem restricts the possible
arcs at this limit; it does not prove the desired rate exponent there.

## 2. An exact identity retaining the off-diagonal terms

Let \(D\) be the ten core edges. Each perfect matching of six sites has
exactly two edges in \(D\), so the constant weight \(\rho_e=1/2\) gives
total matching weight one. For \(h=b,c\), let \(w(e,h)\) be the word with
\(a\) on the endpoints of \(e\) and \(h\) on the other four sites.
Write \(q_e=Q_e(a,a)\), so \(|q_e|=1\).

Because \(Q^{[2]}=0\),

\[
 H(Q+X)=QX^{[2]}+H(X).
\]

In the receiving word \(w(e,h)\), the quadratic term is exactly
\(q_e\operatorname{haf}(X^h[V\setminus e])\): the base edge must occupy
the two positions colored \(a\). The matching-cover identity therefore gives

\[
 \boxed{H_{h^6}(Q+X)=
  \sum_{e\in D}\frac{X_e(h,h)}{2q_e}
       \bigl(H_{w(e,h)}(Q+X)-H_{w(e,h)}(X)\bigr).}          \tag{2}
\]

The last term is a degree-four polynomial in \(X\). It retains all
off-diagonal contributions that prevent the earlier diagonal argument from
extending directly. It has not been dropped or assumed to vanish.

The coefficient vector in (2) has norm at most \(\delta/2\). Every receiving
word is off target, so its vector norm for \(H(Q+X)\) is at most
\(\epsilon\). Also

\[
                  \|H(X)\|\le \delta^3/\sqrt{15}.          \tag{3}
\]

To see (3), replace each edge block by its Frobenius norm. The tensor norm
is bounded by the resulting nonnegative scalar hafnian, by the triangle
inequality over the fifteen matching tensors. Applying
[Roos's scalar bound, equation (42)](https://arxiv.org/html/1906.06176),
with six sites and total squared edge norm \(\delta^2\), gives (3).
Thus (2) bounds \(|H_{h^6}(Q+X)|\) by
\(\delta\epsilon/2+\delta^4/(2\sqrt{15})\).
Since \(|H_{h^6}-\lambda|\le\epsilon\), (1) follows.

When \(F\to1\), \(\epsilon/|\lambda|\to0\). Absorb the first term
of (1) into its left side to obtain the stated fourth-order onset.

## 3. Polynomial certificates through fourth order

For a formal path
\[
 A(t)=Q+tB+t^2C+t^3D_3+t^4D_4+\cdots,
 \qquad H(A(t))=\sum_j t^j H_j,
\]
all four source jets may be arbitrary. For \(h=b,c\), equation (2) gives

\[
 (H_3)_{h^6}=H_{h^6}(B)
       =\sum_{e\in D}\frac{B_e(h,h)}{2q_e}(H_2)_{w(e,h)}. \tag{4}
\]

Hence vanishing second-order output forces both non-ground pure cubic
amplitudes to vanish. Neither \(C\) nor \(D_3\) can restore them.
At the next order,

\[
 (H_4)_{h^6}=\sum_{e\in D}\frac{1}{2q_e}
  \left[B_e(h,h)(H_3)_{w(e,h)}+
        C_e(h,h)(H_2)_{w(e,h)}-
        B_e(h,h)H_{w(e,h)}(B)\right].                    \tag{5}
\]

If \(H_2=H_3=0\), the possible fourth-order pure signal is therefore
the explicit quartic expression

\[
             -\sum_{e\in D}\frac{B_e(h,h)}{2q_e}
                                      H_{w(e,h)}(B).       \tag{6}
\]

This supplies a concrete next obstruction to analyze on the quadratic cone
\(QB^{[2]}=0\). No claim that (6) vanishes on that cone is made here.

The checker expands (4)--(5) as polynomial identities in **540 formal
variables**, one for every cell of each of the four jets. It also checks
all 729 first-order coefficients and an exact full-complex example of (2).
An intentionally omitted matching-cover term is rejected.

## 4. Straight rays cannot approach high GHZ fidelity

For a fixed \(B\), the entire ray has
\(H(Q+tB)=t^2QB^{[2]}+t^3H(B)\). If its quadratic term is nonzero,
that leading tensor has neither a pure \(b\) nor a pure \(c\) amplitude.
If the quadratic term vanishes, equation (4) says the same about the cubic
term. Consequently every ray with nonzero output satisfies

\[
                       \lim_{t\to0}F(Q+tB)\le1/3.
\]

This is a bound for each fixed ray, not a uniform neighborhood fidelity gap.
A curved approach can move its direction as it approaches the base. Such
approaches, starting at order four or later, are the remaining question.
