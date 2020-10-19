#variables

#suits
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')

#ranks
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

#values
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':[1,11]}

import random
import time


#reshuffle counter
reshuffle = 6

class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
        
    def __str__(self): 
        return self.rank + ' of ' + self.suit  

class Deck:
    
    def __init__(self):
        #when initiated, a new deck is created using the Card class
        self.all_cards = [] 
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit,rank))
                
    def shuffle(self):
        #in place. Nothing is returned.
        random.shuffle(self.all_cards)
        
    def deal_one(self):
        # Remove the "top" card from the list of all_cards
        return self.all_cards.pop(0)

class Person: 
    '''
    Base class to create Player and Dealer class to reduce code repetition
    '''
    
    def __init__(self):
        self.hand = []
        self.handvalue = 0
        self.ace_in_hand = False
        self.bust = False 
        self.hand_1 = ''
        self.hand_spelt_out = ''
         
        
    def setbust(self): #This could be changed so it returns a boolean and eliminates the need for self.bust attribute
        if type(self.handvalue) == type(1):
            if self.handvalue > 21:
                self.bust = True
                           
        else:
            if self.handvalue[0] > 21 and self.handvalue[1] > 21:
                self.bust = True
                
    def has_blackjack(self):
        '''
        Return Boolean based on whether Person has Blackjack
        '''
        if self.ace_in_hand == True and len(self.hand) == 2: #it's only a BJ if it's 21 with 2 cards
            if self.handvalue[1] == 21: #with ace in hand
                return True
            else:
                return False
        else:                          #without ace in hand
            if len(self.hand) == 2:
                if self.handvalue == 21:
                    return True
                else:
                    return False
            
            else:
                return False
        
    def has_21(self):
        '''
        Returns boolean for whether person has 21 (but no BJ)
        '''
        if type(self.handvalue) == type(1): #without ace
                    
            if self.handvalue == 21 and len(self.hand) != 2:
                return True
            else:
                return False
                      
        else: # with ace
            if self.handvalue[0] == 21 and len(self.hand) != 2 or self.handvalue[1] == 21 and len(self.hand) != 2:
                return True
            else:
                return False
            
                    
    def add_cards(self,new_card): 
        '''
        Take a card object (from Deck) add it to person's hand and value of hand
        '''
        self.hand.append(new_card) 
        
        #if hand already has an ace and there is a second ace drawn set new ace's value to 1
        if self.ace_in_hand == True and type(new_card.value) == type([]):
            self.handvalue[0] += new_card.value[0]
            self.handvalue[1] += new_card.value[0]
        
        #if hand doesn't already have an ace and ace is drawn, split value to 'list' with two alternative values
        elif type(new_card.value) == type([]):
            self.ace_in_hand = True
            self.handvalue = [self.handvalue + new_card.value[0], self.handvalue + new_card.value[1]]
        #if hand doesn't already have an ace and card drawn is not an ace, just add it 
        else:
            if self.ace_in_hand == False:
                self.handvalue += new_card.value
            
            else:
                self.handvalue[0] += new_card.value
                self.handvalue[1] += new_card.value


class Dealer(Person):
    
    def __init__(self, name):
        Person.__init__(self)
        self.name = name
    
    
    def __str__(self):
        '''
        printing the player and the dealer will be the way the user is informed about the state of the game so this 
        method shows relevant details. Separaet for dealer and person since details differ.
        '''
        
        self.hand_1 = f"{self.name}'s hand:\n"
        self.hand_spelt_out = ''
        
        for card in self.hand:
            self.hand_spelt_out += "  " + str(card) + '\n' 
        
        try: #display value as int if no ace in hand, display two alternative values if there is ace in hand
            return self.hand_1 + self.hand_spelt_out + f'Hand value: {self.handvalue[0]} or {self.handvalue[1]}.\n'
        except:
            return self.hand_1 + self.hand_spelt_out + f'Hand value: {self.handvalue}.\n'
        
        
    def reset(self):
        '''
        Restes relevant values to default at the end of the round in prepration for the new round.
        '''
        self.hand = []
        self.handvalue = 0
        self.ace_in_hand = False
        self.bust = False
        self.hand_1 = ''
        self.hand_spelt_out = ''
        
    def is_draw(self):
        '''
        Returns boolean for whether Dealer needs to draw given current hand of cards
        '''
        
        if self.ace_in_hand == False: #without ace, draw if handvalue is 16 or lower.
            if self.handvalue < 17:
                return True
            else:
                return False
        
        else:
            if self.handvalue[0] < 18: #with ace, draw if soft handvalue is 17 or lower. No need to check for win or BJ due to order of statements
                return True
            else:
                return False

class Player(Person):
    
    def __init__(self,name):
        Person.__init__(self)
        self.name = name
        self.bet = 0
        self.bank = 300
        self.choice = 'null'
    
    
    def __str__(self):
        '''
        Printing the player and the dealer will be the way the user is informed about the state of the game so this 
        method shows relevant details. Separaet for dealer and person since details differ.
        '''
        
        self.hand_1 = f"{self.name}'s hand:\n"
        self.hand_spelt_out = ''
        
        for card in self.hand:
            self.hand_spelt_out += '  ' + str(card) + '\n' 
        
        try: 
            return self.hand_1 + self.hand_spelt_out + f'Hand value: {self.handvalue[0]} or {self.handvalue[1]}. Your bet: {self.bet}. Your bank: {self.bank}\n\n'
        except:
            return self.hand_1 + self.hand_spelt_out + f'Hand value: {self.handvalue}. Your bet: {self.bet}. Your bank: {self.bank}\n\n'
    
    
    def reset(self):
        '''
        Resets relevant attributes of player to default for the new round
        '''
        self.choice = 'null'
        self.hand = []
        self.handvalue = 0
        self.ace_in_hand = False
        self.bust = False
        self.hand_1 = ''
        self.hand_spelt_out = ''
        
                   
    def do_bet(self):
        '''
        Takes int for user input and saves it in the self.bet attribute for the given round
        '''
              
        while True:
            try:
                self.bet = int(input(f'How much will you bet this round? Your bank: {self.bank}'))
                if self.bank < self.bet:
                    print("You don't have this much in your bank. Try a smaller amount.")
                    self.bet = 0
                    continue
                
                elif self.bank > 9 and self.bet < 10:
                    print("You have to bet at least 10")
                    self.bet = 0
                    continue
                
                else:
                    print("Bet taken.")
                    self.bank -= self.bet
                    break
            except:
                print("This didn't work. Make sure to enter an integer.")
   

    def do_choice(self):
        '''
        Takes user input to learn what the user wants to do in their round and saves it in the self.choice attribute
        Displays and accepts 2 or 3 options depending on whether Double is available based on game state.
        '''
        #if handsize is 2, offer and accept S, H and D
        if len(player.hand) == 2:
            while self.choice not in ['S', 'H', 'D']:
                self.choice = input("What will it be: Stand ('S'), Hit ('H') or Double ('D')?").upper()
            
            if self.choice == 'D': #handle different player bank scenarios for Doubling down
                
                if self.bank == 0: #player has no money in bank to double the bet
                    print("You don't have any money left in your bank, so this is taken as a Hit")
                    time.sleep(4)
                    
                elif self.bank < self.bet: #player doesn't have enough money in bank to double the bet
                    
                    input(f"The bet you want to double is {self.bet}, but you only have {self.bank} in your bank. New bet: {self.bet + self.bank}. Submit anything to continue")
                    self.bet = self.bet + self.bank
                    self.bank = 0
                    
                else: #player has enough money to double the bet
                    self.bet += self.bet
                    self.bank -= self.bet
                
        #otherwise, offer and accept S and H
        else:
            while self.choice not in ['S','H']:
                self.choice = input("What will it be: Stand ('S') or Hit ('H')?").upper()
                if self.choice in ['D', 'd']:
                    print("You can't double because you have more than two cards already")
                    time.sleep(3)
            
                             
    def win(self):
        '''
        Checks whether player has blackjack and applies the two different win ratios based on that. Updates self.bank
        '''
        
        if self.has_blackjack() == True:
            self.bank += self.bet + self.bet*1.5
            print(f'Round won! {self.bet + self.bet*1.5} is added to your bank. Your bank: {self.bank}') 
            
        else: 
            self.bank += self.bet*2
            print(f'Round won! {self.bet*2} is added to your bank. Your bank: {self.bank}')
                  
    
    def win3_2(self):
        '''
        Updates the self.bet attribute for 3:2 win.      
        '''
        
        self.bank += self.bet + self.bet*1.5
        print(f'Round won! {self.bet + self.bet*1.5} is added to your bank. Your bank: {self.bank}') 
        
              
    def win1_1(self):
        '''
        Updates the self.bet attribute for 1:1 win.
        '''
        
        self.bank += self.bet*2
        print(f'Round won! {self.bet*2} is added to your bank. Your bank: {self.bank}')
        
              
    def push(self):
        '''
        Updates bank and messages user for the scenario where the two hands are equal.
        '''
        
        self.bank += self.bet
        print(f"It's a push! Your bet has been refunded. Your bank: {self.bank}")
                  
    
    def lose(self):
        '''
        Messages user about lose scenario. No need to do anything else since bet will be lost when reset() is called.
        '''
        
        print(f"Round lost! You lost your bet. Your bank: {self.bank}")
            
   
    def game_over_msg(self):
        '''
        end-of-game messaging depending on bank when exiting
        '''                
      
        print('\n'*100)
        if player.bank > 300:
            gain = player.bank-300
            print(f'Congratulations! You have increased your bank by {gain}!')

        elif player.bank == 300:
            print("Thank you for playing! Maybe next time you can increase your bank.")

        else:
            print("Thank you for playing! Better luck next time!")
    
    def zero_bank(self):
        '''
        Displays appropriate messaging before game logic ends the game
        '''
        input("You ran out of money! This is the end of your game. Submit anything to continue.")

def game_on_choice():
    '''
    Ask player if they want to continue playing and return boolean to set game_on variable
    '''
    choice = 'null'
    
    while choice not in ['Y', 'N']:
        choice = input('Would you like to keep playing? (Y/N)').upper()
        
        if choice not in ['Y', 'N']:
            print('Invalid input. Enter Y or N.')
        elif choice == 'Y':
            return True
        else:
            return False
        

def compare(obj_d,obj_p): #naming to show that it can be anything
    '''
    Compare the handvalue of Dealer and Player and return a string indicating which one has a higher value or if it's
    a draw.
    '''
    
    dealer_value = 0
    player_value = 0
    
    
    if obj_d.ace_in_hand == False: #if dealer has no ace the value to compare is simply the int handvalue
        dealer_value = obj_d.handvalue
        
    else: #if dealer has ace than value to compare is the higher as long as it's not a bust, in which case it's the lower
        if obj_d.handvalue[1] > 21:
            dealer_value = obj_d.handvalue[0]
        else:
            dealer_value = obj_d.handvalue[1]
    
    if obj_p.ace_in_hand == False: #same for the player
        player_value = obj_p.handvalue
        
    else:
        if obj_p.handvalue[1] > 21:
            player_value = obj_p.handvalue[0]
        else:
            player_value = obj_p.handvalue[1] 
    
    
    if dealer_value > player_value: #return which of the two is the winner or if they have the same value of hand
        return 'Dealer'
    
    elif dealer_value < player_value:
        return 'Player'
    
    else:
        return 'Equal'

    
def game_rules():
    print("RULES OF THE GAME: submit any characters to skip\n\nIn this text-based Blackjack game you start with", \
          "a bank of 300 and your aim is to win as much as possible.", \
          "\nThe game is played with a normal deck of cards. Each round you can decide how much to bet,", \
          "but minimum bet is 10, so if your bank goes below that, you lose.", \
          "\n\nBASICS: Cards are worth points. Its number is its value, and Jacks, Queens and Kings are worth 10 points.", \
          "Aces are worth 1 or 11 points, whichever is better for the player.", \
          "You start with two cards and you can see one card of the dealer. Based on this info you need to decide if you want to:", \
          "\n\n-HIT: draw another card", \
          "\n-STAND: stop and see whether you can beat the dealer with your current hand", \
          "\n-DOUBLE: available as an action only when you have two cards. You can double your bet, draw a card.", \
          "You can’t draw anymore in this round.", \
          "\n\nIf you have an Ace and another card worth 10 points, you have a Blackjack.", \
          "If you win with this combination you win more money (1.5 times your bet).", \
          "If you win in any other way, you win as much as you bet. If you lose, you lose your bet,", \
          "but you can continue playing with your remaining bank.", \
          "\n\nAt the end of each round, you can decide if you want to keep playing or stop.")


## game on
game_on = True

#set up game

#create deck
gamedeck = Deck()
#shuffle deck
gamedeck.shuffle()
#display rules
game_rules()
input("Press any key to continue")
print('\n'*100)

#create player / dealer
while True:
    
    player = Player(input("Who's playing?"))
    
    if player.name == '':
        continue
    else:
        break
        
dealer = Dealer("Dealer")
##### game logic

while game_on:
#GAME STARTS
    
    #ask player to bet
    player.do_bet()


    #deck needs to be reshuffled (recreated and shuffled) after 5 rounds with one player
    reshuffle -= 1
    
    if reshuffle == 0:
        time.sleep(2)
        gamedeck = Deck()
        gamedeck.shuffle()
        reshuffle = 5
        
        print("\nReshuffling deck...")   

    time.sleep(2)

    #deal 
    player.add_cards(gamedeck.deal_one())
    player.add_cards(gamedeck.deal_one())
    
    dealer.add_cards(gamedeck.deal_one())
    
    #display dealer and player hand and first card of dealer
    print('\n'*100)
    
    print(player)
    time.sleep(2)
    print(dealer) 
    time.sleep(2)
    #ask playerchoice
    while True: #PLAYER ROUND
        
        #Blackjack in hand! Go to dealer's turn!
        if player.has_blackjack() == True: 
            print("Blackjack! Let's see the dealer!")
            break
        
        #No Blackjack in hand: player gets to choose what to do
        else:
            player.do_choice()
            if player.choice == 'S':
                print("Okay, now let's see the dealer!") #continue to dealer outside of loop
                break

            elif player.choice == 'H':
                time.sleep(1)
                print("Drawing card...")
                time.sleep(1)
                
                player.add_cards(gamedeck.deal_one())
                player.choice = 'null'
                player.setbust()
                print('\n'*100)
                
                print(player)
                print(dealer)
                time.sleep(2)               
                               
                #check for bust: if true offer choice for playing again              
                if player.bust == True:
                    
                    print("That's a bust...") 
                    time.sleep(2)
                    
                    if player.bank < 10:
                        player.zero_bank()
                        time.sleep(2)
                        game_on = False
                        break
                        
                    else:
                        game_on = game_on_choice()
                        break
               
                #check for 21, if true go to dealers                                
                elif player.has_21() == True:
                    print("That's 21! Let's see the dealer!")
                    time.sleep(2)
                    break             
                       

            elif player.choice == 'D':
                
                print("Doubling bet...")
                print("Drawing card...")
                time.sleep(2)
                                
                player.add_cards(gamedeck.deal_one())
                
                player.choice = 'null'
                player.setbust()
                print('\n'*100)
                
                print(player)
                print(dealer)
                
                time.sleep(2) 
                
                if player.bust == True:
                    
                    print("That's a bust...") 
                    time.sleep(2)
                    
                    if player.bank < 10:
                        player.zero_bank()
                        time.sleep(2)
                        game_on = False
                        break
                        
                    else:
                        game_on = game_on_choice()
                        break
               
                #check for 21, if true go to dealers                                
                elif player.has_21() == True:
                    print("That's 21! Let's see the dealer!")
                    time.sleep(2)
                    break
                    
                break
            
            else: #later other options can come here: split
                pass
            
    #script arrives here after player's turn is over + or -
    if game_on == False: #player has quit, stop script
        
        print('\n'*100)
        player.game_over_msg()
        break
    
    else:
        if player.bust == True: #player is bust and wants to play more: reset attributes and break
            
            print('\n'*100)
            player.reset()
            dealer.reset()
            
            if player.bank < 10:
                print("Sadly, you ran of money!")
                player.game_over_msg()
                game_on == False
                break
            
            continue
        else:
            #DEALER TURN!
            #dealer draws second card
            
            
            print("Dealer draws their second card...")
            time.sleep(2)
            dealer.add_cards(gamedeck.deal_one())
            
            time.sleep(2)            
            print('\n'*100)
            
            print(player)
            print(dealer)
                        
            time.sleep(3)
            
            while True:
                
                #check for dealer bust (function)
                dealer.setbust()
                if dealer.bust == True:
                    #player has blackjack, player wins 3:2, else player wins 1:1
                    print("\nDealer is a bust...")
                    player.win()
                    game_on = game_on_choice()
                    break                  
                       
                #if dealer.has_blackjack()
                elif dealer.has_blackjack() == True:
                    #if player.has_blackjack()
                    if player.has_blackjack() == True:
                        #push, set game_on, break
                        player.push()
                        game_on = game_on_choice()
                        break
                        
                    #else player.lose(), set game_on, break
                    else:
                        player.lose()
                        if player.bank < 10:
                            player.zero_bank()
                            time.sleep(2)
                            game_on = False
                            break
                        
                        else:
                            game_on = game_on_choice()
                            break
                                                
                #if dealer.has21
                elif dealer.has_21() == True:
                    #if player.has_blackjack()
                    if player.has_blackjack() == True:
                        #player wins3_2
                        player.win3_2()
                        game_on = game_on_choice()
                        break
                        
                    #elif player.has21()
                    elif player.has_21() == True:
                        #player.push(), set game_on, break
                        player.push()
                        game_on = game_on_choice()
                        break
                        
                    #else
                    else:
                        #player.lose(), set game_on, break
                        player.lose()
                        time.sleep(1.5)
                        
                        if player.bank < 10:
                            player.zero_bank()
                            time.sleep(2)
                            game_on = False
                            break
                        
                        else:
                            game_on = game_on_choice()
                            break
                                              
                
                elif dealer.is_draw() == False: #This condition means that the two hands are ready to be compared: dealer is between draw limit and below 21 and player has stopped playing and is not bust
                    #if equal
                    if compare(dealer,player) == 'Equal': #lower case d and p! we input the instances not the parent objects!
                        #push, set game_on, break
                        player.push()
                        game_on = game_on_choice()
                        break
                        
                    #if dealer:
                    elif compare(dealer,player) == 'Dealer':
                        #player.lose(), set game_on, break
                        player.lose()
                        
                        if player.bank < 10:
                            player.zero_bank()
                            time.sleep(2)
                            game_on = False
                            break
                        
                        else:
                            game_on = game_on_choice()
                            break
                       
                        
                    #if player:
                    elif compare(dealer,player) == 'Player':
                        #player.win(), set game_on, break
                        player.win()
                        game_on = game_on_choice()
                        break 
                            
                #else:
                else:
                    #draw card, wait 3 secs
                    print("Dealer hits...")
                    dealer.add_cards(gamedeck.deal_one())
                    time.sleep(2)                   
                    
                    print('\n'*100)
                    print(player)
                    print(dealer)
                                        
                    time.sleep(3)
                                       
            
            if game_on == False:
                #end-of-game msg + quit
                player.game_over_msg()
                break
                
            else:
            
                #reset persons
                player.reset()
                dealer.reset()
                print('\n'*100)
                time.sleep(0.5)