import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class TestSelector:
    def __init__(self, master, test_groups):
        self.master = master
        self.test_groups = test_groups
        self.selected_tests = []
        self.success = False
        self.master.title("Select Tests to Run")
        self.master.attributes('-fullscreen', True)
        self.master.configure()

        style = ttk.Style()
        style.configure('Red.TCheckbutton', font=("Arial", 12, "bold"), foreground="red", padding=16)
        style.configure('Green.TCheckbutton', font=("Arial", 12, "bold"), foreground="green", padding=16)
        style.configure('TButton', font=("Arial", 12, "bold"), padding=16)

        self.test_groups = test_groups
        self.title_label = ttk.Label(master, text="Select Tests to Run (Red = critical test, Green = non-critical test)", font=("Arial", 30, "bold"))
        self.title_label.pack(pady=50)

        self.canvas_frame = ttk.Frame(master, style='primary')
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, background='#000000')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame = ttk.Frame(self.canvas, style='primary')
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.check_vars = {}
        # print(enumerate(test_groups.items()))
        for col, (group_name, tests) in enumerate(test_groups.items()):
            group_label = ttk.Label(self.frame, text=group_name, font=("Arial", 16, "bold"))
            group_label.grid(row=0, column=col, padx=16, pady=10, sticky='n')

            group_var = tk.BooleanVar(value=True)
            self.check_vars[group_name] = group_var
            group_check = ttk.Checkbutton(self.frame, variable=group_var,
                                          command=lambda g=group_name: self.update_group_checks(g), style="primary",
                                          padding=20)
            group_check.grid(row=1, column=col, sticky='n')

            for row, test in enumerate(tests, start=2):
                test_var = tk.BooleanVar(value=test.enabled)
                self.check_vars[test.name] = test_var
                style_name = 'Red.TCheckbutton' if test.critical else 'Green.TCheckbutton'
                test_check = ttk.Checkbutton(self.frame, text=test.name, variable=test_var, style=style_name, padding=16)
                test_check.grid(row=row, column=col, sticky='w', padx=16, pady=10)

        self.frame.bind("<Configure>", self.on_frame_configure)
        # self.frame.bind("<MouseWheel>", self.on_mousewheel)

        self.button_frame = ttk.Frame(master, style='secondary')
        self.button_frame.pack(fill=tk.X, pady=20, side=tk.BOTTOM)

        self.run_button = ttk.Button(self.button_frame, text="Run Selected Tests", command=self.run_selected_tests,
                                     style="success", width=30)
        self.run_button.pack(side="left", padx=20, pady=10)

        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", command=self.master.quit, style="danger",
                                        width=30)
        self.cancel_button.pack(side="right", padx=20, pady=10)

        self.bind_mouse_wheel()

    def bind_mouse_wheel(self):
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind_all("<Button-4>", self.on_mouse_wheel)
        self.canvas.bind_all("<Button-5>", self.on_mouse_wheel)

    def on_mouse_wheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta == 120:
            self.canvas.yview_scroll(-1, "units")

    def update_group_checks(self, group_name):
        group_var = self.check_vars[group_name]
        for test in self.test_groups[group_name]:
            self.check_vars[test.name].set(group_var.get())

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def run_selected_tests(self):
        self.selected_tests = [test_name for test_name, var in self.check_vars.items() if
                               var.get() and test_name not in self.test_groups]
        if self.selected_tests:
            self.success = True
            messagebox.showinfo("Selected Tests", f"Running tests: {', '.join(self.selected_tests)}")
        else:
            messagebox.showinfo("No Tests Selected", "No tests selected to run.")
        self.master.quit()



