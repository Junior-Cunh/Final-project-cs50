import pandas as pd
from sqlalchemy import create_engine
from models import db, Component
from sqlalchemy.orm import sessionmaker

csv_file = "Components data.csv"

engine = create_engine("sqlite:///components.db")

db.metadata.create_all(engine)

df = pd.read_csv("Components data.csv", sep=";", na_values=["none", "None", "NONE"])

df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Creating session
Session = sessionmaker(bind=engine)
session = Session()

# Insert data
for _, row in df.iterrows():
    component = Component(
        name=row['name'],
        category=row['category'],
        current_min=float(row['current_min']) if not pd.isna(row['current_min']) else None,
        current_max=float(row['current_max']) if not pd.isna(row['current_max']) else None,
        voltage_min=float(row['voltage_min']) if not pd.isna(row['voltage_min']) else None,
        voltage_max=float(row['voltage_max']) if not pd.isna(row['voltage_max']) else None,
        power=float(row['power']) if not pd.isna(row['power']) else None,
        capacitance_min=row['capacitance_min'] if not pd.isna(row['capacitance_min']) else None,
        capacitance_max=row['capacitance_max'] if not pd.isna(row['capacitance_max']) else None,
        tolerance=row['tolerance'] if not pd.isna(row['tolerance']) else None,
        datasheet_link=row['datasheet_link'],
        notes=row['notes']
    )
    session.add(component)

session.commit()
session.close()

print("Dados importados com sucesso!")
