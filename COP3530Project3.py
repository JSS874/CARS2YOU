import cx_Oracle
import pandas as pd
import matplotlib.pyplot as plt
import sys
import time
import heapq

# Increase the recursion limit, default is 1000
sys.setrecursionlimit(1500)

# Database connection setup, CISE oracle
username = 'greeneryan'
password = 'v51VjDsYBoITgSY0FBrv18sg'
dsn = 'oracle.cise.ufl.edu/orcl'
connection = cx_Oracle.connect(username, password, dsn)
cursor = connection.cursor()

def execute_query(sql, params=None):
    cursor.execute(sql, params or {})
    columns = [col[0] for col in cursor.description]
    data = pd.DataFrame(cursor.fetchall(), columns=columns)
    return data

car_data_df = execute_query("SELECT * FROM Cars")

# Data structure 1: Skip List implementation using SortedDict
from sortedcontainers import SortedDict

class SkipList:
    def __init__(self):
        self.list = SortedDict()
    
    def insert(self, key, value):
        self.list[key] = value
    
    def search(self, key):
        return self.list.get(key, None)

skip_list = SkipList()
for index, row in car_data_df.iterrows():
    skip_list.insert(row['ID'], row)

# Define closeness calculation function
def calculate_closeness(input_car, car):
    weights = {'MAKE': 0.2, 'MODEL': 0.2, 'YEAR': 0.1, 'COLOR': 0.1, 'MILEAGE': 0.2, 'PRICE': 0.2}
    score = 0
    for key, weight in weights.items():
        if key in ['YEAR', 'MILEAGE', 'PRICE']:  # SQL numerical columns
            # Prevent scaling issues
            range_value = car_data_df[key].max() - car_data_df[key].min()
            normalized_diff = abs(input_car[key] - car[key]) / range_value if range_value else 0
            score += (1 - normalized_diff) * weight
        else:  # SQL categorical columns
            score += (input_car[key] == car[key]) * weight
    return score

# Data structure 2: Min-Heap for finding closest car based on closeness score
def find_closest_car(input_car, car_data_df):
    heap = []
    for _, car in car_data_df.iterrows():
        score = -calculate_closeness(input_car, car)  # Min-Heap using closeness calculation
        heapq.heappush(heap, (score, car))
    closest_car = heapq.heappop(heap)[1]
    return closest_car

# Implement user interaction
def user_interaction():
    choice = input("Choose search method (1 for Skip List based on ID, 2 for Min-Heap based on closeness): ")
    start_time = time.time()  # Start timing for execution time output
    
    if choice == '1':
        search_id = int(input("Enter CAR ID: "))
        result = skip_list.search(search_id)
        if result is not None:
            print("Here is your car!")
            for key in ['ID', 'MAKE', 'MODEL', 'YEAR', 'COLOR', 'MILEAGE', 'PRICE']:
                print(f"{key}: {result[key]}")
        else:
            print("Car not found.")
    elif choice == '2':
        input_car = {
            'MAKE': input("Enter MAKE: "),
            'MODEL': input("Enter MODEL: "),
            'YEAR': int(input("Enter YEAR: ")),
            'COLOR': input("Enter COLOR: "),
            'MILEAGE': float(input("Enter MILEAGE: ")),
            'PRICE': float(input("Enter PRICE: "))
        }
        closest_car = find_closest_car(input_car, car_data_df)
        print("Here is the closest car to your preferences!")
        for key in ['ID', 'MAKE', 'MODEL', 'YEAR', 'COLOR', 'MILEAGE', 'PRICE']:
            print(f"{key}: {closest_car[key]}")
    
    print(f"Execution time: {time.time() - start_time:.2f} seconds")

user_interaction()

cursor.close()  # Close the cursor.
connection.close()  # Close the connection to the database.