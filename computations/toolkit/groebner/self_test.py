#!/usr/bin/env python3
"""Must-fire regression tests for the standardized msolve machinery."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile

from msolve_io import (parse_monic_leading_monomial, read_msolve_basis,
                       read_msolve_input)


PRIME = 1073741827
HERE = Path(__file__).resolve().parent


def write(path: Path, variables: str, polynomials: list[str]) -> None:
    path.write_text(variables + "\n" + str(PRIME) + "\n" +
                    ",\n".join(polynomials) + "\n")


def run(command: list[str]) -> None:
    completed = subprocess.run(command, text=True, capture_output=True,
                               timeout=60, check=False)
    if completed.returncode != 0:
        raise AssertionError(
            f"command failed ({completed.returncode}): {command}\n"
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}")


def main() -> None:
    assert parse_monic_leading_monomial("x^2*y^1", ("x", "y")) == (2, 1)
    assert parse_monic_leading_monomial("1*x^2*y", ("x", "y")) == (2, 1)
    try:
        parse_monic_leading_monomial("2*x^1", ("x",))
    except ValueError:
        pass
    else:
        raise AssertionError("non-monic leading coefficient was accepted")
    with tempfile.TemporaryDirectory(prefix="n8-groebner-selftest-") as raw:
        directory = Path(raw)

        bad = directory / "parenthesized.msolve"
        write(bad, "x,z", ["x", "z*(x)-1"])
        try:
            read_msolve_input(bad, strict=True)
        except ValueError as error:
            assert "forbidden token" in str(error)
        else:
            raise AssertionError("parenthesized Rabinowitsch row was accepted")

        coefficient_after_symbol = directory / "coefficient_after_symbol.msolve"
        write(coefficient_after_symbol, "x,z", ["x-2", "z*2*x-1"])
        try:
            read_msolve_input(coefficient_after_symbol, strict=True)
        except ValueError as error:
            assert "coefficient after a symbolic factor" in str(error)
        else:
            raise AssertionError(
                "coefficient-after-symbol msolve ambiguity was accepted")

        composite = directory / "composite.msolve"
        composite.write_text("x\n1073741825\nx\n")
        try:
            read_msolve_input(composite, strict=True)
        except ValueError as error:
            assert "prime field" in str(error)
        else:
            raise AssertionError("composite characteristic was accepted")

        rab = directory / "rabinowitsch.msolve"
        rab_out = directory / "rabinowitsch.out"
        write(rab, "x,z", ["x", "z*x-1"])
        run(["msolve", "-f", str(rab), "-o", str(rab_out),
             "-g", "2", "-t", "2"])
        assert read_msolve_basis(rab_out, require_full=True).unit

        canonical_coefficient = directory / "canonical_coefficient.msolve"
        canonical_coefficient_out = directory / "canonical_coefficient.out"
        write(canonical_coefficient, "x,z", ["x-2", "2*x*z-1"])
        read_msolve_input(canonical_coefficient, strict=True)
        run(["msolve", "-f", str(canonical_coefficient), "-o",
             str(canonical_coefficient_out), "-g", "2", "-t", "2"])
        canonical_basis = read_msolve_basis(
            canonical_coefficient_out, require_full=True)
        assert any("4*z" in polynomial or "z" in polynomial
                   for polynomial in canonical_basis.polynomials)

        sat = directory / "saturation.msolve"
        sat_out = directory / "saturation.out"
        # Nondegenerate F4SAT must-fire: <xy,xz>:x^infinity = <y,z>.
        # msolve 0.10.1 has a false-negative corner case when the saturator is
        # literally duplicated as an ideal generator, so that is not a useful
        # engine regression.
        write(sat, "x,y,z", ["x*y", "x*z", "x"])
        run(["msolve", "-f", str(sat), "-o", str(sat_out),
             "-S", "-g", "2", "-t", "2"])
        sat_basis = read_msolve_basis(sat_out, require_full=True)
        assert {polynomial.replace("1*", "")
                for polynomial in sat_basis.polynomials} == {"y^1", "z^1"}

        staged = directory / "staged.msolve"
        write(staged, "x,y", ["x-y", "y^2-1", "x"])
        prefix = directory / "staged"
        run([sys.executable, str(HERE / "run_msolve.py"), str(staged),
             "--output-prefix", str(prefix),
             "--mode", "saturate-eliminate", "--eliminate", "1",
             "--threads", "2", "--timeout", "60",
             "--scope", "toolkit staged saturation/elimination self-test",
             "--saturator-label", "x"])
        final = read_msolve_basis(
            Path(str(prefix) + ".elim.full.gb.out"), require_full=True)
        assert not final.unit
        assert any("y^2" in polynomial for polynomial in final.polynomials)

        checker = directory / "checker.py"
        checker.write_text(
            "import hashlib,json,sys\n"
            "from pathlib import Path\n"
            "v={'value':7}\n"
            "v['logical_sha256']=hashlib.sha256(b'value=7').hexdigest()\n"
            "Path(sys.argv[1]).write_text(json.dumps(v,sort_keys=True)+'\\n')\n")
        artifact = directory / "checker.json"
        checker_manifest = directory / "checker.manifest.json"
        run([sys.executable, str(HERE / "run_checker_modes.py"),
             "--artifact", str(artifact), "--manifest", str(checker_manifest),
             "--scope", "toolkit checker-mode self-test", str(checker),
             "--", str(artifact)])
        checker_result = __import__("json").loads(
            checker_manifest.read_text())
        assert checker_result["status"] == "completed_exact_replay"

    print("groebner toolkit self-test: PASS")


if __name__ == "__main__":
    main()
