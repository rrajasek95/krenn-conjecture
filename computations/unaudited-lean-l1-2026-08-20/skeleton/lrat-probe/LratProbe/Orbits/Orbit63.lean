/- UNAUDITED — lane L1, generated. Orbit 63 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit63Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_63.cnf")

def orbit63CNF : CNF Nat :=
  orbit63Parsed.map (·.cnf) |>.getD []

theorem orbit63Parsed_ok : orbit63Parsed.isSome = true := by
  native_decide

theorem orbit63Unsat : orbit63CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit63CNF
    (include_str "../../artifacts/n8k4_63.lrat")
  native_decide

end LratProbe.Orbits
