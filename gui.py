import tkinter as tk
import time
import threading

LARGER_FONT = ("Comic Sans MS", 24)
LARGE_FONT = ("Comic Sans MS", 18)
MEDIUM_FONT = ("Comic Sans MS", 14)
SMALL_FONT = ("Comic Sans MS", 10)

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Atmospheria")
        tk.Tk.wm_geometry(self, "200x200")
        tk.Tk.wm_resizable(self, False, False)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.frames["TimerPage"] = TimerPage(container, self)
        self.frames["TimerPage"].grid(row=0, column=0, sticky="nsew")

    def set_timer(self, p_time):
        self.frames["TimerPage"].set_timer(p_time)


class TimerPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.total_time = 0
        self.set_time = 0

        self.label = tk.Label(self, text="timer page", font=LARGER_FONT)
        self.label.pack(pady=10, padx=10)

        self.timer_frame = tk.Frame(self)
        self.timer_frame.pack(pady=10, padx=10)

        self.minutes = tk.StringVar()
        self.minutes.set("00")
        self.minute_label = tk.Label(self.timer_frame, textvariable=self.minutes, font=LARGE_FONT, border=2, relief="sunken")
        self.minute_label.pack(side="left", padx=10)

        self.seconds = tk.StringVar()
        self.seconds.set("00")
        self.second_label = tk.Label(self.timer_frame, textvariable=self.seconds, font=LARGE_FONT, border=2, relief="sunken")
        self.second_label.pack(side="left", padx=10)

        # stop/start and reset button side by side
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=10, padx=10)

        self.stop_start_button = tk.Button(self.button_frame, text="Start", command=self.stop_start_timer)
        self.stop_start_button.pack(side="left", padx=10)

        self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side="left", padx=10)

        # button to skip to 1 minute
        self.skip_button = tk.Button(self, text="Skip to 1 minute", command=lambda: self.__skip_to_one_minute())
        self.skip_button.pack(pady=10, padx=10)

        # thread for timer
        self.timer_thread_on = False
        self.thread = threading.Thread(target=self.timer)
        self.thread.daemon = True
        self.thread.start()

    def __del__(self):
        self.thread.join()

    def __skip_to_one_minute(self):
        self.total_time = 60

    def set_timer(self, p_minutes):
        self.set_time = p_minutes * 60
        self.total_time = self.set_time
        self.update_timer_labels()
        self.controller.update()

    def stop_start_timer(self):
        if self.stop_start_button["text"] == "Start":
            self.stop_start_button["text"] = "Stop"
            self.reset_button["state"] = "disabled"
            self.timer_thread_on = True
        else:
            self.stop_start_button["text"] = "Start"
            self.reset_button["state"] = "normal"
            self.timer_thread_on = False
        self.controller.update()

    def reset_timer(self):
        self.total_time = self.set_time
        self.update_timer_labels()
        self.controller.update()

    def update_timer_labels(self):
        minute_string = str(self.total_time // 60)
        if len(minute_string) == 1:
            minute_string = "0" + minute_string
        
        second_string = str(self.total_time % 60)
        if len(second_string) == 1:
            second_string = "0" + second_string

        self.minutes.set(minute_string)
        self.seconds.set(second_string)
        self.controller.update()

    def timer(self):
        while True:
            if self.timer_thread_on and self.total_time > 0:
                self.total_time -= 1
                self.update_timer_labels()
                time.sleep(1)
            else:
                time.sleep(0.1)
