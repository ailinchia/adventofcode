use std::{io};
use std::cmp::{max, min};
use std::io::Read;


fn print_grid(grid: &Vec<String>) {
    for row in grid {
        println!("{}", row);
    }
}

fn extend_grid(grid: &mut Vec<String>) {
    let l = grid[0].len();
    grid.insert(0, String::from(".").repeat(l));
    grid.push(String::from(".").repeat(l));

    for row in grid {
        row.insert(0, '.');
        row.push('.');
    }
    // println!();
}

fn get_neighbours(count: usize, mut y: usize, mut x: usize) -> (Vec<(usize, usize)>, (usize, usize)) {
    let mut v = Vec::new();
    match (count % 4) {
        0 => {
            // If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north one step.
            v.push((y - 1, x - 1));
            v.push((y - 1, x));
            v.push((y - 1, x + 1));
            y -= 1;
        }
        1 => {
            // If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south one step.
            v.push((y + 1, x - 1));
            v.push((y + 1, x));
            v.push((y + 1, x + 1));
            y += 1;
        }
        2 => {
            // If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west one step.
            v.push((y - 1, x - 1));
            v.push((y, x - 1));
            v.push((y + 1, x - 1));
            x -= 1;
        }
        3 => {
            // If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east one step.
            v.push((y - 1, x + 1));
            v.push((y, x + 1));
            v.push((y + 1, x + 1));
            x += 1;
        }
        _ => {
            unreachable!("Invalid count {}", count % 4);
        }
    }
    (v, (y, x))
}

fn count_grid(grid: &Vec<String>) -> i32 {
    // get min/max y/x
    let mut min_y = grid.len();
    let mut max_y = 0;
    let mut min_x = grid[0].len();
    let mut max_x = 0;

    for (y, row) in grid.iter().enumerate() {
        if row.contains('#') {
            min_y = min(min_y, y);
            max_y = max(max_y, y);
        }
        for (x, c) in row.chars().enumerate() {
            if c == '#' {
                min_x = min(min_x, x);
                max_x = max(max_x, x);
            }
        }
    }

    let mut count = 0;
    for y in min_y..max_y + 1 {
        for x in min_x..max_x + 1 {
            if grid[y].as_bytes()[x] == '.' as u8 {
                count += 1;
            }
        }
    }
    count
}

fn part1(input: &str) -> String {
    let mut grid: Vec<String> = Vec::new();
    for line in input.lines() {
        grid.push(line.to_string());
    }

    for i in 0..10 {
        extend_grid(&mut grid);

        let mut proposal_grid: Vec<String> = vec![String::from("0").repeat(grid[0].len()); grid.len()];
        const ELF: u8 = '#' as u8;
        for y in 0..proposal_grid.len() {
            for x in 0..proposal_grid[0].len() {
                if grid[y].as_bytes()[x] == ELF {
                    // If no other Elves are in one of those eight positions, the Elf does not do anything.
                    if grid[y - 1].as_bytes()[x] != ELF && grid[y - 1].as_bytes()[x - 1] != ELF && grid[y - 1].as_bytes()[x + 1] != ELF &&
                        grid[y + 1].as_bytes()[x] != ELF && grid[y + 1].as_bytes()[x - 1] != ELF && grid[y + 1].as_bytes()[x + 1] != ELF &&
                        grid[y].as_bytes()[x - 1] != ELF && grid[y].as_bytes()[x + 1] != ELF {
                        let c = (proposal_grid[y].as_bytes()[x] + 1) as char;
                        proposal_grid[y].replace_range(x..x+1, c.to_string().as_str());
                    } else {
                        for j in 0..4 {
                            let mut passed = true;
                            let (rules, (m_y, m_x)) = get_neighbours(i + j, y, x);
                            for (r_y, r_x) in rules {
                                if grid[r_y].as_bytes()[r_x] == ELF {
                                    passed = false;
                                    break;
                                }
                            }
                            if passed {
                                let c = (proposal_grid[m_y].as_bytes()[m_x] + 1) as char;
                                proposal_grid[m_y].replace_range(m_x..m_x+1, c.to_string().as_str());
                                break;
                            }
                        }
                    }
                }
            }
        }

        let mut new_grid: Vec<String> = vec![String::from(".").repeat(grid[0].len()); grid.len()];
        for y in 0..new_grid.len() {
            for x in 0..new_grid[0].len() {
                if grid[y].as_bytes()[x] == ELF {
                    // If no other Elves are in one of those eight positions, the Elf does not do anything.
                    if grid[y - 1].as_bytes()[x] != ELF && grid[y - 1].as_bytes()[x - 1] != ELF && grid[y - 1].as_bytes()[x + 1] != ELF &&
                        grid[y + 1].as_bytes()[x] != ELF && grid[y + 1].as_bytes()[x - 1] != ELF && grid[y + 1].as_bytes()[x + 1] != ELF &&
                        grid[y].as_bytes()[x - 1] != ELF && grid[y].as_bytes()[x + 1] != ELF {
                        new_grid[y].replace_range(x..x+1, "#");
                    } else {
                        let mut all_failed = true;
                        for j in 0..4 {
                            let mut passed = true;
                            let (rules, (m_y, m_x)) = get_neighbours(i + j, y, x);
                            for (r_y, r_x) in rules {
                                if grid[r_y].as_bytes()[r_x] == ELF {
                                    passed = false;
                                    break;
                                }
                            }
                            if passed {
                                all_failed = false;
                                if (proposal_grid[m_y].as_bytes()[m_x]) == '1' as u8 {
                                    new_grid[m_y].replace_range(m_x..m_x + 1, "#");
                                } else {
                                    new_grid[y].replace_range(x..x + 1, "#");
                                }
                                break;
                            }
                        }
                        if all_failed {
                            new_grid[y].replace_range(x..x+1, "#");
                        }
                    }
                }
            }
        }
        // println!("End of round {}", i + 1);
        // println!("Grid:");
        // print_grid(&grid);
        // println!("Proposal Grid:");
        // print_grid(&proposal_grid);
        // println!("New Grid:");
        // print_grid(&new_grid);
        grid = new_grid;
        // print_grid(&grid);
    }

    count_grid(&grid).to_string()
}

fn part2(input: &str) -> String {
    let mut grid: Vec<String> = Vec::new();
    for line in input.lines() {
        grid.push(line.to_string());
    }

    let mut i = 0;
    loop {
        extend_grid(&mut grid);

        let mut proposal_grid: Vec<String> = vec![String::from("0").repeat(grid[0].len()); grid.len()];
        const ELF: u8 = '#' as u8;
        for y in 0..proposal_grid.len() {
            for x in 0..proposal_grid[0].len() {
                if grid[y].as_bytes()[x] == ELF {
                    // If no other Elves are in one of those eight positions, the Elf does not do anything.
                    if grid[y - 1].as_bytes()[x] != ELF && grid[y - 1].as_bytes()[x - 1] != ELF && grid[y - 1].as_bytes()[x + 1] != ELF &&
                        grid[y + 1].as_bytes()[x] != ELF && grid[y + 1].as_bytes()[x - 1] != ELF && grid[y + 1].as_bytes()[x + 1] != ELF &&
                        grid[y].as_bytes()[x - 1] != ELF && grid[y].as_bytes()[x + 1] != ELF {
                        let c = (proposal_grid[y].as_bytes()[x] + 1) as char;
                        proposal_grid[y].replace_range(x..x+1, c.to_string().as_str());
                    } else {
                        for j in 0..4 {
                            let mut passed = true;
                            let (rules, (m_y, m_x)) = get_neighbours(i + j, y, x);
                            for (r_y, r_x) in rules {
                                if grid[r_y].as_bytes()[r_x] == ELF {
                                    passed = false;
                                    break;
                                }
                            }
                            if passed {
                                let c = (proposal_grid[m_y].as_bytes()[m_x] + 1) as char;
                                proposal_grid[m_y].replace_range(m_x..m_x+1, c.to_string().as_str());
                                break;
                            }
                        }
                    }
                }
            }
        }

        let mut new_grid: Vec<String> = vec![String::from(".").repeat(grid[0].len()); grid.len()];
        for y in 0..new_grid.len() {
            for x in 0..new_grid[0].len() {
                if grid[y].as_bytes()[x] == ELF {
                    // If no other Elves are in one of those eight positions, the Elf does not do anything.
                    if grid[y - 1].as_bytes()[x] != ELF && grid[y - 1].as_bytes()[x - 1] != ELF && grid[y - 1].as_bytes()[x + 1] != ELF &&
                        grid[y + 1].as_bytes()[x] != ELF && grid[y + 1].as_bytes()[x - 1] != ELF && grid[y + 1].as_bytes()[x + 1] != ELF &&
                        grid[y].as_bytes()[x - 1] != ELF && grid[y].as_bytes()[x + 1] != ELF {
                        new_grid[y].replace_range(x..x+1, "#");
                    } else {
                        let mut all_failed = true;
                        for j in 0..4 {
                            let mut passed = true;
                            let (rules, (m_y, m_x)) = get_neighbours(i + j, y, x);
                            for (r_y, r_x) in rules {
                                if grid[r_y].as_bytes()[r_x] == ELF {
                                    passed = false;
                                    break;
                                }
                            }
                            if passed {
                                all_failed = false;
                                if (proposal_grid[m_y].as_bytes()[m_x]) == '1' as u8 {
                                    new_grid[m_y].replace_range(m_x..m_x + 1, "#");
                                } else {
                                    new_grid[y].replace_range(x..x + 1, "#");
                                }
                                break;
                            }
                        }
                        if all_failed {
                            new_grid[y].replace_range(x..x+1, "#");
                        }
                    }
                }
            }
        }
        // println!("End of round {}", i + 1);
        // println!("Grid:");
        // print_grid(&grid);
        // println!("Proposal Grid:");
        // print_grid(&proposal_grid);
        // println!("New Grid:");
        // print_grid(&new_grid);
        if grid == new_grid {
            break;
        }
        grid = new_grid;
        i += 1;
        // print_grid(&grid);
    }

    (i + 1).to_string()
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

    const DAY_NUM: &str = "23";

    #[test]
    fn test_input() {
        let filename = format!("day{}/input", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "");
        adventofcode::test_part(filename.as_str(), part2, "");
    }

    #[test]
    fn test_inputa() {
        let filename = format!("day{}/inputa", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "");
        adventofcode::test_part(filename.as_str(), part2, "");
    }
}