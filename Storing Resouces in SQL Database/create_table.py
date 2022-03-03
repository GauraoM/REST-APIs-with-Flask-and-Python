import sqlite3

# Connect to the sqlite3 databases
connection = sqlite3.connect('data.db')

# Run the query and store the result
cursor = connection.cursor()

# Create table of columns
# For auto incrementing id write "INTEGER PRIMARY KEY"
create_table = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items(name text PRIMARY KEY, price real)"
cursor.execute(create_table)

# save the changes made
connection.commit()
# Close the connection
connection.close()