def get_data():
  patterns = []
  t_patterns = []
  with open('data.txt') as f:
    data = [line.strip().replace('.', ' ').replace('#', '•') for line in f.readlines()] + ['']
  pattern = []
  t_pattern = None
  for line in data:
    if len(line) == 0:
      patterns.append(pattern)
      t_patterns.append(t_pattern)
      pattern = []
      t_pattern = None
    else :
      if t_pattern is None:
        t_pattern = [c for c in line[::-1]]
      else:
        t_pattern = [tstr + c for tstr,c in zip(t_pattern,line[::-1])]
      pattern.append(line)
  return patterns,t_patterns
        
def p(d: list[str], v_id: int = 0, h_id: int = 0):
  hline = ''.join(['_' for _ in d[0]])
  if h_id != 0:
    print(hline)
  for i,line in enumerate(d):
    if v_id != 0:
      print(f'|{line[:v_id]}|{line[v_id:]}|')
    if h_id != 0:
      if i == h_id:
        print(hline)
      print(line)
  if h_id != 0:
    print(hline)

def is_mirror_split(s: int, pat: list[str], use_exact_match: bool) -> bool:
  total = 0
  for line in pat:
    total += sum([0 if a == b else 1 for a,b in zip(line[s-1::-1],line[s:])])
    if use_exact_match and total > 0:
      return False

  return use_exact_match or total == 1


def get_split_index(pattern: list[str], use_exact_match: bool) -> int:
  for i in range(1,len(pattern[0])):
    if is_mirror_split(i, pattern, use_exact_match):
      return i
  return 0

def get_value(use_exact_match) -> int:
  pat,tpat = get_data()

  p_sum = 0
  t_sum = 0
  for pid,pair in enumerate(zip(pat,tpat)):
    pattern,transposed_pattern = pair
    # print(f'\npid: {pid}')

    vi = get_split_index(pattern, use_exact_match)
    # if vi != 0:
    #   print(f'vsplit: {vi} // {p_sum} + {vi} -> {p_sum + vi}  //  {p_sum + t_sum} + {vi} -> {p_sum + t_sum + vi}')
    #   p(pattern, v_id=vi)
    p_sum += vi

    hi = get_split_index(transposed_pattern, use_exact_match=use_exact_match)
    val = hi*100
    # if hi != 0:
    #   print(f'hsplit: {hi} // {t_sum} + {val} -> {t_sum + val}  // {p_sum+t_sum} + {val} -> {p_sum + t_sum + val}')
    #   p(pattern, h_id=hi)
    t_sum += val
    print(f'pid: {pid} -> {vi + val}')
  
  print(p_sum + t_sum)

def part1():
  get_value(True)

def part2():
  get_value(False)

part2()