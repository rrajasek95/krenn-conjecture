/- UNAUDITED — lane L1, generated. Orbit 37 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit37Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_37.cnf")

def orbit37CNF : CNF Nat :=
  orbit37Parsed.map (·.cnf) |>.getD []

theorem orbit37Parsed_ok : orbit37Parsed.isSome = true := by
  native_decide

theorem orbit37Unsat : orbit37CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit37CNF
    (include_str "../../artifacts/n8k4_37.lrat")
  native_decide

end LratProbe.Orbits
