package main

import (
	"bufio"
	"fmt"
	"github.com/juliangruber/go-intersect"
	"os"
	"sort"
	"strings"
)

type food struct {
	ingredients []string
	allergens map[string]bool
}

func part1(foods []food, ingredientsList, allergensList map[string]bool) map[string][]interface{} {
	allergensIngredientsList := make(map[string][]interface{})

	for a, _ := range allergensList {
		var ingredientsWithAllergen []interface{}
		for x, fx := range foods {
			if _, ok := fx.allergens[a]; !ok {
				continue
			}
			for _, i := range fx.ingredients {
				ingredientsWithAllergen = append(ingredientsWithAllergen, i)
			}

			for y, fy := range foods {
				if x == y {
					continue
				}
				if _, ok := fy.allergens[a]; !ok {
					continue
				}

				ingredientsWithAllergen = intersect.Hash(ingredientsWithAllergen, fy.ingredients).([]interface{})
			}
		}
		allergensIngredientsList[a] = ingredientsWithAllergen
		for _, ia := range ingredientsWithAllergen {
			ingredientsList[ia.(string)] = false
		}
	}

	count := 0
	for k, v := range ingredientsList {
		if v {
			for _, fx := range foods {
				for _, f := range fx.ingredients {
					if f == k {
						count++
						break
					}
				}
			}
		}
	}
	fmt.Println(count)
	return allergensIngredientsList
}

func part2(allergensIngredientsList map[string][]interface{}) {
	for {
		count := 0
		for x, ilx := range allergensIngredientsList {
			if len(ilx) == 1 {
				ix := ilx[0]
				for y, ily := range allergensIngredientsList {
					if x == y || len(ily) == 1 {
						continue
					}
					var newIly []interface{}
					for _, iy := range ily {
						if iy != ix {
							newIly = append(newIly, iy)
						}
					}
					allergensIngredientsList[y] = newIly
				}
				count++
			}
		}

		if count == len(allergensIngredientsList) {
			break
		}
	}

	var allergens []string
	var ingredients []string
	for a, _ := range allergensIngredientsList {
		allergens = append(allergens, a)
	}
	sort.Strings(allergens)
	for _, a := range allergens {
		ingredients = append(ingredients, allergensIngredientsList[a][0].(string))
	}
	fmt.Println(strings.Join(ingredients, ","))
}


func main() {
	scanner := bufio.NewScanner(os.Stdin)

	allergensList := make(map[string]bool)
	ingredientsList := make(map[string]bool)
	var foods []food
	for scanner.Scan() {
		// mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
		line := scanner.Text()
		values := strings.Split(line, " (contains ")
		var f food

		f.ingredients = strings.Split(values[0], " ")
		for _, i := range f.ingredients {
			ingredientsList[i] = true
		}

		f.allergens = make(map[string]bool)
		as := strings.Split(values[1][:len(values[1]) - 1], ", ")
		for _, a := range as {
			allergensList[a] = true
			f.allergens[a] = true
		}

		foods = append(foods, f)
	}

	allergensIngredientsList := part1(foods, ingredientsList, allergensList)
	part2(allergensIngredientsList)
}
