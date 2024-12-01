from itertools import combinations

GALAXY = '#'

def get_data():
  with open('data.txt') as f:
    return [list(line.strip()) for line in f.readlines()]

def expand(expand_factor: int, d: list[list[str]]) -> tuple[list[tuple[int,int]],list[tuple[int,int]]]:
  y_base = []
  x_base = []
  base = 0
  for y,line in enumerate(d):
    y_base.append(base)
    if line.count(GALAXY) == 0:
      base += expand_factor
    else:
      base += 1
  base = 0
  for x in range(len(d[0])):
    x_base.append(base)
    has_galaxy = False
    for y in range(len(d)):
      if d[y][x] == GALAXY:
        has_galaxy = True
        break
    if not has_galaxy:
      base += expand_factor
    else:
      base += 1
  return x_base,y_base

def find_galaxies(d: list[list[str]]) -> list[tuple[int,int]]:
  galaxies = []
  for y in range(len(d)):
    for x in range(len(d[0])):
      if d[y][x] == GALAXY:
        galaxies.append((x,y))
  return galaxies

def get_dist(galaxies: list[tuple[int,int]], expand_factor: int, d: list[list[str]]) -> int:
  x_ids,y_ids = expand(expand_factor, d)
  expanded_list = [(x_ids[x],y_ids[y]) for x,y in galaxies]
  
  total_dist = sum([abs(g1[0]-g2[0]) +abs(g1[1]-g2[1]) for g1,g2 in combinations(expanded_list, 2)])
  print(f'expand {expand_factor}: {total_dist}')


def observe():
  d = get_data()
  galaxy_list = find_galaxies(d)

  get_dist(galaxy_list, 2, d)
  get_dist(galaxy_list, int(1e6), d)

observe()