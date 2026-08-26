/- UNAUDITED — lane L1, generated. Orbit 43 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit43Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_43.cnf")

def orbit43CNF : CNF Nat :=
  orbit43Parsed.map (·.cnf) |>.getD []

theorem orbit43Parsed_ok : orbit43Parsed.isSome = true := by
  native_decide

theorem orbit43Unsat : orbit43CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit43CNF
    (include_str "../../artifacts/n8k4_43.lrat")
  native_decide

end LratProbe.Orbits
