use std::env;
use std::fs;

fn main() {
    let val = env::args().last().unwrap();
    println!("File name: {val}");
    let data = fs::read_to_string(val).unwrap();
    println!("Data: {data}");
}
