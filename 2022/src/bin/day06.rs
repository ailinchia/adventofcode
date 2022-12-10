use std::{io};
use std::collections::HashSet;
use std::io::Read;


fn get_marker(input: &str, uniq_seq: usize) -> usize {
    for line in input.lines() {
        for i in 0..line.len() {
            if line[i..i + uniq_seq].chars().collect::<HashSet<_>>().len() == uniq_seq {
                return i + uniq_seq
            }
        }
    }
    0
}

fn part1(input: &str) -> String {
    get_marker(input, 4).to_string()
}

fn part2(input: &str) -> String {
    get_marker(input, 14).to_string()
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

    const DAY_NUM: &str = "06";

    #[test]
    fn test_input() {
        let filename = format!("day{}/input", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "1909");
        adventofcode::test_part(filename.as_str(), part2, "3380");
    }

    #[test]
    fn test_inputa() {
        let filename = format!("day{}/inputa", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "7");
        adventofcode::test_part(filename.as_str(), part2, "19");
    }
}