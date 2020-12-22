package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
)

const (
	borderTop    = 0
	borderRight  = 1
	borderBottom = 2
	borderLeft   = 3
	borderMax    = 4
)

func borderStr(b int) string {
	switch b {
	case borderTop:
		return "top"
	case borderBottom:
		return "bottom"
	case borderLeft:
		return "left"
	case borderRight:
		return "right"
	}
	return "invalid"
}

const (
	orientationNormal                 = 0
	orientationFlipHorizontal         = 1
	orientationFlipVertical           = 2
	orientationMax                    = 3
)

func orientationStr(o int) string {
	switch o {
	case orientationNormal:
		return "normal"
	case orientationFlipHorizontal:
		return "flipHorizontal"
	case orientationFlipVertical:
		return "flipVertical"
	}
	return "invalid"
}

type match struct {
	border      int
	orientation int
}

type tile struct {
	id int

	// normal flipHorizontal flipVertical
	// borderTop borderBottom borderLeft borderRight
	borders [orientationMax][borderMax]string

	matches    [orientationMax][borderMax]map[int][]match
	matchesIDs map[int]bool

	orientation int
	image       []string
}

func part1(cornerTiles []tile) {
	sum := 1
	for _, ct := range cornerTiles {
		sum *= ct.id
	}
	fmt.Println(sum)
}

func printImages(images [][]int, max int) {
	for y := 0; y < max; y++ {
		for x := 0; x < max; x++ {
			fmt.Print(images[y][x], "\t")
		}
		fmt.Println("")
	}
}

func flip(image []string, o int) []string {
	var newImage []string
	switch o {
	case orientationNormal:
		newImage = image
		break
	case orientationFlipHorizontal:
		for i := len(image) - 1; i >= 0; i-- {
			newImage = append(newImage, image[i])
		}
		break
	case orientationFlipVertical:
		for i := 0; i < len(image); i++ {
			newImage = append(newImage, reverse(image[i]))
		}
		break
	}
	return newImage
}

func rotate(image []string, step int) []string {
	i := make([][]rune, len(image))
	for y, _ := range i {
		i[y] = make([]rune, len(image))
	}

	for s := 0; s < step; s++ {
		for y := 0; y < len(image); y++ {
			for x := 0; x < len(image); x++ {
				i[x][len(image) - y - 1] = rune(image[y][x])
			}
		}
	}

	var newImage []string
	if step == 0 {
		newImage = image
	} else {
		for _, ix := range i {
			newImage = append(newImage, string(ix))
		}
	}
	return newImage
}

func getBorder(image []string, border int) string {
	if border == borderTop {
		return image[0]
	} else if border == borderBottom {
		return image[len(image) - 1]
	} else {
		s := ""
		for _, i := range image {
			if border == borderLeft {
				s += string(i[0])
			} else {
				s += string(i[len(i) - 1])
			}
		}
		return s
	}
}

func adjustImage(image0 []string, border0 int, image1 []string, border1 int) []string {
	newImage := append([]string(nil), image1...)
	b0 := getBorder(image0, border0)
	for o := 0; o < orientationMax; o++ {
		newImage = flip(image1, o)
		for b := 0; b < borderMax; b++ {
			newImage = rotate(newImage, 1)
			if b0 == getBorder(newImage, border1) {
				return newImage
			}
		}
	}
	return image1
}

func part2(tiles map[int]tile, sideTiles []tile) {
	max := int(math.Sqrt(float64(len(tiles))))
	images := make([][]int, max)
	for i := range images {
		images[i] = make([]int, max)
	}

	var sortedTiles []tile

	sideTilesMap := make(map[int]bool)
	for _, st := range sideTiles {
		sideTilesMap[st.id] = true
	}

	var topLeft tile
	for _, st := range sideTiles {
		if len(st.matches[orientationNormal][borderTop]) == 0 && len(st.matches[orientationNormal][borderLeft]) == 0 {
			topLeft = st
			break
		}
	}

	b := borderRight
	sortedTilesMap := make(map[int]bool)
	sortedTiles = append(sortedTiles, topLeft)
	sortedTilesMap[topLeft.id] = true

	for ; len(sortedTiles) < len(sideTiles); {
		s := sortedTiles[len(sortedTiles)-1]
		found := false
		for o := 0; o < orientationMax; o++ {
			if len(s.matches[o][b]) == 1 {
				for id := range s.matches[o][b] {
					if _, ok := sideTilesMap[id]; ok {
						if _, ok := sortedTilesMap[id]; !ok {
							sortedTiles = append(sortedTiles, tiles[id])
							sortedTilesMap[id] = true
							found = true
						}
					}
				}
			} else {
				break
			}
		}
		if !found {
			b++
			b %= borderMax
		}
	}

	// corners may not be accurate, but assume first entry is top left
	filledTiles := make(map[int]bool)
	y := 0
	x := 0
	for _, st := range sortedTiles {
		images[y][x] = st.id
		filledTiles[st.id] = true

		if y == 0 && x < max-1 {
			x++
		} else if x == max-1 && y < max-1 {
			y++
		} else if x == 0 {
			y--
		} else if y == max-1 {
			x--
		}
	}

	for y := 1; y < max-1; y++ {
		for x := 1; x < max-1; x++ {
			t1 := tiles[images[y-1][x]]
			t2 := tiles[images[y][x-1]]

			found := false
			for ti1, _ := range t1.matchesIDs {
				for ti2, _ := range t2.matchesIDs {
					if ti1 == ti2 {
						if _, ok := filledTiles[ti1]; !ok {
							images[y][x] = ti1
							filledTiles[ti1] = true
							found = true
							break
						}
					}
				}
				if found {
					break
				}
			}
		}
	}

	for y := 0; y < max; y++ {
		for x := 0; x < max; x++ {
			t := tiles[images[y][x]]

			if x+1 < max {
				tr := tiles[images[y][x+1]]
				tr.image = adjustImage(t.image, borderRight, tr.image, borderLeft)
				tiles[images[y][x+1]] = tr
			}
			if y+1 < max {
				tb := tiles[images[y+1][x]]
				tb.image = adjustImage(t.image, borderBottom, tb.image, borderTop)
				tiles[images[y+1][x]] = tb
			}
		}
	}

	var sea []string
	for y := 0; y < max; y++ {
		for z := 1; z < 9; z++ {
			l := ""
			for x := 0; x < max; x++ {
				l += tiles[images[y][x]].image[z][1:9]
				//fmt.Print(tiles[images[y][x]].image[z][1:9])
				//fmt.Print("|")
			}
			//fmt.Println("")
			sea = append(sea, l)
		}
		//for i := 0; i < max; i++ {
		//	fmt.Print("----------+")
		//}
		//fmt.Println("")
	}

	monsterStr := []string{
		"                  # ",
		"#    ##    ##    ###",
		" #  #  #  #  #  #   ",
	}

	type coordinate struct {
		y int
		x int
	}

	var monster []coordinate
	for y, m := range monsterStr {
		for x, c := range m {
			if c == '#' {
				monster = append(monster, coordinate{y, x})
			}
		}
	}


	found := false
	for o := 0; !found && o < orientationMax; o++ {
		newSea := flip(sea, o)
		for b := 0; !found && b < borderMax; b++ {
			newSea = rotate(newSea, 1)

			var seaMap [][]rune
			for _, s := range newSea {
				seaMap = append(seaMap, []rune(s))
			}

			maxY := len(seaMap)
			maxX := len(seaMap[0])
			for y := 0; y < maxY; y++ {
				for x := 0; x < maxX; x++ {
					count := 0
					for _, m := range monster {
						if x + m.x < maxX  && y + m.y < maxY {
							if seaMap[y + m.y][x + m.x] == '#' {
								count++
							}
						}
					}
					if count == len(monster) {
						found = true
						for _, m := range monster {
							seaMap[y + m.y][x + m.x] = 'O'
						}
					}
				}
			}
			if found {
				count := 0
				for y := 0; y < maxY; y++ {
					for x := 0; x < maxX; x++ {
						if seaMap[y][x] == '#' {
							count++
						}
					}
				}
				fmt.Println(count)
			}
		}
	}
}

func reverse(s string) string {
	runes := []rune(s)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

func convertToTile(image []string) tile {
	var t tile
	_, _ = fmt.Sscanf(image[0], "Tile %d", &t.id)

	t.image = image[1:]
	t.borders[orientationNormal][borderTop] = image[1]
	t.borders[orientationNormal][borderBottom] = image[len(image)-1]

	for p, i := range image {
		if p == 0 {
			continue
		}
		t.borders[orientationNormal][borderLeft] += string(i[0])
		t.borders[orientationNormal][borderRight] += string(i[len(i)-1])
	}

	// reverse borderLeft/borderRight
	t.borders[orientationFlipHorizontal][borderTop] = t.borders[orientationNormal][borderTop]
	t.borders[orientationFlipHorizontal][borderBottom] = t.borders[orientationNormal][borderBottom]
	t.borders[orientationFlipHorizontal][borderLeft] = reverse(t.borders[orientationNormal][borderLeft])
	t.borders[orientationFlipHorizontal][borderRight] = reverse(t.borders[orientationNormal][borderRight])

	// reverse borderTop/borderBottom
	t.borders[orientationFlipVertical][borderTop] = reverse(t.borders[orientationNormal][borderTop])
	t.borders[orientationFlipVertical][borderBottom] = reverse(t.borders[orientationNormal][borderBottom])
	t.borders[orientationFlipVertical][borderLeft] = t.borders[orientationNormal][borderLeft]
	t.borders[orientationFlipVertical][borderRight] = t.borders[orientationNormal][borderRight]

	// initialize map
	t.matchesIDs = make(map[int]bool)

	return t
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	tiles := make(map[int]tile)

	var image []string
	for scanner.Scan() {
		line := scanner.Text()

		if len(line) == 0 {
			t := convertToTile(image)
			tiles[t.id] = t
			image = []string{}
			continue
		}

		image = append(image, line)
	}

	// find matching sides
	for i, ti := range tiles {
		for j, tj := range tiles {
			if i == j {
				continue
			}

			for oi := 0; oi < orientationMax; oi++ {
				for oj := 0; oj < orientationMax; oj++ {
					for m, bi := range ti.borders[oi] {
						if ti.matches[oi][m] == nil {
							ti.matches[oi][m] = make(map[int][]match)
						}
						for n, bj := range tj.borders[oj] {
							if bi == bj {
								ti.matchesIDs[tj.id] = true
								ti.matches[oi][m][tj.id] = append(ti.matches[oi][m][tj.id], match{n, oj})
							}
						}
					}
				}
			}
		}
		tiles[i] = ti
	}

	// get corner/side tiles
	var cornerTiles []tile
	var sideTiles []tile
	for _, ti := range tiles {
		zeroCountSide := 0
		for b := 0; b < borderMax; b++ {
			count := 0
			for o := 0; o < orientationMax; o++ {
				count += len(ti.matches[o][b])
			}
			if count == 0 {
				zeroCountSide++
			}
		}

		if zeroCountSide >= 1 {
			sideTiles = append(sideTiles, ti)
			if zeroCountSide == 2 {
				cornerTiles = append(cornerTiles, ti)
			}
		}
	}

	part1(cornerTiles)
	part2(tiles, sideTiles)
}
