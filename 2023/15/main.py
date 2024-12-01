def get_data() -> list[str]:
  data = ''
  with open('data.txt') as f:
    data = f.read().strip().split(',');
  return data

def hash(d: str) -> int:
  t = 0
  for c in d:
    t = ((t + ord(c))* 17) % 256
  return t

def part1():
  data = get_data()
  total = sum([hash(d) for d in data])
  print(total)

part1()