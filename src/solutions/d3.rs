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

fn descent_map(map: &SlopeMap) -> u32 {
    let mut trees_count = 0;
    let mut x_pos = 0;
    let mut y_pos = 0;
    let map_width = map[0].len();
    let map_height = map.len();

    println!("{}x{}", map_width, map_height);

    loop {
        match map[y_pos][x_pos % map_width] {
            Space::Tree => trees_count += 1,
            _ => (),
        }
        x_pos += 3;
        y_pos += 1;
        if y_pos >= map_height {
            break;
        }
    }
    trees_count
}

pub fn run(input: String) {
    let map = parse_tree_map(input);
    let tress = descent_map(&map);
    println!("The path has {} trees.", tress);
}
