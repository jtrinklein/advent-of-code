points = 0
cards = []
with open('data.txt') as f:
  for i,line in enumerate(f.readlines()):
    wins,nums = line.strip().split(': ')[1].split('|')
    wins = [int(x) for x in wins.strip().split(' ') if x]
    nums = [int(num) for num in nums.strip().split(' ') if num]
    cards.append([wins,nums])

for wins,nums in cards:
  winners = len([n for n in nums if n in wins]) - 1
  p = pow(2, winners) if winners >= 0 else 0
  points += p

print(f'part1 points: {points}')
points = 0

card_ids = [i for i in range(len(cards))]
i = 0
while i < len(card_ids):
  card = card_ids[i]
  wins,nums = cards[card]
  winners = len([n for n in nums if n in wins])
  card_ids += range(card+1, card+1+winners)
  
  i += 1

card_count = len(card_ids)
print(f'part2 count: {card_count}')
