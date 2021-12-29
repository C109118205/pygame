import mariadb
import sys

try:
    conn = mariadb.connect(
        user="root",
        password="Skills39",
        host="mbeut.ml",
        port=3306,
        database="pygame_db"

    )
    print('DB connected OK')
except mariadb.Error as e:
    print(f"DB connected error: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()