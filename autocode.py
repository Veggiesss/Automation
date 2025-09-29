#This script automates the redeem code process (Mainly used when redeeming large quantities of code for a roblox game)
#Enter the script in the format "code1 code2 code3", press [ to run, this does require you to manually press [ for each code due to how roblox redeem system works
#Created on September 14, 2025



import pyautogui
import keyboard
import time

# Ask for input and split into array
user_input = input("Enter your string: ")
strings = user_input.split()

print("Press [ to type the next string. Press ESC to quit.")

index = 0

def handle_bracket(e):
    global index
    if index < len(strings):
        # Click mouse
        pyautogui.click()

        # Type the string
        pyautogui.typewrite(strings[index])

        # Press Enter
        pyautogui.press("enter")

        index += 1
    else:
        print("All strings have been used!")

# Bind the [ key (suppress=True prevents it from appearing)
keyboard.on_press_key("[", handle_bracket, suppress=True)

# Keep script alive until ESC
keyboard.wait("esc")
print("Exiting...")
