import streamlit as st
import pandas as pd
from utils import *

# Load the dataset
df = pd.read_csv("merged_output.csv")

# Set up the Streamlit dashboard
st.title("Zillow Listings Dashboard")

# Display the dataframe
st.write("Data Overview:")
st.dataframe(df)

# Add visualizations and other components as needed
st.subheader("Statistics")
selected_columns = ['daysOnMarket', 'home_price','home_area','land_area','Avg_Sqrt_listing','total_Pct_Change_price']  # Replace with your desired columns
st.write(df[selected_columns].describe())




st.subheader("House Price Distribution (600k to 1M)")

# Define bins from 600k to 1M
bins = list(range(600000, 1000001, 50000))
labels = [f'{int(b/1000)}k-{int(bins[i+1]/1000)}k' for i, b in enumerate(bins[:-1])]

# Filter prices to be within this range before binning
filtered_prices = df[(df['home_price'] >= 600000) & (df['home_price'] <= 1000000)]['home_price']

price_categories = pd.cut(filtered_prices, bins=bins, labels=labels, include_lowest=True)

price_counts = price_categories.value_counts().sort_index()

price_counts_df = price_counts.reset_index()
price_counts_df.columns = ['Price Range', 'Count']

st.write(price_counts_df)

st.bar_chart(data=price_counts_df.set_index('Price Range')['Count'])


# display the mean, median, min, max, and quartiles (Q1, Q3) for home prices per area
st.subheader("Home Price Statistics per Area")
if 'area' in df.columns and 'home_price' in df.columns:
    stats = df.groupby('area')['home_price'].agg(
        Mean='mean',
        Median='median',
        Min='min',
        Max='max',
        Q1=lambda x: x.quantile(0.25),
        Q3=lambda x: x.quantile(0.75)
    )
    st.dataframe(stats)
    stat_options = ['Mean', 'Median', 'Min', 'Max', 'Q1', 'Q3']
    selected_stat = st.selectbox("Select statistic to visualize per area", stat_options)
    st.bar_chart(stats[selected_stat].sort_values(ascending=False))
else:
    st.info("Required columns ('area', 'home_price') not found in the data.")



# Sidebar filters
st.sidebar.header("Filter Listings")

# Area filter
areas = df['area'].dropna().unique()
selected_area = st.sidebar.selectbox("Select Area", options=sorted(areas))

# Home price filter
enable_listing_filter = st.sidebar.checkbox("Filter by listing Price")
if enable_listing_filter:
    home_min, home_max = int(df['home_price'].min()), int(df['home_price'].max())
    home_price_range = st.sidebar.slider("Listing Price Range", home_min, home_max, (home_min, home_max))

# Optional sold price filter
enable_sold_filter = st.sidebar.checkbox("Filter by Sold Price")
if enable_sold_filter:
    sold_min_val = df['sold_price'].min()
    sold_max_val = df['sold_price'].max()
    # Provide defaults if all values are NaN
    if pd.isna(sold_min_val) or pd.isna(sold_max_val):
        sold_min, sold_max = 0, 1000000
    else:
        sold_min, sold_max = int(sold_min_val), int(sold_max_val)
    sold_price_range = st.sidebar.slider("Sold Price Range", sold_min, sold_max, (sold_min, sold_max))

# Apply filters
filtered_df = df[
    (df['area'] == selected_area)
]

if enable_sold_filter:
    filtered_df = filtered_df[filtered_df['sold_price'].between(*sold_price_range)]
if enable_listing_filter:
    filtered_df = filtered_df[filtered_df['home_price'].between(*home_price_range)]


st.subheader(f"Filtered Listings in {selected_area}")
st.write(filtered_df)

# Average Home Listing Price per Month for selected area
st.subheader(f"Average Home Listing Price per Month in {selected_area}")
if 'posted' in filtered_df.columns:
    # Ensure 'posted' is datetime
    filtered_df['posted_month'] = pd.to_datetime(filtered_df['posted']).dt.to_period('M').astype(str)
    avg_price_month_area = filtered_df.groupby('posted_month')['home_price'].mean().sort_index()
    st.line_chart(avg_price_month_area)
else:
    st.info("No 'posted' column found in the data.")


# Compute average Avg_Sqrt_listing per month for selected area
st.subheader(f"Average SQRT Listing per Month in {selected_area}")
if 'posted' in filtered_df.columns and 'Avg_Sqrt_listing' in filtered_df.columns:
    filtered_df['posted_month'] = pd.to_datetime(filtered_df['posted']).dt.to_period('M').astype(str)
    avg_sqrt_per_month = filtered_df.groupby('posted_month')['Avg_Sqrt_listing'].mean().sort_index()
    st.line_chart(avg_sqrt_per_month)
else:
    st.info("Required columns ('posted', 'Avg_Sqrt_listing') not found in the data.")



# Average Home Sold Price per Month for selected area
st.subheader(f"Average Home Sold Price per Month in {selected_area}")
if 'sold_date' in filtered_df.columns:
    sold_month = pd.to_datetime(filtered_df['sold_date']).dt.to_period('M').astype(str)
    avg_sold_price_month_area = filtered_df.groupby(sold_month)['sold_price'].mean().sort_index()
    st.line_chart(avg_sold_price_month_area)
else:
    st.info("No 'sold_date' column found in the data.")

# Compute average Avg_Sqrt_sold per month for selected area
st.subheader(f"Average Sqrt Sold per Month in {selected_area}")
if 'sold_date' in filtered_df.columns and 'Avg_Sqrt_sold' in filtered_df.columns:
    sold_month = pd.to_datetime(filtered_df['sold_date']).dt.to_period('M').astype(str)
    avg_sqrt_sold_per_month = filtered_df.groupby(sold_month)['Avg_Sqrt_sold'].mean().sort_index()
    st.line_chart(avg_sqrt_sold_per_month)
else:
    st.info("Required columns ('sold_date', 'Avg_Sqrt_sold') not found in the data.")

st.subheader(f"days On Market Statistics in {selected_area}")
if 'daysOnMarket' in filtered_df.columns:
    stats = filtered_df['daysOnMarket'].agg(
        ['mean', 'median', 'min', 'max']
    )
    q1 = filtered_df['daysOnMarket'].quantile(0.25)
    q3 = filtered_df['daysOnMarket'].quantile(0.75)
    st.write({
        'Mean': stats['mean'],
        'Median': stats['median'],
        'Min': stats['min'],
        'Max': stats['max'],
        'Q1 (25%)': q1,
        'Q3 (75%)': q3
    })
else:
    st.info("No 'daysOnMarket' column found in the data.")

