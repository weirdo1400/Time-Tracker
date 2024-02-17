import customtkinter as ctk
from tkcalendar import Calendar
import threading
import atexit

from tracker_with_threading import Tracker
t = Tracker()
thread_1 = threading.Thread(target=t)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Time Tracker")
        self.geometry("1080x800")
        self.resizable(False, False)

        self.side_menu_frame = SideMenuFrame(self, width=200, height=1000)
        self.side_menu_frame.place(x=0, y=0)

        self.calendar_frame = CalendarFrame(self, width=600, height=500)
        self.calendar_frame.place(x=100, y=0)

    def stop_threads(self):
        if self.thread_1 and self.thread_1.is_alive():
            self.t.stop()
            self.thread_1.join(timeout=3)
            print("Joined thread")
        else:
            print("Thread was not opened yet")

class SideMenuFrame(ctk.CTkFrame):
    def __init__(self, master, width, height):
        super().__init__(master, width=width, height=height)

        self.start_button = ctk.CTkButton(self, text="START", command=self.start_button_callback)
        self.start_button.place(x=0, y=0)
        self.stop_button = ctk.CTkButton(self, text="STOP", command=self.stop_button_callback)
        self.stop_button.place(x=0, y=100)

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
        super().__init__(master, width=width, height=height)

        self.cal = Calendar(self, selectmode = 'day', date_pattern="yyyy-mm-dd")
        self.cal.place(x=0, y=0)

        self.my_date = ctk.CTkLabel(self, text = "")
        self.my_date.place(x=100, y=0)

    def get_date(self):
        # Grab the date
        self.my_date.config(text = "Selected Date is: " + self.cal.get_date())
        global date
        date = self.cal.get_date()

class PlotFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


class ProgramAndTimeTable(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)



if __name__ == "__main__":
    app = App()
    atexit.register(app.stop_threads)
    app.mainloop()