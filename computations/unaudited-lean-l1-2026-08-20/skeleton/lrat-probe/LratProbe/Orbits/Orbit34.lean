/- UNAUDITED — lane L1, generated. Orbit 34 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit34Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_34.cnf")

def orbit34CNF : CNF Nat :=
  orbit34Parsed.map (·.cnf) |>.getD []

theorem orbit34Parsed_ok : orbit34Parsed.isSome = true := by
  native_decide

theorem orbit34Unsat : orbit34CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit34CNF
    (include_str "../../artifacts/n8k4_34.lrat")
  native_decide

end LratProbe.Orbits
