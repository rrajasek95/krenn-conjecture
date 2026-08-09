# Iterated Ward words: the anchor changes matching provenance

## Verdict

All 47 main `(q,r)=(0,2)` profiles are in the common-word Hamming-one sector,
but their selected mixed output words are 3--7 site-colour changes away from
the pure word `1^8`.  The shortest iterated Ward identity is exact at the
level of the complete matching polynomial.  It does not, however, carry the
localized active matching to the pure anchor matching:

- the active matching dies before the pure endpoint in all 47 profiles;
- the pure matching is absent at the initial mixed word in all 47 profiles;
- it appears through formally absent intermediate source coordinates; and
- only 35 of the 47 sparse charts have a Laurent monomial divisibility from
  the active leader to the pure anchor.  The remaining 12 are genuine
  multi-matching provenance guards.

Thus the 35 chart-local units are real but do not prove a uniform Ward
transport lemma.  An additional matching-exchange relation is necessary for
the other 12.

## Exact Ward expansion

For an output word `w` and a site `v` with `w_v != 1`, let

```text
W_v = sum_(u,b) A_vu(1,b) d/d A_vu(w_v,b).
```

Every matching monomial contains exactly one cell incident to `v`, so

```text
W_v F_w = F_(w with v recoloured to 1).                  (1)
```

Ward fields at distinct sites commute.  Recolouring every non-1 site gives a
shortest word whose proper prefixes are mixed and whose endpoint is `1^8`.
Modulo the full target equations, all intermediate coefficients vanish and
the endpoint equals one.

The checker expands (1) by the underlying physical perfect matching at every
prefix.  This is essential when two changed sites are endpoints of the same
edge: the second Ward derivative acts on the coefficient introduced by the
first, and an absent intermediate cell can produce a nonzero final pure
cell.  Reducing only specialized intermediate values would lose this
Leibniz term.

## Complete census

```text
shortest Ward length       3:28, 4:2, 5:12, 6:3, 7:2
active matching death      step 1:45, step 2:2
pure matching birth        final step:46, step 3 of length 5:1
matching difference        C4:35, C4+C4:2, C6:9, C8:1
double-changed pure edges  1:30, 2:15, 3:2
```

The pure `X_1` coefficient is a unique monomial of degree three on every
profile.  The active/pure support-mask overlap is

```text
(active degree, common degree, pure degree)
(1,0,3):5, (1,1,3):7, (2,1,3):7, (2,2,3):28.
```

Consequently the active leader divides the pure monomial in exactly 35
profiles.  There the quotient is a Laurent unit and the familiar sparse
monomial certificate is valid.  In 12 profiles an active coordinate is
absent from the pure anchor, so determinant clearing cannot produce that
quotient without a new exchange equation.

## Canonical divisible profile

For

```text
support = 01:21, 03:11, 17:11, 56:11
w       = 11022111
Ward sites = 2,3,4
```

the paths are

```text
active matching  02|17|34|56:  mask 12, 0, 0, 0
pure matching    03|17|24|56:  0, 0, 0, mask 14.
```

The pure path starts from the absent cells `03:12` and `24:02`.  Its edge
`24` has both endpoints changed, so the two-site Leibniz term passes through
an absent intermediate `24` cell before reaching the existing pure `24:11`
cell.  The matchings differ by the alternating `C4` on `0,2,4,3`.

Here `mask 12` divides `mask 14`, with quotient `03:11` (`mask 2`).  This is
a correct chart-local Laurent unit, but it identifies support variables after
the active physical matching has already died; it is not same-matching Ward
transport.

## Smallest nondivisible guard

The first exact failure is

```text
support = 03:11, 15:00, 15:11, 67:11
w       = 10022011
Ward sites = 1,2,3,4,5
```

with

```text
active matching  02|15|34|67, mask 10
pure matching    03|15|24|67, mask 13.
```

Again the physical matchings differ by the `C4` on `0,2,4,3`, and the pure
path starts from absent `03:12` and `24:02` cells.  But now

```text
active-only mask = 2   (15:00)
pure-only mask   = 5   (03:11 and 15:11).
```

No Laurent monomial quotient turns the active leader into the pure anchor.
The missing statement is exactly a determinant-cleared exchange between the
two active-only and two pure-only edges of the alternating matching cycle (or
a mixed two-term row supplying that exchange).  Iterating more site Ward
operators cannot change this physical matching provenance.

## Scope and reproduction

These are sparse support regressions, not exact Krenn sources.  The result
guards an iterated-Ward shortcut and isolates the next finite `2x2` exchange
test; it does not refute a source-faithful exchange identity using the good
arms and all nine rows.

```text
python3 computations/verify_oo_c8_iterated_ward_provenance.py
python3 -O computations/verify_oo_c8_iterated_ward_provenance.py
```
