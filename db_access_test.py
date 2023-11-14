import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="weirdo",
    database="timetracker"
    )

mycursor = db.cursor()


get_time = "SELECT time_spent FROM Time WHERE time_start LIKE %s"
add_time = "SELECT SUM(time_spent) FROM Time WHERE program_name LIKE %s AND time_start LIKE %s"

var = "2023" + "%"
"""mycursor.execute(get_time, (var,))
results = mycursor.fetchall()

for result in results:
    #Do something with the result
    print(result)
"""
var2 = "%" + "1" + "%"
mycursor.execute(add_time, (var2, var))
summe = mycursor.fetchall()[0][0]
print(summe) 
