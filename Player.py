from enum import Enum

class Suit(Enum):
	Club = 1
	Spade = 2
	Heart = 3
	Diamond = 4

class Power(Enum):
	Two = 2
	Three = 3
	Four = 4
	Five = 5
	Six = 6
	Seven = 7
	Eight = 8
	Nine = 9
	Ten = 10
	Jack = 11
	Queen = 12
	King = 13
	Ace = 14

class Card:
	
	def __init__(self, suit, power) :
		self.power = power
		self.suit = suit

	def __eq__(self, other) :
		return self.power == other.power and self.suit == other.suit

	def __ne__(self, other) :
		return not self == other

	def __str__(self) :
		power = str(self.power.value) if self.power.value <= 10 else self.power.name
		return power + " of " + self.suit.name + "s"

class Player :

	## Called at the begining of a game - Each player is passed information about the game
	##     player_id - string = a unique string used to identify the player
	##     starting_money - int = the amount of money each player will start the game with
	##     rounds - int = the number of rounds that will be played before the game ends and a winner is decided
	##                    the game may be cut short if all but one player goes bankrupt
	##     small_blind - int = the amount of money that the small blind will bet
	##     big_blind - int = the amount of money that the big blind will bet
	def __init__(self, player_id, starting_money, rounds, small_blind, big_blind) :
		raise NotImplementedError()

	## Called at the begining of each round - Each player is passed information about the other players states going into
	## the round as well as their hand and betting order
	##     player_states - [(player_id, betting_order, money), ... ] = an array of tuples containing player information for each player
	##         player_id - string
	##         betting_order - int = a number representing the players position at the table and order they will bet in
	##             0  = dealer
	##             1  = big blind
	##             2  = small blind
	##             3+ = normal player
	##         money - int = a number representing the amount of money the player has 
	##     hand - (Card, Card) = A tuple of card objects representing the 
	def StartRound(self, player_states, hand) :
		raise NotImplementedError()
	
	## Called each time a player has an opportunity to make a decision - small and big blinds are placed automatically without calling
	## this function since placing down a blind has no decision making. This function will not be called for a player after they fold
	##     table_cards - (Card, ...) = a tuple of card objects of length 0, 3, 4, or 5, depending on the round of betting
	##     current_bet - int = the amount of money that must be bet at minimum to stay in (0 if everyone has checked)
	##     player_statuses - [(player_id, in, bet, bet_history), ... ] = an array of tuples containing information about each players bet
	##         player_id - string
	##         in - bool = True => the player has not folded ; False => The player has folded
	##         bet - int = The players current bet in the round
	##         bet_history - [int, ...] = an array of length 0, 1, 2, or 3 depending on the round of betting containing the amount that the player
	##             bet at each previous betting round in the current round
	##
	##   Return - int = The amount the player wishes to bet
	##         return -1 = fold
	##         return current_bet = match (or check if current_bet = 0)
	##         return >current_bet * 2 = raise
	##     placing a bet in the range (current_bet, current_bet * 2) is invalid
	##         If this occurs the bet will be rounded down to a match
	##     a player may go "all in" by betting the amount of money they have left
	##         A player may do this even if the current_bet is greater than their bet
	##         This will result in the pot being split
	##     placing a bet less than current_bet is invalid (unless the player is going all in)
	##         If this occurs, the player will fold
	##     
	def PlaceBet(self, table_cards, current_bet, player_statuses) :
		raise NotImplementedError()

	## Called once a round is decided and a winner(s) has been determined
	##     winners - [(player_id, winnings) ...] = an array of tuples representing the winners of the round and how much they won
	##         player_id - string
	##         winnings - int = the amount that player won
	##       In the event of a tie, winners will be of length >1. If an amount of money must be divided between a number of players
	##       that does not divide evenly, the extra unit of money will be given to a random winner.
	##     pot_size - int = the total amount of money in the pot
	##     table_cards - (Card, ...) = a tuple of card objects of length 0, 3, 4, or 5, depending on how far along the round went
	##     player_statuses - [(player_id, in, hand, bet_history), ...] = an array of tuples containing a summary of the round for each player
	##         player_id - string
	##         in - bool = True => the player did not fold in the round ; False => the player folded during the round
	##         hand - (Card, Card) or None = A tuple representing the players hand during the round
	##             Only included if two or more players made it to the end of the round and the cards were compared
	##             None if player folded or if all but one player folded
	##         bet_history - [int, ...] = an array of length 1, 2, 3, or 4 depending on how far along the round went containing the 
	##             amount that the player bet at each betting round in the current round
	def EndRound(self, winners, pot_size, table_cards, player_statuses) :
		raise NotImplementedError()