'''
Author: Jeremy Sampl
This program is a computer version of the game Blackjack (AKA 21).
- The aim of the game is to approach 21 as much as possible without going over.
- J, Q, K are worth 10, Aces are worth 1 or 11 and the rest of face value.
- The player starts by choosing a starting amount to 'bring to the table'.
- At the start of every round, the player may choose their betting amount.
- Bets are doubled if won, returned if tied, and taken away if lost.
- Both the dealer and the player start off with two cards.
- The dealer receives the second card face down, but must be checked if the
dealer's first card is an ace to see if the second card's value is 10, making 21.
- The player is then able to hit, obtaining another card, in order to attempt to
approach 21 as much as possible until the player holds or surpasses 21.
- If the player surpasses 21 when hitting, they automatically lose.
- After the player holds, the dealer then picks up cards until reaching 17.
- If the dealer goes over in the process, the player automatically wins.
- Otherwise, the dealer and player's scores are compared, determining the winner.
'''

# Imports
from array import *
from random import *
from time import *

# Declaring/initializing variables
cards =[["A .  ", "2    ", "3    ", "4    ", "5    ", "6    ", "7    ", "8    ", "9    ", "10  ^", "J  ww", "Q  ww", "K  WW"],
	[" /.\\ ","  ^  ", "  ^  ", " ^ ^ ", " ^ ^ ", " ^ ^ ", " ^ ^ ", "^ ^ ^", "^ ^ ^", "^ ^ ^", " ^ {)", " ^ {(", " ^ {)"],
	["(_._)", "     ", "  ^  ", "     ", "  ^  ", " ^ ^ ", "^ ^ ^", " ^ ^ ", "^ ^ ^", "^ ^ ^", "(/)% ", "(.)%%", "(.)%%"],
	["  |  ", "  ^  ", "  ^  ", " ^ ^ ", " ^ ^ ", " ^ ^ ", " ^ ^ ", "^ ^ ^", "^ ^ ^", "^ ^ ^", " | % ", " |%%%", " |%%%"],
	["____V", "____Z", "____E", "____h", "____S", "____9", "____L", "____8", "____6", "___0I", "__%%[", "_%%%O", "_%%%>"]
]
dealerCards = []
playerCards = []
dealerSum = 0
playerSum = 0
playing = True
holding = False
dealerCount = False
submittingMoney = True
betting = True
money = int()
bet = int()
################################################################################
# Main function which controls the entire program
def main():
    # Welcomes the user and prompts them to submit a starting amount
    print("Welcome to Black Jack!")
    startingAmount()

    # Loop which encompasses all functions needed for every round
    while playing:
        submitBet()
        randomCards()
        displayCards()
        checkAce()
        # Makes sure the game was not reset (because of a winner)
        if len(dealerCards) != 0:
           hitOrHold()
################################################################################
'''
Function that asks the user the input the starting amount of money.
- Ensures the amount of money is realistic.
'''
def startingAmount():
    # Declare global variables
    global submittingMoney
    global money

    # Loops until the user submits a valid amount
    while submittingMoney:
        # Prompts the user to input an integer starting amount of money
        print("\nHow much money (whole $) are you bringing to the table?")
        money = int(input())

        # Checks if the amount is realistic to avoid errors
        if money <= 0 or money > 9999999999:
            print("Please submit a realistic amount!")
        else:
            print("You have brought ${0} to the table.".format(money))
            submittingMoney = False
################################################################################
'''
Function that controls the betting at the start of every round.
- Asks the user to input a bet.
- Checks if the bet is valid.
- Continues until the user inputs a proper bet.
'''
def submitBet():
    # Declare global variables
    global betting
    global bet
    global money

    # Loops until user places a valid bet
    while betting:
        # Prompts the user to input a bet
        print("\nYour current balance is ${0}.\nHow much would you like to bet?".format(money))
        bet = int(input())

        # Checks whether the bet is valid or not
        if bet > money:
            print("You do not have enough money to bet this amount!")
        elif bet <= 0:
            print("You must place a bet.")
        else:
            print("You have bet ${0}.".format(bet))
            money -= bet
            betting = False
################################################################################
'''
Function that controls the initial randomization of cards.
Also counts the initial sums of the cards visible to the player.
'''
def randomCards():
    # Declare global variables
    global dealerSum
    global playerSum

    # Generates two random cards for both the dealer and player
    for i in range(2):
        randomPlayerCard()
        randomDealerCard()
    
    # Checks to determine the value of the dealer's card visible to the player
    if dealerCards[0] == 1:
        dealerSum = 11
    elif dealerCards[0] > 10:
        dealerSum = 10
    else:
        dealerSum = dealerCards[0]

    # Adds up the player's two initial cards to show the user their current sum
    for i in playerCards:
        if i > 10:
            playerSum += 10
        elif i == 1 and playerSum < 11:
            playerSum += 11
        else:
            playerSum += i

# Function that randomizes a card and adds them to the deck of the player
def randomPlayerCard():
    playerCards.append(randrange(1, 14))

# Function that randomizes a card and adds them to the deck of the dealer
def randomDealerCard():
    dealerCards.append(randrange(1, 14))
################################################################################
'''
Function used to display the cards of both the dealer and player to the user.
- Prints a seperator to make it visually appealing.
- Prints the dealer's cards and then the player's cards.
- Starts by using the number of cards to print out the tops.
- Using the array, it then prints out the face of the cards and their sides.
- It also checks if the second card of the dealer should be hidden.
'''
def displayCards():
    # Seperator used to make it easier to read
    print("\n==========================================\n")

    # Runs twice (once for each the dealer/player)
    for i in range(2):
        # Declare temporary variables
        cardCount = int()
        card = int()

        # Determines which cards are being printed and saves the amount of cards
        if i == 0:
            print("The dealer's cards are:")
            cardCount = len(dealerCards)
        else:
            print("Your cards are:")
            cardCount = len(playerCards)

        # Prints the tops of every card
        for j in range(cardCount):
            print("  _____ ", end = "")

        # Prints row by row
        for j in range(len(cards)):
            # Starts printing out the next line
            print()
            for k in range(cardCount):
                # Determines whether the card being printed is the dealer's
                # flipped second card (not to be shown to user) or not
                if cardCount == 2 and i == 0 and k == 1 and holding == False:
                    if j < len(cards) - 1:
                        print(" |  ?  |", end = "")
                    else:
                        print(" |_____|", end = "")
                else:
                    # Determines whether the cards being printed belong to the
                    # dealer or player in order to print
                    if i == 0:
                        card = dealerCards[k]
                    else:
                        card = playerCards[k]
                    print(" |{0}|".format(cards[j][card - 1]), end = "")
        # Spacer
        print("\n")

    # Display the scores of both the dealer and player
    print("Dealer: {0} | Player: {1}".format(dealerSum, playerSum))

################################################################################
'''
Function that checks if the dealer's first card is an ace and if the second
card contains a value of 10, making 21.
Also checks if the player's cards sum up to 21, making the player win.
'''
def checkAce():
    # Declare global variables
    global holding
    global dealerSum

    # Checks if the dealer's first card is an ace and also checks if the second
    # card contains a value of 10
    if dealerCards[0] == 1 and containsCard(dealerCards, 10):
        # Displays the two-card 21 made by the dealer
        holding = True
        dealerSum = 21
        displayCards()

        # Checks if player also has 21, which would cause a tie
        if containsCard(playerCards, 1) and containsCard(playerCards, 10):
            gameEnd(0)
        else:
            gameEnd(1)
    # Otherwise, checks if player has a two-card 21
    elif containsCard(playerCards, 1) and containsCard(playerCards, 10):
        gameEnd(2)
################################################################################
'''
Function used to count the sum of the cards for either the dealer or player.
- Adds 10 for face cards, keeps track of aces and adds face value for all other cards.
- After counting all other cards, takes any aces and assumes them as 11, unless they
bring the score higher than 21.
''' 
def sumCount():
    # Declare global/temporary variables
    global dealerSum
    global playerSum
    aceCount = 0
    cardSum = 0
    
    # Determines whether the hand being counter is the dealer or player's
    # Assumes face cards as 10 and adds up all other cards as their face value
    # Aces are counted instead of immediately counted in the sum
    if dealerCount:
        for i in dealerCards:
            if i > 10:
                cardSum += 10
            elif i == 1:
                aceCount += 1
            else:
                cardSum += i
    else:
        for i in playerCards:
            if i > 10:
                cardSum += 10
            elif i == 1:
                aceCount += 1
            else:
                cardSum += i

    # If there is an ace, knowing there can only be one ace that can be 11 in
    # Blackjack, it checks if setting that ace to 11 as well as adding the rest
    # of the aces will surpass 21 or not
    # Derives from: cardSum + 11 + (1 * (aceCount - 1)) <= 21
    if aceCount > 0 and cardSum + aceCount <= 11:
        cardSum += 11
        cardSum += aceCount - 1
    else:
        cardSum += aceCount

    # Sets the new sum depending on which cards were counted
    if dealerCount:
        dealerSum = cardSum
    else:
        playerSum = cardSum
################################################################################
'''
Function used to determine whether the player could/would like to hit or hold.
- Ends the game if the player has surpassed 21.
- If player has not surpassed 21, gets the player to input their choice.
- If player hits, calls the functions to determine and display a random card.
- If not, calls the hold function.
'''
def hitOrHold():
    # Declare global variables
    global holding

    # Gets the sum of the cards in order to check if player has surpassed 21
    sumCount()

    # Loops until the player holds or surpasses 21
    while holding == False:
        if playerSum <= 21:
            # Prompts and determines whether the user would like to hit or hold
            print("\nWould you like to hit ('1') or hold ('2')?")
            choice = int(input())
            if choice == 1:
                # Gives the player a random card and displays their cards/score
                randomPlayerCard()
                sumCount()
                displayCards()
            else:
                # Leaves the hitting loop and calls the holding function
                holding = True;
                hold()
                break
        else:
            # Player instantly loses as they have surpassed 21
            gameEnd(1)
            break
################################################################################
'''
Function that controls the dealer's card pick-ups after the player has held.
- Shows the dealers face down card.
- Then it keeps giving a random card to the dealer, adding the sum, and
displaying the cards until the dealer reaches 17.
- Finally it determines the winner from the scores of the dealer and player.
'''
def hold():
    # Declare global variables
    global dealerCount

    # Shows dealer's second card
    dealerCount = True
    sumCount()
    displayCards()

    # Dealer keeps taking cards until a score of 17 is reached
    while(dealerSum < 17):
        sleep(1)
        randomDealerCard()
        sumCount()
        displayCards()

    # Determines a winner
    if playerSum > 21 or (dealerSum > playerSum and dealerSum <= 21):
        gameEnd(1)
    elif dealerSum > 21 or playerSum > dealerSum:
        gameEnd(2)
    else:
        gameEnd(0)
################################################################################
'''
Function that checks if a hand contains a certain value.
This is done by:
- Checking whether the value being searched for is 10 or other.
- For a value of 10, loops through checking for any value greater/equal to 10.
- For any other value, checks if the specific card is in a specific hand.
- Returns a boolean variable to confirm its findings.
'''
def containsCard(array, value):
    # Declare temporary boolean variable
    containsValue = False
    
    if value == 10:
        # Checks if the hand contains a 10 or higher (face card)
        for i in array:
            if i >= value:
                containsValue = True
                break
    else:
        # Checks if the hand contains a specific card
        if value in array:
            containsValue = True

    # Returns boolean variable showing whether the hand contains the card or not
    return containsValue
################################################################################
'''
Function that declares the winner and resets the game if the player decides to
play again.
'''
def gameEnd(winner):
    # Declare global variables
    global money
    global playing
    global betting
    global holding
    global dealerSum
    global playerSum
    global dealerCount

    # Notifies the player of the result of the game
    # Returns earnings from their bet if applicable
    sleep(.5)
    if winner == 0:
        print("\nIt's a draw! Your ${0} bet was returned.".format(bet))
        money += bet
    elif winner == 1:
        print("\nYou lose! Your ${0} bet was taken away.".format(bet))
    else:
        print("\nYou win! You doubled your ${0} bet.".format(bet))
        money += 2 * bet

    # Checks if the player has any money left to bet, kicks them out otherwise
    if money > 0:
        # Notifies the user of their balance and prompts them to decide if they
        # would like to play again or not
        print("Your new balance is ${0}.\n".format(money))
        print("Would you like to play again? (Yes: '1' | No: '2')")
        choice = input()
        if choice == "2":
            # Acknoledges the user's parting and reminds them of their balance
            print("Have a great day! Remember to spend your ${0} wisely.".format(money))
            playing = False
        else:
            # Resets game
            dealerCards.clear()
            playerCards.clear()
            betting = True
            holding = False
            dealerCount = False
            dealerSum = 0
            playerSum = 0
    else:
        # Notifies user that they do not have sufficient funds and ends program
        print("You have run out of money!\nPlease come again with more money!")
        playing = False
################################################################################
# Starts the program
main()
