import pandas as pd

benches_prices = pd.read_csv("data/benches_prices.csv", parse_dates=[0],)


rest_benches = pd.read_csv("data/rest_of_benches.csv", parse_dates=[0], thousands=',' )
rest_benches['Close'] = rest_benches['Close'].astype(float)
products_prices = pd.read_csv("data/products_prices.csv", parse_dates=[0])

combined_df = pd.concat([benches_prices, rest_benches, products_prices])

# Merge 'Unnamed: 0' into 'Date' column
combined_df['Date'] = combined_df['Date'].combine_first(combined_df['Unnamed: 0'])

# Drop the 'Unnamed: 0' column
combined_df = combined_df.drop(columns=['Unnamed: 0'])


combined_df.to_csv("data/combined_df.csv")
