from tkinter import *
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

    helper_array.insert(0, ["YouTube", time_youtube])
    helper_array.insert(1, ["Twitch", time_twitch])
    helper_array.insert(2, ["Visual Studio Code", time_vscode])
    helper_array.insert(3, ["MetaTrader 5", time_mt5_1 + time_mt5_2])
    helper_array.insert(4, ["MetaEditor", time_mteditor])
    helper_array.insert(5, ["Discord", time_discord])
    helper_array.insert(6, ["Spotify Premium", time_spotify])
    helper_array.insert(7, ["League of Legends", time_lol])
    helper_array.insert(8, ["Google Chrome", time_google])
    helper_array.insert(9, ["Rest", time_rest])
    helper_array.insert(9, ["Total", time_total])

    if time_total != 0:
        create_pie_chart()
        update_labels()
           
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

# Add Calendar
cal = Calendar(root, selectmode = 'day', date_pattern="yyyy-mm-dd")
cal.grid(row=1,column=0)

# Add Button and Label
Button(root, text = "Get Date", command = get_date).grid(row=2, column=0)

# Button to start
Button(root, text = "Start tracker", command=start_tracker).grid(row=30, column=4)
# Button to stop
Button(root, text = "Stop tracker", command=stop_tracker).grid(row=30, column=5)
 
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
