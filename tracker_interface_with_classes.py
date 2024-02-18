import customtkinter as ctk
import tkinter as tk
from tkcalendar import Calendar
import threading
import atexit

import json


import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

from tracker_with_threading import Tracker
t = Tracker()
thread_1 = threading.Thread(target=t)

global time_youtube
helper_array = []
formated_data = {}
output_file = "formated_data.json"	
global data
date = ""
input_file = "data.json"		
global extProc
extProc = None

class App(ctk.CTk):
    def __init__(self):
        super().__init__()


        self.title("Time Tracker")

        self.app_width = 1080
        self.app_height = 800

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        self.x = (self.screen_width / 2) - (self.app_width / 2)
        self.y = (self.screen_height / 2) - (self.app_height / 2)
        
        self.geometry(f'{self.app_width}x{self.app_height}+{int(self.x)}+{int(self.y)}')
        self.resizable(False, False)

        self.side_menu_frame = SideMenuFrame(self, width=200, height=self.app_height)
        self.side_menu_frame.place(x=0, y=0)

        self.calendar_frame = CalendarFrame(self, width=300, height=300)
        self.calendar_frame.place(x=210, y=10)

        self.plot_frame = PlotFrame(self, width=550, height=self.app_height-20)
        self.plot_frame.place(x=520, y=10)

        self.open_and_read_json()

    def open_and_read_json(self):
        try:
            with open (input_file, "r") as json_file:
                global data
                data = json.load(json_file)
                print("Existing JSON file:")
                print(data)
            print("File read")
        except:
            print("File is empty or doesnt't exist")

    def stop_threads(self):
        if self.thread_1 and self.thread_1.is_alive():
            self.t.stop()
            self.thread_1.join(timeout=3)
            print("Joined thread")
        else:
            print("Thread was not opened yet")

class SideMenuFrame(ctk.CTkFrame):
    def __init__(self, master, width, height):
        super().__init__(master, width=width, height=height, corner_radius=0, fg_color="#fbd1a2")

        self.start_button = ctk.CTkButton(self, text="START", command=self.start_button_callback, fg_color="#7dcfb6", width=160, height=40)
        self.start_button.place(x=(width/2), y=700, anchor=ctk.CENTER)
        self.stop_button = ctk.CTkButton(self, text="STOP", command=self.stop_button_callback, fg_color="#f96d6d", width=160, height=40)
        self.stop_button.place(x=(width/2), y=750, anchor=ctk.CENTER)

    def start_button_callback(self):
        print("start_button pressed")
        try:
            self.thread_1 = threading.Thread(target=self.start_tracker)
            self.thread_1.start()
            print("thread started")

        except:
            print("thread already open")
 
    def start_tracker(self):
        self.t = Tracker()
        self.t.get_current_app()

    def stop_button_callback(self):
        if self.thread_1 and self.thread_1.is_alive():
            self.t.stop()
            self.thread_1.join(timeout=3)
            print("Joined thread")
        else:
            print("Thread was not opened yet")

class CalendarFrame(ctk.CTkFrame):
    def __init__(self, master, width, height):
        super().__init__(master, width=width, height=height, corner_radius=10, fg_color="#fbd1a2")

        self.cal = Calendar(self, selectmode = 'day', date_pattern="yyyy-mm-dd", selectbackground="#fbd1a2")
        self.cal.place(x=(width/2), y=100, anchor=ctk.CENTER)

        self.get_date_button = ctk.CTkButton(self, text="Select Date", command=self.get_date, width=160, height=40, fg_color="#7dcfb6")
        self.get_date_button.place(x=(width/2), y=250, anchor=ctk.CENTER)

        self.my_date = ctk.CTkLabel(self, text = "")
        self.my_date.place(x=50, y=700)

    def get_date(self):
        # Grab the date
        self.my_date.configure(text = "Selected Date is: " + self.cal.get_date())
        global date
        date = self.cal.get_date()
        print("hget date")
        plot = PlotFrame(self, width=0, height=0)
        plot.summarize_data(date, data)
        #plot.summarize_data(date, data)

class PlotFrame(ctk.CTkFrame):
    def __init__(self, master, width, height):
        super().__init__(master, width=width, height=height, corner_radius=10)

        self.create_labels()
        


        #fig = Figure(figsize=(5, 4), dpi=100)
        #t = np.arange(0, 3, .01)
        #fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

        #canvas = FigureCanvasTkAgg(fig, master=self)
        #canvas.draw()
        #canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=1)
        #self.update()

    def create_labels(self):
        self.x_dist = 5
        # Create all label for time and apps
        self.youtube_label = ctk.CTkLabel(self, text="Youtube")
        self.youtube_label.place(x=self.x_dist, y=450)
        self.youtube_time_label = ctk.CTkLabel(self, text="Time")
        self.youtube_time_label.place(x=200, y=450)

        self.twitch_label = ctk.CTkLabel(self, text="Twitch", fg_color="blue")
        self.twitch_label.place(x=self.x_dist, y=475)
        self.twitch_time_label = ctk.CTkLabel(self, text="Time")
        self.twitch_time_label.place(x=200, y=475)

        self.vscode_label = ctk.CTkLabel(self, text="VS Code")
        self.vscode_label.place(x=self.x_dist, y=500)
        self.vscode_time_label = ctk.CTkLabel(self, text="Time")
        self.vscode_time_label.place(x=100, y=500)

        self.mt5_label = ctk.CTkLabel(self, text="MetaTrader 5")
        self.mt5_label.place(x=self.x_dist, y=525)
        self.mt5_time_label = ctk.CTkLabel(self, text="Time")
        self.mt5_time_label.place(x=100, y=525)

        self.mteditor_label = ctk.CTkLabel(self, text="MetaEditor")
        self.mteditor_label.place(x=self.x_dist, y=550)
        self.mteditor_time_label = ctk.CTkLabel(self, text="Time")
        self.mteditor_time_label.place(x=100, y=550)

        self.discord_label = ctk.CTkLabel(self, text="Discord")
        self.discord_label.place(x=self.x_dist, y=575)
        self.discord_time_label = ctk.CTkLabel(self, text="Time")
        self.discord_time_label.place(x=100, y=575)

        self.lol_label = ctk.CTkLabel(self, text="League of Legends")
        self.lol_label.place(x=self.x_dist, y=600)
        self.lol_time_label = ctk.CTkLabel(self, text="Time")
        self.lol_time_label.place(x=100, y=600)

        self.spotify_label = ctk.CTkLabel(self, text="Spotify")
        self.spotify_label.place(x=self.x_dist, y=625)
        self.spotify_time_label = ctk.CTkLabel(self, text="Time")
        self.spotify_time_label.place(x=100, y=625)

        self.google_label = ctk.CTkLabel(self, text="Google Chrome")
        self.google_label.place(x=self.x_dist, y=650)
        self.google_time_label = ctk.CTkLabel(self, text="Time")
        self.google_time_label.place(x=100, y=650)

        self.rest_label = ctk.CTkLabel(self, text="Rest")
        self.rest_label.place(x=self.x_dist, y=675)
        self.rest_time_label = ctk.CTkLabel(self, text="Time")
        self.rest_time_label.place(x=100, y=675)

        self.total_label = ctk.CTkLabel(self, text="Total")
        self.total_label.place(x=self.x_dist, y=700)
        self.total_time_label = ctk.CTkLabel(self, text="Time")
        self.total_time_label.place(x=100, y=700)


    def open_and_read_json(self):
        try:
            with open (input_file, "r") as json_file:
                global data
                data = json.load(json_file)
                print("Existing JSON file:")
                print(data)
            print("File read")
        except:
            print("File is empty or doesnt't exist")

    def summarize_data(self, formated_date, data):
        global time_rest
        time_rest = 0
        global time_youtube
        time_youtube = 0
        global time_twitch
        time_twitch = 0
        global time_vscode
        time_vscode = 0
        global time_mt5
        time_mt5 = 0
        global time_mteditor
        time_mteditor = 0
        global time_spotify
        time_spotify = 0
        global time_lol
        time_lol = 0
        global time_google
        time_google = 0
        global time_discord
        time_discord = 0
        global time_total
        time_total = 0
        for entry in data[formated_date]:
            if entry[0].find("YouTube") != -1:
                time_youtube += entry[1]
            elif entry[0].find("Twitch") != -1:
                time_twitch += entry[1]
            elif entry[0].find("Visual Studio Code") != -1:
                time_vscode += entry[1]
            elif entry[0].find("MetaTrader 5") != -1:
                time_mt5 += entry[1]
            elif entry[0].find("ICMarketsSC") != -1:
                time_mt5 += entry[1]
            elif entry[0].find("MetaEditor") != -1:
                time_mteditor += entry[1]
            elif entry[0].find("Discord") != -1:
                time_discord += entry[1]
            elif entry[0].find("Spotify") != -1:
                time_spotify += entry[1]
            elif entry[0].find("League of Legends") != -1:
                time_lol += entry[1]
            elif entry[0].find("Google Chrome") != -1:
                time_google += entry[1]
            else:
                time_rest += entry[1]

            time_total += entry[1]

        helper_array.insert(0, ["YouTube", time_youtube])
        helper_array.insert(1, ["Twitch", time_twitch])
        helper_array.insert(2, ["Visual Studio Code", time_vscode])
        helper_array.insert(3, ["MetaTrader 5", time_mt5])
        helper_array.insert(4, ["MetaEditor", time_mteditor])
        helper_array.insert(5, ["Discord", time_discord])
        helper_array.insert(6, ["Spotify", time_spotify])
        helper_array.insert(7, ["League of Legends", time_lol])
        helper_array.insert(8, ["Google Chrome", time_google])
        helper_array.insert(9, ["Rest", time_rest])
        helper_array.insert(10, ["Total", time_total])
        formated_data[formated_date] = helper_array
        #self.create_labels()
        self.create_json_store_data(formated_date)
        self.create_pie_chart()
        self.update_labels()

    def create_json_store_data(self, formated_date):
        try:
            with open (output_file, "w") as json_file:
                json_string = json.dumps(formated_data, indent=2)
                json_file.write(json_string)
                json_file.close()
        except:
            print("File is empty or doesnt't exist")

    def create_pie_chart(self):
        self.youtube_pie = 100 / time_total * time_youtube
        self.twitch_pie = 100 / time_total * time_twitch
        self.vscode_pie = 100 / time_total * time_vscode
        self.mt5_pie = 100 / time_total * time_mt5
        self.mteditor_pie= 100 / time_total * time_mteditor
        self.discord_pie = 100 / time_total * time_discord
        self.spotify_pie = 100 / time_total * time_spotify
        self.google_pie = 100 / time_total * time_google
        self.lol_pie = 100 / time_total * time_lol
        self.rest_pie = 100 - self.youtube_pie - self.twitch_pie - self.vscode_pie - self.mt5_pie - self.mteditor_pie - self.discord_pie - self.spotify_pie - self.lol_pie
        self.pie_chart_array = np.array([self.youtube_pie, self.twitch_pie, self.vscode_pie, self.mt5_pie, self.mteditor_pie, self.discord_pie, self.spotify_pie, self.lol_pie, self.google_pie,  self.rest_pie])
        self.pie_labels = ["YouTube", "Twitch", "Visual Studio Code", "MetaTrader 5", "MetaEditor", "Discord", "Spotify", "League of Legends", "Google Chrome", "Rest"]
        
        self.updated_pie_labels, self.updated_pie_chart_array = self.check_if_program_was_used(self.pie_chart_array, self.pie_labels)
        
        self.fig = Figure(figsize=(4, 4), dpi=100)
        
        self.fig.add_subplot(111).pie(x=self.updated_pie_chart_array, labels=self.updated_pie_labels)

        self.canvas = FigureCanvasTkAgg(self.fig)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=795, y=240, anchor=ctk.CENTER)
        self.update()  

    def update_labels(self):
        self.youtube_time_label.configure(text = str(time_youtube) + " sec")
        self.twitch_time_label.configure(text = str(time_twitch) + " sec")
        self.vscode_time_label.configure(text = str(time_vscode) + " sec")
        self.mt5_time_label.configure(text = str(time_mt5) + " sec")
        self.mteditor_time_label.configure(text = str(time_mt5) + " sec")
        self.mteditor_time_label.configure(text = str(time_mteditor) + " sec")
        self.discord_time_label.configure(text = str(time_discord) + " sec")
        self.spotify_time_label.configure(text = str(time_spotify) + " sec")
        self.google_time_label.configure(text = str(time_google) + " sec")
        self.lol_time_label.configure(text = str(time_lol) + " sec")
        self.rest_time_label.configure(text = str(time_rest) + " sec")
        self.total_time_label.configure(text= str(time_total) + " sec")

    def check_if_date_exists(self, formated_date, data):
        if formated_date in data:
            date_exists = True
            print("Date exists")
            print(data[formated_date])
            self.summarize_data(formated_date, data)
        else:
            print("Date does not exist")

    def check_if_program_was_used(self, values, labels):
        updated_labels = []
        updated_values = []

        for i, value in enumerate(values):
            if (value > 0):
                updated_values.append(value)
                updated_labels.append(labels[i])

        updated_values = np.array(updated_values)

        return updated_labels, updated_values

class ProgramAndTimeTable(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)



if __name__ == "__main__":
    app = App()
    atexit.register(app.stop_threads)
    app.mainloop()