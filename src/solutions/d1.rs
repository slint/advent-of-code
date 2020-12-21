pub fn run(input: String) {
    let numbers: Vec<u32> = input
        .lines()
        .map(|n| n.parse::<u32>().expect("Not a number"))
        .collect();
    for n1 in numbers.iter() {
        for n2 in numbers.iter() {
            for n3 in numbers.iter() {
                if n1 + n2 + n3 == 2020 {
                    println!("{}, {}, {}: {}", n1, n2, n3, n1 * n2 * n3);
                    return;
                }
            }
        }
    }
}
