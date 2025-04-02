# Import necessary libraries  
import streamlit as st  
import numpy as np  
import plotly.graph_objects as go  
  
# Title of the app  
st.title("Sine Wave Visualization")  
  
# Description  
st.write("This is a simple Streamlit app that plots a sine wave using Plotly.")  
  
# Generate sample data for the plot  
x = np.linspace(0, 10, 100)  
y = np.sin(x)  
  
# Create a Plotly figure  
fig = go.Figure()  
  
# Add the sine wave trace  
fig.add_trace(go.Scatter(  
    x=x,   
    y=y,  
    mode='lines',  
    name='sin(x)',  
    line=dict(color='#766CDB', width=3)  
))  
  
# Update layout for a professional look  
fig.update_layout(  
    title={  
        'text': "Sine Wave",  
        'y':0.9,  
        'x':0.5,  
        'xanchor': 'center',  
        'yanchor': 'top',  
        'font': dict(size=24, color='#222222', family="Arial, sans-serif")  
    },  
    xaxis_title={  
        'text': "X axis",  
        'font': dict(size=18, color='#333333', family="Arial, sans-serif")  
    },  
    yaxis_title={  
        'text': "Y axis",  
        'font': dict(size=18, color='#333333', family="Arial, sans-serif")  
    },  
    xaxis=dict(  
        tickfont=dict(size=14, color='#555555'),  
        gridcolor='#E0E0E0',  
        showline=True,  
        linewidth=1,  
        linecolor='#333333'  
    ),  
    yaxis=dict(  
        tickfont=dict(size=14, color='#555555'),  
        gridcolor='#E0E0E0',  
        showline=True,  
        linewidth=1,  
        linecolor='#333333'  
    ),  
    plot_bgcolor='white',  
    legend=dict(  
        yanchor="top",  
        y=0.99,  
        xanchor="left",  
        x=0.01,  
        font=dict(size=14, color='#333333')  
    ),  
    width=800,  
    height=500,  
    margin=dict(l=80, r=80, t=100, b=80),  
)  
  
# Display the plot in the Streamlit app  
st.plotly_chart(fig, use_container_width=True)  
  
# Add interactive elements  
st.subheader("Interactive Controls")  
frequency = st.slider("Frequency", min_value=0.1, max_value=2.0, value=1.0, step=0.1)  
amplitude = st.slider("Amplitude", min_value=0.1, max_value=2.0, value=1.0, step=0.1)  
  
if st.button("Update Plot"):  
    y_new = amplitude * np.sin(frequency * x)  
    # Create a new Plotly figure for the updated plot  
    fig_new = go.Figure()  
    fig_new.add_trace(go.Scatter(  
        x=x,   
        y=y_new,  
        mode='lines',  
        name=f'{amplitude}*sin({frequency}x)',  
        line=dict(color='#766CDB', width=3)  
    ))  
    fig_new.update_layout(  
        title={  
            'text': f"Sine Wave: {amplitude}*sin({frequency}x)",  
            'y':0.9,  
            'x':0.5,  
            'xanchor': 'center',  
            'yanchor': 'top',  
            'font': dict(size=24, color='#222222', family="Arial, sans-serif")  
        },  
        xaxis_title={  
            'text': "X axis",  
            'font': dict(size=18, color='#333333', family="Arial, sans-serif")  
        },  
        yaxis_title={  
            'text': "Y axis",  
            'font': dict(size=18, color='#333333', family="Arial, sans-serif")  
        },  
        xaxis=dict(  
            tickfont=dict(size=14, color='#555555'),  
            gridcolor='#E0E0E0',  
            showline=True,  
            linewidth=1,  
            linecolor='#333333'  
        ),  
        yaxis=dict(  
            tickfont=dict(size=14, color='#555555'),  
            gridcolor='#E0E0E0',  
            showline=True,  
            linewidth=1,  
            linecolor='#333333'  
        ),  
        plot_bgcolor='white',  
        legend=dict(  
            yanchor="top",  
            y=0.99,  
            xanchor="left",  
            x=0.01,  
            font=dict(size=14, color='#333333')  
        ),  
        width=800,  
        height=500,  
        margin=dict(l=80, r=80, t=100, b=80),  
    )  
    st.plotly_chart(fig_new, use_container_width=True)  
  
st.write("Streamlit app with Plotly visualization is now working!")  