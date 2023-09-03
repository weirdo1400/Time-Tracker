from win32gui import GetWindowText, GetForegroundWindow
import time
import datetime as dt
import json 

global array
global date_today
global date_exists
global data
global dictionary
global time_start
global open_window
global json_file
open_window = ""

date_exists = False
file = "data.json"
date_today = dt.date.today()

def calculate_time_and_store_in_list(not_existing, time_start, open_window):
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
		not_existing = False
	print(array)

def open_json_and_load_data(file):
	date_today = dt.date.today()
	try:
		with open (file, "r") as json_file:
			data = json.load(json_file)
			print("Existing JSON file:")
			print(data)
		if str(date_today) in data:
			date_exists = True
			array = data[str(date_today)]
			print("date exists")
		else:
			array = []
		print("File read")
	except:
		print("File is empty or doesnt't exist")
		array = []
		data = {}

	open_window = GetWindowText(GetForegroundWindow()) 
	print("Open window: " + open_window)
	time_start = dt.datetime.now()
	return time_start, array, data

def get_current_app(open_window, time_start):
	try:
		while True:
			not_existing = True
			if open_window != GetWindowText(GetForegroundWindow()):
				print("Not same window")			
				calculate_time_and_store_in_list(not_existing, time_start, open_window)	
				time_start = dt.datetime.now()
				open_window = GetWindowText(GetForegroundWindow())
				print("new open window")
				print(GetWindowText(GetForegroundWindow()))
			time.sleep(2)
	except KeyboardInterrupt:
		calculate_time_and_store_in_list(not_existing, time_start, open_window)
		print("Interrupted!")

def safe_data(data):
	data[str(date_today)] = array
	print(data)
	try:
		with open (file, "w+") as output:
			json_string = json.dumps(data, indent=2)	
			output.write(json_string)  
			output.close()
	except:
		print("Error wrtiting to file")

# Run program
time_start, array, data = open_json_and_load_data(file)
get_current_app(open_window, time_start)
safe_data(data)
