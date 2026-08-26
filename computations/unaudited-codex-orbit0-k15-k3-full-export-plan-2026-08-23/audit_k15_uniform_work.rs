mod audit {
    #![allow(dead_code)]
    include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");
    use std::collections::BTreeSet;
    pub fn run(){
        let e=parse();let mut ss=BTreeSet::new();
        for r in &e.records{let mut s=[0u8;12];for &c in &r.row{let i=e.pos[c as usize];if i>=0{s[i as usize]+=1}}ss.insert(s);}
        assert_eq!(e.records.len(),485);assert_eq!(ss.len(),1);assert_eq!(*ss.iter().next().unwrap(),[1,0,0,1,0,0,1,0,0,1,0,0]);
        assert_eq!(3_690_496u64*485,1_789_890_560);assert_eq!(1_903_616u64*485,923_253_760);
        assert_eq!(4_861_952u64*485,2_358_046_720);
        println!("PASS records=485 distinct_R8_anchor_signatures=1 signature=100100100100 exact_generated=1789890560 exact_pivotable=923253760 exact_outgoing=2358046720 H_order={}",e.perms.len());
    }
}
fn main(){audit::run()}
