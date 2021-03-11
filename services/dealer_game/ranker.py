from .card_h import *
from .community_cards_h import *
from .player_h import *

ROYAL_FLUSH = 91413121110
STRAIGHT_FLUSH = 90000000000
FOUR_OF_A_KIND = 80000000000
FULL_HOUSE = 70000000000 
FLUSH = 60000000000 
STRAIGHT = 50000000000
THREE_OF_A_KIND = 40000000000 
TWO_PAIR = 30000000000 
PAIR = 20000000000 
HIGH_CARD = 10000000000 

def combine_cards(player, community_cards):
    player_hand = player.get_hand()
    return player_hand + community_cards.cards

def get_aces(cards):
    aces = []
    for c in cards:
        if c.get_value_as_int() == 14:
            aces.append(c)
    return aces

def score_cards(cards):
    score = 0
    for i, c in enumerate(cards, start=0):
        score += c.get_value_as_int() * (10 ** (8 - 2 *i))
    return score

def dedup(cards):
    #print("deduping", cards)
    duplicates = []
    deduped = []
    last_card = Card('0', Suit.spades) # empty card
    for i, c in enumerate(cards, start=0):
        if c.get_value_as_int() != last_card.get_value_as_int():
            deduped.append(c)
        last_card = c
    #print("deduped?", deduped)
    return deduped

def get_best_excluding(cards, to_exclude):
    best_excluding = []
    for c in cards:
        if c not in to_exclude:
            best_excluding.append(c)
    return best_excluding
    

def find_reps_or_high_card(cards):
    cards.sort(reverse=True)
    pairs = []
    no_reps = []
    card_buffer = []
    three_of_a_kind = []
    four_of_a_kind = []
    repetitions = 0
    #print("reps:", cards)
    assert(len(cards) == 7)

    for i, c in enumerate(cards, start=0):
        if i + 1 >= len(cards):
            next_card = Card('0', Suit.spades)
        else:
            next_card = cards[i + 1]
        if next_card == c:
            if repetitions == 0:
                repetitions = 2
                card_buffer.append(c)
                card_buffer.append(next_card)
            else:
                repetitions += 1
                card_buffer.append(next_card)
        elif repetitions == 2:
            #print("appending pair", card_buffer)
            pairs.append(card_buffer)
            card_buffer = []
            repetitions = 0
        elif repetitions == 3:
            if len(three_of_a_kind) > 0:
            #    print("appending pair", card_buffer)
                pairs.append(card_buffer[:2])
            else:
            #    print("appending 3 of a kind", card_buffer)
                three_of_a_kind.append(card_buffer)
            card_buffer = []
            repetitions = 0
        elif repetitions == 4:
            four_of_a_kind.append(card_buffer)
            card_buffer = []
            repetitions = 0
        elif repetitions == 0:
            no_reps.append(c)
        else:
            print(cards, "ERROR!")
            assert(False)

    if len(four_of_a_kind) > 0:
        kicker = get_best_excluding(cards, four_of_a_kind[0])
        hand = four_of_a_kind[0] + kicker[:1]
        score = FOUR_OF_A_KIND + score_cards(hand)
    elif len(three_of_a_kind) > 0 and len(pairs) > 0:
        hand = three_of_a_kind[0] + pairs[0]
        score = FULL_HOUSE + score_cards(hand)
    elif len(three_of_a_kind) > 0:
        hand = three_of_a_kind[0] + no_reps[:2]
        score = THREE_OF_A_KIND + score_cards(hand)
    elif len(pairs) >= 2:
        kicker = get_best_excluding(cards, pairs[0] + pairs[1])
        hand = pairs[0] + pairs[1] + kicker[:1]
        score = TWO_PAIR + score_cards(hand)
    elif len(pairs) > 0:
        hand = pairs[0] + no_reps[:3]
        score = PAIR + score_cards(hand)
    else:
        hand = no_reps[:5]
        score = HIGH_CARD + score_cards(hand)
    return score, hand

def find_straights(cards):
    #print("find_straights", cards)
    cards.sort(reverse=True)
    #print("find_straights sorted:", cards)
    dedupped = dedup(cards)
    #print("deduped:", dedupped)
    straights = []
    straight = []
    for i, c in enumerate(dedupped, start=0):
        #print("finding straights:", c)
        if i + 1 >= len(dedupped):
            break
        c_val = c.get_value_as_int()    
        next_c = dedupped[i + 1]
        next_val = next_c.get_value_as_int()
        if c_val == next_val + 1:
            if len(straight) == 0:
                #print("making straight with", next_val, c_val)
                straight.append(c)
                straight.append(next_c)
            else:
                #print("making straight with", next_val)
                straight.append(next_c)
        elif next_val == 2 and len(straight) == 4:
            aces = get_aces(dedupped)
            for a in aces:
                straights.append(straight + [ a ] )
            break # no other possible straights below 2, A, etc.
        else: 
            straight = []
        if len(straight) >= 5:
            straights.append(straight[-5:])        
    return straights

def find_all_flushes(cards):
    #print("find best flush")
    cards.sort(reverse=True, key=lambda c: (c.suit.value, c))
    #print("find best flush", cards)
    flushes = []
    for i, c in enumerate(cards, start=0):
        #print("looking at:", c)
        if len(cards) <= i + 1:
            break
        next_card = cards[i + 1]
        if c.suit == next_card.suit:
            if len(flushes) == 0:
                flushes.append(c)
                flushes.append(next_card)
            else:
                flushes.append(next_card)
        elif len(flushes) >= 5: 
            break
        else:
            flushes = []

    if len(flushes) < 5:
        flushes = []

    return flushes
    
def find_straight_flush(flushes):
    flushes.sort(reverse=True)
    #print("find_straights sorted:", cards)
    dedupped = dedup(flushes)
    #print("deduped:", dedupped)
    straight = []
    if len(dedupped) < 5:
        return straight
    for i, c in enumerate(dedupped, start=0):
        #print("finding straights:", c)
        if i + 1 >= len(dedupped):
            break
        c_val = c.get_value_as_int()    
        next_c = dedupped[i + 1]
        next_val = next_c.get_value_as_int()
        if c_val == next_val + 1:
            if len(straight) == 0:
                #print("making straight with", next_val, c_val)
                straight.append(c)
                straight.append(next_c)
            else:
                #print("making straight with", next_val)
                straight.append(next_c)
        elif next_val == 2 and len(straight) == 4:
            aces = get_aces(dedupped)
            for a in aces:
                return straight + [ a ]
        else: 
            straight = []
        if len(straight) >= 5:
            return straight
    return []

def unbracket(cards):
    return str(str(cards)[1:-1])
    
def get_hand_score(player, community_cards):
    combined_cards = combine_cards(player, community_cards)
    assert(len(combined_cards) == 7)
    flushes = find_all_flushes(combined_cards)
    straight_flush = find_straight_flush(flushes)
    if len(straight_flush) > 0:
        showdown_hand = "Player " + str(player.id) 
        showdown_hand += " with a straight flush: "
        showdown_hand += unbracket(straight_flush)
        player.showdown_hand = showdown_hand
        return STRAIGHT_FLUSH + score_cards(straight_flush)
    score_reps, rep_hand = find_reps_or_high_card(combined_cards)
    if score_reps >= FOUR_OF_A_KIND:
        showdown_hand = "Player " + str(player.id) + " with four of a kind: "
        showdown_hand += unbracket(rep_hand)
        player.showdown_hand = showdown_hand
        return score_reps
    if score_reps >= FULL_HOUSE:
        showdown_hand = "Player " + str(player.id) + " with a full house: "
        showdown_hand += unbracket(rep_hand)
        player.showdown_hand = showdown_hand
        return score_reps
    best_flush = flushes[:5]
    if len(best_flush) == 5:
        showdown_hand = "Player " + str(player.id) + " with a flush: "
        showdown_hand += unbracket(best_flush)
        player.showdown_hand = showdown_hand
        return FLUSH + score_cards(best_flush)
    straights = find_straights(combined_cards)
    if len(straights) > 0:
        showdown_hand = "Player " + str(player.id) + " with a straight: "
        straights[0].sort(reverse=True)
        showdown_hand += unbracket(straights[0])
        player.showdown_hand = showdown_hand
        return STRAIGHT + score_cards(straights[0])
    if score_reps >= THREE_OF_A_KIND:
        showdown_hand = "Player " + str(player.id) + " with three of a kind: "
        showdown_hand += unbracket(rep_hand)
        player.showdown_hand = showdown_hand
        return score_reps
    if score_reps >= TWO_PAIR:
        showdown_hand = "Player " + str(player.id) + " with two pairs: "
        showdown_hand += unbracket(rep_hand)
        player.showdown_hand = showdown_hand
        return score_reps
    if score_reps >= PAIR:
        showdown_hand = "Player " + str(player.id) + " with a pair: "
        showdown_hand += unbracket(rep_hand)
        player.showdown_hand = showdown_hand
        return score_reps
    else: #high card
        showdown_hand = "Player " + str(player.id) + " with high card: "
        showdown_hand += unbracket(rep_hand)
        player.showdown_hand = showdown_hand
        return score_reps

def get_hand_name(hand_score):
    if hand_score == ROYAL_FLUSH:
        return "royal flush"
    if hand_score > STRAIGHT_FLUSH:
        return "straight flush"
    if hand_score > FOUR_OF_A_KIND:
        return "four of a kind"
    if hand_score > FULL_HOUSE:
        return "full house"
    if hand_score > FLUSH:
        return "flush"
    if hand_score > STRAIGHT:
        return "straight"
    if hand_score > THREE_OF_A_KIND:
        return "three of a kind"
    if hand_score > TWO_PAIR:
        return "two pair"
    if hand_score > PAIR:
        return "pair"
    if hand_score > HIGH_CARD:
        return "high card"
    return "ERROR"

def find_winners(players, community_cards):
    cc = community_cards
    scored_players =  [ [p, get_hand_score(p, cc)] for p in players]
    scored_players.sort(reverse=True, key=lambda c: c[1])
    highest_score = scored_players[0][1]
    winners = []
    for player, score in scored_players:
        if score < highest_score:
            break
        winners.append( [player, score] )
    return winners
