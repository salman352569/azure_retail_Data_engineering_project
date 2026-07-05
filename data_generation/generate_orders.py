import pandas as pd 
import logging
from faker import Faker 
from pathlib import Path
import random

NUM_ORDERS = 100000
NUM_CUSTOMERS = 10000

OUTPUT_DIR ="data/orders"
OUTPUT_FILE = "orders.csv"

random.seed(42)
fake = Faker()
Faker.seed(42)

Path(OUTPUT_DIR).mkdir(parents=True,exist_ok=True)

logging.basicConfig(
    level = logging.INFO,
    format ="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(f"{OUTPUT_DIR}/order_generation.log"),
        logging.StreamHandler()
    ]
)
logger =logging.getLogger(__name__)

CHANNELS=[
    "Online",
    "Mobile App",
    "Store"
]
STATUS= [
    "Completed",
    "Shipped",
    "Cancelled",
    "Returned"
]

def generate_orders():

    logger.info("Starting Order Generation")

    orders = []

    for i in range(1,NUM_ORDERS + 1):
        order ={
            "order_id": f"O{i:08}",
            "customer_id":f"CUST{random.randint(1,NUM_CUSTOMERS)}",
            "order_state": fake.date_between(start_date="-2y",end_date="today"),
            "channel": random.choice(CHANNELS),
            "status": random.choice(STATUS),
            "created_at": fake.date_time_between(start_date="-2y",end_date="-1y"),
            "updated_at":fake.date_time_between(start_date="-1y",end_date="now")

                  }
        orders.append(order)

    return pd.DataFrame(orders)

def validate_orders(df):

    if df["order_id"].duplicated().sum() > 0:
        raise ValueError("Duplicate order_id Detected")
    
    if df["order_id"].isnull().sum() > 0:
        raise ValueError("Null order_id Detected")
    
    logger.info("Validation passed")

def main():
    try:

        df = generate_orders()

        validate_orders(df)

        df.to_csv(f"{OUTPUT_DIR}/{OUTPUT_FILE}",index=False)

        logger.info(f"{len(df)} orders generated successfully")

    except Exception  as e:
        logger.exception("order generation Falied")
    
if __name__ == "__main__":
    main()


