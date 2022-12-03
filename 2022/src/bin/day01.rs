use std::{io};
use std::cmp::max;
use std::io::Read;


fn part1(input: &str) -> String {
    let mut max_calories = 0;
    let mut current_calories = 0;
    for line in input.lines() {
        if line.is_empty() {
            max_calories = max(max_calories, current_calories);
            current_calories = 0;
            continue;
        }
        current_calories += line.parse::<i32>().unwrap();
    }

    max_calories.to_string()
}

fn part2(input: &str) -> String {
    let mut max_calories = 0;
    let mut current_calories = 0;
    let mut calories = Vec::new();
    for line in input.lines() {
        if line.is_empty() {
            max_calories = max(max_calories, current_calories);
            calories.push(current_calories);
            current_calories = 0;
            continue;
        }
        current_calories += line.parse::<i32>().unwrap();
    }

    calories.sort_by(|a, b| b.cmp(a));

    calories.iter().take(3).sum::<i32>().to_string()
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

    const DAY_NUM: &str = "01";

    #[test]
    fn test_input() {
        let filename = format!("day{}/input", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "72602");
        adventofcode::test_part(filename.as_str(), part2, "207410");
    }

    #[test]
    fn test_inputa() {
        let filename = format!("day{}/inputa", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "24000");
        adventofcode::test_part(filename.as_str(), part2, "41000");
    }
}