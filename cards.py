"""
This module provide tkinter's card representation for my Plain-Games package.
"""

from tkinter import PhotoImage

RANKS = 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'
SUITS = 'cshd'

class PlayCard(PhotoImage):

    def __init__(self, rank, suit, **kwargs):
        super(PlayCard, self).__init__(**kwargs)
        self.suit = SUITS.index(suit)
        self.rank = RANKS.index(rank)
        self.face = rank+suit
        self.red = suit in 'hd'

    def isaboveable(self, other) -> bool:
        """
        This method take another card, return the validation of putting 'self' on other in most solitaire games.
        Return True in case of an empty pile/free-cell.
        """
        if other is None:
            return True
        return self.rank == (other.rank-1) and (self.red != other.red)
