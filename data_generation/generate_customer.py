from faker import Faker 
import pandas as pd 
import random 

fake = Faker()

customers = []

for i in range(10000):

    customers.append({
        "customer_id":f"CUST{i+1}",
        "customer_name":fake.name(),
        "city":fake.city(),
        "state":fake.state(),
        "email":fake.email(),
        "created_at":fake.date_time_between(start_date="-3y",end_date="now"),
        "updated_at":fake.date_time_between(start_date="-1y",end_date="now")

    })

df =pd.DataFrame(customers)
df.to_csv("customers.csv",index=False)

print("Customers Generated")
