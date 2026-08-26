/- UNAUDITED — lane L1, generated. Orbit 69 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit69Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_69.cnf")

def orbit69CNF : CNF Nat :=
  orbit69Parsed.map (·.cnf) |>.getD []

theorem orbit69Parsed_ok : orbit69Parsed.isSome = true := by
  native_decide

theorem orbit69Unsat : orbit69CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit69CNF
    (include_str "../../artifacts/n8k4_69.lrat")
  native_decide

end LratProbe.Orbits
