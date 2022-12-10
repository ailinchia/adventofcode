use std::{io};
use std::borrow::Borrow;
use std::collections::HashMap;
use std::io::Read;
use regex::Regex;

struct Arrangement {
    to: usize,
    from: usize,
    count: usize,
}

fn process_input(input: &str) -> (HashMap<usize, String>, Vec<Arrangement>, usize) {
    let mut starting_crates = Vec::new();
    let mut arrangement = Vec::new();
    let mut done_crate = false;
    let re = Regex::new(r"move (\d+) from (\d+) to (\d+)").unwrap();
    for line in input.lines() {
        if line.is_empty() {
            done_crate = true;
            continue;
        }

        if !done_crate {
            starting_crates.push(line);
        } else {
            re.captures(line).map(|cap| {
                arrangement.push(Arrangement {
                    to: cap[3].parse::<usize>().unwrap(),
                    from: cap[2].parse::<usize>().unwrap(),
                    count: cap[1].parse::<usize>().unwrap(),
                });
            });
        }
    }

    let last = starting_crates.pop();
    let total_crates = last.unwrap().split_ascii_whitespace().last().unwrap().parse::<usize>().unwrap();

    let mut crates:HashMap<usize, String> = HashMap::new();
    starting_crates.iter().map(|line| {
        line.chars().enumerate().filter(|(i, _)| *i != 0 && (*i - 1) % 4 == 0).map(|(_, c)| c).collect::<String>()
    }).rev().for_each(|s | {
        s.chars().enumerate().for_each(|(j, c)| {
            if c.is_ascii_alphabetic() {
                crates.entry(j + 1).or_insert(String::new()).push(c);
            }
        });
    });

    (crates, arrangement, total_crates)
}

fn part1(input: &str) -> String {
    let (mut crates, arrangements, total_crates) = process_input(&input);
    arrangements.iter().for_each(|arrangement| {
        let s = crates[arrangement.from.borrow()].clone();
        let m = s[(s.len() - arrangement.count)..].chars().rev().collect::<String>();

        crates.entry(arrangement.from).or_insert(String::new()).truncate(s.len() - arrangement.count);
        crates.entry(arrangement.to).or_insert(String::new()).push_str(&m);
    });

    let mut s = String::new();
    for i in 1..total_crates + 1 {
        s.push(crates[&i].chars().last().unwrap());
    }
    s
}

fn part2(input: &str) -> String {
    let (mut crates, arrangements, total_crates) = process_input(&input);
    arrangements.iter().for_each(|arrangement| {
        let s = crates[arrangement.from.borrow()].clone();
        let m = s[(s.len() - arrangement.count)..].chars().collect::<String>();

        crates.entry(arrangement.from).or_insert(String::new()).truncate(s.len() - arrangement.count);
        crates.entry(arrangement.to).or_insert(String::new()).push_str(&m);
    });

    let mut s = String::new();
    for i in 1..total_crates + 1 {
        s.push(crates[&i].chars().last().unwrap());
    }
    s
}

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();

    println!("{}", part1(&input));
    println!("{}", part2(&input));
}

#[cfg(test)]
mod tests {
    use super::*;

    const DAY_NUM: &str = "05";

    #[test]
    fn test_input() {
        let filename = format!("day{}/input", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "TQRFCBSJJ");
        adventofcode::test_part(filename.as_str(), part2, "RMHFJNVFP");
    }

    #[test]
    fn test_inputa() {
        let filename = format!("day{}/inputa", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "CMZ");
        adventofcode::test_part(filename.as_str(), part2, "MCD");
    }
}