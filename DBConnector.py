import psycopg2

# DB Credentials
conn = psycopg2.connect(
    host="localhost",
    database="interview_app_DB",
    user="postgres",
    password="Smoothhippo8",
)



# Cursor
cur = conn.cursor()


# Close connection
#conn.close()

