use std::fs::File;
use std::io::{BufReader,Read};
use std::convert::TryInto;
const D:&str="computations/unaudited-codex-orbit0-k19-profile-census-2026-08-23/";
struct S{r:BufReader<File>,left:u64,cur:Option<[u8;43]>}
impl S{fn new(name:&str)->Self{let mut r=BufReader::with_capacity(1<<20,File::open(format!("{}keys_{}.bin",D,name)).unwrap());let mut h=[0;16];r.read_exact(&mut h).unwrap();assert_eq!(&h[..8],b"K19KEY1\0");let left=u64::from_le_bytes(h[8..].try_into().unwrap());let mut s=Self{r,left,cur:None};s.bump();s}fn bump(&mut self){if self.left==0{self.cur=None}else{let mut x=[0;43];self.r.read_exact(&mut x).unwrap();self.left-=1;self.cur=Some(x)}}}
fn main(){let mut a=[S::new("direct"),S::new("k14"),S::new("k15")];let mut mask=[0u64;8];loop{let m=a.iter().filter_map(|s|s.cur).min();if m.is_none(){break}let x=m.unwrap();let mut b=0;for i in 0..3{if a[i].cur==Some(x){b|=1<<i;a[i].bump()}}mask[b]+=1}let union:u64=mask.iter().sum();let text=format!("{{\"status\":\"PASS_EXACT_SORTED_KEY_MERGE\",\"union_unique_enriched_keys\":{},\"mask_counts\":{{\"direct_only\":{},\"k14_only\":{},\"direct_k14\":{},\"k15_only\":{},\"direct_k15\":{},\"k14_k15\":{},\"all_three\":{}}}}}",union,mask[1],mask[2],mask[3],mask[4],mask[5],mask[6],mask[7]);std::fs::write(format!("{}results_key_union.json",D),&text).unwrap();println!("{}",text)}
