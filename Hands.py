import copy

import numpy as np
class Tile:
    #Suit - (bam, dot, crak, wind, or an empty string)
    #Value - (1-9 or dragon for bam/dot/crak, north/east/west/south for wind, dragon, flower, or joker)
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __eq__(self, other):
        return self.suit == other.suit and self.value == other.value

    def __lt__(self, other):
        if self.suit == other.suit:
            return self.value < other.value
        return self.suit < other.suit

    def __str__(self):
        if self.suit == "":
            return f"{self.value}"
        if self.value == "dragon":
            dragon_suits = {"bam": "green", "dot": "white", "crak": "red"}
            return f"{dragon_suits[self.suit]} dragon"
        return f"{self.value} {self.suit}"


#Hands are written in the format of four lists of strings and a boolean.
#The first list contains the values of all "suit-less" tiles (flowers, winds),
    #as well as explicitly listed white dragons (usually taking the form of a '0' on the card).
#The last three lists contain the values of any other tiles in the hand.
#The boolean indicates if the hand is concealed. True = concealed, False = open
#Tiles in the same list must have the same suit.
#A hand that contains less than three suits fills lists starting from the left.
hands = [
    #2025
    [["flower", "flower", "flower", "flower", "white dragon"], ["2", "2", "5"], ["2", "2", "2"], ["2", "2", "2"], False],
    [["flower", "flower", "flower", "flower", "white dragon"], ["2", "2", "5"], ["5", "5", "5"], ["5", "5", "5"], False],
    [["white dragon", "white dragon", "white dragon", "white dragon"], ["2", "2", "2"], ["2", "2", "2", "5", "5", "5", "5"], [], False],
    [["white dragon"], ["2", "2", "5"], ["2", "2", "2", "5", "5", "5"], ["dragon", "dragon", "dragon"], False],
    [["flower", "flower", "white dragon", "white dragon", "white dragon"], ["2", "2", "2"], ["2", "2", "2"], ["5", "5", "5"], True],
    #2468
    [[], ["2", "2", "2", "4", "4", "4", "4", "6", "6", "6", "8", "8", "8", "8"], [], [], False],
    [[], ["2", "2", "2", "4", "4", "4", "4"], ["6", "6", "6", "8", "8", "8", "8"], [], False],
    [["flower", "flower"], ["2", "2", "2", "2"], ["4", "4", "4", "4"], ["6", "6", "6", "6"], False],
    [["flower", "flower"], ["2", "2", "2", "2"], ["6", "6", "6", "6"], ["8", "8", "8", "8"], False],
    [[], ["2", "2", "4", "4", "4", "6", "6", "8", "8", "8", "dragon", "dragon", "dragon", "dragon"], [], [], False],
    [["flower", "flower", "flower", "flower"], ["2", "4", "6", "8"], ["2", "2", "2"], ["2", "2", "2"], False],
    [["flower", "flower", "flower", "flower"], ["2", "4", "6", "8"], ["4", "4", "4"], ["4", "4", "4"], False],
    [["flower", "flower", "flower", "flower"], ["2", "4", "6", "8"], ["6", "6", "6"], ["6", "6", "6"], False],
    [["flower", "flower", "flower", "flower"], ["2", "4", "6", "8"], ["8", "8", "8"], ["8", "8", "8"], False],
    [["flower", "flower", "flower"], ["2", "2", "4", "4", "6", "6", "6", "8", "8", "8", "8"], [], [], False],
    [[], ["2", "2", "2", "4", "4", "4", "4", "6", "6", "6"], ["8", "8"], ["8", "8"], False],
    [["flower", "flower"], ["2", "2", "2", "2"], ["2", "2", "2", "2"], ["dragon", "dragon", "dragon", "dragon"], False],
    [["flower", "flower"], ["4", "4", "4", "4"], ["4", "4", "4", "4"], ["dragon", "dragon", "dragon", "dragon"], False],
    [["flower", "flower"], ["6", "6", "6", "6"], ["6", "6", "6", "6"], ["dragon", "dragon", "dragon", "dragon"], False],
    [["flower", "flower"], ["8", "8", "8", "8"], ["8", "8", "8", "8"], ["dragon", "dragon", "dragon", "dragon"], False],
    [[], ["2", "2", "4", "4", "6", "6", "8", "8"], ["2", "2", "2"], ["2", "2", "2"], True],
    [[], ["2", "2", "4", "4", "6", "6", "8", "8"], ["4", "4", "4"], ["4", "4", "4"], True],
    [[], ["2", "2", "4", "4", "6", "6", "8", "8"], ["6", "6", "6"], ["6", "6", "6"], True],
    [[], ["2", "2", "4", "4", "6", "6", "8", "8"], ["8", "8", "8"], ["8", "8", "8"], True],
    #Any Like Numbers
    [["flower", "flower"], ["1", "1", "1", "1", "dragon"], ["1", "1", "1", "1", "dragon"], ["1", "1"], False],
    [["flower", "flower"], ["2", "2", "2", "2", "dragon"], ["2", "2", "2", "2", "dragon"], ["2", "2"], False],
    [["flower", "flower"], ["3", "3", "3", "3", "dragon"], ["3", "3", "3", "3", "dragon"], ["3", "3"], False],
    [["flower", "flower"], ["4", "4", "4", "4", "dragon"], ["4", "4", "4", "4", "dragon"], ["4", "4"], False],
    [["flower", "flower"], ["5", "5", "5", "5", "dragon"], ["5", "5", "5", "5", "dragon"], ["5", "5"], False],
    [["flower", "flower"], ["6", "6", "6", "6", "dragon"], ["6", "6", "6", "6", "dragon"], ["6", "6"], False],
    [["flower", "flower"], ["7", "7", "7", "7", "dragon"], ["7", "7", "7", "7", "dragon"], ["7", "7"], False],
    [["flower", "flower"], ["8", "8", "8", "8", "dragon"], ["8", "8", "8", "8", "dragon"], ["8", "8"], False],
    [["flower", "flower"], ["9", "9", "9", "9", "dragon"], ["9", "9", "9", "9", "dragon"], ["9", "9"], False],
    [["flower", "flower", "flower", "flower"], ["1", "1", "1", "1"], ["1", "1", "1"], ["1", "1", "1"], False], #FOUR OF A KIND IS REALLY TWO PAIRS
    [["flower", "flower", "flower", "flower"], ["2", "2", "2", "2"], ["2", "2", "2"], ["2", "2", "2"], False], #FOUR OF A KIND IS REALLY TWO PAIRS
    [["flower", "flower", "flower", "flower"], ["3", "3", "3", "3"], ["3", "3", "3"], ["3", "3", "3"], False], #FOUR OF A KIND IS REALLY TWO PAIRS
    [["flower", "flower", "flower", "flower"], ["4", "4", "4", "4"], ["4", "4", "4"], ["4", "4", "4"], False], #FOUR OF A KIND IS REALLY TWO PAIRS
    [["flower", "flower", "flower", "flower"], ["5", "5", "5", "5"], ["5", "5", "5"], ["5", "5", "5"], False], #FOUR OF A KIND IS REALLY TWO PAIRS
    [["flower", "flower", "flower", "flower"], ["6", "6", "6", "6"], ["6", "6", "6"], ["6", "6", "6"], False], #FOUR OF A KIND IS REALLY TWO PAIRS
    [["flower", "flower", "flower", "flower"], ["7", "7", "7", "7"], ["7", "7", "7"], ["7", "7", "7"], False], #FOUR OF A KIND IS REALLY TWO PAIRS
    [["flower", "flower", "flower", "flower"], ["8", "8", "8", "8"], ["8", "8", "8"], ["8", "8", "8"], False], #FOUR OF A KIND IS REALLY TWO PAIRS
    [["flower", "flower", "flower", "flower"], ["9", "9", "9", "9"], ["9", "9", "9"], ["9", "9", "9"], False], #FOUR OF A KIND IS REALLY TWO PAIRS
    [["flower", "flower"], ["1", "1", "1", "dragon", "dragon", "dragon"], ["1", "1", "1"], ["1", "1", "1"], True],
    [["flower", "flower"], ["2", "2", "2", "dragon", "dragon", "dragon"], ["2", "2", "2"], ["2", "2", "2"], True],
    [["flower", "flower"], ["3", "3", "3", "dragon", "dragon", "dragon"], ["3", "3", "3"], ["3", "3", "3"], True],
    [["flower", "flower"], ["4", "4", "4", "dragon", "dragon", "dragon"], ["4", "4", "4"], ["4", "4", "4"], True],
    [["flower", "flower"], ["5", "5", "5", "dragon", "dragon", "dragon"], ["5", "5", "5"], ["5", "5", "5"], True],
    [["flower", "flower"], ["6", "6", "6", "dragon", "dragon", "dragon"], ["6", "6", "6"], ["6", "6", "6"], True],
    [["flower", "flower"], ["7", "7", "7", "dragon", "dragon", "dragon"], ["7", "7", "7"], ["7", "7", "7"], True],
    [["flower", "flower"], ["8", "8", "8", "dragon", "dragon", "dragon"], ["8", "8", "8"], ["8", "8", "8"], True],
    [["flower", "flower"], ["9", "9", "9", "dragon", "dragon", "dragon"], ["9", "9", "9"], ["9", "9", "9"], True],
    #Quints
    [["flower", "flower"], ["1", "1", "1"], ["2", "2", "2", "2"], ["3", "3", "3", "3", "3"], False],
    [["flower", "flower"], ["2", "2", "2"], ["3", "3", "3", "3"], ["4", "4", "4", "4", "4"], False],
    [["flower", "flower"], ["3", "3", "3"], ["4", "4", "4", "4"], ["5", "5", "5", "5", "5"], False],
    [["flower", "flower"], ["4", "4", "4"], ["5", "5", "5", "5"], ["6", "6", "6", "6", "6"], False],
    [["flower", "flower"], ["5", "5", "5"], ["6", "6", "6", "6"], ["7", "7", "7", "7", "7"], False],
    [["flower", "flower"], ["6", "6", "6"], ["7", "7", "7", "7"], ["8", "8", "8", "8", "8"], False],
    [["flower", "flower"], ["7", "7", "7"], ["8", "8", "8", "8"], ["9", "9", "9", "9", "9"], False],
    [["north", "north", "north", "north"], ["1", "1", "1", "1", "1", "2", "2", "2", "2", "2"], [], [], False],
    [["east", "east", "east", "east"], ["1", "1", "1", "1", "1", "2", "2", "2", "2", "2"], [], [], False],
    [["west", "west", "west", "west"], ["1", "1", "1", "1", "1", "2", "2", "2", "2", "2"], [], [], False],
    [["south", "south", "south", "south"], ["1", "1", "1", "1", "1", "2", "2", "2", "2", "2"], [], [], False],
    [["north", "north", "north", "north"], ["2", "2", "2", "2", "2", "3", "3", "3", "3", "3"], [], [], False],
    [["east", "east", "east", "east"], ["2", "2", "2", "2", "2", "3", "3", "3", "3", "3"], [], [], False],
    [["west", "west", "west", "west"], ["2", "2", "2", "2", "2", "3", "3", "3", "3", "3"], [], [], False],
    [["south", "south", "south", "south"], ["2", "2", "2", "2", "2", "3", "3", "3", "3", "3"], [], [], False],
    [["north", "north", "north", "north"], ["3", "3", "3", "3", "3", "4", "4", "4", "4", "4"], [], [], False],
    [["east", "east", "east", "east"], ["3", "3", "3", "3", "3", "4", "4", "4", "4", "4"], [], [], False],
    [["west", "west", "west", "west"], ["3", "3", "3", "3", "3", "4", "4", "4", "4", "4"], [], [], False],
    [["south", "south", "south", "south"], ["3", "3", "3", "3", "3", "4", "4", "4", "4", "4"], [], [], False],
    [["north", "north", "north", "north"], ["4", "4", "4", "4", "4", "5", "5", "5", "5", "5"], [], [], False],
    [["east", "east", "east", "east"], ["4", "4", "4", "4", "4", "5", "5", "5", "5", "5"], [], [], False],
    [["west", "west", "west", "west"], ["4", "4", "4", "4", "4", "5", "5", "5", "5", "5"], [], [], False],
    [["south", "south", "south", "south"], ["4", "4", "4", "4", "4", "5", "5", "5", "5", "5"], [], [], False],
    [["north", "north", "north", "north"], ["5", "5", "5", "5", "5", "6", "6", "6", "6", "6"], [], [], False],
    [["east", "east", "east", "east"], ["5", "5", "5", "5", "5", "6", "6", "6", "6", "6"], [], [], False],
    [["west", "west", "west", "west"], ["5", "5", "5", "5", "5", "6", "6", "6", "6", "6"], [], [], False],
    [["south", "south", "south", "south"], ["5", "5", "5", "5", "5", "6", "6", "6", "6", "6"], [], [], False],
    [["north", "north", "north", "north"], ["6", "6", "6", "6", "6", "7", "7", "7", "7", "7"], [], [], False],
    [["east", "east", "east", "east"], ["6", "6", "6", "6", "6", "7", "7", "7", "7", "7"], [], [], False],
    [["west", "west", "west", "west"], ["6", "6", "6", "6", "6", "7", "7", "7", "7", "7"], [], [], False],
    [["south", "south", "south", "south"], ["6", "6", "6", "6", "6", "7", "7", "7", "7", "7"], [], [], False],
    [["north", "north", "north", "north"], ["7", "7", "7", "7", "7", "8", "8", "8", "8", "8"], [], [], False],
    [["east", "east", "east", "east"], ["7", "7", "7", "7", "7", "8", "8", "8", "8", "8"], [], [], False],
    [["west", "west", "west", "west"], ["7", "7", "7", "7", "7", "8", "8", "8", "8", "8"], [], [], False],
    [["south", "south", "south", "south"], ["7", "7", "7", "7", "7", "8", "8", "8", "8", "8"], [], [], False],
    [["north", "north", "north", "north"], ["8", "8", "8", "8", "8", "9", "9", "9", "9", "9"], [], [], False],
    [["east", "east", "east", "east"], ["8", "8", "8", "8", "8", "9", "9", "9", "9", "9"], [], [], False],
    [["west", "west", "west", "west"], ["8", "8", "8", "8", "8", "9", "9", "9", "9", "9"], [], [], False],
    [["south", "south", "south", "south"], ["8", "8", "8", "8", "8", "9", "9", "9", "9", "9"], [], [], False],
    [["flower", "flower"], ["1", "1", "1", "1", "1"], ["1", "1"], ["1", "1", "1", "1", "1"], False],
    [["flower", "flower"], ["2", "2", "2", "2", "2"], ["2", "2"], ["2", "2", "2", "2", "2"], False],
    [["flower", "flower"], ["3", "3", "3", "3", "3"], ["3", "3"], ["3", "3", "3", "3", "3"], False],
    [["flower", "flower"], ["4", "4", "4", "4", "4"], ["4", "4"], ["4", "4", "4", "4", "4"], False],
    [["flower", "flower"], ["5", "5", "5", "5", "5"], ["5", "5"], ["5", "5", "5", "5", "5"], False],
    [["flower", "flower"], ["6", "6", "6", "6", "6"], ["6", "6"], ["6", "6", "6", "6", "6"], False],
    [["flower", "flower"], ["7", "7", "7", "7", "7"], ["7", "7"], ["7", "7", "7", "7", "7"], False],
    [["flower", "flower"], ["8", "8", "8", "8", "8"], ["8", "8"], ["8", "8", "8", "8", "8"], False],
    [["flower", "flower"], ["9", "9", "9", "9", "9"], ["9", "9"], ["9", "9", "9", "9", "9"], False],
    #Consecutive Run
    [[], ["1", "1", "2", "2", "2", "3", "3", "3", "3", "4", "4", "4", "5", "5"], [], [], False],
    [[], ["5", "5", "6", "6", "6", "7", "7", "7", "7", "8", "8", "8", "9", "9"], [], [], False],
    [[], ["1", "1", "1", "2", "2", "2", "2", "3", "3", "3", "4", "4", "4", "4"], [], [], False],
    [[], ["1", "1", "1", "2", "2", "2", "2"], ["3", "3", "3", "4", "4", "4", "4"], [], False],
    [[], ["2", "2", "2", "3", "3", "3", "3", "4", "4", "4", "5", "5", "5", "5"], [], [], False],
    [[], ["2", "2", "2", "3", "3", "3", "3"], ["4", "4", "4", "5", "5", "5", "5"], [], False],
    [[], ["3", "3", "3", "4", "4", "4", "4", "5", "5", "5", "6", "6", "6", "6"], [], [], False],
    [[], ["3", "3", "3", "4", "4", "4", "4"], ["5", "5", "5", "6", "6", "6", "6"], [], False],
    [[], ["4", "4", "4", "5", "5", "5", "5", "6", "6", "6", "7", "7", "7", "7"], [], [], False],
    [[], ["4", "4", "4", "5", "5", "5", "5"], ["6", "6", "6", "7", "7", "7", "7"], [], False],
    [[], ["5", "5", "5", "6", "6", "6", "6", "7", "7", "7", "8", "8", "8", "8"], [], [], False],
    [[], ["5", "5", "5", "6", "6", "6", "6"], ["7", "7", "7", "8", "8", "8", "8"], [], False],
    [[], ["6", "6", "6", "7", "7", "7", "7", "8", "8", "8", "9", "9", "9", "9"], [], [], False],
    [[], ["6", "6", "6", "7", "7", "7", "7"], ["8", "8", "8", "9", "9", "9", "9"], [], False],
    [["flower", "flower", "flower", "flower"], ["1", "1", "1", "1", "2", "2", "3", "3", "3", "3"], [], [], False],
    [["flower", "flower", "flower", "flower"], ["1", "1", "1", "1"], ["2", "2"], ["3", "3", "3", "3"], False],
    [["flower", "flower", "flower", "flower"], ["2", "2", "2", "2", "3", "3", "4", "4", "4", "4"], [], [], False],
    [["flower", "flower", "flower", "flower"], ["2", "2", "2", "2"], ["3", "3"], ["4", "4", "4", "4"], False],
    [["flower", "flower", "flower", "flower"], ["3", "3", "3", "3", "4", "4", "5", "5", "5", "5"], [], [], False],
    [["flower", "flower", "flower", "flower"], ["3", "3", "3", "3"], ["4", "4"], ["5", "5", "5", "5"], False],
    [["flower", "flower", "flower", "flower"], ["4", "4", "4", "4", "5", "5", "6", "6", "6", "6"], [], [], False],
    [["flower", "flower", "flower", "flower"], ["4", "4", "4", "4"], ["5", "5"], ["6", "6", "6", "6"], False],
    [["flower", "flower", "flower", "flower"], ["5", "5", "5", "5", "6", "6", "7", "7", "7", "7"], [], [], False],
    [["flower", "flower", "flower", "flower"], ["5", "5", "5", "5"], ["6", "6"], ["7", "7", "7", "7"], False],
    [["flower", "flower", "flower", "flower"], ["6", "6", "6", "6", "7", "7", "8", "8", "8", "8"], [], [], False],
    [["flower", "flower", "flower", "flower"], ["6", "6", "6", "6"], ["7", "7"], ["8", "8", "8", "8"], False],
    [["flower", "flower", "flower", "flower"], ["7", "7", "7", "7", "8", "8", "9", "9", "9", "9"], [], [], False],
    [["flower", "flower", "flower", "flower"], ["7", "7", "7", "7"], ["8", "8"], ["9", "9", "9", "9"], False],
    [["flower", "flower", "flower"], ["1", "2", "3"], ["4", "4", "4", "4"], ["5", "5", "5", "5"], False],
    [["flower", "flower", "flower"], ["2", "3", "4"], ["5", "5", "5", "5"], ["6", "6", "6", "6"], False],
    [["flower", "flower", "flower"], ["3", "4", "5"], ["6", "6", "6", "6"], ["7", "7", "7", "7"], False],
    [["flower", "flower", "flower"], ["4", "5", "6"], ["7", "7", "7", "7"], ["8", "8", "8", "8"], False],
    [["flower", "flower", "flower"], ["5", "6", "7"], ["8", "8", "8", "8"], ["9", "9", "9", "9"], False],
    [["flower", "flower"], ["1", "1", "2", "2", "2", "3", "3", "3", "3", "dragon", "dragon", "dragon"], [], [], False],
    [["flower", "flower"], ["2", "2", "3", "3", "3", "4", "4", "4", "4", "dragon", "dragon", "dragon"], [], [], False],
    [["flower", "flower"], ["3", "3", "4", "4", "4", "5", "5", "5", "5", "dragon", "dragon", "dragon"], [], [], False],
    [["flower", "flower"], ["4", "4", "5", "5", "5", "6", "6", "6", "6", "dragon", "dragon", "dragon"], [], [], False],
    [["flower", "flower"], ["5", "5", "6", "6", "6", "7", "7", "7", "7", "dragon", "dragon", "dragon"], [], [], False],
    [["flower", "flower"], ["6", "6", "7", "7", "7", "8", "8", "8", "8", "dragon", "dragon", "dragon"], [], [], False],
    [["flower", "flower"], ["7", "7", "8", "8", "8", "9", "9", "9", "9", "dragon", "dragon", "dragon"], [], [], False],
    [[], ["1", "1", "1", "2", "2", "2", "3", "3", "3", "3"], ["dragon", "dragon"], ["dragon", "dragon"], False],
    [[], ["2", "2", "2", "3", "3", "3", "4", "4", "4", "4"], ["dragon", "dragon"], ["dragon", "dragon"], False],
    [[], ["3", "3", "3", "4", "4", "4", "5", "5", "5", "5"], ["dragon", "dragon"], ["dragon", "dragon"], False],
    [[], ["4", "4", "4", "5", "5", "5", "6", "6", "6", "6"], ["dragon", "dragon"], ["dragon", "dragon"], False],
    [[], ["5", "5", "5", "6", "6", "6", "7", "7", "7", "7"], ["dragon", "dragon"], ["dragon", "dragon"], False],
    [[], ["6", "6", "6", "7", "7", "7", "8", "8", "8", "8"], ["dragon", "dragon"], ["dragon", "dragon"], False],
    [[], ["7", "7", "7", "8", "8", "8", "9", "9", "9", "9"], ["dragon", "dragon"], ["dragon", "dragon"], False],
    [[], ["1", "1", "2", "3", "4", "5"], ["1", "1", "1", "1"], ["1", "1", "1", "1"], False],
    [[], ["1", "2", "2", "3", "4", "5"], ["2", "2", "2", "2"], ["2", "2", "2", "2"], False],
    [[], ["1", "2", "3", "3", "4", "5"], ["3", "3", "3", "3"], ["3", "3", "3", "3"], False],
    [[], ["1", "2", "3", "4", "4", "5"], ["4", "4", "4", "4"], ["4", "4", "4", "4"], False],
    [[], ["1", "2", "3", "4", "5", "5"], ["5", "5", "5", "5"], ["5", "5", "5", "5"], False],
    [[], ["2", "2", "3", "4", "5", "6"], ["2", "2", "2", "2"], ["2", "2", "2", "2"], False],
    [[], ["2", "3", "3", "4", "5", "6"], ["3", "3", "3", "3"], ["3", "3", "3", "3"], False],
    [[], ["2", "3", "4", "4", "5", "6"], ["4", "4", "4", "4"], ["4", "4", "4", "4"], False],
    [[], ["2", "3", "4", "5", "5", "6"], ["5", "5", "5", "5"], ["5", "5", "5", "5"], False],
    [[], ["2", "3", "4", "5", "6", "6"], ["6", "6", "6", "6"], ["6", "6", "6", "6"], False],
    [[], ["3", "3", "4", "5", "6", "7"], ["3", "3", "3", "3"], ["3", "3", "3", "3"], False],
    [[], ["3", "4", "4", "5", "6", "7"], ["4", "4", "4", "4"], ["4", "4", "4", "4"], False],
    [[], ["3", "4", "5", "5", "6", "7"], ["5", "5", "5", "5"], ["5", "5", "5", "5"], False],
    [[], ["3", "4", "5", "6", "6", "7"], ["6", "6", "6", "6"], ["6", "6", "6", "6"], False],
    [[], ["3", "4", "5", "6", "7", "7"], ["7", "7", "7", "7"], ["7", "7", "7", "7"], False],
    [[], ["4", "4", "5", "6", "7", "8"], ["4", "4", "4", "4"], ["4", "4", "4", "4"], False],
    [[], ["4", "5", "5", "6", "7", "8"], ["5", "5", "5", "5"], ["5", "5", "5", "5"], False],
    [[], ["4", "5", "6", "6", "7", "8"], ["6", "6", "6", "6"], ["6", "6", "6", "6"], False],
    [[], ["4", "5", "6", "7", "7", "8"], ["7", "7", "7", "7"], ["7", "7", "7", "7"], False],
    [[], ["4", "5", "6", "7", "8", "8"], ["8", "8", "8", "8"], ["8", "8", "8", "8"], False],
    [[], ["5", "5", "6", "7", "8", "9"], ["5", "5", "5", "5"], ["5", "5", "5", "5"], False],
    [[], ["5", "6", "6", "7", "8", "9"], ["6", "6", "6", "6"], ["6", "6", "6", "6"], False],
    [[], ["5", "6", "7", "7", "8", "9"], ["7", "7", "7", "7"], ["7", "7", "7", "7"], False],
    [[], ["5", "6", "7", "8", "8", "9"], ["8", "8", "8", "8"], ["8", "8", "8", "8"], False],
    [[], ["5", "6", "7", "8", "9", "9"], ["9", "9", "9", "9"], ["9", "9", "9", "9"], False],
    [["flower", "flower"], ["1", "2", "2", "3", "3", "3"], ["1", "2", "2", "3", "3", "3"], [], True],
    [["flower", "flower"], ["2", "3", "3", "4", "4", "4"], ["2", "3", "3", "4", "4", "4"], [], True],
    [["flower", "flower"], ["3", "4", "4", "5", "5", "5"], ["3", "4", "4", "5", "5", "5"], [], True],
    [["flower", "flower"], ["4", "5", "5", "6", "6", "6"], ["4", "5", "5", "6", "6", "6"], [], True],
    [["flower", "flower"], ["5", "6", "6", "7", "7", "7"], ["5", "6", "6", "7", "7", "7"], [], True],
    [["flower", "flower"], ["6", "7", "7", "8", "8", "8"], ["6", "7", "7", "8", "8", "8"], [], True],
    [["flower", "flower"], ["7", "8", "8", "9", "9", "9"], ["7", "8", "8", "9", "9", "9"], [], True],
    #13579
    [[], ["1", "1", "3", "3", "3", "5", "5", "5", "5", "7", "7", "7", "9", "9"], [], [], False],
    [[], ["1", "1", "3", "3", "3"], ["5", "5", "5", "5"], ["7", "7", "7", "9", "9"], False],
    [[], ["1", "1", "1", "3", "3", "3", "3"], ["3", "3", "3", "5", "5", "5", "5"], [], False],
    [[], ["5", "5", "5", "7", "7", "7", "7"], ["7", "7", "7", "9", "9", "9", "9"], [], False],
    [[], ["1", "1", "1", "1", "3", "3", "3", "5", "5", "5", "5", "dragon", "dragon", "dragon"], [], [], False],
    [[], ["5", "5", "5", "5", "7", "7", "7", "9", "9", "9", "9", "dragon", "dragon", "dragon"], [], [], False],
    [["flower", "flower", "flower", "flower", "white dragon"], ["1", "1", "1", "1", "9", "9", "9", "9"], ["1"], [], False],
    [["flower", "flower", "flower"], ["1", "3", "5", "7", "7", "7", "7", "9", "9", "9", "9"], [], [], False],
    [["flower", "flower", "flower"], ["1", "3", "5"], ["7", "7", "7", "7"], ["9", "9", "9", "9"], False],
    [[], ["1", "1", "1", "3", "3", "3", "5", "5", "5", "5"], ["dragon", "dragon"], ["dragon", "dragon"], False],
    [[], ["5", "5", "5", "7", "7", "7", "9", "9", "9", "9"], ["dragon", "dragon"], ["dragon", "dragon"], False],
    [["north", "east", "west", "south"], ["1", "1", "3", "3", "3"], ["3", "3", "3", "5", "5"], [], False],
    [["north", "east", "west", "south"], ["5", "5", "7", "7", "7"], ["7", "7", "7", "9", "9"], [], False],
    [[], ["1", "1", "1", "1", "9", "9", "9", "9"], ["3", "3", "5", "5", "7", "7"], [], False],
    [["flower", "flower"], ["1", "1", "3", "3"], ["1", "1", "1", "3", "3", "3"], ["5", "5"], True],
    [["flower", "flower"], ["5", "5", "7", "7"], ["5", "5", "5", "7", "7", "7"], ["9", "9"], True],
    #Winds-Dragons
    [["north", "north", "north", "north", "east", "east", "east", "west", "west", "west", "south", "south", "south", "south"], [], [], [], False],
    [["north", "north", "north", "east", "east", "east", "east", "west", "west", "west", "west", "south", "south", "south"], [], [], [], False],
    [["flower", "flower"], ["1", "2", "3", "dragon", "dragon", "dragon", "dragon"], ["dragon", "dragon"], ["dragon", "dragon", "dragon"], False],
    [["flower", "flower"], ["2", "3", "4", "dragon", "dragon", "dragon", "dragon"], ["dragon", "dragon"], ["dragon", "dragon", "dragon"], False],
    [["flower", "flower"], ["3", "4", "5", "dragon", "dragon", "dragon", "dragon"], ["dragon", "dragon"], ["dragon", "dragon", "dragon"], False],
    [["flower", "flower"], ["4", "5", "6", "dragon", "dragon", "dragon", "dragon"], ["dragon", "dragon"], ["dragon", "dragon", "dragon"], False],
    [["flower", "flower"], ["5", "6", "7", "dragon", "dragon", "dragon", "dragon"], ["dragon", "dragon"], ["dragon", "dragon", "dragon"], False],
    [["flower", "flower"], ["6", "7", "8", "dragon", "dragon", "dragon", "dragon"], ["dragon", "dragon"], ["dragon", "dragon", "dragon"], False],
    [["flower", "flower"], ["7", "8", "9", "dragon", "dragon", "dragon", "dragon"], ["dragon", "dragon"], ["dragon", "dragon", "dragon"], False],
    [["flower", "flower", "flower", "north", "north", "east", "east", "west", "west", "west", "south", "south", "south", "south"], [], [], [], False],
    [["flower", "flower", "flower", "flower", "north", "east", "west", "south"], ["dragon", "dragon", "dragon"], ["dragon", "dragon", "dragon"], [], False],
    [["north", "north", "north", "north", "south", "south", "south", "south"], ["1"], ["1", "1"], ["1", "1", "1"], False],
    [["north", "north", "north", "north", "south", "south", "south", "south"], ["3"], ["3", "3"], ["3", "3", "3"], False],
    [["north", "north", "north", "north", "south", "south", "south", "south"], ["5"], ["5", "5"], ["5", "5", "5"], False],
    [["north", "north", "north", "north", "south", "south", "south", "south"], ["7"], ["7", "7"], ["7", "7", "7"], False],
    [["north", "north", "north", "north", "south", "south", "south", "south"], ["9"], ["9", "9"], ["9", "9", "9"], False],
    [["east", "east", "east", "east", "west", "west", "west", "west"], ["2"], ["2", "2"], ["2", "2", "2"], False],
    [["east", "east", "east", "east", "west", "west", "west", "west"], ["4"], ["4", "4"], ["4", "4", "4"], False],
    [["east", "east", "east", "east", "west", "west", "west", "west"], ["6"], ["6", "6"], ["6", "6", "6"], False],
    [["east", "east", "east", "east", "west", "west", "west", "west"], ["8"], ["8", "8"], ["8", "8", "8"], False],
    [["north", "north", "east", "east", "east", "west", "west", "west", "south", "south", "white dragon"], ["2", "2", "5"], [], [], False],
    [["north", "north", "north", "east", "east", "west", "west", "south", "south", "south", "white dragon"], ["2", "2", "5"], [], [], False],
    [["north", "north", "east", "east", "west", "west", "west", "south", "south", "south"], ["dragon", "dragon", "dragon", "dragon"], [], [], True],
    #369
    [[], ["3", "3", "3", "6", "6", "6", "6"], ["6", "6", "6", "9", "9", "9", "9"], [], False],
    [[], ["3", "3", "3", "6", "6", "6", "6"], ["6", "6", "6"], ["9", "9", "9", "9"], False],
    [["flower", "flower"], ["3", "3", "3", "3", "6", "6", "6", "6", "9", "9", "9", "9"], [], [], False],
    [["flower", "flower"], ["3", "3", "3", "3"], ["6", "6", "6", "6"], ["9", "9", "9", "9"], False],
    [[], ["3", "3", "3", "3", "dragon", "dragon", "dragon"], ["3", "3", "3", "3", "dragon", "dragon", "dragon"], [], False],
    [[], ["6", "6", "6", "6", "dragon", "dragon", "dragon"], ["6", "6", "6", "6", "dragon", "dragon", "dragon"], [], False],
    [[], ["9", "9", "9", "9", "dragon", "dragon", "dragon"], ["9", "9", "9", "9", "dragon", "dragon", "dragon"], [], False],
    [["flower", "flower", "flower"], ["3", "3", "3", "3", "9", "9", "9", "9"], ["3", "6", "9"], [], False],
    [[], ["3", "3", "6", "6", "9", "9"], ["3", "3", "3", "3"], ["3", "3", "3", "3"], False],
    [[], ["3", "3", "6", "6", "9", "9"], ["6", "6", "6", "6"], ["6", "6", "6", "6"], False],
    [[], ["3", "3", "6", "6", "9", "9"], ["9", "9", "9", "9"], ["9", "9", "9", "9"], False],
    [["flower", "flower"], ["3", "3", "3", "dragon"], ["6", "6", "6", "dragon"], ["9", "9", "9", "dragon"], True],
    #Singles and Pairs
    [["north", "north", "east", "west", "south", "south"], ["1", "1", "2", "2", "3", "3", "4", "4"], [], [], True],
    [["north", "north", "east", "west", "south", "south"], ["2", "2", "3", "3", "4", "4", "5", "5"], [], [], True],
    [["north", "north", "east", "west", "south", "south"], ["3", "3", "4", "4", "5", "5", "6", "6"], [], [], True],
    [["north", "north", "east", "west", "south", "south"], ["4", "4", "5", "5", "6", "6", "7", "7"], [], [], True],
    [["north", "north", "east", "west", "south", "south"], ["5", "5", "6", "6", "7", "7", "8", "8"], [], [], True],
    [["north", "north", "east", "west", "south", "south"], ["6", "6", "7", "7", "8", "8", "9", "9"], [], [], True],
    [["flower", "flower"], ["2", "4", "6", "8", "dragon", "dragon"], ["2", "4", "6", "8", "dragon", "dragon"], [], True],
    [[], ["3", "3", "6", "6", "9", "9"], ["3", "3", "6", "6", "9", "9"], ["3", "3"], True],
    [[], ["3", "3", "6", "6", "9", "9"], ["3", "3", "6", "6", "9", "9"], ["6", "6"], True],
    [[], ["3", "3", "6", "6", "9", "9"], ["3", "3", "6", "6", "9", "9"], ["9", "9"], True],
    [["flower", "flower"], ["1", "1", "2", "2"], ["1", "1", "2", "2"], ["1", "1", "2", "2"], True],
    [["flower", "flower"], ["2", "2", "3", "3"], ["2", "2", "3", "3"], ["2", "2", "3", "3"], True],
    [["flower", "flower"], ["3", "3", "4", "4"], ["3", "3", "4", "4"], ["3", "3", "4", "4"], True],
    [["flower", "flower"], ["4", "4", "5", "5"], ["4", "4", "5", "5"], ["4", "4", "5", "5"], True],
    [["flower", "flower"], ["5", "5", "6", "6"], ["5", "5", "6", "6"], ["5", "5", "6", "6"], True],
    [["flower", "flower"], ["6", "6", "7", "7"], ["6", "6", "7", "7"], ["6", "6", "7", "7"], True],
    [["flower", "flower"], ["7", "7", "8", "8"], ["7", "7", "8", "8"], ["7", "7", "8", "8"], True],
    [["flower", "flower"], ["8", "8", "9", "9"], ["8", "8", "9", "9"], ["8", "8", "9", "9"], True],
    [[], ["1", "1", "3", "3", "5", "5", "7", "7", "9", "9"], ["1", "1"], ["1", "1"], True],
    [[], ["1", "1", "3", "3", "5", "5", "7", "7", "9", "9"], ["3", "3"], ["3", "3"], True],
    [[], ["1", "1", "3", "3", "5", "5", "7", "7", "9", "9"], ["5", "5"], ["5", "5"], True],
    [[], ["1", "1", "3", "3", "5", "5", "7", "7", "9", "9"], ["7", "7"], ["7", "7"], True],
    [[], ["1", "1", "3", "3", "5", "5", "7", "7", "9", "9"], ["9", "9"], ["9", "9"], True],
    [["flower", "flower", "white dragon", "white dragon", "white dragon"], ["2", "2", "5"], ["2", "2", "5"], ["2", "2", "5"], True]
]

joker_exception_list = [[["flower", "flower", "flower", "flower"], ["1", "1", "1", "1"], ["1", "1", "1"], ["1", "1", "1"], False],
                        [["flower", "flower", "flower", "flower"], ["2", "2", "2", "2"], ["2", "2", "2"], ["2", "2", "2"], False],
                        [["flower", "flower", "flower", "flower"], ["3", "3", "3", "3"], ["3", "3", "3"], ["3", "3", "3"], False],
                        [["flower", "flower", "flower", "flower"], ["4", "4", "4", "4"], ["4", "4", "4"], ["4", "4", "4"], False],
                        [["flower", "flower", "flower", "flower"], ["5", "5", "5", "5"], ["5", "5", "5"], ["5", "5", "5"], False],
                        [["flower", "flower", "flower", "flower"], ["6", "6", "6", "6"], ["6", "6", "6"], ["6", "6", "6"], False],
                        [["flower", "flower", "flower", "flower"], ["7", "7", "7", "7"], ["7", "7", "7"], ["7", "7", "7"], False],
                        [["flower", "flower", "flower", "flower"], ["8", "8", "8", "8"], ["8", "8", "8"], ["8", "8", "8"], False],
                        [["flower", "flower", "flower", "flower"], ["9", "9", "9", "9"], ["9", "9", "9"], ["9", "9", "9"], False]]

def sort_and_convert_hand(rack: [Tile]):
    #Converts and sorts hand into four string lists: suit-less, bams, dots, craks
    sorted_rack = [[], [], [], []]
    for tile in rack:
        match tile.suit:
            case "bam":
                sorted_rack[1].append(tile.value)
            case "dot":
                sorted_rack[2].append(tile.value)
            case "crak":
                sorted_rack[3].append(tile.value)
            case _:
                sorted_rack[0].append(tile.value)
    return sorted_rack

def revert_hand(rack: [[str]]):
    #Converts list of four string lists (suit-less, bams, dots, craks) into a list of Tiles
    #Suit - (bam, dot, crak, wind, or an empty string)
    #Value - (1-9 or dragon for bam/dot/crak, north/east/west/south for wind, dragon, flower, or joker)
    tiles = []
    for tile in rack[0]:
        if tile in ["north", "east", "west", "south"]:
            tiles.append(Tile("wind", tile))
        elif tile == "white dragon":
            tiles.append(Tile("dot", "dragon"))
        else:
            tiles.append(Tile("", tile))
    suits = ["bam", "dot", "crak"]
    for index in np.arange(1, 4):
        for tile in rack[index]:
            tiles.append(Tile(suits[index-1], tile))
    return tiles

def hand_permutations(rack: [[str]]):
    #Returns a list of all suit permutations of the hand, not including the first element, since suit-less doesn't move
    #First element of the returned list is always the original list
    return [rack,
            [rack[0], rack[1], rack[3], rack[2]],
            [rack[0], rack[2], rack[1], rack[3]],
            [rack[0], rack[2], rack[3], rack[1]],
            [rack[0], rack[3], rack[1], rack[2]],
            [rack[0], rack[3], rack[2], rack[1]]]

def hand_distance(rack: [Tile], hand: [[str], [str], [str], [str]]):
    #Returns the number of tiles needed to reach hand from given rack

    #Check rack length
    if len(rack) != 13 and len(rack) != 14:
        raise Exception("Invalid rack size of " + str(len(rack)))

    sorted_rack = sort_and_convert_hand(rack) #Converts rack to str lists in order of [suit-less, bams, dots, craks]

    #Evaluate which permutations are necessary to check
    if not hand[1]:
        #Hand does not contain any bam/crak/dots, so we only have to consider one permutation
        perms = [hand]
    elif not hand[2]:
        #Hand contains only one suit, so we only need to consider three permutations
        perms = [hand, [hand[0], [], hand[1], []], [hand[0], [], [], hand[1]]]
    else:
        #Otherwise, we need to consider all six permutations
        perms = hand_permutations(hand)

    #Find the minimum distance between each permutation
    min_distance = 14
    unused_tiles = []
    for perm in perms: #Iterate through each permutation (1, 3, or 6 times)
        rack_copy = copy.deepcopy(sorted_rack)
        cur_distance = 14
        for i in np.arange(4): #Iterate through each suit slot (4 times)
            #print(perm[i])
            for val in perm[i]: #Iterate through each tile in current suit (0-14 times)
                if rack_copy[i].count(val) != 0: #Tile found in rack
                    cur_distance -= 1
                    rack_copy[i].remove(val)
                elif i == 0 and val == "white dragon" and rack_copy[2].count("dragon") != 0: #White dragon found and have dragon in dots
                    cur_distance -= 1
                    rack_copy[2].remove("dragon")
                elif (rack_copy[0].count("joker") != 0 and hand[i].count(val) > 2 #Joker usable for tile
                      and not (hand in joker_exception_list and len(hand[i]) == 4 and i != 0)): #Exception for specific hand
                    cur_distance -= 1
                    rack_copy[0].remove("joker")
        if cur_distance < min_distance:
            min_distance = cur_distance
            unused_tiles = copy.deepcopy(rack_copy)
    return min_distance, unused_tiles

def find_closest_hands(rack: [Tile], show_depth=1, depth=2):
    dtype_hand = [('hand', list), ('distance', int), ('unused', list)]
    top_hands = np.ndarray(len(hands), dtype=dtype_hand)
    index = 0
    for hand in hands:
        distance, unused_tiles = hand_distance(rack, hand[0:4])
        top_hands[index] = (hand, distance, unused_tiles)
        index += 1
    top_hands.sort(order='distance')
    top_discards = evaluate_discards(rack, top_hands, depth)
    return top_hands[0:find_depth_index(top_hands, show_depth)], top_discards

def find_depth_index(top_hands: np.ndarray, show_depth: int):
    best = top_hands[0]['distance']
    target_depth = best + show_depth + 1
    index = 0
    for hand in top_hands:
        if hand['distance'] == target_depth:
            break
        index += 1
    return index

def evaluate_discards(rack: [Tile], top_hands: np.ndarray, depth=2):
    dtype_rack = [('tile', Tile), ('strength rating', float)] #Higher strength rating = tile is more useful
    dtype_usage = [('tile', Tile), ('exposed', int), ('concealed', int)]
    top_discards = np.ndarray(len(rack), dtype=dtype_rack)
    curr_usage = np.ndarray(len(rack), dtype=dtype_usage)
    index = 0
    for tile in rack:
        top_discards[index] = (tile, 0)
        curr_usage[index] = (tile, 0, 0)
        index += 1
    best_tier = top_hands[0]['distance']
    curr_tier = best_tier
    curr_size = 0
    best_size = 0
    top_hands_index = 0
    for hand in top_hands:
        if hand['distance'] != curr_tier or top_hands_index == (len(top_hands) - 1):
            if curr_tier == best_tier:
                best_size = curr_size
            index = 0
            for tile in top_discards:
                rating = get_usage_rating(curr_usage[index]['exposed'], curr_usage[index]['concealed'],
                                          curr_tier, best_tier, curr_size, best_size)
                tile['strength rating'] = round(tile['strength rating'] + rating, 2)
                curr_usage[index]['exposed'] = 0
                curr_usage[index]['concealed'] = 0
                index += 1
            curr_tier = hand['distance']
            curr_size = 0
        if (curr_tier - best_tier) > depth:
            break
        hand_type = 'concealed' if hand['hand'][4] else 'exposed'
        curr_unused = revert_hand(hand['unused'])
        for entry in curr_usage:
            tile = entry['tile']
            if curr_unused.count(tile) == 0:
                entry[hand_type] += 1
            else: curr_unused.remove(tile)
        curr_size += 1
        top_hands_index += 1
    top_discards.sort(order='strength rating')
    return top_discards


    #- Rating = (
    #               (exposed hands that use tile in tier / tier size) ---> basic exposed usability proportion
    #               +
    #               ((concealed hands that use tile in tier / tier size) ---> basic concealed usability proportion
    #               / 1.5^(tier - 1)) ---> factor to reduce weight of concealed hands, especially ones with many tiles left
    #           )
    #           * tier size / best tier size ---> factor to favor having more options
    #           / (tier - best tier + 1)^3 ---> factor to favor closer hands
    #

def get_usage_rating(exposed_count, concealed_count, tier, best_tier, tier_size, best_tier_size):
    return (((exposed_count / tier_size) + ((concealed_count / tier_size) / (1.5 ** (tier - 1))))
            * tier_size / best_tier_size
            / ((tier - best_tier + 1) ** 3))


