import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Simulation functions ---

R = 0.05
C = 10000
T0 = 20
dt = 10

def dT_dt(T, T_ambient_now, Q_heat, Q_cool):
    Q_total = Q_heat + Q_cool
    return (1 / (R * C)) * (T_ambient_now - T) + Q_total / C

def rk4_heating_cooling(f, T0, t, T_ambient, T_on, T_off, T_cool_on, T_cool_off, heater_power, cooler_power):
    T = np.zeros(len(t))
    Q_heat = np.zeros(len(t))
    Q_cool = np.zeros(len(t))
    T[0] = T0
    heater_on = True
    cooler_on = False

    for i in range(1, len(t)):
        T_prev = T[i - 1]

        if T_prev < T_on:
            heater_on = True
        elif T_prev > T_off:
            heater_on = False

        if T_prev > T_cool_on:
            cooler_on = True
        elif T_prev < T_cool_off:
            cooler_on = False

        Q_heat[i] = heater_power if heater_on else 0
        Q_cool[i] = -cooler_power if cooler_on else 0

        h = t[i] - t[i - 1]
        T_amb_now = T_ambient[i - 1]

        k1 = h * f(T_prev, T_amb_now, Q_heat[i], Q_cool[i])
        k2 = h * f(T_prev + 0.5 * k1, T_amb_now, Q_heat[i], Q_cool[i])
        k3 = h * f(T_prev + 0.5 * k2, T_amb_now, Q_heat[i], Q_cool[i])
        k4 = h * f(T_prev + k3, T_amb_now, Q_heat[i], Q_cool[i])
        T[i] = T_prev + (k1 + 2*k2 + 2*k3 + k4) / 6

    return T, Q_heat, Q_cool

# --- GUI Setup ---

class RoomTempApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Room Temperature Simulator")
        self.geometry("800x700")

        # Inputs frame
        frame = ttk.Frame(self)
        frame.pack(pady=10)

        # Duration
        ttk.Label(frame, text="Duration (minutes):").grid(row=0, column=0, sticky="w")
        self.duration_var = tk.IntVar(value=120)
        ttk.Entry(frame, textvariable=self.duration_var, width=10).grid(row=0, column=1)

        # Heater power
        ttk.Label(frame, text="Heater Power (W):").grid(row=1, column=0, sticky="w")
        self.heater_power_var = tk.IntVar(value=1000)
        ttk.Entry(frame, textvariable=self.heater_power_var, width=10).grid(row=1, column=1)

        # Cooler power
        ttk.Label(frame, text="Cooler Power (W):").grid(row=2, column=0, sticky="w")
        self.cooler_power_var = tk.IntVar(value=1500)
        ttk.Entry(frame, textvariable=self.cooler_power_var, width=10).grid(row=2, column=1)

        # Temp thresholds
        ttk.Label(frame, text="Heater ON Threshold (°C):").grid(row=3, column=0, sticky="w")
        self.T_on_var = tk.DoubleVar(value=21.0)
        ttk.Entry(frame, textvariable=self.T_on_var, width=10).grid(row=3, column=1)

        ttk.Label(frame, text="Heater OFF Threshold (°C):").grid(row=4, column=0, sticky="w")
        self.T_off_var = tk.DoubleVar(value=24.0)
        ttk.Entry(frame, textvariable=self.T_off_var, width=10).grid(row=4, column=1)

        ttk.Label(frame, text="Cooler ON Threshold (°C):").grid(row=5, column=0, sticky="w")
        self.T_cool_on_var = tk.DoubleVar(value=26.0)
        ttk.Entry(frame, textvariable=self.T_cool_on_var, width=10).grid(row=5, column=1)

        ttk.Label(frame, text="Cooler OFF Threshold (°C):").grid(row=6, column=0, sticky="w")
        self.T_cool_off_var = tk.DoubleVar(value=24.5)
        ttk.Entry(frame, textvariable=self.T_cool_off_var, width=10).grid(row=6, column=1)

        # Run button
        self.run_button = ttk.Button(frame, text="Run Simulation", command=self.run_simulation)
        self.run_button.grid(row=7, column=0, columnspan=2, pady=10)

        # Matplotlib figure
        self.fig, self.axs = plt.subplots(4, 1, figsize=(7, 8), sharex=True)
        plt.tight_layout(pad=3)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack()

    def run_simulation(self):
        try:
            duration_min = self.duration_var.get()
            heater_power = self.heater_power_var.get()
            cooler_power = self.cooler_power_var.get()
            T_on = self.T_on_var.get()
            T_off = self.T_off_var.get()
            T_cool_on = self.T_cool_on_var.get()
            T_cool_off = self.T_cool_off_var.get()

            t_end = duration_min * 60
            t = np.arange(0, t_end + dt, dt)
            T_ambient = 10 + 5 * np.sin(2 * np.pi * t / 3600)

            T_sim, Q_heat_sim, Q_cool_sim = rk4_heating_cooling(
                dT_dt, T0, t, T_ambient, T_on, T_off, T_cool_on, T_cool_off, heater_power, cooler_power
            )

            # Clear previous plots
            for ax in self.axs:
                ax.clear()

            self.axs[0].plot(t / 60, T_ambient, color='blue')
            self.axs[0].set_ylabel("Ambient Temp (°C)")
            self.axs[0].grid()

            self.axs[1].plot(t / 60, T_sim, color='orange')
            self.axs[1].axhline(T_on, color='green', linestyle='--')
            self.axs[1].axhline(T_off, color='red', linestyle='--')
            self.axs[1].axhline(T_cool_on, color='purple', linestyle='--')
            self.axs[1].axhline(T_cool_off, color='cyan', linestyle='--')
            self.axs[1].set_ylabel("Room Temp (°C)")
            self.axs[1].grid()

            self.axs[2].step(t / 60, Q_heat_sim, where='post', color='red')
            self.axs[2].set_ylabel("Heater Power (W)")
            self.axs[2].grid()

            self.axs[3].step(t / 60, Q_cool_sim, where='post', color='blue')
            self.axs[3].set_ylabel("Cooler Power (W)")
            self.axs[3].set_xlabel("Time (minutes)")
            self.axs[3].grid()

            self.fig.suptitle("Room Temperature Simulation", fontsize=14)
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = RoomTempApp()
    app.mainloop()
