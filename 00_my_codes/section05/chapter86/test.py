import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"

# Executing the query in sqlite
cursor.execute(create_table)

# Inserting values to the table.
user = (1, "jose", "asdf")
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

users = [
    (2, "rolf", "asdf"),
    (3, "anne", "xyz")
]
# This will execute each element of the list from the insert query.
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

# We need to tell the database to save the operation into the database.
connection.commit()

# This will close the connection from the database.
connection.close()