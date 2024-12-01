DOWN_RIGHT = '┌'
DOWN_LEFT = '┐'
UP_RIGHT = '└'
UP_LEFT = '┘'
HORIZONTAL = '─'
VERTICAL = '│'
START = '①'
BORDER = '▪'
EMPTY  = ' '
CONTAINED = '∙'

def get_data() -> list[list[str]]:
  data = []
  with open('data.txt') as f:
    data = [
      list(line.strip()
      .replace('F',DOWN_RIGHT)
      .replace('7', DOWN_LEFT)
      .replace('L', UP_RIGHT)
      .replace('J', UP_LEFT)
      .replace('|', VERTICAL)
      .replace('-', HORIZONTAL)
      .replace('.', ' ')
      .replace('S', START))
      for line in f.readlines()]
  return data

def get_start(d: list[list[str]], w: int, h: int)->tuple[int,int]:
  for y in range(h):
    for x in range(w):
      if d[y][x] == START:
        return x,y
  return None

def p(d: list[list[str]]):
  for line in d:
    print(''.join(line))

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
dirs = [(0,-1), (1,0), (0,1), (-1,0)]
M= ['↑','→','↓','←']

def get_max_dist(sx: int, sy: int, moving: int, d: list[list[str]], border_map: list[list[str]]) -> tuple[int,int]:
  n = 0
  x = sx
  y = sy
  r = 0

  while True:
    n += 1
    dx,dy = dirs[moving]
    x += dx
    y += dy
    p = d[y][x]
    border_map[y][x] = BORDER
    # print(f'step: {n}, {M[moving]}, {p}')
    if p == START:
      return n//2, r
    if moving == LEFT:
      if p == DOWN_RIGHT:
        moving = DOWN
        r -= 1
      elif p == UP_RIGHT:
        moving = UP
        r += 1
    elif moving == RIGHT:
      if p ==  DOWN_LEFT:
        moving = DOWN
        r += 1
      elif p == UP_LEFT:
        moving = UP
        r -= 1
    elif moving == UP:
      if p == DOWN_LEFT:
        moving = LEFT
        r -= 1
      elif p == DOWN_RIGHT:
        moving = RIGHT
        r += 1
    else:
      if p == UP_RIGHT:
        moving = RIGHT
        r -= 1
      elif p == UP_LEFT:
        moving = LEFT
        r += 1

def flood(x:int, y: int, map: list[list[str]]) -> list[list[str]]:
  points = [(x,y)]
  while len(points) > 0:
    x,y = points.pop()
    map[y][x] = CONTAINED
    for dx,dy in dirs:
      if map[y+dy][x+dx] == EMPTY:
        points.append((x+dx,y+dy))
  return map
def fill_borders(fill_dir: int, sx: int, sy: int, moving: int, d: list[list[str]], border_map: list[list[str]]) -> list[list[int]]:
  
  x = sx
  y = sy
  n = 0
  while True:
    n += 1
    dx,dy = dirs[moving]
    fdx,fdy = dirs[(moving+fill_dir)%4]
    x += dx
    y += dy
    fx = x + fdx
    fy = y + fdy
    if border_map[fy][fx] == EMPTY:
      border_map = flood(fx,fy,border_map)
    p = d[y][x]
    if p == START:
      return border_map
    if moving == LEFT:
      if p == DOWN_RIGHT:
        moving = DOWN
      elif p == UP_RIGHT:
        moving = UP
    elif moving == RIGHT:
      if p ==  DOWN_LEFT:
        moving = DOWN
      elif p == UP_LEFT:
        moving = UP
    elif moving == UP:
      if p == DOWN_LEFT:
        moving = LEFT
      elif p == DOWN_RIGHT:
        moving = RIGHT
    else:
      if p == UP_RIGHT:
        moving = RIGHT
      elif p == UP_LEFT:
        moving = LEFT

def part1():
  d = get_data()
  borders = [[EMPTY for _ in line] for line in d]
  w = len(d[0])
  h = len(d)
  sx,sy = get_start(d, w, h)
  moving = RIGHT
  if d[sy][sx+1] == HORIZONTAL or d[sy][sx+1] == DOWN_LEFT or d[sy][sx+1] == UP_LEFT:
    moving = RIGHT
  elif d[sy][sx-1] == HORIZONTAL or d[sy][sx-1] == DOWN_RIGHT or d[sy][sx-1] == UP_RIGHT:
    moving = LEFT
  elif d[sy+1][sx] == VERTICAL or d[sy+1][sx] == UP_RIGHT or d[sy+1][sx] == UP_LEFT:
    moving = DOWN
  else:
    moving = UP
  
  print(f'moving: {moving}')
  dist,r = get_max_dist(sx,sy,moving,d, borders)
  p(borders)
  borders = fill_borders(r //abs(r), sx, sy, moving, d, borders)
  p(borders)
  included_spaces = sum([line.count(CONTAINED) for line in borders])
  
  print(f'dist: {dist}, included_spaces: {included_spaces}')

part1()