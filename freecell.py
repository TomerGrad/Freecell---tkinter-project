"""
FreeCell solitaire game.
Run and play!
The Plain-Games package, play with fun and care!
"""

from tkinter import *
from tkinter.messagebox import showinfo
from random import shuffle

from cards import RANKS, SUITS, PlayCard

def closest(coord, positions: range):
    delta = [abs(pos-coord) for pos in positions]
    return delta.index(min(delta))


class Game(Canvas):

    def __init__(self, master=None, **kwargs):
        super(Game, self).__init__(master, bg='#006000', width=640, height=640, **kwargs)
        self.master.geometry("640x640+200+1")
        self.master.resizable(False, False)
        self.master.title('FreeCell')
        for i in range(4, 221, 72):
            self.create_rectangle(i, 4, i+72, 100, fill='#005800')
        for i in range(348, 565, 72):
            self.create_rectangle(i, 4, i+72, 100, fill='#005800')

        self.table = [[] for _ in range(8)]
        self.uplevel = [[] for _ in range(8)]

        self.upcard_stack = None
        self.upcard = None

        self.slots_pos = range(40, 601, 80)
        self.freecells_pos = range(40, 257, 72)
        self.decks_pos = range(384, 601, 72)

        # load, shuffle and deal the cards
        cards = [PlayCard(rank=rank, suit=suit, file=fr'cards\{rank}{suit}.gif')
                 for rank in RANKS for suit in SUITS]
        shuffle(cards)
        for i, card in enumerate(cards):
            self.table[i%8].append(card)

        self.bind('<Button-1>', self.onclick)
        self.bind('<Button1-ButtonRelease>', self.onrelease)
        self.bind('<Double-Button-1>', self.doubleclick)
        self.bind('<Button-3>', self.onrightclick)

        self.update()
        self.pack()

    def update(self):
        self.delete('card')
        for i, slot in enumerate(self.table):
            for j, card in enumerate(slot):
                self.create_image(self.slots_pos[i], 300+j*30*(0.75 if len(slot) > 10 else 1), image=card, tags=('card', card.face))
        for i, slot in enumerate(self.uplevel):
            for card in slot:
                if i < 4:
                    self.create_image(self.freecells_pos[i], 52, image=card, tags=('card', card.face))
                else:
                    self.create_image(self.decks_pos[i-4], 52, image=card, tags=('card', card.face))
        if all(map(lambda l: len(l)==14, self.uplevel[:4])):
            showinfo('yay you WON!')
            exit()

    def onclick(self, event):
        if event.y < 240:
            self.upcard_stack = self.uplevel[:4][closest(event.x, self.freecells_pos)]
        else:
            self.upcard_stack = self.table[closest(event.x, self.slots_pos)]
        if self.upcard_stack:
            self.upcard = self.upcard_stack[-1]
            self.move(self.upcard.face, 0, 30)

    def onrelease(self, event):
        if not self.upcard:
            return
        if event.y > 240:
            slot = self.table[closest(event.x, self.slots_pos)]
            last = slot[-1] if slot else None
            valid = self.upcard.isaboveable(last)
        elif event.y < 240 and event.x < 320:
            slot = self.uplevel[:4][closest(event.x, self.freecells_pos)]
            valid = not slot
        else:
            slot = self.uplevel[4:][self.upcard.suit]
            valid = self.upcard.rank == len(slot)
        if valid:
            slot.append(self.upcard_stack.pop())
            self.upcard = None
        self.update()

    def doubleclick(self, *event):
        for cell in self.uplevel[:4]:
            if not cell:
                cell.append(self.upcard_stack.pop())
                self.upcard = None
                break
        self.upcard_stack = None

    def onrightclick(self, *event):
        for slot in self.table:
            if slot and slot[-1].rank == len(self.uplevel[4:][slot[-1].suit]):
                self.uplevel[4:][slot[-1].suit].append(slot.pop())
                self.onrightclick()
        for slot in self.uplevel[:4]:
            if slot and slot[-1].rank == len(self.uplevel[4:][slot[-1].suit]):
                self.uplevel[4:][slot[-1].suit].append(slot.pop())
                self.onrightclick()
        self.update()


if __name__ == '__main__':
    Game().mainloop()
