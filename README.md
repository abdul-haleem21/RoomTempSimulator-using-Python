# RoomTempSimulator-using-Python
Room Temperature Simulator: Numerical modeling of HVAC heating and cooling control using RK4 integration with Python Tkinter GUI and streamlit

# Room Temperature Simulator

This project models and simulates room temperature control with heating and cooling systems using numerical methods.  
The room's thermal dynamics are solved using the 4th order Runge-Kutta (RK4) method applied to the differential equations governing heat transfer.

---

## Features

- **Numerical Simulation:** Uses RK4 integration to solve the thermal dynamic ODE for room temperature.
- **Dynamic Ambient Temperature:** Ambient temperature varies sinusoidally to mimic daily temperature cycles.
- **Heating and Cooling Control:** Heater and cooler are automatically turned ON/OFF based on user-defined temperature thresholds.
- **Interactive GUI:** Tkinter-based graphical interface allows users to adjust parameters and visualize results in real-time.
- **Plots:** Temperature, heater power, cooler power, and ambient temperature are plotted over the simulation time.

---

## Installation

Make sure you have Python 3.x installed.  
Install the required dependencies using pip:

pip install numpy matplotlib
