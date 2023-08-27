from win32gui import GetWindowText, GetForegroundWindow
import time
import datetime as dt
import pprint
import json 


def calculate_time_and_store_in_list(counter, not_existing):
	time_end = dt.datetime.now()		
	timedelta = (time_end - time_start).seconds
	counter += 1
	print(str(open_window) + " has been open for " + str(timedelta))
	
	for p in array:
		if open_window == p[0]:
			p[1] += timedelta
			not_existing = False
			print("already opened")
			pass
		
	if not_existing:
		print("not opened yet")
		array.insert(counter, [open_window, timedelta])	

open_window = GetWindowText(GetForegroundWindow()) 
print(open_window)
time_start = dt.datetime.now()

try:
	array = []
	counter = 0
	while True:
		not_existing = True
		if open_window != GetWindowText(GetForegroundWindow()):
			calculate_time_and_store_in_list(counter, not_existing)	
			time_start = dt.datetime.now()
			open_window = GetWindowText(GetForegroundWindow())
			print(GetWindowText(GetForegroundWindow()))

		time.sleep(2)
except KeyboardInterrupt:
	calculate_time_and_store_in_list(counter, not_existing)
	print("Interrupted!")

json_string = json.dumps(array)
json_file = open("C:/Coding/Time_Tracker/data.json", "w")
json_file.write(json_string)
json_file.close()

