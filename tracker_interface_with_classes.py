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
        self.geometry("400x500")
        
        self.cal = Calendar(self, selectmode = 'day', date_pattern="yyyy-mm-dd")
        self.cal.grid(row=1,column=0)

        self.start_button = ctk.CTkButton(self, text="START", command=self.start_button_callback)
        self.start_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.stop_button = ctk.CTkButton(self, text="STOP", command=self.stop_button_callback)
        self.stop_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

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

    def stop_threads(self):
        self.stop_button_callback()


if __name__ == "__main__":
    app = App()
    atexit.register(app.stop_threads)
    app.mainloop()