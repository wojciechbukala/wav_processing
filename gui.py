import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import tkinterDnD as dnd
from tkinter import BOTTOM, RIGHT, LEFT, TOP
import pygame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import check_wav
import sys
from tkinter import messagebox

class GUI:
    def __init__(self, root):
        self.root = root  
        self.root.title("WavProcessing Application")
        self.root.geometry('800x550')
        root.resizable(width=True, height=False)
        
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

    def parameters_page(self, cwav):
        # Create StringVar() for labels
        header = tk.StringVar(self.wav_parameters, cwav.header_to_string())
        header_chunk = tk.StringVar(self.wav_parameters, cwav.header_chunk_to_string())
        data_chunk = tk.StringVar(self.wav_parameters, cwav.data_to_string())
        format_chunk = tk.StringVar(self.wav_parameters, cwav.format_to_string())
        meta_chunk = tk.StringVar(self.wav_parameters, cwav.meta_to_string())

        # Header Label
        self.header_lbl = tk.Label(self.wav_parameters, textvariable=header, wraplength=870, justify="center")
        self.header_lbl.grid(row=0, column=0, columnspan=2, padx=70)

        # Header Chunk Label
        self.header_chunk_frame = tk.Frame(self.wav_parameters)
        self.header_chunk_frame.grid(row=1, column=0, padx=10, pady=10)
        header_chunk_title = tk.Label(self.header_chunk_frame, text="HEADER CHUNK", justify="center")
        header_chunk_title.pack()
        header_chunk_lbl = tk.Label(self.header_chunk_frame, textvariable=header_chunk, justify="center")
        header_chunk_lbl.pack()

        # Format Chunk Label
        self.format_chunk_frame = tk.Frame(self.wav_parameters)
        self.format_chunk_frame.grid(row=1, column=1, padx=0, pady=10)
        format_chunk_title = tk.Label(self.format_chunk_frame, text="FORMAT CHUNK", justify="center")
        format_chunk_title.pack()
        format_chunk_lbl = tk.Label(self.format_chunk_frame, textvariable=format_chunk, justify="center")
        format_chunk_lbl.pack()

        # Data Chunk Label
        self.data_chunk_frame = tk.Frame(self.wav_parameters)
        self.data_chunk_frame.grid(row=2, column=0, padx=10, pady=10)
        data_chunk_title = tk.Label(self.data_chunk_frame, text="DATA CHUNK", justify="center")
        data_chunk_title.pack()
        data_chunk_lbl = tk.Label(self.data_chunk_frame, textvariable=data_chunk, justify="center")
        data_chunk_lbl.pack()

        # Metadata Chunk Label
        self.meta_chunk_frame = tk.Frame(self.wav_parameters)
        self.meta_chunk_frame.grid(row=2, column=1, padx=0, pady=10)
        meta_chunk_title = tk.Label(self.meta_chunk_frame, text="METADATA CHUNK", justify="center")
        meta_chunk_title.pack()
        meta_chunk_lbl = tk.Label(self.meta_chunk_frame, textvariable=meta_chunk, justify="center")
        meta_chunk_lbl.pack()


    def destory_pages(self):
        for child in self.wav_parameters.winfo_children():
            child.destroy()

    def plots_page(self, cwav):
        plt_figure = cwav.plots()

        # Integrate matplotlib with tkinter
        canvas = FigureCanvasTkAgg(plt_figure, master=self.wav_parameters)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def fourier_transform_page(self, cwav):
        fourier_transform_lbl = tk.Label(self.wav_parameters, text="DODAJ TRANSFORMATE FOURIERA KOLESZKO",
                                          font=('Arial', 36), wraplength=800, justify="center")
        fourier_transform_lbl.pack()

    def save_file_page(self, cwav):
        save_wav_lbl = tk.Label(self.wav_parameters, text="Please enter file path to save anonimous copy",
                                pady=10, font=('Arial', 20))
        input_txt = tk.Text(self.wav_parameters, height = 1, width =20)
        save_wav_lbl.pack()
        input_txt.pack()
        
        def get_input():
            new_file_path = input_txt.get(1.0, "end-1c")
            if self.check_if_wav(new_file_path):
                cwav.save_anonimous_wav(new_file_path)
                messagebox.showinfo("Info", "File saved")
            else:
                messagebox.showwarning("Warning", "Not a .wav file")
        
        save_button = tk.Button(self.wav_parameters, text = "Submit", 
                                command = get_input, pady= 15)
        save_button.pack()

    def next_page(self):
        self.current_page += 1
        if self.current_page == 4:
            self.current_page = 0

        self.destory_pages()

        match self.current_page:
            case 0:
                self.parameters_page(self.cwav)
            case 1:
                self.plots_page(self.cwav)
            case 2:
                self.fourier_transform_page(self.cwav)
            case 3:
                self.save_file_page(self.cwav)
            

    def prev_page(self):
        self.current_page -= 1
        if self.current_page == -1:
            self.current_page = 2

        self.destory_pages()

        match self.current_page:
            case 0:
                self.parameters_page(self.cwav)
            case 1:
                self.plots_page(self.cwav)
            case 2:
                self.fourier_transform_page(self.cwav)

    def wav_file_window(self):
        self.navigation_and_title = tk.Frame(self.root, highlightbackground="grey", highlightthickness=1)
        self.navigation_and_title.pack(side = TOP, fill="x")

        self.wav_parameters = tk.Frame(self.root, bg="white")
        self.wav_parameters.pack(fill="both", expand=True)

        self.wav_player = tk.Frame(self.root, highlightbackground="grey", highlightthickness=1)
        self.wav_player.pack(side = BOTTOM, fill="x")

        #images for play and pause music buttons
        self.play_btn_image = tk.PhotoImage(file='images/play.png')
        self.stop_btn_image = tk.PhotoImage(file='images/stop.png')

        #creating play and pasue buttons
        self.play_btn = tk.Button(self.wav_player, image=self.play_btn_image,
                                command=self.play_wav)
        self.play_btn.pack(side = LEFT)
        self.stop_btn = tk.Button(self.wav_player, image=self.stop_btn_image,
                                command=self.stop_wav)
        self.stop_btn.pack(side = LEFT)

        #creating track name
        self.file_name = self.wav_file.split("/")[-1]
        self.file_name_lbl = tk.Label(self.wav_player, text=self.file_name, font=("Arial", 20))
        self.file_name_lbl.pack(fill="y", expand=True)

        #initialize pygame
        pygame.mixer.init()

        #create check_wav object
        self.cwav = check_wav.Check_wav(self.wav_file)
        self.parameters_page(self.cwav)
        self.current_page = 0

        #images for play and pause music buttons
        self.next_page_btn_image = tk.PhotoImage(file='images/next_page.png')
        self.prev_page_btn_image = tk.PhotoImage(file='images/prev_page.png')

        # Previous page button
        self.prev_page_btn = tk.Button(self.navigation_and_title, image=self.prev_page_btn_image,
                                        command=self.prev_page)
        self.prev_page_btn.pack(side=LEFT)

        # Title
        self.title_label = tk.Label(self.navigation_and_title, text=".wav Processing App", font=('Arial', 24))
        self.title_label.pack(side=LEFT, padx= 170)

        # Next page button
        self.next_page_btn = tk.Button(self.navigation_and_title, image=self.next_page_btn_image,
                                        command=self.next_page)
        self.next_page_btn.pack(side=RIGHT)

        # Fit size of buttons
        self.next_page_btn.config(width=64, height=64)
        self.prev_page_btn.config(width=64, height=64)


        # Register a callback to stop audio when the window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        

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
        sys.exit() 
