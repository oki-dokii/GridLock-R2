import pandas as pd
import json

df = pd.read_csv('jan to may police violation_anonymized791b166.csv')

print("Unique Vehicle Types:")
print(df['vehicle_type'].unique())
print("\nUnique Updated Vehicle Types:")
print(df['updated_vehicle_type'].unique())

print("\nUnique Violation Types:")
# Since violation_type is stored as a list-like string, let's parse it
all_violation_types = set()
for v in df['violation_type'].dropna().unique():
    try:
        v_list = json.loads(v.replace("'", '"'))
        for val in v_list:
            all_violation_types.add(val)
    except Exception as e:
        all_violation_types.add(v)

print(sorted(list(all_violation_types)))
