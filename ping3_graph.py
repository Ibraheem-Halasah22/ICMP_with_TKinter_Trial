import ping3
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends import backend_tkagg
import tkinter as tk

class PingMonitor:
    def __init__(self, hostname, interval=1):
        self.hostname = hostname
        self.interval = interval
        self.timestamps = []
        self.availabilities = []
        self.root = tk.Tk()
        self.root.wm_title("Ping Monitor: " + hostname)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.fig = plt.figure(figsize=(10, 5))
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.set_ylim(0, 1)
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Availability")
        self.line, = self.ax.plot([], [])
        self.canvas = backend_tkagg.FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()
        self.animation = animation.FuncAnimation(self.fig, self.update_graphs, interval=interval*1000)

    def ping(self):
        result = ping3.ping(self.hostname)
        if result is not None:
            self.availabilities.append(1)
        else:
            self.availabilities.append(0)
        self.timestamps.append(len(self.availabilities))

    def update_graphs(self, i):
        self.ping()
        self.line.set_data(self.timestamps, self.availabilities)
        self.ax.set_xlim(0, max(10, len(self.availabilities)))
        self.canvas.draw()

    def on_closing(self):
        self.animation.event_source.stop()
        self.root.destroy()

if __name__ == "__main__":
    monitor = PingMonitor('google.com', interval=1)
    monitor.root.mainloop()
