def get_data() -> list[list[int]]:
  data=[]
  with open('data.txt') as f:
    data = [[int(i) for i in line.strip().split(' ')] for line in f.readlines()]
  return data

def get_next_value(history: list[int], reverse: bool, output: bool) -> int:
  h = history[0] if reverse else history[-1]
  change = [l - r for r,l in zip(history[:-1], history[1:])]
  s = set(change)
  if len(s) == 1 and 0 in s:
    if output: print(change)
    return h
  c = get_next_value(change, reverse, output)
  if output:
    print(change[:] + [f'({c})'])
    print(history)
    print(f'next: {h+c}')
  return h - c if reverse else h+c

def part1():
  data = get_data()
  total = sum([get_next_value(line, False, False) for line in data])
  print(f'total: {total}')

def part2():
  data = get_data()
  total = sum([get_next_value(line, True, False) for line in data])
  print(f'total2: {total}')

part2()