pub fn run(input: String) {
    let depths: Vec<u32> = input
        .lines()
        .map(|n| n.parse::<u32>().expect("Not a number"))
        .collect();
    let mut prev_sum: u32 = depths[..3].iter().sum();
    let mut increases: u32 = 0;

    for d in depths.windows(3) {
        let sum = d.iter().sum();
        if sum > prev_sum {
            increases += 1;
        }
        prev_sum = sum;
    }
    println!("{}", increases);
}
