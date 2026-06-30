# ==========================================
# 1. Upload the Dataset in Google Colab
# ==========================================
from google.colab import files
import pandas as pd

print("Please upload your 'customer_shopping_behavior.csv' file:")
uploaded = files.upload()

# Load the uploaded dataset using pandas
# (Takes the first uploaded file dynamically)
file_name = list(uploaded.keys())[0]
df = pd.read_csv(file_name)

# Display initial data
print("\n--- Data Head ---")
print(df.head())

# ==========================================
# 2. Data Cleaning & Preprocessing
# ==========================================
# Imputing missing values in Review Rating column with the median rating of the product category
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))

# Renaming columns according to snake casing for better readability
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ', '_')
df = df.rename(columns={'purchase_amount_(usd)': 'purchase_amount'})

# Create a new column: age_group
def assign_age_group(age):
    if age <= 31:
        return 'Young Adult'
    elif age <= 44:
        return 'Adult'
    elif age <= 57:
        return 'Middle-aged'
    else:
        return 'Senior'

# 2. Use .apply() to create the new column
df['age_group'] = df['age'].apply(assign_age_group)

# Create a new column: purchase_frequency_days
frequency_mapping = {
    'Fortnightly': 14, 'Weekly': 7, 'Monthly': 30, 
    'Quarterly': 90, 'Bi-Weekly': 14, 'Annually': 365, 
    'Every 3 Months': 90
}
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)

# Dropping redundant promo code used column (since it matches discount_applied)
if 'promo_code_used' in df.columns:
    df = df.drop('promo_code_used', axis=1)

print("\nData processing complete!")

# ==========================================
# 3. Save and Download the Cleaned Data
# ==========================================
output_filename = 'cleaned_customer_shopping_behavior.csv'

# Save to the Colab environment
df.to_csv(output_filename, index=False)
print(f"\nSaved successfully as '{output_filename}'")

# Trigger browser download
files.download(output_filename)
