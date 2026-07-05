import pandas as pd 
import random 
import logging
from faker import Faker 
from pathlib import Path 

faker = Faker()
#----------------------- Configuration-------------------------
NUM_PRODUCTS = 5000
OUTPUT_DIR = "data/products"
OUTPUT_FILE = "product.csv"
RANDOM_SEED = 42

#-----------------------LOGGING ---------------------------------
Path(OUTPUT_DIR).mkdir(parents=True,exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(f"{OUTPUT_DIR}/product_generation.log"),
        logging.StreamHandler()
    ]
)

logger =logging.getLogger(__name__)

#-------------------------------FAKER  SETUP --------------------------------
random.seed(RANDOM_SEED)

CATEGORIES =[
    "Electronics",
    "clothing",
    "Books",
    "Home Appliances",
    "Sports",
    "Furniture"
]

PRODUCT_PREFIX = {
    "Electronics":["Laptop","Phone","Headphone","Tablet"],
    "clothing":["Tshirt","Jeans","Jacket","Shoes"],
    "Books":["Pyhton","SQL","Spark","Hadoop"],
    "Home Appliances":["Microwave","Mixer","AC","Fridge"],
    "Sports":["Bat","Ball","Shoes","Racket"],
    "Furniture":["Chair","Table","Desk","Sofa"]
    }

def generate_product_name(category):
    prefix = random.choice(PRODUCT_PREFIX[category])
    return f"{prefix}{random.randint(100,999)}"

def generate_products(num_products):
    logger.info("starting Product Generation")

    products= []
    try:

        for i in range(1,num_products + 1):
            category = random.choice(CATEGORIES)

            product ={
                "product_id":f"p{i:06}",
                "product_name":generate_product_name(category),
                "category":category,
                "price":round(random.uniform(100,50000),2),
                "created_at": faker.date_time_between(start_date="-2y",end_date="-1y"),
                "updated_at": faker.date_time_between(start_date="-1y",end_date="now")
            }
            products.append(product)
        
        logger.info(f"Generated {len(products)} products")

        return pd.DataFrame(products)
       
    except Exception as e:
        logger.error(f"Generation Failed{str(e)}")
        raise

def validate_products(df):

    logger.info("Running Validating Checks")

    if df["product_id"].duplicated().sum() > 0:
        raise ValueError("Duplicates product_id Detected")
    if df["product_id"].isnull().sum() > 0:
        raise ValueError("Null product_id is Detected")
    if (df['price'] <= 0 ).sum() > 0:
        raise ValueError("Invalid Price Detected")
    logger.info("Validation Passed")
def save_product(df):
    output_path = f"{OUTPUT_DIR}/{OUTPUT_FILE}"

    try:
        df.to_csv(output_path,index=False)

        logger.info(f"FIle Saved Successfully: {output_path}")

    except Exception as e:
        logger.exception(f"File save Falied: {e}")

        raise

def main():
    try:
        df=generate_products(NUM_PRODUCTS)
       
        validate_products(df)

        save_product(df)

        logger.info(f"Process Cpmpleted Successfully")
    except Exception as e:
        logger.exception(f"Pipeline Failed :{e}")
    
if __name__ == "__main__":
    main()
    