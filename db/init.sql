DROP DATABASE IF EXISTS employees;
CREATE DATABASE employees;
USE employees;

CREATE TABLE employee_data (
 Employee_Name VARCHAR(50),
 Title VARCHAR(50)
);

INSERT INTO employee_data
 (Employee_Name, Title)
VALUES
 ('Kim Jojn', 'Manager'),
 ('Anjali Gupta', 'Engineer');
