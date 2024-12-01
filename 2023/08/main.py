from math import lcm
def get_data()-> tuple[list[int], dict[str,tuple[str,str]]]:
  data = []
  with open('data.txt') as f:
    data = [line.strip() for line in f.readlines()]
  choices = [0 if c == 'L' else 1 for c in list(data[0])]
  map = {}
  for line in data[2:]:
    key,vals = line.split(' = (')
    map[key] = vals[:-1].split(', ')

  return choices,map

def part1():
  choices, map = get_data()
  key = 'AAA'
  steps = 0
  c = 0
  n_choices = len(choices)
  while key != 'ZZZ':
    key = map[key][choices[c]]
    steps += 1
    c = (c+1)%n_choices
  print(f'steps: {steps}')

def part2():
  choices,map = get_data()
  keys = [k for k in map.keys() if k[-1] == 'A']
  n_keys= len(keys)
  print(f'active keys: {n_keys}')
  steps = 0
  c = 0
  n_choices = len(choices)
  done = False
  while not done:
    done = True
    for k in range(n_keys):
      keys[k] = map[keys[k]][choices[c]]
      done = done and keys[k][-1] == 'Z'
    steps += 1
    c = (c+1) % n_choices
  print(f'steps: {steps}')

def walk_to_z(key: str, choices: list[int], map: dict[str,tuple[int,int]]) -> int:
  steps = 0
  c = 0
  n_choices = len(choices)
  done = False
  while not done:
  
    key = map[key][choices[c]]
    steps += 1
    c = (c+1)%n_choices
    done = key[-1] == 'Z'
    # print(key)
  return steps

def part2alt():
  choices,map = get_data()
  
  steps = [walk_to_z(k, choices, map) for k in map.keys() if k[-1] == 'A']
  total_steps = lcm(*steps)
  print(f'steps: {total_steps}')

# part1()
part2alt()