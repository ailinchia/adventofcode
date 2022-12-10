use std::{io};
use std::io::Read;

#[derive(Clone)]
struct Motion {
    direction: char,
    distance: i32,
}

fn parse_input(input: &str) -> Vec<Motion> {
    input.lines().map(|line| {
        line.split_once(" ").map(|(a, b)| {
            Motion { direction: a.chars().next().unwrap(), distance: b.parse::<i32>().unwrap() }
        }).unwrap()
    }).collect::<Vec<_>>()
}

// fn print_map(map: &Vec<Vec<char>>, move_cursor: bool) {
//     for y in 0..map.len() {
//         for x in 0..map[y].len() {
//             print!("{}", map[y][x]);
//         }
//         println!();
//     }
//     if move_cursor {
//         print!("\x1b[{}A", map.len());
//     }
// }

fn is_touching(hy: usize, hx: usize, ty: usize, tx: usize) -> bool {
    (hy as i32 - ty as i32).abs() <= 1 && (hx as i32 - tx as i32).abs() <= 1
}

fn move_tail(map: &mut Vec<Vec<char>>, hy: usize, hx: usize, ty: &mut usize, tx: &mut usize, c: char, tc: char) {
    if !is_touching(hy, hx, *ty, *tx) {
        if hy == *ty {
            // same row
            *tx = if hx < *tx { *tx - 1 } else { *tx + 1 };
        } else if hx == *tx {
            // same column
            *ty = if hy < *ty { *ty - 1 } else { *ty + 1 };
        } else {
            // diagonal
            *ty = if hy < *ty { *ty - 1 } else { *ty + 1 };
            *tx = if hx < *tx { *tx - 1 } else { *tx + 1 };
        }
    }

    if c == tc {
        map[*ty][*tx] = c;
    }
}

fn count_map(map: &Vec<Vec<char>>, c: char) -> i32 {
    let mut count = 0;
    for y in 0..map.len() {
        for x in 0..map[y].len() {
            if map[y][x] == c {
                count += 1;
            }
        }
    }
    count
}

fn process_motions(motions: Vec<Motion>, len: usize) -> i32 {
    // 2d map
    let size_y = 400;
    let size_x = 400;
    let mut map = vec![vec!['.'; size_x]; size_y];

    let mut y = vec![size_y / 2; len];
    let mut x = vec![size_x / 2; len];

    let c = (len as u8 - 2 + '0' as u8) as char;

    for motion in motions {
        for _ in 0..motion.distance {
            match motion.direction {
                'U' => {
                    y[0] -= 1;
                }
                'D' => {
                    y[0] += 1;
                }
                'L' => {
                    x[0] -= 1;
                }
                'R' => {
                    x[0] += 1;
                }
                _ => panic!("Unknown direction"),
            }
            for i in 0..y.len() - 1 {
                move_tail(&mut map, y[i], x[i], &mut y[i + 1], &mut x[i + 1], i.to_string().chars().next().unwrap(), c);
            }
        }
    }
    // print_map(&map, false);
    count_map(&map, c)
}

fn part1(input: &str) -> String {
    let motions = parse_input(&input);
    process_motions(motions, 2).to_string()
}

fn part2(input: &str) -> String {
    let motions = parse_input(&input);
    process_motions(motions, 10).to_string()
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

    const DAY_NUM: &str = "09";

    #[test]
    fn test_input() {
        let filename = format!("day{}/input", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "6243");
        adventofcode::test_part(filename.as_str(), part2, "2630");
    }

    #[test]
    fn test_inputa() {
        let filename = format!("day{}/inputa", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "13");
    }

    #[test]
    fn test_inputb() {
        let filename = format!("day{}/inputb", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part2, "36");
    }
}