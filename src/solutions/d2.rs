use std::str::FromStr;

struct RuleMatch {
    range_start: u8,
    range_end: u8,
    letter: char,
    password: String,
}

impl RuleMatch {
    fn is_valid(&self) -> bool {
        let start_char = self
            .password
            .chars()
            .nth((self.range_start - 1) as usize)
            .unwrap();
        let end_char = self
            .password
            .chars()
            .nth((self.range_end - 1) as usize)
            .unwrap();
        (start_char == self.letter) ^ (end_char == self.letter)
    }
}

impl FromStr for RuleMatch {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut parts = s.split(' ');
        let mut range = parts.next().unwrap().split('-');
        let range_start = range.next().unwrap().parse::<u8>().unwrap();
        let range_end = range.next().unwrap().parse::<u8>().unwrap();
        let letter: char = parts.next().unwrap().chars().next().unwrap();
        let password = parts.next().unwrap();
        Ok(RuleMatch {
            range_start: range_start,
            range_end: range_end,
            letter: letter,
            password: password.to_string(),
        })
    }
}

pub fn run(input: String) {
    let rules: Vec<RuleMatch> = input
        .lines()
        .map(|n| n.parse::<RuleMatch>().unwrap())
        .collect();

    let valid_count = rules.iter().filter(|r| r.is_valid()).count();
    println!("There are {} valid passwords.", valid_count);
}
