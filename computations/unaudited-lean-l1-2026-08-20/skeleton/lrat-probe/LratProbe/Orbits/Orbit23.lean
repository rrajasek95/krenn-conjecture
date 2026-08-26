/- UNAUDITED — lane L1, generated. Orbit 23 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit23Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_23.cnf")

def orbit23CNF : CNF Nat :=
  orbit23Parsed.map (·.cnf) |>.getD []

theorem orbit23Parsed_ok : orbit23Parsed.isSome = true := by
  native_decide

theorem orbit23Unsat : orbit23CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit23CNF
    (include_str "../../artifacts/n8k4_23.lrat")
  native_decide

end LratProbe.Orbits
