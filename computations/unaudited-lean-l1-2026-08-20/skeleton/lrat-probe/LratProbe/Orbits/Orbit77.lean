/- UNAUDITED — lane L1, generated. Orbit 77 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit77Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_77.cnf")

def orbit77CNF : CNF Nat :=
  orbit77Parsed.map (·.cnf) |>.getD []

theorem orbit77Parsed_ok : orbit77Parsed.isSome = true := by
  native_decide

theorem orbit77Unsat : orbit77CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit77CNF
    (include_str "../../artifacts/n8k4_77.lrat")
  native_decide

end LratProbe.Orbits
