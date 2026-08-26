/- UNAUDITED — lane L1, generated. Orbit 5 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit5Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_5.cnf")

def orbit5CNF : CNF Nat :=
  orbit5Parsed.map (·.cnf) |>.getD []

theorem orbit5Parsed_ok : orbit5Parsed.isSome = true := by
  native_decide

theorem orbit5Unsat : orbit5CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit5CNF
    (include_str "../../artifacts/n8k4_5.lrat")
  native_decide

end LratProbe.Orbits
