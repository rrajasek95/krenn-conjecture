/- UNAUDITED — lane L1, generated. N=6 orbit 2 of 13 (z=0 encoding). -/
import LratProbe.CnfCheck

namespace LratProbe.N6

open Std.Sat
open Std.Tactic.BVDecide
open LratProbe

def orbit2Parsed : Option ParsedDimacs :=
  parseDimacs (include_str "../../artifacts/n6/n6_2.cnf")

def orbit2CNF : CNF Nat :=
  orbit2Parsed.map (·.cnf) |>.getD []

theorem orbit2Parsed_ok : orbit2Parsed.isSome = true := by
  native_decide

theorem orbit2Unsat : orbit2CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit2CNF
    (include_str "../../artifacts/n6/n6_2.lrat")
  native_decide

end LratProbe.N6
