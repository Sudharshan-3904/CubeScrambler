import time
import customtkinter as ctk
import scramble


class Interface(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Scrambler and Timer")
        self.geometry("1200x800")

        self.timer_running = False
        self.start_time = None
        self.solve_times = []  # List to store solve times
        self.cube_type_map = {"3x3x3": scramble.Cube_3x3, "4x4x4": scramble.Cube_4x4, "5x5x5": scramble.Cube_5x5}
        self.current_cube = scramble.Cube_3x3()

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Left panel for timer and settings
        self.left_frame = ctk.CTkFrame(self, corner_radius=5, width=400)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.timer_label = ctk.CTkLabel(self.left_frame, text="00:00.00", font=("Arial", 25))
        self.timer_label.pack(pady=10)

        self.start_button = ctk.CTkButton(self.left_frame, text="Start", command=self.start_timer)
        self.start_button.pack(pady=5)

        self.stop_button = ctk.CTkButton(self.left_frame, text="Stop", command=self.stop_timer, state="disabled")
        self.stop_button.pack(pady=5)

        # Timer History Section
        self.history_frame = ctk.CTkFrame(self.left_frame, height=300, width=350)
        self.history_frame.pack_propagate(False)  # Prevent expanding based on content
        self.history_frame.pack(pady=20)

        self.history_label = ctk.CTkLabel(self.history_frame, text="Timer History", font=("Arial", 15, "bold"))
        self.history_label.pack()

        self.history_text = ctk.CTkLabel(self.history_frame, text="", justify="left", font=("Arial", 12))
        self.history_text.pack(fill="both", expand=True)

        # Scramble settings
        self.settings_frame = ctk.CTkFrame(self.left_frame)
        self.settings_frame.pack(pady=20)

        self.type_label = ctk.CTkLabel(self.settings_frame, text="Cube Type:")
        self.type_label.grid(row=0, column=0, padx=5, pady=5)

        self.type_dropdown = ctk.CTkComboBox(self.settings_frame, values=list(self.cube_type_map.keys()))
        self.type_dropdown.set("3x3x3")
        self.type_dropdown.grid(row=0, column=1, padx=5, pady=5)
        self.type_dropdown.bind("<<ComboboxSelected>>", self.update_cube_type)

        self.scramble_count_label = ctk.CTkLabel(self.settings_frame, text="Scrambles:")
        self.scramble_count_label.grid(row=1, column=0, padx=5, pady=5)

        self.scramble_count_entry = ctk.CTkEntry(self.settings_frame)
        self.scramble_count_entry.insert(0, "25")
        self.scramble_count_entry.grid(row=1, column=1, padx=5, pady=5)

        self.separate_check = ctk.CTkCheckBox(self.settings_frame, text="Separate")
        self.separate_check.select()
        self.separate_check.grid(row=2, column=0, padx=5, pady=5)

        self.fru_only_check = ctk.CTkCheckBox(self.settings_frame, text="FRU Only")
        self.fru_only_check.grid(row=2, column=1, padx=5, pady=5)

        self.generate_button = ctk.CTkButton(self.settings_frame, text="Scramble", command=self.generate_scrambles)
        self.generate_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Scramble display
        self.scramble_display_frame = ctk.CTkScrollableFrame(self, corner_radius=5)
        self.scramble_display_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    def update_cube_type(self, _):
        cube_type = self.type_dropdown.get()
        self.current_cube = self.cube_type_map[cube_type]()

    def start_timer(self):
        self.timer_running = True
        self.start_time = time.time()
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.update_timer()

    def stop_timer(self):
        self.timer_running = False
        self.stop_button.configure(state="disabled")
        self.start_button.configure(state="normal")

        # Calculate and store solve time
        elapsed_time = time.time() - self.start_time
        self.solve_times.append(elapsed_time)
        self.update_history()

    def update_timer(self):
        if self.timer_running:
            elapsed_time = time.time() - self.start_time
            self.timer_label.configure(text=f"{elapsed_time:.2f}")
            self.after(50, self.update_timer)

    def update_history(self):
        # Update timer statistics
        last_20 = self.solve_times[-20:]
        avg_time = sum(last_20) / len(last_20) if last_20 else None
        best_time_all = min(self.solve_times) if self.solve_times else None
        worst_time = max(self.solve_times) if self.solve_times else None
        best_last_5 = min(self.solve_times[-5:]) if len(self.solve_times) >= 5 else None
        best_last_12 = min(self.solve_times[-12:]) if len(self.solve_times) >= 12 else None

        def format_time(t):
            return f"{t:.2f}" if t is not None else "--"

        last_20_display = "\n".join(format_time(t) for t in last_20)

        history_text = f"""
        Average Time: {format_time(avg_time)} sec
        Best Time (All): {format_time(best_time_all)} sec
        Best of Last 5: {format_time(best_last_5)} sec
        Best of Last 12: {format_time(best_last_12)} sec
        Worst Time: {format_time(worst_time)} sec

        Last 20 Times:
        {last_20_display}
        """
        self.history_text.configure(text=history_text)

    def generate_scrambles(self):
        for widget in self.scramble_display_frame.winfo_children():
            widget.destroy()

        scramble_count = int(self.scramble_count_entry.get())
        self.current_cube.fru_only = self.fru_only_check.get()
        self.current_cube.seperete = self.separate_check.get()

        for _ in range(scramble_count):
            scramble = self.current_cube.new_moves()

            scramble_frame = ctk.CTkFrame(self.scramble_display_frame)
            scramble_frame.pack(pady=5, fill="x", expand=True)

            returned_text = scramble
            label = ctk.CTkLabel(scramble_frame, text=(returned_text + " "), wraplength=600)
            label.pack(side="left", padx=5)

            separator = ctk.CTkFrame(self.scramble_display_frame, height=2, bg_color="gray")
            separator.pack(fill="x", pady=5)


if __name__ == "__main__":
    app = Interface()
    app.mainloop()
