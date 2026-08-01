# `SP-CLEAN-BRIDGE` at eight vertices is the open case

Research evidence only.  Krenn's conjecture remains open, `SP-CLEAN-BRIDGE`
is untouched, and no certified dependency changes.  Nothing here is a partial
case of the conjecture, and nothing here bears on whether \((8,3)\) has a
solution.

## 1. Prior art first

This is the \(N=8\) **base case of Corollary 5.1** of
[the descent target](clean-pair-cap-exact-descent-target.md), whose proof
already reads "order six is excluded by the proved arbitrary-complex six-site
theorem".  The equivalence below is that corollary plus vacuous truth in the
other direction.

Two things are new, and only two:

1. the argument is re-derived at the **aggregate** level, so the decorated-source
   reconstruction of that note's Theorem 1.1 is not needed;
2. the equivalence is written down.

## 2. Outcome

`SP-CLEAN-BRIDGE` at \(N=8\) asks for an **active clean cap**: a covector \(K\)
with \(s\kappa_0\kappa_1\kappa_2\neq0\) and \(\mathcal E_{p,q}(K)=0\).  At
\(h=3\) the nine-row system is the \(n=8\), \(d=3\) coefficient system, so a
nine-row solution is exactly an exact ternary aggregate source on eight
vertices.

> **Unconditionally, given certified `SP-K6`: no eight-vertex exact ternary
> aggregate source admits an active clean cap, at any pair, for any \(K\).**

The proof is three lines.  If the packet satisfies all \(6561\) rows and \(K\)
is active and clean, the six-site aggregate array \(A_{\mathrm{cap}}=sq+R(K)\)
has \(H_6(A_{\mathrm{cap}})=\sum_cs^2\kappa_cX_c^U\).  Rescaling the blocks at
one site on its colour axis by \(\mu_c=1/(s^2\kappa_c)\) — defined **precisely
because** activity gives \(s\neq0\) and \(\kappa_c\neq0\) — is invertible and,
by multilinearity of the diagonal site map, turns that into \(\Delta_{6,3}\).
`SP-K6` (Theorem 1.1 of
[the six-site obstruction](../proofs/six-site-arbitrary-complex-obstruction.md))
forbids exactly this, for an **arbitrary complex** six-site block array, with no
genericity, positivity or source hypothesis.  \(A_{\mathrm{cap}}\) is such an
array and the hypotheses are met verbatim.

Hence:

\[
 \boxed{\;\texttt{SP-CLEAN-BRIDGE}\ \text{at}\ N=8
 \iff\text{the}\ (8,3)\ \text{case is empty.}\;}
\]

Both directions are cheap.  Forwards: a nine-row solution would have to carry an
active clean cap for the bridge to say anything, and by the above it carries
none — so the bridge holds only vacuously, which is to say only if there is no
solution.  Backwards: if the variety is empty, the bridge's universally
quantified hypothesis is never met and the statement is vacuously true.
Quantifier hygiene matters here and the two readings agree: "*some* chart has an
active clean cap" and "*every* chart does" are both equivalent to emptiness.

## 3. What this costs

The identity cap \(\mathcal E(I)=0\) with \(\tau\neq0\) is the **active
analogue** of the \(\chi=0\) landing —
[the cap-line note](cap-line-cubic-and-why-the-landing-is-inactive.md) section 3
proposes it, and it does certify an *active* root, which \(\chi=0\) never can.
Section 2 prices it: the statement "the nine rows force \(\tau\neq0\) and
\(\mathcal E(I)=0\)" is **vacuously true if the variety is empty and false
otherwise**.  Proving it is therefore exactly as hard as proving emptiness.  It
is a correct observation and not a usable intermediate target.

The resulting asymmetry is the whole content of this note and its companion:

| target | certifies | status |
|---|---|---|
| \(\chi=0\) | an **inactive** root \(z=0\) | reachable, gives no descent |
| \(\mathcal E(I)=0,\ \tau\neq0\) | an **active** root | gives the descent, equivalent to the case |

**This does not retire \(\chi=0\).**  Section 2 is about *active* clean caps.
\(\chi=0\) is the cleanliness of an *inactive* one; it implies no descent, and
so implies nothing whatever about emptiness.  Reachable-but-useless versus
useful-but-equivalent-to-the-case is the shape of the difficulty, not a reason
to discard either.

## 4. \(N=8\) is not special

The same argument runs at every size: once \(N-2\) is settled,

\[
 \texttt{SP-CLEAN-BRIDGE}\ \text{at}\ N\iff\text{no exact ternary source at }N.
\]

So `SP-CLEAN-BRIDGE` in full is equivalent to the remainder of the conjecture,
and eight is simply where the induction currently stands.  Reading section 2 as
a peculiarity of eight vertices would be a mistake.

## 5. The certificate sector, for the record

Grading by site-colour degree together with the two endpoint-label degrees, as
in [the multigrading note](terminal-class-ideal-membership-multigrading-bounds.md):
every \(\mathcal E(I)_w\) monomial has site-colour degree \(\sigma(w)\), is
label balanced with \(|\nu|=3\) — all ten \(\nu\) occur — and has d-degree at
most one.  Since \(\sigma(w')\leq\sigma(w)\) forces \(w'=w\), the only
generators available at \(\mathcal E(I)\)'s own multidegree are the same word's
rows with \(i,j\in\operatorname{supp}\nu\), each forced to carry a degree-two
d-monomial multiplier.  Every such contribution has d-degree in \(\{2,3\}\)
against a target at \(\{0,1\}\), so the row sector cannot contribute at the
target's own d-degrees and its \(\{2,3\}\) part must cancel against the anchor
multipliers.

That is the **same** conclusion the multigrading note reaches for \(\chi\), by
the same filter — not a worse one.  There \(\chi\) has one admissible generator
\(d_{01}^2\operatorname{Row}(0,1,2^6)\); here \(\mathcal E(I)\) has \(36\)
across the ten balanced \(\nu\).  Both targets have an exact cap split,

\[
 \operatorname{haf}(\alpha q+A)=\alpha^2\operatorname{Row}(a,b,w)+\chi,
 \qquad
 \operatorname{haf}(\tau q+B)=\tau^2\sum_l\operatorname{Row}(l,l,w)+\mathcal E(I),
\]

so if anything \(\mathcal E(I)\) has strictly *more* row-sector freedom.  The
three anchor generators \(\operatorname{Row}(c,c,c^6)-1\) are inhomogeneous, so
a full argument needs the degree-\(D^\*\) and constant components treated
separately.

## 6. Guards

Two, both at \(6559\) rows — the pure-word anchors missing.  With \(d=I\), the
seven-row guard has an **active clean** identity cap and packet C an **active
unclean** one.  So these \(6559\) rows force neither verdict; the two missing
anchors are what section 2 uses.

Separately, all \(56\) alternating-eight-cycle charts sit at \(6560\) rows
with \(\mathcal E(I)=0\) — but **not all for the same reason**, and star-rank
one is the reason for only \(32\) of them.  Counting live trace-response
edges *per word*, since \(B^{[2]}\) and \(B^{[3]}\) at a word need two or
three edges live at **that** word:

| endpoint distance | charts | \(\tau\) | live edges per word |
|---|---|---|---|
| 1 | 16 | 1 | \(\leq1\) |
| 2 | 16 | 0 | \(\leq1\) |
| 3 | 16 | 0 | 2 at some word |
| 4 | 8 | 0 | 2 at some word |

On the \(32\) charts at distance one and two a single live edge gives
\(B^{[2]}=B^{[3]}=0\) identically — star-rank one.  On the other \(24\) it
does not apply: there \(\tau=0\) kills the \(\tau B^{[2]}q\) term, and two
live edges cannot fill a three-edge matching, so \(B^{[3]}=0\).  The \(16\)
distance-one charts are the only **active** ones, so their clean identity cap
is support concentration and carries no information.

## 7. What this does not say

1. Nothing about whether \((8,3)\) has a solution.
2. The equivalence is not new; see section 1.
3. It does not retire \(\chi=0\); see section 3.
4. It changes no certified dependency.  `SP-K6` is quoted as certified and is
   not re-audited here.

## 8. Audit

The dependency-free checker
[`verify_identity_cap_activity_and_k6_obstruction.py`](../computations/verify_identity_cap_activity_and_k6_obstruction.py)
verifies the formal identity
\(\operatorname{haf}_w(sq^w+R^w)=s^2\sum_{lm}K_{lm}\operatorname{Row}(l,m,w)+\mathcal E(K)_w\)
in the sixty generic symbols; that \(\mathcal E(I)\) is \([z^3]\) of every cap
line and independent of \((a,b)\); the trace row
\(\sum_l\operatorname{Row}(l,l,w)=\tau G_0+G_1\); that rows are \(\tau\)-weight
zero and \(\mathcal E(I)\) weight six; multilinearity of the diagonal site map;
the multigraded census of section 5; the free-direct-block guards of section 6;
and the \(56\)-chart census.  Sections C1 and C2 are checked on seven probe
words, not all \(729\).

Standard library only, exact `Fraction` arithmetic, about six seconds, passing
normal, `-O` and `-I -S`, deterministic across hash seeds.

Independently re-audited: the formal identities, both guards, the \(56\)-chart
census and the multigraded census were rebuilt from the descent note's
definitions by separately written code sharing nothing with the checker.
