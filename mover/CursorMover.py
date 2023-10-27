import tkinter as tk
from tkinter import ttk
import pyautogui
import math
import threading

# Flag to control the cursor movement loop
stop_cursor_movement = False


def on_escape(event):
    global stop_cursor_movement
    stop_cursor_movement = True


def move_cursor_in_circle():
    global stop_cursor_movement
    stop_cursor_movement = False

    # Get the screen size
    screen_width, screen_height = pyautogui.size()

    # Initial position (center of the screen)
    x, y = screen_width // 2, screen_height // 2

    # Radius of the circle
    radius = 100

    # Start the angle at 0
    angle = 0

    while not stop_cursor_movement:
        # Calculate the new cursor position
        new_x = int(x + radius * math.cos(math.radians(angle)))
        new_y = int(y + radius * math.sin(math.radians(angle)))

        # Move the cursor
        pyautogui.moveTo(new_x, new_y)

        # Increase the angle
        angle += 1
        if angle > 360:
            angle = 0

        # Small delay
        pyautogui.sleep(0.01)


def start_cursor_movement():
    threading.Thread(target=move_cursor_in_circle).start()


# Initialize Tkinter window
root = tk.Tk()
root.title("Cursor Mover")
root.geometry("200x200")

# Add button to start cursor movement
start_button = ttk.Button(root, text="Start", command=start_cursor_movement)
start_button.grid(row=0, columnspan=2)

# Bind the 'Esc' key to stop the cursor movement
root.bind('<Escape>', on_escape)

root.mainloop()
