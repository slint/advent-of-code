use itertools::Itertools;
use std::collections::HashMap;

const ROWS: usize = 5;
const COLUMNS: usize = 5;

#[derive(Hash, Eq, PartialEq, Debug)]
struct BingoCell {
    col: usize,
    row: usize,
    hit: bool,
}

fn board_has_match(board: &HashMap<usize, BingoCell>) -> bool {
    let mut found = false;
    dbg!(board.values().filter(|c| c.hit).collect());
    for (check_col, row) in &board.values().filter(|c| c.hit).group_by(|v| v.col) {
        let row_res = row.collect::<Vec<&BingoCell>>();
        dbg!(check_col, &row_res);
        if row_res.len() == COLUMNS {
            return true;
        }
    }
    for (check_row, col) in &board.values().filter(|c| c.hit).group_by(|v| v.row) {
        let col_res = col.collect::<Vec<&BingoCell>>();
        dbg!(check_row, &col_res);
        if col_res.len() == COLUMNS {
            return true;
        }
    }
    found
}

pub fn run(input: String) {
    let (numbers_str, boards_str) = input.split_once("\n\n").unwrap();

    // Parse bingo numbers
    let numbers: Vec<usize> = numbers_str.split(",").map(|x| x.parse().unwrap()).collect();

    let mut boards: Vec<HashMap<usize, BingoCell>> = Vec::new();

    // Parse bingo boards
    for board_str in boards_str.split("\n\n") {
        let mut board = HashMap::new();
        let board_nums = board_str.split_whitespace().map(|n| n.parse().unwrap());
        for (idx, num) in board_nums.enumerate() {
            board.insert(
                num,
                BingoCell {
                    col: (idx % COLUMNS),
                    row: (idx / ROWS),
                    hit: false,
                },
            );
        }
        boards.push(board);
    }

    // 12 75 58 21 87
    &boards[0].entry(12).and_modify(|c| c.hit = true);
    &boards[0].entry(75).and_modify(|c| c.hit = true);
    &boards[0].entry(58).and_modify(|c| c.hit = true);
    &boards[0].entry(21).and_modify(|c| c.hit = true);
    &boards[0].entry(87).and_modify(|c| c.hit = true);
    // dbg!(board_has_match(&boards[0]));

    // 12
    // 55
    // 37
    // 72
    // 91

    // &boards[0].entry(12).and_modify(|c| c.hit = true);
    &boards[0].entry(55).and_modify(|c| c.hit = true);
    &boards[0].entry(37).and_modify(|c| c.hit = true);
    &boards[0].entry(72).and_modify(|c| c.hit = true);
    &boards[0].entry(91).and_modify(|c| c.hit = true);
    dbg!(&boards[0]);
    dbg!(board_has_match(&boards[0]));
}
