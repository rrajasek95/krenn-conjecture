# The complete Hasse tower has a canonical alternating totalization

## The structural point

The nonzero order-six faces

```text
16, 401, 916, 697, 166
```

at levels two through six are not separate correction equations.  Before
repeated derivative directions are symmetrized, the six derivative
occurrences are labelled slots.  For a set of slots `S`, put

\[
 \Delta e_S=\sum_{A\sqcup B=S}e_A\otimes e_B.          \tag{1}
\]

This is the Boolean form of the divided-power Hasse coproduct.  It is
coassociative.  Its reduced cobar differential is

\[
 b(c_1|\cdots|c_r)=
 \sum_i(-1)^{i-1}
 c_1|\cdots|\Delta'c_i|\cdots|c_r,                    \tag{2}
\]

and coassociativity gives `b^2=0`: every ordered three-block splitting has
two parenthesizations with opposite signs.

After the labelled slots are symmetrized, a size-`k` face occurs below
exactly `6-k` size-`k+1` faces.  Thus (1) gives the already audited identities

\[
             \operatorname{down}(L_{k+1})=(6-k)L_k.    \tag{3}
\]

Equation (3) is the unsigned shadow of the alternating complex (2), rather
than a substitute for it.  This supplies the previously missing sign
totalization.

## Source rows remain source-labelled

For a polynomial ring, Hasse translation is an algebra map:

\[
 \partial^{[\alpha]}(fg)=
 \sum_{\beta+\gamma=\alpha}
 \partial^{[\beta]}f\,\partial^{[\gamma]}g.            \tag{4}
\]

Consequently the complete coefficient equations and all of their polynomial
multiples form a cosimplicial principal-parts module.  Splitting a derivative
between a multiplier and a complete source row does not leave the source
presentation; it is exactly one coproduct term in (4).  No matching term is
dropped, and repeated directions are retained with their binomial
multiplicity.

Thus the exact order-six operator has a canonical source-labelled
totalization in the **complete principal-parts source resolution**.  The
higher faces are the homotopies required by the product rule.  Asking one
operator representative to make all of them vanish is both unnecessary and,
from `down(L_3)=4L_2`, impossible when `L_2=-delta`.

## Consequence for the proof frontier

The pinned physical facts now assemble as follows:

1. literal source and first transfer vanish;
2. the canonical secondary transfer is
   \(D_2=-\delta=(-1,+1,+1,-1)\);
3. all higher source faces totalize by (1)--(4);
4. the two fine-word pieces have one total source-module degree; and
5. endpoint oddness kills every protected even augmentation.

Therefore neither higher-face enumeration, alternating-sign discovery, nor
complete-row product-rule closure remains a proof target.  The remaining
local theorem is narrower:

> Construct the comparison from this canonical multigraded
> principal-parts resolution to the physical augmented correction complex,
> carrying `D2` to labelled ordinary residue and the commuting ridge
> `-dOmega_v` to its physical eta/sigma and `W`/anchor interpretation.

This is still a real requirement.  A principal-parts chain is not, merely by
being source-valid, an ordinary physical coordinate correction.  The
comparison may fail by one relative class.  The augmented
generator-or-annihilator alternative remains the correct treatment of that
failure.

## Why this replaces case enumeration

Every support-tier calculation of another Hasse face was resolving a piece
of (1) by hand.  The coproduct proves the whole tower at once and in every
order.  Finite computation should now test only the physical comparison and
its smallest terminal/rank guards, not larger collections of source faces.

Verification:

```text
python3 computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py
python3 -O computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py
python3 -I -S computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py
```

Frozen ledger SHA-256:

```text
67c53150b2e62cdd09519252c7da748cedf982ee02bcb0e608ff820fffbf5cca
```
