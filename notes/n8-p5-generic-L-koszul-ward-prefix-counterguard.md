# Generic-L Koszul-Ward dual-prefix counterguard

The exact site-7 Ward field can be made tangent to the four recovered P5
centres on the additional dense subchart `z9 != 0`, but this finite
four-equation correction does **not** preserve the full selected mixed prefix.

Start with the constant shear on P5,

```text
delta(z46)=b=z44+z45,
delta(z54)=z52+z53.
```

Since `delta(L)=-z11*b`, add

```text
(z11*b/z9) * d/dz25
```

to kill `L`.  The remaining corrections are unique and triangular because

```text
dF1/ds = z11,   dF2/dt = z11*b,   dG/dr3 = -1.
```

Thus only the already localized units `z11,b`, the additional dense unit
`z9`, and the monic `G` pivot are used.  Exact characteristic-zero reduction
confirms that the resulting derivation kills `L,F1,F2,G`.

## Exact dual-prefix verdict

Apply the corrected derivation to the 26 nonzero mixed germs

```text
m_i = Q_i^(6) + epsilon*Q_i^(7) mod epsilon^2
```

in the committed M30-principal prefix quotient.  Twenty-four derivatives
reduce to zero.  Exactly M30 and M33 survive:

```text
theta(M30): 83-term normal form,
theta(M33): 61-term normal form.
```

The ideal remains nonunit.  Every tested pure derivative still reduces to
zero: H0 windows `(4,5),(5,6),(6,7)` and H1 windows `(5,6),(6,7)`.

This is a sharp counterguard to the proposed four-centre shortcut.  The
constant Ward field plus the `L/F1/F2/G` Koszul corrections does not prove the
all-order Nakayama recurrence.  It isolates the missing calculation to the
same exceptional pair M30/M33 that generated every earlier centre.

An exploratory exact standard-basis test of whether the 83- and 61-term
remainders generate one common next direction exceeded a 300-second cap, so
no dependence or independence is inferred.  The next bounded calculation is
to introduce the next filtered `z46` bend (or an equivalent one-scalar
correction) and test whether it kills both remainders; this is smaller and
more faithful than another global order-eight reduction.

The exact checker is
`computations/analyze_n8_p5_generic_L_koszul_ward_prefix.py`.
Its frozen ledger has SHA-256
`c8cc428530534cd69916fb173f20a5fafe28ce9d1cc3f0b81e9e5bb15ed3c03a`.
