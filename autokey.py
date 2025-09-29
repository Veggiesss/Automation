#Auto key presser, mouse clicker. Can set custom intervals and is capable of performing multiple actions at once
#Made to AFK in grinding games
#Made on August 3, 2025


from pynput import keyboard, mouse
from pynput.keyboard import Controller as KeyController, Key
from pynput.mouse import Controller as MouseController, Button
import threading
import time

keyboard_controller = KeyController()
mouse_controller = MouseController()

running = False
threads = []
actions = []  # list of (function, description)


# --------------------------
# Action definitions
# --------------------------

def keyboard_action(key_name, interval):
    def loop():
        global running
        print(f"Keyboard: pressing '{key_name}' every {interval} seconds...")
        while running:
            try:
                if hasattr(Key, key_name):  # special keys like 'enter', 'shift'
                    k = getattr(Key, key_name)
                else:
                    k = key_name
                keyboard_controller.press(k)
                keyboard_controller.release(k)
            except Exception as e:
                print(f"Error pressing key {key_name}: {e}")
            time.sleep(interval)
    return loop


def mouse_click_action(button, interval):
    btn = Button.left if button == "l" else Button.right if button == "r" else Button.middle

    def loop():
        global running
        print(f"Mouse: clicking {button}-button every {interval} seconds...")
        while running:
            mouse_controller.click(btn)
            time.sleep(interval)
    return loop


def mouse_hold_action(button, hold_time):
    btn = Button.left if button == "l" else Button.right if button == "r" else Button.middle

    def loop():
        global running
        print(f"Mouse: holding {button}-button for {hold_time} seconds repeatedly...")
        while running:
            mouse_controller.press(btn)
            time.sleep(hold_time)
            mouse_controller.release(btn)
            time.sleep(0.2)
    return loop


def mouse_scroll_action(dx, dy, interval):
    def loop():
        global running
        print(f"Mouse: scrolling ({dx}, {dy}) every {interval} seconds...")
        while running:
            mouse_controller.scroll(dx, dy)
            time.sleep(interval)
    return loop


def mouse_move_action(mode, interval, x=None, y=None, dx=None, dy=None):
    def loop():
        global running
        if mode == "a":
            print(f"Mouse: moving to absolute ({x}, {y}) every {interval} seconds...")
            while running:
                mouse_controller.position = (x, y)
                time.sleep(interval)
        else:
            print(f"Mouse: moving relative ({dx}, {dy}) every {interval} seconds...")
            while running:
                cx, cy = mouse_controller.position
                mouse_controller.position = (cx + dx, cy + dy)
                time.sleep(interval)
    return loop


# --------------------------
# Setup input process
# --------------------------

while True:
    print("\nSetup Menu:")
    print("1 = Add keyboard action")
    print("2 = Add mouse action")
    print("3 = Done (finish setup)")
    choice = input("Choose option: ").strip()

    if choice == "1":
        key_name = input("Enter the key (example: a, 1, enter, space, shift, f5, left, right): ").strip().lower()
        interval = float(input("Interval between presses (seconds): "))
        actions.append(keyboard_action(key_name, interval))

    elif choice == "2":
        print("Mouse actions:")
        print("1 = Click")
        print("2 = Hold")
        print("3 = Scroll")
        print("4 = Move")
        m_choice = input("Choose mouse action: ").strip()

        if m_choice == "1":
            button = input("Button? (l)eft / (r)ight / (m)iddle: ").strip().lower()
            interval = float(input("Click interval (seconds): "))
            actions.append(mouse_click_action(button, interval))

        elif m_choice == "2":
            button = input("Button? (l/r/m): ").strip().lower()
            hold_time = float(input("Hold duration (seconds): "))
            actions.append(mouse_hold_action(button, hold_time))

        elif m_choice == "3":
            dx = int(input("Scroll horizontally (negative = left): "))
            dy = int(input("Scroll vertically (negative = down): "))
            interval = float(input("Scroll interval (seconds): "))
            actions.append(mouse_scroll_action(dx, dy, interval))

        elif m_choice == "4":
            move_type = input("Move type? (a)bsolute / (r)elative: ").strip().lower()
            interval = float(input("Move interval (seconds): "))
            if move_type == "a":
                x = int(input("Absolute X: "))
                y = int(input("Absolute Y: "))
                actions.append(mouse_move_action("a", interval, x=x, y=y))
            else:
                dx = int(input("Relative ΔX: "))
                dy = int(input("Relative ΔY: "))
                actions.append(mouse_move_action("r", interval, dx=dx, dy=dy))

    elif choice == "3":
        break

    else:
        print("Invalid choice, try again.")


# --------------------------
# Listener for Start/Stop
# --------------------------

def on_press(key):
    global running, threads
    try:
        # Check for regular characters
        if key.char == ']':  # Start
            if not running:
                running = True
                threads = []
                print("Starting actions...")
                for action in actions:
                    t = threading.Thread(target=action)
                    t.start()
                    threads.append(t)
        elif key.char == '[':  # Stop
            if running:
                running = False
                print("Stopping actions...")
    except AttributeError:
        # Check for special keys
        if key == Key.page_down:  # Start
            if not running:
                running = True
                threads = []
                print("Starting actions...")
                for action in actions:
                    t = threading.Thread(target=action)
                    t.start()
                    threads.append(t)
        elif key == Key.page_up:  # Stop
            if running:
                running = False
                print("Stopping actions...")


with keyboard.Listener(on_press=on_press) as listener:
    print("\nPress ']' or 'Page Down' to start all actions. Press '[' or 'Page Up' to stop.")
    listener.join()