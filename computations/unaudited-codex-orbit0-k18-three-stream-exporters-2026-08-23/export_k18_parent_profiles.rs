mod exporter {
    #![allow(dead_code)]
    include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");

    use std::collections::BTreeMap;
    use std::env;
    use std::fs::{File, rename};
    use std::io::{BufWriter, Write};
    use std::path::Path;

    const U: i128 = 400_591_699_200;
    const HEADER_BYTES: usize = 96;
    const RECORD_BYTES: usize = 104;

    #[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
    struct PKey { profile: [u8;29], sig: [u8;12], p2: u8 }

    #[derive(Clone, Copy, Eq, Ord, PartialEq, PartialOrd)]
    struct Witness {
        row: [u8;24], source_index: u64, p1: u8, tail1: u8,
        p2: u8, m1: u8, m2: u8, packet: u8,
    }

    #[derive(Clone, Copy)]
    struct Value { weight: i128, uses: u64, witness: Witness }

    #[derive(Default)]
    struct Stats {
        generated: u64, pivotable: u64, outgoing_uses: u64,
        contribution_weight: i128, emitted_records: u64, emitted_weight: i128,
        parts: u64, denom: BTreeMap<(usize,usize),u64>, stopped_at_cap: bool,
    }

    struct Sink {
        component: u8, prefix: String, key_cap: usize,
        map: HashMap<PKey,Value>, stats: Stats,
    }

    impl Sink {
        fn new(component:u8,prefix:String,key_cap:usize)->Self {
            assert!(key_cap>0); Self{component,prefix,key_cap,map:HashMap::new(),stats:Stats::default()}
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
            assert!(!Path::new(&dst).exists(),"refusing to overwrite {}",dst);
            let count=rows.len() as u64;
            let uses:u64=rows.iter().map(|x|x.1.uses).sum();
            let weight:i128=rows.iter().map(|x|x.1.weight).sum();
            let mut h=[0u8;HEADER_BYTES];
            h[..8].copy_from_slice(b"K18PRF2\0");
            h[8..12].copy_from_slice(&2u32.to_le_bytes());
            h[12]=self.component; h[13]=2;
            h[14..16].copy_from_slice(&(RECORD_BYTES as u16).to_le_bytes());
            h[16..24].copy_from_slice(&(U as u64).to_le_bytes());
            h[24..32].copy_from_slice(&part.to_le_bytes());
            h[32..40].copy_from_slice(&count.to_le_bytes());
            h[40..48].copy_from_slice(&uses.to_le_bytes());
            h[48..64].copy_from_slice(&weight.to_le_bytes());
            let f=File::create(&tmp).unwrap(); let mut w=BufWriter::new(f); w.write_all(&h).unwrap();
            for (k,v) in rows {
                let mut r=[0u8;RECORD_BYTES];
                r[..29].copy_from_slice(&k.profile); r[29..41].copy_from_slice(&k.sig); r[41]=k.p2;
                r[42..58].copy_from_slice(&v.weight.to_le_bytes());
                r[58..66].copy_from_slice(&v.uses.to_le_bytes());
                r[66..90].copy_from_slice(&v.witness.row);
                r[90..98].copy_from_slice(&v.witness.source_index.to_le_bytes());
                r[98]=v.witness.p1; r[99]=v.witness.tail1; r[100]=v.witness.p2;
                r[101]=v.witness.m1; r[102]=v.witness.m2; r[103]=v.witness.packet;
                w.write_all(&r).unwrap();
            }
            w.flush().unwrap(); drop(w); rename(&tmp,&dst).unwrap();
            self.stats.parts+=1; self.stats.emitted_records+=count; self.stats.emitted_weight+=weight;
        }
    }

    fn observe(row:Row,w18:i128,m1:usize,e:&E,sink:&mut Sink,source_index:u64,p1:usize,tail1:usize,packet:u8,cap:u64)->bool {
        sink.stats.generated+=1;
        let s=sig(&row,e); let ps=avail(s,e); if ps.is_empty(){return false}
        sink.stats.pivotable+=1; let m2=ps.len();
        assert_eq!(w18%(m2 as i128),0); assert_eq!(U%((m1*m2)as i128),0);
        let w20=-w18/(m2 as i128); *sink.stats.denom.entry((m1,m2)).or_default()+=1;
        for p2 in ps {
            let key=PKey{profile:profile(&row,p2,e),sig:s,p2:p2 as u8};
            let wit=Witness{row:row.0,source_index,p1:p1 as u8,tail1:tail1 as u8,p2:p2 as u8,m1:m1 as u8,m2:m2 as u8,packet};
            sink.add(key,w20,wit);
        }
        cap>0 && sink.stats.pivotable>=cap
    }

    fn k14(e:&E,start:usize,end:usize,cap:u64,sink:&mut Sink) {
        'outer:for ri in start..end.min(e.records.len()) { let r=&e.records[ri]; let positive=(r.coefficient as i128)*(r.size as i128);
            for a in &e.factor[0][0]{for b in &e.factor[1][0]{for c in &e.factor[2][0]{let head=make(r,a,b,c);let s=sig(&head,e);let ps=valid(s,e);let m1=ps.len();assert_eq!(positive*U%(m1 as i128),0);let w=positive*U/(m1 as i128);for p1 in ps{for (t1,t) in e.tails[p1][2].iter().enumerate(){let row=replace(&head,&e.anchors[p1],t);if observe(row,w,m1,e,sink,ri as u64,p1,t1,0,cap){sink.stats.stopped_at_cap=true;break 'outer}}}}}}
        }
    }

    fn k15(e:&E,start:usize,end:usize,cap:u64,sink:&mut Sink) {
        'outer:for ri in start..end.min(e.records.len()) { let r=&e.records[ri]; let positive=(r.coefficient as i128)*(r.size as i128);
            for hi in 0..3 { let o:Vec<_>=(0..3).filter(|&x|x!=hi).collect();for a in &e.factor[o[0]][0]{for b in &e.factor[o[1]][0]{for c in &e.factor[hi][1]{let head=match hi{0=>make(r,c,a,b),1=>make(r,a,c,b),_=>make(r,a,b,c)};let s=sig(&head,e);let ps=avail(s,e);let m1=ps.len();assert!(m1>0);assert_eq!(positive*U%(m1 as i128),0);let w=positive*U/(m1 as i128);for p1 in ps{for (t1,t) in e.tails[p1][1].iter().enumerate(){let row=replace(&head,&e.anchors[p1],t);if observe(row,w,m1,e,sink,ri as u64,p1,t1,hi as u8,cap){sink.stats.stopped_at_cap=true;break 'outer}}}}}}}
        }
    }

    fn k16(e:&E,start:usize,end:usize,cap:u64,sink:&mut Sink) {
        let d=read(format!("{}checkpoint_direct_k16.bin",DIR)).unwrap();assert_eq!(&d[..8],b"K16DIR1\0");
        'outer:for i in start..end.min(nrec(&d)){let(row,v)=rec(&d,i);let s=sig(&row,e);let ps=avail(s,e);if ps.is_empty(){continue}let m1=ps.len();assert_ne!(v,0);assert_eq!(-(v as i128)*U%(m1 as i128),0);let w=-(v as i128)*U/(m1 as i128);for p1 in ps{for(t1,t)in e.tails[p1][0].iter().enumerate(){let child=replace(&row,&e.anchors[p1],t);if observe(child,w,m1,e,sink,i as u64,p1,t1,255,cap){sink.stats.stopped_at_cap=true;break 'outer}}}}
    }

    fn jhist(x:&BTreeMap<(usize,usize),u64>)->String{x.iter().map(|(&(a,b),&n)|format!("\"{}_{}\":{}",a,b,n)).collect::<Vec<_>>().join(",")}

    fn i128le(x:&[u8])->i128{i128::from_le_bytes(x.try_into().unwrap())}
    fn source_heads(mode:&str,packet:u8,source:usize,e:&E)->HashSet<Row>{
        assert!(source<e.records.len());let r=&e.records[source];let mut out=HashSet::new();
        if mode=="k14"{for a in &e.factor[0][0]{for b in &e.factor[1][0]{for c in &e.factor[2][0]{out.insert(make(r,a,b,c));}}}return out}
        let hi=packet as usize;assert!(hi<3);let o:Vec<_>=(0..3).filter(|&x|x!=hi).collect();for a in &e.factor[o[0]][0]{for b in &e.factor[o[1]][0]{for c in &e.factor[hi][1]{let row=match hi{0=>make(r,c,a,b),1=>make(r,a,c,b),_=>make(r,a,b,c)};out.insert(row);}}}out
    }
    fn verify_part(mode:&str,path:&str){
        let component=match mode{"k14"=>1,"k15"=>2,"k16"=>3,_=>panic!("unknown mode")};let degree=match mode{"k14"=>4,"k15"=>3,"k16"=>2,_=>0};
        let e=parse();let b=read(path).unwrap();assert!(b.len()>=HEADER_BYTES);assert_eq!(&b[..8],b"K18PRF2\0");assert_eq!(u32le(&b[8..12]),2);assert_eq!(b[12],component);assert_eq!(b[13],2);assert_eq!(u32::from(u16::from_le_bytes(b[14..16].try_into().unwrap())),RECORD_BYTES as u32);assert_eq!(u64le(&b[16..24]),U as u64);let n=u64le(&b[32..40])as usize;assert_eq!(b.len(),HEADER_BYTES+n*RECORD_BYTES);
        let d=if mode=="k16"{Some(read(format!("{}checkpoint_direct_k16.bin",DIR)).unwrap())}else{None};
        let(mut uses,mut weight)=(0u64,0i128);let mut prev:Option<PKey>=None;let mut head_cache:HashMap<(usize,u8),HashSet<Row>>=HashMap::new();
        for i in 0..n{let x=&b[HEADER_BYTES+i*RECORD_BYTES..HEADER_BYTES+(i+1)*RECORD_BYTES];let mut pr=[0;29];pr.copy_from_slice(&x[..29]);let mut sg=[0;12];sg.copy_from_slice(&x[29..41]);let key=PKey{profile:pr,sig:sg,p2:x[41]};if let Some(q)=prev{assert!(q<key)}prev=Some(key);let w=i128le(&x[42..58]);let u=u64le(&x[58..66]);assert_ne!(w,0);assert!(u>0);weight+=w;uses+=u;let mut rr=[0;24];rr.copy_from_slice(&x[66..90]);let row=Row(rr);let source=u64le(&x[90..98])as usize;let p1=x[98]as usize;let t1=x[99]as usize;let p2=x[100]as usize;let m1=x[101]as usize;let m2=x[102]as usize;let packet=x[103];assert_eq!(p2,key.p2 as usize);assert_eq!(sig(&row,&e),key.sig);assert_eq!(profile(&row,p2,&e),key.profile);let ps2=avail(key.sig,&e);assert_eq!(ps2.len(),m2);assert!(ps2.contains(&p2));assert_eq!(U%((m1*m2)as i128),0);assert!(t1<e.tails[p1][degree-2].len());let head=replace(&row,&e.tails[p1][degree-2][t1],&e.anchors[p1]);let ps1=if mode=="k14"{valid(sig(&head,&e),&e)}else{avail(sig(&head,&e),&e)};assert_eq!(ps1.len(),m1);assert!(ps1.contains(&p1));if let Some(ref dd)=d{assert!(rec(dd,source).0==head);assert_eq!(packet,255)}else{assert!(head_cache.entry((source,packet)).or_insert_with(||source_heads(mode,packet,source,&e)).contains(&head))} }
        assert_eq!(uses,u64le(&b[40..48]));assert_eq!(weight,i128le(&b[48..64]));println!("PASS {} records={} uses={} weight={}",mode,n,uses,weight)
    }
    fn finish(mode:&str,start:usize,end:usize,cap:u64,key_cap:usize,elapsed:f64,sink:&mut Sink) {
        sink.flush(); assert_eq!(sink.stats.emitted_weight,sink.stats.contribution_weight);
        let manifest=format!("{}.manifest.json",sink.prefix);assert!(!Path::new(&manifest).exists(),"refusing to overwrite {}",manifest);
        let tmp=format!("{}.tmp",manifest);
        let paths=match mode{"k14"=>"D14:222|R:4-2","k15"=>"D15:{223,232,322}|R:3-2","k16"=>"D16:{224,233,242,323,332,422}|R:2-2",_=>unreachable!()};
        let text=format!(concat!("{{\n  \"status\":\"PASS_EXACT_PREFIX_OR_COMPLETE_SHARD\",\n  \"mode\":\"{}\",\n  \"dag_paths\":\"{}\",\n",
          "  \"source_range\":[{},{}],\n  \"parent_cap\":{},\n  \"complete_source_range\":{},\n  \"scale_U\":\"{}\",\n",
          "  \"key_schema\":\"profile29|signature12|outgoing_pivot_u8\",\n  \"record_schema\":\"key42|weight_i128|uses_u64|witness_row24|source_index_u64|p1|tail1|p2|m1|m2|packet = 104 bytes\",\n",
          "  \"parts\":{},\n  \"emitted_records_local_unique\":{},\n  \"generated_parents\":{},\n  \"pivotable_parents\":{},\n  \"outgoing_pivot_uses\":{},\n",
          "  \"signed_weight_sum_scaled\":\"{}\",\n  \"m1_m2_hist\":{{{}}},\n  \"key_flush_cap\":{},\n  \"elapsed_seconds\":{:.6}\n}}\n"),
          mode,paths,start,end,cap,!sink.stats.stopped_at_cap,U,sink.stats.parts,sink.stats.emitted_records,sink.stats.generated,sink.stats.pivotable,sink.stats.outgoing_uses,sink.stats.contribution_weight,jhist(&sink.stats.denom),key_cap,elapsed);
        std::fs::write(&tmp,&text).unwrap();rename(&tmp,&manifest).unwrap();print!("{}",text);
    }

    pub fn run(){let args:Vec<String>=env::args().collect();if args.len()==4&&args[1]=="verify"{verify_part(&args[2],&args[3]);return}assert_eq!(args.len(),7,"MODE START END PARENT_CAP KEY_CAP OUT_PREFIX");let mode=&args[1];let start=args[2].parse().unwrap();let end=args[3].parse().unwrap();let cap=args[4].parse().unwrap();let key_cap=args[5].parse().unwrap();let prefix=args[6].clone();assert!(start<end);assert!(!Path::new(&format!("{}.manifest.json",prefix)).exists());let begun=Instant::now();let e=parse();if mode=="k14"||mode=="k15"{assert!(end<=e.records.len())}else if mode=="k16"{let d=read(format!("{}checkpoint_direct_k16.bin",DIR)).unwrap();assert!(end<=nrec(&d))}let component=match mode.as_str(){"k14"=>1,"k15"=>2,"k16"=>3,_=>panic!("unknown mode")};let mut sink=Sink::new(component,prefix,key_cap);match mode.as_str(){"k14"=>k14(&e,start,end,cap,&mut sink),"k15"=>k15(&e,start,end,cap,&mut sink),"k16"=>k16(&e,start,end,cap,&mut sink),_=>unreachable!()};let elapsed=begun.elapsed().as_secs_f64();finish(mode,start,end,cap,key_cap,elapsed,&mut sink)}
}

fn main(){exporter::run()}
