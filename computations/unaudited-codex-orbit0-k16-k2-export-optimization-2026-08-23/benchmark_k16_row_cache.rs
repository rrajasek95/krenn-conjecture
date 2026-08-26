mod bench {
    #![allow(dead_code)]
    include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");


    const U2:i128=400_591_699_200;

    #[derive(Clone,Copy,Eq,Hash,Ord,PartialEq,PartialOrd)]
    struct PKey{profile:[u8;29],sig:[u8;12],p2:u8}
    #[derive(Clone,Copy,Default,Eq,PartialEq)] struct PVal{weight:i128,uses:u64}
    #[derive(Clone,Copy,Default)] struct ChildVal{weight:i128,uses:u64}
    #[derive(Clone,Copy,Default)] struct Census{
        sources:u64,pivotable_sources:u64,generated:u64,child_keys:u64,child_zeros:u64,
        pivotable_occ:u64,pivotable_child_keys:u64,outgoing_uses:u64,profile_keys:u64,
        profile_zeros:u64,profile_weight:i128,profile_uses:u64,
    }
    struct Output{c:Census,elapsed:f64}

    fn padd(m:&mut HashMap<PKey,PVal>,k:PKey,w:i128,uses:u64){let v=m.entry(k).or_default();v.weight+=w;v.uses+=uses}
    fn cadd(m:&mut HashMap<Row,ChildVal>,k:Row,w:i128){let v=m.entry(k).or_default();v.weight+=w;v.uses+=1}

    fn staged(e:&E,d:&[u8],start:usize,end:usize)->Output{
        let begun=Instant::now();let mut cm:HashMap<Row,ChildVal>=HashMap::new();let mut c=Census::default();
        for i in start..end{c.sources+=1;let(row,v)=rec(d,i);let s=sig(&row,e);let ps=avail(s,e);if ps.is_empty(){continue}c.pivotable_sources+=1;let m1=ps.len()as i128;assert_eq!(-(v as i128)*U2%m1,0);let w18=-(v as i128)*U2/m1;
            for p1 in ps{for t in &e.tails[p1][0]{let child=replace(&row,&e.anchors[p1],t);c.generated+=1;cadd(&mut cm,child,w18)}}
        }
        c.child_keys=cm.len()as u64;let mut pm:HashMap<PKey,PVal>=HashMap::new();
        for(row,x)in cm{if x.weight==0{c.child_zeros+=1}let s=sig(&row,e);let ps=avail(s,e);if ps.is_empty(){continue}c.pivotable_child_keys+=1;c.pivotable_occ+=x.uses;let m2=ps.len()as i128;assert_eq!(x.weight%m2,0);let w20=-x.weight/m2;c.outgoing_uses+=x.uses*(ps.len()as u64);
            for p2 in ps{padd(&mut pm,PKey{profile:profile(&row,p2,e),sig:s,p2:p2 as u8},w20,x.uses)}
        }
        for x in pm.values(){if x.weight==0{c.profile_zeros+=1}else{c.profile_keys+=1;c.profile_weight+=x.weight;c.profile_uses+=x.uses}}
        Output{c,elapsed:begun.elapsed().as_secs_f64()}
    }

    fn baseline(e:&E,d:&[u8],start:usize,end:usize)->Output{
        let begun=Instant::now();let mut pm:HashMap<PKey,PVal>=HashMap::new();let mut c=Census::default();
        for i in start..end{c.sources+=1;let(row,v)=rec(d,i);let s=sig(&row,e);let ps=avail(s,e);if ps.is_empty(){continue}c.pivotable_sources+=1;let m1=ps.len()as i128;assert_eq!(-(v as i128)*U2%m1,0);let w18=-(v as i128)*U2/m1;
            for p1 in ps{for t in &e.tails[p1][0]{let child=replace(&row,&e.anchors[p1],t);c.generated+=1;let s2=child_sig(s,p1,t,e);assert_eq!(sig(&child,e),s2);let ps2=avail(s2,e);if ps2.is_empty(){continue}c.pivotable_occ+=1;let m2=ps2.len()as i128;assert_eq!(w18%m2,0);let w20=-w18/m2;c.outgoing_uses+=ps2.len()as u64;
                for p2 in ps2{padd(&mut pm,PKey{profile:profile(&child,p2,e),sig:s2,p2:p2 as u8},w20,1)}
            }}
        }
        for x in pm.values(){if x.weight==0{c.profile_zeros+=1}else{c.profile_keys+=1;c.profile_weight+=x.weight;c.profile_uses+=x.uses}}
        Output{c,elapsed:begun.elapsed().as_secs_f64()}
    }

    fn cached_direct(e:&E,d:&[u8],start:usize,end:usize)->(Output,usize){
        let begun=Instant::now();let mut pm:HashMap<PKey,PVal>=HashMap::new();let mut cache:HashMap<[u8;12],Vec<usize>>=HashMap::new();let mut c=Census::default();
        for i in start..end{c.sources+=1;let(row,v)=rec(d,i);let s=sig(&row,e);let ps=avail(s,e);if ps.is_empty(){continue}c.pivotable_sources+=1;let m1=ps.len()as i128;assert_eq!(-(v as i128)*U2%m1,0);let w18=-(v as i128)*U2/m1;
            for p1 in ps{for t in &e.tails[p1][0]{let child=replace(&row,&e.anchors[p1],t);c.generated+=1;let s2=child_sig(s,p1,t,e);let ps2=cache.entry(s2).or_insert_with(||avail(s2,e));if ps2.is_empty(){continue}c.pivotable_occ+=1;let m2=ps2.len()as i128;assert_eq!(w18%m2,0);let w20=-w18/m2;c.outgoing_uses+=ps2.len()as u64;
                for &p2 in ps2.iter(){padd(&mut pm,PKey{profile:profile(&child,p2,e),sig:s2,p2:p2 as u8},w20,1)}
            }}
        }
        for x in pm.values(){if x.weight==0{c.profile_zeros+=1}else{c.profile_keys+=1;c.profile_weight+=x.weight;c.profile_uses+=x.uses}}
        (Output{c,elapsed:begun.elapsed().as_secs_f64()},cache.len())
    }

    fn same(a:&Census,b:&Census){assert_eq!((a.sources,a.pivotable_sources,a.generated,a.pivotable_occ,a.outgoing_uses,a.profile_keys,a.profile_zeros,a.profile_weight,a.profile_uses),(b.sources,b.pivotable_sources,b.generated,b.pivotable_occ,b.outgoing_uses,b.profile_keys,b.profile_zeros,b.profile_weight,b.profile_uses))}
    fn jc(c:Census)->String{format!("{{\"sources\":{},\"pivotable_sources\":{},\"generated\":{},\"child_keys\":{},\"child_exact_zeros\":{},\"pivotable_occurrences\":{},\"pivotable_child_keys\":{},\"outgoing_uses\":{},\"profile_keys\":{},\"profile_exact_zeros\":{},\"profile_weight_scaled\":\"{}\",\"profile_uses\":{}}}",c.sources,c.pivotable_sources,c.generated,c.child_keys,c.child_zeros,c.pivotable_occ,c.pivotable_child_keys,c.outgoing_uses,c.profile_keys,c.profile_zeros,c.profile_weight,c.profile_uses)}

    pub fn run(){let begun=Instant::now();let e=Arc::new(parse());let d=Arc::new(read(format!("{}checkpoint_direct_k16.bin",DIR)).unwrap());assert_eq!(nrec(&d),24_097_095);
        let checks=[(0,2000),(6_000_000,6_002_000),(12_000_000,12_002_000),(20_000_000,20_002_000)];let mut exact=Vec::new();for&(lo,hi)in&checks{let b=baseline(&e,&d,lo,hi);let(c,nc)=cached_direct(&e,&d,lo,hi);let s=staged(&e,&d,lo,hi);same(&b.c,&c.c);same(&b.c,&s.c);exact.push(format!("{{\"range\":[{},{}],\"baseline_seconds\":{:.6},\"cached_direct_seconds\":{:.6},\"staged_seconds\":{:.6},\"cached_signature_states\":{},\"census\":{}}}",lo,hi,b.elapsed,c.elapsed,s.elapsed,nc,jc(s.c)))}
        let starts=[0usize,3_000_000,6_000_000,9_000_000,12_000_000,15_000_000,18_000_000,23_000_000];let mut jobs=Vec::new();for lo in starts{let x=e.clone();let z=d.clone();jobs.push(thread::spawn(move||{let cached=cached_direct(&x,&z,lo,lo+20_000);let staged=staged(&x,&z,lo,lo+20_000);(lo,cached,staged)}))}let mut large=Vec::new();for j in jobs{let(lo,c,s)=j.join().unwrap();same(&c.0.c,&s.c);large.push((lo,c,s))}large.sort_by_key(|x|x.0);let large_json=large.iter().map(|(lo,c,s)|format!("{{\"range\":[{},{}],\"cached_direct_seconds\":{:.6},\"staged_seconds\":{:.6},\"cached_signature_states\":{},\"census\":{}}}",lo,lo+20_000,c.0.elapsed,s.elapsed,c.1,jc(s.c))).collect::<Vec<_>>().join(",");
        let text=format!("{{\n \"status\":\"PASS_BOUNDED_EXACT_ROW_CACHE_BENCHMARK\",\n \"scale_U\":{},\n \"exact_baseline_equal_ranges\":[{}],\n \"parallel_staged_ranges\":[{}],\n \"elapsed_seconds\":{:.6}\n}}\n",U2,exact.join(","),large_json,begun.elapsed().as_secs_f64());std::fs::create_dir_all("computations/unaudited-codex-orbit0-k16-k2-export-optimization-2026-08-23").unwrap();std::fs::write("computations/unaudited-codex-orbit0-k16-k2-export-optimization-2026-08-23/results_k16_row_cache_benchmark.json",&text).unwrap();print!("{}",text)}
}
fn main(){bench::run()}
