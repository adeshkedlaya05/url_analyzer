import pandas as pd
from sklearn.preprocessing import LabelEncoder
from urllib.parse import urlparse
# Load the cleaned dataset from Step 1
df = pd.read_csv(r"replace with path of cleaned_data_set.csv")  # Make sure to specify the correct path to your cleaned dataset
# Step 1: Categorize URLs into malicious (1) and non-malicious (0)
# Assuming 'benign' is non-malicious and all other types are malicious
df['type_label'] = df['type'].apply(lambda x: 0 if x == 'benign' else 1)
# Step 2: Extract Features
# URL Length
df['url_length'] = df['url'].apply(len)
# Number of Special Characters
special_chars = ['?', '&', '=', '-', '_', ':', '/']
df['num_special_chars'] = df['url'].apply(lambda x: sum(c in x for c in special_chars))
# Domain-based Features
df['domain'] = df['url'].apply(lambda x: urlparse(x).netloc)
# Ensure the 'type_label' column is present and used for labels
if 'type_label' not in df.columns:
    raise ValueError("Column 'type_label' is missing. Ensure it was created correctly.")
# Display a sample of the dataset with new features
print("\nData After Feature Engineering (Sample):\n", df.sample(5))
# Save the dataset with new features to a new CSV file
df.to_csv('feature_extracted_dataset.csv', index=False)
print("\nFeature Engineering Completed. The dataset with new features has been saved to 'feature_extracted_dataset.csv'.")
