import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Paste your rk4_heating_cooling and dT_dt functions here or import them

def dT_dt(T, T_ambient_now, Q_heat, Q_cool):
    R = 0.05
    C = 10000
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

# Streamlit app
st.title("Room Temperature Simulation")

# Inputs
duration_min = st.slider("Simulation Duration (minutes)", 30, 180, 120)
heater_power = st.number_input("Heater Power (W)", min_value=500, max_value=5000, value=1000)
cooler_power = st.number_input("Cooler Power (W)", min_value=500, max_value=5000, value=1500)
T_on = st.number_input("Heater ON Threshold (°C)", value=21.0)
T_off = st.number_input("Heater OFF Threshold (°C)", value=24.0)
T_cool_on = st.number_input("Cooler ON Threshold (°C)", value=26.0)
T_cool_off = st.number_input("Cooler OFF Threshold (°C)", value=24.5)

dt = 10
t_end = duration_min * 60
t = np.arange(0, t_end + dt, dt)
T0 = 20
T_ambient = 10 + 5 * np.sin(2 * np.pi * t / 3600)

if st.button("Run Simulation"):
    T_sim, Q_heat_sim, Q_cool_sim = rk4_heating_cooling(
        dT_dt, T0, t, T_ambient, T_on, T_off, T_cool_on, T_cool_off, heater_power, cooler_power)

    # Plotting results
    import matplotlib.pyplot as plt

    fig, axs = plt.subplots(4, 1, figsize=(10, 8), sharex=True)

    axs[0].plot(t / 60, T_ambient, color='blue')
    axs[0].set_ylabel("Ambient Temp (°C)")
    axs[0].grid()

    axs[1].plot(t / 60, T_sim, color='orange')
    axs[1].axhline(T_on, color='green', linestyle='--')
    axs[1].axhline(T_off, color='red', linestyle='--')
    axs[1].axhline(T_cool_on, color='purple', linestyle='--')
    axs[1].axhline(T_cool_off, color='cyan', linestyle='--')
    axs[1].set_ylabel("Room Temp (°C)")
    axs[1].grid()

    axs[2].step(t / 60, Q_heat_sim, where='post', color='red')
    axs[2].set_ylabel("Heater Power (W)")
    axs[2].grid()

    axs[3].step(t / 60, Q_cool_sim, where='post', color='blue')
    axs[3].set_ylabel("Cooler Power (W)")
    axs[3].set_xlabel("Time (minutes)")
    axs[3].grid()

    st.pyplot(fig)
