from win32gui import GetWindowText, GetForegroundWindow
import time
import datetime as dt
import json 

global array
array = []
global date_today
global date_exists
global data
global dictionary
global time_start
global open_window
open_window = ""
dictionary = {}
data = {}
date_exists = False
file = "C:/Coding/Time_Tracker/data.json"
date_today = dt.date.today()

def calculate_time_and_store_in_list(not_existing):
	time_end = dt.datetime.now()		
	timedelta = (time_end - time_start).seconds
	print(str(open_window) + " has been open for " + str(timedelta))
	for p in array:
		if open_window == p[0]:
			p[1] += timedelta
			not_existing = False
			print("already opened")
			pass	
	if not_existing:
		print("not opened yet")
		array.insert(len(array), [open_window, timedelta])	

def open_json_and_load_data(file):
	try:
		with open (file, "r") as json_file:
			data = json.load(json_file)
			print("Existing JSON file:")
			print(data)

		if str(date_today) in data:
			date_exists = True
			array = data[str(date_today)]
		print("File read")
	except:
		print("File is empty or doesnt't exist")
	open_window = GetWindowText(GetForegroundWindow()) 
	print(open_window)
	time_start = dt.datetime.now()

def get_current_app(open_window):
	try:
		counter = 0
		while True:
			not_existing = True
			if open_window != GetWindowText(GetForegroundWindow()):
				print("doesnt exist")			
				calculate_time_and_store_in_list(not_existing)	
				time_start = dt.datetime.now()
				open_window = GetWindowText(GetForegroundWindow())
			
				print(GetWindowText(GetForegroundWindow()))

			time.sleep(2)
	except KeyboardInterrupt:
		calculate_time_and_store_in_list(not_existing)
		print("Interrupted!")

def safe_data():
	try:
		data[str(date_today)] = array
		json_string = json.dumps(data, indent=2)
	except:
		dictionary[str(date_today)] = array
		print(dictionary)
		json_string = json.dumps(dictionary, indent=2)	
	json_file = open("C:/Coding/Time_Tracker/data.json", "w")
	json_file.write(json_string)  
	json_file.close()

# Run program
open_json_and_load_data(file)
time_start = dt.datetime.now()
open_window = GetWindowText(GetForegroundWindow())
get_current_app(open_window)
safe_data()