use std::collections::BTreeMap;
use std::convert::TryInto;
use std::fs::File;
use std::io::{BufReader, Read};

fn main() {
    let path="computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/hidden_k16_decorated_pair_orbits_full.bin";
    let mut r=BufReader::with_capacity(8<<20,File::open(path).unwrap());
    let mut h=[0u8;80];r.read_exact(&mut h).unwrap();
    assert_eq!(&h[..8],b"H16ORM1\0");
    assert_eq!(i128::from_le_bytes(h[8..24].try_into().unwrap()),400_591_699_200);
    assert_eq!(u16::from_le_bytes(h[28..30].try_into().unwrap()),53);
    let zero=u64::from_le_bytes(h[40..48].try_into().unwrap());
    let n=u64::from_le_bytes(h[48..56].try_into().unwrap());
    let expected=i128::from_le_bytes(h[64..80].try_into().unwrap());
    let mut hist=BTreeMap::<u16,u64>::new();let mut sum=0i128;let mut uses=0u128;
    let mut prior:Option<[u8;25]>=None;
    for _ in 0..n {let mut b=[0u8;53];r.read_exact(&mut b).unwrap();
        let key:[u8;25]=b[..25].try_into().unwrap();if let Some(p)=prior{assert!(p<key)}prior=Some(key);
        let w=i128::from_le_bytes(b[25..41].try_into().unwrap());assert_ne!(w,0);sum+=w;
        uses+=u64::from_le_bytes(b[41..49].try_into().unwrap())as u128;
        let os=u16::from_le_bytes(b[49..51].try_into().unwrap());let ss=u16::from_le_bytes(b[51..53].try_into().unwrap());
        assert_eq!(u32::from(os)*u32::from(ss),384);*hist.entry(ss).or_default()+=1;
    }
    let mut eof=[0];assert_eq!(r.read(&mut eof).unwrap(),0);assert_eq!(sum,expected);
    println!("{{\"status\":\"PASS_PAIR_LEDGER_STREAM_REFEREE\",\"count\":{},\"orbit_zero\":{},\"weight_sum_scaled\":\"{}\",\"uses_sum\":\"{}\",\"stabilizer_histogram\":\"{:?}\"}}",n,zero,sum,uses,hist);
}
