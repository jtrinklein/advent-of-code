CUBE = '#'
ROUND= 'O'
EMPTY = '.'

def get_data() -> list[list[str]]:
  data = []

  with open('data.txt') as f:
    data = [list(line.strip()) for line in f.readlines()]
  columns =None
  for line in data:
    if columns is None:
      columns = [[c] for c in line[::-1]]
    else:
      columns = [tstr + [c] for tstr,c in zip(columns,line[::-1])]
  return columns

def p(d: list[str]):
  for line in d:
    print(line)

def get_stress(d: list[str]):
  total = 0
  length = len(d[0])
  # print('0')
  # print('1987654321')
  for line in d:
    # print(line, end='')
    sections = line.split(CUBE)
    base = 0
    l_total = 0
    for s in sections:
      total += sum([i for i in range(length - base,length - s.count(ROUND) - base, -1)])
      base += len(s) + 1
      # print(f' {v}', end='')
      # l_total += v
    # print(f'  {l_total}')
    # total += l_total
  return total

d = get_data()
print(get_stress(d))
    