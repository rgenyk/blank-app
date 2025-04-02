import streamlit as st  
import pandas as pd  
import seaborn as sns  
import matplotlib.pyplot as plt  
import numpy as np  
from datetime import datetime, timedelta  
import io  
from matplotlib.colors import ListedColormap  
  
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
        pivot_table = df.pivot_table(index='Time Opened', columns='Day of Week',   
                                     values='Normalized P/L', aggfunc='mean')  
        rounded_pivot_table = pivot_table.round(0)  
        ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']  
        # Filter columns that exist in the data  
        existing_days = [day for day in ordered_days if day in rounded_pivot_table.columns]  
        overall_table = rounded_pivot_table[existing_days].copy()  
        # Rename columns by adding "365d" prefix  
        overall_table = overall_table.rename(columns=lambda x: "365d " + x)  
          
        # Create a second pivot table for entries within the last 90 days   
        ninety_days_ago = datetime.now() - timedelta(days=90)  
        recent_df = df[df['Date Opened'] >= ninety_days_ago]  
        recent_pivot_table = recent_df.pivot_table(index='Time Opened', columns='Day of Week',   
                                                   values='Normalized P/L', aggfunc='mean')  
        rounded_recent_table = recent_pivot_table.round(0)  
        # Filter and rename columns with "90d" prefix  
        recent_table = rounded_recent_table[existing_days].copy()  
        recent_table = recent_table.rename(columns=lambda x: "90d " + x)  
          
        # Combine the two tables side by side on the index  
        combined_table = overall_table.join(recent_table)  
          
        # --- Create a mask matrix for custom coloring ---  
        # For each column calculate column average and mark as 1 when cell > average, else 0.  
        mask_matrix = combined_table.copy()  
        for col in combined_table.columns:  
            col_avg = combined_table[col].mean()  
            mask_matrix[col] = np.where(combined_table[col] > col_avg, 1, 0)  
          
        # Create a binary custom colormap: 0 -> white, 1 -> green  
        cmap = ListedColormap(["white", "green"])  
          
        # --- Create a heatmap using the mask with annotations from combined_table ---  
        plt.figure(figsize=(14, 10))  
        ax = sns.heatmap(mask_matrix, annot=combined_table, fmt='.0f',   
                         cmap=cmap, cbar=False, vmin=0, vmax=1, linewidths=0.5)  
        ax.xaxis.tick_top()                # Move the x-axis labels to the top  
        ax.xaxis.set_label_position('top') # Ensure any x-axis label appears at the top  
        plt.xticks(rotation=45, ha='left')  
        plt.title("365d vs 90d Normalized P/L Heatmap", fontsize=20, pad=15)  
        plt.xlabel("Day of Week", fontsize=16, labelpad=10)  
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
        "This application analyzes options trading data to visualize performance patterns "  
        "by day of the week and time of day.\n\n"  
        "The heatmap displays both overall historical performance (365d) and recent performance (90d), "  
        "with Normalized P/L computed as: $$\\text{Normalized P/L} = \\left(\\frac{P/L}{Premium}\\right) \\times \\max(Premium)$$."  
    )  
    st.header("Instructions")  
    st.write(  
        "1. Upload your CSV file using the drag and drop area above.\n"  
        "2. Optionally display the raw data.\n"  
        "3. The app processes the data, generating two pivot tables (365d and 90d) and combines them.\n"  
        "4. The heatmap highlights cells in green if they are above the column average.\n"  
        "5. You can download the heatmap as a PNG file."  
    )  