import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class ModelRunnerPopup:
    def __init__(self, master):

        self.master = master
        self.master.title("Run Model")
        # self.master.geometry("600x500")
        self.master.attributes('-fullscreen', True)
        self.master.configure(bg='#000000')

        self.style = ttk.Style()
        self.style.configure('TButton', font=("Arial", 40), padding=20)
        self.style.configure('TRadiobutton', font=("Arial", 30))
        self.style.configure('TEntry', font=("Arial", 30))

        self.title_label = ttk.Label(master, text="Select options for visualization", font=("Arial", 40, "bold"))
        self.title_label.pack(pady=50)

        self.frame = ttk.Frame(master, padding=20)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.flag = False

        self.model_label = ttk.Label(self.frame, text="What type of model? Lumped or Distributed:",
                                     font=("Arial", 30, "bold"))
        self.model_label.grid(row=0, column=0, sticky="w", pady=20)

        self.model_var = tk.StringVar(value="Lumped")
        self.lumped_rb = ttk.Radiobutton(self.frame, text="Lumped", variable=self.model_var, value="Lumped",
                                         bootstyle="success", command=self.update_visualisation_question)
        self.lumped_rb.grid(row=1, column=0, sticky="w")

        self.distributed_rb = ttk.Radiobutton(self.frame, text="Distributed", variable=self.model_var,
                                              value="Distributed", bootstyle="success",
                                              command=self.update_visualisation_question)
        self.distributed_rb.grid(row=1, column=1, sticky="w")

        self.variable_label = ttk.Label(self.frame, text="Name of output variable:",
                                        font=("Arial", 30, "bold"))
        self.variable_label.grid(row=2, column=0, sticky="w", pady=20)

        self.variable_entry = ttk.Entry(self.frame, width=30, bootstyle="info", font=("Arial", 20, "bold"))
        self.variable_entry.grid(row=3, column=0, columnspan=2, sticky="w")

        self.date_label = ttk.Label(self.frame, text="Start date and end date (YYYY-MM-DD):",
                                                     font=("Arial", 30, "bold"))
        self.date_label.grid(row=4, column=0, sticky="w", pady=10)

        self.start_date_entry = ttk.Entry(self.frame, width=30, bootstyle="info", font=("Arial", 20, "bold"))
        self.start_date_entry.grid(row=5, column=0, sticky="w", padx=5)
        self.start_date_entry.insert(0, "2000-01-01")

        self.end_date_entry = ttk.Entry(self.frame, width=30, bootstyle="info", font=("Arial", 20, "bold"))
        self.end_date_entry.grid(row=5, column=1, sticky="w", padx=5)
        self.end_date_entry.insert(0, "2000-12-31")

        # Placeholder for the graph type question
        self.graph_type_frame = ttk.Frame(self.frame, padding=20)
        self.graph_type_frame.grid(row=6, column=0, columnspan=2, sticky="w")

        # Buttons: Run and Cancel
        self.button_frame = ttk.Frame(master, bootstyle='secondary')
        self.button_frame.pack(fill=tk.X, pady=20, side=tk.BOTTOM)

        self.run_button = ttk.Button(self.button_frame, text="Run", command=self.run_model, bootstyle="success",
                                     width=15)
        self.run_button.pack(side="left", padx=20, pady=10)

        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", command=self.master.quit, bootstyle="danger",
                                        width=15)
        self.cancel_button.pack(side="right", padx=20, pady=10)

        self.update_visualisation_question()

    def update_visualisation_question(self):
        for widget in self.graph_type_frame.winfo_children():
            widget.destroy()

        model_type = self.model_var.get()

        if model_type == "Distributed":
            # Question: Graph type? LineGraph or HeatMap
            self.graph_type_label = ttk.Label(self.graph_type_frame, text="Graph type? LineGraph or HeatMap:",
                                              font=("Arial", 30, "bold"))
            self.graph_type_label.grid(row=0, column=0, sticky="w", pady=20)

            self.graph_type_var = tk.StringVar(value="HeatMap")
            self.LineGraph_rb = ttk.Radiobutton(self.graph_type_frame, text="LineGraph", variable=self.graph_type_var,
                                                 value="LineGraph", bootstyle="success",
                                                 command=self.update_graph_type_question)
            self.LineGraph_rb.grid(row=1, column=1, sticky="w")

            self.map_rb = ttk.Radiobutton(self.graph_type_frame, text="HeatMap", variable=self.graph_type_var, value="HeatMap",
                                          bootstyle="success", command=self.update_graph_type_question)
            self.map_rb.grid(row=1, column=0, sticky="w")
            self.update_graph_type_question()

    def update_graph_type_question(self):
        for widget in self.graph_type_frame.grid_slaves():
            if int(widget.grid_info()["row"]) > 1:
                widget.grid_forget()

        graph_type = self.graph_type_var.get()
        if graph_type == "LineGraph":

            self.longlat = ttk.Label(self.graph_type_frame, text="Longitude and Latitude",
                                                 font=("Arial", 30, "bold"))
            self.longlat.grid(row=2, column=0, sticky="w", pady=10)

            self.longitude_entry = ttk.Entry(self.graph_type_frame, width=30, bootstyle="info", font=("Arial", 20, "bold"))
            self.longitude_entry.grid(row=3, column=0, sticky="w", padx=5)
            self.longitude_entry.insert(0, "6.395395")

            self.latitude_entry = ttk.Entry(self.graph_type_frame, width=30, bootstyle="info", font=("Arial", 20, "bold"))
            self.latitude_entry.grid(row=3, column=1, sticky="w", padx=5)
            self.latitude_entry.insert(0, "51.756918")

    def run_model(self):
        model_type = self.model_var.get()
        variable_name = self.variable_entry.get()
        if model_type == "Lumped":
            start_date = self.start_date_entry.get()
            end_date = self.end_date_entry.get()
            messagebox.showinfo("Model Run",
                                f"Model: {model_type}\nVariable: {variable_name}\nStart Date: {start_date}\nEnd Date: {end_date}")
        else:
            end_date = self.end_date_entry.get()
            graph_type = self.graph_type_var.get()
            if graph_type == "LineGraph":
                try:
                    longitude = float(self.longitude_entry.get())
                    latitude = float(self.latitude_entry.get())
                    messagebox.showinfo("Model Run",
                                        f"Model: {model_type}\nVariable: {variable_name}\nEnd Date: {end_date}\nGraph Type: {graph_type}\nLongitude: {longitude}\nLatitude: {latitude}")
                except ValueError:
                    messagebox.showinfo("Longitude and Latitude must be numbers")
            else:
                messagebox.showinfo("Model Run",
                                    f"Model: {model_type}\nVariable: {variable_name}\nEnd Date: {end_date}\nGraph Type: {graph_type}")
        self.flag = True
        self.master.quit()


# if __name__ == '__main__':
#     root = ttk.Window(themename="darkly")
#     app = ModelRunnerPopup(root)
#     root.mainloop()

