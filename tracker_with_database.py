from win32gui import GetWindowText, GetForegroundWindow
import time
import datetime as dt
import mysql.connector
import mysql.connector.locales.eng.client_error

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="weirdo",
    database="timetracker"
    )

mycursor = db.cursor(buffered=True)

# Was used to create the DB the first time
#mycursor.execute("CREATE DATABASE timetracker") 
# Create a table in the database
#mycursor.execute("CREATE TABLE Time (id int PRIMARY KEY AUTO_INCREMENT, program_name VARCHAR(100), time_spent int UNSIGNED, time_start VARCHAR(50), time_end VARCHAR(50))")
#mycursor.execute("ALTER TABLE Time CHANGE time_end time_end datetime")

#global array
global date_today
global date_exists
global data
global dictionary
global time_start
global open_window
global json_file
global running_tracker

class Tracker:
	def __init__(self):
		self.date_exists = False
		self.date_today = dt.date.today()
		self.open_window = "TimeTracker"
		self.running_tracker = True
		self.start = False
		self.array = []

	def calculate_time_and_store_in_db(self, time_start, open_window):
		time_end = dt.datetime.now()		
		timedelta = (time_end - time_start).seconds
		if timedelta > 0:
			print(str(open_window) + " has been open for " + str(timedelta))
			mycursor.execute("INSERT INTO Time (program_name, time_spent, time_start, time_end) VALUES (%s, %s, %s, %s)", (open_window, timedelta, str(time_start), str(time_end)))
			# Commit changes to DB
			db.commit()
		else:
			print("Time == 0")
	
	def get_current_app(self, open_window, time_start):
		try:
			while self.running_tracker:
				if open_window != GetWindowText(GetForegroundWindow()):
					print("Not the same window")			
					self.calculate_time_and_store_in_db(time_start, open_window)	
					time_start = dt.datetime.now()
					open_window = GetWindowText(GetForegroundWindow())
					print("New window open")
					print(GetWindowText(GetForegroundWindow()))
				time.sleep(2)
		except KeyboardInterrupt:
			self.calculate_time_and_store_in_db(time_start, open_window)
			print("Interrupted!")
	
	def run_tracker(self):
		time_start = dt.datetime.now()
		self.get_current_app(self.open_window, time_start)
		
if __name__  == "__main__":
	track = Tracker()
	track.run_tracker()