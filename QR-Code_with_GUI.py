import qrcode
import os
from PIL import Image,  ImageTk
import pyfiglet
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox, ttk
import re
import csv
pictures_folder = Path.home() / "Pictures"
folder_path = fr'{pictures_folder}\qrcode_folder\Personal Information'
def generate_vcard_qrcode(person_details, company_info, latitude, longitude, filename):
    vcard_data = f"BEGIN:VCARD\n" \
                 f"VERSION:3.0\n" \
                 f"N:{person_details['first_name']}\n" \
                 f"ORG:{company_info['name']}\n" \
                 f"TEL;TYPE=work,voice:{person_details['phone']}\n" \
                 f"ADR;TYPE=work:;;{company_info['address']}\n" \
                 f"EMAIL:{person_details['email']}\n" \
                 f"TITLE:{person_details['title']}\n" \
                 f"END:VCARD"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(vcard_data)
    qr.make(fit=True)
    qr_code_img = qr.make_image(fill_color='black', back_color="white")
    qr_code_img = qr_code_img.resize((300, 300))  # Resize the image
    tk_qr_image = ImageTk.PhotoImage(qr_code_img)
    
    qr_label.config(image=tk_qr_image)
    qr_label.image = tk_qr_image

    os.makedirs(folder_path, exist_ok=True)
    filename = os.path.join(folder_path, f'{person_details["first_name"]}.png')
    qr_code_img.save(filename)
    return filename

def generate_qr_code():
    person_name = name_entry.get().title()
    person_phone = str(phone_entry.get())
    title = title_entry.get()
    email = email_entry.get().lower()
    if "@" not in email:
        email = email + "@gmail.com"

    person_details = {
        'first_name': person_name,
        'title': title,
        'phone': person_phone,
        'email': email
    }

    company_name = company_name_entry.get()
    if company_name == "":
        company_name = "Regis International Co, LTD."

    company_address = company_address_entry.get()
    if company_address == "":
        company_address = "Building A, Union Financial Centre, 07-01"

    company_info = {
        'name': company_name,
        'address': company_address
    }

    latitude = 16.774722  # Example latitude (decimal format)
    longitude = 96.167667
    pictures_folder = Path.home() / "Pictures"
    folder_path = fr'{pictures_folder}\qrcode_folder'

    filename = f'{person_details["first_name"]}.png'
    qr_code_filename = os.path.join(folder_path, filename)

    

    # Check if the QR code with the same name already exists
    if os.path.exists(qr_code_filename):
        answer = tk.messagebox.askquestion("QR Code Exists", "Do you want to replace your QR code?")
        if answer == 'yes':
            os.replace(qr_code_filename,qr_code_filename)
        else:
            result_label.config(text='Enter another name!')
            return
    # Save person_details and company_info to a CSV file
    csv_file = os.path.join(folder_path, "Personal Information.csv")
    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([person_details["first_name"], person_details["title"], person_details["phone"], person_details["email"],
                         company_info["name"], company_info["address"]])
  
    qr_code_filename = generate_vcard_qrcode(person_details, company_info, latitude, longitude, folder_path)
    result_label.config(text='QR Code generated!')
    spt.config(text=f"Photo Path : {qr_code_filename}")
    # image = Image.open(qr_code_filename)
    # image.show()

    # Clear the text entry widgets
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    title_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    company_name_entry.delete(0, tk.END)
    company_address_entry.delete(0, tk.END)

# Create the main window
window = tk.Tk()
window.title("QR Code Generator")

# Create the input fields
name_label = tk.Label(window, text="Name:")
name_entry = tk.Entry(window)
name_label.grid(row=0, column=0, padx=5, pady=5)
name_entry.grid(row=0, column=1, padx=5, pady=5)

phone_label = tk.Label(window, text="Phone:")
phone_entry = tk.Entry(window)
phone_label.grid(row=1, column=0, padx=5, pady=5)
phone_entry.grid(row=1, column=1, padx=5, pady=5)

title_label = tk.Label(window, text="Title:")
title_entry = tk.Entry(window)
title_label.grid(row=2, column=0, padx=5, pady=5)
title_entry.grid(row=2, column=1, padx=5, pady=5)

email_label = tk.Label(window, text="Email:")
email_entry = tk.Entry(window)
email_label.grid(row=3, column=0, padx=5, pady=5)
email_entry.grid(row=3, column=1, padx=5, pady=5)

company_name_label = tk.Label(window, text="Company Name:")
company_name_entry = tk.Entry(window)
company_name_label.grid(row=4, column=0, padx=5, pady=5)
company_name_entry.grid(row=4, column=1, padx=5, pady=5)

company_address_label = tk.Label(window, text="Company Address:")
company_address_entry = tk.Entry(window)
company_address_label.grid(row=5, column=0, padx=5, pady=5)
company_address_entry.grid(row=5, column=1, padx=5, pady=5)

# Create the generate button
generate_button = tk.Button(window, text="Generate QR Code", command=generate_qr_code)
generate_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Create the result label
result_label = tk.Label(window, text="")
result_label.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

spt= tk.Label(window, text="")
spt.grid(row=8, column=0, columnspan=2, padx=5, pady=5)
qr_label = ttk.Label(window)
qr_label.grid(row=9, column=0, columnspan=2, padx=5, pady=5)
# Run the main event loop
window.mainloop()