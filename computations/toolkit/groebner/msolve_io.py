#!/usr/bin/env python3
"""Strict parsing and deterministic hashing for the msolve text format."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Iterable


FORBIDDEN_INPUT_TOKENS = ("(", ")", "[", "]", ";")
COEFFICIENT_AFTER_SYMBOL = re.compile(
    r"(?:^|[^A-Za-z0-9_])"
    r"[A-Za-z_][A-Za-z0-9_]*(?:\^\d+)?\*[+-]?\d")


def is_prime_u64(value: int) -> bool:
    """Deterministically test primality for the 64-bit msolve use case."""
    if value < 2:
        return False
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    if value in small_primes:
        return True
    if any(value % prime == 0 for prime in small_primes):
        return False
    if value >= 1 << 64:
        raise ValueError("characteristic exceeds deterministic 64-bit guard")
    odd_part = value - 1
    exponent = 0
    while odd_part % 2 == 0:
        exponent += 1
        odd_part //= 2
    # This base set is deterministic for every unsigned 64-bit integer.
    for base in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if base % value == 0:
            continue
        witness = pow(base, odd_part, value)
        if witness in (1, value - 1):
            continue
        for _ in range(exponent - 1):
            witness = witness * witness % value
            if witness == value - 1:
                break
        else:
            return False
    return True


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalized_polynomial(value: str) -> str:
    return re.sub(r"\s+", "", value)


def polynomial_sha256(value: str) -> str:
    return sha256(normalized_polynomial(value).encode("ascii")).hexdigest()


def logical_input_sha256(variables: Iterable[str], characteristic: int,
                         polynomials: Iterable[str]) -> str:
    payload = {
        "variables": list(variables),
        "characteristic": characteristic,
        "polynomials": [normalized_polynomial(value)
                        for value in polynomials],
    }
    encoded = json.dumps(payload, sort_keys=True,
                         separators=(",", ":")).encode("ascii")
    return sha256(encoded).hexdigest()


def split_polynomial_list(body: str) -> tuple[str, ...]:
    """Split msolve's comma-separated polynomial list.

    Parentheses are deliberately forbidden by the strict input parser, so a
    comma can only be a row separator.  Output bases do not contain commas
    inside a polynomial either.
    """
    return tuple(value.strip() for value in body.split(",") if value.strip())


@dataclass(frozen=True)
class MsolveInput:
    path: Path
    variables: tuple[str, ...]
    characteristic: int
    polynomials: tuple[str, ...]
    file_sha256: str
    logical_sha256: str
    polynomial_sha256: tuple[str, ...]

    def manifest(self, labels: tuple[str, ...] | None = None) -> dict:
        if labels is None:
            labels = tuple(f"row_{index:04d}"
                           for index in range(len(self.polynomials)))
        if len(labels) != len(self.polynomials):
            raise ValueError("label count does not match polynomial count")
        return {
            "path": str(self.path),
            "file_sha256": self.file_sha256,
            "logical_sha256": self.logical_sha256,
            "variables": list(self.variables),
            "characteristic": self.characteristic,
            "polynomial_count": len(self.polynomials),
            "polynomials": [
                {"index": index, "label": label, "sha256": digest}
                for index, (label, digest) in enumerate(
                    zip(labels, self.polynomial_sha256, strict=True))
            ],
        }


def read_msolve_input(path: Path, *, strict: bool = True,
                      allow_characteristic_zero: bool = False) -> MsolveInput:
    text = path.read_text()
    lines = text.splitlines()
    if len(lines) < 3:
        raise ValueError("msolve input needs variables, characteristic, rows")
    variables = tuple(value.strip() for value in lines[0].split(","))
    if not variables or any(not value for value in variables):
        raise ValueError("invalid variable declaration")
    if len(set(variables)) != len(variables):
        raise ValueError("duplicate variable declaration")
    if any(not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value)
           for value in variables):
        raise ValueError("unsupported variable name")
    characteristic = int(lines[1].strip())
    if characteristic == 0 and allow_characteristic_zero:
        pass
    elif not is_prime_u64(characteristic):
        raise ValueError("toolkit requires a prime field characteristic")
    body = "\n".join(lines[2:]).strip()
    polynomials = split_polynomial_list(body)
    if not polynomials:
        raise ValueError("empty polynomial list")
    if strict:
        for index, polynomial in enumerate(polynomials):
            token = next((value for value in FORBIDDEN_INPUT_TOKENS
                          if value in polynomial), None)
            if token is not None:
                raise ValueError(
                    f"row {index} contains forbidden token {token!r}; "
                    "msolve 0.10.1 silently misparses parenthesized "
                    "products, so expand every polynomial first")
            if "**" in polynomial:
                raise ValueError(f"row {index} uses ** instead of ^")
            if COEFFICIENT_AFTER_SYMBOL.search(polynomial):
                raise ValueError(
                    f"row {index} places an integer coefficient after a "
                    "symbolic factor; msolve 0.10.1 silently changes terms "
                    "such as z*2*x, so print coefficients first")
    row_hashes = tuple(polynomial_sha256(value) for value in polynomials)
    return MsolveInput(
        path=path,
        variables=variables,
        characteristic=characteristic,
        polynomials=polynomials,
        file_sha256=file_sha256(path),
        logical_sha256=logical_input_sha256(
            variables, characteristic, polynomials),
        polynomial_sha256=row_hashes,
    )


@dataclass(frozen=True)
class MsolveBasis:
    path: Path
    variables: tuple[str, ...]
    characteristic: int
    declared_length: int
    polynomials: tuple[str, ...]
    kind: str
    unit: bool
    file_sha256: str
    polynomial_sha256: tuple[str, ...]
    leading_monomials: tuple[tuple[int, ...], ...]

    def manifest(self) -> dict:
        return {
            "path": str(self.path),
            "file_sha256": self.file_sha256,
            "kind": self.kind,
            "variables": list(self.variables),
            "characteristic": self.characteristic,
            "declared_length": self.declared_length,
            "parsed_length": len(self.polynomials),
            "unit": self.unit,
            "polynomial_sha256": list(self.polynomial_sha256),
            "leading_monomials": [list(value)
                                  for value in self.leading_monomials],
        }


def parse_monic_leading_monomial(polynomial: str,
                                 variables: tuple[str, ...]) -> tuple[int, ...]:
    """Parse the first (leading) term printed by msolve's reduced basis."""
    value = normalized_polynomial(polynomial)
    if value in {"1", "-1"}:
        return tuple(0 for _ in variables)
    # Prime-field reduced bases are printed monic, with the leading term first.
    first = re.split(r"(?=[+-])", value, maxsplit=1)[0]
    factors = first.split("*")
    if not factors:
        raise ValueError(f"non-monic/unsupported leading term: {first!r}")
    # Full (-g 2) output usually spells the coefficient as ``1*x^1``;
    # leading-ideal-only (-g 1) output emits the same monomial as ``x^1``.
    # Both are monic.  Any other explicit numeric factor remains forbidden.
    if factors[0] == "1":
        factors = factors[1:]
    elif re.fullmatch(r"[+-]?\d+", factors[0]):
        raise ValueError(f"non-monic/unsupported leading term: {first!r}")
    exponents = {name: 0 for name in variables}
    for factor in factors:
        match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*)(?:\^(\d+))?", factor)
        if match is None or match.group(1) not in exponents:
            raise ValueError(f"unsupported leading monomial factor: {factor!r}")
        exponents[match.group(1)] += int(match.group(2) or "1")
    return tuple(exponents[name] for name in variables)


def validate_reduced_leading_monomials(
        monomials: tuple[tuple[int, ...], ...]) -> None:
    if len(set(monomials)) != len(monomials):
        raise ValueError("duplicate leading monomials in reduced basis")
    for left_index, left in enumerate(monomials):
        for right_index, right in enumerate(monomials):
            if left_index == right_index:
                continue
            if all(a <= b for a, b in zip(left, right, strict=True)):
                raise ValueError(
                    "leading monomial divisibility in claimed reduced basis: "
                    f"{left_index} divides {right_index}")


def read_msolve_basis(path: Path, *, require_full: bool = False) -> MsolveBasis:
    text = path.read_text()
    if not text.strip():
        raise ValueError("zero-byte/empty msolve output")
    kind = ("full" if "#Reduced Groebner basis data" in text else
            "leading" if "#Leading ideal data" in text else "solution")
    if require_full and kind != "full":
        raise ValueError("staged elimination requires an msolve -g 2 basis")
    characteristic_match = re.search(
        r"^#field characteristic:\s*(\d+)\s*$", text, re.MULTILINE)
    variables_match = re.search(
        r"^#variable order:\s*(.*?)\s*$", text, re.MULTILINE)
    length_match = re.search(
        r"^#length of basis:\s*(\d+)\s+elements", text, re.MULTILINE)
    if characteristic_match is None or variables_match is None:
        if text.strip() == "[-1]":
            return MsolveBasis(path, (), 0, 1, ("1",), "solution", True,
                               file_sha256(path), (polynomial_sha256("1"),),
                               ((),))
        raise ValueError("missing msolve basis metadata")
    start = text.find("[")
    end = text.rfind("]")
    if start < 0 or end < start:
        raise ValueError("unbalanced/missing bracketed basis")
    # msolve 0.10.1 terminates a serialized basis with ``]:``.  Accept that
    # documented delimiter, but reject any other payload after the bracket.
    trailing = text[end + 1:].strip()
    if trailing not in {"", ":"}:
        raise ValueError("unexpected data after closing basis bracket")
    body = text[start + 1:end].strip()
    polynomials = split_polynomial_list(body)
    declared = int(length_match.group(1)) if length_match else len(polynomials)
    if len(polynomials) != declared:
        raise ValueError(
            f"basis count mismatch: declared {declared}, parsed "
            f"{len(polynomials)}")
    variables = tuple(value.strip() for value in
                      variables_match.group(1).split(","))
    characteristic = int(characteristic_match.group(1))
    if not is_prime_u64(characteristic):
        raise ValueError("basis declares a non-prime characteristic")
    unit = (len(polynomials) == 1 and
            normalized_polynomial(polynomials[0]) in {"1", "-1"})
    hashes = tuple(polynomial_sha256(value) for value in polynomials)
    leading = tuple(parse_monic_leading_monomial(value, variables)
                    for value in polynomials)
    validate_reduced_leading_monomials(leading)
    return MsolveBasis(path, variables, characteristic, declared,
                       polynomials, kind, unit, file_sha256(path), hashes,
                       leading)


def write_input_from_full_basis(basis: MsolveBasis, output: Path) -> None:
    if basis.kind != "full":
        raise ValueError("only a full -g 2 basis can seed a staged run")
    text = (",".join(basis.variables) + "\n" +
            str(basis.characteristic) + "\n" +
            ",\n".join(basis.polynomials) + "\n")
    output.write_text(text)
    # Reparse strictly so no generated stage can bypass the input guard.
    read_msolve_input(output, strict=True)
