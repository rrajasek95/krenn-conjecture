/- UNAUDITED — lane L1, generated. Orbit 49 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit49Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_49.cnf")

def orbit49CNF : CNF Nat :=
  orbit49Parsed.map (·.cnf) |>.getD []

theorem orbit49Parsed_ok : orbit49Parsed.isSome = true := by
  native_decide

theorem orbit49Unsat : orbit49CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit49CNF
    (include_str "../../artifacts/n8k4_49.lrat")
  native_decide

end LratProbe.Orbits
