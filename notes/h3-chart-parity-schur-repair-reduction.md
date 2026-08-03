# The Schur repair must carry chart-odd mass −3 at its own face and 0 at the others

The literal \(h=3\) no-go
[`h3-literal-full-nine-schur-polar-no-go.md`](h3-literal-full-nine-schur-polar-no-go.md)
proves that the five marked polar cochains have source-relative connecting
matrix \(I_5\), so none of them admits a lift \(\Lambda T'=MA'\).  It leaves
one stated escape: a denominator-marked two-edge comparison cell, its
generator (18) carrying a free sign \(\sigma\), whose tail contributes
\(-I_5\).

This note reduces that escape to an exact numerical criterion.  The two
marked chart copies are exchanged by an involution \(\iota\); the polar
cochains are \(\iota\)-odd; so only \(\iota\)-odd material can contribute
at all, and it contributes through a single number per face:

> a repair tail contributes \(-1\) at the face \(v\) **precisely when its
> \(pq\)-direct mass on \(h_v\) is \(-3\)**.

Applied to a whole family \(\{R_w\}\) the repair condition is therefore the
full 25-entry statement

\[
 \bigl[\operatorname{mass}_v(R_w)\bigr]=-3\,I_5,
\]

i.e. **each tail carries \(pq\)-direct mass \(-3\) at its own face and
\(0\) at the other four**.  Mass \(-3\) at every face would give the
all-\((-1)\) rank-one matrix, not \(-I_5\).  That 25-entry mass condition
is the reduction.  It is **not** a sign:
\(-I_5\) is realized by chart-odd tails far outside the span of the
external Rees squares, and this note displays one.

Krenn's conjecture remains open.  Nothing here changes the certified spine.

## 1. The chart-parity involution

For each deleted odd site \(v\in D=\{1,\dots,5\}\) the marked polar of the
common 90-term direct-free row is the three-term face hafnian \(h_v\).  The
checker verifies that this marked polar is literally the \(m\)-coloured
deletion-face hafnian, and that it appears in exactly two places:

\[
 (h_v)_{pq,\mathrm{direct}}\quad\text{and}\quad
 (h_v)_{pr,\mathrm{two\text{-}star}}.
\]

Both facts are genuine outputs of `chart_partition` and `sparse_derivative`,
not chosen labels: differentiating by \(a_{pq}^{00}\) kills the
\(pq\)-two-star piece, and the direct-free hypothesis kills the
\(pr\)-direct piece.

Note the two *sectors* are not the same size — the \(pq\) chart splits the
row \(15+75\) and the \(pr\) chart splits it \(0+90\).  It is the two
**marked copies** that carry the same labelled monomials.  On them there is
a basis-permuting involution

\[
 \iota:\ (pq,\mathrm{direct},M)\longleftrightarrow
        (pr,\mathrm{two\text{-}star},M),                    \tag{1}
\]

splitting the marked leading space as \(V^{+}\oplus V^{-}\) over
\(\mathbb Q\).  Physical identification of the two copies is exactly the
quotient by \(V^{-}\) — which is why the Schur test must run before it.

The no-go's normalized cochains are

\[
 \Lambda_v=\tfrac16\!\!\sum_{M\in h_v}\!\!
   \bigl[(pq,\mathrm{direct},M)^{*}-(pr,\mathrm{two\text{-}star},M)^{*}\bigr],
                                                            \tag{2}
\]

so \(\Lambda_v\circ\iota=-\Lambda_v\) — by construction, since (2) writes
\(\pm1/6\) on the two copies.  The checker records this but it is not an
independent verification.

What *is* independent, and is the structural core, is that the tail of the
kernel vector \(k_v=r_v^{pq}-r_v^{pr}\) is

\[
 T'(k_v)=(h_v)_{pq,\mathrm{direct}}-(h_v)_{pr,\mathrm{two\text{-}star}}
       =S_v,                                                \tag{3}
\]

verified as an exact vector identity.  \(S_v\) is \(\iota\)-odd.  Hence the
connecting class of **any** leading cochain depends only on that cochain's
\(\iota\)-odd part; choosing \(\Lambda_v\) \(\iota\)-odd loses nothing.

## 2. Chart-neutral material is invisible

For any \(\iota\)-even \(w\), oddness of \(\Lambda_v\) gives

\[
 \Lambda_v(w)=\Lambda_v(\iota w)=-\Lambda_v(w),
 \qquad\text{so}\qquad \Lambda_v(w)=0.                       \tag{4}
\]

Equation (4) is a proof over \(\mathbb Q\), and it applies to **every**
chart-neutral tail whatever its origin.

**The modelling hypothesis.**  Applying (4) to denominator and face columns
requires knowing that they *are* chart-neutral — that they enter the two
chart copies with equal coefficient.  That is a modelling hypothesis
inherited from the no-go checker's construction of the leading block
\(B'\), where the pure denominator faces are placed diagonally.

**And that placement is provenance, not evidence.**  The no-go builds
\(B'\) from the *pure* faces (all-zero colours), whose monomials are
disjoint from every \(h_v\) (which carries the \(m\)-colours).  So
\(\Lambda_vB'=0\) holds there by disjoint monomial support, **independently
of how \(B'\) is placed** — placing it anti-diagonally gives zero too.  The
no-go therefore supplies no test of diagonality at all.

The hypothesis is plausible (a denominator column is not labelled by a
chart) but it is **not verified here**, and nothing in the repo settles it:
it is a statement about the comparison complex, which has never been
constructed.
The 405 columns the checker builds are *constructed* diagonally, so their
\(\iota\)-evenness is true by construction, not tested.  Only 5 of the 405
meet a cochain's support at all; the rest pair to zero by disjoint support.

So the honest form of the conclusion is conditional: *on the hypothesis
that denominator/face columns are chart-neutral, they contribute nothing.*

## 3. The mass criterion — the actual reduction

Only \(\iota\)-odd tails matter, and for those the pairing collapses to one
number per face.  If \(w\) is \(\iota\)-odd then \(w(pr,M)=-w(pq,M)\), so
(2) gives

\[
 \Lambda_v(w)=\frac13\sum_{M\in h_v}w(pq,\mathrm{direct},M).  \tag{5}
\]

Hence a repair cell contributes \(-1\) at \(v\) **precisely when its
chart-odd tail has total \(pq\)-direct mass \(-3\) on \(h_v\)**.  This is
fully general over chart-odd tails; the derivation above is the proof and
the checker's seventeen exact rational probes are a confirmation.

## 4. Why this is a mass condition and not a sign

The external marked Rees square

\[
 S_v=(h_v)_{pq,\mathrm{direct}}-(h_v)_{pr,\mathrm{two\text{-}star}}
                                                             \tag{6}
\]

has \(pq\)-direct mass \(3\) on \(h_v\) and \(0\) on \(h_w\) for \(w\ne v\),
so its pairing matrix is exactly \(I_5\) — the connecting matrix itself.
Within the *displayed literal face family* (the ten tails, the 405
chart-neutral columns, the five squares) the \(\iota\)-odd part has rank
exactly five and equals \(\langle S_1,\dots,S_5\rangle\), so inside that
family the only way to reach \(-I_5\) is \(-1\) on each square.

**But \(-I_5\) is not confined to that span.**  Put the whole mass on a
single monomial: pick any \(M_v\in h_v\) and set

\[
 R_v=-3\,(pq,\mathrm{direct},M_v)+3\,(pr,\mathrm{two\text{-}star},M_v).
                                                             \tag{7}
\]

Each \(R_v\) is \(\iota\)-odd, the pairing matrix \([\Lambda_v(R_w)]\) is
exactly \(-I_5\), and \(\operatorname{rank}(R+S)=10\): the span of the
\(R_v\) meets \(\langle S_v\rangle\) only in zero.  The checker verifies
all of this.

So the escape is a 25-entry mass condition on an unbounded space, not a
choice of sign.  An earlier draft of this note claimed the reduction was
"one sign"; that claim was false and (7) refutes it.

## 5. A recorded discrepancy about \(\sigma\)

Two cited files do not agree about where the free sign lives, and per the
handoff guide's rule the discrepancy is recorded rather than resolved.

* [`h3-literal-full-nine-schur-polar-no-go.md`](h3-literal-full-nine-schur-polar-no-go.md),
  equation (18), displays the generator
  \([\,K_v;\ d_{v,m_v};\ a_{xv}^{00},a_{pq}^{00};\ \sigma\,]\) — with a
  \(\sigma\) slot.
* [`h3-qzero-denominator-rees-four-cube.md`](h3-qzero-denominator-rees-four-cube.md),
  equation (12), displays
  \(\mathsf J_{v,N}=[K_v;d_{v,m_v};u_v,t;e_1,e_2]\) — with **no**
  \(\sigma\) slot.  Its equation (9), reached from
  \(K_v=r_{c_v}^{pq}-r_{c_v}^{pr}\), displays the external Rees symbol with
  a determinate \(+\).  Its section 2 says the denominator face's sign is
  chosen to cancel the reset commutator and "the tensor convention then
  fixes the signs of **both one-edge faces**" — the internal
  \(\partial_{e_i}\) faces, not the external face.

So the four-cube note does not leave the external sign open.  Any argument
about \(\sigma\) must cite the no-go's (18), not the four-cube note.

## 6. Scope

1. Finite, \(h=3\), direct-free specialization
   \(x=0,\ D=(1,2,3,4,5),\ p=6,\ q=7,\ r=3,\ A_{pr}=0\), word \(m=12112\).
2. Equations (3), (4), (5) and the witness (7) are proved/verified exactly.
   Equation (4)'s *application to denominator material* rests on the
   unverified chart-neutrality hypothesis of section 2.
3. The rank statement in section 4 is about the displayed literal face
   family only, and (7) shows it does not extend.
4. The attaching chain is not constructed and its sign is not decided.
   Nothing changes on the certified spine; Krenn's conjecture remains open.

## 7. Verification

Run

~~~text
python3 computations/verify_h3_chart_parity_schur_repair_reduction.py
python3 -O computations/verify_h3_chart_parity_schur_repair_reduction.py
python3 -I computations/verify_h3_chart_parity_schur_repair_reduction.py
python3 -S computations/verify_h3_chart_parity_schur_repair_reduction.py
python3 -I -S computations/verify_h3_chart_parity_schur_repair_reduction.py
~~~

The checker rebuilds the ten labelled source columns, their tails and the
five-dimensional lower kernel from the literal geometry, independently
reproduces the connecting matrix \(I_5\), verifies (3) as a vector
identity, verifies (4) on the even part of every literal vector in play,
verifies the parity decomposition and (5) on seventeen chart-odd probes,
computes the displayed family's chart-odd rank by exact elimination
(the ledger names this `displayed_family_*`, since it is a stipulated list
and not all conceivable tails),
verifies that coefficient \(-1\) on each square realizes \(-I_5\) there
(uniqueness following from the \(I_5\) pairing matrix), and verifies the
off-span witness (7) including \(\operatorname{rank}=10\).  Its frozen
ledger digest is

~~~text
55ea1477db5178cda2954cba16b639abb1cc88f569a4f509a15679495a1a8189
~~~

Two recorded checks are true by construction and are not independent
verifications: \(\Lambda_v\circ\iota=-\Lambda_v\) (the constructor writes
\(\pm1/6\)) and the \(\iota\)-evenness of the 405 columns (the constructor
places them diagonally).  The load-bearing geometric inputs are the
marked-polar identification and the two-sector placement of the tails.

Mutation-tested: inverting the cochain sign, un-signing the external
square, perturbing the mass divisor, un-diagonalizing a face column,
inverting the connecting-matrix assertion, and flipping a kernel vector
each raise under both `python3` and `python3 -O`, with a message naming the
broken property.
