#!/usr/bin/env python3
"""Raw generator for branch-zero, off-diagonal-base defect strata.

Discovery helper only.  On edge e use [a_e,b_e,c_e,d_e] with
c_e=-(1+a_e*d_e)/b_e, and set d_e=0 off the requested defect set.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
import argparse
import importlib.util
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
SCREEN_PATH = HERE / "screen_lowq_joint_branch_orbits.py"


def load():
    spec = importlib.util.spec_from_file_location("n8_defect_screen", SCREEN_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SCREEN = load()


class Chart:
    def __init__(self, defects):
        self.defects = tuple(sorted(defects))
        self.n = 12 + len(self.defects)
        self.d_index = {edge: 12 + index
                        for index, edge in enumerate(self.defects)}
        self.one = {(0,) * self.n: F(1)}
        self.names = ([f"a{i}" for i in range(6)]
                      + [f"b{i}" for i in range(6)]
                      + [f"d{i}" for i in self.defects])
        self.entries = self._entries()

    @staticmethod
    def clean(poly):
        return {monomial: coefficient for monomial, coefficient in poly.items()
                if coefficient}

    def add(self, *polys):
        answer = Counter()
        for poly in polys:
            answer.update(poly)
        return self.clean(answer)

    def scale(self, poly, coefficient):
        return self.clean({monomial: F(coefficient) * value
                           for monomial, value in poly.items()})

    def multiply(self, *polys):
        answer = self.one
        for poly in polys:
            updated = Counter()
            for left, left_coefficient in answer.items():
                for right, right_coefficient in poly.items():
                    exponent = tuple(a + b for a, b in zip(left, right))
                    updated[exponent] += left_coefficient * right_coefficient
            answer = self.clean(updated)
        return answer

    def variable(self, index, exponent=1):
        powers = [0] * self.n
        powers[index] = exponent
        return {tuple(powers): F(1)}

    def _entries(self):
        answer = []
        for edge in range(6):
            a_value, b_value = self.variable(edge), self.variable(6 + edge)
            d_value = (self.variable(self.d_index[edge])
                       if edge in self.d_index else {})
            c_value = self.scale(self.variable(6 + edge, -1), -1)
            if d_value:
                c_value = self.add(c_value, self.scale(self.multiply(
                    a_value, d_value, self.variable(6 + edge, -1)), -1))
            answer.extend((a_value, b_value, c_value, d_value))
        return tuple(answer)

    def substitute(self, raw_poly):
        answer = {}
        for monomial, coefficient in raw_poly.items():
            term = self.scale(self.one, coefficient)
            for raw_variable in monomial:
                term = self.multiply(term, self.entries[raw_variable])
            answer = self.add(answer, term)
        return answer

    def clear_denominators(self, poly):
        shifts = tuple(-min([monomial[index] for monomial in poly] + [0])
                       for index in range(self.n))
        return {tuple(exponent + shift for exponent, shift
                      in zip(monomial, shifts)): coefficient
                for monomial, coefficient in poly.items()}

    def singular(self, poly):
        pieces = []
        for exponent, coefficient in sorted(poly.items()):
            factors = [self.names[index] +
                       (f"^{power}" if power != 1 else "")
                       for index, power in enumerate(exponent) if power]
            body = "*".join(factors) or "1"
            magnitude = abs(coefficient)
            if magnitude != 1:
                body = f"{magnitude.numerator}/{magnitude.denominator}*{body}"
            pieces.append(("-" if coefficient < 0 else
                           ("+" if pieces else "")) + body)
        return "".join(pieces) or "0"

    def rows_and_hafnian(self):
        equations, hafnian = SCREEN.PROBE.equations(SCREEN.branch_bits(0))
        rows, seen = [], set()
        for index, raw in enumerate(equations):
            specialized = self.substitute(raw)
            if not specialized:
                continue
            cleared = self.clear_denominators(specialized)
            encoded = self.singular(cleared)
            if encoded in seen:
                continue
            seen.add(encoded)
            rows.append((index, cleared, encoded))
        literal_h = self.substitute(hafnian)
        return tuple(rows), literal_h, self.clear_denominators(literal_h)

    def command(self, characteristic, order="dp"):
        rows, _, hafnian = self.rows_and_hafnian()
        live = [f"b{i}" for i in range(6)]
        live += [f"a{edge}*d{edge}" for edge in self.defects]
        names = ",".join(self.names + ["u"])
        return (
            f"ring R={characteristic},({names}),{order};"
            f"ideal I={','.join(row[2] for row in rows)},"
            f"u*({self.singular(hafnian)})*({'*'.join(live)})-1;"
            'ideal G=slimgb(I);print("BEGIN");reduce(1,G);'
            'print(size(G));print("END");quit;'
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("defects", nargs="*", type=int)
    parser.add_argument("--characteristic", type=int, default=1009)
    parser.add_argument("--timeout", type=float, default=10)
    parser.add_argument("--print-rows", action="store_true")
    args = parser.parse_args()
    chart = Chart(args.defects)
    rows, _, hafnian = chart.rows_and_hafnian()
    print("defects / rows / H terms:", chart.defects, len(rows), len(hafnian))
    if args.print_rows:
        for index, _, encoded in rows:
            print(index, encoded)
    try:
        completed = subprocess.run(
            ["Singular", "-q", "-c", chart.command(args.characteristic)],
            text=True, capture_output=True, timeout=args.timeout, check=False)
        print("returncode:", completed.returncode)
        print(completed.stdout[-1000:])
        print(completed.stderr[-500:])
    except subprocess.TimeoutExpired:
        print("TIMEOUT")


if __name__ == "__main__":
    main()
