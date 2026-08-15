# The one-line overlap forces a factorized dark rank-two cap

## Result

Retain the literal full-nine identities at an eight-site pair chart,

\[
 a_{ij}q^{[3]}+p_i s_jq^{[2]}=\delta_{ij}X_i.             \tag{1}
\]

Suppose the two endpoint-star maps are injective and meet in exactly one
line.  Write its unique relation as

\[
                 Pu=Sv=\ell ,\qquad u,v\ne0.             \tag{2}
\]

Assume that \(Q=q^{[3]}\) has a mixed coefficient.  Then there is a nonzero
physical linear form \(h\in\operatorname{im}P+\operatorname{im}S\) and a
nonzero cap matrix \(M\) such that

\[
 \boxed{
 \operatorname{rank}M\le2,\quad
 \operatorname{diag}M=0,\quad
 \langle M,a\rangle=0,\quad
 r(M)=\ell h,\quad
 r(M)q^{[2]}=0.}                                       \tag{3}
\]

This is a strict, basis-free descent from the invertible scalar-zero
\(K_*\) to a factorized dark cap of pairing rank at most two.  The hypotheses
that \(K_*\) is invertible and \(r(K_*)^{[3]}\ne0\) do not obstruct the
construction; the checker gives a six-site square-free fixture in which
both hold.

Equation (3) is the sharp exact terminal currently justified.  It is not by
itself an active cap: all three physical diagonal readouts and the direct
scalar vanish.  Nor is \(\ell hq^{[2]}=0\) automatically a source-labelled
support deletion.  Promoting it to deletion requires one additional
factorized-annihilator lemma.  No formal star fixture below is presented as
a common-\(q\) EqSystem source.

The exact checker is
`computations/verify_h3_k1_overlap_sharedline_rankdrop.py`.

## 1. The five-to-four multiplication map

Put

\[
                   G=\ell q^{[2]}.                     \tag{4}
\]

Contract (1) with the two expressions in (2).  The six literal identities
are

\[
\begin{aligned}
 p_iG&=v_iX_i-(av)_iQ,\\
 Gs_j&=u_jX_j-(u^{\mathsf T}a)_jQ.
\end{aligned}                                           \tag{5}
\]

Let

\[
 F:\mathbb C^3_P\oplus\mathbb C^3_S\longrightarrow
 L=\operatorname{im}P+\operatorname{im}S,
 \qquad F(c,d)=Pc+Sd.                                  \tag{6}
\]

Here \(\dim L=5\) and
\(\ker F=\mathbb C(u,-v)\).  Multiplication by \(G\) restricts to

\[
       \mu_G:L\longrightarrow
       W=\operatorname{span}\{Q,X_0,X_1,X_2\}.          \tag{7}
\]

Because \(Q\) has a mixed coefficient while the \(X_i\) are three distinct
pure words, these four tensors are linearly independent.  In particular
\(\dim W=4\), so

\[
                    \dim\ker\mu_G\ge1.                 \tag{8}
\]

This is the basis-free elimination that is absent from the ordinary
product-kernel calculation: the latter has dimension zero when the star
intersection has dimension one, but the shared *five-form* \(G\) necessarily
has a physical annihilator.

## 2. The quotient-to-cap injection

Choose \(0\ne h\in\ker\mu_G\) and lift it as

\[
                         h=Pc+Sd.                       \tag{9}
\]

Define

\[
                         M=cv^{\mathsf T}+ud^{\mathsf T}. \tag{10}
\]

The construction does not depend on the lift.  Replacing
\((c,d)\) by \((c,d)+\lambda(u,-v)\) changes the right side of (10) by

\[
                \lambda uv^{\mathsf T}-\lambda uv^{\mathsf T}=0. \tag{11}
\]

It is also injective on the quotient.  If \(M=0\), choose an index with
\(v_j\ne0\).  The \(j\)-th column of (10) makes \(c\) proportional to
\(u\).  Choosing an index with \(u_i\ne0\) then makes \(d\) the opposite
multiple of \(v\).  Thus \((c,d)\in\ker F\), contrary to \(h\ne0\).
Consequently

\[
 \theta:\ker(\mu_G\circ F)/\ker F\hookrightarrow\operatorname{Mat}_3,
 \qquad [(c,d)]\longmapsto M                            \tag{12}
\]

is a well-defined injection.  Its image contains a nonzero matrix, and
(10) makes every image matrix have rank at most two.

## 3. The literal dark equations

For the lift (9), equations (5) give

\[
 hG=
 \sum_i(c_iv_i+u_id_i)X_i-
 \bigl(c^{\mathsf T}av+u^{\mathsf T}ad\bigr)Q.          \tag{13}
\]

The left side is zero.  Independence of the one mixed tensor \(Q\) and the
three pure anchors forces

\[
 c_iv_i+u_id_i=0\quad(0\le i\le2),\qquad
 c^{\mathsf T}av+u^{\mathsf T}ad=0.                    \tag{14}
\]

These are exactly

\[
                   \operatorname{diag}M=0,
                   \qquad\langle M,a\rangle=0.         \tag{15}
\]

Finally the response is literal, not a target-span projection:

\[
\begin{aligned}
 r(M)
 &=\sum_{ij}(c_iv_j+u_id_j)p_is_j\\
 &=(Pc)(Sv)+(Pu)(Sd)=\ell(Pc+Sd)=\ell h.               \tag{16}
\end{aligned}
\]

Together with \(hG=0\), this gives

\[
                         r(M)q^{[2]}=\ell hq^{[2]}=0,   \tag{17}
\]

and proves (3).  Every endpoint order, colour index, direct-block entry and
pure target word occurring in (1) survives this derivation.

## 4. Pure top versus mixed top

The mixed coefficient of \(Q\) is used only at (14), where it separates the
direct scalar from the pure anchors.  If \(Q\) is pure, the already isolated
unary/binary/ternary residual-source branch must be used instead.  If
\(Q=0\), the same dimension argument gives annihilators and forces
\(\operatorname{diag}M=0\), but it need not force
\(\langle M,a\rangle=0\).  The zero-top branch therefore remains separate;
silently applying (15) there would be an overclaim.

The assumptions on \(K_*\) play a different role.  They ensure that the
starting scalar-zero response is a genuine rank-three, nonzero-top packet;
they do not enlarge the four-dimensional codomain in (7), and hence cannot
remove (8).  The reduction is therefore strict:

```text
invertible scalar-zero K_* with r(K_*)^[3] != 0
                         |
                         v
nonzero M, rank(M)<=2, diag(M)=sigma(M)=0,
response ell*h and ell*h*q^[2]=0.
```

## 5. Exact scope and the remaining lemma

There are two different assertions here.

1. **Source-valid conditional theorem.**  In every literal full-nine source
   with a one-line star overlap and mixed \(q^{[3]}\), the matrix (10) and
   all identities in (3) exist.  This part uses the actual common
   \(q^{[2]},q^{[3]}\).
2. **Formal sharpness fixture.**  The checker realizes injective physical
   stars with union dimension five, \(K_*=I\), scalar zero and
   \([r(K_*)^3]_{012345}=-12\).  It also realizes the exact target-map
   quotient and the rank-two matrix in (3).  It does **not** provide a
   quadratic \(q\) realizing all nine rows, so it is not a Krenn source or
   a counterexample.

There is one harmless-looking but important zero-response subcase.  The
matrix (M) and the physical form (h) are nonzero, but multiplication in
the site-square-zero algebra can still make (ell h=0).  That produces an
extra physical response-kernel direction, still with zero diagonal and
zero direct scalar; it is not silently called active.  When
(z=ell h\ne0), the shortest remaining statement is:

> **Factorized-dark-annihilator descent.**  In a source-minimal literal
> full-nine packet, a nonzero response \(z=\ell h\) with
> \(zq^{[2]}=0\), arising from the same one-line endpoint overlap as in
> (2), either exposes a removable source-labelled derivative/occupied cell,
> a literal unit, or an active clean cap.

The theorem proved here supplies every algebraic hypothesis of that lemma
and lowers the cap-pairing rank from three to at most two.  In the
zero-response subcase the corresponding missing statement is the analogous
dark response-kernel deletion.  What the present theorem does not supply is
occurrence ownership: (17) may be a cancellation among several four-edge
cofactors.  A deletion proof must retain those occurrence labels or show
that a support-minimal term of (ell h) has a private cofactor.
