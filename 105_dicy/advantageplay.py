#!/usr/bin/python3
"""RZFeeser | Alta3 Research
   Player - Class model
   Cheat_Swapper(Player) - Subclass model
   Cheat_Loaded_Dice(Player) - Subclass model"""

# standard library
from random import randint
import time
import keyboard

class Player:
    def __init__(self):
        self.dice = []

    def roll(self):
        self.dice = [] # clears current dice
        for i in range(3):  # make 3 rolls
            self.dice.append(randint(1,6))   # 1 to 6 inclusive

    def get_dice(self): # returns the dice rolls
        return self.dice

# allows user to turn their last roll into a 6
class Cheat_Swapper(Player):  # inheritance of Player
    def cheat(self):
        self.dice[-1] = 6

# allows user to increase all rolls if they were less than a 6
class Cheat_Loaded_Dice(Player): # inheritance of Player
    def cheat(self):
        i = 0
        while i < len(self.dice):
            if self.dice[i] < 6:
                self.dice[i] += 1
            i += 1
class mulligan(Player):
    def reroll(self):
        if sum(self.dice) <9:
            self.dice=[]
        self.dice.extend(map(lambda _: randint(1, 6), range(3)))

class noisy(Player):
    def rickroll(self):
        lyrics = [
            "[Intro]",
			"Desert you",
			"Ooh-ooh-ooh-ooh",
			"Hurt you",
			"",
			"[Verse 1]",
			"We're no strangers to love",
			"You know the rules and so do I (Do I)",
			"A full commitment's what I'm thinking of",
			"You wouldn't get this from any other guy",
			"",
			"[Pre-Chorus]",
			"I just wanna tell you how I'm feeling",
			"Gotta make you understand",
			"",
			"[Chorus]",
			"Never gonna give you up",
			"Never gonna let you down",
			"Never gonna run around and desert you",
			"Never gonna make you cry",
			"Never gonna say goodbye",
			"Never gonna tell a lie and hurt you",
			"",
			"[Verse 2]",
			"We've known each other for so long",
			"Your heart's been aching, but you're too shy to say it (To say it)",
			"Inside, we both know what's been going on (Going on)",
			"We know the game, and we're gonna play it",
			"See Rick Astley Live",
			"Get tickets as low as $45",
			"You might also like",
			"ILLEGALS IN MY YARD",
			"The Fox and Rice Experience",
			"A&W",
			"Lana Del Rey",
			"Area Codes",
			"Kaliii",
			"[Pre-Chorus]",
			"And if you ask me how I'm feeling",
			"Don't tell me you're too blind to see",
			"",
			"[Chorus]",
			"Never gonna give you up",
			"Never gonna let you down",
			"Never gonna run around and desert you",
			"Never gonna make you cry",
			"Never gonna say goodbye",
			"Never gonna tell a lie and hurt you",
			"Never gonna give you up",
			"Never gonna let you down",
			"Never gonna run around and desert you",
			"Never gonna make you cry",
			"Never gonna say goodbye",
			"Never gonna tell a lie and hurt you",
			"",
			"[Post-Chorus]",
			"Ooh (Give you up)",
			"Ooh-ooh (Give you up)",
			"Ooh-ooh",
			"Never gonna give, never gonna give (Give you up)",
			"Ooh-ooh",
			"Never gonna give, never gonna give (Give you up)",
			"[Bridge]",
			"We've known each other for so long",
			"Your heart's been aching, but you're too shy to say it (To say it)",
			"Inside, we both know what's been going on (Going on)",
			"We know the game, and we're gonna play it",
			"",
			"[Pre-Chorus]",
			"I just wanna tell you how I'm feeling",
			"Gotta make you understand",
			"",
			"[Chorus]",
			"Never gonna give you up",
			"Never gonna let you down",
			"Never gonna run around and desert you",
			"Never gonna make you cry",
			"Never gonna say goodbye",
			"Never gonna tell a lie and hurt you",
			"Never gonna give you up",
			"Never gonna let you down",
			"Never gonna run around and desert you",
			"Never gonna make you cry",
			"Never gonna say goodbye",
			"Never gonna tell a lie and hurt you",
			"Never gonna give you up",
			"Never gonna let you down",
			"Never gonna run around and desert you",
			"Never gonna make you cry",
			"Never gonna say goodbye",
			"Never gonna tell a lie and hurt you"
                ]
        while sum(self.dice)%2==0:
            for verse in lyrics:
                print(verse)
                time.sleep(1.5)
                if keyboard.is_pressed('r'):
                    print("Sorry I just got even")
                    break


