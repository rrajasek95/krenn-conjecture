mod production {
    #![allow(dead_code)]
    include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");

    use std::collections::BTreeMap;
    use std::env;
    use std::fs::{metadata, File, rename};
    use std::io::{BufReader, BufWriter, Read, Write};
    use std::path::Path;

    const U: i128 = 400_591_699_200;
    const HEADER: usize = 96;
    const RECORD: usize = 104;
    const INPUT_N: usize = 24_097_095;

    #[derive(Clone,Copy,Eq,Hash,Ord,PartialEq,PartialOrd)]
    struct PKey { profile:[u8;29], sig:[u8;12], p2:u8 }

    #[derive(Clone,Copy,Eq,Ord,PartialEq,PartialOrd)]
    struct Witness {
        row:[u8;24], source:u64, p1:u8, tail1:u8, p2:u8,
        m1:u8, m2:u8, packet:u8,
    }

    #[derive(Clone,Copy,Eq,PartialEq)]
    struct Value { weight:i128, uses:u64, witness:Witness }

    #[derive(Default,Eq,PartialEq)]
    struct Stats {
        sources:u64, pivotable_sources:u64, generated:u64, pivotable:u64,
        outgoing_uses:u64, contribution_weight:i128, emitted_records:u64,
        emitted_weight:i128, parts:u64, cache_states:u64,
        denom:BTreeMap<(usize,usize),u64>,
    }

    struct Sink { prefix:String, key_cap:usize, map:HashMap<PKey,Value>, stats:Stats }

    impl Sink {
        fn new(prefix:String,key_cap:usize)->Self {
            assert!(key_cap>0);
            Self{prefix,key_cap,map:HashMap::new(),stats:Stats::default()}
        }
        fn add(&mut self,key:PKey,weight:i128,witness:Witness) {
            self.stats.outgoing_uses+=1;
            self.stats.contribution_weight+=weight;
            let mut delete=false;
            match self.map.get_mut(&key) {
                Some(v)=>{v.weight+=weight;v.uses+=1;if witness<v.witness{v.witness=witness}delete=v.weight==0},
                None=>{self.map.insert(key,Value{weight,uses:1,witness});}
            }
            if delete { self.map.remove(&key); }
            if self.map.len()>=self.key_cap { self.flush(); }
        }
        fn flush(&mut self) {
            if self.map.is_empty(){return}
            let mut rows:Vec<_>=self.map.drain().collect();
            rows.sort_unstable_by_key(|x|x.0);
            let part=self.stats.parts;
            let dst=format!("{}.part{:06}.bin",self.prefix,part);
            let tmp=format!("{}.tmp",dst);
            assert!(!Path::new(&dst).exists()&&!Path::new(&tmp).exists(),"refusing overwrite {}",dst);
            let count=rows.len() as u64;
            let uses:u64=rows.iter().map(|x|x.1.uses).sum();
            let weight:i128=rows.iter().map(|x|x.1.weight).sum();
            let mut h=[0u8;HEADER];
            h[..8].copy_from_slice(b"K18PRF2\0");
            h[8..12].copy_from_slice(&2u32.to_le_bytes());
            h[12]=3; h[13]=2;
            h[14..16].copy_from_slice(&(RECORD as u16).to_le_bytes());
            h[16..24].copy_from_slice(&(U as u64).to_le_bytes());
            h[24..32].copy_from_slice(&part.to_le_bytes());
            h[32..40].copy_from_slice(&count.to_le_bytes());
            h[40..48].copy_from_slice(&uses.to_le_bytes());
            h[48..64].copy_from_slice(&weight.to_le_bytes());
            let mut w=BufWriter::with_capacity(8<<20,File::create(&tmp).unwrap());
            w.write_all(&h).unwrap();
            for(k,v)in rows {
                let mut r=[0u8;RECORD];
                r[..29].copy_from_slice(&k.profile);r[29..41].copy_from_slice(&k.sig);r[41]=k.p2;
                r[42..58].copy_from_slice(&v.weight.to_le_bytes());r[58..66].copy_from_slice(&v.uses.to_le_bytes());
                r[66..90].copy_from_slice(&v.witness.row);r[90..98].copy_from_slice(&v.witness.source.to_le_bytes());
                r[98]=v.witness.p1;r[99]=v.witness.tail1;r[100]=v.witness.p2;r[101]=v.witness.m1;
                r[102]=v.witness.m2;r[103]=v.witness.packet;w.write_all(&r).unwrap();
            }
            w.flush().unwrap();drop(w);rename(&tmp,&dst).unwrap();
            self.stats.parts+=1;self.stats.emitted_records+=count;self.stats.emitted_weight+=weight;
        }
    }

    fn run_range(e:&E,d:&[u8],start:usize,end:usize,key_cap:usize,prefix:String)->Stats {
        let mut sink=Sink::new(prefix,key_cap);
        let mut cache:HashMap<[u8;12],Vec<usize>>=HashMap::new();
        for i in start..end {
            sink.stats.sources+=1;
            let(row,v)=rec(d,i);assert_ne!(v,0);
            let s=sig(&row,e);let ps=avail(s,e);if ps.is_empty(){continue}
            sink.stats.pivotable_sources+=1;
            let m1=ps.len();assert_eq!(-(v as i128)*U%(m1 as i128),0);
            let w18=-(v as i128)*U/(m1 as i128);
            for p1 in ps { for(tail1,t)in e.tails[p1][0].iter().enumerate() {
                sink.stats.generated+=1;
                let child=replace(&row,&e.anchors[p1],t);
                let s2=child_sig(s,p1,t,e);
                debug_assert_eq!(sig(&child,e),s2);
                let ps2=cache.entry(s2).or_insert_with(||avail(s2,e));
                if ps2.is_empty(){continue}
                sink.stats.pivotable+=1;
                let m2=ps2.len();assert_eq!(w18%(m2 as i128),0);assert_eq!(U%((m1*m2)as i128),0);
                let w20=-w18/(m2 as i128);
                *sink.stats.denom.entry((m1,m2)).or_default()+=1;
                for &p2 in ps2.iter() {
                    let key=PKey{profile:profile(&child,p2,e),sig:s2,p2:p2 as u8};
                    let witness=Witness{row:child.0,source:i as u64,p1:p1 as u8,tail1:tail1 as u8,
                        p2:p2 as u8,m1:m1 as u8,m2:m2 as u8,packet:255};
                    sink.add(key,w20,witness);
                }
            }}
        }
        sink.stats.cache_states=cache.len()as u64;
        sink.flush();assert_eq!(sink.stats.emitted_weight,sink.stats.contribution_weight);
        sink.stats
    }

    fn add_mem(map:&mut HashMap<PKey,Value>,key:PKey,weight:i128,witness:Witness) {
        let mut delete=false;
        match map.get_mut(&key){
            Some(v)=>{v.weight+=weight;v.uses+=1;if witness<v.witness{v.witness=witness}delete=v.weight==0},
            None=>{map.insert(key,Value{weight,uses:1,witness});}
        }
        if delete{map.remove(&key);}
    }

    fn control_map(e:&E,d:&[u8],start:usize,end:usize,cached:bool)->HashMap<PKey,Value>{
        let mut out=HashMap::new();let mut cache:HashMap<[u8;12],Vec<usize>>=HashMap::new();
        for i in start..end {let(row,v)=rec(d,i);let s=sig(&row,e);let ps=avail(s,e);if ps.is_empty(){continue}
            let m1=ps.len();let w18=-(v as i128)*U/(m1 as i128);
            for p1 in ps{for(tail1,t)in e.tails[p1][0].iter().enumerate(){let child=replace(&row,&e.anchors[p1],t);
                let s2=if cached{child_sig(s,p1,t,e)}else{sig(&child,e)};
                if cached{assert_eq!(s2,sig(&child,e));}
                let ps2=if cached{cache.entry(s2).or_insert_with(||avail(s2,e)).clone()}else{avail(s2,e)};
                if ps2.is_empty(){continue}let m2=ps2.len();assert_eq!(U%((m1*m2)as i128),0);let w20=-w18/(m2 as i128);
                for p2 in ps2{let key=PKey{profile:profile(&child,p2,e),sig:s2,p2:p2 as u8};
                    let witness=Witness{row:child.0,source:i as u64,p1:p1 as u8,tail1:tail1 as u8,p2:p2 as u8,
                        m1:m1 as u8,m2:m2 as u8,packet:255};add_mem(&mut out,key,w20,witness);}
            }}
        }out
    }

    fn control(){let e=parse();let d=read(format!("{}checkpoint_direct_k16.bin",DIR)).unwrap();
        assert_eq!(&d[..8],b"K16DIR1\0");assert_eq!(nrec(&d),INPUT_N);
        let ranges=[(0,2000),(6_000_000,6_002_000),(12_000_000,12_002_000),(20_000_000,20_002_000)];
        let mut rows=Vec::new();for&(lo,hi)in&ranges{let a=control_map(&e,&d,lo,hi,false);let b=control_map(&e,&d,lo,hi,true);assert!(a==b);rows.push((lo,hi,a.len()));}
        println!("PASS_PRODUCTION_BASELINE_CACHED_WITNESS_CONTROL {:?}",rows);
    }

    fn i128x(x:&[u8])->i128{i128::from_le_bytes(x.try_into().unwrap())}
    fn verify(start:usize,end:usize,parts:u64,prefix:&str){
        let e=parse();let d=read(format!("{}checkpoint_direct_k16.bin",DIR)).unwrap();assert_eq!(nrec(&d),INPUT_N);
        let(mut total_n,mut total_uses,mut total_weight)=(0u64,0u64,0i128);
        for part in 0..parts {let path=format!("{}.part{:06}.bin",prefix,part);let mut r=BufReader::with_capacity(8<<20,File::open(&path).unwrap());
            let mut h=[0u8;HEADER];r.read_exact(&mut h).unwrap();assert_eq!(&h[..8],b"K18PRF2\0");assert_eq!(u32le(&h[8..12]),2);
            assert_eq!((h[12],h[13],u16::from_le_bytes(h[14..16].try_into().unwrap())as usize),(3,2,RECORD));
            assert_eq!(u64le(&h[16..24]),U as u64);assert_eq!(u64le(&h[24..32]),part);
            let n=u64le(&h[32..40]);assert_eq!(metadata(&path).unwrap().len(),HEADER as u64+RECORD as u64*n);
            let(mut prior,mut uses,mut weight)=(None,0u64,0i128);
            for _ in 0..n{let mut x=[0u8;RECORD];r.read_exact(&mut x).unwrap();let mut key=[0u8;42];key.copy_from_slice(&x[..42]);if let Some(p)=prior{assert!(p<key)}prior=Some(key);
                let w=i128x(&x[42..58]);let u=u64le(&x[58..66]);assert_ne!(w,0);assert!(u>0);weight+=w;uses+=u;
                let mut rr=[0u8;24];rr.copy_from_slice(&x[66..90]);let row=Row(rr);let source=u64le(&x[90..98])as usize;
                let(p1,t1,p2,m1,m2,packet)=(x[98]as usize,x[99]as usize,x[100]as usize,x[101]as usize,x[102]as usize,x[103]);
                assert!(source>=start&&source<end&&p1<78&&t1<12&&p2<78&&m1>0&&m2>0);assert_eq!(packet,255);assert_eq!(p2,key[41]as usize);
                let s=sig(&row,&e);assert_eq!(&s[..],&key[29..41]);assert_eq!(&profile(&row,p2,&e)[..],&key[..29]);
                let ps2=avail(s,&e);assert_eq!(ps2.len(),m2);assert!(ps2.contains(&p2));assert_eq!(U%((m1*m2)as i128),0);
                let head=replace(&row,&e.tails[p1][0][t1],&e.anchors[p1]);assert!(rec(&d,source).0==head);
                let ps1=avail(sig(&head,&e),&e);assert_eq!(ps1.len(),m1);assert!(ps1.contains(&p1));
            }
            let mut z=[0u8;1];assert_eq!(r.read(&mut z).unwrap(),0);assert_eq!((uses,weight),(u64le(&h[40..48]),i128x(&h[48..64])));
            total_n+=n;total_uses+=uses;total_weight+=weight;
        }
        println!("PASS_PREFIX_LITERAL_VERIFY start={} end={} parts={} records={} uses={} weight={}",start,end,parts,total_n,total_uses,total_weight);
    }

    fn jhist(x:&BTreeMap<(usize,usize),u64>)->String{x.iter().map(|(&(a,b),&n)|format!("\"{}_{}\":{}",a,b,n)).collect::<Vec<_>>().join(",")}
    fn execute(start:usize,end:usize,key_cap:usize,prefix:String){
        assert!(start<end&&end<=INPUT_N);assert!(!Path::new(&format!("{}.kernel.json",prefix)).exists());
        let begun=Instant::now();let e=parse();let d=read(format!("{}checkpoint_direct_k16.bin",DIR)).unwrap();assert_eq!(nrec(&d),INPUT_N);
        let s=run_range(&e,&d,start,end,key_cap,prefix.clone());let elapsed=begun.elapsed().as_secs_f64();
        let text=format!(concat!("{{\n \"status\":\"PASS_COMPLETE_K16_CACHED_SHARD\",\n \"source_range\":[{},{}],\n \"scale_U\":\"{}\",\n",
            " \"source_rows\":{},\n \"pivotable_source_rows\":{},\n \"generated_k18_parents\":{},\n \"pivotable_k18_parents\":{},\n",
            " \"outgoing_pivot_uses\":{},\n \"signed_weight_scaled\":\"{}\",\n \"parts\":{},\n \"emitted_records_local_unique\":{},\n",
            " \"cache_states\":{},\n \"denominator_histogram\":{{{}}},\n \"key_cap\":{},\n \"elapsed_seconds\":{:.6}\n}}\n"),
            start,end,U,s.sources,s.pivotable_sources,s.generated,s.pivotable,s.outgoing_uses,s.contribution_weight,s.parts,s.emitted_records,
            s.cache_states,jhist(&s.denom),key_cap,elapsed);
        let dst=format!("{}.kernel.json",prefix);let tmp=format!("{}.tmp",dst);std::fs::write(&tmp,text).unwrap();rename(tmp,dst).unwrap();print!("{}",std::fs::read_to_string(format!("{}.kernel.json",prefix)).unwrap());
    }

    pub fn run(){let a:Vec<String>=env::args().collect();match a.get(1).map(String::as_str){
        Some("control")=>{assert_eq!(a.len(),2);control()},
        Some("run")=>{assert_eq!(a.len(),7,"run START END KEY_CAP PREFIX RESERVED");execute(a[2].parse().unwrap(),a[3].parse().unwrap(),a[4].parse().unwrap(),a[5].clone())},
        Some("verify")=>{assert_eq!(a.len(),6);verify(a[2].parse().unwrap(),a[3].parse().unwrap(),a[4].parse().unwrap(),&a[5])},
        _=>panic!("control | run START END KEY_CAP PREFIX RESERVED | verify START END PARTS PREFIX")}}
}
fn main(){production::run()}
