# The cap-parameter sign does not split off pure residue

## Result

The normalized old cap graph is

```text
dT=-w,    d(rho)=w,    G=T+rho.
```

It is tempting to fix `T`, negate `rho`, and antisymmetrize `G`, apparently
producing the target-zero residue `2*rho`.  That transformation is not a
chain map.  The candidate has

```text
d(2*rho)=2w,
```

so it is exactly the old relative residue obstruction, not a new cap class.

The exact universal statement explains why.  Over `Q[Y]`, there is a legal
semilinear involution

```text
Y -> -Y,    T -> T,    rho -> -rho,    w -> -w.
```

Both signs act on the graph coefficient, hence

```text
T+Y*rho -> T+Y*rho.
```

The legal involution fixes the graph; its anti-part is zero.  It exchanges
the fibres `Y=1` and `Y=-1`, since `(Y-1)` maps to `-(Y+1)`, and therefore
does not descend to an internal symmetry of the normalized physical fibre.

## Fixed-fibre obstruction

At `Y=1`, require an internal map to preserve physical target and negate
ordinary residue.  Its degree-one matrix is forced to be

```text
M=diag(1,-1).
```

If its action on `w` is multiplication by `s`, the chain equation

```text
[-1,1] M = s[-1,1]
```

requires simultaneously `s=1` and `s=-1`.  Thus no such chain map exists
in characteristic zero.  Equivalently, every target-zero old-cap chain is
`b*rho`, with boundary `b*w`; the target-zero cycle kernel is zero.

## Consequence for the proof frontier

Signed Weyl or cap-parameter antisymmetrization cannot manufacture the
primitive pure-residue class.  A presentation-safe comparison between the
two parameter fibres would retain a relative carrier rather than make it
absolute.  To close the cap block one still needs an invisible degree-one
chain `n` with `dn=w` (with the required scalar factor), or equivalently the
physical response-to-cap word/fine/repeated-grade placement already isolated
at Gate II.

This retires only the cap-sign shortcut.  It does not obstruct a genuinely
new physical mixed comparison cell.

Checker:
[`verify_h3_cap_y_sign_antisymmetrization_no_go.py`](../computations/verify_h3_cap_y_sign_antisymmetrization_no_go.py).
