import numpy as np
import matplotlib.pyplot as plt

# Constants
R = 0.05          # Thermal resistance (°C/W)
C = 10000         # Thermal capacitance (J/°C)
T_ambient = 10    # Outside temperature (°C)
T0 = 20           # Initial room temperature (°C)
t_end = 7200      # 2 hours simulation
dt = 10           # Time step (s)

# Control thresholds
T_on = 21
T_off = 24

# Differential Equation
def dT_dt(T, t, Q):
    return (1/(R*C)) * (T_ambient - T) + Q/C

# RK4 with Control Logic
def rk4_with_control(f, T0, t):
    T = np.zeros(len(t))
    Q = np.zeros(len(t))
    T[0] = T0
    heater_on = True  # Start with heater ON

    for i in range(1, len(t)):
        # Control logic
        if T[i-1] < T_on:
            heater_on = True
        elif T[i-1] > T_off:
            heater_on = False
        
        Q[i] = 1000 if heater_on else 0

        h = t[i] - t[i-1]
        k1 = h * f(T[i-1], t[i-1], Q[i])
        k2 = h * f(T[i-1] + 0.5 * k1, t[i-1] + 0.5 * h, Q[i])
        k3 = h * f(T[i-1] + 0.5 * k2, t[i-1] + 0.5 * h, Q[i])
        k4 = h * f(T[i-1] + k3, t[i-1] + h, Q[i])
        T[i] = T[i-1] + (k1 + 2*k2 + 2*k3 + k4)/6

    return T, Q

# Time vector
t = np.arange(0, t_end + dt, dt)

# Simulate
T_sim, Q_sim = rk4_with_control(dT_dt, T0, t)

# Plot
plt.figure(figsize=(10, 5))

plt.subplot(2, 1, 1)
plt.plot(t/60, T_sim, label="Room Temperature")
plt.axhline(T_on, color='green', linestyle='--', label="Heater ON Threshold")
plt.axhline(T_off, color='red', linestyle='--', label="Heater OFF Threshold")
plt.ylabel("Temperature (°C)")
plt.title("Room Temperature with ON/OFF Heater Control")
plt.grid(True)
plt.legend()

plt.subplot(2, 1, 2)
plt.step(t/60, Q_sim, where='post', label="Heater Power (W)")
plt.ylabel("Heater Power (W)")
plt.xlabel("Time (minutes)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
