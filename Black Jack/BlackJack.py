# BlackJack Game: one player vs computer dealer

import random

# list of suits, list of ranks, rank to value dict

suits = ['Heart', 'Diamond', 'Spade', 'Club']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

rank_to_value = {'J': 10, 'Q': 10, 'K': 10, 'A': 11}
for i in range(2, 11):
    rank_to_value[str(i)] = i

# print(rank_to_value)

# Define class 'Card'
# rank = {'2', '3', ..., '10', 'J', 'Q', 'K', 'A'}


class Card():
    '''
    instance = Card(suit, rank)
    suit in {'Heart', 'Diamond', 'Spade', 'Club'}
    rank in {'2', '3', ..., '10', 'J', 'Q', 'K', 'A'}
    '''

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = rank_to_value[rank]

    def __str__(self):
        return self.suit + ' ' + self.rank


#test_card = Card('Heart', '2')
# print(test_card)


class Desk():
    '''
    instance of Desk contains a list of 52 cards
    methods: 'shuffle', 'draw_one'
    '''

    def __init__(self):
        self.cards = []
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit, rank)
                self.cards.append(created_card)

    def __str__(self):
        return 'There are ' + str(len(self.cards)) + ' remaining cards.'

    # shuffle the list of all cards, return none
    def shuffle(self):
        return random.shuffle(self.cards)

    def draw_one(self):
        return (self.cards).pop(0)


'''test_desk = Desk()
print(test_desk.shuffle())
print(test_desk)
print(test_desk.draw_one())
print(test_desk)'''


class Player():
    """
    instance = Player('name', money)
    methods: 'bet', 'hit_or_stay', 'count'
    """

    def __init__(self, name='No name', money=0):
        self.name = name
        self.money = money  # amount of money left
        self.cards = []  # list of cards

    def __str__(self):
        return 'Player: '+self.name+'\n' + 'Money: '+str(self.money)


# print(Player('Huachen', 1000))


    def bet(self):
        '''
        Player.bet() asks for an input as the amount of bet
        '''
        # flag: whether player has placed a valid bet
        have_bet = False
        while not have_bet:
            try:
                # print the current balance
                print("{}'s current balance is {}".format(self.name, str(self.money)))
                # ask for an input as the amount of bet

                bit = int(input('Please place your bet:'))

                if bit > self.money:
                    print('Sorry, insufficient funds.')
                    continue
                else:
                    print(self.name + ' place a bit: ' + str(bit))
                    have_bet = True
                    break
            except:
                print('Sorry, invalid input.')

        return bit

    def hit_or_stay(self):
        '''ask play whether hit or stay:
            return True if hit
            return False if stay
        '''
        # flag: whether player has decided to hit or stay
        have_decided = False
        hit = False
        while not have_decided:
            try:
                # ask player to choose hit or stay
                player_choice = input('Would you like to hit (y or n):')
                if player_choice.lower()[0] == 'y':
                    print(self.name+' choose to hit.')
                    hit = True
                    have_decided = True
                    break
                elif player_choice.lower()[0] == 'n':
                    print(self.name+' choose to stay.')
                    hit = False
                    have_decided = True
                    break
                else:
                    print('Sorry, invalid input.')
                    break

            except:
                print('Sorry, invalid input.')
                continue
        return hit

    def count(self):
        # Add all card values, count A as 11
        count = 0
        for card in self.cards:
            count += card.value
        # if the count is less than 21, return it
        if count <= 21:
            return count
        # otherwise, see if there is any A's
        else:
            # number of A cards
            number_of_A = len([card for card in self.cards if card.rank == 'A'])
            if not number_of_A:
                return count
            else:
                while number_of_A and count > 21:
                    count -= 10  # count one of the A's as 1 instead of 11
                    number_of_A -= 1
                return count

    def play_again(self):
        # ask player if want to play play_again, return True or False
        valid_input = False
        while not valid_input:
            try:
                # print the current balance
                print(self.name + "'s current balance is " + str(self.money))
                # ask for an input as the amount of bet
                player_input = (input('Would you like to play again (y or n):'))
                if player_input.lower()[0] == 'y':
                    again = True
                    valid_input = True
                elif player_input.lower()[0] == 'n':
                    again = False
                    valid_input = True
                else:
                    print('Sorry, please enter y or n.')
                    continue

            except:
                print('Sorry, invalid input.')
                continue

        return again


# player = Player('Huachen', 100)
# print(player)
# player.bet()
# player.hit_or_stay()
# player.cards.extend([Card('Heart', 'A'), Card('Heart', '9'),
#                     Card('Heart', 'A'), Card('Heart', '9')])
# print(player.count())

print('Welcome to BlackJack!')

player_name = input('Please enter player name: ')
# Create Player(name, money)
player = Player(player_name, 100)
dealer = Player('Dealer', 10000)


game_on = True

while game_on:
    print('Game On!')
    # Create current desk and shuffle
    player.cards = []
    dealer.cards = []

    desk = Desk()
    desk.shuffle()

    bet = player.bet()

    for iter in range(2):
        player.cards.append(desk.draw_one())
        dealer.cards.append(desk.draw_one())

    print("Player's current cards: {} and {}".format(*player.cards))
    print("Dealer's faceup card: {} ".format(*dealer.cards))

    player_turn = True

    while player_turn:
        # ask player if want to hit, return True or False
        player_hit = player.hit_or_stay()

        # if player choose hit
        if player_hit:
            # player get one card
            player.cards.append(desk.draw_one())
            # count player's current hand
            player_current_hand = player.count()

            # if player bust
            if player_current_hand > 21:
                print("Player's current cards:")
                for card in player.cards:
                    print(card)
                print('Player bust, dealer wins.')
                player.money -= bet
                dealer.money += bet

                break
            # if player not bust
            else:
                print("Player's current cards:")
                for card in player.cards:
                    print(card)
                continue

        else:
            # player choose to stay, player's turn ends
            player_turn = player_hit
            print('Player stay.')

    # Dealer's turn
    dealer_turn = not player_turn

    player_current_hand = player.count()
    while dealer_turn:

        # if player busted, game ends
        if player_current_hand > 21:
            break

        # otherwise, dealer will draw_one until count larger than player
        else:
            print("Dealer's turn....")
            while dealer.count() <= player_current_hand:
                dealer.cards.append(desk.draw_one())

            # if dealer busted:
            if dealer.count() > 21:
                print('Dealer bust, {} wins!!'.format(player.name))
                player.money += bet
                dealer.money -= bet
                dealer_turn = False
                break
            # otherwsie, dealer wins
            else:
                print("Dealer's cards are:")
                for card in dealer.cards:
                    print(card)
                print('Dealer wins.')
                player.money -= bet
                dealer.money += bet
                dealer_turn = False
                break

    # ask player if want to play again: if y, game_on = True; if n, game_on = False
    if player.money > 0:
        game_on = player.play_again()
    else:
        game_on = False
        print('Game over. 赌博一时爽，欠债火葬场！')
