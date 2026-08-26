/- UNAUDITED — lane L1, generated. Orbit 11 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit11Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_11.cnf")

def orbit11CNF : CNF Nat :=
  orbit11Parsed.map (·.cnf) |>.getD []

theorem orbit11Parsed_ok : orbit11Parsed.isSome = true := by
  native_decide

theorem orbit11Unsat : orbit11CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit11CNF
    (include_str "../../artifacts/n8k4_11.lrat")
  native_decide

end LratProbe.Orbits
