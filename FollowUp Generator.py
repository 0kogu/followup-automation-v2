import tkinter as tk
from tkinter import filedialog, messagebox
from tkcalendar import Calendar
import datetime
import os
from data_handling import get_stats
from image_editing import write_stats
from managers_ids import ids
import time

def generate_followups():
    """Handles the submission process for all managers."""
    try:
        bearer = string_entry.get().strip()
        chosen_folder = folder_var.get()
        inserted_date = calendar.get_date()

        if not bearer:
            messagebox.showerror("Error", "Authorization token cannot be empty.")
            return

        if not chosen_folder:
            messagebox.showerror("Error", "Please select a folder.")
            return

        if not os.path.isdir(chosen_folder):
            messagebox.showerror("Error", "Selected folder does not exist.")
            return

        # Create folder for the selected date
        create_date_folder(chosen_folder, inserted_date)

        for manager_id in ids:
            submit(bearer, chosen_folder, inserted_date, manager_id)

        time.sleep(1)
        messagebox.showinfo("Completed", "Processing completed successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def submit(bearer, chosen_folder, inserted_date, manager_id):
    """Handles data retrieval and image generation for a single manager."""
    try:
        stats = get_stats(inserted_date, bearer, manager_id)
        write_stats(inserted_date, stats, bearer, chosen_folder, manager_id)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process manager {manager_id}: {str(e)}")


def select_folder():
    """Opens a dialog for the user to select a folder."""
    folder_selected = filedialog.askdirectory()
    folder_var.set(folder_selected)


def create_date_folder(chosen_folder, inserted_date):
    """Creates a folder named after the selected date if it doesn't already exist."""
    try:
        month, day, year = inserted_date.split("/")
        formatted_date = f"{day}_{month}_{year}"
        folder_path = os.path.join(chosen_folder, formatted_date)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    except Exception as e:
        messagebox.showerror("Error", f"Could not create folder: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("Manager Stats Generator")

# Create a frame to hold the widgets
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

# Authorization token entry
tk.Label(frame, text="Enter Your Authorization:").grid(row=0, column=0, sticky="w")
string_entry = tk.Entry(frame, width=40)
string_entry.grid(row=0, column=1)

# Folder selection
tk.Label(frame, text="Select Folder:").grid(row=1, column=0, sticky="w")
folder_var = tk.StringVar()  # To store the selected folder path
folder_entry = tk.Entry(frame, textvariable=folder_var, width=30)
folder_entry.grid(row=1, column=1)
folder_button = tk.Button(frame, text="Browse", command=select_folder)
folder_button.grid(row=1, column=2)

# Date picker using Calendar widget
tk.Label(frame, text="Select Date:").grid(row=2, column=0, sticky="w")
calendar = Calendar(frame, selectmode="day", year=datetime.datetime.now().year, 
                    month=datetime.datetime.now().month, day=datetime.datetime.now().day)
calendar.grid(row=2, column=1, pady=10)

# Submit button
submit_button = tk.Button(frame, text="Generate Reports", command=generate_followups)
submit_button.grid(row=3, column=0, columnspan=3, pady=10)

# Start the Tkinter event loop
root.mainloop()
