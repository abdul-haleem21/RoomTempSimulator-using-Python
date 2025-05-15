# Title: "Smart HVAC Control System: Thermal Modeling and Optimization using Runge-Kutta and Project Management Principles"

 # Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt

  # Define the parameters for the thermal model
     # R is the thermal resistance (°C/W)
     # C is the thermal capacitance (J/°C)
     # T_ambient is the outside temperature (°C)
     # Q is the heat input (W)
     # T0 is the initial temperature (°C)
     # t_end is the simulation time (s)
     # dt is the time step (s)
  
  # Given Parameters
R = 0.05  # Thermal resistance (°C/W)
C = 10000 # Thermal capacitance (J/°C)
T_ambient = 10  # Outside temperature (°C)
Q = 1000  # Heat input (W)
T0 = 20  # Initial temperature (°C)
t_end = 3600  # Simulation time (s)
dt = 10  # Time step (s)

# Differential equation for the thermal model
def dT_dt(T, t, Q): # T is the current temperature, t is time, Q is heat input
    return (1/(R * C)) * (T_ambient - T) + Q/C # This is the equation of the thermal model


# Runge-Kutta 4th order method for solving ODEs 
def runge_kutta_4th_order(f, T0, t, Q): # f is the function, T0 is the initial temperature, t is time, Q is heat input
    T = np.zeros(len(t)) # Initialize the temperature array
    T[0] = T0 # Set the initial temperature
    for i in range(1, len(t)):
        h = t[i] -t[i - 1] # Calculate the time step
        k1 = h * f(T[i - 1], t[i - 1], Q) # Calculate k1
        k2 = h * f(T[i - 1] + 0.5 * k1, t[i - 1] + 0.5 * h, Q) # Calculate k2
        k3 = h * f(T[i - 1] + 0.5 * k2, t[i - 1] + 0.5 * h, Q) # Calculate k3
        k4 = h * f(T[i - 1] + k3, t[i - 1] + h, Q) # Calculate k4
        T[i] = T[i - 1] + (k1 + 2 * k2 + 2 * k3 + k4)/6 # Update the temperature
    return T # Return the temperature array

# Time Array or Vector
t = np.arange(0, t_end + dt, dt) # Create a time array from 0 to t_end with step dt

# simulate the thermal model using Runge-Kutta method
T_sim =  runge_kutta_4th_order(dT_dt, T0, t, Q) # Call the Runge-Kutta function to simulate the thermal model

# Plotting the results
plt.plot(t/60, T_sim, label="Room Temperature") # Plot the simulated temperature
plt.axhline(T_ambient, color='gray', linestyle='--', label="Ambient Temp") # Plot the ambient temperature
plt.xlabel("Time (minutes)") # Set the labels for x and y axes
plt.ylabel("Temperature (°C)") # Set the labels for x and y axes
plt.title("Room Temperature vs Time (Heater ON)") # Set the title of the plot
plt.legend() # Add legend to the plot
plt.grid(True) # Add grid for better readability
plt.show() # Display the plot