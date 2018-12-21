#!/usr/bin/env python3

data = 793031


# Only two recipes are on the board: the first recipe got a score of 3, the second, 7.
recipes = [3, 7]

#The Elves think their skill will improve after making a few recipes (your puzzle input)

def create_recipes(r1, r2):
    return [int(x) for x in list(str(r1 + r2))]

def next_recipe_id(e, r, recipes):
    return (e + r + 1)%len(recipes)

def part1(recipes):
    e1 = 0
    e2 = 1
    while len(recipes) < (data + 10):
        
        r1 = recipes[e1]
        r2 = recipes[e2]
        # print('1:', e1, '->', r1)
        # print('2:', e2, '->', r2)
        # To create new recipes, the two Elves combine their current recipes.
        # This creates new recipes from the digits of the sum of the current recipes' scores.
        # ex 7 + 3 = 10 => 1, 0

        # The new recipes are added to the end of the scoreboard in the order they are created. 
        recipes += create_recipes(r1, r2)
        
        # print(iteration, recipes)
        # print(recipes)
        # each Elf picks a new current recipe
        # 1 plus the score of their current recipe
        # If they run out of recipes, they loop back around to the beginning.
        e1 = next_recipe_id(e1, r1, recipes)
        e2 = next_recipe_id(e2, r2, recipes)

    # you must identify the scores of the ten recipes after that
    # 793031 - 793041
    next_ten = recipes[-10:]
    print(''.join([str(x) for x in next_ten]))
    print('4910101614')

def part2(recipes):
    e1 = 0
    e2 = 1
    # data = 59414
    sdata = str(data)
    count = len(sdata)
    ldata = [int(x) for x in list(sdata)]
    while True:
        if len(recipes) > 67049746: # my answer has to be less than this
            print('too long..... try again')
            return
        r1 = recipes[e1]
        r2 = recipes[e2]
        new_recipes = create_recipes(r1, r2)
        for r in new_recipes:
            recipes.append(r)
            if len(recipes) > count:
                # match = True
                c = sum([1 for i in range(count) if recipes[-1 - i] != ldata[-1 - i]])
                # for i in range(count):
                #     if recipes[-1 - i] != ldata[-1 - i]:
                #         match = False
                #         break

                if c == 0:
            
                    print(len(recipes[:-1*count]))
                    print('67049746')
                    return

        e1 = next_recipe_id(e1, r1, recipes)
        e2 = next_recipe_id(e2, r2, recipes)

# part1(recipes[:])
part2(recipes[:])


# 3  7  1  0 [1] 0  1  2 (4) 5  1  5  8  9  1  6  7  7  9  2