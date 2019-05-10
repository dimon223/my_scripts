import random
from time import sleep

def card_setter():

    face_card = { 2:2, 3:3, 4:4, 5:5, 6:6, 7:7,8:8, 9:9, 10:10, 
    11:'J', 12:'Q', 13:'K', 14:'A', 'J':10, 'Q':10, 'K':10, 'A':11 }

    deck_list = [(suit, face_card[num]) for num in range(2,15) for suit in
        ('\u2660', '\u2665', '\u2666', '\u2663') ]
    
    random.shuffle(deck_list)

    poper = deck_list.pop(0)
    card = '''
 _____
|{i:^5}|
|     |
|{s:^5}|
|_____| '''.format(i=poper[1], s=poper[0])

    return card, face_card[poper[1]]

class Player():

    def __init__(self, name):
        self.name = name
        self.my_cards = []
        self.my_nums = []
        self.score = 0

    def take_card(self):
        card, num = card_setter()
        self.my_cards.append(card) 
        self.my_nums.append(num) 

    def think(self):
        if sum(self.my_nums) > 21 and 11 not in self.my_nums:
            print(f'{self.name} busted')
            self.score = sum(self.my_nums)
            return 'I am failed'
            
        elif sum(self.my_nums) > 21 and 11 in self.my_nums:
            num_of_aces = self.my_nums.count(11)
            if sum(self.my_nums) - 10 * num_of_aces > 21:
                print(f'{self.name} busted')
                self.score = sum(self.my_nums)                
                return 'I am failed'
            elif sum(self.my_nums) - 10 <= 21:
                self.score = sum(self.my_nums) - 10
            elif sum(self.my_nums) - 10 * num_of_aces <= 21:
                self.score = sum(self.my_nums) - 10 * num_of_aces

        elif sum(self.my_nums) <= 21:
            self.score = sum(self.my_nums)

    def show_hand(self):
        '''
        the below process to print multiple strings in a row was found in
        https://stackoverflow.com/questions/43372078/how-to-print-multiline-strings-on-the-same-line-in-python
        '''  

        strings_by_column = [s.split('\n') for s in self.my_cards]

        strings_by_line = zip(*strings_by_column)

        max_length_by_column = [
            max([len(s) for s in col_strings])
            for col_strings in strings_by_column]
        print(f'\n {self.name} cards')
        for parts in strings_by_line:
            padded_strings = [
                parts[i].ljust(max_length_by_column[i])
                for i in range(len(parts)) ]
            print( ''.join(padded_strings))

def main():

    dealer = Player('Dealer')
    dealer.take_card()
    dealer.show_hand()

    player = Player('Player')
    player.take_card()
    player.take_card()
    player.think()
    player.show_hand()

    while True:
        player_action = input('Would you like to stand or hit? (stand/hit) ')
        
        if player_action == 'hit':
            player.take_card()
            dealer.show_hand()
            player.show_hand()
            did_i_fail = player.think()
            if did_i_fail == 'I am failed':
                break
            
        elif player_action == 'stand':
            print('Player stands. Dealer is playing.')
            while dealer.score < player.score:
                print('Dealer takes a card')
                sleep(3)
                dealer.take_card()
                dealer.show_hand()
                player.show_hand()
                did_i_fail = dealer.think()
                if did_i_fail == 'I am failed':
                    break
                sleep(3)
            if dealer.score >21:
                break

            competitors = (player, dealer)
            if player.score == dealer.score:
                print(f'Player score: {player.score} Dealer score: {dealer.score} \nPush')
                break
            else:
                winner = max(competitors , key=lambda x: x.score)
                dealer.show_hand()
                player.show_hand()
                print(f'Player score: {player.score} Dealer score: {dealer.score} \n{winner.name} wins')
                break
        else:
            print('plese enter "hit" or "stand"')
main()


