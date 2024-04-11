import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image
from pytube import YouTube
import os
from pathlib import Path
from threading import *

TITLE = "YoinkTube"

ICON_PATH = "_internal/images/icon.ico"
LOGO_PATH = "_internal/images/logo.png"

directory = "YoinkTube"
home_dir = str(Path.home())
SAVE_PATH = os.path.join(home_dir, directory)

DARK_MODE = "dark"

ctk.set_appearance_mode(DARK_MODE)
ctk.set_default_color_theme("dark-blue")

def center_window(self, width=300, height=200):
    # get screen width and height
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    self.geometry('%dx%d+%d+%d' % (width, height, x, y))
    self.resizable(False,False)

class App(ctk.CTk):
    def center_window(width=300, height=200):
        # get screen width and height
        screen_width = App.winfo_screenwidth()
        screen_height = App.winfo_screenheight()

        # calculate position x and y coordinates
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        App.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)

        center_window(self, 600, 350)

        self.title(TITLE)
        self.iconbitmap(ICON_PATH)

        self.link_stored = ""

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def open_destination_folder(self):
        os.startfile(SAVE_PATH, 'open')
    
    def shift_format(self, link, target_format, quality):
        print(link)
        print(target_format)
        print(quality)

        try: 
            yt = YouTube(link) 
        except:
            print("Connection Error")
            messagebox.showerror("", "Connection Error.\nCheck your internet connection and make sure the link is correct.")
            self.show_frame("StartPage")


        is_only_audio = True if target_format == "mp3" else False

        if is_only_audio:
            d_video = yt.streams.filter(only_audio=is_only_audio).first()
        else:
            d_video = yt.streams.filter(res=quality).first()

        try:
            os.mkdir(SAVE_PATH)
        except FileExistsError:
            pass

        try: 
            if is_only_audio:
                downloaded_file = d_video.download(output_path=SAVE_PATH)

                base, ext = os.path.splitext(downloaded_file)
                new_file = base + '.mp3'
                os.rename(downloaded_file, new_file)

                self.show_frame("StartPage")
                messagebox.showinfo("", "Audio downloaded successfully!")
            else:
                d_video.download(output_path=SAVE_PATH)
                self.show_frame("StartPage")
                messagebox.showinfo("", "Video downloaded successfully!")

            self.open_destination_folder()
        except: 
            print("Unknown Error!")
            self.show_frame("StartPage")
            messagebox.showerror("", "Some Error!")


class StartPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        top = ctk.CTkFrame(self, fg_color="transparent")
        middle = ctk.CTkFrame(self, fg_color="transparent")
        bottom  = ctk.CTkFrame(self, fg_color="transparent")

        top.pack(side="top", fill="x", padx=8, pady=8)
        middle.pack(side="top", fill="x", padx=8, pady=8)
        bottom.pack(side="bottom", fill="x", padx=8, pady=8)

        logo = ctk.CTkImage(light_image=Image.open(LOGO_PATH), 
                                dark_image=Image.open(LOGO_PATH), 
                                size=(300,100)) # WidthxHeight
        
        label_logo = ctk.CTkLabel(top, text="", image=logo)
        label_logo.pack(side="top", pady=10)

        def callback(event):


            if event.state & 4 > 0 and event.keycode == 86 and event.keysym == "??":
                entry.insert(0, self.controller.clipboard_get())

            elif event.state & 4 > 0 and event.keysym == "??":
                entry.select_range(0, 'end')
                entry.icursor('end')

        self.controller.bind("<Key>", callback)

        entry = ctk.CTkEntry(middle, placeholder_text="Paste a URL", corner_radius=30, justify="center")
        entry.pack(side="top", ipadx=100, padx=10, pady=10)

        def enter_link(event):
            if entry.get() != "":
                store_yt_url(self)
                entry.delete(0, 'end')
                controller.show_frame("PageOne")

        def store_yt_url(self):
            self.controller.link_stored = entry.get()

        entry.bind('<Return>', enter_link)

        label_description = ctk.CTkLabel(bottom, text="Free, unlimited and user-friendly YouTube downloader and converter.")
        label_description.pack(side="left", padx=(100, 0))



class PageOne(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        top = ctk.CTkFrame(self, fg_color="transparent")
        middle = ctk.CTkFrame(self, fg_color="transparent")
        bottom = ctk.CTkFrame(self, fg_color="transparent")

        top.pack(side="top", fill="x", padx=8, pady=8)
        middle.pack(side="top", fill="x", padx=8, pady=8)
        bottom.pack(side="bottom", fill="x", padx=8, pady=8)

        label_format = ctk.CTkLabel(top, text="Format")
        label_format.pack(side="left", pady=10)

        radio_var = ctk.StringVar(value="mp4")

        def radiobutton_event():
            print(radio_var.get())
            update_download_text(radio_var.get())
            if radio_var.get() == "mp3":
                hide_me(label_quality)
                hide_me(combobox_quality)
            else:
                label_quality.pack(side="left", padx=(0, 10))
                combobox_quality.pack(side="left", padx=0)

        def hide_me(widget):
            widget.pack_forget()
        
        radio_btn1 = ctk.CTkRadioButton(top, text="MP3 (Audio)", command=radiobutton_event, variable=radio_var, value="mp3")
        radio_btn1.pack(side="left", padx=10)

        radio_btn2 = ctk.CTkRadioButton(top, text="MP4 (Video)", command=radiobutton_event, variable=radio_var, value="mp4")
        radio_btn2.pack(side="left", padx=10)

        label_quality = ctk.CTkLabel(middle, text="Quality")
        label_quality.pack(side="left", pady=10)
        
        combobox_var = ctk.StringVar(value="720p")

        def combobox_callback(choice):
            print("combobox dropdown clicked:", choice)

        combobox_quality = ctk.CTkComboBox(middle, state="readonly", values=["144p", "240p", "360p", "480p", "720p"], command=combobox_callback, variable=combobox_var)
        combobox_quality.pack(side="left", padx=10)

        button_back = ctk.CTkButton(bottom, text="Go to the start page",
                                    command=lambda: controller.show_frame("StartPage"))
        button_back.pack(side="left")

        def update_download_text(text):
            if text == "mp3":
                button_download.configure(text="Format shift to MP3")
            else:
                button_download.configure(text="Format shift to MP4")


        def threading(): 
            self.controller.show_frame("PageTwo")
            t1=Thread(target=lambda: controller.shift_format(self.controller.link_stored, radio_var.get(), combobox_var.get()))
            t1.start() 
        
        button_download = ctk.CTkButton(bottom, command=threading)
        button_download.pack(side="right")

        update_download_text(radio_var.get())



class PageTwo(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        
        progress_label = ctk.CTkLabel(self, text="Downloading...")
        progress_label.pack(side="left", padx=10)

        progress_bar = ctk.CTkProgressBar(self, mode="indeterminate", width=500)
        progress_bar.pack(side="left", padx=10)

        progress_bar.start()
        self.update_idletasks()


if __name__ == "__main__":
    app = App()
    app.mainloop()