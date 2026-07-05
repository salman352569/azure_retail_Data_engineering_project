import pandas as pd 
import logging
from faker import Faker 
from pathlib import Path
import random

NUM_ORDERS = 100000
NUM_PRODUCTS = 5000

OUTPUT_DIR = "data/order_items"
OUTPUT_FILE = "order_items.csv"

random.seed(42)
fake =Faker()

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(f"{OUTPUT_DIR}/order_items_generation.log"),
        logging.StreamHandler()
    ]
)
logger =logging.getLogger(__name__)

def generate_order_items():

    logger.info(f"Generating order items")

    items =[]
    item_id=1

    for order_num in range(1,NUM_ORDERS + 1):
        order_id =f"O{order_num:08}"

        product_count= random.randint(1,5)

        selected_products =random.sample(
            range(1,NUM_PRODUCTS + 1),
            product_count
)       
        for product_num in selected_products:

            quantity = random.randint(1,5)

            unit_price = round(
                random.uniform(100,50000),
                2
            )
            sales_amount = round(quantity * unit_price,2)

            items.append({
                "order_item_id":item_id,
                "order_id":order_id,
                "product_id":f"p{product_num:06}",
                "quantity":quantity,
                "sales_amount":sales_amount
            })
            item_id += 1

        
    return pd.DataFrame(items)
def validate_items(df):

    if df["order_item_id"].duplicated().sum() > 0:
        raise ValueError("Duplicate order items id is detected")
    if (df["sales_amount"] < 0).sum() > 0:
        raise ValueError("Negative Sales amount is found")
    
    logger.info("Validation passed")

def main():
    try:

        df = generate_order_items()

        validate_items(df)

        output_path =f"{OUTPUT_DIR}/{OUTPUT_FILE}"

        df.to_csv(output_path,index=False)

        logger.info(f"{len(df)} order items generated")

    except Exception as e:
        logger.exception("Order items generation failed")

if __name__ == "__main__":
    main()