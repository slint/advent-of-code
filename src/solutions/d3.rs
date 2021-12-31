trait BitIndex {
    fn bit_at(&self, pos: usize) -> Self;
}

impl BitIndex for usize {
    fn bit_at(&self, pos: usize) -> Self {
        (self >> pos) & 1
    }
}

fn bit_counts(numbers: &Vec<usize>, pos: usize) -> usize {
    return numbers.iter().fold(0, |ret, n| ret + n.bit_at(pos));
}

pub fn run(input: String) {
    let num_length = input.lines().next().unwrap().len();
    let numbers: Vec<usize> = input
        .lines()
        .map(|l| usize::from_str_radix(l, 2).unwrap())
        .collect();

    let mut gamma: usize = 0;
    for idx in 0..num_length {
        let bit_criteria = (bit_counts(&numbers, idx) >= (numbers.len() / 2)) as usize;
        gamma += (bit_criteria) << idx;
    }
    let epsilon = !gamma & ((1 << num_length) - 1);
    let oxygen: usize = find_rating(&numbers, num_length, true);
    let co2: usize = find_rating(&numbers, num_length, false);

    dbg!(gamma, epsilon, gamma * epsilon);
    dbg!(oxygen, co2, oxygen * co2);
}

fn find_rating(numbers: &Vec<usize>, num_length: usize, most_common: bool) -> usize {
    let mut result: usize = 0;
    let mut current_numbers = numbers.clone();
    for idx in 0..num_length {
        let bin_pos = num_length - idx - 1;
        let length = current_numbers.len();
        let ones_count = bit_counts(&current_numbers, bin_pos);
        let zeroes_count = length - ones_count;
        let bit_criteria = if most_common {
            ones_count >= zeroes_count
        } else {
            zeroes_count > ones_count
        } as usize;
        current_numbers = current_numbers
            .into_iter()
            .filter(|n| n.bit_at(bin_pos) == bit_criteria)
            .collect();
        if current_numbers.len() == 1 {
            result = current_numbers[0];
            break;
        }
    }
    result
}
