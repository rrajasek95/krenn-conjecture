# Sole-plane \(2^3 1^7\) closure

The exact degree-78 certificate below has been reconstructed independently
with a second prime and reversed variable orders.  Its separate audit is
[here](live-three-zero-sole-plane-fourth-high-three-double-closure-independent-audit.md).

## 1. Result

This note closes the first residual profile left by
[the fourth-high sole-plane frontier](live-three-zero-sole-plane-fourth-high-frontier.md):

\[
                              2^3 1^7.                         \tag{1}
\]

**Theorem 1.1.**  On the sole-plane layer \((r,t)=(7,13)\), a profile with
three double beta classes and seven singleton beta classes has a nonzero
noncoordinate permanent pivot.  Equivalently, the complete shared-zero
response is injective on (1), with arbitrary row plane and direct scale.

The unified exact audit is

```text
.venv/bin/python computations/verify_live_three_zero_sole_plane_fourth_high_three_double_closure.py
```

## 2. Necessary parameter obstructions

Normalize the three double values to \(1,v,w\).  Structural admissibility is

\[
 L=vw(v-1)(v+1)(w-1)(w+1)(v-w)(v+w)\ne0.                    \tag{2}
\]

The pair-determinant construction in
[the three-double frontier](live-three-zero-sole-plane-fourth-high-three-double-frontier.md)
gives a first cross identity.  Ten confluent evaluations generate the unit
ideal over \(\mathbb Q(v,w)\).  The exact `liftstd` matrix has shape
\(10\times1\), has 34 coefficient terms, and all coefficient denominators
are one.

Remove only factors of (2) and cyclically choose each double value as the
normalized anchor.  This gives

\[
 h_1,h_2,h_3\in\mathbb Q[v,w],\qquad \deg h_i=30.            \tag{3}
\]

Every putative counterexample satisfies \(h_1=h_2=h_3=0\).  Put
\(H=(h_1,h_2,h_3)\subset\mathbb Q[v,w]\).

## 3. Homogeneous degree-78 rank

Let

\[
 S=\mathbb Q[t,v,w],\qquad
 J=(h_1^h,h_2^h,h_3^h)\subset S,                             \tag{4}
\]

where each homogenized generator has degree 30.  For a homogeneous ideal
\(I\), write

\[
 \operatorname{HF}_I(D)=\dim (S/I)_D.
\]

The degree-78 Macaulay map of (4) has 3160 target monomials.  Exact
arithmetic over \(\mathbb F_{32003}\) gives

\[
 \operatorname{HF}_{J_{32003}}(78)=318,
 \qquad \operatorname{rank}(M_{78}\bmod32003)=3160-318=2842. \tag{5}
\]

The checker recomputes the full modular standard basis and its Hilbert
numerator.  Reduction modulo a good prime cannot increase the rank of an
integral matrix, hence

\[
 \operatorname{rank}_{\mathbb Q}M_{78}\ge2842,
 \qquad \operatorname{HF}_{J}(78)\le318.                    \tag{6}
\]

This is the only modular inequality used in the proof.  No unit ideal or
membership over \(\mathbb Q\) is inferred from a modular one.

## 4. Exact rational overideals

Set

\[
                         Q=t^{46}(L^h)^4\in S_{78}.           \tag{7}
\]

The checker literally verifies \(\deg Q=78\) and
\(Q|_{t=1}=L^4\).

### 4.1 The affine overideal

Modular reconstruction proposes an affine rational overideal, after which
fresh exact arithmetic over \(\mathbb Q\) verifies the proposal.  Its
homogenized standard basis defines a homogeneous ideal \(A\subset S\) with

\[
 J\subseteq A,\qquad Q\in A,qquad
 \operatorname{HF}_A(78)=192.                               \tag{8}
\]

The exact basis of \(A\), computed in order \(dp(t,v,w)\), has 55 elements.
Its first Hilbert numerator is

\[
 1-4z^{18}-8z^{19}+8z^{20}+3z^{21}-z^{22}+z^{23}.           \tag{9}
\]

The checker also computes the exact standard basis of \(A+(t^{16})\) and
finds

\[
                  \operatorname{HF}_{A+(t^{16})}(78)=0.      \tag{10}
\]

### 4.2 The second overideal

In the same abstract polynomial ring, use the smaller computational order
\(dp(v,w,t)\).  An explicit name-preserving map sends the source variables
\((t,v,w)\) to the variables with those same names, and the checker prints
and asserts the order \((v,w,t)\).

Starting with \(J+(t^{16})\), modular reconstruction proposes a rational
overideal \(B\).  All facts used below are then checked exactly over
\(\mathbb Q\):

\[
 J+(t^{16})\subseteq B,qquad Q\in B,qquad
 \operatorname{HF}_B(78)=126.                               \tag{11}
\]

The exact homogeneous standard basis has 73 elements.  Its Hilbert
numerator is

\[
 1-z^{16}-3z^{30}+3z^{46}+14z^{48}+4z^{49}-18z^{50}.        \tag{12}
\]

The order \(dp(v,w,t)\) is only an efficiency choice: modulo 32003 it has
73 basis elements and 11,449 terms, versus 319 elements and 59,274 terms
for \(dp(t,v,w)\).  Equations (11)--(12) are exact rational checks.

## 5. The exact degreewise squeeze

Let \(C=A\cap B\).  Equations (8) and (11) give

\[
                         J\subseteq C,qquad Q\in C.          \tag{13}
\]

Since \(t^{16}\in B\), one has

\[
 A+(t^{16})\subseteq A+B.
\]

Therefore (10) forces

\[
                       \operatorname{HF}_{A+B}(78)=0.        \tag{14}
\]

The standard exact sequence

\[
 0\longrightarrow S/(A\cap B)
 \longrightarrow S/A\oplus S/B
 \longrightarrow S/(A+B)\longrightarrow0
\]

and (8), (11), (14) now give

\[
                  \operatorname{HF}_{C}(78)=192+126=318.    \tag{15}
\]

Because \(J\subseteq C\), equation (15) gives
\(\operatorname{HF}_{J}(78)\ge318\).  Combined with (6), this proves

\[
                    \operatorname{HF}_{J}(78)=318,
                    \qquad J_{78}=C_{78}.                   \tag{16}
\]

Finally, \(Q\in C_{78}\) by (13), so (16) gives \(Q\in J_{78}\).  Setting
\(t=1\) yields the exact characteristic-zero membership

\[
                              L^4\in H.                       \tag{17}
\]

No explicit thousand-term multiplier vector is needed: (17) follows from
the exact finite-dimensional rank squeeze.

## 6. Contradiction and projective boundary

At a common zero of (3), equation (17) gives \(L^4=0\), contrary to (2).
This proves Theorem 1.1.

For completeness, the frontier audit finds only the two combined infinity
directions

\[
 [t:v:w]=[0:1:0],\qquad[0:0:1].                             \tag{18}
\]

Both lie on the structural discriminant

\[
 \Delta=t v w(v-t)(v+t)(w-t)(w+t)(v-w)(v+w)=0.              \tag{19}
\]

They are not admissible three-double configurations.  The complete
126-dimensional exact \(B\)-term is retained, rather than discarded, in the
homogeneous squeeze above.  The proof only needs \(B\) as an overideal and
does not identify it as a primary component.

## 7. Reproducibility and audit scope

The checker performs in one fail-closed run:

1. the row, scale, exchange, first-lift, term-count, and denominator audits;
2. construction of the three cyclic degree-30 obstructions;
3. the modular degree-78 Hilbert/rank computation (5);
4. exact rational reconstruction, normalization, homogeneity, inclusion,
   target-membership, and Hilbert checks for \(A\), \(A+(t^{16})\), and
   \(B\); and
5. Python evaluation of the four printed Hilbert numerators, followed by
   the numerical assertions \(318,192,0,126\) and the squeeze (15).

The independent audit rechecks the rank direction in (6), the variable-name
map used for \(B\), every inclusion in (8) and (11), and the exact-sequence
calculation (14)--(16).

The remaining dense-double profiles at \((7,13)\) are

\[
                         2^4 1^5,\qquad2^5 1^3,\qquad2^6 1. \tag{20}
\]

They are not closed by this note.
