import psycopg2

connection = psycopg2.connect(
    host = 'localhost',
    user = 'postgres',
    password = '1234'
)

# Disable transaction
connection.autocommit = True

# Create a cursor object
cursor = connection.cursor()

# Create the database
cursor.execute("CREATE DATABASE w9new")


# Close the cursor and connection
cursor.close()
connection.close()

print('All Done!')