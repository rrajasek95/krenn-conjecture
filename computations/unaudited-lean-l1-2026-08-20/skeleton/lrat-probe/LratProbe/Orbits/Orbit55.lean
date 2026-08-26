/- UNAUDITED — lane L1, generated. Orbit 55 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit55Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_55.cnf")

def orbit55CNF : CNF Nat :=
  orbit55Parsed.map (·.cnf) |>.getD []

theorem orbit55Parsed_ok : orbit55Parsed.isSome = true := by
  native_decide

theorem orbit55Unsat : orbit55CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit55CNF
    (include_str "../../artifacts/n8k4_55.lrat")
  native_decide

end LratProbe.Orbits
