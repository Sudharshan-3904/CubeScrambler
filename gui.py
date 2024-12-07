import scrabmle
import customtkinter as ctk

class Interface(ctk.CTk):
    def __init__(self):
        # Declaring Object and Variables
        self.__scramble_obj = scrabmle.Cube_3x3()
        self.__timer_running = False
        self.__start_time = 0
        self.__stop_time = 0
        self.__last_times = []  # Store the last three solve times

        super().__init__()

        # Configure window
        self.title("CustomTkinter Timer and Scrambler")
        self.geometry(f"{1000}x{600}")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Sidebar Configuration
        self.__sidebar_frame = ctk.CTkScrollableFrame(self, width=350, corner_radius=5)
        self.__sidebar_frame.grid(row=0, column=0, rowspan=15, sticky="nsew")

        # Timer Frame
        self.__timer_parent_frame = ctk.CTkFrame(self.__sidebar_frame, border_width=2)
        self.__timer_parent_frame.grid(row=1, column=0, padx=20, pady=10)

        self.__timer_label = ctk.CTkLabel(self.__timer_parent_frame, text="00:00:00", font=("Ariel", 25))
        self.__timer_label.grid(row=0, column=0, columnspan=2, padx=20, pady=5)

        self.__start_btn = ctk.CTkButton(self.__timer_parent_frame, text="Start", command=self.start_time, font=("Ariel", 25))
        self.__start_btn.grid(row=1, column=0, padx=20, pady=5)

        self.__stop_btn = ctk.CTkButton(self.__timer_parent_frame, text="Stop", command=self.stop_time, font=("Ariel", 25), state="disabled")
        self.__stop_btn.grid(row=1, column=1, padx=20, pady=5)

        # Times Display
        self.__times_parent_frame = ctk.CTkFrame(self.__sidebar_frame, border_width=2)
        self.__times_parent_frame.grid(row=3, column=0, padx=20, pady=10)

        self.__times_title_label = ctk.CTkLabel(self.__times_parent_frame, text="Last 3 Times")
        self.__times_title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=5)

        self.__last_times_label = ctk.CTkLabel(self.__times_parent_frame, text="--\n--\n--", justify="left")
        self.__last_times_label.grid(row=1, column=0, columnspan=2, padx=20, pady=5)

        # Scramble Generator
        self.__scramble_button = ctk.CTkButton(self.__sidebar_frame, text="Generate Scramble", command=self.generate_scramble, font=("Ariel", 20))
        self.__scramble_button.grid(row=4, column=0, padx=20, pady=10)

        self.__scramble_label = ctk.CTkLabel(self.__sidebar_frame, text="", font=("Ariel", 15), wraplength=300)
        self.__scramble_label.grid(row=5, column=0, padx=20, pady=5)

        # Quit Button
        self.__quit_sidebar_button = ctk.CTkButton(self.__sidebar_frame, text="Quit", command=lambda: self.destroy())
        self.__quit_sidebar_button.grid(row=200, column=0, padx=20, pady=5)

    def start_time(self):
        self.__timer_label.configure(text="00:00.00")
        if not self.__timer_running:
            self.__start_time = time.time()
            self.__timer_running = True
        self.__start_btn.configure(state="disabled")
        self.__stop_btn.configure(state="enabled")
        self.update_timer()

    def stop_time(self):
        self.__stop_time = time.time()
        self.__timer_running = False
        self.__start_btn.configure(state="enabled")
        self.__stop_btn.configure(state="disabled")

        solve_time = round(self.__stop_time - self.__start_time, 2)
        self.__last_times.insert(0, solve_time)
        self.__last_times = self.__last_times[:3]
        self.update_last_times_label()

    def update_timer(self):
        if self.__timer_running:
            elapsed_time = time.time() - self.__start_time
            self.__timer_label.configure(text=f"{elapsed_time:.2f}".replace(".", ":"))
            self.__timer_label.after(50, self.update_timer)

    def update_last_times_label(self):
        self.__last_times_label.configure(
            text="\n".join(f"{time:.2f}s" for time in self.__last_times)
        )

    def generate_scramble(self):
        scramble = self.__scramble_obj.generate_moves()
        self.__scramble_label.configure(text=scramble)


app = Interface()
app.mainloop()
