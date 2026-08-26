# k5 full interior `0:63:31`, branch `d1=d2`

Status: **source-faithful exact export PASS; sole 600-second characteristic-zero gate TIMEOUT**.

The canonical parent gauge is `b0=b1=b2=d0=1`.  Substituting `d2=d1`
turns raw row 8 into

```
2*a5*b5*d1 - b5^2 - 2*b5 + 1.
```

All sixteen literal source rows `6..21` were retained.  The exact original
live product after substitution retains the multiplicity `d1^2`; its expanded
Rabinowitsch localizer has 2,464 terms.  The canonical coefficient-first
input has SHA256

```
6120bec2f1c4d9c38aeb44f2dd853ff48f6925066f709629d977a39c9a0a1252
```

The one authorized exact char0 `msolve` run terminated after 600.333 seconds
with return `-15`, zero-byte output, and no sentinel.  This is not an
algebraic verdict.  The timeout/source auditor rejects the zero-byte file as
a RUR or unit certificate and passes source-sign, Rabinowitsch, and sentinel
mutations.

Standard, `-O`, and isolated `-I -S` timeout replays passed with respective
digests `ef8b26df...`, `89802562...`, and `ef391c93...`.  The source export
logical digest is
`d6b035ed2be1e2b343fabea0639bd009dd7a866582dbd88b4e306c8be529d24c`.

Scope: only the `d1=d2` branch of `0:63:31`; the sibling is handled by the
separate structural package and no closure is claimed here.
