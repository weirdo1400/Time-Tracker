from tkinter import *
from tkcalendar import Calendar

import json

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

import subprocess as sp

import tracker

global time_youtube
helper_array = []
formated_data = {}
output_file = "formated_data.json"	
global data
date = ""
input_file = "data.json"		
global extProc
extProc = None
track = tracker.Tracker()


def get_date():
    # Grab the date
    my_date.config(text = "Selected Date is: " + cal.get_date())
    global date
    date = cal.get_date()
    summarize_data(date, data)

def open_and_read_json():
    try:
        with open (input_file, "r") as json_file:
            global data
            data = json.load(json_file)
            print("Existing JSON file:")
            print(data)
        print("File read")
    except:
        print("File is empty or doesnt't exist")

def check_if_date_exists(formated_date, data):
    if formated_date in data:
        date_exists = True
        print("Date exists")
        print(data[formated_date])
        summarize_data(formated_date, data)
    else:
        print("Date does not exist")

def summarize_data(formated_date, data):
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
        elif entry[0].find("Spotify Premium") != -1:
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
    helper_array.insert(6, ["Spotify Premium", time_spotify])
    helper_array.insert(7, ["League of Legends", time_lol])
    helper_array.insert(8, ["Google Chrome", time_google])
    helper_array.insert(9, ["Rest", time_rest])
    helper_array.insert(10, ["Total", time_total])
    formated_data[formated_date] = helper_array
    create_json_store_data(formated_date)
    create_pie_chart()
    update_labels()
           
def create_json_store_data(formated_date):
    try:
        with open (output_file, "w") as json_file:
            json_string = json.dumps(formated_data, indent=2)
            json_file.write(json_string)
            json_file.close()
    except:
        print("File is empty or doesnt't exist")

def create_pie_chart():
    youtube_pie = 100 / time_total * time_youtube
    twitch_pie = 100 / time_total * time_twitch
    vscode_pie = 100 / time_total * time_vscode
    mt5_pie = 100 / time_total * time_mt5
    mteditor_pie= 100 / time_total * time_mteditor
    discord_pie = 100 / time_total * time_discord
    spotify_pie = 100 / time_total * time_spotify
    google_pie = 100 / time_total * time_google
    lol_pie = 100 / time_total * time_lol
    rest_pie = 100 - youtube_pie - twitch_pie - vscode_pie - mt5_pie - mteditor_pie - discord_pie - spotify_pie - lol_pie
    pie_chart_array = np.array([youtube_pie, twitch_pie, vscode_pie, mt5_pie, mteditor_pie, discord_pie, spotify_pie, lol_pie, google_pie,  rest_pie])
    pie_labels = ["YouTube", "Twitch", "Visual Studio Code", "MetaTrader 5", "MetaEditor", "Discord", "Spotify", "League of Legends", "Google Chrome", "Rest"]
    fig = Figure()
    pie_chart = fig.add_subplot()
    pie_chart.pie(pie_chart_array, labels=pie_labels)
    canvas = FigureCanvasTkAgg(fig, master=root)  
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=1, padx=20)

    print("pie chart created")

def update_labels():
    youtube_time_label.config(text = str(time_youtube) + " sec")
    twitch_time_label.config(text = str(time_twitch) + " sec")
    vscode_time_label.config(text = str(time_vscode) + " sec")
    mt5_time_label.config(text = str(time_mt5) + " sec")
    mteditor_time_label.config(text = str(time_mt5) + " sec")
    mteditor_time_label.config(text = str(time_mteditor) + " sec")
    discord_time_label.config(text = str(time_discord) + " sec")
    spotify_time_label.config(text = str(time_spotify) + " sec")
    google_time_label.config(text = str(time_google) + " sec")
    lol_time_label.config(text = str(time_lol) + " sec")
    rest_time_label.config(text = str(time_rest) + " sec")
    total_time_label.config(text= str(time_total) + " sec")

def start_tracker():
    print("start")
    #track.running_tracker = True
    track.run_tracker()
    #extProc = sp.Popen(['python','tracker.py']) # runs tracker.py
    #status = sp.Popen.poll(extProc) # status should be 'None'

def stop_tracker(track): 
    #track.running_tracker = False
    print("change running_tracker to False") 
    
root = Tk()
#root = tb.Window(themename="superhero")
root.title("Test APP")
root.geometry("1080x800")

open_and_read_json()

#my_date = tb.DateEntry(root, bootstyle="primary", firstweekday=0)
#my_date.pack(pady=50)

# Add Calendar
cal = Calendar(root, selectmode = 'day', date_pattern="yyyy-mm-dd")
cal.grid(row=1,column=0)

# Add Button and Label
Button(root, text = "Get Date",
       command = get_date).grid(row=2, column=0)

# Button to start
Button(root, text = "Start tracker", command=start_tracker).grid(row=14, column=4)

# Button to stop
Button(root, text = "Stop tracker", command=stop_tracker).grid(row=14, column=5)
 
my_date = Label(root, text = "")
my_date.grid(row=3, column=0)

# Create all label for time and apps
youtube_label = Label(root, text="Youtube")
youtube_label.grid(row=4, column=0)
youtube_time_label = Label(root, text="Time")
youtube_time_label.grid(row=4, column=1)

twitch_label = Label(root, text="Twitch")
twitch_label.grid(row=5, column=0)
twitch_time_label = Label(root, text="Time")
twitch_time_label.grid(row=5, column=1)

vscode_label = Label(root, text="VS Code")
vscode_label.grid(row=6, column=0)
vscode_time_label = Label(root, text="Time")
vscode_time_label.grid(row=6, column=1)

mt5_label = Label(root, text="MetaTrader 5")
mt5_label.grid(row=7, column=0)
mt5_time_label = Label(root, text="Time")
mt5_time_label.grid(row=7, column=1)

mteditor_label = Label(root, text="MetaEditor")
mteditor_label.grid(row=8, column=0)
mteditor_time_label = Label(root, text="Time")
mteditor_time_label.grid(row=8, column=1)

discord_label = Label(root, text="Discord")
discord_label.grid(row=9, column=0)
discord_time_label = Label(root, text="Time")
discord_time_label.grid(row=9, column=1)

lol_label = Label(root, text="League of Legends")
lol_label.grid(row=10, column=0)
lol_time_label = Label(root, text="Time")
lol_time_label.grid(row=10, column=1)

spotify_label = Label(root, text="Spotify Premium")
spotify_label.grid(row=11, column=0)
spotify_time_label = Label(root, text="Time")
spotify_time_label.grid(row=11, column=1)

google_label = Label(root, text="Google Chrome")
google_label.grid(row=12, column=0)
google_time_label = Label(root, text="Time")
google_time_label.grid(row=12, column=1)

rest_label = Label(root, text="Rest")
rest_label.grid(row=13, column=0)
rest_time_label = Label(root, text="Time")
rest_time_label.grid(row=13, column=1)

total_label = Label(root, text="Total")
total_label.grid(row=14, column=0)
total_time_label = Label(root, text="Time")
total_time_label.grid(row=14, column=1)


root.mainloop() 