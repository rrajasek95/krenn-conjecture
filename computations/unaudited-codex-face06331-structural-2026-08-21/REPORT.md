# k5 full interior `0:63:31` structural source interface

Status: **exact normalized source and first linear split frozen; no solver
launched.**

The all-offdiagonal selected graph uses tree edges `01,02,03`. Their live
`b` entries fix three site ratios and the remaining common scale fixes live
`d01`, giving the canonical gauge

```text
b0=b1=b2=d0=1.
```

The 13 remaining variables are

```text
a0,a1,a2,a3,a4,a5,b3,b4,b5,d1,d2,d3,d4.
```

All 16 literal triangle/cofactor rows raw `6,...,21` survive and have exact
constant-coefficient rank 16 over Q. Their term counts are

```text
16,16,9,9,18,10,14,17,14,17,12,20,12,20,14,30.
```

The exact live product is

```text
H * (b3*b4*b5)
  * (a0*a1*a2*a3*a4*d1*d2*d3*d4)
  * (1+a0)*(1+a1*d1)*(1+a2*d2)*(1+a3*d3)*(1+a4*d4).
```

Its factor profiles are: `H` 121 terms/degree 8, selected base one
term/degree 3, both-live monomial one term/degree 9, remaining-`c` product
32 terms/degree 9, and expanded full product 2,992 terms/degree 29.

The shortest linear pivot is raw 8 (`t_023`), with exact identity

```text
raw8 = (d1-d2)*(a1+a2*b5^2)
       + a5*b5*(d1+d2)-b5^2-2*b5+1.
```

Thus `d1-d2 != 0` solves `a1`; on `d1=d2`, raw 8 leaves the four-term
residual

```text
2*a5*b5*d1-b5^2-2*b5+1=0.
```

This is a structural split only. Neither branch is closed and no
Gröbner/F4SAT/msolve or ideal-membership computation was launched.

Standard, `-O`, and isolated `-I -S` runs agree on logical digest
`f4aa22e5a6c5d3d2dc71ff8e85d9b12df7faf5059c296d40e5d123098637e158`.
