# The four-hole response contraction is blind to the terminal class

Research evidence only.  Krenn's conjecture remains open; no certified
dependency is changed, and `SP-CLEAN-BRIDGE` is untouched.

## 1. Outcome

Write \(W=\{0,\ldots,5\}\), let \(q,R\) be symmetric zero-diagonal edge
arrays, and put

\[
 Q_j=[t^j]\operatorname{haf}(q+tR),\qquad
 H_k(e)=[t^k]\operatorname{haf}\bigl((q+tR)[W\setminus e]\bigr).
\]

For a single array \(A\), the **four-hole vector** is
\(H(A)_e=\operatorname{haf}(A[W\setminus e])\), the edge gradient of the
hafnian; the graded \(H_k\) above are its layers along \(q+tR\).  The
**cross-star** \(\mathcal B_{ij}(A)=\sum_{|S|=2,\,S\subset U}
\prod_{s\in S}A_{is}\prod_{u\in U\setminus S}A_{ju}\) for
\(U=W\setminus\{i,j\}\), with \(\mathcal B_{ii}=0\), is the defect in
[`three-anchor-apolar-double-polar-bianchi-reduction.md`](three-anchor-apolar-double-polar-bianchi-reduction.md).
Write \(\langle X,Y\rangle=\sum_{e}X_eY_e\) over the fifteen edges.

**Polarization.**  For \(k=0,1,2\),

\[
 \boxed{\langle R,H_k\rangle=(k+1)Q_{k+1},
 \qquad
 \langle q,H_k\rangle=(3-k)Q_k.}                        \tag{1}
\]

These are the graded polarizations of Euler's identity for the hafnian
(Euler proper is \(\langle A,H(A)\rangle=3\operatorname{haf}A\); only that
special case is literally Euler).  Proof: \(H\) is the edge gradient, and a
matching counted by \(Q_{k+1}\) is recovered from each of its \(k+1\)
marked edges exactly once, the unmarked edges giving the factor \(3-k\).

**Cap ledger.**  With the selected source row \(\alpha Q_0+Q_1=0\), the cap
\(A_{\rm cap}=\alpha q+R\), and \(\chi=\alpha Q_2+Q_3\),

\[
\begin{aligned}
 \langle R,H(A_{\rm cap})\rangle&=\alpha^2Q_1+2\alpha Q_2+3Q_3,\\
 \langle q,H(A_{\rm cap})\rangle&=3\alpha^2Q_0+2\alpha Q_1+Q_2,\\
 \langle A_{\rm cap},H(A_{\rm cap})\rangle
   &=3\operatorname{haf}(A_{\rm cap})=3\chi.
\end{aligned}                                            \tag{2}
\]

**Blindness.**  In the response-translation jet basis

\[
 J_0=\alpha Q_0+Q_1,\quad J_1=\alpha Q_1+2Q_2,\quad
 J_2=\alpha Q_2+3Q_3,\quad J_3=\alpha Q_3,
\]

the terminal class is \(\alpha\chi=\alpha J_2-2J_3\), whereas

\[
 \boxed{\alpha\langle R,H(A_{\rm cap})\rangle=\alpha^2J_1+3J_3.} \tag{3}
\]

No \(J_2\) occurs.  Hence, **for \(\alpha\ne0\)**, the response contraction
of the four-hole vector is a function of \((\alpha,J_1,J_3)\) alone and
**cannot detect cleanliness**.

The hypothesis \(\alpha\ne0\) is necessary, and the corner is instructive.
At \(\alpha=0\) the source row reads \(Q_1=0\), so \(A_{\rm cap}=R\) and
\(\chi=Q_3\); then (1) at \(k=2\) gives

\[
 \langle R,H(A_{\rm cap})\rangle=\langle R,H_2\rangle=3Q_3=3\chi,  \tag{3'}
\]

so the response contraction detects cleanliness *exactly* there.  Boxed (3)
still holds at \(\alpha=0\), but only as \(0=0\); the division by \(\alpha\)
that produces the blindness reading is what fails.

By contrast \(\langle q,H(A_{\rm cap})\rangle\) does carry
a \(J_2\) component,

\[
 \alpha^2\langle q,H(A_{\rm cap})\rangle
   =3\alpha^3J_0-\alpha^2J_1+3\alpha J_2-9J_3,           \tag{4}
\]

and the two probes recombine into the Euler statement in (2):

\[
 \boxed{\chi={1\over3}\langle A_{\rm cap},H(A_{\rm cap})\rangle
      ={1\over3}\bigl(\alpha\langle q,H(A_{\rm cap})\rangle
       +\langle R,H(A_{\rm cap})\rangle\bigr).}          \tag{5}
\]

## 2. The blindness is non-vacuous

Two explicit integer packets, both satisfying the selected source row with
\(\alpha=-1\) and both with \(J_3=0\):

| | layers \((Q_0,Q_1,Q_2,Q_3)\) | \(J_1\) | \(J_2\) | \(\chi\) | \(\langle R,H\rangle\) | \(\langle q,H\rangle\) | \(\langle A_{\rm cap},H\rangle\) |
|---|---|---|---|---|---|---|---|
| A | \((6,6,0,0)\) | \(-6\) | \(0\) | \(0\) | \(6\) | \(6\) | \(0\) |
| B | \((4,4,-1,0)\) | \(-6\) | \(1\) | \(1\) | \(6\) | \(3\) | \(3\) |

Packet A is clean and packet B is not, yet they agree on \(\alpha\),
\(J_1\), \(J_3\) and on the entire response contraction.  The internal
contraction and the cap self-pairing separate them.  The literal arrays are
in the checker as `BLIND_A_Q/R` and `BLIND_B_Q/R`.

## 3. Localization of the seven-row guard

On the audited seven-row packet of
[`h3-diagonal-segre-second-transgression-seven-row-guard.md`](h3-diagonal-segre-second-transgression-seven-row-guard.md)
— its equations (5), (6), (13), (16), scalarized on the \(X_2\)
coefficient — the layers are \((0,0,-2,0)\) and the jets are

\[
                 (J_0,J_1,J_2,J_3)=(0,-4,-2,0).           \tag{6}
\]

Both the source jet \(J_0\) and the **terminal jet \(J_3=\alpha Q_3\)
vanish**: the guard's entire failure \(\chi=-2\) sits in \(J_2\), which is
exactly the component invisible to (3).

This is not merely a re-coordinatization.  The blindness is realized
against this very guard: the clean packet

\[
\begin{aligned}
 R&=\{01\!:\!2,\ 04\!:\!1\},\\
 q&=\{01\!:\!-2,02\!:\!-2,04\!:\!-2,05\!:\!1,12\!:\!-2,13\!:\!-2,14\!:\!-1,\\
  &\qquad 15\!:\!-2,23\!:\!2,25\!:\!1,34\!:\!2,35\!:\!-1,45\!:\!-1\}
\end{aligned}                                             \tag{7}
\]

has layers \((4,-4,0,0)\), hence \(\chi=0\), and reproduces the seven-row
guard's **exact** response readout

\[
 (\alpha,J_1,J_3,\langle R,H(A_{\rm cap})\rangle)=(1,-4,0,-4).  \tag{8}
\]

So the response contraction literally cannot distinguish the audited
non-clean guard from a clean packet.  That is what makes section 3 an
explanation of the guard rather than a restatement of it.

The edgewise four-hole geometry there is also sharp.  The defect
\(H(H(A_{\rm cap}))-2\mathcal B(A_{\rm cap})=\chi A_{\rm cap}\) is supported
exactly on \(\operatorname{supp}(A_{\rm cap})\); the cross-star
\(\mathcal B\) vanishes on every defect edge, so the whole defect is
carried by the iterated four-hole hafnian; the four-hole vector has
grade-0 support \(\{23\}\) (the present anchor's carrier), grade-1 support
the response support, and grade-2 support \(\{45\}\) alone.  Against the
three diagonal-anchor responses, the pairings with the four-hole vector are
\((0,0,1)\) and with the cap are \((0,0,0)\): the two **missing** anchors are
orthogonal to both objects, while the internal quadratic detects the cap.

## 4. Consequence for the four-hole route

Sections 1--3 do not prove the physical landing.  They constrain which
linear probe can prove it.  The exact statement is a uniqueness one.  Seek
\(S=\lambda q+\mu R\) with \(\langle S,H(A_{\rm cap})\rangle=\chi\)
identically in the layers.  Under the source row \(Q_1=-\alpha Q_0\), the
coefficients on \((Q_0,Q_2,Q_3)\) give

\[
 \lambda\alpha^2-\mu\alpha^3=0,\qquad
 \lambda+2\alpha\mu=\alpha,\qquad
 3\mu=1,                                                  \tag{9}
\]

whose unique solution is \(\lambda=\alpha/3,\ \mu=1/3\) — the last two
equations alone already pin it, with determinant \(3\ne0\).  Hence

\[
 \boxed{\text{within }\operatorname{span}\{q,R\},\ 
 S=A_{\rm cap}/3\text{ is the \emph{unique} probe returning }\chi.} \tag{10}
\]

In particular the response \(R\) alone is insufficient, by (3) and the
realized blindness of sections 2--3.  This is a statement about linear
probes in \(\operatorname{span}\{q,R\}\) only: it does not exclude a
pairing against a third array, nor any non-linear function of the
fifteen-component vector \(H(A_{\rm cap})\), which carries strictly more
information than either contraction.

Since the two missing anchors annihilate both the four-hole vector and the
cap on the guard, the diagonal sector must enter before the pairing, not
after it.

This is a guard, not a theorem: it narrows the admissible interface and
does not supply the aggregate landing.

## 5. Audit

The dependency-free checker
[`verify_fourhole_cap_polarization_terminal_blindness.py`](../computations/verify_fourhole_cap_polarization_terminal_blindness.py)
proves (1), (2), (3), (4) and the double-polar defect identity **formally**,
as polynomial identities in the thirty edge variables \(q_e,R_e\) with a
formal \(\alpha\); it then verifies the guard geometry of section 3, the
rank-two clean packet (fifteen edgewise zeros against twenty nonzero cut
values), a deterministic rational packet, the section 2 witness pair, the
\(\alpha=0\) corner (3'), the probe uniqueness (9)--(10), and the
confusion packet (7)--(8), in exact integer/`Fraction` arithmetic.
Equation (5) is deliberately not claimed formally in \(\alpha\): it needs
the source row, so it cannot hold with \(\alpha\) free.  Standard library only; runs in
well under a second; passes normal, `-O`, and `-I -S`.

Provenance note: the formal and packet sections were drafted by an agent
that terminated before running them; the draft contained a monomial-key
type defect which made the cap ledger unrunnable.  That defect is fixed and
every claim above was executed and checked afterwards.  The scalarization
of the seven-row guard was verified line by line against equations (5),
(6), (13) and (16) of the cited audited note.

An independent audit of the first version returned PASS with two
substantive corrections, both applied above and both now encoded as
checker assertions rather than prose: the missing \(\alpha\ne0\) hypothesis
with its corner (3'), and the replacement of an unearned "must pair against
\(q\)" by the provable uniqueness (10).  The confusion packet (7)--(8) was
supplied by the same audit and independently re-verified here.
