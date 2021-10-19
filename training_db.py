import psycopg2
from config import host, user, password, db_name

try:

    connection = psycopg2.connect(host=host,
                                  user=user,
                                  password=password,
                                  database=db_name)
    connection.autocommit=True
    cursor = connection.cursor()
    cursor.execute(
        """SELECT EXISTS (SELECT 1 FROM users WHERE user_id=12345);""")


    if not cursor.fetchone()[0]:
        cursor.execute("""INSERT INTO users VALUES (12345,)""")


    print("ff")
except Exception as e:
    print(e)
    print('Error while working with PostgresSQL', e)
else:
    if connection:
        connection.close()
        cursor.close()
        print('PostgresSQL connection closed')
