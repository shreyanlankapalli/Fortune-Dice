import tkinter as tk
import random
import pygame
import time
import os
import wave
import struct
from PIL import Image, ImageTk  # for background image

# --- Sound Setup ---
pygame.mixer.init(frequency=44100, size=-16, channels=1)

#I used ai to fix an error in this part 
def create_silent_wav(filename, duration_ms=500):
    if os.path.exists(filename):
        return
    with wave.open(filename, 'w') as f:
        nchannels = 1
        sampwidth = 2
        framerate = 44100
        nframes = int(framerate * duration_ms / 1000)
        comptype = "NONE"
        compname = "not compressed"
        f.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
        silence = [0] * nframes
        frames = struct.pack('<' + ('h' * len(silence)), *silence)
        f.writeframes(frames)

# Create fallback silent sounds
create_silent_wav("roll.wav")
create_silent_wav("jingle.wav")

class SoundPlayer:
    def __init__(self):
        self.roll_sound = pygame.mixer.Sound("roll.wav")
        self.jingle_sound = pygame.mixer.Sound("jingle.wav")
        self.roll_sound.set_volume(1.0)
        self.jingle_sound.set_volume(1.0)

    def play_roll(self):
        self.roll_sound.play()

    def play_jingle(self):
        self.jingle_sound.play()

# --- Message Logic ---
class MessageGenerator:
    def __init__(self):
        self.messages = {
            1: "you're gonna have the best day ever!",
            2: "Stay focused!",
            3: "You’re doing great!",
            4: "Keep up the good work!",
            5: "you'll ace today !",
            6: "You’re lucky today!"
        }

    def get_message(self, roll):
        return self.messages.get(roll, "No message.")

# --- Math & Stats ---
# I used ai to set the math and aihelped me to fix it
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
        self.root.geometry("800x600")

        # Background Image Setup
        bg_img = Image.open("background.png").resize((800, 600))
        self.bg_image = ImageTk.PhotoImage(bg_img)
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Game Logic Setup
        self.dice = Dice()
        self.math = DiceMath()
        self.messages = MessageGenerator()
        self.sound = SoundPlayer()

        # Widgets
        self.label = tk.Label(root, text="Click to Roll!", font=("Helvetica", 20), bg="white")
        self.roll_button = tk.Button(root, text="Roll Dice", font=("Helvetica", 18), command=self.roll_dice)
        self.message_box = tk.Label(root, text="", font=("Helvetica", 16), fg="blue", bg="white")
        self.stats_box = tk.Label(root, text="", font=("Helvetica", 12), fg="green", bg="white")

        # Place widgets on canvas
        self.canvas.create_window(400, 100, window=self.label)
        self.canvas.create_window(400, 180, window=self.roll_button)
        self.canvas.create_window(400, 260, window=self.message_box)
        self.canvas.create_window(400, 310, window=self.stats_box)

    def roll_dice(self):
        self.sound.play_roll()
        self.roll_button.config(state="disabled")
        self.root.after(500, self.finish_roll)

    def finish_roll(self):
        roll = self.dice.roll()
        self.sound.play_jingle()
        message = self.messages.get_message(roll)
        self.math.update_stats(roll)

        self.label.config(text=f"You rolled a {roll}")
        self.message_box.config(text=message)
        avg = self.math.get_average()
        self.stats_box.config(text=f"Total Rolls: {self.math.total_rolls} | Average: {avg:.2f}")
        self.roll_button.config(state="normal")

# --- Main Program ---
class DailyDiceApp:
    def __init__(self):
        self.root = tk.Tk()
        self.gui = DiceGUI(self.root)

    def run(self):
        self.root.mainloop()

# Run the app
if __name__ == "__main__":
    app = DailyDiceApp()
    app.run()
