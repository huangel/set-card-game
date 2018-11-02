import random
import time
import os
import sys
import threading
import tkinter as tk
from os.path import expanduser
from pynput.keyboard import Key, Controller

import termios
import struct
import fcntl

def set_winsize(fd, row, col, xpix=0, ypix=0):
	"""
	Resizes the terminal/console window
	"""
	winsize = struct.pack("HHHH", row, col, xpix, ypix)
	fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)

class Card:
	def __init__(self, value, size, shape):
		self.value = value
		self.size = size
		self.shape = shape

	def __str__(self):
		out = None
		if self.shape == 'tuple':
			out = ['(',')']
		elif self.shape == 'list':
			out = ['[',']']
		elif self.shape == 'set':
			out = ['{','}']

		for i in range(self.size):
			out.insert(1, str(self.value))
		return str("".join(out))

class TimeApp(tk.Tk):
    def __init__(self, seconds, GAME):
        tk.Tk.__init__(self)
        self.label = tk.Label(self, text="", width=10)
        self.label.pack()
        self.remaining = 0
        self.countdown(seconds)
        self.GAME = GAME

    def countdown(self, remaining = None):
        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.label.configure(text="time's up!")
            self.GAME.end_game()
        else:
            self.label.configure(text="%d" % self.remaining)
            self.remaining = self.remaining - 1
            self.after(1000, self.countdown)

class Deck:
	def __init__(self):
		self.available_cards = self.generate_cards()

	def get_cards(self, n):
		"""	
			pops n cards off the deck, and returns them in a list
			returns None if no cards left.
		"""
		popped_cards = []
		for i in range(n):
			popped_cards.append(self.available_cards.pop())
		return popped_cards

	def generate_cards(self):
		"""
			Generates a list of all possible cards, randomly shuffled
		"""
		full_deck = []
		for num in range(0, 3): #0, 1, 2 for value
			for size in range(1, 4): # 1, 2,3 for size
				for shape in ['tuple', 'list', 'set']:
					full_deck.append(Card(num, size, shape))
		random.shuffle(full_deck)
		return full_deck


class Game:

	def __init__(self, game_length = 45):
		self.score = 0
		self.current_cards = None
		self.start_time = time.time()
		self.game_length = game_length
		self.deck = Deck()
		self.current_cards = self.deck.get_cards(12)
		self.main_thread = threading.Thread(target=self.main, args=())
		self.main_thread.daemon = True
		self.timer_app = None
		self.high_score = self.get_high_score()
		self.main_thread_active = True

	def start(self):
		# resize terminal
		sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=40, cols=80))
		self.display_banner()
		self.get_instructions()
		start = input("Do you want to start the game? [Y/N]").upper()
		if start == "Y":
			self.main_thread.start()
			self.start_timer()
			keyboard = Controller()
			keyboard.press(Key.enter)
			keyboard.release(Key.enter)		
			self.end_game()	
			
		print('\nEnd of Game! Your score is', self.score)
		if self.score > self.high_score[1]:
			print("New high score! You beat {}'s high score of {}".format(self.high_score[0], self.high_score[1]))
			print("what is your name?")
			name = sys.stdin.readline()
			self.set_high_score(name, self.score)

		else:
			print("{} has the high score of {}".format(self.high_score[0], self.high_score[1]))

	def start_timer(self):
		self.timer_app = TimeApp(self.game_length, self)
		self.timer_app.mainloop()


	def end_game(self):
		self.main_thread_active = False
		try:
			self.timer_app.destroy()
		except:
			pass
		self.main_thread.join(1)

	def main(self):
		while self.main_thread_active:
			self.display_cards()
			if len(self.current_cards) < 3:
				print("Congrats! You've finished the game.")
				break
			else:
				print('What three cards make a SET?')
				value = sys.stdin.readline()
				try:
					if value.strip().upper() == 'A':
						self.current_cards.extend(self.deck.get_cards(3))
						continue
					else:
						x, y, z = value.split()
						x = int(x)
						y = int(y)
						z = int(z)
				except:
					print("Please enter three integers (i.e. `2 4 5`) or `A` to add 3 cards")
					time.sleep(2)
					continue					

				if (x > len(self.current_cards) or x < 0 or y > len(self.current_cards) or y < 0 or z > len(self.current_cards) or z < 0):
					print("please enter the index of the cards")
					time.sleep(2)
					continue

				if self.is_set(x, y, z) and len(self.current_cards) > 12: #check if the inputs make a set 
					self.score +=1
					self.remove_cards([x, y, z])
				elif self.is_set(x, y, z):
					if len(self.deck.available_cards) > 2:
						self.current_cards[x] = self.deck.get_cards(1)[0] #replace card x 
						self.current_cards[y] = self.deck.get_cards(1)[0]
						self.current_cards[z] = self.deck.get_cards(1)[0]
						self.score += 1
					else:
						self.remove_cards([x, y, z])
						self.score += 1

				else:
					sys.stdout.write("\r")
					sys.stdout.write("Sorry! That's not a SET.")
					sys.stdout.flush()
					time.sleep(2)

	def set_high_score(self, name, score):
		# save to a file the score and name
		home = expanduser("~")
		file_path = os.path.join(home, '.setgame')
		with open(file_path, 'w') as f:
			f.write(str(name)+","+str(score))

	def get_high_score(self):
		home = expanduser("~")
		file_path = os.path.join(home, '.setgame')
		exists = os.path.isfile(file_path)
		high_score = -1
		name = None
		if exists:
			with open(file_path, 'r') as f:
				value = f.read()
			name, high_score = value.split(',')[0].strip(), int(value.split(',')[1].strip())
		return (name, high_score)

	def display_cards(self):
		"""
			outputs to the user the cards in self.current_cards
		"""
		os.system('cls' if os.name == 'nt' else 'clear')
		self.display_banner()
		print('Score', self.score)
		current = [str(i) for i in self.current_cards]
		print('--------------')
		for i in range(len(current)):
			print('{:^{}}'.format(i, 4) + '* {:^{}} *'.format(current[i], 5))
			print('--------------')


	def is_set(self, x, y, z):
		x = int(x)
		y = int(y)
		z = int(z)
		val = False
		val_x = self.current_cards[x].value
		val_y = self.current_cards[y].value
		val_z = self.current_cards[z].value

		size = False
		size_x = self.current_cards[x].size
		size_y = self.current_cards[y].size
		size_z = self.current_cards[z].size

		shape = False
		shape_x = self.current_cards[x].shape
		shape_y = self.current_cards[y].shape
		shape_z = self.current_cards[z].shape

		if (val_x == val_y == val_z) or (val_x != val_y != val_z):
			val = True
		if (size_x == size_y == size_z) or (size_x != size_y != size_z):
			size = True
		if (shape_x == shape_y == shape_z) or (shape_x != shape_y != shape_z):
			shape = True

		if val and size and shape:
			return True

	def display_banner(self):
    # Clears the terminal screen, and displays a title bar.
	    os.system('cls' if os.name == 'nt' else 'clear') #cls for window and clear for Linux/Mac
	              
	    print("\t**********************************************")
	    print("\t***              Game of SET               ***")
	    print("\t**********************************************")


	def get_instructions(self):
		print("Welcome to SET!\n")
		print("There are five basic rules.\n")
		print("1. Identify as many SETs as possible in the given time.")
		print("2. There are three features - shape (the type of the card), value (the number in the card, and size (the length of the card).")
		print("3. A SET consists three cards in which each feature is either the same on each card or is different on each card.")
		print("4. If you find a SET, enter the indexes of the three cards, separating each index with a space.")
		print("5. If you can't find a SET in the given 12 cards, enter A for the dealer to generate three additional cards.\n")

	def remove_cards(self, indicies):
		new = []
		for i, ele in enumerate(self.current_cards):
			if i not in indicies:
				new.append(ele)
		self.current_cards = new

if __name__ == '__main__':
	# d = Deck()
	# cards = d.generate_cards()
	# print(len(d.available_cards))

	s = Game()
	start = s.start()

	# d = Deck()
	# cards = d.generate_cards()
	# result = [str(i) for i in cards]
	# print(result)
	# print(str(d.get_cards(1)[0]))
	# print(result)
