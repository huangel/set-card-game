Rules:
The objective of the game is to identify a 'set' of three cards from 12 cards laid out on the table. Each card has a variation of the following three features:

(A) Shape: Shape is identified using the type of the card, i.e./ a list, a tuple, or a set
(B) Value: Value is represented by the number in the card, either 0, 1, or 2
(C) Size: Size is shown through the length of the card, ranging from 1 to 3. 

A 'SET' consists of three cards in which each feature is EITHER the same on each card OR is different on each card. To put it in simpler terms, any feature in the 'SET' of three cards is either common to all three cards or is different on each card. Within the given time, identify as many SETs as possible. 

The play
The dealer/computer generates and shows 12 cards. They player remove a 'SET' of three cards as he/she sees it. Each 'SET' is checked by the computer. If correct, the 'SET' is replaced by three new cards from the deck and the score increases by 1. If the player can't find a 'SET' in the twelve cards showing, three more cards (making a total of fifteen) are laid face up, which won't be replaced when the next 'SET' is picked up, making the number of cards back to twelve again. 

The game ends after 45 seconds. The highest score played on the laptop is saved as a hidden file .setgame. Only the highest score will be saved. 


Running the code: 
Please ensure the following library is installed on your laptop. All other imported libraries should pre-exist already. 
Pynput (pip install pynput)

In the console/terminal, please use 'cd' to go into the folder where the SET Game.py is located in. Run the code by sending the command line 'python SET Game.py' (python can be replaced by python3 depending on the python version). 

If the player wishes to delete the highest score record, please type in 'rm ~/.setgame' in the terminal/console and delete the .setgame file. 

Design Choice: 
The program is divided into four classes to keep a proper, organized structure: TimeApp, Card, Deck, and Game. TimeApp creates a popup through Tkinter, showing the countdown timer. Card initializes the structure and display of the cards. Deck initializes the playing deck of the game. Game initializes and starts the game! 
I decided to go with Python because it is a good general-purpose language and has a more straightforward implementation of threading, which is needed to run both a countdown timer and the game itself. 
The SET_test.py file tests all of the basic simple functions in the SET_Game.py program by utilizing unittesting, isolating every individual function. After basic functions passed the test cases successfully, the game itself was tested several times to ensure that there are no bugs while playing the game in the console. Seeing as the maximum number of cards is 27, a special, efficient algorithm wasn't implemented since efficiency isn't a problem here. 