//! Independent hash-aggregate referee for the 31-way sorted profile merge.
use std::collections::HashMap;
use std::convert::TryInto;
use std::fs::{File,write};
use std::io::{BufReader,Read};
use std::time::Instant;

const DIR:&str="computations/unaudited-codex-orbit0-k14-hidden-k16-parent-full-2026-08-23/";
const U:i128=400_591_699_200;

fn main(){
    let begun=Instant::now();
    let mut map:HashMap<[u8;43],i128>=HashMap::with_capacity(6_700_000);
    let(mut inputs,mut input_sum)=(0u64,0i128);
    for start in(0..485usize).step_by(16){
        let end=(start+16).min(485);
        let path=format!("{}profiles_{:03}_{:03}.bin",DIR,start,end);
        let mut reader=BufReader::with_capacity(1<<20,File::open(path).unwrap());
        let mut header=[0u8;40];reader.read_exact(&mut header).unwrap();
        assert_eq!(&header[..8],b"H16PF2\0\0");
        assert_eq!(i128::from_le_bytes(header[8..24].try_into().unwrap()),U);
        assert_eq!((u16::from_le_bytes(header[24..26].try_into().unwrap())as usize,
                    u16::from_le_bytes(header[26..28].try_into().unwrap())as usize,
                    u16::from_le_bytes(header[28..30].try_into().unwrap())),
                   (start,end,59));
        let count=u64::from_le_bytes(header[32..40].try_into().unwrap());
        for _ in 0..count{
            let mut key=[0u8;43];let mut value=[0u8;16];
            reader.read_exact(&mut key).unwrap();reader.read_exact(&mut value).unwrap();
            let value=i128::from_le_bytes(value);assert_ne!(value,0);assert_eq!(key[42],0);
            *map.entry(key).or_default()+=value;inputs+=1;input_sum+=value;
        }
        let mut extra=[0u8;1];assert_eq!(reader.read(&mut extra).unwrap(),0);
    }
    let distinct=map.len()as u64;
    let zeros=map.values().filter(|&&value|value==0).count()as u64;
    let mut nonzero:Vec<_>=map.into_iter().filter(|(_,value)|*value!=0).collect();
    nonzero.sort_unstable_by_key(|(key,_)|*key);
    let output_sum:i128=nonzero.iter().map(|(_,value)|*value).sum();
    assert_eq!(input_sum,output_sum);

    let path=format!("{}hidden_k16_second_pivot_profiles_full.bin",DIR);
    let mut reader=BufReader::with_capacity(1<<20,File::open(path).unwrap());
    let mut header=[0u8;32];reader.read_exact(&mut header).unwrap();
    assert_eq!(&header[..8],b"H16MER2\0");
    assert_eq!(i128::from_le_bytes(header[8..24].try_into().unwrap()),U);
    assert_eq!(u64::from_le_bytes(header[24..32].try_into().unwrap()),nonzero.len()as u64);
    for (expected_key,expected_value) in &nonzero{
        let mut key=[0u8;43];let mut value=[0u8;16];
        reader.read_exact(&mut key).unwrap();reader.read_exact(&mut value).unwrap();
        assert_eq!(&key,expected_key);assert_eq!(i128::from_le_bytes(value),*expected_value);
    }
    let mut extra=[0u8;1];assert_eq!(reader.read(&mut extra).unwrap(),0);
    assert_eq!((inputs,distinct,zeros,nonzero.len()as u64),
               (21_116_357,6_585_438,355_738,6_229_700));
    let text=format!("{{\"status\":\"PASS_INDEPENDENT_EXACT_PROFILE_MERGE\",\"input_records\":{},\"distinct_keys\":{},\"exact_zero_keys\":{},\"output_nonzero_keys\":{},\"signed_sum_scaled\":\"{}\",\"elapsed_seconds\":{:.6}}}\n",inputs,distinct,zeros,nonzero.len(),output_sum,begun.elapsed().as_secs_f64());
    write("computations/unaudited-codex-orbit0-k14-hidden-parent-full-referee-2026-08-23/results_profile_merge_referee.json",text.as_bytes()).unwrap();
    print!("{}",text);
}
