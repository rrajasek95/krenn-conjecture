//! Independent sparse two-prime rank referee for a K17 colour-content shell.
//!
//! Binary input (little endian): magic `K17CCR1\0`; u32 scope (1 literal,
//! 2 abstract), u32 coordinate_count, u32 vector_count; then target and each
//! vector as u32 nnz followed by nnz `(u32 coordinate, i64 coefficient)` pairs.
use std::collections::BTreeMap;
use std::convert::TryInto;
use std::env;
use std::fs::{read,write};
use std::time::Instant;

const DIR:&str="computations/unaudited-codex-orbit0-k17-colour-content-rank-referee-2026-08-23/";

fn u32le(x:&[u8])->u32{u32::from_le_bytes(x.try_into().unwrap())}
fn i64le(x:&[u8])->i64{i64::from_le_bytes(x.try_into().unwrap())}
fn read_vector(b:&[u8],p:&mut usize,ncoords:usize)->Vec<(u32,i64)>{
    let n=u32le(&b[*p..*p+4])as usize;*p+=4;let mut out=Vec::with_capacity(n);let mut previous=None;
    for _ in 0..n{let c=u32le(&b[*p..*p+4]);*p+=4;let v=i64le(&b[*p..*p+8]);*p+=8;
        assert!((c as usize)<ncoords&&v!=0);if let Some(old)=previous{assert!(old<c)}previous=Some(c);out.push((c,v))}out
}
fn modulo(x:i64,p:u32)->u32{let y=x%(p as i64);if y<0{(y+p as i64)as u32}else{y as u32}}
fn mul(a:u32,b:u32,p:u32)->u32{((a as u64*b as u64)%(p as u64))as u32}
fn inverse(x:u32,p:u32)->u32{let(mut a,mut b,mut u,mut v)=(x as i64,p as i64,1i64,0i64);while b!=0{let q=a/b;(a,b)=(b,a-q*b);(u,v)=(v,u-q*v)}assert_eq!(a,1);modulo(u,p)}

struct Basis{p:u32,rows:Vec<Option<Vec<(u32,u32)>>>,rank:usize}
impl Basis{
    fn new(p:u32,n:usize)->Self{Self{p,rows:vec![None;n],rank:0}}
    fn reduce(&self,input:&[(u32,i64)])->BTreeMap<u32,u32>{
        let mut x=BTreeMap::new();for &(c,v)in input{let z=modulo(v,self.p);if z!=0{x.insert(c,z);}}
        loop{let Some((&pivot,&value))=x.first_key_value()else{return x};let Some(row)=&self.rows[pivot as usize]else{return x};
            // Stored basis rows are monic at their first coordinate.
            for &(c,a) in row{let old=*x.get(&c).unwrap_or(&0);let sub=mul(value,a,self.p);let new=if old>=sub{old-sub}else{old+self.p-sub};if new==0{x.remove(&c);}else{x.insert(c,new);}}
        }
    }
    fn insert(&mut self,input:&[(u32,i64)])->bool{let x=self.reduce(input);let Some((&pivot,&value))=x.first_key_value()else{return false};let inv=inverse(value,self.p);
        let row=x.into_iter().map(|(c,a)|(c,mul(a,inv,self.p))).collect();assert!(self.rows[pivot as usize].is_none());self.rows[pivot as usize]=Some(row);self.rank+=1;true}
    fn normal_form(&self,input:&[(u32,i64)])->BTreeMap<u32,u32>{
        let mut x=BTreeMap::new();for &(c,v)in input{let z=modulo(v,self.p);if z!=0{x.insert(c,z);}}
        let mut cursor=0u32;
        while (cursor as usize)<self.rows.len(){let Some((&pivot,&value))=x.range(cursor..).next()else{break};let Some(row)=&self.rows[pivot as usize]else{cursor=pivot+1;continue};
            for &(c,a)in row{let old=*x.get(&c).unwrap_or(&0);let sub=mul(value,a,self.p);let new=if old>=sub{old-sub}else{old+self.p-sub};if new==0{x.remove(&c);}else{x.insert(c,new);}}
        }x
    }
}

fn main(){let start=Instant::now();let args:Vec<_>=env::args().collect();assert_eq!(args.len(),2,"usage: rank_colour_content_shell INPUT.bin");let b=read(&args[1]).unwrap();let mut q=0usize;
    assert_eq!(&b[q..q+8],b"K17CCR1\0");q+=8;let scope=u32le(&b[q..q+4]);q+=4;assert!(scope==1||scope==2);let ncoords=u32le(&b[q..q+4])as usize;q+=4;let nvec=u32le(&b[q..q+4])as usize;q+=4;
    if ncoords>100_000||nvec>100_000{println!("{{\"status\":\"CENSUS_CAP\",\"scope\":{},\"coordinates\":{},\"vectors\":{},\"cap\":100000}}",scope,ncoords,nvec);return}
    let target=read_vector(&b,&mut q,ncoords);let mut vectors=Vec::with_capacity(nvec);let mut nnz=0usize;for _ in 0..nvec{let x=read_vector(&b,&mut q,ncoords);nnz+=x.len();vectors.push(x)}assert_eq!(q,b.len());
    let mut parts=Vec::new();for prime in [32003u32,32009u32]{let mut basis=Basis::new(prime,ncoords);for x in &vectors{basis.insert(x);}let remainder=basis.normal_form(&target);let inside=remainder.is_empty();
        let mut text=String::from("coordinate_id\tresidue\n");for(c,v)in &remainder{text.push_str(&format!("{}\t{}\n",c,v));}write(format!("{}target_remainder_p{}.tsv",DIR,prime),text).unwrap();
        parts.push(format!("{{\"prime\":{},\"rank\":{},\"augmented_rank\":{},\"target_in_span\":{},\"target_remainder_nnz\":{}}}",prime,basis.rank,basis.rank+(!inside as usize),inside,remainder.len()));}
    let output=format!("{{\"status\":\"PARTIAL_SHELL_TWO_PRIME_RANK\",\"scope_code\":{},\"scope\":\"{}\",\"coordinates\":{},\"vectors\":{},\"vector_nnz\":{},\"target_nnz\":{},\"results\":[{}],\"elapsed_seconds\":{:.3},\"inference_guard\":\"capped target-rooted literal first shell only; modular quotient rank, not full-shell membership\"}}\n",scope,if scope==1{"literal_source_columns"}else{"abstract_necessary_quotient"},ncoords,nvec,nnz,target.len(),parts.join(","),start.elapsed().as_secs_f64());write(format!("{}results_colour_content_rank.json",DIR),&output).unwrap();print!("{}",output);
}
