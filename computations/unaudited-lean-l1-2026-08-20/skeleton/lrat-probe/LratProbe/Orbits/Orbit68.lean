/- UNAUDITED — lane L1, generated. Orbit 68 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit68Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_68.cnf")

def orbit68CNF : CNF Nat :=
  orbit68Parsed.map (·.cnf) |>.getD []

theorem orbit68Parsed_ok : orbit68Parsed.isSome = true := by
  native_decide

theorem orbit68Unsat : orbit68CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit68CNF
    (include_str "../../artifacts/n8k4_68.lrat")
  native_decide

end LratProbe.Orbits
