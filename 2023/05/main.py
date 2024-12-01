from dataclasses import dataclass
from math import inf

@dataclass
class Mapper:
  d_starts: list[int]
  s_starts: list[int]
  s_ends: list[int]
  count: int

  def add_map(self, d_start, s_start, s_end):
    self.d_starts.append(d_start)
    self.s_starts.append(s_start)
    self.s_ends.append(s_end)
    self.count += 1

  def map(self, value: int) -> int:
    for i in range(self.count):
      if self.s_starts[i] <= value < self.s_ends[i]:
        return self.d_starts[i] + (value - self.s_starts[i])
    return value

seed_to_soil: Mapper = Mapper([], [], [], 0)
soil_to_fert: Mapper = Mapper([], [], [], 0)
fert_to_water: Mapper = Mapper([], [], [], 0)
water_to_light: Mapper = Mapper([], [], [], 0)
light_to_temp: Mapper = Mapper([], [], [], 0)
temp_to_hum: Mapper = Mapper([], [], [], 0)
hum_to_loc: Mapper = Mapper([], [], [], 0)


# soiled_seeds = {}
# ferted_soils = {}
# watered_ferts = {}
# lit_waters= {}
# temps_lit = {}
# hums_temped = {}
# locs_humed = {}

seeds = []
seed_pairs = []

with open('data.txt') as f:
  mappers = [seed_to_soil,soil_to_fert, fert_to_water, water_to_light, light_to_temp, temp_to_hum, hum_to_loc]
  # maps = [soiled_seeds,ferted_soils, watered_ferts, lit_waters, temps_lit, hums_temped, locs_humed]
  
  lines =  [x.strip() for x in f.readlines()]
  seed_line = lines.pop(0)

  i = 0
  for line in lines[2:]:
    # print(f'section: {i}')
    if len(line) == 0:
      i += 1
      continue
    if ':' in line:
      continue

    d,s,count = [int(x) for x in line.split(' ')]
    # sections[i].append([int(x) for x in line.split(' ')])
    mappers[i].add_map(d, s, s + count)
    # for j in range(section[-1]):
    #   maps[i][section[1] + j] = section[0] + j
    
  seeds = [int(s) for s in seed_line.split(' ')[1:]]
  for i in range(0, len(seeds), 2):
    seed_pairs.append([seeds[i], seeds[i+1]])

def soil(seed: int) -> int:
  return seed_to_soil.map(seed)
  # return soiled_seeds.get(seed, seed)

def fert(soil: int) -> int:
  return soil_to_fert.map(soil)
  # return ferted_soils.get(soil, soil)

def water(fert: int) -> int:
  return fert_to_water.map(fert)
  # return watered_ferts.get(fert, fert)

def light(water: int) -> int:
  return water_to_light.map(water)
  # return lit_waters.get(water, water)

def temp(light: int) -> int:
  return light_to_temp.map(light)
  # return temps_lit.get(light, light)

def hum(tmp: int) -> int:
  return temp_to_hum.map(tmp)
  # return hums_temped.get(t, t)

def loc(hum: int) -> int:
  return hum_to_loc.map(hum)
  # return locs_humed.get(hum, hum)

def part1() -> int:
  lowest = inf
  for seed in seeds:
    l = loc(hum(temp(light(water(fert(soil(seed)))))))
    lowest = min(lowest, l)
    # print(lowest)
  return lowest
def part2() -> int:
  lowest = inf
  i = 0
  for s,n in seed_pairs:
    print(f'pair: {i+1}')
    for seed in range(s, s+n):
      l = loc(hum(temp(light(water(fert(soil(seed)))))))
      lowest = min(lowest, l)
  return lowest

lowest = part1()
# lowest = part2()
print(f'lowest loc: {lowest}')

