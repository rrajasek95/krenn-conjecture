mod inherited {
    #![allow(dead_code, unused_imports)]
    include!("k24_hidden_base.rs");
    include!("k24_hidden_decorated_impl.rs");
}
fn main() { inherited::k24_main(); }

