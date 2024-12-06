use std::env;
use std::fs;

fn main() {
    let val = env::args().last().unwrap();
    println!("File name: {val}");
    let data = fs::read_to_string(val).unwrap();

    let mut left_list: Vec<u32> = Vec::new();
    let mut right_list: Vec<u32> = Vec::new();

    data.lines()
        .filter_map(|x| {
            if !x.trim().is_empty() {
                Some(x.split_whitespace())
            } else {
                None
            }
        })
        .for_each(|mut line| {
            let left: u32 = line.next().unwrap().parse().unwrap();
            let right: u32 = line.next().unwrap().parse().unwrap();
            left_list.push(left);
            right_list.push(right);
        });

    part_one(&left_list, &right_list);
    part_two(&left_list, &right_list);
}

fn part_one(left_list: &[u32], right_list: &[u32]) {
    let mut left_list = left_list.to_owned();
    let mut right_list = right_list.to_owned();
    left_list.sort();
    right_list.sort();

    let mut sum_of_diffs = 0;

    for (left, right) in left_list.iter().zip(right_list.iter()) {
        // absolute difference
        let diff = left.abs_diff(*right);
        sum_of_diffs += diff;
    }

    println!("Sum of differences: {}", sum_of_diffs);
}

fn part_two(left_list: &[u32], right_list: &[u32]) {
    let mut sum_of_similar = 0;
    for left in left_list.iter() {
        let total_similar = right_list.iter().filter(|x| *x == left).count() as u32;
        sum_of_similar += left * total_similar;
    }
    println!("Sum of similarities: {}", sum_of_similar);
}
