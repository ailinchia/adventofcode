use std::{io};
use std::cmp::{max, min};
use std::collections::{HashMap, HashSet};
use std::io::Read;
use pathfinding::num_traits::abs;
use rust_lapper::Lapper;

#[derive(Debug, Clone, Copy)]
struct Coord {
    x: i32,
    y: i32,
}

fn print_grid(grid: &Vec<Vec<char>>) {
    for (y, row) in grid.iter().enumerate() {
        print!("{}\t", y);
        for col in row {
            print!("{}", col);
        }
        println!();
    }
}

const Y_POS: i32 = 2000000;

// 2732042 too low
// 4712648 too low
fn part1(input: &str) -> String {
    let re = regex::Regex::new(r"Sensor at x=([0-9\-]+), y=([0-9\-]+): closest beacon is at x=([0-9\-]+), y=([0-9\-]+)").unwrap();
    let mut beacons = Vec::new();
    let mut sensors = Vec::new();

    for line in input.lines() {
        let cap = re.captures(line).unwrap();
        let sensor = Coord {
            x: cap[1].parse().unwrap(),
            y: cap[2].parse().unwrap(),
        };
        let beacon = Coord {
            x: cap[3].parse().unwrap(),
            y: cap[4].parse().unwrap(),
        };

        // println!("sensor={:?} beacon={:?}", sensor.clone(), beacon.clone());
        beacons.push(beacon);
        sensors.push(sensor);
    }

    // let mut grid = vec![vec!['.'; (max_x - min_x + 1) as usize]; (max_y - min_y + 1) as usize];
    let mut row_y = HashSet::new();
    let mut beacon_y = HashSet::new();
    for i in 0..beacons.len() {
        let beacon = beacons[i];
        let sensor = sensors[i];

        if beacon.y == Y_POS {
            beacon_y.insert(beacon.x);
        }
        let distance = abs(beacon.y - sensor.y) + abs(beacon.x - sensor.x);
        let distance_y = abs(sensor.y - Y_POS);
        // println!("distance={} distance_y={}", distance, distance_y);
        if distance_y < distance {
            let d_y = distance - distance_y;
            for d in 0..=d_y {
                row_y.insert(sensor.x + d);
                row_y.insert(sensor.x - d);
            }
        }
    }

    (row_y.len() - beacon_y.len()).to_string()
}

const MAX_Y: i32 = 4000000;
const MAX_X: i32 = 4000000;

fn part2(input: &str) -> String {
    let re = regex::Regex::new(r"Sensor at x=([0-9\-]+), y=([0-9\-]+): closest beacon is at x=([0-9\-]+), y=([0-9\-]+)").unwrap();
    let mut beacons = Vec::new();
    let mut sensors = Vec::new();

    for line in input.lines() {
        let cap = re.captures(line).unwrap();
        let sensor = Coord {
            x: cap[1].parse().unwrap(),
            y: cap[2].parse().unwrap(),
        };
        let beacon = Coord {
            x: cap[3].parse().unwrap(),
            y: cap[4].parse().unwrap(),
        };
        beacons.push(beacon);
        sensors.push(sensor);
    }

    for y in 0..=MAX_Y {
        // for x in 0..=MAX_X {
        // let mut row_y = HashSet::new();
        let mut mm_lap = Vec::new();
        let mut mm_y = Vec::new();
        let mut beacon_y = HashSet::new();
        for i in 0..beacons.len() {
            let beacon = beacons[i];
            let sensor = sensors[i];

            if beacon.y == y {
                beacon_y.insert(beacon.x);
            }
            let distance = abs(beacon.y - sensor.y) + abs(beacon.x - sensor.x);
            let distance_y = abs(sensor.y - y);
            // println!("distance={} distance_y={}", distance, distance_y);
            if distance_y < distance {
                let d_y = distance - distance_y;
                let mut ls = 0;
                if (sensor.x - d_y) > 0 {
                    ls = (sensor.x - d_y) as u32;
                }
                let mut le = MAX_Y as u32;
                if (sensor.x + d_y) < MAX_Y {
                    le = (sensor.x + d_y) as u32;
                }

                mm_lap.push(rust_lapper::Interval {
                    start: ls,
                    stop: le + 1,
                    val: 0,
                });
                mm_y.push((sensor.x - d_y, sensor.x + d_y));
                // for d in 0..=d_y {
                //     if sensor.x + d <= MAX_X {
                //         row_y.insert(sensor.x + d);
                //     }
                //     if sensor.x - d >= 0 {
                //         row_y.insert(sensor.x - d);
                //     }
                // }
            }
        }

        // println!("y={} mm_y={}", y, mm_y.len());
        // println!("y={} row_y={:?}", y, mm_y);
        // }
        let mut laps = Lapper::new(mm_lap);
        let mut count = laps.cov();
        if count == MAX_Y as u32 {
            // println!("y={} lap_y={}", y, count);
            laps.merge_overlaps();
            return (laps.intervals[0].stop as u64 * 4000000 as u64 + y as u64).to_string();
        }
    }

    "".to_string()
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

    const DAY_NUM: &str = "15";

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