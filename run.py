import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import tkinterDnD as dnd
import gui

root = dnd.Tk()
wav_gui = gui.GUI(root)
wav_gui.drop_wav_window()
root.mainloop()