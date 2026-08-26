/- UNAUDITED — lane L1, generated. Orbit 21 of the 87 N=8 diagonal cases. -/
import LratProbe.CnfCheck

namespace LratProbe.Orbits

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit21Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n8k4_21.cnf")

def orbit21CNF : CNF Nat :=
  orbit21Parsed.map (·.cnf) |>.getD []

theorem orbit21Parsed_ok : orbit21Parsed.isSome = true := by
  native_decide

theorem orbit21Unsat : orbit21CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit21CNF
    (include_str "../../artifacts/n8k4_21.lrat")
  native_decide

end LratProbe.Orbits
