# daily_dice.py

import tkinter as tk
import random
import threading

try:
    from playsound import playsound
    SOUND_ENABLED = True
except ImportError:
    SOUND_ENABLED = False
