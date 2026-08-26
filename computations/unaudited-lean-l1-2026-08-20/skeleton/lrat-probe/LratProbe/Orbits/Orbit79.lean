/- UNAUDITED — lane L1, generated. Orbit 79 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit79Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_79.cnf")

def orbit79CNF : CNF Nat :=
  orbit79Parsed.map (·.cnf) |>.getD []

theorem orbit79Parsed_ok : orbit79Parsed.isSome = true := by
  native_decide

theorem orbit79Unsat : orbit79CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit79CNF
    (include_str "../../artifacts/n8k4_79.lrat")
  native_decide

end LratProbe.Orbits
