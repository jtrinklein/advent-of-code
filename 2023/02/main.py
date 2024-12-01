from dataclasses import dataclass

@dataclass
class RoundInfo:
  r: int
  g: int
  b: int


@dataclass()
class GameStats:
  id: int
  max_r: int
  max_g: int
  max_b: int

  def get_power(self) -> int:
    return max(1, self.max_r) * max(1, self.max_g) * max(1, self.max_b)
  
  def under_limit(self, limit: RoundInfo) -> bool:
    return self.max_r <= limit.r and self.max_g <= limit.g and self.max_b <= limit.b

data = []
with open('data.txt') as f:
  data = [line.strip() for line in f.readlines()]

limits = RoundInfo(12,13,14)

total_part1 = 0
total_part2 = 0

for i, line in enumerate(data):
  gs = GameStats(i+1, 0,0,0)
  for round in [round.split(' ') for round in line.split(': ')[-1].strip().split('; ')]:
    info = RoundInfo(0,0,0)
    for j in range(0, len(round), 2):
      n = int(round[j])
      c = round[j+1][0]
      if c == 'r':
        info.r += n
      elif c == 'g':
        info.g += n
      else:
        info.b += n
    gs.max_r = max(info.r, gs.max_r)
    gs.max_g = max(info.g, gs.max_g)
    gs.max_b = max(info.b, gs.max_b)
  if gs.under_limit(limits):
    total_part1 += gs.id
  total_part2 += gs.get_power()

print(f'sum of valid ids: {total_part1}')
print(f'sum of powers: {total_part2}')

