import pandas as pd
import numpy as np

# Load the first 10000 rows to quickly check columns and values
df = pd.read_csv('jan to may police violation_anonymized791b166.csv', nrows=100)
print("Columns:")
print(df.columns)
print("Sample row:")
print(df.iloc[0])
