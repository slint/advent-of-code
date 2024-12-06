use std::env;
use std::fs;

fn main() {
    let val = env::args().last().unwrap();
    println!("File name: {val}");
    let data = fs::read_to_string(val).unwrap();

    part_one(&data);
    part_two(&data);
}

fn part_two(data: &str) {
    let mut safe_report_count = 0;
    for line in data.lines().filter(|x| !x.is_empty()) {
        let report: Vec<i32> = line
            .split_whitespace()
            .map(|x| x.parse::<i32>().unwrap())
            .collect();

        if is_safe_report(&report) {
            safe_report_count += 1;
        } else {
            // Retry with removing one element from the report
            for i in 0..report.len() {
                let mut new_report = report.clone();
                new_report.remove(i);
                if is_safe_report(&new_report) {
                    safe_report_count += 1;
                    break;
                }
            }
        }
    }
    println!("Safe reports (w/ element removal): {safe_report_count}");
}

fn part_one(data: &str) {
    let mut safe_report_count = 0;
    for line in data.lines().filter(|x| !x.is_empty()) {
        let report: Vec<i32> = line
            .split_whitespace()
            .map(|x| x.parse::<i32>().unwrap())
            .collect();

        if is_safe_report(&report) {
            safe_report_count += 1;
        }
    }
    println!("Safe reports: {safe_report_count}");
}

fn is_safe_report(report: &[i32]) -> bool {
    // Check for increase or decrease within 1-3
    let bad_diff = report.windows(2).any(|x| {
        let diff = x[0].abs_diff(x[1]);
        !(1..=3).contains(&diff)
    });

    let is_sorted = report
        .windows(3)
        .all(|x| (x[0] <= x[1] && x[1] <= x[2]) || (x[0] >= x[1] && x[1] >= x[2]));

    is_sorted && !bad_diff
}
