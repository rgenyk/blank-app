# Import necessary libraries  
import streamlit as st  
import numpy as np  
import matplotlib.pyplot as plt  
  
# Title of the app  
st.title("Matplotlib in Streamlit")  
  
# Description  
st.write("This is a simple Streamlit app that plots a sine wave using matplotlib.")  
  
# Generate sample data for the plot  
x = np.linspace(0, 10, 100)  
y = np.sin(x)  
  
# Create the plot following a scientific and elegant theme  
fig, ax = plt.subplots(figsize=(9, 6))  
plt.subplots_adjust(left=0.15, right=0.85, top=0.85, bottom=0.15)  
  
# Plot the sine wave  
ax.plot(x, y, color='#766CDB', label='sin(x)')  
  
# Set title and labels with specified formatting  
ax.set_title("Sine Wave", pad=15, fontsize=20, fontweight='semibold', color='#222222')  
ax.set_xlabel("X axis", labelpad=10, fontsize=16, fontweight='medium', color='#333333')  
ax.set_ylabel("Y axis", labelpad=10, fontsize=16, fontweight='medium', color='#333333')  
  
# Configure tick labels  
ax.tick_params(labelsize=14, colors='#555555')  
  
# Style grid and axes  
ax.grid(True, color='#E0E0E0')  
ax.set_axisbelow(True)  
ax.legend(fontsize=12, loc='lower center')  
  
# Display the plot in the Streamlit app  
st.pyplot(fig)  
  
# Footer  
st.write("Streamlit app with matplotlib visualization is now working!")  