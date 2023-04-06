import subprocess
import tkinter as tk
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class PingMonitor:
    def __init__(self, hostname, interval=1):
        self.hostname = hostname
        self.interval = interval
        self.availability_data = []
        self.packet_loss_data = []
        self.timestamps = [datetime.now()]

        self.root = tk.Tk()
        self.root.title(f"Ping Monitor - {hostname}")

        self.availability_fig = Figure(figsize=(5, 3), dpi=100)
        self.availability_ax = self.availability_fig.add_subplot(111)
        self.availability_ax.set_ylim(0, 1)
        self.availability_ax.set_xlim(0, 60)
        self.availability_ax.set_ylabel('Availability')
        self.availability_ax.set_xlabel('Time (s)')
        self.availability_ax.grid(True)
        self.availability_canvas = FigureCanvasTkAgg(self.availability_fig, self.root)
        self.availability_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.packet_loss_fig = Figure(figsize=(5, 3), dpi=100)
        self.packet_loss_ax = self.packet_loss_fig.add_subplot(111)
        self.packet_loss_ax.set_ylim(0, 100)
        self.packet_loss_ax.set_xlim(0, 60)
        self.packet_loss_ax.set_ylabel('Packet Loss (%)')
        self.packet_loss_ax.set_xlabel('Time (s)')
        self.packet_loss_ax.grid(True)
        self.packet_loss_canvas = FigureCanvasTkAgg(self.packet_loss_fig, self.root)
        self.packet_loss_canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.ping()

    def ping(self):
        output = subprocess.getoutput(f'ping -n 1 {self.hostname}')
        if 'could not find host' in output:
            packet_loss = 100
            availability = 0
        else:
            packet_loss = 100 if 'packet loss' in output else 0
            availability = 1 if packet_loss == 0 else 0
        self.availability_data.append(availability)
        self.packet_loss_data.append(packet_loss)
        self.update_graphs()
        self.root.after(self.interval * 1000, self.ping)

    def update_graphs(self):
        now = datetime.now()
        elapsed_time = [(now - dt).seconds for dt in self.timestamps]
        self.availability_ax.plot(elapsed_time, self.availability_data, 'b-')
        self.packet_loss_ax.plot(elapsed_time, self.packet_loss_data, 'r-')
        self.availability_canvas.draw()
        self.packet_loss_canvas.draw()
        self.timestamps.append(now)

monitor = PingMonitor('google.com', interval=1)
tk.mainloop()
