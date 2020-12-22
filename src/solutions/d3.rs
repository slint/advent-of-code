#[derive(Debug, Copy, Clone)]
enum Space {
    None,
    Tree,
    Open,
}

type SlopeMap = Vec<Vec<Space>>;

fn parse_tree_map(data: String) -> SlopeMap {
    let lines: Vec<&str> = data.lines().collect();
    let mut map = vec![vec![Space::None; lines.iter().nth(0).unwrap().len()]; lines.len()];
    for (row, line) in lines.iter().enumerate() {
        for (col, c) in line.chars().enumerate() {
            map[row][col] = match c {
                '.' => Space::Open,
                '#' => Space::Tree,
                _ => Space::None,
            }
        }
    }
    map
}

fn descent_map(map: &SlopeMap, x_add: usize, y_add: usize) -> u32 {
    let mut trees_count = 0;
    let mut x_pos: usize = 0;
    let mut y_pos: usize = 0;
    let map_width = map[0].len();
    let map_height = map.len();

    println!("{}x{}", map_width, map_height);

    loop {
        match map[y_pos][x_pos % map_width] {
            Space::Tree => trees_count += 1,
            _ => (),
        }
        x_pos += x_add;
        y_pos += y_add;
        if y_pos >= map_height {
            break;
        }
    }
    trees_count
}

pub fn run(input: String) {
    let map = parse_tree_map(input);
    let pairs: Vec<(usize, usize)> = vec![(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)];

    let res: u64 = pairs
        .iter()
        .map(|(x, y)| descent_map(&map, *x, *y) as u64)
        .product();
    println!("The product of all slope trees is {}.", res);
}
