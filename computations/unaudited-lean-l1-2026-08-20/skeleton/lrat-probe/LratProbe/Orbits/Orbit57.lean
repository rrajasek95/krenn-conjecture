/- UNAUDITED — lane L1, generated. Orbit 57 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit57Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_57.cnf")

def orbit57CNF : CNF Nat :=
  orbit57Parsed.map (·.cnf) |>.getD []

theorem orbit57Parsed_ok : orbit57Parsed.isSome = true := by
  native_decide

theorem orbit57Unsat : orbit57CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit57CNF
    (include_str "../../artifacts/n8k4_57.lrat")
  native_decide

end LratProbe.Orbits
