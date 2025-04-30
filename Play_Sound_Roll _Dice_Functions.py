def play_sound(sound_path):
    if SOUND_ENABLED:
        try:
            playsound(sound_path)
        except:
            pass  # Ignore sound errors silently

def roll_dice():
    result = random.randint(1, 6)
    dice_label.config(text=DICE_UNICODE[result - 1], font=("Arial", 100))
    message_label.config(text=MESSAGES[result])

    if SOUND_ENABLED:
        threading.Thread(target=lambda: play_sound(ROLL_SOUND)).start()
        threading.Thread(target=lambda: play_sound(JINGLE_SOUND)).start()
