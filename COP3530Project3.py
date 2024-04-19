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

# Function to execute SQL queries. It takes an SQL string and optional parameters.
def execute_query(sql, params=None):
    cursor.execute(sql, params or {})  # Execute the SQL with or without parameters.
    columns = [col[0] for col in cursor.description]  # Extract column names from the query result.
    data = pd.DataFrame(cursor.fetchall(), columns=columns)  # Convert the query result into a DataFrame.
    return data

# Function to calculate closeness
def calculate_closeness(vehicle, input_data):
    weights = {
        'price': 0.4,
        'miles': 0.3,
        'year': 0.2,
        'make': 0.1,
        'model': 0.05
    }
    
    closeness_score = 0
    closeness_score += weights['price'] * (1 - abs(vehicle['PRICE'] - input_data['price']) / input_data['price'])
    closeness_score += weights['miles'] * (1 - abs(vehicle['ODOMETER'] - input_data['miles']) / input_data['miles'])
    closeness_score += weights['year'] * (1 - abs(vehicle['YEAR'] - input_data['year']) / input_data['year'])
    closeness_score += weights['make'] * (vehicle['MAKE'].lower() == input_data['make'].lower())
    closeness_score += weights['model'] * (vehicle['MODEL'].lower() == input_data['model'].lower())
    
    return closeness_score

# Function to get the closest vehicle match from the Oracle database
def get_closest_vehicle(input_data):
    # SQL query to fetch all vehicles from the 'cars' table.
    sql = "SELECT * FROM cars"
    df = execute_query(sql)
    
    df['closeness'] = df.apply(lambda vehicle: calculate_closeness(vehicle, input_data), axis=1)
    closest_vehicle = df.loc[df['closeness'].idxmax()]
    return closest_vehicle

# Example user input
make = input('Enter car make: ')
model = input('Enter car model: ')
year = int(input('Enter car year: '))
miles = int(input('Enter car mileage: '))
price = int(input('Enter price: '))

# Create a dictionary of user input data
user_input = {
    'make': make,
    'model': model,
    'year': year,
    'miles': miles,
    'price': price
}

# Get the closest vehicle match based on user input
closest_vehicle = get_closest_vehicle(user_input)
print(closest_vehicle)

# Close the cursor and connection when done
cursor.close()
connection.close()