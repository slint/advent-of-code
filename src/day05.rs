use std::cmp;
use std::collections::HashMap;
use std::env;
use std::fs;

fn main() {
    let val = env::args().last().unwrap();
    println!("File name: {val}");
    let data = fs::read_to_string(val).unwrap();

    let (rules_block, pages_block) = data.split_once("\n\n").unwrap();

    let comes_before: HashMap<&str, Vec<&str>> = rules_block
        .lines()
        .map(|line| line.split_once('|').unwrap())
        .fold(HashMap::new(), |mut map, (key, val)| {
            map.entry(key).or_default().push(val);
            map
        });

    let comes_after: HashMap<&str, Vec<&str>> = rules_block
        .lines()
        .map(|line| line.split_once('|').unwrap())
        .fold(HashMap::new(), |mut map, (key, val)| {
            map.entry(val).or_default().push(key);
            map
        });

    let page_series = pages_block
        .lines()
        .map(|line| {
            line.split(',')
                .map(|s| s.to_string())
                .collect::<Vec<String>>()
        })
        .collect::<Vec<Vec<String>>>();

    let mut valid_series_middle_page_sum = 0;
    let mut incorrect_series_middle_page_sum = 0;
    for pages in page_series {
        let out_of_order_pages = get_out_of_order_pages(&pages, &comes_before, &comes_after);
        if out_of_order_pages.is_empty() {
            valid_series_middle_page_sum += pages[pages.len() / 2].parse::<u32>().unwrap();
        } else {
            let pages = correct_page_order(pages, out_of_order_pages, &comes_before, &comes_after);
            incorrect_series_middle_page_sum += pages[pages.len() / 2].parse::<u32>().unwrap();
        }
    }

    println!(
        "Sum of valid series middle pages: {}",
        valid_series_middle_page_sum
    );

    println!(
        "Sum of incorrect series middle pages: {}",
        incorrect_series_middle_page_sum
    );
}

fn correct_page_order(
    pages: Vec<String>,
    mut out_of_order_pages: Vec<String>,
    comes_before: &HashMap<&str, Vec<&str>>,
    comes_after: &HashMap<&str, Vec<&str>>,
) -> Vec<String> {
    // Remove all out of order pages
    let mut pages: Vec<String> = pages
        .clone()
        .iter()
        .filter_map(|page| {
            if !out_of_order_pages.contains(page) {
                Some(page.to_string())
            } else {
                None
            }
        })
        .collect();

    // Start adding each page until we find it's valid position
    while let Some(page) = out_of_order_pages.pop() {
        for insert_idx in 0..=pages.len() {
            let mut new_pages = pages.clone();
            new_pages.insert(insert_idx, page.clone());
            if get_out_of_order_pages(&new_pages, comes_before, comes_after).is_empty() {
                pages.insert(insert_idx, page);
                break;
            }
        }
    }
    pages
}

fn get_out_of_order_pages(
    pages: &Vec<String>,
    comes_before: &HashMap<&str, Vec<&str>>,
    comes_after: &HashMap<&str, Vec<&str>>,
) -> Vec<String> {
    pages
        .iter()
        .enumerate()
        .flat_map(|(cur_page_idx, cur_page)| {
            pages.iter().enumerate().filter_map(move |(idx, page)| {
                let is_page_valid = match cur_page_idx.cmp(&idx) {
                    cmp::Ordering::Less => comes_before
                        .get(cur_page.as_str())
                        .map(|page_list| page_list.contains(&page.as_str()))
                        .unwrap_or(true),
                    cmp::Ordering::Greater => comes_after
                        .get(cur_page.as_str())
                        .map(|page_list| page_list.contains(&page.as_str()))
                        .unwrap_or(true),
                    cmp::Ordering::Equal => true,
                };
                if !is_page_valid {
                    Some(cur_page.to_string())
                } else {
                    None
                }
            })
        })
        .collect::<std::collections::HashSet<_>>()
        .into_iter()
        .collect()
}
