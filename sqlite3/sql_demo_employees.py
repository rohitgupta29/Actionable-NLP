# Set connection
# If used for testing, use memory as db
# curson to execute sql commands
# execute() to execute commands
#


import sqlite3
from employee import Employee

#connection object

# conn = sqlite3.connect('employee.db')

# If we want database that runs on RAM. It helps get fresh clean database everytime.Good for testing things.
conn = sqlite3.connect(':memory:')

#cursor to execute sql commands
c = conn.cursor()

# now we can execute sql commands using execute() method.
# sql command in doc strings
c.execute("""CREATE TABLE IF NOT EXISTS employees (
            first TEXT,
            last TEXT,
            pay INTEGER)""")

def insert_emp(emp):

    with conn:
        c.execute("INSERT INTO employees VALUES (:first,:last,:pay)", {'first': emp.first, 'last': emp.last, 'pay': emp.pay})

def get_emps_by_name (lastname):
    c.execute("SELECT * FROM employees WHERE last = :last", {'last': lastname})
    return c.fetchall()

def update_pay(emp,pay):
    with conn:
        c.execute("""UPDATE employees SET pay = :pay 
                    WHERE first = :first AND last = :last""",
                  {'first':emp.first,'last':emp.last,'pay':pay})

def remove_emp (emp):
    with conn:
        c.execute("""DELETE from employees WHERE first = :first AND last = :last""",
                    {'first': emp.first, 'last': emp.last, 'pay': emp.pay})

emp_1 = Employee('John','Doe', 80000)
emp_2 = Employee('Jane', 'Doe', 90000)


insert_emp(emp_1)
insert_emp(emp_2)

emps = get_emps_by_name('Doe')
print(emps)

update_pay(emp_2,95000)
remove_emp(emp_1)

emps = get_emps_by_name('Doe')
print(emps)

conn.close()
