# Raw (N=8) minimum-source interface audit

Status: **UNAUDITED CODEX REFEREE REPORT**. No certified-spine file was
changed. The executable artifact is
`computations/unaudited-codex-n8-source-referee-2026-08-20/audit_n8_source_interface.py`.

## Outcome

Accepted outcome (3): there is a sharply delimited residual statement, but
neither the proposed thirteen-exit packet nor any existing finite residual
decomposition is proved to cover every minimum (N=8) exact ternary source.

The honest raw interface is:

> Let (A) be a hypothetical exact ternary (N=8) source of globally
> minimum occupied-cell support. Then its support is positively balanced,
> every pure colour has a live perfect-matching occurrence, and no mixed word
> has exactly one live occurrence. It is not proved that (A) contains the
> parent configuration needed to enter the thirteen-exit packet, nor that an
> arbitrary entered packet terminates in a unit, active clean cap, or strict
> source-valid support reduction.

Three additional dependencies are now explicit:

1. the literal (N=8) lift of the six-site packet has 90 crossing-tail
   occurrences, grouped into 45 first-response terms, beyond the familiar
   thirteen direct/common-tail exits;
2. a binary-restriction decomposition must use genuinely trichromatic rows;
3. normalization must be ordered as global minimum support first if the
   balance theorem is to be invoked without another synchronization lemma.

## 1. Raw coefficient system

For (u<v), retain all endpoint-ordered cells

\[
                 a_{uv}^{ij},\qquad 0\le i,j\le2.
\]

There are (28\cdot9=252) variables. For a word
(w\in\{0,1,2\}^8), its coefficient is

\[
 F_w(A)=\sum_{M\in\operatorname{PM}(8)}
             \prod_{uv\in M}a_{uv}^{w_u w_v}.
\]

Each dense row has 105 matching terms, and the complete exact system is

\[
 F_w(A)=
 \begin{cases}
 1,&w=0^8,1^8,2^8,\\
 0,&\text{otherwise},
 \end{cases}
 \qquad(3^8=6561\text{ rows}).
\]

The checker evaluates all 6,561 equations from this definition using two
independent engines: explicit matching enumeration and hafnian recursion.
It imports no auxiliary response-complex presentation.

Two support consequences are immediate and should not be strengthened in
prose:

* every pure row has at least one live perfect matching;
* a mixed row cannot have exactly one live perfect matching, because its
  sole monomial would be a product of occupied, hence nonzero, cells.

The first statement supplies matching occurrences, not mutual-anchor edges.

## 2. What minimum support really normalizes

Let (S) be the occupied-cell support of a globally minimum-support exact
source, and associate

\[
                 b_s=e_{u,i}+e_{v,j}
 \quad\text{to }s=(uv;i,j).
\]

Let

\[
 H=\left\{h:\sum_v h(v,c)=0\text{ for }c=0,1,2\right\}.
\]

If (h\in H) has \(\langle h,b_s\rangle\ge0\) for every (s\in S),
with one strict inequality, the target-torus scaling

\[
 a_{uv}^{ij}\longmapsto
 t^{h(u,i)+h(v,j)}a_{uv}^{ij}
\]

has a finite (t\to0) limit which fixes the three pure target values and
preserves every mixed zero. It deletes at least one cell, contradicting
global support minimality. The strict Stiemke alternative therefore gives
positive \(\alpha_s\) such that

\[
 \sum_s\alpha_s b_s(v,c)=\mu_c
 \quad\text{independently of }v.
\]

This is the valid balance theorem. The checker verifies the 21-dimensional
incidence interface and exact balance certificates; the preceding paragraph,
not the finite checker, is the proof of the general Stiemke implication.

Balance is a weighted-load statement. It does not say that the occupied
entries have equal modulus, and it supplies no licence to replace every
modulus by one.

There is also a normalization-order issue. The repo uses both:

1. global minimum support, which gives the balance theorem above; and
2. global maximum mutual-anchor count followed by minimum support in that
   stratum, used by several anchor-extremal lemmas.

These are different lexicographic selections. I found no source-level theorem
which transfers global support balance to the second choice. The clean
(N=8) interface should therefore select global minimum support first and,
if useful, maximize mutual anchors only among globally minimum-support
sources. Any lemma requiring the stronger anchor-first extremality must be
reproved for that ordering or explicitly listed as an additional hypothesis.

## 3. Correction to the phase-only record

The stored A1 thirteen-cell object is not a full exact ternary source. A raw
replay of all 6,561 equations gives

```text
pure values:       F_00000000 = 1, F_11111111 = 0, F_22222222 = 0
mixed failures:    none
live words:        four
```

Its two two-term fibres and one three-term fibre do force a non-equilateral
modulus relation; at the stored point their term lists are

```text
01000100:  +1, -1
00010001:  +1, -1
01010101:  +1, -2, +1.
```

But the support is in the degenerating branch, not the balanced branch. The
pure-neutral cocharacter

\[
 h(0,1)=-\tfrac12,\qquad h(1,1)=\tfrac12,
\]

with every other coordinate zero is nonnegative on all thirteen occupied
cells and strictly positive on two. It deletes
(a_{01}^{01}) and (a_{12}^{10}).

Thus the correct record is:

* “all moduli one” is not a proved normalization and must not be used;
* the thirteen-cell object is a mixed-equation/non-equilateral guard;
* it does **not** refute the existence of an all-moduli-one representative
  on the hypothetical globally minimum full exact locus.

The last, stronger statement remains unproved either way. The former wording
that A1 supplied an “exact 13-cell (N=8) witness” was materially too broad.

## 4. The thirteen-exit packet is not an (N=8) coverage theorem

On six residual sites the exact matching classification is sound. For

```text
M0 = 05|12|34,     M1 = 01|25|34,
```

the other thirteen perfect matchings split as

```text
1  cap complement,
4  one-tail neighbours of M0,
4  one-tail neighbours of M1,
4  transverse C6 exits.
```

This proves the combinatorics of an already-entered six-site packet. It does
not prove universal entry. Entry still requires, at minimum:

* live parent occurrences in the required labelled word sections; and
* an absent endpoint-colour multiplier cell on which the literal deletion
  construction is valid.

Neither follows from balance, pure-row liveness, singleton-freeness, or
maximum-anchor selection as presently proved. As a sharp support-level
guard, full 252-cell support has a positive balance certificate
(\mu=(21,21,21)), 105 live matchings in every row, and no absent multiplier
cell. This is not an exact source; it shows only that the normalized support
conditions themselves do not imply packet entry.

More importantly, the literal (N=8) lift with spectator edge `67` does not
have only fifteen terms. Of its 105 matching occurrences:

```text
15  contain the literal common tail 67
90  cross the 67 window twice
```

After removing the two parents, the first sector gives the familiar thirteen
exits. The 90 crossing-tail occurrences group into 45 pairs, the two
endpoint orderings in one physical first-response term. Therefore:

> A bare thirteen-exit closure is not source-complete at (N=8). The honest
> local object is the thirteen direct/common-tail exits together with 45
> response groups.

Even inside the six-site sector, the existing positive theorem covers only
the support-minimum completion of the transverse (C_6) guard. An arbitrary
larger completion may add every singleton mate simultaneously. Termination
of that completion is open.

## 5. W40 supplies both the obstruction and the calibration

The integral W40 (X_4) point was re-evaluated directly over
(\mathbb Q,\mathbb F_{13},\mathbb F_{37}). Its 20-cell support has an exact
positive balance certificate with \(\mu=(3,3,3)\) and seven mutual-anchor
cells. It satisfies:

* every one of the 765 words using at most two colours;
* all 4,881 rows of the level-4 system.

Exactly three raw equations fail:

| word | value | fine | profile |
|---|---:|---|---|
| `01110222` | (1) | `06|12|34|57` | ((3,3,2)) |
| `12221000` | (1) | `05|13|24|67` | ((3,3,2)) |
| `20002111` | (-1) | `04|17|23|56` | ((3,3,2)) |

All three are genuinely trichromatic singleton rows of off-count five.
Consequently, pure compatibility plus the three exact binary restrictions is
not an (N=8) coverage theorem. Any finite decomposition must visibly
consume the trichromatic rows rather than infer them from pair restrictions.

The same point is a positive calibration for clean-cap extraction. At pair
`67`, take

\[
                         K=-I_3.
\]

Direct evaluation gives

\[
 s=-1,\qquad \kappa_0=\kappa_1=\kappa_2=-1,
 \qquad s\kappa_0\kappa_1\kappa_2=1,
\]

and the exact (h=3) error polynomial vanishes on all (3^6=729) residual
words. Thus this boundary point has an explicit active clean cap. It does
**not** refute a theorem of the form “(X_4) plus the correct source
hypotheses forces an active clean cap”; it is a required positive control for
such a theorem.

## 6. Exact proved/open dependency boundary

| Arrow | Status |
|---|---|
| raw (252)-variable, 6,561-row system | definition, exhaustively replayed |
| global minimum support \(\Rightarrow\) positive balance | proved by the Stiemke/1-PS argument |
| exactness \(\Rightarrow\) three live pure matching occurrences and no mixed singleton | elementary |
| balanced minimum source \(\Rightarrow\) thirteen-exit packet entry | **open** |
| six-site entered packet \(\Rightarrow\) `1+4+4+4` exit classification | proved |
| bare six-site packet \(\Rightarrow\) complete (N=8) packet | **false as stated**; 90 crossing occurrences are omitted |
| full (13+45)-response packet \(\Rightarrow\) unit/cap/reduction | **open** |
| arbitrary nonminimum transverse completion terminates | **open** |
| three exact binary restrictions \(\Rightarrow) full ternary exactness | **false**; W40 boundary point |
| W40 (X_4) point has an active clean cap | exact positive probe, independently raw-evaluated here |

The block-diagonal theorem and the conditional Route-A/Route-B strata are
valuable proper-subspace results. None supplies the missing universal entry
map from an arbitrary endpoint-ordered minimum source. Accordingly, no
existing finite case ledger is a partition of the full raw minimum-source
locus.

## 7. Recommended (N=8) attack

The next theorem should not be called the thirteen-exit lemma. A source-faithful
target is:

> **(N=8) response-packet trichotomy.** For a globally minimum-cell exact
> ternary source, produce either a literal mixed unit, an active clean cap,
> or a raw coefficient-preserving deformation of strictly smaller support,
> by using a labelled direct/common-tail packet together with all 45
> crossing-tail response groups and the genuinely trichromatic rows.

A disciplined attack has four stages:

1. Fix global minimum support first and retain its positive balance
   certificate. Do not assume all moduli one.
2. Prove an entry lemma from the raw rows: either find a suitable absent-cell
   parent packet, or route directly to a unit/cap when no such cell exists.
3. Replace the isolated thirteen-exit recurrence by the complete
   `13 + 45 response groups` packet. Use the ((3,3,2)) rows as the first
   equations coupling those response groups.
4. Calibrate cap extraction on the W40 point, where `pair 67, K=-I` must be
   found. Any filter which rejects that point before the full cap check is
   over-strong.

This stays entirely at (N=8). No all-order induction or auxiliary
homological presentation is needed until this response-packet theorem is
either proved or sharply falsified.

## 8. Reproduction and controls

Run:

```text
PYTHONDONTWRITEBYTECODE=1 python3 computations/unaudited-codex-n8-source-referee-2026-08-20/audit_n8_source_interface.py
PYTHONDONTWRITEBYTECODE=1 python3 -O computations/unaudited-codex-n8-source-referee-2026-08-20/audit_n8_source_interface.py
PYTHONDONTWRITEBYTECODE=1 python3 -I -S computations/unaudited-codex-n8-source-referee-2026-08-20/audit_n8_source_interface.py
```

The checker requires all seven declared controls to execute:

1. matching enumeration versus independent hafnian recursion on both raw
   points and all 6,561 words;
2. phase-guard scope plus (\mathbb Q/\mathbb F_{13}/\mathbb F_{37}) checks;
3. W40 raw boundary plus the same field controls;
4. explicit `67, -I` cap error on all 729 residual words;
5. a balance-certificate mutation;
6. a source-value mutation; and
7. the dense packet-entry and matching-count guard.

Frozen ledger SHA-256:

```text
157a9baba793c79700e7ad87f870cfa48eaf19c5d67c2273eda071474a1ce90b
```

