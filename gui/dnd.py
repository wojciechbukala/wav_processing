import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import tkinterDnD as dnd


root = dnd.Tk()  
root.title("WavProcessing Application")

stringvar = tk.StringVar()
stringvar.set('Drop .wav file here!')


def drop(event):
    # This function is called, when stuff is dropped into a widget
    stringvar.set(event.data)

#Label for droping .wav file
label_1 = tk.Label(root, textvar=stringvar, relief="solid")
label_1.pack(fill="both", expand=True, padx=20, pady=20)

label_1.register_drop_target("*")
label_1.bind("<<Drop>>", drop)


root.mainloop()