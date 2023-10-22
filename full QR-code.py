import qrcode
import os
from PIL import Image
import pyfiglet
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import re
import subprocess

# ... (The rest of your code remains the same)

# Function to open the new window
def open_new_window():
    subprocess.call(["python", r"D:\Python project\QR-Code\QR-Code_with_GUI.py"])

def open_second_window():
    subprocess.call(["python", r"D:\Python project\QR-Code\website url.py"])
window = tk.Tk()
window.title("QR Code Generator")
# Create a button to open the new window
open_new_button = tk.Button(window, text="Personal Information", command=open_new_window)
open_new_button.grid(row=8, column=0, columnspan=2, padx=5, pady=5)
open_second_button = tk.Button(window, text="Website URL", command=open_second_window)
open_second_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5)
# Run the main event loop
window.mainloop()
