/- UNAUDITED — lane L1, generated. Orbit 64 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit64Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_64.cnf")

def orbit64CNF : CNF Nat :=
  orbit64Parsed.map (·.cnf) |>.getD []

theorem orbit64Parsed_ok : orbit64Parsed.isSome = true := by
  native_decide

theorem orbit64Unsat : orbit64CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit64CNF
    (include_str "../../artifacts/n8k4_64.lrat")
  native_decide

end LratProbe.Orbits
