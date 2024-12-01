race_times = []
race_dists = []
race_time = 0
race_dist = 0
with open('data.txt') as f:

  time,dist = [x.strip() for x in f.readlines()]
  race_times = [int(t) for t in time.split(':')[-1].split(' ') if len(t) > 0]
  race_dists = [int(d) for d in dist.split(':')[-1].split(' ') if len(d) > 0]
  race_time = int(time.split(':')[-1].replace(' ', ''))
  race_dist = int(dist.split(':')[-1].replace(' ', ''))
result = 1
for time,dist in zip(race_times,race_dists):
  count = 0
  t = time;
  for t in range (time):
    if ((time - t)*t) > dist:
      count += 1
  print(f'rt: {time}, d: {dist}, count: {count}')
  result *= count
print(f'result: {result}')

part2_result = 0
for t in range(race_time):
  if ((race_time - t)*t) > race_dist:
    part2_result += 1
print(f'part2: {part2_result}')