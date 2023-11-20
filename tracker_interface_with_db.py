import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
from tkcalendar import Calendar

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

import subprocess as sp

import mysql.connector
from mysql.connector.locales.eng import client_error

import threading

from tracker_with_database import Tracker

t1 = Tracker()
thread1 = threading.Thread(target=t1.run_tracker)


db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="weirdo",
    database="timetracker"
    )

mycursor = db.cursor(buffered=True)

global time_youtube
helper_array = []
formated_data = {}
global data
global extProc
extProc = None
global formatted_date
formatted_date = ""
global date
global pie_labels
pie_labels = []
global pie_values
pie_values = []



def get_date():
    # Grab the date
    date = cal.get_date()
    my_date.config(text = "Selected Date is: " + date)
    formatted_date = str(date + "%")
    summarize_data(formatted_date)

def summarize_data(formatted_date):
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
    global time_mt5_1
    time_mt5_1 = 0
    global time_mt5_2
    time_mt5_2 = 0
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

    db.cmd_refresh(1)
    add_time = "SELECT SUM(time_spent) FROM Time WHERE program_name LIKE %s AND time_start LIKE %s"
    
    mycursor.execute(add_time, ("%YouTube%", formatted_date))
    time_youtube = float(mycursor.fetchall()[0][0] or 0)
    mycursor.execute(add_time, ("%Twitch%", formatted_date))
    time_twitch = float(mycursor.fetchall()[0][0] or 0)
    mycursor.execute(add_time, ("%Visual Studio Code%", formatted_date))
    time_vscode = float(mycursor.fetchall()[0][0] or 0)  
    mycursor.execute(add_time, ("%ICMarketsSC%", formatted_date))
    time_mt5_1 = float(mycursor.fetchall()[0][0] or 0)
    mycursor.execute(add_time, ("%MetaTrader 5%", formatted_date))
    time_mt5_2 = float(mycursor.fetchall()[0][0] or 0)
    mycursor.execute(add_time, ("%MetaEditor%", formatted_date))
    time_mteditor = float(mycursor.fetchall()[0][0] or 0)
    mycursor.execute(add_time, ("%Discord%", formatted_date))
    time_discord = float(mycursor.fetchall()[0][0] or 0)
    mycursor.execute(add_time, ("%Spotify Premium%", formatted_date))
    time_spotify = float(mycursor.fetchall()[0][0] or 0)
    mycursor.execute("SELECT SUM(time_spent) FROM Time WHERE program_name LIKE %s AND program_name NOT LIKE '%Twitch%' AND program_name NOT LIKE '%YouTube%' AND time_start LIKE %s", ("%\Google Chrome%", formatted_date))
    time_google = float(mycursor.fetchall()[0][0] or 0)
    mycursor.execute(add_time, ("%\League of Legends%", formatted_date))
    time_lol = float(mycursor.fetchall()[0][0] or 0)
    mycursor.execute("SELECT SUM(time_spent) FROM Time WHERE time_start LIKE %s", (formatted_date, ))
    time_total = float(mycursor.fetchall()[0][0] or 0)
    time_mt5 = time_mt5_2 + time_mt5_1
    time_rest = time_total - time_twitch - time_youtube - time_spotify - time_lol - time_google - time_mt5 - time_mteditor - time_discord - time_vscode

    if time_total != 0:

        create_pie_chart()
        update_labels()

def add_labels_and_values(value, label):
    if value != 0:
        pie_values.append(value)
        pie_labels.append(label)

def create_pie_chart():
    pie_labels.clear()
    pie_values.clear()
    youtube_pie = 100 / time_total * time_youtube
    twitch_pie = 100 / time_total * time_twitch
    vscode_pie = 100 / time_total * time_vscode
    mt5_pie = 100 / time_total * time_mt5
    mteditor_pie= 100 / time_total * time_mteditor
    discord_pie = 100 / time_total * time_discord
    spotify_pie = 100 / time_total * time_spotify
    google_pie = 100 / time_total * time_google 
    lol_pie = 100 / time_total * time_lol
    rest_pie = 100 - youtube_pie - twitch_pie - vscode_pie - mt5_pie - mteditor_pie - discord_pie - spotify_pie - lol_pie - google_pie
    add_labels_and_values(youtube_pie, "YouTube")
    add_labels_and_values(twitch_pie, "Twitch")
    add_labels_and_values(vscode_pie, "Visual Studio Code")
    add_labels_and_values(youtube_pie, "MetaTrader 5")
    add_labels_and_values(mteditor_pie, "MetaEditor")
    add_labels_and_values(discord_pie, "Discord")
    add_labels_and_values(spotify_pie, "Spotify")
    add_labels_and_values(lol_pie, "League of Legends")
    add_labels_and_values(google_pie, "Google Chrome")
    add_labels_and_values(rest_pie, "Rest")

    pie_values_np = np.array(pie_values)
    fig = Figure()
    pie_chart = fig.add_subplot()
    pie_chart.pie(pie_values_np)
    pie_chart.legend(pie_labels, bbox_to_anchor=(1.3,0.5), loc="center right")
    canvas = FigureCanvasTkAgg(fig, master=root)  
    canvas.draw()
    canvas.get_tk_widget().place(x=380, y=80)

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
    t1.running_tracker = True
    try:
        print("start")
        thread1.start()
    except:
        print("Thread is already started once")

def stop_tracker(): 
    t1.running_tracker = False
    try:
        thread1.join()
    except:
        print("Thread was not started yet")
    print("Change running_tracker to False") 
    
root = Tk()
root.title("Time Tracker APP")
root.geometry("1080x800")

# Create a font
normalfont = tkFont.Font(family="Verdana",size=12,weight="normal")
boldfont = tkFont.Font(family="Verdana",size=12,weight="bold")
smallfont = tkFont.Font(family="Verdana",size=8,weight="normal")

# Add Calendar
cal = Calendar(root, selectmode = 'day', date_pattern="yyyy-mm-dd")
cal.place(x=10, y=10)

# Add Button and Label
Button(root, text = "Get Date", command = get_date, font=normalfont).place(x=75, y=230)

# Button to start
Button(root, text = "Start tracker", command=start_tracker, font=normalfont, bg='green').place(x=750, y=750)
# Button to stop
Button(root, text = "Stop tracker", command=stop_tracker, font=normalfont, bg='red').place(x=900, y=750)
 
my_date = Label(root, text = "", font=normalfont)
my_date.place(x=15, y=200)

# Set row and column weights to make the frame expand with the window
"""root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)"""

def on_resize(event):
    # Do something when the window is resized
    pass

# Bind the on_resize function to the <Configure> event of the root window
root.bind("<Configure>", on_resize)

# Create all label for time and apps
youtube_label = Label(root, text="Youtube", font=normalfont)
youtube_label.place(x=30, y=300)
youtube_time_label = Label(root, text="Time", font=normalfont)
youtube_time_label.place(x=220, y=300)

twitch_label = Label(root, text="Twitch", font=normalfont)
twitch_label.place(x=30, y=330)
twitch_time_label = Label(root, text="Time", font=normalfont)
twitch_time_label.place(x=220, y=330)

vscode_label = Label(root, text="VS Code", font=normalfont)
vscode_label.place(x=30, y=360)
vscode_time_label = Label(root, text="Time", font=normalfont)
vscode_time_label.place(x=220, y=360)

mt5_label = Label(root, text="MetaTrader 5", font=normalfont)
mt5_label.place(x=30, y=390)
mt5_time_label = Label(root, text="Time", font=normalfont)
mt5_time_label.place(x=220, y=390)

mteditor_label = Label(root, text="MetaEditor", font=normalfont)
mteditor_label.place(x=30, y=420)
mteditor_time_label = Label(root, text="Time", font=normalfont)
mteditor_time_label.place(x=220, y=420)

discord_label = Label(root, text="Discord", font=normalfont)
discord_label.place(x=30, y=450)
discord_time_label = Label(root, text="Time", font=normalfont)
discord_time_label.place(x=220, y=450)

lol_label = Label(root, text="League of Legends", font=normalfont)
lol_label.place(x=30, y=480)
lol_time_label = Label(root, text="Time", font=normalfont)
lol_time_label.place(x=220, y=480)

spotify_label = Label(root, text="Spotify Premium", font=normalfont)
spotify_label.place(x=30, y=510)
spotify_time_label = Label(root, text="Time", font=normalfont)
spotify_time_label.place(x=220, y=510)

google_label = Label(root, text="Google Chrome", font=normalfont)
google_label.place(x=30, y=540)
google_time_label = Label(root, text="Time", font=normalfont)
google_time_label.place(x=220, y=540)

rest_label = Label(root, text="Rest", font=normalfont)
rest_label.place(x=30, y=570)
rest_time_label = Label(root, text="Time", font=normalfont)
rest_time_label.place(x=220, y=570)

total_label = Label(root, text="Total", font=boldfont)
total_label.place(x=30, y=600)
total_time_label = Label(root, text="Time", font=boldfont)
total_time_label.place(x=220, y=600)

root.mainloop()
