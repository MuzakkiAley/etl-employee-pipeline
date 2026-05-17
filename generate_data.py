import pandas as pd
from faker import Faker
import random

fake = Faker('id_ID')

departments = ['Engineering', 'Marketing', 'Finance', 'HR', 'Operations']
statuses = ['Active', 'Active', 'Active', 'Inactive', 'Active']  # weighted active

def generate_employees(n=200):
    data = []
    for i in range(n):
        # Intentionally add some dirty data for ETL to clean
        salary = random.choice([
            random.randint(4000000, 20000000),
            None,        # missing value
            'N/A',       # string error
            random.randint(4000000, 20000000)
        ])

        join_date = random.choice([
            fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d'),
            fake.date_between(start_date='-5y', end_date='today').strftime('%d/%m/%Y'),  # wrong format
            None
        ])

        data.append({
            'employee_id': f'EMP{str(i+1).zfill(4)}',
            'name': fake.name(),
            'email': fake.email() if random.random() > 0.05 else None,
            'department': random.choice(departments),
            'salary': salary,
            'join_date': join_date,
            'status': random.choice(statuses),
            'phone': fake.phone_number()
        })

    # Add some duplicate rows
    duplicates = random.sample(data, 10)
    data.extend(duplicates)

    return pd.DataFrame(data)

if __name__ == '__main__':
    df = generate_employees(200)
    df.to_csv('employees_raw.csv', index=False)
    print(f"Generated {len(df)} rows (including duplicates) -> employees_raw.csv")
    print(f"Sample data:\n{df.head()}")