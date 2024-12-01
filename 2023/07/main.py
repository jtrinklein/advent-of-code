FIVE_X = 7
FOUR_X = 6
FULL_HOUSE = 5
THREE_X = 4
TWO_PAIR = 3
ONE_PAIR = 2
HIGH_CARD = 1

def get_value_jokers(hand: list[str]) -> int:
  if 'J' not in hand:
    return get_value(hand)

  hand_set = set(hand)
  hand_set.remove('J')
  unique_count = len(hand_set)
  joker_count = hand.count('J')
  if joker_count == 5:
    return FIVE_X
  
  if unique_count == 4: # [J , w, x, y ,z]
    return ONE_PAIR
  elif unique_count == 3:# [J , x, x, y ,z] | [J , x, y, y ,z]  | [J , x, y, z, z] | [J, J, x, y, z]
    return THREE_X
  elif unique_count == 1:# [J , x, x, x ,x]
    return FIVE_X
  elif unique_count == 2:# [J, x, y, y, y] | [J, J, x, y, y] | [J, J, J, x, y]
                         # [J, x, x, y, y] | [J, J, x, x, y]
                         # [J, x, x, x, y]
    best_group = max([hand.count(card) for card in hand_set]) + joker_count
    if best_group == 4:
      return FOUR_X
    return FULL_HOUSE
  return 0


def get_value(hand: list[str]) -> int:
  hand_set = set(hand)
  unique_count = len(hand_set)
  if unique_count == 5:
    return HIGH_CARD
  elif unique_count == 4:
    return ONE_PAIR
  elif unique_count == 1:
    return FIVE_X
  elif unique_count == 3:
    for card in hand_set:
      if hand.count(card) == 3:
        return THREE_X
    return TWO_PAIR
  elif unique_count == 2:
    for card in hand_set:
      if hand.count(card) == 4:
        return FOUR_X
    return FULL_HOUSE
  return 0


def get_data(use_jokers = False) -> tuple[list[str],int,int]:
  hands = []
  with open('data.txt') as f:
    for line in f.readlines():
      hand,bet = line.strip().split(' ')
      hand = list(hand)
      bet = int(bet)

      value = get_value_jokers(hand) if use_jokers else get_value(hand)
      hands.append([hand, bet, value])
  return hands


def should_swap(left_hand: tuple[list[str],int,int], right_hand: tuple[list[str],int,int], use_jokers: bool) -> bool:
  normal_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
  joker_ranks = [ 'J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
  if use_jokers:
    return should_swap_impl(left_hand, right_hand, joker_ranks)
  return should_swap_impl(left_hand, right_hand, normal_ranks)

def should_swap_impl(left_hand: tuple[list[str],int,int], right_hand: tuple[list[str],int,int], ranks: list[str]) -> bool:
  
  left_v = left_hand[-1]
  right_v = right_hand[-1]
  if left_v < right_v:
    return False
  if left_v > right_v:
    return True
  left_cards = left_hand[0]
  right_cards = right_hand[0]
  for l,r in zip(left_cards, right_cards):
    
    if ranks.index(l) < ranks.index(r):
      return False
    if ranks.index(l) > ranks.index(r):
      return True
  return False

def sort_hands(hands: list[tuple[list[str],int,int]], use_jokers = False) -> list[tuple[list[str],int,int]]:
  # sorted_hands = hands[:]
  
  i = 1
  while i < len(hands):
    if should_swap(hands[i-1], hands[i], use_jokers):
      hands[i],hands[i-1] = hands[i-1],hands[i]
      i = max(i-1, 1)
    else:
      i += 1
  return hands

def part1():
  hands = get_data()
  total = sum([hand[1]*(i+1) for i,hand in enumerate(sort_hands(hands))])
  print(f'total: {total}')

def part2():
  hands = get_data(use_jokers=True)
  total = sum([hand[1]*(i+1) for i,hand in enumerate(sort_hands(hands, use_jokers=True))])
  print(f'joker total: {total}')

part1()
part2()