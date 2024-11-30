use std::env;
use std::fs;
use std::str::FromStr;

#[derive(Debug)]
struct Report {
    conditions: String,
    counts: Vec<u8>,
}

fn parse_report(data: &str) -> Report {
    let mut spl = data.split(" ");
    Report {
        conditions: spl.next().unwrap().to_string(),
        counts: spl
            .next()
            .unwrap()
            .split(",")
            .filter_map(|word| u8::from_str(word).ok())
            .collect(),
    }
}

/*
* ..
* .#
* #.
* ##
*
* ...
* ..#
* .#.
* .##
* #..
* #.#
* ##.
* ###
*
*/


fn combinations(chars: &[char], length: usize) -> Vec<String> {
    let mut combinations: Vec<String> = chars.iter().map(|c| c.to_string()).collect();
    for _ in 1..length {
        let mut new_combinations = Vec::new();

        for comb in combinations.iter() {
            println!("Now checking {comb:?}");
            for &ch in chars.iter().filter(|&&c| !comb.contains(c)) {
                let mut new_combo = comb.clone();
                new_combo.push(ch);
                new_combinations.push(new_combo);
            }
        }
        combinations = new_combinations;
    }
    combinations
}

fn report_configs(report: &Report) -> u32 {
    unimplemented!()
}

fn part_1(data: String) -> u32 {
    let reports: Vec<Report> = data.lines().map(parse_report).collect();
    println!("Reports: {reports:?}");

    for report in reports.iter() {
        let unknown_count: usize = report.conditions.chars().filter(|c| c == &'?').count();
        let combos = combinations(&vec!['.', '#'], unknown_count);
        println!("Combos: {combos:?}");
    }

    return 0;
}

fn main() {
    let val = env::args().last().unwrap();
    println!("File name: {val}");
    let data = fs::read_to_string(val).unwrap();
    println!("Data: {data}");

    part_1(data);
}
