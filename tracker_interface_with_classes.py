import customtkinter as ctk
from tkcalendar import Calendar
from PIL import ImageTk
import threading
import atexit
import datetime as dt

import json

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

from tracker_with_threading import Tracker
global t
t = Tracker() 

helper_array = []
formated_data = {}
output_file = "formated_data.json"	
global data
date = ""
input_file = "data.json"		
class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color="#D3D3D3")
        self.title("Time Tracker")
        self.iconpath = ImageTk.PhotoImage(file="C:\Coding\Time_Tracker\icon\watch.png")
        self.wm_iconbitmap()
        self.iconphoto(False, self.iconpath)
        global thread_1, t

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

        self.calendar_frame = OverviewFrame(self, width=855, height=self.app_height-20)
        self.calendar_frame.place(x=212, y=10)

        self.open_and_read_json()

        atexit.register(self.stop_threads)

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
        global thread_1, t
    
        if thread_1 and thread_1.is_alive():
            t.stop()
            thread_1.join(timeout=3)
            print("Joined thread hlo")
        else:
            print("Thread was not opened yet")
        

class SideMenuFrame(ctk.CTkFrame):
    def __init__(self, master, width, height):
        super().__init__(master, width=width, height=height, corner_radius=0, fg_color="#fbd1a2")
        global thread_1, t

        self.tracker_running = False

        self.title_font = ctk.CTkFont(family='Helvetica', size=20, weight='bold')

        self.start_button = ctk.CTkButton(self, text="START", command=self.start_button_callback, fg_color="#7dcfb6", width=160, height=40, font=self.title_font, text_color="#ffffff")
        self.start_button.place(x=(width/2), y=650, anchor=ctk.CENTER)
        self.stop_button = ctk.CTkButton(self, text="STOP", command=self.stop_button_callback, fg_color="#f96d6d", width=160, height=40, font=self.title_font, text_color="#ffffff")
        self.stop_button.place(x=(width/2), y=700, anchor=ctk.CENTER)

        self.running_label = ctk.CTkLabel(self, text=f'Tracker inactive', text_color='#ff4343', font=self.title_font)
        self.running_label.place(x=(width/2), y=750, anchor=ctk.CENTER)

    def start_button_callback(self):
        global thread_1
        print("start_button pressed")
        try:
            thread_1 = threading.Thread(target=self.start_tracker, daemon=True)
            thread_1.start()
            print("thread started")
            self.tracker_running = True
            
        except:
            print("thread already open")
        self.update_status_label()
 
    def start_tracker(self):
        global t
        t = Tracker()
        t.get_current_app()

    def stop_button_callback(self):
        global thread_1, t, data
        if thread_1 and thread_1.is_alive():
            t.stop()
            thread_1.join(timeout=3)
            self.a, self.b, data, self.c = t.open_json_and_load_data(input_file)
            print("Joined thread hellow")
            self.tracker_running = False
        else:
            print("Thread was not opened yet")
        self.update_status_label()

    def update_status_label(self):
        if self.tracker_running:
            self.running_label.configure(text='Tracker is active', text_color='#3DAC9C')
        else:
            self.running_label.configure(text='Tracker is inactive', text_color='#ff4343')
    
class OverviewFrame(ctk.CTkFrame):
    def __init__(self, master, width, height):
        super().__init__(master, width=width, height=height, corner_radius=10, fg_color="#ffffff")
        self.key_exists = False
        global t

        self.colors = ['#f79256', '#fbd1a2', '#1d4e89', '#00b2ca', '#7dcfb6', '#DE576E', '#EDB1B0', '#7A71C9', '#831691', '#ACDE57']

        self.table_font = ctk.CTkFont(family='Helvetica', size=15)
        self.title_font = ctk.CTkFont(family='Helvetica', size=20, weight='bold')
        self.table_title_font = ctk.CTkFont(family='Helvetica', size=15, weight='bold')

        self.cal = Calendar(self, selectmode = 'day', date_pattern="yyyy-mm-dd", selectbackground="#fbd1a2")
        self.cal.place(x=150, y=115, anchor=ctk.CENTER)

        self.get_date_button = ctk.CTkButton(self, text="Select Date", command=self.get_date, width=160, height=40, fg_color="#7dcfb6", font=self.title_font, text_color="#ffffff")
        self.get_date_button.place(x=150, y=245, anchor=ctk.CENTER)

        self.my_date = ctk.CTkLabel(self, text = "", font=self.title_font)
        self.my_date.place(x=560, y=30, anchor=ctk.CENTER)

        self.create_lables()

    def create_lables(self):
        self.x_base = 360
        self.x_dist = 200
        self.row_n = 1
        self.base_row = 420
        self.row_dist = 25
        self.color_1 = "#7dcfb6"
        self.color_2 = "#00b2ca"
        self.height = 25
        self.width = 200
        self.color_index = 0
        self.time_padx = 5
        self.program_padx = 5
        # Create all label for time and apps
        self.program_title = ctk.CTkLabel(self, text="Programm", height=self.height, width=self.width, fg_color="#216760", text_color="#ffffff", anchor=ctk.W, padx=self.program_padx, font=self.table_title_font)
        self.program_title.place(x=self.x_base, y=self.base_row+self.row_dist*self.row_n-2)
        self.time_title = ctk.CTkLabel(self, text="Time", height=self.height, width=self.width, fg_color="#216760", text_color="#ffffff", anchor=ctk.E, padx=3*self.time_padx, font=self.table_title_font)
        self.time_title.place(x=self.x_base+self.x_dist, y=self.base_row+self.row_dist*self.row_n-2)
        self.row_n += 1

        self.youtube_label = ctk.CTkLabel(self, text="Youtube", fg_color=self.colors[self.color_index], height=self.height, width=self.width, anchor=ctk.W, padx=self.program_padx, font=self.table_font)
        self.youtube_label.place(x=self.x_base, y=self.base_row+self.row_dist*self.row_n)
        self.youtube_time_label = ctk.CTkLabel(self, text="", fg_color=self.colors[self.color_index], height=self.height, width=self.width, anchor=ctk.E, padx=self.time_padx, font=self.table_font)
        self.youtube_time_label.place(x=self.x_base+self.x_dist, y=self.base_row+self.row_dist*self.row_n)
        self.row_n += 1
        self.color_index += 1

        self.twitch_label = ctk.CTkLabel(self, text="Twitch", fg_color=self.colors[self.color_index], height=self.height, width=self.width, anchor=ctk.W, padx=self.program_padx, font=self.table_font)
        self.twitch_label.place(x=self.x_base, y=self.base_row+self.row_dist*self.row_n)
        self.twitch_time_label = ctk.CTkLabel(self, text="", fg_color=self.colors[self.color_index], height=self.height, width=self.width, anchor=ctk.E, padx=self.time_padx, font=self.table_font)
        self.twitch_time_label.place(x=self.x_base+self.x_dist, y=self.base_row+self.row_dist*self.row_n)
        self.row_n += 1
        self.color_index += 1

        self.vscode_label = ctk.CTkLabel(self, text="VS Code", fg_color=self.colors[self.color_index], height=self.height, width=self.width, anchor=ctk.W, padx=self.program_padx, font=self.table_font)
        self.vscode_label.place(x=self.x_base, y=self.base_row+self.row_dist*self.row_n)
        self.vscode_time_label = ctk.CTkLabel(self, text="", fg_color=self.colors[self.color_index], height=self.height, width=self.width, anchor=ctk.E, padx=self.time_padx, font=self.table_font)
        self.vscode_time_label.place(x=self.x_base+self.x_dist, y=self.base_row+self.row_dist*self.row_n)
        self.row_n += 1
        self.color_index += 1

        self.mt5_label = ctk.CTkLabel(self, text="MetaTrader 5", fg_color=self.colors[self.color_index], height=self.height, width=self.width, anchor=ctk.W, padx=self.program_padx, font=self.table_font)
        self.mt5_label.place(x=self.x_base, y=self.base_row+self.row_dist*self.row_n)
        self.mt5_time_label = ctk.CTkLabel(self, text="", fg_color=self.colors[self.color_index], height=self.height, width=self.width, anchor=ctk.E, padx=self.time_padx, font=self.table_font)
        self.mt5_time_label.place(x=self.x_base+self.x_dist, y=self.base_row+self.row_dist*self.row_n)
        self.row_n += 1
        self.color_index += 1
        
        self.mteditor_label = ctk.CTkLabel(self, text="MetaEditor", fg_color=self.colors[self.color_index], height=self.height, width=self.width, anchor=ctk.W, padx=self.program_padx, font=self.table_font)
        self.mteditor_label.place(x=self.x_base, y=self.base_row+self.row_dist*self.row_n)
        self.mteditor_time_label = ctk.CTkLabel(self, text="", fg_color=self.colors[self.color_index], height=self.height, width=self.width, anchor=ctk.E, padx=self.time_padx, font=self.table_font)
        self.mteditor_time_label.place(x=self.x_base+self.x_dist, y=self.base_row+self.row_dist*self.row_n)
        self.row_n += 1
        self.color_index += 1

        self.discord_label = ctk.CTkLabel(self, text="Discord", fg_color=self.colors[self.color_index], height=self.height, width=self.width, anchor=ctk.W, padx=self.program_padx, font=self.table_font)
        self.discord_label.place(x=self.x_base, y=self.base_row+self.row_dist*self.row_n)
        self.discord_time_label = ctk.CTkLabel(self, text="", fg_color=self.colors[self.color_index], height=self.height, width=self.width, anchor=ctk.E, padx=self.time_padx, font=self.table_font)
        self.discord_time_label.place(x=self.x_base+self.x_dist, y=self.base_row+self.row_dist*self.row_n)
        self.row_n += 1
        self.color_index += 1

        self.lol_label = ctk.CTkLabel(self, text="League of Legends", fg_color=self.colors[self.color_index], height=self.height, width=self.width, anchor=ctk.W, padx=self.program_padx, font=self.table_font)
        self.lol_label.place(x=self.x_base, y=self.base_row+self.row_dist*self.row_n)
        self.lol_time_label = ctk.CTkLabel(self, text="", fg_color=self.colors[self.color_index], height=self.height, width=self.width, anchor=ctk.E, padx=self.time_padx, font=self.table_font)
        self.lol_time_label.place(x=self.x_base+self.x_dist, y=self.base_row+self.row_dist*self.row_n)
        self.row_n += 1
        self.color_index += 1

        self.spotify_label = ctk.CTkLabel(self, text="Spotify", fg_color=self.colors[self.color_index], height=self.height, width=self.width, anchor=ctk.W, padx=self.program_padx, font=self.table_font)
        self.spotify_label.place(x=self.x_base, y=self.base_row+self.row_dist*self.row_n)
        self.spotify_time_label = ctk.CTkLabel(self, text="", fg_color=self.colors[self.color_index], height=self.height, width=self.width, anchor=ctk.E, padx=self.time_padx, font=self.table_font)
        self.spotify_time_label.place(x=self.x_base+self.x_dist, y=self.base_row+self.row_dist*self.row_n)
        self.row_n += 1
        self.color_index += 1

        self.google_label = ctk.CTkLabel(self, text="Google", fg_color=self.colors[self.color_index], height=self.height, width=self.width, anchor=ctk.W, padx=self.program_padx, font=self.table_font)
        self.google_label.place(x=self.x_base, y=self.base_row+self.row_dist*self.row_n)
        self.google_time_label = ctk.CTkLabel(self, text="", fg_color=self.colors[self.color_index], height=self.height, width=self.width, anchor=ctk.E, padx=self.time_padx, font=self.table_font)
        self.google_time_label.place(x=self.x_base+self.x_dist, y=self.base_row+self.row_dist*self.row_n)
        self.row_n += 1
        self.color_index += 1

        self.rest_label = ctk.CTkLabel(self, text="Rest", fg_color=self.colors[self.color_index], height=self.height, width=self.width, anchor=ctk.W, padx=self.program_padx, font=self.table_font)
        self.rest_label.place(x=self.x_base, y=self.base_row+self.row_dist*self.row_n)
        self.rest_time_label = ctk.CTkLabel(self, text="", fg_color=self.colors[self.color_index], height=self.height, width=self.width, anchor=ctk.E, padx=self.time_padx, font=self.table_font)
        self.rest_time_label.place(x=self.x_base+self.x_dist, y=self.base_row+self.row_dist*self.row_n)
        self.row_n += 1
        self.color_index += 1

        self.total_label = ctk.CTkLabel(self, text="Total", height=self.height, width=self.width, fg_color="#216760", text_color="#ffffff", anchor=ctk.W, padx=self.program_padx, font=self.table_title_font)
        self.total_label.place(x=self.x_base, y=self.base_row+self.row_dist*self.row_n+2)
        self.total_time_label = ctk.CTkLabel(self, text="", height=self.height, width=self.width, fg_color="#216760", text_color="#ffffff", anchor=ctk.E, padx=self.time_padx, font=self.table_title_font)
        self.total_time_label.place(x=self.x_base+self.x_dist, y=self.base_row+self.row_dist*self.row_n+2)

    def get_date(self):
        # Grab the date
        
        global date, t, thread_1
        date = self.cal.get_date()

        
        #t.calculate_time_and_store_in_list(t.not_existing, self.time_start, t.open_window)
        #t.safe_data(data=data)
        """        try:
            if thread_1 and thread_1.is_alive():
                print("THREAD")
                t.open_json_and_load_data(input_file)
                t.calculate_time_and_store_in_list(t.not_existing, t.time_start, t.open_window)
                t.safe_data(data)
            else:
                print(":NOTHREAD")
                t.open_json_and_load_data(input_file)
                t.calculate_time_and_store_in_list(t.not_existing, t.time_start, t.open_window)
                t.safe_data(data)
            print(data)
        except:
            print("smash or pass")
            print(data)
            pass
        #"""

        self.summarize_data(date, data)

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

        if formated_date in data.keys():
            print(f"Key '{formated_date}' exists.")
            self.key_exists = True
        else:
            print(f"Key '{formated_date}' does not exist.")
            self.key_exists = False

        if self.key_exists:
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
            self.create_json_store_data()   
            self.create_pie_chart()

        self.update_labels()

    def create_json_store_data(self):
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
        
        self.updated_pie_labels, self.updated_pie_chart_array, self.updated_colors = self.check_if_program_was_used(self.pie_chart_array, self.pie_labels, self.colors)
        
        self.fig = Figure(figsize=(3.1, 3.1), dpi=120, layout='constrained')
        self.fig.add_subplot(111).pie(x=self.updated_pie_chart_array, colors=self.updated_colors, autopct='%1.1f%%', pctdistance=0.85, radius=1.6)
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=560, y=240, anchor=ctk.CENTER)
        self.update()  

    def update_labels(self):
        if self.key_exists:
            self.youtube_time_label.configure(text = str(dt.timedelta(seconds=time_youtube)))
            self.twitch_time_label.configure(text = str(dt.timedelta(seconds=time_twitch)))
            self.vscode_time_label.configure(text = str(dt.timedelta(seconds=time_vscode)))
            self.mt5_time_label.configure(text = str(dt.timedelta(seconds=time_mt5)))
            self.mteditor_time_label.configure(text = str(dt.timedelta(seconds=time_mteditor)))
            self.discord_time_label.configure(text = str(dt.timedelta(seconds=time_discord)))
            self.spotify_time_label.configure(text = str(dt.timedelta(seconds=time_spotify)))
            self.google_time_label.configure(text = str(dt.timedelta(seconds=time_google)))
            self.lol_time_label.configure(text = str(dt.timedelta(seconds=time_lol)))
            self.rest_time_label.configure(text = str(dt.timedelta(seconds=time_rest)))
            self.total_time_label.configure(text= str(dt.timedelta(seconds=time_total)))
            self.my_date.configure(text = self.cal.get_date())
        else:
            self.my_date.configure(text = f"{str(self.cal.get_date())} does not exist")
            

    def check_if_date_exists(self, formated_date, data):
        if formated_date in data:
            date_exists = True
            print("Date exists")
            print(data[formated_date])
            self.summarize_data(formated_date, data)
        else:
            print("Date does not exist")

    def check_if_program_was_used(self, values, labels, colors):
        updated_labels = []
        updated_values = []
        updated_colors = []

        for i, value in enumerate(values):
            if (value > 0):
                updated_values.append(value)
                updated_labels.append(labels[i])
                updated_colors.append(colors[i])

        updated_values = np.array(updated_values)

        return updated_labels, updated_values, updated_colors



if __name__ == "__main__":
    
    app = App()
    atexit.register(app.stop_threads)
    app.mainloop()