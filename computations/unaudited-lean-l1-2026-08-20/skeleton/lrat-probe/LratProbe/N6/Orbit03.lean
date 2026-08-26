/- UNAUDITED — lane L1, generated. N=6 orbit 3 of 13 (z=0 encoding). -/
import LratProbe.CnfCheck

namespace LratProbe.N6

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit3Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n6/n6_3.cnf")

def orbit3CNF : CNF Nat :=
  orbit3Parsed.map (·.cnf) |>.getD []

theorem orbit3Parsed_ok : orbit3Parsed.isSome = true := by
  native_decide

theorem orbit3Unsat : orbit3CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit3CNF
    (include_str "../../artifacts/n6/n6_3.lrat")
  native_decide

end LratProbe.N6
