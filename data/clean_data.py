import pandas as pd

# Load the raw dataset
df = pd.read_csv("Raw_ECommerce_Dataset.csv")

# Step 1: Inspect the data
print(df.info())
print(df.isnull().sum())

# Step 2: Handle missing values
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce')
df['Avg Order Value'] = pd.to_numeric(df['Avg Order Value'], errors='coerce')
df.dropna(subset=['CustomerName', 'Amount', 'Profit'], inplace=True)

# Step 3: Convert data types
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
df['Quantity'] = df['Quantity'].fillna(0).astype(int)

# Step 4: Standardize categorical columns
df['State'] = df['State'].str.strip().str.title()
df['City'] = df['City'].str.strip().str.title()
df['Category'] = df['Category'].str.strip().str.title()

# Step 5: Remove duplicates
df.drop_duplicates(inplace=True)

# Step 6: Save cleaned data
df.to_csv("Enhanced_ECommerce_Dataset.csv", index=False)

print("Data cleaned and saved successfully.")
