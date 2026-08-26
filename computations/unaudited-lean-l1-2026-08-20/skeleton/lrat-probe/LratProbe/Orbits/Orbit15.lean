/- UNAUDITED — lane L1, generated. Orbit 15 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit15Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_15.cnf")

def orbit15CNF : CNF Nat :=
  orbit15Parsed.map (·.cnf) |>.getD []

theorem orbit15Parsed_ok : orbit15Parsed.isSome = true := by
  native_decide

theorem orbit15Unsat : orbit15CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit15CNF
    (include_str "../../artifacts/n8k4_15.lrat")
  native_decide

end LratProbe.Orbits
