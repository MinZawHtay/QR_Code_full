import qrcode
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pathlib import Path
import os

pictures_folder = Path.home() / "Pictures"
folder_path = fr'{pictures_folder}\qrcode_folder\wbsite_url'
count = 0  # Initialize the count

def generate_qr_code():
    global count  # Use the global count variable
    website_url = website_url_entry.get()
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(website_url)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")

    qr_image = qr_image.resize((300, 300))
    tk_qr_image = ImageTk.PhotoImage(qr_image)

    qr_label.config(image=tk_qr_image)
    qr_label.image = tk_qr_image

    count += 1
    os.makedirs(folder_path, exist_ok=True)
    filename = f"website_{count}.png"  # Use an underscore between "website" and the count
    qr_code_filename = os.path.join(folder_path, filename)
    qr_image.save(qr_code_filename)

    spt.config(text=f"Photo Path : {folder_path}")

    website_url_entry.delete(0, tk.END)

app = tk.Tk()
app.title("QR Code Generator")

website_url_label = tk.Label(app, text="Website URL:")
website_url_label.pack()
website_url_entry = tk.Entry(app)
website_url_entry.pack()

generate_button = tk.Button(app, text="Generate QR Code", command=generate_qr_code)
generate_button.pack()

qr_label = tk.Label(app)
qr_label.pack()
spt = tk.Label(app, text="")
spt.pack()
app.mainloop()
