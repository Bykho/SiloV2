import os
import tkinter as tk
from PIL import Image, ImageTk  # Pillow library for handling images

def list_files_in_directory(directory_path):
    files = []
    for file in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, file)):
            files.append(file)
    return files

def display_files_in_panel(directory_path):
    root = tk.Tk()
    root.title("File Display Panel")

    files = list_files_in_directory(directory_path)

    listbox = tk.Listbox(root)
    listbox.pack()

    for file_name in files:
        listbox.insert(tk.END, file_name)

        # Check if the file is an image (you can customize this check)
        if file_name.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
            img = Image.open(os.path.join(directory_path, file_name))
            img.thumbnail((100, 100))  # Resize the image to fit the listbox
            img = ImageTk.PhotoImage(img)
            label = tk.Label(root, image=img, text=file_name)
            label.image = img  # Keep a reference to the image to prevent it from being garbage collected
            label.pack()

    root.mainloop()

if __name__ == "__main__":
    user_home = os.path.expanduser("~")
    target_directory = os.path.join(user_home, "Desktop", "SiloV2", "SH")
    display_files_in_panel(target_directory)
