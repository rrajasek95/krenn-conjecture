# The witness-splitting dichotomy: a factorization attack on clean-cap existence

Status: **proposal / attack plan** (nothing below is claimed proved unless
cited to an existing artifact). Written as a continuation of the
problem-first intrinsic reduction and the weakest-constructive-object
audit, which reduce the constructive branch to one tuple `(p,q,K)` with

    s(K) kappa_0(K) kappa_1(K) kappa_2(K) != 0   and   E_pq(K) = 0.   (W)

## 1. The observation

At `h = 3` the error is the explicit K-cubic (descent note, eq. 17)

    6 E_pq(K) = 3 s r^2 x + r^3,

and every quantity in the witness conditions is LINEAR in `K`: `s` is
contraction with the edge block, and each `kappa_c(K) = K(e_c, e_c)` is a
coordinate functional (in particular `kappa_c` is never the zero form).
Hence for a live pair (`s` not identically zero), the witness set is

    { E_pq = 0 }  minus the four hyperplanes  {s=0}, {kappa_c=0}

inside `P^8 = P((V_p tensor V_q)^*)`. By the Nullstellensatz over C:

> **Dichotomy (elementary, to be formalized).** For each pair `(p,q)` of a
> normalized exact source, exactly one holds:
> (a) a clean-cap witness exists at `(p,q)` — descent fires; or
> (b) the cubic `6 E_pq`, as a polynomial in `K`, is nonzero and every
>     irreducible factor is one of the four linear forms
>     `s, kappa_0, kappa_1, kappa_2` (up to scalar); or
> (c) `E_pq = 0` identically in `K` (equivalently the pair is
>     r-degenerate, e.g. `r^2 = 0`), in which case EVERY generic `K` is a
>     witness unless `s = 0` identically (dead edge).

Case (c) is favourable (generic witness). Case (b) is therefore the ONLY
way a live pair avoids descent, and it says: a specific source-determined
cubic in nine variables splits into three linear factors drawn from a
named four-element set — at most 20 patterns
`E ~ l_1 l_2 l_3`, `l_i in {s, kappa_0, kappa_1, kappa_2}`.

## 2. The splitting system

Each pattern is a finite system of polynomial identities on the SOURCE
variables (coefficientwise comparison of two explicit K-cubics: 165
coefficients in P^8, with massive structural collapse from the
square-zero site algebra). A minimal counterexample must satisfy, at
EVERY live pair simultaneously, one of:

    dead edge (s == 0),  or  one of <= 20 splitting patterns.        (S)

The support floor already bounds the number of dead edges. So the
counterexample satisfies a completely explicit, intrinsic, finite
polynomial system (S) on top of the GHZ equations — no enriched
presentation, no auxiliary B/Eq data, exactly the objects the
problem-first reduction declares intrinsic.

## 3. The plan

P1 (formalize): state and prove the dichotomy (radical membership for a
   cubic against a product of four linear forms is elementary); extract
   the exact coefficient systems for all splitting patterns, using the
   committed descent checker's own constructors for `s, r, x, kappa`.
P2 (calibrate at six sites): for the 19-type census strata, verify that
   (S)-everywhere is impossible — this must reproduce Theorem A and, if
   the computation is clean, yields an INDEPENDENT second proof of the
   six-site theorem in purely intrinsic terms.
P3 (kill patterns structurally at N=8): show individual patterns force
   excluded degeneracies (e.g. factors `kappa_c^2 | E` force rank
   conditions on the pair block; `r^2`-type collapse forces case (c));
   the goal is to cut the 20 patterns to a small survivor list.
P4 (meet the band): impose (S) on the surviving support band
   (floor 18 up to the falling ceiling) and grind with the same exact
   census machinery the ratchet uses. Success = the dense-side
   meeting theorem: "support >= k  =>  some live pair violates (S)
   =>  witness exists  =>  clean pair", closing the pincer without the
   enrichment census.

## 4. Falsifiers and discipline

Per the decision rule: no claim below the level of "an actual (p,q,K)
verified by the committed descent checker" or "an exhaustive (S)-system
refutation over a named stratum" counts as closure. If some pattern
proves satisfiable on a live stratum, that stratum is precisely where the
counterexample portrait sharpens — report it, do not route around it.
