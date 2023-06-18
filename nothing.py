import tkinter as tk
from tkinter import ttk

def start_animation():
    global progressbar
    progressbar.start()

def stop_animation():
    global progressbar
    progressbar.stop()

def create_gui():
    global progressbar
    root = tk.Tk()
    root.title("Animated GUI")

    # Create a ttk.Progressbar widget
    progressbar = ttk.Progressbar(root, mode="indeterminate")
    progressbar.pack(pady=20)

    # Create buttons to start and stop the animation
    start_button = ttk.Button(root, text="Start Animation", command=start_animation)
    start_button.pack(pady=10)

    stop_button = ttk.Button(root, text="Stop Animation", command=stop_animation)
    stop_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()