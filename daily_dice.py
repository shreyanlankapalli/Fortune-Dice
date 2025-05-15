import tkinter as tk
import random
import threading
import pygame
import time

# --- Sound Setup ---
pygame.mixer.init()

class SoundPlayer:
    def __init__(self):
        self.roll_sound = pygame.mixer.Sound("roll.wav")
        self.jingle_sound = pygame.mixer.Sound("jingle.wav")

    def play_roll(self):
        self.roll_sound.play()

    def play_jingle(self):
        self.jingle_sound.play()

# --- Message Logic ---
class MessageGenerator:
    def __init__(self):
        self.messages = {
            1: "Try again tomorrow!",
            2: "Stay focused!",
            3: "You’re doing great!",
            4: "Keep it up!",
            5: "Almost there!",
            6: "You’re lucky today!"
        }

    def get_message(self, roll):
        return self.messages.get(roll, "No message.")

# --- Math & Stats ---
class DiceMath:
    def __init__(self):
        self.total_rolls = 0
        self.roll_history = []

    def update_stats(self, roll):
        self.total_rolls += 1
        self.roll_history.append(roll)

    def get_average(self):
        if self.total_rolls == 0:
            return 0
        return sum(self.roll_history) / self.total_rolls

# --- Dice Object ---
class Dice:
    def roll(self):
        return random.randint(1, 6)

# --- GUI Management ---
class DiceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DailyDice Roller")

        self.dice = Dice()
        self.math = DiceMath()
        self.messages = MessageGenerator()
        self.sound = SoundPlayer()

        self.label = tk.Label(root, text="Click to Roll!", font=("Helvetica", 20))
        self.label.pack(pady=20)

        self.roll_button = tk.Button(root, text="Roll Dice", font=("Helvetica", 18), command=self.roll_dice)
        self.roll_button.pack(pady=10)

        self.message_box = tk.Label(root, text="", font=("Helvetica", 16), fg="blue")
        self.message_box.pack(pady=10)

        self.stats_box = tk.Label(root, text="", font=("Helvetica", 12), fg="green")
        self.stats_box.pack(pady=5)

    def roll_dice(self):
        self.sound.play_roll()
        time.sleep(0.5)  # slight delay before message
        roll = self.dice.roll()
        self.sound.play_jingle()

        message = self.messages.get_message(roll)
        self.math.update_stats(roll)

        self.label.config(text=f"You rolled a {roll}")
        self.message_box.config(text=message)
        avg = self.math.get_average()
        self.stats_box.config(text=f"Total Rolls: {self.math.total_rolls} | Average: {avg:.2f}")

# --- Main Program ---
class DailyDiceApp:
    def __init__(self):
        self.root = tk.Tk()
        self.gui = DiceGUI(self.root)

    def run(self):
        self.root.mainloop()

try:
    from playsound import playsound
    SOUND_ENABLED = True
except ImportError:
    SOUND_ENABLED = False
# Run the app
if __name__ == "__main__":
    app = DailyDiceApp()
    app.run()