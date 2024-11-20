# Program to add and input 100 fake entries

import random
from faker import Faker
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Faker for generating random data
fake = Faker()

# Set up the MongoDB URI from environment variables
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["mydb"]  # Replace 'mydb' with your database name
users_collection = db["users"]

# Function to generate a random user entry
def generate_random_user():
    first_name = fake.first_name()
    middle_name = fake.first_name() if random.choice([True, False]) else None  # Randomly decide to include or not
    last_name = fake.last_name()
    dob = fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%d-%m-%Y")
    mobile = fake.phone_number()
    short_address = fake.address().splitlines()[0]  # Taking only the first line of the address
    city = fake.city()

    # Create a dictionary to represent the user entry
    user = {
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name,
        "dob": dob,
        "mobile": mobile,
        "address": short_address,
        "city": city
    }
    
    # Convert dictionary keys to a list and randomly omit some fields
    fields_to_remove = random.sample(list(user.keys()), random.randint(0, len(user)//2))  # Random number of fields to omit
    for field in fields_to_remove:
        user.pop(field, None)

    return user

# Generate and insert 100 dummy users into MongoDB
def insert_dummy_data(num_entries=100):
    for _ in range(num_entries):
        user = generate_random_user()
        users_collection.insert_one(user)

    print(f"Successfully inserted {num_entries} dummy user entries into MongoDB.")

if __name__ == "__main__":
    # Insert 100 dummy users
    insert_dummy_data(100)
