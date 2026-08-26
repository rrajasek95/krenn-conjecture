# No-fourth matching charts: exact first completion shell

## Result

The twelve rank-respecting matching geometries with no fourth physical
matching are all excluded through the complete one-cell and two-cell support
shell around their canonical diagonal witnesses.

There is no one-cell mate interface.  There are 868 distinct two-cell mate
interfaces, forming 182 orbits under the exact stabilizers of the twelve
representatives.  Exhausting every one of the 240 possible single additions
and every one of the `C(240,2)` pair additions on each chart shows that an
original literal mixed singleton always remains.  The best pair addition
still leaves two singletons (chart 19); the other chart minima range from 3
to 69.

Of the 868 quadratic interfaces, 842 complete a genuinely new physical
perfect matching.  The remaining 26 use one of the chosen physical layers
with alternative repeated-edge colours.  Those 26 are the guard against the
tempting but false claim that every cancellation mate is a fourth physical
matching.  Each nevertheless leaves another literal singleton.

Clean-cap activity is not inferred from support: it is coefficient-level.
It is unnecessary in this shell because the retained singleton already
excludes every completion considered.

## Exact interface

For a literal word `w` and perfect matching `N`, its source monomial is
uniquely the four-cell set

`{ A_uv[w_u,w_v] : uv in N }`.

Subtracting the twelve selected cells gives the exact completion deficit.
The checker enumerates all 105 choices of `N` for every base singleton word
and keeps deficits of size one or two.  Thus there is no tangent
approximation hidden in the counts: these are all linear and first quadratic
source-labelled mate interfaces.

The theorem is deliberately local.  It does not exclude additions of three
or more cells, identify the alternating witness with the pure localization
triple, or promote any support pattern to a clean cap.

Logical digest:
`717b6c79c51c1ea396641d425253316a4c649be70281a8319c5fcbea6014c12f`.

## Replay

Run `audit_no_fourth_completion_shell.py` in standard, `-O`, and `-I -S`
modes.  Hostile mutations drop a chart, falsely call all interfaces new
physical matchings, or ignore the retained singleton; all must fail.
