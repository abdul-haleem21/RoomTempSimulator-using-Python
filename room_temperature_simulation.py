import numpy as np
import matplotlib.pyplot as plt

# === Constants ===
R = 0.05          # Thermal resistance (°C/W)
C = 10000         # Thermal capacitance (J/°C)
T0 = 20           # Initial room temperature (°C)
t_end = 7200      # Simulation time: 2 hours in seconds
dt = 10           # Time step (s)

# Control thresholds
T_on = 21         # Turn heater ON below this
T_off = 24        # Turn heater OFF above this

# === Time vector ===
t = np.arange(0, t_end + dt, dt)

# === Varying ambient temperature: sinusoidal fluctuation ===
T_ambient = 10 + 5 * np.sin(2 * np.pi * t / 3600)  # Oscillates every hour from 5°C to 15°C

# === Differential equation ===
def dT_dt(T, T_ambient_now, Q):
    return (1 / (R * C)) * (T_ambient_now - T) + Q / C

# === RK4 with ON/OFF control ===
def rk4_with_control(f, T0, t, T_ambient):
    T = np.zeros(len(t))     # Room temperature
    Q = np.zeros(len(t))     # Heater power at each time step
    T[0] = T0
    heater_on = True         # Start with heater ON

    for i in range(1, len(t)):
        # Control logic
        if T[i-1] < T_on:
            heater_on = True
        elif T[i-1] > T_off:
            heater_on = False
        
        Q[i] = 1000 if heater_on else 0  # Power in watts

        h = t[i] - t[i-1]
        T_amb_now = T_ambient[i-1]

        k1 = h * f(T[i-1], T_amb_now, Q[i])
        k2 = h * f(T[i-1] + 0.5 * k1, T_amb_now, Q[i])
        k3 = h * f(T[i-1] + 0.5 * k2, T_amb_now, Q[i])
        k4 = h * f(T[i-1] + k3, T_amb_now, Q[i])
        T[i] = T[i-1] + (k1 + 2*k2 + 2*k3 + k4) / 6

    return T, Q

# === Run Simulation ===
T_sim, Q_sim = rk4_with_control(dT_dt, T0, t, T_ambient)

# === Plotting ===
plt.figure(figsize=(12, 6))

plt.subplot(3, 1, 1)
plt.plot(t / 60, T_ambient, color='blue', label='Ambient Temperature')
plt.ylabel("Ambient Temp (°C)")
plt.grid(True)
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(t / 60, T_sim, color='orange', label='Room Temperature')
plt.axhline(T_on, color='green', linestyle='--', label="Heater ON Threshold")
plt.axhline(T_off, color='red', linestyle='--', label="Heater OFF Threshold")
plt.ylabel("Room Temp (°C)")
plt.grid(True)
plt.legend()

plt.subplot(3, 1, 3)
plt.step(t / 60, Q_sim, where='post', color='black', label="Heater Power")
plt.ylabel("Power (W)")
plt.xlabel("Time (minutes)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.suptitle("Room Temperature Simulation with Varying Ambient Temp & Heater Control", y=1.02)
plt.show()
# This code simulates the room temperature over time with a heater that turns on and off based on the current temperature.
# The ambient temperature varies sinusoidally, and the heater's power is controlled based on the defined thresholds.