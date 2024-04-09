import mysql.connector

# Function to establish connection to MySQL database
def connect_to_database():
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'employees'
    }
    connection = mysql.connector.connect(**config)
    return connection

# Function to create a new employee record
def create_employee(employee_name, title):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO employee_data (Employee_Name, Title) VALUES (%s, %s)", (employee_name, title))
    connection.commit()
    cursor.close()
    connection.close()

# Function to read all employee data
def read_employee_data():
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT Employee_Name, Title FROM employee_data')
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

# Function to update an employee record
def update_employee(employee_name, new_title):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("UPDATE employee_data SET Title = %s WHERE Employee_Name = %s", (new_title, employee_name))
    connection.commit()
    cursor.close()
    connection.close()

# Function to delete an employee record
def delete_employee(employee_name):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM employee_data WHERE Employee_Name = %s", (employee_name,))
    connection.commit()
    cursor.close()
    connection.close()