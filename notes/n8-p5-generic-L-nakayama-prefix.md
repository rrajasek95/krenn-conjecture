# P5 generic-L Nakayama recurrence through the dual-number prefix

The source-faithful 207-row Schur graph now tests the proposed principal
mixed recurrence one order beyond the monic `G` initial.  The checker is
`computations/verify_n8_p5_schur_generic_L_nakayama_prefix.py`.

Work in the completed quotient by the 207 selected normal/transverse rows and
on the dense chart

```text
L=F1=F2=0,
b*z_binv=z11*z11inv=z16*z16inv=z41*z41inv=1,
(z26+z45)*u_inv=1.
```

The last localization makes the known coefficient of the selected row
`M30` a unit.  If `epsilon` denotes the strict parameter after removing the
common sixth order, the exact graph supplies

```text
m_i = Q_i^(6) + epsilon*Q_i^(7)  mod epsilon^2.
```

The two coefficient families have 11,102 and 60,859 terms and 26 nonzero
rows each.  Exact characteristic-zero reduction proves that all 26 rows lie
in

```text
<L,F1,F2, localizers, epsilon^2, m_30>.
```

In particular `M33` does not add an independent saturated lead at this
order.  This is precisely the principal Nakayama recurrence modulo
`epsilon^2`; equivalently, the proposed relation

```text
m_i = c_i*m_30 + epsilon*sum_j B_ij*m_j
```

has no obstruction in the first dual-number layer.

The same source graph was applied to the two full pure rows.  Their raw graph
term counts through order seven are

```text
H0: 0,0,0,4,54,358,1636
H1: 0,0,0,0,2,23,159.
```

Every consecutive dual window available in this range reduces to zero in
the selected prefix ideal:

```text
H0: (4,5), (5,6), (6,7)
H1: (5,6), (6,7).
```

Thus neither pure germ produces a prefix counterguard through graph order
seven.

The frozen ledger SHA-256 is
`4e36eb6cc9360ad366818339a857c13b9d197a4739aff0c3b9fec0ef99b2b626`.
An order-eight/`epsilon^3` graph was constructed, but its exact Gröbner
reduction did not finish inside five minutes and supplies no result.  The
dual-number pass is strong evidence for the finite Nakayama promotion, not
an all-order proof: a source-level transfer identity or a finite
conormal/equivariant certificate is still required.

No coordinate map from this P5 Ferrers component to normalized `chart26` is
proved here, so the result says nothing by itself about closure of chart26.
