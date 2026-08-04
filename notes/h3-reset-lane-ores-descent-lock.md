# The reset lane is closed: an ordinary-residue descent lock

Negative, lane-closing result.  Krenn's conjecture remains **OPEN**.  This
note proves that the reset lane -- the last live comparison-type keystone
candidate -- cannot deliver the \(-\kappa Y_0\) readout: every chain-map
descent through the committed Hasse/Koszul/cap totalization has ordinary
residue given by a functional of the source equation alone, and in the
physical EqSystem-row-plus-cap module no element of the required type
\((\kappa Yw,0,0)\) exists at all.  The comparison proof style is thereby
empty of live candidates (the marked-polar lane was closed
model-independently earlier); the keystone search moves to the certificate
style.  Everything below is a theorem about the **committed model**; the
audit flags in section 9 name exactly the unfixed data whose resolution
could change that model.

## 1. Statement

Work in the committed direct-free presentation of
[the totalization note](h3-full-hasse-koszul-cap-totalization.md), eqs
(1)-(2): the universal labelled-edge ring \(R\), rows
\(dr_0=(H_0-u)\,e_{\rm Eq}\), \(dr_m=H_m\,e_{\rm Eq}\), cap block
\(dT=-Yw\), \(d\rho=w\), with target supported on \(r_0,T\) and ordinary
residue on \(\rho\).  For a deleted odd site \(v\) and matching \(N\) of
\(F_v\), \(\mathcal N=\tau(H_m)(r_0-T)-\tau(H_0-u)r_m\) is the totalized
chain and \(\mathcal Z=\kappa(\mathcal N-\tau(H_m)Y\rho)\) its response
cycle; \(\pi_U\) extracts the Hasse face \(U\subseteq\{u,t,e,f\}\).  All
arithmetic is exact rational.

**Theorem D** (ores descent; PROVED).  Let
\(\rho_g=\sum_U g_U\pi_U\) be any \(R\)-linear Hasse-face readout with
arbitrary polynomial coefficients \(g_U\).  Then, with the original
differential,

\[
 \operatorname{defect}(\rho_g)
   =\Bigl(\sum_{U\ne\emptyset}g_U\,\partial_UH_m\Bigr)(H_0-u)\,e_{\rm Eq},
 \qquad
 \operatorname{ores}(\rho_g\mathcal Z)
   =-\kappa Y\Bigl(g_\emptyset H_m
     +\sum_{U\ne\emptyset}g_U\,\partial_UH_m\Bigr).      \tag{D}
\]

Hence if \(\rho_g\) is a chain map, then
\(\operatorname{ores}(\rho_g\mathcal Z)=-\kappa Y g_\emptyset H_m\): a
functional of the source equation alone, identically zero on the source.
This is the same death shape as the marked-polar lane ("the value is a
functional of \(\Lambda B'\) alone"), transported to the reset lane.

**Theorem E** (fifteen-column ores descent; PROVED).  On the denominator
columns \(\Phi_s=[\epsilon_{u_s}\epsilon_t]\mathcal N_s\) the \(r_m\)
compensator is absent, so **every** internal face, the bottom included,
carries a defect, and with \(\lambda_s=\sum_{U\subseteq\{e,f\}}
g_U\,\partial_Uh_s\),

\[
 \operatorname{defect}(\rho_g,s)=\lambda_s\,(H_0-u)\,e_{\rm Eq},
 \qquad
 \operatorname{ores}(\rho_g\mathcal Z_s)=-\kappa Y\lambda_s.  \tag{E}
\]

The defect functional and the ores functional **coincide**.  Column by
column, \(\rho_g\) is a chain map on column \(s\) iff
\(\operatorname{ores}(\rho_g\mathcal Z_s)=0\); the total ordinary residue
of any chain-map descent through the full fifteen-column presentation is
identically zero, and the \(-\kappa Y\) readout at the Kronecker column
\((v,m_v)\) is attainable only together with the nonzero eq-defect
\((H_0-u)e_{\rm Eq}\).  The leaks are the eq-defect; killing them kills
the readout.

**Reset-lane lock** (PROVED, under HYP-L).  Let
\(M=\bigl(\bigoplus_\alpha Rg_\alpha\bigr)\oplus RT\oplus R\rho\) with
\(dg_\alpha=F_\alpha e_{\rm Eq}\), \(dT=-Yw\), \(d\rho=w\), and the
committed target convention
\(F_\alpha|_{\rm edges=0}=-\operatorname{tgt}(g_\alpha)\,u\).  Then no
\(n\in M\) satisfies

\[
 (d,\operatorname{tgt},\operatorname{ores})(n)=(\kappa Yw,0,0),
 \qquad \kappa\ne0.                                       \tag{L}
\]

**Comparison refutation** (PROVED, committed codomain).  In the prolonged
Hasse/Spencer module the escape is real: \(\kappa(s_I-T)\) has exactly the
type in (L).  The naive scalar argument "the transported boundary is
\(c\kappa Yw\), so the lock gives \(c=0\)" is **false** for polynomial
\(c\): the bottom Koszul cell
\(\kappa\bigl(H_m(r_0-T)-(H_0-u)r_m\bigr)\) is a physical element of type
\((c\kappa Yw,0,0)\) with \(c=H_m\ne0\), because the lock extraction only
forces \(c|_0=0\).  The correct and stronger statement transports the cap
generators as well.  Let \(\Lambda\) be any \(R\)-linear chain map from
the prolonged totalization to the committed physical module \(M\) that
preserves target and ordinary residue, with
\(\Lambda w=c\,w+q\,e_{\rm Eq}\) -- the general degree-zero image, \(c,q\)
arbitrary polynomials.  Transporting \(T\) forces \(c|_0=1\); transporting
the escape forces \(c|_0=0\) when \(q=0\); and in the wider \(q\)-form the
\(\rho\)- and escape-transports force the impossible identity
\(\kappa u=Y\sigma\) with \(\sigma\) polynomial.  Hence **no such
\(\Lambda\) exists, for any polynomial \(c\) and \(q\)** (section 6).
Option 1 of the totalization note section 6 is thereby **refuted** for
every comparison landing in the committed physical module, and Option 2
(source-valid Hasse-Schmidt corrections) is excluded for every correction
that produces an element of the committed physical module with polynomial
coefficients (HYP-L), because the corrected object would be of type (L)
there.  The reading of Option 1 whose codomain is the uncommitted "actual
filtered source resolution" is a scope caveat of the same kind as
section 9.

## 2. Reconstruction of the lane's objects (VERIFIED)

The checker rebuilds all fifteen \((v,N)\) literal objects and verifies, on
each: \([\epsilon_u\epsilon_t\epsilon_e\epsilon_f]\mathcal N=r_0-T\); the
typing \((d,\operatorname{tgt},\operatorname{ores})(n_I)=(Yw,0,0)\); the
\(\kappa\)-normalized cap identity
\([\epsilon_u\epsilon_t\epsilon_e\epsilon_f]\mathcal Z
=\kappa(r_0-T-Y\rho)\) with \(\operatorname{ores}=-\kappa Y\); and the
diagonal commutator \([d,\pi_{\rm top}]n_I=(H_0-u)e_{\rm Eq}\)
(totalization note (11a)).  Each typing check is paired with a
discrimination probe: dropping \(T\) makes the target probe fire and the
\(w\)-boundary vanish, and a fabricated ores map with
\(\operatorname{ores}(T)=1\) sees the top chain -- so none of the zero
checks is vacuous.

## 3. Proof of Theorem D

The two per-face identities

\[
 [d,\pi_U]\mathcal N=(1-\delta_{U,\emptyset})\,
   \partial_U(H_m)\,(H_0-u)\,e_{\rm Eq},
 \qquad
 \operatorname{ores}(\pi_U\mathcal Z)=-\kappa Y\,\partial_U(H_m)  \tag{3.1}
\]

are verified exactly on all sixteen faces, with
\(\partial_U(H_m)\ne0\) confirmed for every \(U\) so that no instance is
vacuous.  Theorem D is their \(R\)-linear span; the checker additionally
verifies (D) verbatim on two nontrivial polynomial coefficient families
(one involving \(u\) and \(\kappa\)).  \(\pi_\emptyset\) is the only
chain-map face, and it is the physical Koszul cell
\(H_m(r_0-T)-(H_0-u)r_m\).  Three certificates pin the boundary cases:

1. the Koszul syzygy readout
   \((\partial_{ef}H_m)\pi_{ut}-(\partial_{ut}H_m)\pi_{ef}\) is a chain
   map with ores exactly \(0\);
2. the Reynolds/top readout \(\pi_{ef}\) has the nonzero defect
   \(\partial_U(H_m)(H_0-u)e_{\rm Eq}\) -- which is precisely why its
   residue \(-\kappa Y\partial_U(H_m)\) is unavailable;
3. the unique \(R\)-algebra retraction of the square-zero Hasse algebra is
   \(\epsilon\mapsto0\); it reads \(\pi_\emptyset\) and returns
   \(-\kappa Y H_m\).

## 4. Proof of Theorem E and the leak ledger

For each of the five selected columns \((s,m_s)\) the checker verifies
\(\Phi_s=\tau_{e,f}(h_s)(r_0-T)\), its totalized boundary
\(\tau_{e,f}(h_s)Yw\), and the per-face identities

\[
 [d,\pi_U]\Phi_s=\partial_U(h_s)\,(H_0-u)\,e_{\rm Eq}
 \quad(\text{every }U\text{, including }U=\emptyset),
 \qquad
 \operatorname{ores}(\pi_U\mathcal Z_s)=-\kappa Y\,\partial_U(h_s)
\]

on all twenty face/column pairs (the ten columns with \(a\ne m_s\) vanish
identically).  Because the bottom face is no longer defect-free, the two
functionals in (E) coincide, and the equivalence "chain map iff ores
zero" follows since \(H_0-u\ne0\) and \(\kappa Y\ne0\) in the (domain)
polynomial ring.  Both directions are witnessed: a nonzero coefficient
family with \(\lambda_s=0\) is exhibited and is a chain map with ores
\(0\); the Kronecker-column top readout has defect exactly
\((H_0-u)e_{\rm Eq}\) and residue exactly \(-\kappa Y\).

The 5/3/3/1 ladder holds for all fifteen \((v,N)\), with Kronecker top
support at \(s=v\).  The leak ledger (all twenty computed polynomials
\(\partial_U h_s\), hashed into the frozen certificate) has rank **12**
over its **22** monomials, and at each one-edge face the three nonzero
leaks live on three distinct columns with pairwise disjoint monomial
support -- no signed combination of columns cancels the leaks without
killing the top.

## 5. Proof of the lock

Write \(n=\sum_\alpha A_\alpha g_\alpha+aT+b\rho\).  Then
\(\operatorname{ores}(n)=0\) gives \(b=0\); the \(w\)-component of
\(dn=\kappa Yw\) gives \(-aY+b=\kappa Y\), so \(a=-\kappa\);
\(\operatorname{tgt}(n)=0\) gives
\(\sum_\alpha A_\alpha\operatorname{tgt}(g_\alpha)=\kappa\); and the
\(e_{\rm Eq}\)-component gives \(\sum_\alpha A_\alpha F_\alpha=0\).
Extract the edge-degree-zero \(u\)-part of the last equation.  The checker
verifies that **every** hafnian row over all \(3^8=6561\) eight-site
colourings is a sum of exactly-four-edge monomials, and that the monomial
\(u\) occurs in \(F_0=H_0-u\) alone, with coefficient \(-1\); hence the
extraction returns
\(-\bigl(\sum_\alpha A_\alpha|_{\text{edge-deg }0}
\operatorname{tgt}(g_\alpha)\bigr)u=0\), while the target equation makes
the same sum equal \(\kappa\).  Equating the two uses the edges \(=0\)
part of the target equation
\(\sum_\alpha A_\alpha\operatorname{tgt}(g_\alpha)=\kappa\), which is
legitimate because \(\kappa\) and the target values have edge-degree
zero, so its edge-degree-zero part is
\(\sum_\alpha A_\alpha|_0\operatorname{tgt}(g_\alpha)=\kappa\).  So
\(\kappa=0\), contradiction.  No
hypothesis on the number of rows, their degrees, or flatness of any base
change is used.  The single hypothesis is

> **HYP-L**: the syzygy coefficients \(A_\alpha\) are **polynomial** in the
> labelled-edge variables -- no localization inverting an edge-dependent
> element.  The obvious localized escape
> \(A_m=-\kappa(H_0-u)/H_m\) inverts the source equation itself, which
> vanishes identically on the source locus, so it is unavailable to any
> construction that has a source.  (The checker confirms \(H_m\) is not a
> unit and does not divide \(H_0-u\) -- every monomial of a polynomial
> multiple of \(H_m\) has edge-degree at least four, while \(H_0-u\)
> contains \(-u\) at edge-degree zero -- so this really is a
> localization.)

The lock extends the bare-cap lock (9a) of
[the Reynolds-attach note](h3-reynolds-attach-coupled-obstruction.md) from
\(\langle T,\rho\rangle\) to the full bounded EqSystem-row-plus-cap
module.  With the full-nine convention
\(F_{ij}=H_{ij}-\delta_{ij}X_i\), \(\operatorname{tgt}(r_{ij})
=\delta_{ij}\), the same extraction runs verbatim (stated, not separately
mechanized).  The checker also verifies that the extraction
**discriminates**: in a fabricated module where \(u\) occurs in two rows
(\(F_{\rm fake}=H_m+u\) with declared target \(0\)) the combination
\(\kappa F_0+\kappa F_{\rm fake}\) has zero \(u\)-part, so the extraction
does *not* force \(\kappa=0\) there -- and that fabricated row violates
the committed convention \(F_\alpha|_0=-\operatorname{tgt}(g_\alpha)u\),
which is exactly the verified input the proof rests on.

## 6. The derived escape and why no comparison carries it down

The prolonged cycle \(s_I=\sum_S(\partial_SH_m)r_0[I\setminus S]
-(H_0-u)r_m[I]\) is closed (17 terms), and its only target-carrying term
is \(r_0[\emptyset]\) with unit coefficient \(\partial_IH_m=1\)
(totalization note (17)).  The checker verifies that
\(\kappa(s_I-T)\) has \((d,\operatorname{tgt},\operatorname{ores})
=(\kappa Yw,0,0)\) **in the prolonged module**: the lock does not apply
there because the target is carried by a unit, not by a row vanishing at
edges \(=0\).

**The scalar-only argument is false.**  An earlier draft argued: a
cap-normalized comparison sends the escape to a physical element of type
\((c\kappa Yw,0,0)\), and the lock forces \(c\kappa=0\), hence \(c=0\).
For polynomial \(c\) this inference is wrong: the lock extraction only
forces \((c\kappa)|_0=0\), i.e. \(c|_0=0\).  The checker exhibits the
counterexample (machine-verified): \(c=H_m\) is realized by the bottom
Koszul cell \(\kappa\bigl(H_m(r_0-T)-(H_0-u)r_m\bigr)=\kappa\,
\pi_\emptyset\mathcal N\), which lies in \(M\), has boundary
\(H_m\kappa Yw\), target \(0\), ores \(0\), and passes the old extraction
because \(\varepsilon(H_m\kappa)=0\), where \(\varepsilon\) denotes
evaluation at edges \(=0\).

**The repaired refutation transports the cap generators.**  Let
\(\Lambda\) be an \(R\)-linear chain map from the prolonged totalization
to the committed physical module \(M\), preserving target and ordinary
residue.  Its degree-zero component must land in the degree-zero part of
\(M\), so \(\Lambda w=c\,w+q\,e_{\rm Eq}\) with polynomial \(c,q\).
Write physical elements as \(A_0r_0+A_mr_m+aT+b\rho\); the checker
verifies with generic symbolic coefficients that the boundary is
\((A_0F_0+A_mH_m)e_{\rm Eq}+(-aY+b)w\), the target \(A_0+a\), the
ordinary residue \(b\), and that \(\varepsilon\) is a ring homomorphism
with \(\varepsilon(F_0)=-u\) and \(\varepsilon=0\) on every hafnian row
-- so the \(u\)-extraction is valid for arbitrary polynomial
coefficients.

(i) *T-transport* (\(q=0\)): \(\Lambda T\) has
\(\operatorname{ores}=0\Rightarrow b=0\); the \(w\)-component of
\(d\Lambda T=-cYw\) gives \(Y(a-c)=0\Rightarrow a=c\); the vanishing
eq-component gives \(\varepsilon(A_0)=0\) by the \(u\)-extraction; and
the edges \(=0\) part of \(\operatorname{tgt}(\Lambda T)=1\) gives
\(\varepsilon(c)=1-\varepsilon(A_0)=1\).

(ii) *Escape transport* (\(q=0\)): \(\Lambda(\kappa(s_I-T))\) has type
\((c\kappa Yw,0,0)\), so \(b=0\), \(a=-c\kappa\),
\(A_0=c\kappa\) from the target equation, and the \(u\)-extraction of the
vanishing eq-component gives \(\varepsilon(c)\kappa=0\), hence
\(\varepsilon(c)=0\).  With (i): \(1=0\).  No such \(\Lambda\) exists for
any polynomial \(c\) -- in particular \(c=H_m\) and even \(c=0\) are
excluded.

(iii) *Wider normalization* \(\Lambda w=c\,w+q\,e_{\rm Eq}\): the
\(\rho\)-transport (\(\operatorname{ores}(\Lambda\rho)=1\Rightarrow b=1\),
\(-aY+b=c\)) gives \(\varepsilon(c)=1-\varepsilon(a)Y\); the escape
transport's eq-line \(u\)-extraction gives
\(-\varepsilon(c)\kappa u=\kappa Y\varepsilon(q)\).  Substituting,
\(\kappa u=Y\bigl(\varepsilon(a)\kappa u-\kappa\varepsilon(q)\bigr)\):
the left side has the \(Y\)-free monomial \(\kappa u\), while every
right-side monomial contains \(Y\).  Impossible.  The checker verifies
the \(Y\)-free residual is exactly \(-\kappa u\ne0\), and, as a
discrimination probe, that dropping the \(\rho\)-transport pin makes the
extraction identity solvable -- the \(\rho\)-transport is load-bearing.

Hence there is **no** \(R\)-linear target- and ores-preserving chain map
from the prolonged totalization to the committed physical module, for any
polynomial normalization \(\Lambda w=c\,w+q\,e_{\rm Eq}\); in particular
\(\operatorname{ores}(\Lambda(\kappa(s_I-T-Y\rho)))\) can never be
\(-\kappa Y_0\).

**Codomain scope.**  Option 1 of the totalization note section 6 asks for
"a comparison from this derived Eq/Koszul Hasse totalization to the
actual filtered source resolution".  That codomain exists as no committed
artifact.  The refutation above covers every comparison landing in the
committed physical module \(M\); the uncommitted-codomain reading is not
addressed here and remains a scope caveat of the same kind as section 9.

## 7. Parity transport (VERIFIED)

Chart parity (the \(pq/pr\) involution): the lane's chart-odd object
\(\mathcal N^{pq}-\mathcal N^{pr}\) has no \(T\) and no \(\rho\)
component, zero \(w\)-boundary, and zero ores; the chart-even part
carries the cap with coefficient \(-2\tau(H_m)\) (bottom face
\(-2H_m\), vanishing on the source) and nonzero boundary
\(2\tau(H_m)Yw\).  The cap target \(\kappa Yw\) is chart-**even**, and the
only free-invisible object the lane produces is chart-**odd** with zero
cap boundary -- structurally the same separation that killed the
marked-polar lane, transported to the chart grading.

Word parity (\(|w|=\sum_iw_i\bmod2\) on the odd five-letter words):

| tag | digit sum | parity | reset \({\sf P}_{\rm tag}\) |
|---|---|---|---|
| 12112 | 7 | odd | parity-mixing (odd \(\to\) even) |
| 22012 | 7 | odd | parity-mixing |
| 02012 | 5 | odd | parity-mixing |
| 12212 | 8 | even | parity-diagonal |

\(Y_0=00000\) is even.  The word-parity mixing of 12112/22012/02012 is the
honest reason the lane survived the marked-polar parity identity: word
parity is a different grading from chart parity and the lane is
inhomogeneous for it.  The lane nevertheless dies, by the
\(u\)-degree/eq-defect coupling of sections 3-5, not by parity.

## 8. Indeterminacy: the two direct-free tags (VERIFIED)

The second direct-free tag \(m'_8=01221222\) (odd part 12212) has
\(\partial_e\partial_f\partial_u\partial_tH_{m'}=1\) at all fifteen
\((v,N)\), hence the **same** top chain \(r_0-T\) and top boundary
\(Yw\).  The difference of the two descended objects has top face exactly
zero; its bottom face is \(H_m-H_{m'}\) (180 monomials, vanishing at
edges \(=0\)).  By Theorem D, any chain-map readout of the difference
returns \(-\kappa Yg_\emptyset(H_m-H_{m'})\): nonzero as a polynomial,
zero on every genuine source.  The frontier's zero-readout requirement on
lift differences therefore holds -- but **vacuously**, because the lock
makes the set of physical lifts empty.  The committed word-space fact
\(({\sf P}_{12112}-{\sf P}_{12212})[12112]=[00000]\ne0\)
([reset no-go note](h3-mixed-word-reset-cross-quotient-chain-lift-no-go.md),
eq (5)) is unaffected: the two resets remain distinct quotient maps.

## 9. Audit flags and scope (CONVENTIONS; recorded, not silently dropped)

The lock is a theorem about the committed model.  The following flags,
found while reconstructing the committed artifacts, name exactly the
unfixed data whose resolution could change that model.  None is repaired
here.

- **A1** (vacuous assertions): in the direct-free presentation the
  \(pr\) edge is forbidden, so the \(pr\)-direct sector of \(H_m\) is
  identically empty and \(pr\)-two-star \(=H_m\).  Every "did not enter
  the pr-direct sector" check in
  `verify_h3_full_hasse_koszul_cap_totalization.py` is therefore vacuous.
- **A2** (no distinct pr-chart row tested): the committed model gives
  \(r_*^{pq}\) and \(r_*^{pr}\) **identical** boundaries, so the chart
  cycle (23) of the totalization note is the antisymmetrization of two
  identical copies and its closure is a tautology.  No committed artifact
  tests a genuinely distinct \(pr\)-chart row.
- **CONV-1** (\(Y\equiv Y_0\) unfixed): the totalization uses an abstract
  cap variable \(Y\) with \(dT=-Yw\); the jet/denominator presentations
  use \(Y_0=[00000]\).  No committed checker identifies the two; the
  identification is an unfixed convention (the Reynolds-attach note's
  \(\gamma\in\{1,Y\}\) normalization records the same residual freedom).
- **CONV-2** (\(\operatorname{ores}(s_v)=0\) declared, not derived): in
  the jet definition it is declared "structural only"; in the totalization
  it is automatic because ores is supported on \(\rho\) alone.  Both are
  statements about the derived presentation, not the physical residue --
  Theorem E is precisely the test of what that structural declaration is
  worth on the denominator columns.

If A2, CONV-1, or HYP-L is resolved in a way that changes the model, the
lock must be re-derived; the checker pins the file digests of all three
committed inputs so any such change is detected.

## 10. What is and is not proved

Proved here: Theorems D and E, the reset-lane lock (under HYP-L), and the
comparison refutation (for comparisons landing in the committed physical
module), all inside the committed direct-free model.  Not
proved: Krenn's conjecture (OPEN); any statement about models resolving
the section-9 flags differently; nonexistence of certificate-style
keystones.  The consequence for the attack map
([wip-attack-map-2026-08-03.md](wip-attack-map-2026-08-03.md), section
24): the comparison proof style is now empty of live candidates, and the
keystone must come from the certificate style
(n=4 anatomy \(\to\) n=6 Wiedemann \(\to\) colour law).

## 11. Exact verification

Run

```sh
.venv/bin/python computations/verify_h3_reset_lane_ores_descent_lock.py
```

The dependency-free checker (exact `fractions.Fraction`, stdlib only,
`require`-based -- no `assert`, so it is `-O`-safe) imports the committed
totalization machinery via `importlib` with fresh module instances, pins
the sha256 file digests of
`verify_h3_full_hasse_koszul_cap_totalization.py`,
`verify_h3_mixed_word_reset_cross_quotient_chain_lift_no_go.py`, and
`verify_h3_reynolds_attach_coupled_obstruction.py`, and re-runs the latter
two as baselines (certificate digests `ee3699d5...` and `e6cdf0ba...`
re-checked).  It verifies sections 2-8 above, pairing every zero check
with a discrimination probe.  The comparison stage mechanizes section 6
in full: the \(c=H_m\) counterexample (accepted by the old scalar-only
extraction, killed by the transport constraints), the generic-coefficient
module bookkeeping, the ring-homomorphism property of edges \(=0\)
evaluation, the (i)/(ii) contradiction \(\varepsilon(c)=1\) versus
\(\varepsilon(c)\kappa=0\), the wider-normalization \(Y\)-free residual
\(-\kappa u\), and the probe showing the \(\rho\)-transport is
load-bearing.  It freezes a sha256 ledger over the **computed** content
-- the twenty leak polynomials, the sixteen per-face derivatives
\(\partial_UH_m\), the ladder census for all fifteen \((v,N)\), the
computed top chain, the lock extraction coefficients, the counterexample
boundary and \(Y\)-free residual, the computed parity boundaries, and the
180-monomial difference row.  Its frozen ledger digest is

    07a9b589df4b4708133c0849d64bf9e98d7d53d4a4aeeed2f6103a2a3945a828

Runtime is about 5.5 s.  It passes identically under `python3`,
`python3 -O`, `python3 -I`, `python3 -S`, `python3 -I -S`, and
`python3 -m py_compile`.

Mutation audit (each fabricated-geometry mutation raises `RuntimeError`
under both `python3` and `python3 -O`, then was reverted and the clean run
re-verified byte-identical):

| mutation | fabricated geometry | raise message |
|---|---|---|
| M1 | stray edge-degree-0 monomial \(u\) injected into the mixed hafnian row | `direct-free row size changed` |
| M2 | cap differential sign flipped to \(dT=+Yw\) | `[d, pi_top]N is not the nonzero defect (H_0-u)*eq` |
| M3 | one face-hafnian coefficient of \(h_1\) doubled | `Phi_s is not tau(h_s)*(r_0-T) at s=1` |
| M4 | \(\operatorname{tgt}(T)\) flipped to \(0\) inside the transport stage | `generic physical target is not A0+a` |
| M5 | \(\rho\)-transport pin dropped (\(\varepsilon(c)=\varepsilon(a)Y\) instead of \(1-\varepsilon(a)Y\)) | `wider normalization Lambda(w)=c*w+q*eq escaped: the Y-free monomial -kappa*u of the extraction identity vanished` |
