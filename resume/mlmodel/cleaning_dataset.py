# Step 1: Import necessary libraries
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
# Step 2: Load the dataset
# Replace 'path_to_dataset.csv' with the actual path to your CSV file
df = pd.read_csv(r"path to your dataset")
# Step 3: Explore the dataset
print("Dataset Shape:", df.shape)
print("\nFirst 5 Rows:\n", df.head())
print("\nDataset Info:")
print(df.info())
print("\nMissing Values in Each Column:\n", df.isnull().sum())
missing_percent = df.isnull().sum() / len(df) * 100
print("\nPercentage of Missing Values:\n", missing_percent)
# Step 4: Data Cleaning
# Remove duplicate rows if any
num_duplicates = df.duplicated().sum()
print("\nNumber of Duplicated Rows:", num_duplicates)
if num_duplicates > 0:
    df.drop_duplicates(inplace=True)
    print("Dataset Shape after removing duplicates:", df.shape)
# Handling Missing Values
if 'url' in df.columns:
    df['url'].fillna('unknown_url', inplace=True)

if 'type' in df.columns:
    df['type'].fillna(df['type'].mode()[0], inplace=True)
# Step 5: Feature Encoding
if 'type' in df.columns:
    le = LabelEncoder()
    df['type_label'] = le.fit_transform(df['type'])
# Verify Encoding
print("\nType Value Counts (after encoding):")
print(df['type_label'].value_counts())
# Optional: Print unique label mapping
label_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
print("\nLabel Mapping:", label_mapping)
# Step 6: Sample and Plot
sample_size = 1000  # Adjust as needed
if len(df) < sample_size:
    sample_size = len(df)
sample_df = df.sample(n=sample_size, random_state=42)
# Save the cleaned and preprocessed dataset to a new CSV file in a specified path
output_path = r"cleaned_dataset.csv file would be created"
df.to_csv(output_path, index=False)
# Plotting
plt.figure(figsize=(10, 6))
sns.countplot(x=sample_df['type_label'])
plt.title("Distribution of Types (Labels) in Sampled Data")
plt.xlabel("Type")
plt.ylabel("Count")
plt.ylim(0, sample_df['type_label'].value_counts().max() + 100)  # Adding a buffer
plt.xticks(ticks=range(len(label_mapping)), labels=label_mapping.keys())  # Label x-axis with category names
plt.show()
# Step 7: Final Dataset Check
print("\nFinal Dataset Shape:", df.shape)
print("\nSample of Data After Cleaning and Preprocessing:\n", df.sample(5))
