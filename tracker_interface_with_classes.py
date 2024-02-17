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

        self.calendar_frame = CalendarFrame(self, width=300, height=self.app_height)
        self.calendar_frame.place(x=205, y=0)

    def stop_threads(self):
        if self.thread_1 and self.thread_1.is_alive():
            self.t.stop()
            self.thread_1.join(timeout=3)
            print("Joined thread")
        else:
            print("Thread was not opened yet")

class SideMenuFrame(ctk.CTkFrame):
    def __init__(self, master, width, height):
        super().__init__(master, width=width, height=height, corner_radius=0, fg_color="red")

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
        super().__init__(master, width=width, height=height, corner_radius=0, fg_color="red")

        self.cal = Calendar(self, selectmode = 'day', date_pattern="yyyy-mm-dd", foreground="green")
        self.cal.place(x=5, y=5)

        self.get_date_button = ctk.CTkButton(self, text="Get Date", command=self.get_date)
        self.get_date_button.place(x=0, y=200)

        self.my_date = ctk.CTkLabel(self, text = "")
        self.my_date.place(x=50, y=700)

    def get_date(self):
        # Grab the date
        self.my_date.configure(text = "Selected Date is: " + self.cal.get_date())
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