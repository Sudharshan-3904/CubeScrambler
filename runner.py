import time
import random
import customtkinter as ctk

class Scrambler:
    def __init__(self) -> None:
        self.__moves_3x3 = ("F", "B", "R", "L", "U", "D", 
                            "F'", "B'", "R'", "L'", "U'", "D'", 
                            "2F", "2B", "2R", "2L", "2U", "2D")
        self.__fru_moves_3x3 = ("F", "R", "U", "F'", "R'", "U'", "2F", "2R", "2U")
        self.__generated = []

    def list_to_str(self, ipList=[]):
        resultString = ""
        for i in ipList:
            resultString += str(i)
            resultString += " "
        
        return resultString
    
    def generate_moves_3x3(self, length: int = 25, separate: bool = True, sepLen: int = 5, fru_only: bool = False):
        if not fru_only:
            for _ in range(length):
                self.__generated.append(random.choice(self.__moves_3x3))
        
        elif not fru_only:
            for _ in range(length):
                self.__generated.append(random.choice(self.__fru_moves_3x3))
        
        if separate:
            for i in range(0, length, (sepLen + 1)):
                self.__generated.insert(i, "-")
            self.__generated.pop(0)
        
        return self.list_to_str(self.__generated)


class Interface(ctk.CTk):
    def __init__(self):        
        #declaring Object and Variables
        self.__scramble_obj = Scrambler()
        self.__timer_running = False
        self.__start_time = 0
        self.__stop_time = 0
        super().__init__()

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1000}x{600}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        #Sidebar Configuration
        self.__sidebar_frame = ctk.CTkScrollableFrame(self, width=350, corner_radius=5)

        self.__timer_parent_frame = ctk.CTkFrame(self.__sidebar_frame, border_width=2)
        self.__timer_parent_frame.grid(row=1, column=0)

        self.__timer_label = ctk.CTkLabel(self.__timer_parent_frame, text="00:00:00", font=("Ariel", 25))
        self.__timer_label.grid(row=0, column=0, columnspan=2, padx=20, pady=5)

        self.__start_btn = ctk.CTkButton(self.__timer_parent_frame, text="Start", command=self.start_time, font=("Ariel", 25))
        self.__start_btn.grid(row=1, column=0, padx=20, pady=5)

        self.__stop_btn = ctk.CTkButton(self.__timer_parent_frame, text="Stop", command=self.stop_time, font=("Ariel", 25), state='disabled')
        self.__stop_btn.grid(row=1, column=1, padx=20, pady=5)

        self.__stats_container_frame = ctk.CTkFrame(self.__sidebar_frame)
        self.__stats_container_frame.grid(row=2, column=0, padx=20, pady=5)

        self.__best_time_title_label = ctk.CTkLabel(self.__stats_container_frame, text="Best Time")
        self.__best_time_title_label.grid(row=0, column=0, padx=10, pady=5)

        self.__best_time_output_label = ctk.CTkLabel(self.__stats_container_frame, text="--:--:--")
        self.__best_time_output_label.grid(row=0, column=1, padx=10, pady=5)

        self.__avg_5_title_label = ctk.CTkLabel(self.__stats_container_frame, text="Average of 5")
        self.__avg_5_title_label.grid(row=1, column=0, padx=10, pady=5)

        self.__avg_5_output_label = ctk.CTkLabel(self.__stats_container_frame, text="--:--:--")
        self.__avg_5_output_label.grid(row=1, column=1, padx=10, pady=5)

        self.__avg_12_title_label = ctk.CTkLabel(self.__stats_container_frame, text="Average of 12")
        self.__avg_12_title_label.grid(row=2, column=0, padx=10, pady=5)

        self.__avg_12_output_label = ctk.CTkLabel(self.__stats_container_frame, text="--:--:--")
        self.__avg_12_output_label.grid(row=2, column=1, padx=10, pady=5)

        self.__solved_scrabbles_label = ctk.CTkLabel(self.__stats_container_frame, text="Solved")
        self.__solved_scrabbles_label.grid(row=3, column=0, padx=10, pady=5)

        self.__solved_scrabbles_output_label = ctk.CTkLabel(self.__stats_container_frame, text="0")
        self.__solved_scrabbles_output_label.grid(row=3, column=1, padx=10, pady=5)

        self.__times_parent_frame = ctk.CTkFrame(self.__sidebar_frame, border_width=2)
        self.__times_parent_frame.grid(row=3, column=0)

        self.__times_title_label = ctk.CTkLabel(self.__times_parent_frame, text="Solved Times")
        self.__times_title_label.grid(row=0, column=0, padx=20, pady=5)
        
        self.__quit_sidebar_button = ctk.CTkButton(self.__sidebar_frame, text="Quit", command=lambda: self.destroy())
        self.__quit_sidebar_button.grid(row=200, column=0, padx=20, pady=5)

        self.__appearance_mode_label = ctk.CTkLabel(self.__sidebar_frame, text="Appearance Mode", anchor="w")
        self.__appearance_mode_label.grid(row=300, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_options_menu = ctk.CTkComboBox(self.__sidebar_frame, values=["Dark", "Light", "System"],command=self.change_appearance_mode_event)
        self.appearance_mode_options_menu.grid(row=400, column=0, padx=20, pady=5)

        self.__scaling_label = ctk.CTkLabel(self.__sidebar_frame, text="UI Scaling", anchor="w")
        self.__scaling_label.grid(row=500, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_options_menu = ctk.CTkComboBox(self.__sidebar_frame, values=["80%", "90%", "100%", "110%", "120%", ],command=self.change_scaling_event)
        self.appearance_mode_options_menu.grid(row=600, column=0, padx=20, pady=5)

        self.__section_content_frame = ctk.CTkFrame(master=self, corner_radius=5)
        self.__section_content_frame.grid(row=0, column=1, rowspan=15, sticky="nsew")

        #Main Scramble Configuration
        self.__sidebar_frame.grid(row=0, column=100, rowspan=15, sticky="nsew")

        self.change_appearance_mode_event("Dark")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
        self.updateSection()
        self.update()

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
        self.update_timer()
    
    def update_timer(self):
        if not self.__timer_running:
            self.__solve_time = self.__stop_time - self.__start_time
        elif self.__timer_running:
            self.__solve_time = time.time() - self.__start_time
        
        self.__timer_label.configure(text=(("{:.2f}".format(self.__solve_time).replace('.', ':'))))
        self.__timer_label.after(50, self.update_timer)
        self.updateSection()

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)
    
    def updateSection(self):
        self.update()


if __name__ == "__main__":
    app = Interface()
    app.mainloop()
