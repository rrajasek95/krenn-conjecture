/- UNAUDITED — lane L1, generated. Orbit 16 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit16Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_16.cnf")

def orbit16CNF : CNF Nat :=
  orbit16Parsed.map (·.cnf) |>.getD []

theorem orbit16Parsed_ok : orbit16Parsed.isSome = true := by
  native_decide

theorem orbit16Unsat : orbit16CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit16CNF
    (include_str "../../artifacts/n8k4_16.lrat")
  native_decide

end LratProbe.Orbits
