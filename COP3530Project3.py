# Import necessary libraries for database connection, data manipulation, and plotting.
import cx_Oracle
import pandas as pd
import matplotlib.pyplot as plt

# Setting up the database connection details.
username = 'greeneryan'
password = 'v51VjDsYBoITgSY0FBrv18sg'
dsn = 'oracle.cise.ufl.edu/orcl'
connection = cx_Oracle.connect(username, password, dsn)
cursor = connection.cursor()

# Function to execute SQL queries.
def execute_query(sql, params=None):
    cursor.execute(sql, params or {})  
    columns = [col[0] for col in cursor.description]  
    data = pd.DataFrame(cursor.fetchall(), columns=columns)  
    return data

# Retrieve data from the database
car_data_df = execute_query("SELECT * FROM Cars")

# Binary Search Tree implementation
class BSTNode:
    def __init__(self, key, data):
        self.left = None
        self.right = None
        self.key = key
        self.data = data

    def insert(self, key, data):
        if key < self.key:
            if self.left is None:
                self.left = BSTNode(key, data)
            else:
                self.left.insert(key, data)
        else:
            if self.right is None:
                self.right = BSTNode(key, data)
            else:
                self.right.insert(key, data)

    def search(self, key):
        if key == self.key:
            return self.data
        elif key < self.key and self.left:
            return self.left.search(key)
        elif key > self.key and self.right:
            return self.right.search(key)
        else:
            return None

def build_bst_from_df(df):
    root = BSTNode(df.iloc[0]['ID'], df.iloc[0])
    for _, row in df.iterrows():
        root.insert(row['ID'], row)
    return root

bst_root = build_bst_from_df(car_data_df)

# Function to calculate closeness based on weights
def calculate_closeness(input_car, target_car):
    weights = {'Make': 0.2, 'Model': 0.2, 'Year': 0.15, 'Color': 0.1, 'Mileage': 0.2, 'Price': 0.15}
    score = 0
    for key in weights:
        if input_car[key] == target_car[key]:
            score += weights[key]
    return score

# User interaction to choose data structure for car search
def user_interaction():
    choice = input("Choose search method (1 for BST based on ID, 2 for hash table based on attributes): ")
    if choice == '1':
        search_id = int(input("Enter car ID: "))
        result = bst_root.search(search_id)
        if result is not None:
            print("Here is your car!")
            print(f"ID: {result['ID']}, MAKE: {result['Make']}, MODEL: {result['Model']}, YEAR: {result['Year']}, COLOR: {result['Color']}, MILEAGE: {result['Mileage']}, PRICE: {result['Price']}")
        else:
            print("Car not found.")
    elif choice == '2':
        make = input("Enter Make: ")
        model = input("Enter Model: ")
        year = input("Enter Year: ")
        color = input("Enter Color: ")
        mileage = float(input("Enter Mileage: "))
        price = float(input("Enter Price: "))
        input_car = {'Make': make, 'Model': model, 'Year': year, 'Color': color, 'Mileage': mileage, 'Price': price}
        closest_car, highest_score = None, 0
        for _, car in car_data_df.iterrows():
            score = calculate_closeness(input_car, car)
            if score > highest_score:
                highest_score = score
                closest_car = car
        if closest_car is not None:
            print("Here is the closest car to your preferences!")
            print(f"ID: {closest_car['ID']}, MAKE: {closest_car['Make']}, MODEL: {closest_car['Model']}, YEAR: {closest_car['Year']}, COLOR: {closest_car['Color']}, MILEAGE: {closest_car['Mileage']}, PRICE: {closest_car['Price']}")
        else:
            print("No matching car found.")

user_interaction()