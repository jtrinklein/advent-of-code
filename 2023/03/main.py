data = []
with open('data.txt') as f:
  data = [list(line.strip()) for line in f.readlines()]

def get_number_bounds(x: int, y: int, w: int, d: list[list[str]]) -> list[int]:
  start= 0
  end = 0
  i = 0
  while (x-i) >= 0 and d[y][x-i].isdigit():
    i += 1
  start = x-i+1
  i = 0
  while (x+i) < w and d[y][x+i].isdigit():
    i += 1
  end = x + i
  return start,end

def get_gear_ratio(sx: int, sy: int, w: int, h: int, d: list[list[str]]) -> int:
  ratio = 1
  yl = max(sy-1, 0)
  yh = min(sy+1, h-1)
  y = yl
  n = 0
  while y <= yh:
    xl = max(sx-1, 0)
    xh = min(sx+1, w-1)
    x = xl
    while x <= xh:
      if d[y][x].isdigit():
        s,e = get_number_bounds(x,y,w,d)
        ratio *= int(''.join(d[y][s:e]))
        x = e
        n += 1
      x += 1
    y += 1

  return ratio if n == 2 else 0

def get_part_number(sx: int, sy: int, w: int, h: int, d: list[list[str]]) -> int:
  pn = 0
  yl = max(sy-1, 0)
  yh = min(sy+1, h-1)
  y = yl
  while y <= yh:
    xl = max(sx-1, 0)
    xh = min(sx+1, w-1)
    x = xl
    while x <= xh:
      if d[y][x].isdigit():
        s,e = get_number_bounds(x,y,w,d)
        pn += int(''.join(d[y][s:e]))
        x = e
      x += 1
    y += 1
  return pn

total = 0
gear_ratio_total = 0
h = len(data)
w = len(data[0])
for y,row in enumerate(data):
  for x,c in enumerate(row):
    if c != '.' and not c.isdigit():
      if c == '*':
        gear_ratio_total += get_gear_ratio(x,y,w,h,data)
      total += get_part_number(x,y,w,h,data)
print(f'part number total: {total}')
print(f'gear ratio total: {gear_ratio_total}')