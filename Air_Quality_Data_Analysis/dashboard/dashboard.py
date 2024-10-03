import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
sns.set(style='dark')

# Title page
st.set_page_config(page_title="Air Quality Index Analysis by dhimas_pram71")
# Load dataset
data = pd.read_csv("Final_data.csv")

# Title of the dashboard
st.title('Air Quality Analysis Dashboard  :sparkles:')

st.markdown("""
# About Me
- **Nama:** Dhimas Pramudya Tridharma
- **Email:** dhimas.pramudya.71@gmail.com
- **ID Dicoding:** [dhimas_pram71] https://www.dicoding.com/users/dhimas_pram71/
""")
data['date'] = pd.to_datetime(data[['year', 'month', 'day']])

min_date = data["date"].min()
max_date = data["date"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://lh3.googleusercontent.com/NtORZkpsdeRJDkdA4DdUYwMUdpL1pNNO1HOVby1F6Qst1jwx6yVRkDmHJeaOtWzFLQWMPZxU_XFurb3646KdxYX8n7cYNoJeC0kpiVOhPWhayI5Z6e0X=w600")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = data[(data["date"] >= str(start_date)) & 
                (data["date"] <= str(end_date))]
st.subheader("Monthly Air Quality Index")

mean_data = main_df.groupby("station")[["AQI"]].mean()
x = mean_data.index
y = mean_data["AQI"]

# Normalize AQI values to map color gradient
norm_y = (y - y.min()) / (y.max() - y.min())
colors = plt.cm.RdYlGn(1 - norm_y)  # Use a green to red color map

st.write(f"### Rentang Waktu: {start_date} hingga {end_date}")

# Create a bar plot with color gradient
fig, ax = plt.subplots()
ax.bar(x, y, color=colors)
ax.set_xticks(range(len(x)))
ax.set_xticklabels(x, rotation=90)
plt.title('Rata-rata Kualitas udara di Stasiun')
plt.xlabel("Stasiun")
plt.ylabel("Mean kualitas udara")

# Display the plot in Streamlit
st.pyplot(fig)

st.markdown("""
### Penjelasan Warna:
- Blok berwarna **Hijau**: Menandakan kualitas udara yang **bagus**.
- Blok berwarna **Merah**: Menandakan kualitas udara yang **buruk**.
- Blok berwarna **Kuning** atau **Oranye**: Menandakan kualitas udara yang **sedang**.
""")

main_df.set_index('date', inplace=True)


AQI_by_month = main_df.groupby('station').resample('D').mean().reset_index()

# Get unique stations
stations = AQI_by_month['station'].unique()

# Loop through each station and plot AQI over time
for station in stations:
    station_data = AQI_by_month[AQI_by_month['station'] == station]

    # Create a figure and axis for each station's AQI plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(station_data['date'], station_data['AQI'], label=station, color='b', marker='o')

    # Set the title and labels
    ax.set_title(f"Monthly AQI for Station: {station}")
    ax.set_xlabel('Date')
    ax.set_ylabel('AQI')
    plt.xticks(rotation=60, horizontalalignment='right', fontsize=10)

    # Display the plot in Streamlit
    st.pyplot(fig)

polutant_sum = main_df.iloc[:,5:11].sum()

labels = polutant_sum.index
sizes = polutant_sum.values
colors = ['lightblue', 'lightgreen', 'lightcoral', 'gold', 'violet', 'lightyellow']

plt.figure(figsize=(8, 6))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
fig = px.pie(values=sizes, names=labels, title='Pollutant Distribution')
# plt.axis('equal')
# plt.title('Total Concentrations of Pollutants')
st.plotly_chart(fig)