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
os.makedirs(folder_path, exist_ok=True)
csv_file = os.path.join(folder_path, "Personal Information.csv")
if not os.path.isfile(csv_file):
        with open(csv_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Title", "Phone", "Email", "Company Name", "Company Address"])
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
    
    #  Create a PhotoImage object from the QR code image
    # qr_code_image = Image.open(filename)
    # qr_code_image = ImageTk.PhotoImage(qr_code_image)

    # Update the qr_label with the new QR code image
    # qr_label.config(image=qr_code_image)
    # qr_label.image = qr_code_image  # Keep a reference to the image to prevent it from being garbage collected
    
    logo = Image.open(r"D:\Python project\QR-Code\eagle-logo.jpg")  # Replace with the path to your logo image
    logo = logo.resize((60, 60))  # Adjust the size as needed

    # Calculate the position to paste the logo in the center
    qr_width, qr_height = qr_code_img.size
    logo_width, logo_height = logo.size
    position = ((qr_width - logo_width) // 2, (qr_height - logo_height) // 2)

    # Paste the logo onto the QR code
    qr_code_img.paste(logo, position)
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
    folder_path = fr'{pictures_folder}\qrcode_folder\Personal Information'

    filename = f'{person_details["first_name"]}.png'
    qr_code_filename = os.path.join(folder_path, filename)

    # Read the existing CSV file to check if the person's name and phone are already present
    csv_file = os.path.join(folder_path, "Personal Information.csv")
    person_exists = False

    # Keep track of the index of the existing entry for updating
    existing_entry_index = None

    with open(csv_file, mode="r", newline="") as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if row and row[0].lower() == person_name.lower() and row[2] == person_phone:
                person_exists = True
                existing_entry_index = i
                break

    if person_exists:
        # Update the existing entry in the CSV file
        with open(csv_file, mode="r", newline="") as file:
            lines = file.readlines()
            lines[existing_entry_index] = [
                person_details["first_name"], person_details["title"], person_details["phone"], person_details["email"],
                company_info["name"], company_info["address"]
            ]

        with open(csv_file, mode="w", newline="") as file:
            file.writelines(lines)

        # Regenerate the QR code
        qr_code_filename = generate_vcard_qrcode(person_details, company_info, latitude, longitude, folder_path)
        result_label.config(text='CSV and QR Code updated!')
        spt.config(text=f"Photo Path : {qr_code_filename}")

    else:
    # Find the row with the existing person's details
        existing_row = None
    with open(csv_file, mode="r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0].lower() == person_name.lower() and row[2] == person_phone:
                existing_row = row
                break

    if existing_row:
        # Update the CSV file with the new details
        existing_row[1] = person_details["title"]
        existing_row[3] = person_details["email"]
        existing_row[4] = company_info["name"]
        existing_row[5] = company_info["address"]

        with open(csv_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Title", "Phone", "Email", "Company Name", "Company Address"])  # Write header
            writer.writerows(existing_row for existing_row in existing_row if existing_row)

        # Generate a new QR code
        qr_code_filename = generate_vcard_qrcode(person_details, company_info, latitude, longitude, folder_path)
        result_label.config(text='CSV and QR Code updated!')
        spt.config(text=f"Photo Path : {qr_code_filename}")
    else:
        # Write a new entry to the CSV file
        with open(csv_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([person_details["first_name"], person_details["title"], person_details["phone"], person_details["email"],
                            company_info["name"], company_info["address"]])

        # Generate a new QR code
        qr_code_filename = generate_vcard_qrcode(person_details, company_info, latitude, longitude, folder_path)
        result_label.config(text='QR Code generated!')
        spt.config(text=f"Photo Path : {qr_code_filename}")


    # Clear the text entry widgets
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    title_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    company_name_entry.delete(0, tk.END)
    company_address_entry.delete(0, tk.END)


# def view_qr_code():
#     person_name = name_entry.get().title()
#     qr_code_filename = os.path.join(folder_path, f'{person_name}.png')

#     if os.path.exists(qr_code_filename):
#         qr_image = ImageTk.PhotoImage(Image.open(qr_code_filename))
#         qr_label.configure(image=qr_image)
#         qr_label.image = qr_image
#     else:
#         result_label.config(text='QR Code does not exist!')
#     spt.config(text=f"Photo Path : {qr_code_filename}")

# def update_qr_code():
#     person_name = name_entry.get().title()
#     qr_code_filename = os.path.join(folder_path, f'{person_name}.png')
#     os.replace(qr_code_filename,qr_code_filename)
#     if os.path.exists(qr_code_filename):
        
#         qr_image = ImageTk.PhotoImage(Image.open(qr_code_filename))
#         qr_label.configure(image=qr_image)
#         qr_label.image = qr_image
#         # Check if the person's name already exists in the CSV file
        
#     else:
#         result_label.config(text='QR Code does not exist!')
#         return
# Create the main window
window = tk.Tk()
window.title("QR Code Generator")
window.iconbitmap(r"D:\Python project\QR-Code\1.ico")
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
spt.grid(row=9, column=0, columnspan=2, padx=5, pady=5)
qr_label = ttk.Label(window)
qr_label.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

# view_qr_code_button = ttk.Button(window, text="View QR Code", command=view_qr_code)
# view_qr_code_button.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

# # Create the "Update QR Code" button
# update_button = ttk.Button(window, text="Update QR Code", command=update_qr_code)
# update_button.grid(row=11, column=0, columnspan=2, padx=5, pady=5)

# Run the main event loop
window.mainloop()
