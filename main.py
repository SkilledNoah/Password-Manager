"""
---------------------------------------
    * Course: 100 Days of Code - Dra. Angela Yu
    * Author: Noah Louvet
    * Day: 29 - Password Manager
    * Subject: Tkinter GUI - json format - csv data
---------------------------------------
"""

import json
from tkinter import *
from tkinter import messagebox, scrolledtext
from random import choice, randint, shuffle
import pyperclip
import pandas
import csv


# ---------------------------- PASSWORD GENERATOR (From previous project)---------------------- #


def generate_password():
    password_entry.delete(0, END)

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = randint(8, 10)
    nr_symbols = randint(2, 4)
    nr_numbers = randint(2, 4)

    password_list = [choice(letters) for char in range(nr_letters)]
    password_list += [choice(symbols) for char in range(nr_symbols)]
    password_list += [choice(numbers) for char in range(nr_numbers)]
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email = user_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if all([website, email, password]) and not any(" " in field for field in [website, email, password]):

        is_ok = messagebox.askokcancel(title=website, message=f"Entered details: \nEmail: {email}"
                                                              f"\nPassword: {password} \nDo you want to save?")
        if is_ok:
            with open("data.csv", mode="a", newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([website, email, password])

            try:
                with open("data.json", mode="r") as json_file:
                    # Load existing JSON data if the file is not empty
                    json_data = json.load(json_file)
            except (FileNotFoundError, json.JSONDecodeError):
                # If the file is empty or doesn't exist, start with an empty dictionary
                json_data = {}

            # Update the JSON data with new_data
            json_data.update(new_data)

            # Save the updated JSON data back to the file
            with open("data.json", mode="w") as json_file:
                json.dump(json_data, json_file, indent=4)

            website_entry.delete(0, END)
            password_entry.delete(0, END)
    else:
        messagebox.showwarning(title="Unable to save", message="Please fill all the credentials correctly.\n"
                                                               "Check for an empty entry or a space character.")


# ---------------------------- PASSWORD VIEWER ------------------------------- #


def view_passwords():
    password_view = pandas.read_csv('data.csv', names=['Website', 'Email/Username', 'Password'])
    password_window = Tk()
    password_window.title("Password viewer")
    password_window.config(padx=50, pady=50, bg="gray12")

    # Create a Text widget within the window
    text_widget = scrolledtext.ScrolledText(password_window, width=60, height=20, bg="gray14", fg="white")
    text_widget.pack()

    # Convert the dataframe to string and insert it into the Text widget
    dataframe_str = str(password_view)
    text_widget.insert(END, dataframe_str)

    # Make the window visible
    password_window.mainloop()


# ---------------------------- SEARCH ------------------------------- #


def search():
    website = website_entry.get()
    # used to check if search_view file found or not
    try:
        with open("data.json", mode="r") as json_file:
            search_view = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showwarning(title="Error", message="No data file found")
    else:
        if website in search_view:
            website_email = search_view[website]["email"]
            website_password = search_view[website]["password"]
            messagebox.showinfo(title=f"{website} Info", message=f"Email: {website_email}\n"
                                                                 f"Password: {website_password}")
        else:
            messagebox.showwarning(title="Error", message="No details found for this website")


# better to use if else statement rather than try except if possible, use try except for things not easy to catch
# exception handling should happen occasionally, if else functionality above may happen often

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="gray12")

canvas = Canvas(width=200, height=200, bg="gray12", highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:", bg="gray12", fg="white")
website_label.grid(column=0, row=1)
user_label = Label(text="Email/Username:", bg="gray12", fg="white")
user_label.grid(column=0, row=2)
password_label = Label(text="Password:", bg="gray12", fg="white")
password_label.grid(column=0, row=3)

website_entry = Entry(width=36)
website_entry.grid(column=1, row=1, padx=5, pady=5)
website_entry.focus()
user_entry = Entry(width=55)
user_entry.grid(column=1, row=2, columnspan=2, padx=5, pady=5)
user_entry.insert(0, "noahlou08@gmail.com")
password_entry = Entry(width=36)
password_entry.grid(column=1, row=3, padx=5, pady=5)

generate_pass_button = Button(text="Generate Password", command=generate_password)
generate_pass_button.grid(column=2, row=3, padx=5, pady=5)
add_button = Button(text="Add", width=47, command=save)
add_button.grid(column=1, row=4, columnspan=2, padx=5, pady=5)
view_pw_button = Button(text="View passwords", command=view_passwords)
view_pw_button.grid(column=1, row=5, columnspan=2, padx=5, pady=5)
search_button = Button(text="Search", width=14, command=search)
search_button.grid(column=2, row=1, padx=5, pady=5)

window.mainloop()
