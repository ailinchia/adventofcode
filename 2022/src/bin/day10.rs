use std::{io};
use std::io::Read;

fn signal_strength(cycle: i32, x: i32) -> i32 {
    if cycle == 20 || ((cycle - 20) % 40) == 0 {
        cycle * x
    } else {
        0
    }
}

fn part1(input: &str) -> String {
    let mut cycle = 0;
    let mut x = 1;
    let mut sum = 0;

    for line in input.lines() {
        cycle += 1;
        sum += signal_strength(cycle, x);
        if line == "noop" {
            continue;
        } else {
            cycle += 1;
            sum += signal_strength(cycle, x);
            x += line.split_once(" ").map(|(a, b)| (a, b.parse::<i32>().unwrap())).unwrap().1;
        }
    }
    sum.to_string()
}

fn print_crt(crt: &Vec<Vec<char>>) {
    for y in 0..crt.len() {
        for x in 0..crt[y].len() {
            print!("{}", crt[y][x]);
        }
        println!();
    }
}

fn set_crt(crt: &mut Vec<Vec<char>>, cycle: i32, x: i32) {
    let sprite_start_pos = x - 1;
    let crt_draw_pos = (cycle - 1) % 40;
    if crt_draw_pos >= sprite_start_pos && crt_draw_pos <= sprite_start_pos + 2 {
        let row = crt.get_mut(((cycle - 1) / 40) as usize).unwrap();
        row[crt_draw_pos as usize] = '#';
    }
}

fn part2(input: &str) -> String {
    let mut crt = vec![vec![' '; 40]; 6];

    let mut cycle = 0;
    let mut x = 1;
    for line in input.lines() {
        cycle += 1;
        set_crt(&mut crt, cycle, x);
        if line == "noop" {
            continue;
        } else {
            cycle += 1;
            set_crt(&mut crt, cycle, x);
            let tokens = line.split_once(" ").map(|(a, b)| (a, b.parse::<i32>().unwrap())).unwrap();
            x += tokens.1;
        }
    }
    // print_crt(&crt);

    crt.iter().map(|row| {
        let mut s = row.iter().collect::<String>();
        s.push('\n');
        s
    }).collect::<String>()
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

    const DAY_NUM: &str = "10";

    #[test]
    fn test_input() {
        let filename = format!("day{}/input", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "15140");

        let expected = "\
###  ###    ##  ##  ####  ##   ##  ###  \n\
#  # #  #    # #  #    # #  # #  # #  # \n\
###  #  #    # #  #   #  #    #  # #  # \n\
#  # ###     # ####  #   # ## #### ###  \n\
#  # #    #  # #  # #    #  # #  # #    \n\
###  #     ##  #  # ####  ### #  # #    \n\
";
        adventofcode::test_part(filename.as_str(), part2, expected);
    }

    #[test]
    fn test_inputa() {
        let filename = format!("day{}/inputa", DAY_NUM);
        adventofcode::test_part(filename.as_str(), part1, "13140");

        let expected = "\
##  ##  ##  ##  ##  ##  ##  ##  ##  ##  \n\
###   ###   ###   ###   ###   ###   ### \n\
####    ####    ####    ####    ####    \n\
#####     #####     #####     #####     \n\
######      ######      ######      ####\n\
#######       #######       #######     \n\
";
        adventofcode::test_part(filename.as_str(), part2, expected);
    }
}