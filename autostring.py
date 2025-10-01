#A simpler version of autocode.py, it prints out a string each time [ is pressed, the string is defined by the user
#Made on September 12, 2025


import keyboard

# Ask the user for the string to type
text_to_type = input("Enter the string you want to type when [ is pressed: ")

def type_string(e):
    # Suppress the [ key and type the string instead
    keyboard.write(text_to_type)

# Bind "[" with suppression
keyboard.on_press_key("[", type_string, suppress=True)

print("Press [ to type the string (without typing [). Press ESC to quit.")
keyboard.wait("esc")
