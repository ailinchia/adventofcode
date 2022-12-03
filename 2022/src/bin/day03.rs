use std::{io};
use std::collections::HashSet;
use std::io::Read;

fn get_priority(c: char) -> i32 {
    if c.is_lowercase() {
        c as i32 - 'a' as i32 + 1
    } else {
        c as i32 - 'A' as i32 + 27
    }
}

fn part1(input: &str) -> String {
    let mut priorities = 0;
    input.lines().for_each(|line| {
        let (l1, l2) = line.split_at(line.len() / 2);
        priorities = l1.chars().filter(|c| l2.contains(*c)).collect::<HashSet<_>>().iter().fold(priorities, |acc, c| acc + get_priority(*c))
    });
    priorities.to_string()
}

fn part2(input: &str) -> String {
    let mut it = input.lines().into_iter();
    let mut priorities = 0;
    while let Some(l1) = it.next() {
        let l2 = it.next().unwrap();
        let l3 = it.next().unwrap();
        priorities = l1.chars().filter(|c| l2.contains(*c) && l3.contains(*c)).collect::<HashSet<_>>().iter().fold(priorities, |acc, c| acc + get_priority(*c))
    }
    priorities.to_string()
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

    const DAY_NUM: &str = "03";

    #[test]
    fn test_input() {
        let filename = format!("day{}/input", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "7817");
        adventofcode::test_part(filename.as_str(), part2, "2444");
    }

    #[test]
    fn test_inputa() {
        let filename = format!("day{}/inputa", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "157");
        adventofcode::test_part(filename.as_str(), part2, "70");
    }
}