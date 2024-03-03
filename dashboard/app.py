import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime
import numpy as np

#load bikeDay
bikeDay = pd.read_excel('dashboard/bikeRental.xlsx', sheet_name='day')
bikePeriod = pd.read_excel('dashboard/bikeRental.xlsx', sheet_name='period')

def sidebar(bikeDay):
    bikeDay['dteday'] = pd.to_datetime(bikeDay['dteday'])
    min_date = bikeDay['dteday'].min()
    max_date = bikeDay['dteday'].max()
    with st.sidebar:
        st.image('https://png.pngtree.com/png-clipart/20230807/original/pngtree-vector-illustration-of-a-bicycle-rental-logo-on-a-white-background-vector-picture-image_10130406.png')

        def on_change():
            st.session_state.date =date
        
        date = st.date_input(
            label='Date Range',
            min_value=min_date,
            max_value=max_date,
            value=[min_date,max_date],
            on_change=on_change
        )
    return date

dateBar = sidebar(bikeDay)
if len(dateBar) == 2:
    main_bikeDay = bikeDay[(bikeDay['dteday'] >= str(dateBar[0])) & (bikeDay['dteday'] <= str(dateBar[1]))]
else:
    main_bikeDay = bikeDay[(bikeDay['dteday'] >= str(st.session_date[0]) & (bikeDay['dteday'] <= str(st.session_state.date[1])))]

st.sidebar.write('Dashboard by: Arlynandhita Felisya Putri Wibowo')

total = int(main_bikeDay['total'].sum())
average = round(main_bikeDay['total'].mean())
current_date = datetime.datetime.now()
def get_season(month):
    if month in range(3, 6):
        return "Spring"
    elif month in range(6, 9):
        return "Summer"
    elif month in range(9, 12): 
        return "Autumn"
    else: 
        return "Winter"
current_date = datetime.datetime.now()
current_month = current_date.month
current_season = get_season(current_month)

st.title("Bike Sharing Dashboard")
left_col, mid_col, right_col = st.columns(3)
with left_col:
    st.subheader("Rent Total:")
    st.subheader(f"{total:,}")
with mid_col:
    st.subheader("Rent Average:")
    st.subheader(f"{average:,}")
with right_col:
    st.subheader("Season Today:")
    st.subheader(f"{current_season}")

st.markdown("---")

# --- Visualization 1 ------------------------------------------
st.subheader('Total Rental Count by Month in 2011 and 2012')
totalRentMnth = bikeDay.groupby(['year','month']).agg({
    'total':'sum'
}).reset_index()

month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
totalRentMnth['month'] = pd.Categorical(totalRentMnth['month'], categories=month_order, ordered=True)
totalRentMnth = totalRentMnth.sort_values(by=['month'])

# Plotting
fig, ax = plt.subplots(figsize=(20, 12))
totalRentMnth.groupby('year').plot(kind='line', x='month', y='total', marker='o', ax=ax)
ax.tick_params(axis = 'x', labelsize=20)
ax.tick_params(axis = 'y', labelsize=20)
ax.legend(title='Year')
ax.grid(True)
st.pyplot(fig)

#---Visualization 2 ------------------------------------------------
st.subheader('Total Rental Bike in weekday and weekend by Period')

weekdayFilter = bikePeriod[bikePeriod['weekday'].isin(["Mon", "Tue", "Wed", "Thu", "Fri"])]
totalRentWeekday = weekdayFilter.groupby(['period']).agg({
    'total': ['sum', 'mean', 'max', 'min'],
})
totalRentWeekday.sort_values(('total', 'sum'), ascending=False)

weekendFilter = bikePeriod[bikePeriod['weekday'].isin(["Sun", "Sat"])]
totalRentWeekend = weekendFilter.groupby(['period']).agg({
    'total': ['sum', 'mean', 'max', 'min'],
})
totalRentWeekend.sort_values(('total', 'sum'), ascending=False)

# Plotting total rental bike for weekday by period
totalRentPeriodWeekday_sum = totalRentWeekday[('total', 'sum')].sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(20, 12))
totalRentPeriodWeekday_sum.plot(kind='bar', label='Weekday', ax=ax)

# Plotting total rental bike for weekend by period
totalRentPeriodWeekend_sum = totalRentWeekend[('total', 'sum')].sort_values(ascending=False)
totalRentPeriodWeekend_sum.plot(kind='bar', color='red', alpha=0.7, label='Weekend', ax=ax)

ax.tick_params(axis='x', rotation = 0, labelsize=20)
ax.tick_params(axis='y', labelsize=20)
ax.legend()
for i, value in enumerate(totalRentPeriodWeekday_sum):
    plt.text(i, value, str(int(value)), ha='center', va='bottom', fontsize=20)
for i, value in enumerate(totalRentPeriodWeekend_sum):
    plt.text(i, value, str(int(value)), ha='center', va='bottom', fontsize=20)


# Displaying the plot
st.pyplot(fig)

#--- Visualization 3 ---------------------------------------------------------------
st.subheader('Total Rental Bike by Weather Situation')
weather_counts = bikeDay.groupby('weathersit')['total'].mean()
fig, ax = plt.subplots(figsize=(10, 6))
# Create the bar plot
weatherEffect = sns.barplot(x=weather_counts.index, y=weather_counts.values, palette="rocket", ax=ax)

# Add labels to the bars
for bar in weatherEffect.patches:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, int(height), ha='center', va='bottom', fontsize=10)
    
ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=10)

st.pyplot(fig)

#--- Visualization 4 -----------------------------------------------------------------
st.subheader('Total Rental Bike by Season')
seasonal_trends = bikeDay.groupby('season')['total'].mean()

fig, ax = plt.subplots(figsize=(10, 6))
seasonal_trends = sns.barplot(x=seasonal_trends.index, y=seasonal_trends.values, palette="muted", ax=ax)

# Add labels to the bars
for bar in seasonal_trends.patches:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, int(height), ha='center', va='bottom', fontsize=10)
    
ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=10)
st.pyplot(fig)

#--- Visualization 5 -------------------------------------------------------------------
st.subheader('Correlation between temperature, humidity, and windspeed and the count of total rental bikes')
fig, ax = plt.subplots(figsize=(10, 6))
correlation = bikeDay[['temp','hum','windspeed','total']]
correlation = correlation.corr()
sns.heatmap(correlation, annot=True, ax=ax)
st.pyplot(fig)
#--- Visualization 6 ---------------------------------------------------------------------
st.subheader('Original Data vs Rolling Mean')
rolling_mean = bikeDay['total'].rolling(window=7).mean()

# Create a Streamlit figure
st.set_option('deprecation.showPyplotGlobalUse', False)  # Hide deprecation warning
plt.figure(figsize=(10, 6))

# Plot original data and rolling mean
plt.plot(bikeDay['total'], label='Original Data')
plt.plot(rolling_mean, color='red', label='Rolling Mean (7 days)')
plt.xlabel('Date')
plt.ylabel('Rental Count')
plt.legend()

# Display the plot using Streamlit
st.pyplot()