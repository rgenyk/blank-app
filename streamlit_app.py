import streamlit as st  
import pandas as pd  
import matplotlib.pyplot as plt  
#import seaborn as sns  
import numpy as np  
from datetime import datetime, timedelta  
import io  

st.title("Entry Time Analysis")  
st.write("Drag and drop your CSV file to visualize Normalized P/L by day of week and time.")  
  
# File uploader widget for drag and drop  
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])  
  
if uploaded_file is not None:  
    try:  
        # Read the CSV file into a DataFrame  
        df = pd.read_csv(uploaded_file)  
        st.success("File uploaded successfully!")  
          
        # Optionally display the raw data  
        if st.checkbox("Show raw data"):  
            st.dataframe(df.head())  
  
        # Data processing:  
        # Convert 'Date Opened' to datetime and create 'Day of Week' column  
        df['Date Opened'] = pd.to_datetime(df['Date Opened'])  
        df['Day of Week'] = df['Date Opened'].dt.day_name()  
          
        # Calculate Normalized P/L using: (P/L / Premium) * max(Premium)  
        max_premium = df['Premium'].max()  
        df['Normalized P/L'] = (df['P/L'] / df['Premium']) * max_premium  
          
        # Create the overall pivot table: index = 'Time Opened', columns = day of week (Monday to Friday)  
        pivot_table = df.pivot_table(index='Time Opened', columns='Day of Week', values='Normalized P/L', aggfunc='mean')  
        rounded_pivot_table = pivot_table.round(0)  
        ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']  
        # Filter columns that exist in the data  
        existing_days = [day for day in ordered_days if day in rounded_pivot_table.columns]  
        rounded_pivot_table = rounded_pivot_table[existing_days]  
          
        # Create a second pivot table for entries within the last 90 days  
        ninety_days_ago = datetime.now() - timedelta(days=90)  
        recent_df = df[df['Date Opened'] >= ninety_days_ago]  
        recent_pivot_table = recent_df.pivot_table(index='Time Opened', columns='Day of Week', values='Normalized P/L', aggfunc='mean').round(0)  
        # Make sure to only include the ordered days that exist in recent data  
        existing_recent_days = [day for day in ordered_days if day in recent_pivot_table.columns]  
        recent_pivot_table = recent_pivot_table[existing_recent_days]  
          
        # Combine the two pivot tables:  
        overall_table = rounded_pivot_table.copy()  
        overall_table.columns = ['Overall ' + col for col in overall_table.columns]  
        recent_table = recent_pivot_table.copy()  
        recent_table.columns = ['Recent ' + col for col in recent_table.columns]  
        combined_table = overall_table.join(recent_table, how='outer')  
          
        # Reorder columns: for each day, group Overall and Recent side by side  
        ordered_columns = []  
        for day in ordered_days:  
            overall_col = 'Overall ' + day  
            recent_col = 'Recent ' + day  
            if overall_col in combined_table.columns:  
                ordered_columns.append(overall_col)  
            if recent_col in combined_table.columns:  
                ordered_columns.append(recent_col)  
        combined_table = combined_table[ordered_columns]  
          
        # Display the combined table  
        st.subheader("Combined Table (Overall & Recent)")  
        st.dataframe(combined_table)  
          
        # Create a heatmap from the combined table  
        plt.figure(figsize=(14, 10))  
        sns.heatmap(combined_table, annot=True, fmt='.0f', cmap='coolwarm',   
                    cbar_kws={'label': 'Normalized P/L'}, linewidths=0.5)  
        plt.title("Overall vs Recent Normalized P/L Heatmap", fontsize=20, pad=15)  
        plt.xlabel("Day of Week (Overall and Recent)", fontsize=16, labelpad=10)  
        plt.ylabel("Time Opened", fontsize=16, labelpad=10)  
        plt.tight_layout()  
          
        # Render the plot in Streamlit  
        st.pyplot(plt.gcf())  
          
        # Optionally, allow download of the figure as PNG  
        buf = io.BytesIO()  
        plt.savefig(buf, format="png", dpi=300)  
        buf.seek(0)  
        st.download_button("Download Heatmap", data=buf, file_name="trading_heatmap.png", mime="image/png")  
          
    except Exception as e:  
        st.error("Error processing file: " + str(e))  
else:  
    st.info("Please upload a CSV file to begin the analysis.")  
  
# Sidebar with additional information  
with st.sidebar:  
    st.header("About This App")  
    st.write(  
        "This application analyzes options trading data to visualize performance patterns by day of the week and time of day.\n\n"  
        "The heatmap displays both overall historical performance and recent performance (last 90 days), "  
        "with Normalized P/L computed as: $$\\text{Normalized P/L} = \\left(\\frac{P/L}{Premium}\\right) \\times \\max(Premium)$$."  
    )  
    st.header("Instructions")  
    st.write(  
        "1. Upload your CSV file using the drag and drop area above.\n"  
        "2. Optionally display the raw data.\n"  
        "3. The app processes the data, generating two pivot tables and combining them.\n"  
        "4. The resulting heatmap allows you to compare Overall vs. Recent performance side by side for each day of the week.\n"  
        "5. You can download the heatmap as a PNG file."  
    )  