#!/usr/bin/env python3

data = None
with open('./15-data.txt') as f:
    data = f.read().splitlines()
data = [
    'Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8',
    'Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3',
]
ingredients = []
for line in data:
    # Sugar: capacity -1, durability 0, flavor 0, texture 2, calories 8
    name, stats = line.split(': ')
    name = name[:-1]
    ingredient = {'stats': [], 'value': 0}
    
    for stat in stats.split(', '):
        stat_name, value = stat.split()
        value = int(value)
        # ingredient[stat_name] = value
        ingredient['stats'].append(value)
        ingredient['value'] += value
    
    ingredients.append(ingredient)
ingredients.sort(key=lambda x: x['value'], reverse=True)

def get_score(weights):
    scores = []
    # for each stat 
    for i in range(4):
        stat_score = 0
        # sum the weighted score for each ingredient 
        for j in range(len(ingredients)):
            stat = ingredients[j]['stats'][i]
            weight = weights[j]
            stat_score += weight * stat
        scores.append(max(0, stat_score))

    return sum(scores)

def get_best_score():
    initial_weight = 100 // len(ingredients)
    weights = [initial_weight for x in range(len(ingredients))]
    if sum(weights) < 100:
        weights[0] += 100 - sum(weights)
    
    base = get_score(weights)
    weights[0] += 1
    weights[-1] -= 1
    np1 = get_score(weights)
    if np1 > base:
        while np1 > base and weights[-1] >= 0:
            base = np1
            weights[0] += 1
            weights[-1] -= 1
            np1 = get_score(weights)
        weights[0] -= 1
        weights[-1] += 1
    else:
        base, np1 = np1, base
        while np1 > base and weights[0] >= 0:
            base = np1
            weights[0] -= 1
            weights[-1] += 1
            np1 = get_score(weights)
        weights[0] += 1
        weights[-1] -= 1
    
    return base, weights

score, weights = get_best_score()
print(f'score: {score} weights: {weights}')



    



print(ingredients)
print('ok')