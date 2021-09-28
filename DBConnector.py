import psycopg2

# DB Credentials
conn = psycopg2.connect(
    host="",
    database="",
    user="",
    password="",
)



# Cursor
cur = conn.cursor()


# Close connection
#conn.close()

