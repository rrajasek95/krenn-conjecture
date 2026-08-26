# Full balanced-contrast ideal referee

The full 1,680-generator contrast-only radical route is terminal.

An independent checker, importing no discovery code, uses the rational point

```text
D_uv = [[1,0],[0,0]] for every u<v except
D_01 = [[1,1],[0,0]].
```

Every one of the 105 matching terms in every balanced `(3,3,2)` contraction
vanishes: each assignment has at least two `q` sites, the base blocks kill
`q` at either endpoint, and the one exceptional oriented edge can service at
most one `q` site.  An independent expansion through all raw three-colour
Hafnians gives zero mismatches.  Nevertheless `(A,B,C)=(105,0,90)` and the
Heron product is `-43875`.

Thus Heron is not in the radical of the full contrast ideal.  This does not
give a zero of all original mixed Hafnians and does not challenge N=8; it only
rules out a proof using the 1,680 balanced contractions alone.

Primary checker: `audit_single_exception_counterexample_independent.py`.
Stable three-mode result SHA:
`5da9b17a59ae3138bc27431af7ded6da762ecb575460f975d1ea4894526b2ed7`.
