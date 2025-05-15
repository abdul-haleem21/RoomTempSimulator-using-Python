import numpy as np
import matplotlib.pyplot as plt

# === Constants ===
R = 0.05          # Thermal resistance (°C/W)
C = 10000         # Thermal capacitance (J/°C)
T0 = 20           # Initial room temperature (°C)
t_end = 7200      # 2 hours
dt = 10           # Time step (s)

# Control thresholds
T_on = 21
T_off = 24
T_cool_on = 26
T_cool_off = 24.5

# Time vector
t = np.arange(0, t_end + dt, dt)

# Ambient temperature: sinusoidal (5°C–15°C)
T_ambient = 10 + 5 * np.sin(2 * np.pi * t / 3600)

# === Differential equation ===
def dT_dt(T, T_ambient_now, Q_heat, Q_cool):
    Q_total = Q_heat + Q_cool  # Cooling is negative
    return (1 / (R * C)) * (T_ambient_now - T) + Q_total / C

# === RK4 Solver with heater & cooler control ===
def rk4_heating_cooling(f, T0, t, T_ambient):
    T = np.zeros(len(t))
    Q_heat = np.zeros(len(t))
    Q_cool = np.zeros(len(t))
    T[0] = T0
    heater_on = True
    cooler_on = False

    for i in range(1, len(t)):
        T_prev = T[i - 1]

        # Heater control
        if T_prev < T_on:
            heater_on = True
        elif T_prev > T_off:
            heater_on = False

        # Cooler control
        if T_prev > T_cool_on:
            cooler_on = True
        elif T_prev < T_cool_off:
            cooler_on = False

        Q_heat[i] = 1000 if heater_on else 0
        Q_cool[i] = -1500 if cooler_on else 0

        h = t[i] - t[i - 1]
        T_amb_now = T_ambient[i - 1]

        k1 = h * f(T_prev, T_amb_now, Q_heat[i], Q_cool[i])
        k2 = h * f(T_prev + 0.5 * k1, T_amb_now, Q_heat[i], Q_cool[i])
        k3 = h * f(T_prev + 0.5 * k2, T_amb_now, Q_heat[i], Q_cool[i])
        k4 = h * f(T_prev + k3, T_amb_now, Q_heat[i], Q_cool[i])
        T[i] = T_prev + (k1 + 2*k2 + 2*k3 + k4) / 6

    return T, Q_heat, Q_cool

# === Run simulation ===
T_sim, Q_heat_sim, Q_cool_sim = rk4_heating_cooling(dT_dt, T0, t, T_ambient)

# === Plotting ===
plt.figure(figsize=(12, 8))

plt.subplot(4, 1, 1)
plt.plot(t / 60, T_ambient, label="Ambient Temp (°C)", color='blue')
plt.ylabel("Ambient (°C)")
plt.grid()
plt.legend()

plt.subplot(4, 1, 2)
plt.plot(t / 60, T_sim, label="Room Temp (°C)", color='orange')
plt.axhline(T_on, color='green', linestyle='--', label='Heater ON')
plt.axhline(T_off, color='red', linestyle='--', label='Heater OFF')
plt.axhline(T_cool_on, color='purple', linestyle='--', label='Cooler ON')
plt.axhline(T_cool_off, color='cyan', linestyle='--', label='Cooler OFF')
plt.ylabel("Room Temp (°C)")
plt.grid()
plt.legend()

plt.subplot(4, 1, 3)
plt.step(t / 60, Q_heat_sim, where='post', label="Heater Power (W)", color='red')
plt.ylabel("Heater (W)")
plt.grid()
plt.legend()

plt.subplot(4, 1, 4)
plt.step(t / 60, Q_cool_sim, where='post', label="Cooler Power (W)", color='blue')
plt.ylabel("Cooler (W)")
plt.xlabel("Time (minutes)")
plt.grid()
plt.legend()

plt.tight_layout()
plt.suptitle("Room Temperature Simulation with Heater and Cooler", y=1.02)
plt.show()
