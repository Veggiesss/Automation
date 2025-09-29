#Auto mouse holder, intervals are customizable. Holds left click
#Made for AFK in games
#Made on September 26, 2025


from pynput import mouse, keyboard
from pynput.mouse import Controller, Button
import time
import threading

mouse_controller = Controller()
running = False
duration = None

def long_press_loop():
    global running
    while running:
        mouse_controller.press(Button.left)
        time.sleep(duration)
        mouse_controller.release(Button.left)
        time.sleep(0.1)  # tiny delay before next cycle

def on_press(key):
    global running
    if key == keyboard.KeyCode.from_char('['):
        if not running:
            running = True
            print("Started long press loop.")
            threading.Thread(target=long_press_loop, daemon=True).start()
    elif key == keyboard.KeyCode.from_char(']'):
        if running:
            running = False
            print("Stopped long press loop.")

if __name__ == "__main__":
    try:
        duration = float(input("Enter hold time in seconds: "))
    except ValueError:
        print("Please enter a valid number.")
        exit(1)

    print("Press [ to start, ] to stop. Press ESC to quit.")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
