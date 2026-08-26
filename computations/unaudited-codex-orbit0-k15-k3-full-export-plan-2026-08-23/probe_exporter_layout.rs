use std::mem::{align_of,size_of};
#[derive(Clone,Copy)]struct PKey{profile:[u8;29],sig:[u8;12],p2:u8}
#[derive(Clone,Copy)]struct Witness{row:[u8;24],source_index:u64,p1:u8,tail1:u8,p2:u8,m1:u8,m2:u8,packet:u8}
#[derive(Clone,Copy)]struct Value{weight:i128,uses:u64,witness:Witness}
fn main(){println!("PKey size={} align={} Witness size={} align={} Value size={} align={} tuple_size={} tuple_align={}",size_of::<PKey>(),align_of::<PKey>(),size_of::<Witness>(),align_of::<Witness>(),size_of::<Value>(),align_of::<Value>(),size_of::<(PKey,Value)>(),align_of::<(PKey,Value)>());}
