# market_analysis_app.py
import tkinter as tk
from pymongo import MongoClient
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from GraphFunctions import GraphFunctions

class MarketAnalysis:
    def __init__(self, root):
        self.root = root
        self.root.title("2023 Linkedin Market Analysis")
        self.db = MongoClient('mongodb://localhost:27017/')['MarketAnalysis']
        
        # Setup the Figure and Axes
        self.fig = Figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack()

        # Instantiate GraphFunctions
        self.graph_functions = GraphFunctions(self.db)

        # Create buttons
        self.create_buttons()

        # Create text widget
        self.text_widget = tk.Text(self.root, height=10, width=100)
        self.text_widget.pack()

        # Set the close protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_buttons(self):
        run_button1 = tk.Button(self.root, text="Calculate Sponsored Percentage",
                                command=lambda: self.graph_functions.sponsored(self.ax, self.canvas, self.text_widget))
        run_button1.pack()

        run_button2 = tk.Button(self.root, text="Top 10 Most Frequent Job titles",
                                command=lambda: self.graph_functions.num_of_job(self.ax, self.canvas, self.text_widget))
        run_button2.pack()

        run_button3 = tk.Button(self.root, text="Number of Jobs in each State in US",
                                command=lambda: self.graph_functions.jobs_in_each_state(self.ax, self.canvas, self.text_widget))
        run_button3.pack()

    def on_closing(self):
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MarketAnalysis(root)
    root.mainloop()
