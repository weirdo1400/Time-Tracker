from win32gui import GetWindowText, GetForegroundWindow
import time
import datetime as dt
import json 

#global array
global date_today
global date_exists
global data
global dictionary
global time_start
global open_window
global json_file
global running_tracker
global not_existing
class Tracker:
	def __init__(self):
		self.date_exists = False
		self.file = "data.json"
		self.date_today = dt.date.today()
		self.open_window = ""
		self.running_tracker = True
		self.start = False
		self.array = []
		global test
		
		test = True

	def calculate_time_and_store_in_list(self, not_existing, time_start, open_window):
		time_end = dt.datetime.now()		
		timedelta = (time_end - time_start).seconds
		print(str(open_window) + " has been open for " + str(timedelta))
		for p in self.array:
			if open_window == p[0]:
				p[1] += timedelta
				not_existing = False
				print("already opened")
				pass	
		if not_existing:
			print("not opened yet")
			self.array.insert(len(self.array), [open_window, timedelta])	
			not_existing = False
		print(self.array)

	def open_json_and_load_data(self, file):
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

	def get_current_app(self, open_window, time_start):
		try:
			while self.running_tracker:
				not_existing = True
				if open_window != GetWindowText(GetForegroundWindow()):
					print("Not same window")			
					self.calculate_time_and_store_in_list(not_existing, time_start, open_window)	
					time_start = dt.datetime.now()
					open_window = GetWindowText(GetForegroundWindow())
					print("new open window")
					print(GetWindowText(GetForegroundWindow()))
				time.sleep(2)
		except KeyboardInterrupt:
			self.calculate_time_and_store_in_list(not_existing, time_start, open_window)
			self.safe_data(data=data)
			print("Interrupted!")

	def safe_data(self, data):
		data[str(self.date_today)] = self.array
		print(data)
		try:
			with open (self.file, "w+") as output:
				json_string = json.dumps(data, indent=2)	
				output.write(json_string)  
				output.close()
		except:
			print("Error wrtiting to file")
	
	def run_tracker(self):
		#self.time_start, self.array, self.data = self.open_json_and_load_data(self.file)
		self.get_current_app(self.open_window, self.time_start)
		#self.safe_data(self.data)

	def stop(self):
		self.running_tracker = False
		print("stopped tracker in tracker.py")


# Run program

#time_start, array, data = open_json_and_load_data(file)
#get_current_app(open_window, time_start)
#safe_data(data)

if __name__  == "__main__":
	track = Tracker()
	track.run_tracker()