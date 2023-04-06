import subprocess
import re
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class PingGraph(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        
        self.fig = Figure(figsize=(10, 4), dpi=100)
        self.ax1 = self.fig.add_subplot(121)
        self.ax2 = self.fig.add_subplot(122)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        self.x_data = []
        self.y_data_availability = []
        self.y_data_packet_loss = []
        self.max_data_points = 50

        self.ping_interval = 1  # in seconds
        self.hostname = 'www.google.com'

        self.ping_count = 0
        self.ping_received = 0
        self.ping_lost = 0
        
        self.update_graph()

    def create_widgets(self):
        ttk.Label(self, text="Ping Graph").pack()

    def update_graph(self):
        self.ping()
        self.x_data.append(self.ping_interval * self.ping_count)
        self.y_data_availability.append(self.get_availability())
        self.y_data_packet_loss.append(self.get_packet_loss())

        if len(self.x_data) > self.max_data_points:
            self.x_data.pop(0)
            self.y_data_availability.pop(0)
            self.y_data_packet_loss.pop(0)

        self.ax1.clear()
        self.ax1.plot(self.x_data, self.y_data_availability)
        self.ax1.set_xlabel('Time (s)')
        self.ax1.set_ylabel('Availability (%)')
        self.ax1.set_title(f'Ping to {self.hostname}')
        
        self.ax2.clear()
        self.ax2.plot(self.x_data, self.y_data_packet_loss)
        self.ax2.set_xlabel('Time (s)')
        self.ax2.set_ylabel('Packet Loss (%)')
        self.ax2.set_title(f'Ping to {self.hostname}')
        
        self.canvas.draw()

        self.after(self.ping_interval * 1000, self.update_graph)

    def ping(self):
        output = subprocess.getoutput(f'ping -c 1 {self.hostname}')
        print(output)
        self.ping_count += 1

        if '1 received' in output:
            self.ping_received += 1
        else:
            self.ping_lost += 1

    def get_availability(self):
        if self.ping_count == 0:
            return 100

        return self.ping_received / self.ping_count * 100

    def get_packet_loss(self):
        if self.ping_count == 0:
            return 0

        return self.ping_lost / self.ping_count * 100

root = tk.Tk()
app = PingGraph(master=root)
app.mainloop()
