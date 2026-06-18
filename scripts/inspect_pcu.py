import pandas as pd

df = pd.read_csv('jan to may police violation_anonymized791b166.csv')

def get_pcu(vtype):
    v = str(vtype).upper()
    if v in ['SCOOTER', 'MOTOR CYCLE', 'MOPED']:
        return 0.5
    elif v in ['CAR', 'PASSENGER AUTO', 'GOODS AUTO', 'JEEP']:
        return 1.0
    elif v in ['MAXI-CAB', 'LGV', 'VAN', 'TEMPO', 'MINI LORRY']:
        return 1.5
    elif v in ['PRIVATE BUS', 'BUS (BMTC/KSRTC)', 'HGV', 'LORRY/GOODS VEHICLE', 'TOURIST BUS', 'SCHOOL VEHICLE', 'TANKER', 'FACTORY BUS', 'TRACTOR']:
        return 3.0
    else:
        return 1.0 # default for OTHERS and nan

df['pcu'] = df['vehicle_type'].apply(get_pcu)
print("PCU sums by vehicle_type:")
print(df.groupby('vehicle_type')['pcu'].sum())
print("\nTotal PCU sum:", df['pcu'].sum())
