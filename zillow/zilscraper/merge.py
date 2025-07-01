import os
import pandas as pd
import numpy as np

# Always read files relative to this script's location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build full file paths
file1 = os.path.join(BASE_DIR, 'output.json')         # from zilspider
file2 = os.path.join(BASE_DIR, 'sold_homes.json')     # from zilsoldspider



# Read the JSON files
df1 = pd.read_json(file1)
df2 = pd.read_json(file2)


if 'image_urls' in df1.columns:
    df1 = df1.drop(columns=['image_urls'])

if 'home_main_image' in df1.columns:
    df1 = df1.drop(columns=['home_main_image'])

if 'home_address_sold_Page' in df2.columns:
    df2 = df2.drop(columns=['home_address_sold_Page'])





# Merge on zpid
merged_df = pd.merge(df1, df2, on='zpid', how='left')

mask = merged_df['sold_date'] < merged_df['posted']
merged_df.loc[mask, ['sold_date', 'sold_price', 'daysOnZillow_soldPage']] = np.nan



# clean data
merged_df["sold_date"] = pd.to_datetime(merged_df["sold_date"], errors='coerce')
merged_df["posted"] = pd.to_datetime(merged_df["posted"], errors='coerce')
merged_df['area'] = merged_df['home_address'].apply(lambda x: x.split(',')[-2].strip())
merged_df.loc[merged_df["sold_date"] > merged_df["posted"], "home_status"] = "SOLD"

merged_df["Avg_Sqrt_listing"] = (
    merged_df["home_price"] / merged_df["home_area"]
).where(merged_df["home_area"] > 0).round().astype("Int64")


merged_df["Avg_Sqrt_sold"] = (
    (merged_df["sold_price"] / merged_df["home_area"])
    .where(
        (merged_df["home_area"] > 0) & (~merged_df["sold_price"].isna())
    )
    .round()
    .astype("Int64")
)



condition = (~merged_df['Avg_Sqrt_sold'].isna()) & (~merged_df['Avg_Sqrt_listing'].isna())

merged_df['difference_Avg_Sqrt'] = (
    merged_df['Avg_Sqrt_sold'] - merged_df['Avg_Sqrt_listing']
).where(condition)


condition_valid =(~merged_df['home_price'].isna()) & \
       (~merged_df['sold_price'].isna())&\
       (~merged_df['sold_date'].isna()) & \
       (~merged_df['posted'].isna())



merged_df['total_Pct_Change_price'] = np.where(
    condition_valid,
    ((merged_df['sold_price'] - merged_df['home_price']) / merged_df['home_price']) * 100,
    np.nan
)




merged_df.to_csv(r'D:\code\Python\zillow\zillow\zillow_dash\src\merged_output.csv', index=False, encoding='utf-8')

