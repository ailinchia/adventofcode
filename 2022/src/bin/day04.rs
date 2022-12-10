use std::{io};
use std::io::Read;


fn part1(input: &str) -> String {
    let mut count = 0;
    input.lines().for_each(|line| {
        let (p1, p2) = line.split_once(",").unwrap();
        let (p1_start, p1_end) = p1.split_once("-").map(|(a, b)| (a.parse::<i32>().unwrap(), b.parse::<i32>().unwrap())).unwrap();
        let (p2_start, p2_end) = p2.split_once("-").map(|(a, b)| (a.parse::<i32>().unwrap(), b.parse::<i32>().unwrap())).unwrap();
        if (p1_start >= p2_start && p1_start <= p2_end) && (p1_end >= p2_start && p1_end <= p2_end) ||
            (p2_start >= p1_start && p2_start <= p1_end) && (p2_end >= p1_start && p2_end <= p1_end) {
            count += 1;
        }
    });
    count.to_string()
}

fn part2(input: &str) -> String {
    let mut count = 0;
    input.lines().for_each(|line| {
        let (p1, p2) = line.split_once(",").unwrap();
        let (p1_start, p1_end) = p1.split_once("-").map(|(a, b)| (a.parse::<i32>().unwrap(), b.parse::<i32>().unwrap())).unwrap();
        let (p2_start, p2_end) = p2.split_once("-").map(|(a, b)| (a.parse::<i32>().unwrap(), b.parse::<i32>().unwrap())).unwrap();
        if (p1_start >= p2_start && p1_start <= p2_end) || (p1_end >= p2_start && p1_end <= p2_end) ||
            (p2_start >= p1_start && p2_start <= p1_end) || (p2_end >= p1_start && p2_end <= p1_end) {
            count += 1;
        }
    });
    count.to_string()
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

    const DAY_NUM: &str = "04";

    #[test]
    fn test_input() {
        let filename = format!("day{}/input", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "477");
        adventofcode::test_part(filename.as_str(), part2, "830");
    }

    #[test]
    fn test_inputa() {
        let filename = format!("day{}/inputa", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "2");
        adventofcode::test_part(filename.as_str(), part2, "4");
    }
}