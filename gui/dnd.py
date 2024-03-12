import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import tkinterDnD as dnd
from tkinter import BOTTOM, RIGHT, LEFT, TOP
import pygame

class GUI:
    def __init__(self, root):
        self.root = root  
        self.root.title("WavProcessing Application")
        self.root.geometry('800x500')
        
        self.drop_here = tk.StringVar()
        self.drop_here.set('Drop .wav file here!')

        self.path_str = tk.StringVar()
        self.path_str.set('')

    def check_if_wav(self, file_path):
        if file_path.endswith(".wav"):
            return True
        else:
            return False
        
    def drop(self, event):
    # This function is called, when stuff is dropped into a widget
        self.path_str.set(event.data)

        #if user droped .wav file
        if self.check_if_wav(self.path_str.get()):
            print("Plik .wav")
            self.wav_file = self.path_str.get()
            self.drop_wav_window_reset()
            self.wav_file_window()
        
        #if user droped diferent type of files
        else:
            print("Inny plik")
            self.label1.destroy()

    def drop_wav_window(self):
        self.label1 = tk.Label(self.root, textvar=self.drop_here, relief="solid")
        self.label1.pack(fill="both", expand=True, padx=20, pady=20)
        self.label1.register_drop_target("*")
        self.label1.bind("<<Drop>>", self.drop)
    
    def drop_wav_window_reset(self):
        self.label1.destroy()

    def wav_file_window(self):
        self.wav_player = tk.Frame(self.root)
        self.wav_player.pack(side = BOTTOM)

        #images for play and pause music buttons
        self.play_btn_image = tk.PhotoImage(file='play.png')
        self.stop_btn_image = tk.PhotoImage(file='stop.png')

        #creating play and pasue buttons
        self.play_btn = tk.Button(self.wav_player, image=self.play_btn_image,
                                  state=tk.DISABLED, command=self.play_wav)
        self.play_btn.pack(side = LEFT, padx = 5)
        self.stop_btn = tk.Button(self.wav_player, image=self.stop_btn_image,
                                  state=tk.DISABLED, command=self.stop_wav)
        self.stop_btn.pack(side = LEFT, padx = 5)

        #initialize pygame
        pygame.mixer.init()

        # Register a callback to stop audio when the window is closed
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

        

    def play_wav(self):
        pygame.mixer.music.load(self.wav_file)
        pygame.mixer.music.play()
        self.play_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)

    def stop_wav(self):
        pygame.mixer.music.pause()
        self.play_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)


    def on_closing(self):
        #chceck if audio is currently playing
        if pygame.mixer.music.get_busy():
            #stop audio playback
            pygame.mixer.music.stop()
        self.root.destroy() 

root = dnd.Tk()
wav_gui = GUI(root)
wav_gui.drop_wav_window()
root.mainloop()